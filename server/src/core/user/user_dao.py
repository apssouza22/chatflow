# TODO: Remove this file.

from typing import Dict, Optional

from psycopg2 import IntegrityError  # FIXME: Does it work with SQLAlchemy?
from sqlalchemy.orm import Session

from pydantic import BaseModel

from core.common.file_db import FileDB
from core.scheme import ChatMessages, User


class UserDao:
    def __init__(self, pg_conn):
        self.db = pg_conn

    def get_all(self) -> Dict[str, User]:
        with Session(self.db) as session:
            return session.query(ChatMessages).all()

    def get_by_email(self, email: str) -> User:
        with Session(self.db) as session:
            return session.query(ChatMessages).filter_by(email=email).first()

    def add(self, user: User):
        try:
            with Session(self.db) as session:
                session.add(user)
        except IntegrityError as e:
            print("Inserting user:", e)
            return False

    def edit(self, user: User):
        try:
            with Session(self.db) as session:
                session.add(user)
        except IntegrityError as e:
            print("Updating user:", e)
            return False

    def remove(self, pk: int):
        User.query.filter_by(id=pk).delete()
