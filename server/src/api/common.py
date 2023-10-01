import typing as t
import requests
from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

from api.user import User, get_current_user

common_router = r = APIRouter()


@r.post("/send-email", response_model=t.Dict)
async def send_email(
        send_email_req: t.Dict,
        current_user: User = Depends(get_current_user),
) -> JSONResponse:
    return JSONResponse({"message": "Email sent successfully"}, status_code=200)


@r.post("/command", response_model=t.Dict)
def command(
        command_req: t.Dict
) -> JSONResponse:
    url = command_req.get("url", "")
    method = command_req.get("method", "GET")
    headers = command_req.get("headers", {})

    response = requests.request(method, url, headers=headers, json=command_req.get("body", {}))
    if not response.ok:
        return JSONResponse({"message": response.text}, status_code=response.status_code)

    data = response.json()

    return JSONResponse(data, status_code=response.status_code)
