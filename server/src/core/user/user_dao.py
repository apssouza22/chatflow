from typing import Dict, Optional

from psycopg2 import IntegrityError

from pydantic import BaseModel

from core.common.file_db import FileDB


class User(BaseModel):
    pk: Optional[int] = None
    email: str
    password: str  # TODO: encrypted password
    name: str = None


class UserDao:
    def __init__(self, pg_conn):
        self.db = pg_conn

    def get_all(self) -> Dict[str, User]:
        users = self.db.fetch_all("SELECT * FROM users")
        return [User(**u) for u in users]

    def get_by_email(self, email: str) -> User:
        user = self.db.fetch_one("SELECT * FROM users WHERE email=%s", (email,))
        return User(**user)

    def add(self, user: User):
        try:
            self.db.execute(
                "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)",
                (user.email, user.password, user.name)
            )
        except IntegrityError as e:
            print("Inserting user:", e)
            return False

    def edit(self, user: User):
        try:
            self.db.execute(
                "UPDATE users SET email=%s, password=%s, name=%s",
                (user.email, user.password, user.name)
            )
        except IntegrityError as e:
            print("Updating user:", e)
            return False

    def remove(self, pk: int):
        self.db.execute(
            "DELETE FROM users WHERE id=%s",
            (pk,)
        )
