from core.agency.agents import AgentBase, Task


class UserIntentAgent(AgentBase):

    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)

    def process(self, task: Task):
        return self.llm_service.infer([
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": task.input
            }
        ])


class JSONFixerAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)

    def process(self, task: Task):
        return self.llm_service.infer([
            {
                "role": "system",
                "content": "You are a JSONFixer. You are a bot that helps users fix their JSON responses."
            },
            {
                "role": "user",
                "content": "This is a JSON response: " + task.input
            }
        ])
