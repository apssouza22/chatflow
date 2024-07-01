from core.agency.agents import DefaultAgent, Task
from core.agency.command_agent import CommandAgent
from core.agency.command_func_agent import CommandFuncAgent
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
        # self.command_agent = CommandAgent("command", llm)
        self.command_agent = CommandFuncAgent("command", llm)
        self.doc_service = doc_service
        self.llm = llm
        self.dock_picker_agent = DocPickerAgent("dock-picker", llm)
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_extractor_agent = JSONExtractorAgent("json-extractor", llm)
        self.long_term_memory_agent = LongMemoryAgent("long-term-memory", llm, chat_memory, self.json_extractor_agent)

    def run_tasks(self, prompt: str) -> dict:
        username = "user1234"
        docs = self.doc_service.search_docs("chat|demo", prompt)
        doc_task = self.dock_picker_agent.process(Task(prompt, docs))
        doc = self.dock_picker_agent.filter_doc(docs, doc_task.output.message)
        task = self.user_intent_agent.process(Task(prompt))
        self.long_term_memory_agent.process(Task(prompt, username))
        self.chat_memory.update_short_memory(username, {"message": prompt, "role": "user", "context": doc.text})
        if not self.user_intent_agent.is_action(task):
            resp = self.question_answer_agent.process(Task(prompt, username))
            self.chat_memory.update_short_memory(username, {"message": resp.output.message, "role": "assistant"})
            return resp.output.message

        resp = self.command_agent.process(Task(prompt, doc.text))
        self.chat_memory.update_short_memory(username, {"message": resp.output.message, "role": "assistant"})
        if resp.output.tools:
            return self.command_agent.handle_response(resp)
        json_data = self.json_extractor_agent.process(Task(resp.output.message))
        return json_data.output.message


def agent_service_factory(llm: LLMService, doc_service: DocService, chat_memory: ChatMemoryService) -> AgentService:
    return AgentService(llm, doc_service, chat_memory)
