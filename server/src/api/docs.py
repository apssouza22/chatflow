import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from core.common import conn

redis_client = conn.get_redis_instance()

docs_router = r = APIRouter()


class SearchRequest(BaseModel):
    text: str
    tags: str = ""


@r.post("/docs/search", response_model=t.Dict)
async def find_docs(search_req: SearchRequest) -> t.Dict:
    tags = "demo|chat|"
    search_req.tags = tags
    return {"message": "Hello World"}
