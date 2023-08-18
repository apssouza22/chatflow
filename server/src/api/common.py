import typing as t

from fastapi import Depends, Request, APIRouter, HTTPException
from starlette.responses import JSONResponse

from api.factory import agent, apps, cost_service
from api.user import User, get_current_user
from core.agent.agent_service import UserInputDto
from core.app.app_dao import App
from core.docs_search.dtos import (
    CompletionRequest
)

common_router = r = APIRouter()


@r.post("/send-email", response_model=t.Dict)
async def send_email(
        send_email_req: t.Dict,
        current_user: User = Depends(get_current_user),
) -> JSONResponse:
    return JSONResponse({"message": "Email sent successfully"}, status_code=200)
