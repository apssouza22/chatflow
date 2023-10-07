import json
import time
import typing
from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, List

from core.app.app_dao import App

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


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value


class MessageDict(TypedDict):
    role: MessageRole
    content: str
    def __str__(self):
        return {
            "role": self.role.value,
            "content": self.content
        }

@dataclass
class MessageCompletion:
    role: MessageRole
    context: str = ""
    query: str = ""
    response: str = ""


def get_msg_cycle(doc_context: str, sanitized_query: str) -> List[MessageDict]:
    # TODO: Improve this function to not include system messages. This is a temporary solution
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
        # empty context means that the user is refining the command based on the assistant's response
        if message.role == MessageRole.USER and message.context == "":
            prompts.append(MessageDict(
                role=MessageRole.USER,
                content=f'Here is the user\'s input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):\n\n'
                        f'{message.query}'
            ))
            continue
        if message.role == MessageRole.USER and message.context != "":
            # reset prompts every time we get a new user command with context
            # this is to prevent reach the max tokens limit
            prompts.clear()
            prompts.extend(get_msg_cycle(message.context, message.query))
    return prompts


def prompt_text_form(input: str) -> typing.List[MessageDict]:
    system_msg = """You are an AI responsible for identifying users intent.  Your goal is to analyze the user input and determine if the user requires either text or form as the response \n
If the user input is understood as a question automatically, the response should be a "text". Example: explain me how to add a new address;  tell me what to do; how much does it cost? \n
If the user input is understood as a greeting, the response should be "text".   Example:  How are you; Hi; Oi; Como você está? \n
If the input requires an action, the response should be "form". Example: help me to send an email; book me a class; add a new address;  calculate the distance; help me to buy it \n
If you are unsure about the answer say "text" \n
VERY IMPORTANT: Respond with either "text" or "form".
"""
    prompts = []
    prompts.append(MessageDict(role=MessageRole.SYSTEM, content=system_msg))
    prompts.append(MessageDict(role=MessageRole.USER, content=f'User input: {input}'))
    return prompts


def prepare_prompt_history(history: List[MessageCompletion]) -> List[MessageCompletion]:
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


def build_prompt_answer_questions(app: App, contexts, msgs) -> List[MessageDict]:
    msg = f'Make sure to always translate your reply to the user\'s language, base yourself on the number of words in each language.' \
          f'You are a language model trained to answer questions based on a given content. \n ' \
          f'Given a passage of content, I will ask you questions about it. Please provide concise and accurate answers based on the given information. \n' \
          f'Be friendly. Always make the user feel important. Use your knowledge of effective customer service techniques. \n ' \
          f'End the response with questions to keep the user engaged and achieve your goal which is help the user take the decision about buying the product or service \n' \
          f'IMPORTANT: If the given content contains links, make sure you include them in the answer. \n' \
          f'IMPORTANT: If the given content contains image urls, make sure you include them in the answer. \n' \
          f'IMPORTANT: Consider past user message and the assistant responses as context to your response. \n' \
          f"If you are unsure and the answer is not explicitly written in the documentation, say \"Sorry, I don't know how to help with that. Please try again with more details.\"\n\n"
    app_system_prompt = app.app_description if app.app_description != "" else 'You are a sales assistant responsible for helping answer user questions and help him to take the decision of buying the product or service.'

    system_msg = MessageDict(
        role=MessageRole.SYSTEM,
        content=app_system_prompt + " \n " + msg
    )

    # Max 2 contexts
    if len(contexts) > 2:
        contexts = contexts[-2:]

    context = "\n\n".join(contexts)
    msg_history = "\n".join(msgs)

    user_msg = MessageDict(
        role=MessageRole.USER,
        content=f'CONTENT\n----------------------------\n {context}' \
                f'\n\nHISTORY\n----------------------------\n {msg_history}' \
                f'\nRESPONSE: '
    )
    prompts = [system_msg, user_msg]
    return prompts


def get_prompt_objs_from_history(history: List[MessageCompletion]) -> typing.Tuple[List[str], List[str]]:
    prepared_history = prepare_prompt_history(history)
    msgs = []
    contexts = []
    for message in prepared_history:
        if message.role == MessageRole.ASSISTANT:
            msgs.append("assistant: " + message.response)
            continue
        # empty context means that the user is refining the command based on the assistant's response
        if message.role == MessageRole.USER and message.context == "":
            msgs.append(f"user: {message.query}")
            continue
        if message.role == MessageRole.USER:
            msgs.append(f"user: {message.query}")
            contexts.append(message.context)
    return contexts, msgs
