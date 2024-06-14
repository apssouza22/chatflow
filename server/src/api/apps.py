import random

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.factory import apps, chat_history
from api.user import User, get_current_user
from core.app.app_dao import App

apps_router = r = APIRouter()


@r.post("/applications", response_model=App)
def create_app(app: App, current_user: User = Depends(get_current_user)):
    app_key = random.randint(0, 100000000)
    app = App(
        app_key=f"{app_key}",
        app_name=app.app_name,
        app_description=app.app_description,
        app_user=current_user.email,
        app_model=app.app_model,
        app_temperature=app.app_temperature
    )
    apps.add(current_user.email, app)
    return JSONResponse(content=app.dict())


@r.get("/applications")
def list_apps(current_user: User = Depends(get_current_user)):
    json_compatible_item_data = jsonable_encoder(apps.get_by_user_email(current_user.email))
    return JSONResponse(content=json_compatible_item_data)


@r.put("/applications/{app_key}")
def update_app(app_key: str, app: App, current_user: User = Depends(get_current_user)):
    app_updated = update_user_app(current_user.email, app_key, app)
    if app_updated:
        return JSONResponse(content=app_updated.dict())

    raise HTTPException(status_code=404, detail="App not found")


@r.delete("/applications/{app_key}")
def delete_app(app_key: str, current_user: User = Depends(get_current_user)):
    for a in apps.get_by_user_email(current_user.email):
        if app_key == a.app_key:
            apps.remove(current_user.email, a.app_key)
            return JSONResponse(content={"message": "App deleted successfully"})
    raise HTTPException(status_code=404, detail="App not found")


@r.get("/applications/{app_key}/history")
def get_app_conversation(app_key: str, user: User = Depends(get_current_user)):
    if app_key == "chat":
        return chat_history.get_latest_messages(user.pk, app_key)

    for a in apps.get_by_user_email(user.email):
        if app_key == a.app_key:
            return chat_history.get_latest_messages(user.pk, app_key)

    raise HTTPException(status_code=404, detail="App not found")


def update_user_app(email, app_key, app):
    for a in apps.get_by_user_email(email):
        if app_key == a.app_key:
            a.app_name = app.app_name
            a.app_description = app.app_description
            a.app_model = app.app_model
            a.app_temperature = app.app_temperature
            a.app_user = email
            apps.edit(email, a)
            return a
