import os

import uvicorn
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

frontend_dir = "../../chat-ui/build"
generated_dir = "./uploads"

# if os.path.exists("/app/frontend"):
#     frontend_dir = "/app/frontend"  # inside docker
#     generated_dir = "/app/uploads"

if not os.path.exists(generated_dir):
    os.makedirs(generated_dir)

app.mount("/assets", StaticFiles(directory=frontend_dir), name="assets")
app.mount("/chat-commander-ui", StaticFiles(directory=frontend_dir), name="old-assets")
app.mount("/uploads", StaticFiles(directory=generated_dir), name="generated files")

@app.get("/")
async def read_index():
    print("index.html")
    if os.path.exists(frontend_dir + "/index.html"):
        return FileResponse(frontend_dir + "/index.html")
    else:
        raise HTTPException(status_code=404, detail="Index.html not found")


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
