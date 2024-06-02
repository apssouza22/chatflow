from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


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
