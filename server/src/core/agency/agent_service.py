from core.agency.agents import DefaultAgent, Task
from core.agency.doc_picker_agent import DocPickerAgent
from core.agency.user_intent_agent import UserIntentAgent, JSONFixerAgent
from core.docs_search.doc_service import DocService
from core.llm.llm_service import LLMService


class AgentService:
    def __init__(self, llm: LLMService, doc_service: DocService):
        self.doc_service = doc_service
        self.llm = llm
        self.dock_picker_agent = DocPickerAgent("doc-picker", llm)
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_fixer_agent = JSONFixerAgent("json-fixer", llm)
        self.json_extractor_agent = DefaultAgent("json-extractor", llm)
        self.json_extractor_agent.set_system_prompt("You are a Json extractor, and your job is to extract valid JSON from a text.")

    def run_tasks(self, txt_input: str) -> dict:
        docs = self.doc_service.search_docs("chat", txt_input)
        doc_pick_resp = self.dock_picker_agent.process(Task(txt_input, docs))
        return doc_pick_resp

        # resp = self.user_intent_agent.process(Task(txt_input, doc_pick_resp.message))
        # content = resp.message.replace("}", "}}")
        # fixed_json = self.json_fixer_agent.process(Task(content))
        # return self.json_extractor_agent.process(Task("This is a text with JSON, ensure you return only JSON object" + fixed_json.message))


def agent_service_factory(llm: LLMService, doc_service: DocService) -> AgentService:
    return AgentService(llm, doc_service)
