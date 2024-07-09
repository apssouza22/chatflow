import json
import time

from core.agency.agents import AgentBase, Task
from core.agency.command_func_agent import CommandFuncAgent
from core.agency.command_prompt_agent import CommandPromptAgent


class CommandAgent(AgentBase):
    def __init__(self, name, llm_service, model, json_extractor_agent):
        super().__init__(name, llm_service)
        self.json_extractor_agent = json_extractor_agent
        self.model = model
        if model.startswith("gpt-3"):
            self.command_agent = CommandPromptAgent(name, llm_service)
        else:
            self.command_agent = CommandFuncAgent(name, llm_service)

    def process(self, task: Task) -> Task:
        resp = self.command_agent.process(Task(task.input, task.context))
        task.set_output(resp.output)
        return task

    def handle_response(self, task: Task) -> dict:
        if task.output.tools:
            return self.command_agent.handle_response(task)
        json_data = self.json_extractor_agent.process(Task(task.output.message))
        return json_data.output.message
