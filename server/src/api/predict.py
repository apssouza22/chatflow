import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

predict_router = r = APIRouter()


class CompletionRequest(BaseModel):
    question: str
    context: str


@r.post("/chat/completions", response_model=t.Dict)
async def think(
        question_request: CompletionRequest
) -> t.Dict:
    return {"message": "Hello World"}

