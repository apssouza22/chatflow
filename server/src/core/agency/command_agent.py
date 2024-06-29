import json
import time

from core.agency.agents import AgentBase, Task


class CommandAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = """You are a bot helping the user to execute tasks. \n\n
        If you are unsure and the answer is not explicitly written in the documentation, say 
        "Sorry, I don't know how to help with that." \n\n
        Given the following information from the documentation 
        provide for the user's task using only this information\n\n 
        """

    def process(self, task: Task) -> Task:
        prompt = self._get_main_command_prompt(task.context, task.input)
        infer = self.llm_service.infer_using_basic(prompt)
        task.set_output(infer)
        return task

    def handle_response(self, task: Task) -> dict:
        pass

    def _get_main_command_prompt(self, doc_context: str, sanitized_query: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": f'{self.system_prompt}'
                           f"DOCUMENTATION\n----------------------------\n\n"
                           f"{doc_context}\n\n"
            },
            {
                "role": "system",
                "content": f"The current time and date is {time.strftime('%c')}"
            },
            {
                "role": "user",
                "content": f"Execute the task using only the provided documentation above."
            },
            {
                "role": "user",
                "content": response_format_instructions
            },
            {
                "role": "user",
                "content": 'Determine which command to use, and respond using the format specified above'
            },
            {
                "role": "user",
                "content": f"Under no circumstances should your response deviate from the following JSON FORMAT:  \n{formatted_response_format} \n"
            },
            {
                "role": "user",
                "content": f'Here is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n'
                           f'User input: {sanitized_query}'
            },
        ]


response_format = {
    "thoughts": {
        "reasoning": "reasoning. Use future tense e.g. 'I will do this'",
        "speak": "Friendly thoughts summary to say to user. Use future tense e.g. 'I will do this'. Important: Make sure to always translate your reply to the user's language.",
    },
    "command": {
        "name": "api_call|browse_website|js_func",
        "args": {"arg name": "value"},
        "request_render": {
            "field_name_1": {
                "field_type": "select",
                "field_options": ["SP", "RJ"]
            },
            "field_name_2": {
                "field_type": "password",
                "field_options": []
            }
        },
        "response_render": {
            "render_type": "list",
            "fields": ["total"]
        }
    },
}
formatted_response_format = json.dumps(response_format, indent=4)
response_format_instructions = f"RESPONSE FORMAT INSTRUCTIONS\n----------------------------\n\n" \
                               f"When responding to me, please output a response in one of three formats:\n\n" \
                               f"**Option 1:**\n" \
                               f"Use this if the command is a API call\n" \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command: {{\n   ' \
                               f'"name": "api_call" \\ The command will be an api call\n' \
                               f'"args": {{"url": "<url>", "method": "<http method>","data_request": "<JSON object>","headers": "<JSON object>"}} \\ The arguments for the api call\n' \
                               f'"request_render": {{"<field name>":{{"field_type": "<input|checkbox|select|password>", field_options: "<array string>"}} }} \\ Instruction of how to render the request fields\n' \
                               f'"response_render": {{"render_type": "<list|chart>", fields: "<array string>"}} \\ Instruction of how to render the response\n' \
                               f'}}\n```' \
                               f'\n\n**Option 2:**\n' \
                               f'Use this if the command is a browse website\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "browse_website" \\ The command will be a browse website\n' \
                               f'"args": "url": "<url>" \\ The arguments for the browse website\n' \
                               f'"request_render": "field_type": "<input|checkbox|select|password>", field_options: "<array string>" \\ Instruction of how to render the request fields\n' \
                               f'}}\n```' \
                               f'\n\n**Option 3:**\n' \
                               f'Use this if the command is a Javascript function\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "js_func" \\ The command will be a Javascript function\n' \
                               f'"args": {{"func_name": "<function_name>", "func_code": "<function_code>", "func_params": "<object_params>"}} \\ The javascript function details\n' \
                               f'}}\n ```' \
                               f'Notice: All the options will be along with the ``` thoughts:{{ }}```'
