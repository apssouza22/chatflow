GPT_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "browse_website",
            "description": "Function to browse a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "thoughts": {
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
                    },
                    "args": {
                        "type": "object",
                        "description": "The arguments for the browse website",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url of the website"
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
                    "args",
                    "args.url"
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
                    "thoughts": {
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
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the function"
                    },
                    "code": {
                        "type": "string",
                        "description": "The code of the function"
                    },
                    "param": {
                        "type": "object",
                        "description": "The parameters of the function"
                    }
                },
                "required": [
                    "name",
                    "code",
                    "param"
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
                    "thoughts": {
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
                    },
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
                    "args.url",
                    "args.method",
                    "args.data_request",
                    "args.headers"
                    "request_render"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ask_question",
            "description": "Function to ask a question to the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask"
                    }
                },
                "required": [
                    "question"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "parameters": {
                "type": "object",
                "properties": {
                    "thoughts": {
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
                    },
                    "args": {
                        "type": "object",
                        "description": "The thoughts of the bot",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the sender"
                            },
                            "email": {
                                "type": "string",
                                "description": "The email of the sender"
                            },
                            "subject": {
                                "type": "string",
                                "description": "The subject of the email"
                            },
                            "body": {
                                "type": "string",
                                "description": "The body of the email"
                            }
                        }
                    }
                },
                "required": [
                    "name",
                    "email",
                    "subject",
                    "body"
                ]
            },
            "description": "Function to send an email"
        }
    }
]
