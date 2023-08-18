import os

import uvicorn
from aredis_om import (
    get_redis_connection,
    Migrator
)
from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from api.apps import apps_router
from api.common import common_router
from api.docs import docs_router
from api.predict import predict_router
from api.user import user_router
from core.common import config
from core.docs_search.entities import ItemEntity

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routers
app.include_router(
    predict_router,
    prefix=config.API_V1_STR,
    tags=["api"]
)

app.include_router(
    user_router,
    prefix=config.API_V1_STR,
    tags=["user"]
)

app.include_router(
    docs_router,
    prefix=config.API_V1_STR,
    tags=["docs"]
)
app.include_router(
    apps_router,
    prefix=config.API_V1_STR,
    tags=["apps"]
)
root_router = r = APIRouter()

app.include_router(
    root_router,
    prefix="",
    tags=["hello"]
)
app.include_router(
    common_router,
    prefix=config.API_V1_STR,
    tags=["common"]
)

frontend_dir = "/app/frontend"  # inside docker
if os.path.exists("../../chat-ui/build/index.html"):
    frontend_dir = "../../chat-ui/build"

app.mount("/assets", StaticFiles(directory=frontend_dir), name="assets")
app.mount("/chat-commander-ui", StaticFiles(directory=frontend_dir), name="old-assets")


@app.get("/")
async def read_index():
    print("index.html")
    if os.path.exists(frontend_dir + "/index.html"):
        return FileResponse(frontend_dir + "/index.html")
    else:
        raise HTTPException(status_code=404, detail="Index.html not found")


@app.on_event("startup")
async def startup():
    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    ItemEntity.Meta.database = get_redis_connection(url=config.REDIS_URL, decode_responses=True)
    await Migrator().run()


if __name__ == "__main__":
    env = os.environ.get("DEPLOYMENT", "dev")
    host = os.environ.get("SERVER_HOST", "127.0.0.1")

    server_attr = {
        "host": host,
        "reload": True,
        "port": 8880,
        "workers": 1
    }

    uvicorn.run("server:app", **server_attr)
