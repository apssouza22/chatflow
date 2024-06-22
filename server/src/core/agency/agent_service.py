from core.agency.agents import DefaultAgent, Task
from core.agency.command_agent import CommandAgent
from core.agency.dock_picker_agent import DocPickerAgent
from core.agency.json_extractor_agent import JSONExtractorAgent
from core.agency.question_answer_agent import QuestionAnswerAgent
from core.agency.user_intent_agent import UserIntentAgent
from core.docs_search.doc_service import DocService
from core.llm.llm_service import LLMService


class AgentService:
    def __init__(self, llm: LLMService, doc_service: DocService):
        self.question_answer_agent = QuestionAnswerAgent("question-answer", llm)
        self.command_agent = CommandAgent("command", llm)
        self.doc_service = doc_service
        self.llm = llm
        self.dock_picker_agent = DocPickerAgent("dock-picker", llm)
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_extractor_agent = JSONExtractorAgent("json-extractor", llm)

    def run_tasks(self, prompt: str) -> dict:
        docs = self.doc_service.search_docs("chat|demo", prompt)
        doc_task = self.dock_picker_agent.process(Task(prompt, docs))
        doc = self.dock_picker_agent.filter_doc(docs, doc_task.output.message)
        task = self.user_intent_agent.process(Task(prompt))
        if self.user_intent_agent.is_action(task):
            resp = self.command_agent.process(Task(prompt, doc.text))
            json_data = self.json_extractor_agent.process(Task(resp.output.message))
            return json_data.output.message

        resp = self.question_answer_agent.process(Task(prompt, doc.text))
        return resp.output.message


def agent_service_factory(llm: LLMService, doc_service: DocService) -> AgentService:
    return AgentService(llm, doc_service)
