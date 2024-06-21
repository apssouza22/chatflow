from core.agency.agents import DefaultAgent
from core.agency.user_intent_agent import UserIntentAgent, JSONFixerAgent
from core.llm.llm_service import LLMService


class AgentService:
    def __init__(self, llm: LLMService):
        self.llm = llm
        self.user_intent_agent = UserIntentAgent("user-intent", llm)
        self.json_fixer_agent = JSONFixerAgent("json-fixer", llm)
        self.json_extractor_agent = DefaultAgent("json-extractor", llm)
        self.json_extractor_agent.set_system_prompt("You are a Json extractor, and your job is to extract valid JSON from a text.")

    def run_tasks(self, prompt: str) -> dict:
        resp = self.user_intent_agent.infer(prompt)
        content = resp["choices"][0]["message"]["content"].replace("}", "}}")
        fixed_json = self.json_fixer_agent.infer(content)
        text_with_json = fixed_json["choices"][0]["message"]["content"]
        return self.json_extractor_agent.infer("This is a text with JSON, ensure you return only JSON object" + text_with_json)


def agent_service_factory(llm: LLMService) -> AgentService:
    return AgentService(llm)
