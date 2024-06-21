from core.llm.llm_service import LLMService


class AgentBase:

    def __init__(self, name, llm_service: LLMService):
        self.name = name
        self.llm_service = llm_service

    def infer(self, prompt: str):
        raise NotImplementedError


class DefaultAgent(AgentBase):

    def __init__(self, name, llm_service: LLMService):
        super().__init__(name, llm_service)
        self.system_prompt = "You are a helpful assistant."
        self.prompts = []

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def set_user_prompt(self, prompts: list[str]):
        for prompt in prompts:
            self.prompts.append({
                "role": "user",
                "content": prompt
            })

    def infer(self, prompt: str):
        self.prompts.insert(0, {
            "role": "system",
            "content": self.system_prompt
        })

        self.prompts.append({
            "role": "user",
            "content": prompt
        })


        return self.llm_service.infer(self.prompts)
