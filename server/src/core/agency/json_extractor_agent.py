import json

from core.agency.agents import AgentBase, Task
from core.llm.llm_service import LLMResponse


class JSONExtractorAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)

    def process(self, task: Task):
        json_data = self._parse_json(task.input)
        if json_data:
            task.set_output(LLMResponse(json_data, {}))
            return task

        resp = self.llm_service.infer_using_basic([
            {
                "role": "system",
                "content": "You are a JSONFixer. You are a bot that helps users fix their JSON responses."
            },
            {
                "role": "user",
                "content": "This is a JSON response: " + task.input
            }
        ])

        json_data = self._parse_json(resp.message)
        if json_data:
            task.set_output(LLMResponse(json_data, resp.usage))
            return task

        task.set_output(resp)
        return task

    @staticmethod
    def _parse_json(txt_input):
        json_str = _extract_longest_curly_braces_content(txt_input)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None


def _extract_longest_curly_braces_content(s):
    """Extract the longest content between valid curly braces in a string."""
    stack = []
    start = -1
    result = ''
    longest_len = 0
    longest_content = ''
    for i in range(len(s)):
        if s[i] == '{':
            stack.append(i)
        elif s[i] == '}':
            if len(stack) == 0:
                start = i
            else:
                start = stack.pop()
                if len(stack) == 0:
                    content = s[start + 1:i]
                    content_len = len(content)
                    if content_len > longest_len:
                        longest_len = content_len
                        longest_content = content
    return f"{{{longest_content}}}"
