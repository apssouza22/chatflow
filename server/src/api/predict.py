import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.llm.llm_service import llm_service_factory

predict_router = r = APIRouter()


class CompletionRequest(BaseModel):
    question: str
    context: str

llm_service = llm_service_factory()
@r.post("/chat/llm", response_model=t.Dict)
async def think(
) -> t.Dict:
    # response = llm_service.infer("Hello World chatGPT, how are you?")
    response = llm_service.create_embedding("Hello World chatGPT, how are you?")
    return {
        "message": "Hello World chatGPT, how are you?",
        "response": response
    }

