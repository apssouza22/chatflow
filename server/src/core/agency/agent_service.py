from core.agency.agents import Task
from core.agency.command_agent import CommandAgent
from core.agency.dock_picker_agent import DocPickerAgent
from core.agency.json_extractor_agent import JSONExtractorAgent
from core.agency.long_memory_agent import LongMemoryAgent
from core.agency.question_answer_agent import QuestionAnswerAgent
from core.agency.user_intent_agent import UserIntentAgent
from core.docs_search.doc_service import DocService
from core.llm.llm_service import LLMService
from core.memory.chat_memory_service import ChatMemoryService


class AgentService:
    def __init__(self, llm: LLMService, doc_service: DocService, chat_memory: ChatMemoryService):
        self.chat_memory = chat_memory
        self.question_answer_agent = QuestionAnswerAgent("question-answer", llm, chat_memory)
        self.doc_service = doc_service
        self.llm = llm
        self.dock_picker_agent = DocPickerAgent("dock-picker", llm)
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_extractor_agent = JSONExtractorAgent("json-extractor", llm)
        self.long_term_memory_agent = LongMemoryAgent("long-term-memory", llm, chat_memory, self.json_extractor_agent)
        self.command_agent = CommandAgent("command", llm, "gpt-3", self.json_extractor_agent)

    def run_tasks(self, prompt: str) -> dict:
        username = "user1234"
        pipeline = TaskPipeline(self, prompt, username)
        pipeline.search_docs()
        pipeline.update_memory()
        pipeline.check_user_intent()
        pipeline.build_ui_resp()
        pipeline.update_short_memory()
        return pipeline.get_user_resp()


class TaskPipeline:
    def __init__(self, agent_service: AgentService, prompt: str, username: str):
        self.assistant_msg = None
        self.username = username
        self.prompt = prompt
        self.user_resp = None
        self.is_action = False
        self.doc = None
        self.agent_service = agent_service

    def search_docs(self):
        docs = self.agent_service.doc_service.search_docs("chat|demo", self.prompt)
        doc_task = self.agent_service.dock_picker_agent.process(Task(self.prompt, docs))
        self.doc = self.agent_service.dock_picker_agent.filter_doc(docs, doc_task.output.message)

    def update_memory(self):
        self.agent_service.long_term_memory_agent.process(Task(self.prompt, self.username))
        self.agent_service.chat_memory.update_short_memory(
            self.username,
            {"message": self.prompt, "role": "user", "context": self.doc.text}
        )

    def check_user_intent(self):
        task = self.agent_service.user_intent_agent.process(Task(self.prompt))
        self.is_action = self.agent_service.user_intent_agent.is_action(task)

    def build_ui_resp(self):
        if not self.is_action:
            resp = self.agent_service.question_answer_agent.process(Task(self.prompt, self.username))
            self.user_resp = resp.output.message
            self.assistant_msg = resp.output.message
            return

        resp = self.agent_service.command_agent.process(Task(self.prompt, self.doc.text))
        self.assistant_msg = resp.output.message
        self.user_resp = self.agent_service.command_agent.handle_response(resp)

    def update_short_memory(self):
        self.agent_service.chat_memory.update_short_memory(self.username, {"message": self.assistant_msg, "role": "assistant"})

    def get_user_resp(self):
        return self.user_resp


def agent_service_factory(llm: LLMService, doc_service: DocService, chat_memory: ChatMemoryService) -> AgentService:
    return AgentService(llm, doc_service, chat_memory)
