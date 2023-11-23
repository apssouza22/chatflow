import os
import random
import typing as t
import requests
from fastapi import Depends, APIRouter, UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.factory import llm_service
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


@r.post("/upload")
async def upload_file(
        file: UploadFile,
        request: Request,
        current_user: User = Depends(get_current_user)):
    try:
        appkey = request.headers.get("appkey")
        if file.filename:
            upload_folder = 'uploads' + os.sep + appkey
            filename = await save_file(file, upload_folder)

            return {"message": "File uploaded successfully", "filename": upload_folder + "/" + filename}

        return {"message": "No file selected"}
    except Exception as e:
        return {"error": str(e)}

@r.post("/speech-to-text")
async def audio(
        file: UploadFile,
        request: Request,
        current_user: User = Depends(get_current_user)):
    try:
        appkey = request.headers.get("appkey")
        if file.filename:
            upload_folder = 'uploads' + os.sep + appkey + os.sep + "audios"
            filename = await save_file(file, upload_folder)
            file_path = os.path.join(upload_folder, filename)
            text = llm_service.audio_to_text(file_path)
            return {"message": text}

        return {"message": "No file selected"}
    except Exception as e:
        return {"error": str(e)}


async def save_file(file, upload_folder):
    os.makedirs(upload_folder, exist_ok=True)
    filename = str(random.randint(0, 100000000)) + "_" + file.filename
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return filename
