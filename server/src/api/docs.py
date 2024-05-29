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

docs_router = r = APIRouter()


@r.post("/docs/search", response_model=t.Dict)
async def find_docs(search_req: SearchRequest, request: Request, current_user: User = Depends(get_current_user)) -> t.Dict:
    if cost_service.has_allowance_exceeded(current_user.email, search_req.app_key):
        raise HTTPException(status_code=402, detail="You have exceeded the free allowance for this app")

    is_plugin_mode = request.headers.get("pluginmode").lower() == "true"
    tags = "demo|chat|"
    if is_plugin_mode:
        tags = ""
    tags += search_req.app_key if search_req.app_key != "" else "chat"
    search_req.tags = tags
    search_req.user_email = current_user.email
    return await doc_search_service.full_search(search_req)


@r.post("/docs", response_model=t.Dict)
async def add_doc(request: AddDocRequest, current_user: User = Depends(get_current_user)) -> t.Dict:
    return await add_app_doc(request)


@r.get("/docs", response_model=t.Dict)
async def all_docs(app: t.Optional[str], current_user: User = Depends(get_current_user)) -> t.Dict:
    return await get_all_docs(app)



@r.delete("/docs/{pk}", response_model=t.Dict)
async def delete_doc(pk: str, current_user: User = Depends(get_current_user)) -> JSONResponse:
    vector_key = "data_vector:" + pk
    item_vector = await redis_client.hgetall(vector_key)
    if item_vector is None:
        return JSONResponse(content={"message": "doc not found"}, status_code=404)

    await redis_client.delete(vector_key)
    return JSONResponse(content={"message": "doc deleted successfully"}, status_code=200)


async def get_all_docs(app_key) -> t.Dict:
    if app_key == "":
        raise HTTPException(status_code=400, detail="app_key can not be empty")

    data = await doc_search_service.get_vector_docs_by_app(app_key)
    return {
        'total': data["total"],
        'data': data
    }


async def add_app_doc(request) -> t.Dict:
    item_id = randint(0, 100000000)
    key = "data_vector:" + str(item_id)
    # vector = TEXT_MODEL.encode(request.text).astype(np.float32).tolist()
    embedding = llm_service.embed_text(request.text)[0]
    openai_vector = np.array(embedding, dtype=np.float32).tobytes()
    mappings = {
        "item_id": int(item_id),
        "application": request.app_key,
        "text_vector": np.array([], dtype=np.float32).tobytes(),
        "openai_text_vector": openai_vector,
        "title": request.title,
        "text_raw": request.text,
    }
    hset_result = redis_client.hset(key, mapping=mappings)
    # hset returns int if the key already exists
    if not isinstance(hset_result, int):
        await hset_result
    return {
        "message": "doc added successfully",
    }
