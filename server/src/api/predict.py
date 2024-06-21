import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.agency.agent_service import agent_service_factory
from core.common import conn
from core.docs_search.doc_service import doc_service_factory
from core.llm.llm_service import llm_service_factory

predict_router = r = APIRouter()


class CompletionRequest(BaseModel):
    question: str
    context: str


llm_service = llm_service_factory()
doc_service = doc_service_factory(llm_service, conn.get_redis_instance())
agent_service = agent_service_factory(llm_service, doc_service)


@r.post("/chat/llm", response_model=t.Dict)
async def think(
) -> t.Dict:
    response = agent_service.run_tasks("Provide a valid JSON example")
    # response = llm_service.infer("Hello World chatGPT, how are you?")
    return {
        "response": response
    }
