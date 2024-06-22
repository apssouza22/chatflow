from core.agency.agents import AgentBase, Task


class UserIntentAgent(AgentBase):

    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = """You are an AI responsible for identifying users intent.  Your goal is to analyze the user input and determine if the user requires either text or form as the response \n
If the user input is understood as a question automatically, the response should be a "text". Example: explain me how to add a new address;  tell me what to do; how much does it cost? \n
If the user input is understood as a greeting, the response should be "text".   Example:  How are you; Hi; Oi; Como você está? \n
If the input requires an action, the response should be "form". Example: help me to send an email; book me a class; add a new address;  calculate the distance; help me to buy it \n
If you are unsure about the answer say "text" \n
VERY IMPORTANT: Respond with either "text" or "form".
"""

    def process(self, task: Task) -> Task:
        resp = self.llm_service.infer_using_pro([
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": "This is a user input: " + task.input
            }
        ])
        task.set_output(resp)
        return task


class JSONFixerAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)

    def process(self, task: Task):
        return self.llm_service.infer_using_basic([
            {
                "role": "system",
                "content": "You are a JSONFixer. You are a bot that helps users fix their JSON responses."
            },
            {
                "role": "user",
                "content": "This is a JSON response: " + task.input
            }
        ])
