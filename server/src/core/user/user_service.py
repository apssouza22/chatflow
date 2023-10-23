from typing import List

from psycopg2 import IntegrityError

from core.app.app_dao import AppDao
from core.user.user_dao import UserDao, User


class UserService:
    def __init__(self, user_storage: UserDao, app_dao: AppDao):
        self.app_dao = app_dao
        self.dao = user_storage
        try:
            self.add_user(User(name="Alex", password="123", email="admin@gmail.com"))
            self.dao.db.conn.commit()
        except IntegrityError as e:
            print("IGNORED EXCEPTION", e)  # TODO: Remove this line.
            self.dao.db.conn.rollback()

    def authenticate_user(self, email, password):
        print("AAA", email)
        user = self.dao.get_by_email(email)
        if user is None:
            return None
        if user.password == password:
            return user

        return None

    # TODO: wrong responsibility
    def exists_app(self, email: str, app_key: str) -> bool:
        app = self.app_dao.get_by_id(email, app_key)
        if app is None:
            return False
        return True

    def get_user_by_email(self, email):
        return self.dao.get_by_email(email)

    def add_user(self, user: User):
        self.dao.add(user)

    # TODO: Should be removed.
    def get_all_users(self) -> List[User]:
        users = self.dao.get_all().values()
        for user in users:
            user.password = None
        return list(users)
