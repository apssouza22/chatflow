import json
from enum import Enum


def filter_content(contexts: list, option: str):
    """Filter contexts based on the option selected by the llm."""
    for i, context in enumerate(contexts):
        if f"{i}" == option.lower():
            return [context]
        if f"option {i}" == option.lower():
            return [context]
    return contexts


class EnumEncoder(json.JSONEncoder):
    """JSON encoder for Enum objects."""

    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
