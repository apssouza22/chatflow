import re

from core.agency.agents import AgentBase, Task
from core.docs_search.doc_service import Doc


class DocPickerAgent(AgentBase):

    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)

        self.system_prompt = f"You are an AI assistant helping to pick the right content from the list contents. \n"
        f"Your decision will be based on the user input. \n"
        f"IMPORTANT: you should respond only with the option number (int type) and nothing else."

    def process(self, task: Task):
        content = self._build_message(task.context, task.input)
        infer = self.llm_service.infer([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content}
        ])
        option = self._filter_content(task.context, infer.message)
        return option

    @staticmethod
    def _build_message(contexts: list[Doc], user_input: str):
        contents = ""
        for index, context in enumerate(contexts):
            contents += f"**Option {index}**: \n {context.text} \n\n"

        msg = """Given the contents below, please answer which content option it should be used to replay to the user input.
    CONTENTS
    ---
    """
        msg += contents
        msg += f"USER INPUT \n---\n"
        msg += user_input
        msg += f"\n\nRESPONSE: "
        return msg

    @staticmethod
    def _filter_content(contexts: list[Doc], option: str):
        match = re.findall(r'\d+', option)
        if len(match) < 1:
            return contexts[0]

        for i, context in enumerate(contexts):
            if f"{i}" == match[0]:
                print(f"Doc selected: {context.title}")
                return context
        return contexts[0]
