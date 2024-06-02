from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, List

from pydantic import BaseModel


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    def __str__(self):
        return self.value


@dataclass
class MessageCompletion:
    role: MessageRole
    context: str = ""
    query: str = ""
    response: str = ""


class MessageDict(TypedDict):
    role: MessageRole
    content: str

    def __str__(self):
        return {
            "role": self.role.value,
            "content": self.content
        }


class Usage(BaseModel):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    model: str


class LLMResponse(BaseModel):
    usage: List[Usage]
    message: str
