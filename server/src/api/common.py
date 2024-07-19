from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

user_router = r = APIRouter()


class LoginRequestBody(BaseModel):
    email: str
    password: str


class App(BaseModel):
    app_name: str
    app_description: str
    app_key: str = ""
    app_user: str = ""
    app_model: str = ""
    app_temperature: float = 0.1


@r.post("/user/login")
def login(form_data: LoginRequestBody):
    return JSONResponse(content={"access_token": "access-token", "token_type": "bearer"})


@r.post("/applications", response_model=App)
def create_app(app: App):
    return JSONResponse(content=app.dict())
