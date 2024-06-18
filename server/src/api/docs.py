import typing as t
from random import randint

import numpy as np
from fastapi import Depends, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse

from api.factory import doc_search_service, redis_client, llm_service
from core.docs_search.dtos import AddDocRequest
from core.docs_search.dtos import (
    SearchRequest
)

docs_router = r = APIRouter()


@r.post("/docs/search", response_model=t.Dict)
async def find_docs(search_req: SearchRequest, request: Request) -> t.Dict:
    tags = "demo|chat|"
    search_req.tags = tags
    return await doc_search_service.full_search(search_req)

