import json

from pydantic import BaseModel

from core.common import conn
from core.agent.cache import PredictCache
from core.app.app_dao import App
from core.history.chat_history import ChatHistoryService, AddMessageDto
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

    def __init__(self, history: ChatHistoryService, cost_service: CostService, llm: LLMService, cache: PredictCache):
        self.cache = cache
        self.history = history
        self.resp_handler = OpenAIResponseHandler(llm)
        self.cost_service = cost_service
        self.llm = llm

    def update_cost(self, usages: [Usage], user_email: str, app_key: str):
        for usage in usages:
            cost = Cost(**usage.dict())
            self.cost_service.put_cost(cost, user_email, app_key)

    def is_action(self, req: UserInputDto) -> bool:
        if req.question.startswith('++'):
            return True
        if req.question.endswith('?'):
            return False
        if "#action" not in req.context:
            return False
        if "#action" in req.context and "#text" not in req.context:
            return True
        text_form = self.llm.get_text_or_form(req.question)
        self.update_cost(text_form.usage, req.user.email, req.app.app_key)
        return text_form.message.lower() == "form"

    async def handle_user_input(self, req: UserInputDto) -> dict:
        current_user = req.user
        add_message_dto = AddMessageDto(
            user_email=current_user.email,
            app_key=req.app.app_key,
            session_id=req.session_id,
            message=MessageCompletion(
                role=MessageRole.USER,
                context=req.context,
                query=req.question
            )
        )
        await self.history.add_message(add_message_dto)
        is_action = self.is_action(req)

        # TODO: Eliminate `cache.exists` call:
        if await self.cache.exists(req.question):
            message = await self.cache.get(req.question)
        else:
            llm_resp = await self._get_llm_response(req, is_action)
            message = llm_resp.message
            self.update_cost(llm_resp.usage, current_user.email, req.app.app_key)
            await self.cache.put(req.question, llm_resp.message)
            message = llm_resp.message

        add_message_dto = AddMessageDto(
            user_email=current_user.email,
            app_key=req.app.app_key,
            session_id=req.session_id,
            message=MessageCompletion(
                role=MessageRole.ASSISTANT,
                response=message
            )
        )
        await self.history.add_message(add_message_dto)

        if is_action:
            commands = self.resp_handler.extract_json_schema(message)
            if type(commands) is not dict:
                commands = json.loads(commands)
            return commands

        return self.create_user_resp_obj(message)

    def user_history_process(self, req: UserInputDto) -> dict:
        add_message_dto = AddMessageDto(
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


    def create_user_resp_obj(self, message: str):
        return {
            "type": "question",
            "thoughts": {
                "answer": message,
            }
        }

    async def _get_llm_response(self, req: UserInputDto, is_action) -> LLMResponse:
        user_history = self._get_user_history(req)
        if is_action:
            return self.llm.get_task_command(user_history, app=req.app)
        return self.llm.get_question_answer(req.question, req.app, user_history)

    def _get_user_history(self, req):
        user_history = await self.history.get_history(req.session_id)
        if user_history is None:
            user_history = []
        return user_history


def agent_factory(chat_history: ChatHistoryService, cost_service: CostService, llm: LLMService):
    return AgentService(
        chat_history,
        cost_service,
        llm,
        PredictCache(conn.get_redis_instance())
    )
