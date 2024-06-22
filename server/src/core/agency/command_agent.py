import json

from core.agency.agents import AgentBase, Task


class CommandAgent(AgentBase):
    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = "You are a CommandAgent. You are a bot that helps users to execute commands. Your job is to help users execute commands. You will be given a command and you will be asked to execute the command based on the given prompt."

    def process(self, task: Task) -> Task:
        return task



response_format = {
    "thoughts": {
        "reasoning": "reasoning. Use future tense e.g. 'I will do this'",
        "speak": "Friendly thoughts summary to say to user. Use future tense e.g. 'I will do this'. Important: Make sure to always translate your reply to the user's language.",
        "criticism": "constructive self-criticism"
    },
    "command": {
        "name": "api_call|browse_website|send_email|chat_question",
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
                               f"When responding to me, please output a response in one of five formats:\n\n" \
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
                               f'Use this if the command is a javascript function\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "js_func" \\ The command will be a Javascript function\n' \
                               f'"function": {{"name": "<function_name>", "code": "<function_code>", "param": "<json_param>"}} \\ The javascript function details\n' \
                               f'}}\n ```' \
                               f'Notice: All the options will be along with the ``` thoughts:{{ }}```'
