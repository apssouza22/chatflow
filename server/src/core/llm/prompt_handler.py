import json
import time
from typing import List

from core.llm.dtos import MessageDict, MessageRole, MessageCompletion

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
                               f'Use this if the command is a send email\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "send_email" \\ The command will be a send email\n' \
                               f'"args": {{"name": "<your name>","email": "<your email>", "subject": "<subject>", "body": "<email body>"}} \\ The arguments for the send email\n' \
                               f'}}\n```' \
                               f'\n\n**Option 4:**\n' \
                               f'Use this command if you want to ask a question to the user\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "chat_question" \\ The command will be a chat question\n' \
                               f'}}\n ```' \
                               f'\n\n**Option 5:**\n' \
                               f'Use this if the command is a javascript function\n' \
                               f'Markdown code snippet formatted in the following schema:\n\n' \
                               f'```json\n command:{{\n   ' \
                               f'"name": "js_func" \\ The command will be a Javascript function\n' \
                               f'"function": {{"name": "<function_name>", "code": "<function_code>", "param": "<json_param>"}} \\ The javascript function details\n' \
                               f'}}\n ```' \
                               f'Notice: All the options will be along with the ``` thoughts:{{ }}```'


def _get_main_command_prompt(doc_context: str, sanitized_query: str) -> List[MessageDict]:
    return [
        MessageDict(
            role=MessageRole.SYSTEM,
            content=f"You are a bot helping the user to execute tasks. \n\n"
                    f"If you are unsure and the answer is not explicitly written in the documentation, say "
                    f"\"Sorry, I don't know how to help with that.\"\n\n"
                    f"Given the following information from the documentation "
                    f"provide for the user's task using only this information\n\n "
                    f"DOCUMENTATION\n----------------------------\n\n"
                    f"{doc_context}\n\n"
        ),
        MessageDict(
            role=MessageRole.SYSTEM,
            content=f"The current time and date is {time.strftime('%c')}"
        ),
        MessageDict(
            role=MessageRole.USER,
            content=f"Execute the task using only the provided documentation above."
        ),
        MessageDict(
            role=MessageRole.USER,
            content=response_format_instructions
        ),
        MessageDict(
            role=MessageRole.USER,
            content='Determine which command to use, and respond using the format specified above'
        ),
        MessageDict(
            role=MessageRole.USER,
            content=f"Under no circumstances should your response deviate from the following JSON FORMAT:  \n{formatted_response_format} \n"
        ),
        MessageDict(
            role=MessageRole.USER,
            content=f'Here is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n'
                    f'User input: {sanitized_query}'
        ),
    ]


def build_prompt_command(history: List[MessageCompletion]) -> List[MessageDict]:
    prompts = []

    for message in history:
        if message.role == MessageRole.ASSISTANT:
            prompts.append(MessageDict(role=MessageRole.ASSISTANT, content=message.response))
            continue

        # Empty context means that the user is refining the command based on the assistant's response
        if message.role == MessageRole.USER and message.context == "":
            prompts.append(MessageDict(
                role=MessageRole.USER,
                content=f'Here is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n'
                        f'{message.query}'
            ))
            continue

        # Reset prompts every time we get a new user command with context
        # this is to prevent reach the max tokens limit
        if message.role == MessageRole.USER and message.context != "":
            prompts.clear()
            prompts.extend(_get_main_command_prompt(message.context, message.query))

    return prompts


def _prepare_prompt_history(history: List[MessageCompletion]) -> List[MessageCompletion]:
    local_history = []
    count = 0

    for message in reversed(history):
        # if message.role == "user" and message.context and message.context != "":
        if message.role == MessageRole.USER:
            count += 1
        local_history.append(message)
        if count == 3:
            break

    last_message = local_history[0]
    for message in local_history[1:]:
        if last_message.context == message.context:
            message.context = ""
    local_history.reverse()
    return local_history


def prompt_pick_content(contexts: List[str], user_input) -> List[MessageDict]:
    system_msg = MessageDict(
        role=MessageRole.SYSTEM,
        content=f"You are an AI assistant helping to pick the right content from the list contents. \n"
                f"Your decision will be based on the user input. \n"
                f"IMPORTANT: you should respond only with the option number (int type) and nothing else."
    )
    contents = ""
    for index, context in enumerate(contexts):
        contents += f"**Option {index}**: \n {context} \n\n"

    msg = """Given the contents below, please answer which content option it should be used to replay to the user input.
CONTENTS
---
"""
    msg += contents
    msg += f"USER INPUT \n---\n"
    msg += user_input
    msg += f"\n\nRESPONSE: "
    user_msg = MessageDict(
        role=MessageRole.USER,
        content=msg
    )
    return [system_msg, user_msg]
