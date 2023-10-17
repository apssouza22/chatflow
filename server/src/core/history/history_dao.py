from typing import List, Dict
from core.common import pg_conn
import sqlalchemy
from sqlalchemy.orm import Session

from core.scheme import ChatMessages


class HistoryDao:
    def __init__(self, db: sqlalchemy.engine.base.Engine):
        self.db = db

    def persist_message(self, user_ref, app_key, msg, is_bot_replay):
        self.db.insert(
            "chat_messages",
            user_ref=user_ref,
            chatbot_id=app_key,
            message=msg,
            is_bot_reply=is_bot_replay,
        )

    def get_latest_messages(self, user_ref: str, app_key: str) -> List[Dict]:
        with Session(self.db) as session:
            objs = session.query(ChatMessages).filter_by(chatbot_id=app_key).filter_by(user_ref=user_ref).all()
        # Convert objs to dicts:
        return [obj.__dict__ for obj in objs]  # It somehow sucks to convert objects to dicts in a DAO class.
