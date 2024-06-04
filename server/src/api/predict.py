import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from api.factory import llm_service
from core.llm.dtos import MessageDict, MessageRole, MessageCompletion

predict_router = r = APIRouter()


class CompletionRequest(BaseModel):
    question: str
    context: str


@r.post("/chat/completions", response_model=t.Dict)
async def think(question_request: CompletionRequest) -> t.Dict:
    message = MessageCompletion(role=MessageRole.USER, context=question_request.context, query=question_request.question)
    resp = llm_service.get_task_command(message)

    print(resp)
    return resp

