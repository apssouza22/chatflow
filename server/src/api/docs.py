import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.common import conn
from core.docs_search.doc_service import doc_service_factory
from core.docs_search.query import search_docs
from core.llm.llm_service import llm_service_factory

redis_client = conn.get_redis_instance()

docs_router = r = APIRouter()


class SearchRequest(BaseModel):
    text: str
    tags: str = ""


llm_service = llm_service_factory()
doc_service = doc_service_factory(llm_service, redis_client)


@r.post("/docs/search", response_model=t.Dict)
async def find_docs(search_req: SearchRequest) -> t.Dict:
    resp = doc_service.search_docs(search_req.tags, search_req.text)
    return {"response": resp}
