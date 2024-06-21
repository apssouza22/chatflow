from core.agency.agents import DefaultAgent, Task
from core.agency.dock_picker_agent import DocPickerAgent
from core.agency.user_intent_agent import UserIntentAgent, JSONFixerAgent
from core.docs_search.doc_service import DocService
from core.llm.llm_service import LLMService


class AgentService:
    def __init__(self, llm: LLMService, doc_service: DocService):
        self.doc_service = doc_service
        self.llm = llm
        self.dock_picker_agent = DocPickerAgent("dock-picker", llm)
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_fixer_agent = JSONFixerAgent("json-fixer", llm)
        self.json_extractor_agent = DefaultAgent("json-extractor", llm)
        self.json_extractor_agent.set_system_prompt("You are a Json extractor, and your job is to extract valid JSON from a text.")

    def run_tasks(self, prompt: str) -> dict:
        docs = self.doc_service.search_docs("chat|demo", prompt)
        doc_task = self.dock_picker_agent.process(Task(prompt, docs))
        task = self.user_intent_agent.process(Task(prompt))
        return task.output

        # docs = self.user_intent_agent.process(Task(prompt))
        # content = docs["choices"][0]["message"]["content"].replace("}", "}}")
        # fixed_json = self.json_fixer_agent.infer(content)
        # text_with_json = fixed_json["choices"][0]["message"]["content"]
        # return self.json_extractor_agent.infer("This is a text with JSON, ensure you return only JSON object" + text_with_json)


def agent_service_factory(llm: LLMService, doc_service: DocService) -> AgentService:
    return AgentService(llm, doc_service)
