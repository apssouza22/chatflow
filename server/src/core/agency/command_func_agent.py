import json
import time

from core.agency.agents import AgentBase, Task


class CommandFuncAgent(AgentBase):

    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = """You are a bot helping the user to execute tasks. \n\n"
        If you are unsure and the answer is not explicitly written in the documentation, say 
        "Sorry, I don't know how to help with that." \n\n
        Given the following information from the documentation 
        provide for the user's task using only this information\n\n 
        """

    def process(self, task: Task) -> Task:
        prompt = self._get_prompt(task.context, task.input)
        infer = self.llm_service.infer_using_pro(prompt, GPT_FUNCTIONS)
        task.set_output(infer)

        return task

    @staticmethod
    def handle_response(task: Task) -> dict:
        func = task.output.tools[0]["function"]
        args_str = func["arguments"]
        args = json.loads(args_str)
        return {
            "thoughts": args["thoughts"],
            "command": {
                "name": func["name"],
                "args": args["args"] if "args" in args else {},
                "request_render": args["request_render"] if "request_render" in args else {},
                "response_render": args["response_render"] if "response_render" in args else {},
            }
        }

    def _get_prompt(self, doc_context: str, txt_input: str) -> list[dict]:
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
                "content": f"Help me to execute the task using only the provided documentation"
            },
            {
                "role": "user",
                "content": f"Please use one of the provided functions as the response:\n"
                           f"Option 1: Use the api_call function if the command is a API call\n\n"
                           f"Option 2: Use the browse_website function if the command is to browse website\n\n"
                           f"Option 3: Use the js_func function if the command is a javascript function"
            },
            {
                "role": "user",
                "content": f'Here is the user\'s input :\n\n {txt_input}'
            }
        ]


thoughts = {
    "type": "object",
    "description": "The thoughts of the bot",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "The reasoning of the bot. Use future tense e.g. 'I will do this'"
        },
        "speak": {
            "type": "string",
            "description": "Friendly thoughts summary to say to the user. Use future tense e.g. 'I will do this'. Important: Make sure to always translate your reply to the user's language."
        }
    }
}
functions = {
    "type": "object",
    "description": "The function details",
    "properties": {
        "func_name": {
            "type": "string",
            "description": "The function's name"
        },
        "func_code": {
            "type": "string",
            "description": "The function's code"
        },
        "func_params": {
            "type": "object",
            "description": "The function's parameters"
        }
    }
}

GPT_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "browse_website",
            "description": "Function to browse a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "thoughts": thoughts,
                    "args": {
                        "type": "object",
                        "description": "The arguments for the browse website",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url of the website"
                            },
                            "method": {
                                "type": "string",
                                "description": "The request method"
                            }
                        }
                    },
                    "request_render": {
                        "type": "object",
                        "description": "The instruction of how to render the request fields",
                        "properties": {
                            "field_type": {
                                "type": "string",
                                "description": "The type of the field",
                                "enum": [
                                    "input",
                                    "checkbox",
                                    "select",
                                    "password"
                                ]
                            },
                            "field_options": {
                                "type": "array",
                                "description": "The options for the field",
                                "items": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                },
                "required": [
                    "thoughts",
                    "args",
                    "args.url"
                    "args.method"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "js_func",
            "description": "Execute a javascript function",
            "parameters": {
                "type": "object",
                "properties": {
                    "thoughts": thoughts,
                    "args": functions,
                },
                "required": [
                    "thoughts",
                    "name",
                    "code",
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "api_call",
            "description": "Function to call REST APIs",
            "parameters": {
                "type": "object",
                "properties": {
                    "thoughts": thoughts,
                    "args": {
                        "type": "object",
                        "description": "The arguments for the http request",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url of the http request"
                            },
                            "method": {
                                "type": "string",
                                "description": "The http method of the http request"
                            },
                            "data_request": {
                                "type": "object",
                                "description": "The data of the http request"
                            },
                            "headers": {
                                "type": "object",
                                "description": "The headers of the http request"
                            }
                        }
                    },
                    "request_render": {
                        "type": "object",
                        "description": "The instruction of how to render the request fields",
                        "properties": {
                            "field_type": {
                                "type": "string",
                                "description": "The type of the field",
                                "enum": [
                                    "input",
                                    "checkbox",
                                    "select",
                                    "password"
                                ]
                            },
                            "field_options": {
                                "type": "array",
                                "description": "The options for the field",
                                "items": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "response_render": {
                        "type": "object",
                        "description": "The instruction of how to render the response",
                        "properties": {
                            "render_type": {
                                "type": "string",
                                "description": "The type of the render",
                                "enum": [
                                    "list",
                                    "chart"
                                ]
                            },
                            "fields": {
                                "type": "array",
                                "description": "The fields to render",
                                "items": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                },
                "required": [
                    "thoughts",
                    "args.url",
                    "args.method",
                    "args.data_request",
                    "args.headers"
                    "request_render"
                ]
            }
        }
    }
]
