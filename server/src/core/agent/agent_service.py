import json

from pydantic import BaseModel

from core.common import conn
from core.agent.cache import PredictCache
from core.app.app_dao import App
from core.history.chat_history import ChatHistoryService, AddHistoryDto
from core.cost.cost_dao import Cost
from core.cost.cost_service import CostService
from core.agent.chat_response_handler import OpenAIResponseHandler
from core.llm.llm_service import LLMService, LLMResponse, Usage
from core.llm.prompt_handler import MessageCompletion, MessageRole
from core.user.user_dao import User


class UserInputDto(BaseModel):
    user: User
    context: str
    question: str
    is_plugin_mode: bool
    app: App
    session_id: str


class AgentService:

    def __init__(self, history: ChatHistoryService, cost_service: CostService, llm: LLMService, cache: PredictCache, ):
        self.predict_cache: PredictCache = cache
        self.history = history
        self.resp_handler = OpenAIResponseHandler(llm)
        self.cost_service = cost_service
        self.llm = llm

    def update_cost(self, usages: [Usage], user_email: str, app_key: str):
        for usage in usages:
            cost = Cost(**usage.dict())
            self.cost_service.put_cost(cost, user_email, app_key)

    async def handle_user_input(self, req: UserInputDto) -> dict:
        handler = GetPredictHandler(self, req)
        handler.update_history()
        handler.evaluate_type_query()
        handler.load_history()
        await handler.predict_response()
        handler.update_history()
        return handler.get_response()

    def user_history_process(self, req: UserInputDto) -> dict:
        add_message_dto = AddHistoryDto(
            user_email=req.user.email,
            app_key=req.app.app_key,
            session_id=req.session_id,
            message=MessageCompletion(
                role=MessageRole.USER,
                context=req.context,
                query=req.question
            )
        )
        self.history.add_message(add_message_dto)
        return self._get_user_history(req)

    def _get_user_history(self, req):
        user_history = self.history.get_history(req.session_id)
        if user_history is None:
            user_history = []
        return user_history


class GetPredictHandler:

    def __init__(self, agent: AgentService, req: UserInputDto):
        self.req = req
        self.message: str = ""
        self.user_history = None
        self.is_action = True
        self.agent: AgentService = agent
        self.cache: PredictCache = agent.predict_cache
        self.history: ChatHistoryService = agent.history
        self.cost_service: CostService = agent.cost_service
        self.llm: LLMService = agent.llm

    def update_history(self):
        current_user = self.req.user
        item = AddHistoryDto(
            user_email=current_user.email,
            app_key=self.req.app.app_key,
            session_id=self.req.session_id,
            message=MessageCompletion(
                role=MessageRole.ASSISTANT,
                response=self.message
            )
        )
        if self.message:
            self.history.add_message(item)
            return

        item.message = MessageCompletion(
            role=MessageRole.USER,
            context=self.req.context,
            query=self.req.question
        )

        self.history.add_message(item)

    def evaluate_type_query(self):
        if self.req.question.startswith('++'):
            return True
        if self.req.question.endswith('?'):
            return False
        if "#action" not in self.req.context:
            return False
        if "#action" in self.req.context and "#text" not in self.req.context:
            return True
        text_form = self.llm.get_text_or_form(self.req.question)
        self.agent.update_cost(text_form.usage, self.req.user.email, self.req.app.app_key)
        self.is_action = text_form.message.lower() == "form"

    def load_history(self):
        self.user_history = self.history.get_history(self.req.session_id)
        if self.user_history is None:
            self.user_history = []

    async def predict_response(self):
        if await self.cache.exists(self.req.question):
            self.message = await self.cache.get(self.req.question)
            return
        else:
            llm_resp = self._get_llm_response()
            self.message = llm_resp.message
            self.agent.update_cost(llm_resp.usage, self.req.user.email, self.req.app.app_key)
            await self.cache.put(self.req.question, self.message)

    def _get_llm_response(self) -> LLMResponse:
        if self.is_action:
            return self.llm.get_task_command(self.user_history, app=self.req.app)
        return self.llm.get_question_answer(self.req.question, self.req.app, self.user_history)

    def get_response(self):
        if self.is_action:
            commands = self.agent.resp_handler.extract_json_schema(self.message)
            if type(commands) is not dict:
                commands = json.loads(commands)
            return commands

        return {
            "type": "question",
            "thoughts": {
                "answer": self.message,
            }
        }


def agent_factory(chat_history: ChatHistoryService, cost_service: CostService, llm: LLMService):
    return AgentService(
        chat_history,
        cost_service,
        llm,
        PredictCache(conn.get_redis_instance())
    )
