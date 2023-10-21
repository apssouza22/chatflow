from typing import Annotated, Optional
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import Cookie
from fastapi import Response

from api.factory import user_service, current_session, cost_service
from api.jwttoken import decode_access_token, create_access_token
from core.user.user_dao import User

user_router = r = APIRouter()


class LoginRequestBody(BaseModel):
    email: str
    password: str


class SessionReq(BaseModel):
    app_key: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[Optional[str], Cookie()] = None):
    if token is None:
        return None
    payload = decode_access_token(token)
    user = user_service.get_user_by_email(payload["sub"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


# Deprecated endpoints
@r.post("/admin/user/register", deprecated=True)
def register(user: User):
    return signup(user)


@r.post("/admin/user/login", deprecated=True)
def login(form_data: LoginRequestBody):
    return user_login(form_data)


@r.put("/admin/user/session", deprecated=True)
def session(session_req: SessionReq, current_user: User = Depends(get_current_user)):
    # current_session[current_user.email] = session_req
    return JSONResponse(content={"message": "Session updated successfully"})


# New endpoints
@r.post("/user/register")
def user_register(user: User):
    return signup(user)


@r.post("/user/login")
def login(form_data: LoginRequestBody):
    return user_login(form_data)


@r.put("/user/session")
def session(session_req: SessionReq, current_user: User = Depends(get_current_user)):
    current_session[current_user.email] = session_req
    return JSONResponse(content={"message": "Session updated successfully"})


@r.get("/users")
def get_all_users(user: User = Depends(get_current_user)):
    return user_service.get_all_users()


@r.get("/user/usage")
def usage(user: User = Depends(get_current_user)):
    return cost_service.get_user_costs(user.email)


@r.get("/user/{user_email}/app/{app_key}/auth")
def user_app_auth(user_email: str, app_key: str):
    exists = user_service.exists_app(user_email, app_key)
    if exists:
        access_token = create_access_token(data={"sub": user_email, "type": "app-auth"})
        return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

    raise HTTPException(status_code=401, detail="Invalid user or app.")


def signup(user: User):
    if user_service.get_user_by_email(user.email) is not None:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(name=user.name, password=user.password, email=user.email)
    user_service.add_user(new_user)

    return JSONResponse(content={"message": "User registered successfully"})


def user_login(req: LoginRequestBody):
    user = user_service.authenticate_user(req.email, req.password)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email, "type": "user-auth"})
    resp = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    resp.set_cookie(key="access_token", value=access_token)  # FIXME: In release mode should use `secure=True`.
    return resp
