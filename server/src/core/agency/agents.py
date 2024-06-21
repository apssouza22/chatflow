from typing import Any

from core.llm.llm_service import LLMService


class Task:
    def __init__(self, txt_input: str, context: Any = None):
        self.context = context
        self.input = txt_input
        self.output = None

    def set_output(self, output):
        self.output = output


class AgentBase:

    def __init__(self, name, llm_service: LLMService):
        self.name = name
        self.llm_service = llm_service

    def process(self, task: Task):
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

    def process(self, task: Task):
        self.prompts.insert(0, {
            "role": "system",
            "content": self.system_prompt
        })

        if task.context:
            self.prompts.append({
                "role": "user",
                "content": f'Context: {task.context}'
            })

        self.prompts.append({
            "role": "user",
            "content": task.input
        })

        infer = self.llm_service.infer(self.prompts)
        task.set_output(infer)
        return task
