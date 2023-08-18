# create a class to store and retrieve the data using FileDb
import json
from typing import List, Optional

from pydantic import BaseModel

from core.common.file_db import FileDB


class App(BaseModel):
    app_name: str
    app_description: str
    app_key: str = ""
    app_user: str = ""
    app_model: str = ""
    app_temperature: float = 0.1


class AppDao:
    def __init__(self):
        self.db = FileDB('./file_db/apps')

    def get_by_user_email(self, user_email: str) -> List[App]:
        apps = self.db.get(user_email)
        if apps is None:
            return []

        return [App(**app) for app in json.loads(apps)]

    def add(self, user, app: App):
        if self.get_by_user_email(user) is None:
            self.db.put(user, json.dumps([app.dict()]))
            return

        apps = self.get_by_user_email(user)
        apps.append(app)
        self.put(apps, user)

    def edit(self, user, app: App):
        apps = self.get_by_user_email(user)
        if apps is None:
            return False

        for i, val in enumerate(apps):
            if app.app_key == val.app_key:
                apps[i] = app
                break
        self.put(apps, user)

    def get_by_id(self, user, app_key: str) -> Optional[App]:
        if self.get_by_user_email(user) is None:
            return None
        apps = self.get_by_user_email(user)
        for i in apps:
            if app_key == i.app_key:
                return i
        return None

    def put(self, apps, user):
        self.db.put(user, json.dumps([app.dict() for app in apps]))

    def remove(self, user, app_key):
        if self.get_by_user_email(user) is None:
            return False
        apps = self.get_by_user_email(user)
        for i in apps:
            if app_key == i.app_key:
                apps.remove(i)
        self.put(apps, user)
