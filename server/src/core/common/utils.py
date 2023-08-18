import json
from enum import Enum


def filter_content(contexts: list, option: str):
    for i, context in enumerate(contexts):
        if f"{i}" == option.lower():
            return [context]
        if f"option {i}" == option.lower():
            return [context]
    return contexts


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
