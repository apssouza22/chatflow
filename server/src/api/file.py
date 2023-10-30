import typing as t
from random import randint

import numpy as np
from fastapi import Depends, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse

from api.factory import doc_search_service, redis_client, llm_service, cost_service
from api.user import get_current_user, User
from core.docs_search.dtos import AddDocRequest
from core.docs_search.dtos import (
    SearchRequest
)

r = APIRouter()


@r.post("/file/on-upload", response_model=t.Dict)
async def on_upload(file_id: str, request: Request, current_user: User = Depends(get_current_user)) -> t.Dict:
    TODO