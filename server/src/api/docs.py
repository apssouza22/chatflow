import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.common import conn
from core.docs_search.query import search_docs
from core.llm.llm_service import llm_service_factory

redis_client = conn.get_redis_instance()

docs_router = r = APIRouter()


class SearchRequest(BaseModel):
    text: str
    tags: str = ""


llm_service = llm_service_factory()

@r.post("/docs/search", response_model=t.Dict)
async def find_docs(search_req: SearchRequest) -> t.Dict:
    vector = llm_service.create_embedding(search_req.text)
    resp = search_docs(search_req.tags, vector)
    return {"response": resp}
