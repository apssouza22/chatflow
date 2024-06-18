import os

import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from api.docs import docs_router
from api.predict import predict_router

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
    docs_router,
    prefix=config.API_V1_STR,
    tags=["docs"]
)

root_router = r = APIRouter()

app.include_router(
    root_router,
    prefix="",
    tags=["hello"]
)

frontend_dir = "/app/frontend"  # inside docker
if os.path.exists("../../chat-ui/build/index.html"):
    frontend_dir = "../../chat-ui/build"

app.mount("/assets", StaticFiles(directory=frontend_dir), name="assets")

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
