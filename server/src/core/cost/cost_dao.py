import json
from typing import List

from pydantic import BaseModel

from core.common.file_db import FileDB


class Cost(BaseModel):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    total_cost = 0
    model: str = "gpt3"


def sum_cost(costs: List[Cost]) -> Cost:
    total_cost = Cost()
    for cost in costs:
        total_cost.prompt_tokens += cost.prompt_tokens
        total_cost.completion_tokens += cost.completion_tokens
        total_cost.total_tokens += cost.total_tokens
        total_cost.total_cost += cost.total_cost
        total_cost.model = cost.model
    return total_cost


class CostDao:
    def __init__(self):
        self.db = FileDB('./file_db/costs')

    def get(self, user: str) -> dict:
        cost = self.db.get(user)
        if cost is None:
            return {}
        return json.loads(cost)

    def put(self, user_email: str, cost: dict):
        self.db.put(user_email, json.dumps(cost))
