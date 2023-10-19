# create a class to store and retrieve the data using FileDb
import json
from typing import List, Optional

from pydantic import BaseModel


class App(BaseModel):
    user_ref: Optional[int] = None
    app_name: str
    app_description: str
    app_key: str = ""
    app_model: str = ""
    app_temperature: float = 0.1


class AppDao:
    def __init__(self, pg_conn):
        self.db = pg_conn

    # TODO: Should get by user PK instead of email.
    def get_by_user_email(self, user_email: str) -> List[App]:
        apps = self.db.fetch_all("SELECT apps.* FROM apps INNER JOIN users ON apps.user_ref = users.id WHERE users.email=%s",
                                 (user_email,))
        return [App(**app) for app in apps]

    def add(self, user, app: App):
        self.db.execute(
            "INSERT INTO apps (user_ref, app_name, app_description, app_key, app_model, app_temperature) VALUES (%s, %s, %s, %s, %s, %s)",
            (app.user_ref, app.app_name, app.app_description, app.app_key, app.app_model, app.app_temperature)
        )

    # TODO: Remove `user` parameter.
    def edit(self, user, app: App):
        self.db.execute(
            "UPDATE apps SET app_name=%s, app_description=%s, app_key=%s, app_model=%s, app_temperature=%s WHERE user_ref=%s" \
                "WHERE id=%s",
            (app.app_name, app.app_description, app.app_key, app.app_model, app.app_temperature, app.user_ref,
             app.id)
        )

    # TODO: Should get by user PK instead of email.
    def get_by_id(self, user_email, app_key: str) -> Optional[App]:
        print("XXX", user_email, app_key)
        app = self.db.fetch_one("SELECT apps.* FROM apps INNER JOIN users ON apps.user_ref = users.id WHERE users.email = %s AND apps.app_key=%s",
                                 (user_email, app_key))
        if app is None:
            return None  # TODO: a hack!
        return App(**app)

    # FIXME: `user` parameter is supefrluous.
    def put(self, apps, user):
        for app in apps:
            self.db.execute(
                "INSERT apps (user_ref, app_name, app_description, app_key, app_model, app_temperature VALUES(%s, %s, %s, %s, %s, %s)",
                (app.user_ref, app.app_name, app.app_description, app.app_key, app.app_model, app.app_temperature)
            )

    # TODO: Probably should remove by the PK instead of `app_key`.
    def remove(self, user, app_key):
        self.db.execute(
            "DELETE FROM apps WHERE app_key=%s", (app_key,)
        )