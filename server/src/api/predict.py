import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.agency.agent_service import agent_service_factory
from core.common import conn
from core.docs_search.doc_service import doc_service_factory
from core.llm.llm_service import llm_service_factory
from core.memory.chat_memory_service import factory_chat_memory

predict_router = r = APIRouter()

llm_service = llm_service_factory()
doc_service = doc_service_factory(llm_service, conn.get_redis_instance())
chat_memory = factory_chat_memory()
agent_service = agent_service_factory(llm_service, doc_service, chat_memory)


class UserInput(BaseModel):
    question: str
    context: str


@r.post("/chat/llm", response_model=t.Dict)
async def think(user_input: UserInput) -> t.Dict:
    response = agent_service.run_tasks(user_input.question)
    return response
