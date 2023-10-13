from typing import Dict

from pydantic import BaseModel

from core.common.file_db import FileDB


class User(BaseModel):
    pk: int
    email: str
    password: str
    name: str = None


# FIXME: rewrite with DB.
class UserDao:
    def __init__(self):
        self.db = FileDB('./file_db/users')

    def get_all(self) -> Dict[str, User]:
        users = self.db.get("all")
        print("USERS: ", users)
        if users is None:
            return {}
        return users

    def get(self, user) -> User:
        return self.get_all().get(user)

    def add(self, user: User):
        if self.get(user.email) is not None:
            return False

        users = self.get_all()
        users[user.email] = user

        self.db.put("all", users)

    def edit(self, user: User):
        users = self.get_all()
        if users.get(user.email) is None:
            return False
        users[user.email] = user
        self.db.put("all", users)

    def remove(self, user: str):
        if self.get(user) is None:
            return False
        users = self.get_all()
        del users[user]
        self.db.put("all", users)
