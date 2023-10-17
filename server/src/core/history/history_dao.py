from typing import List, Dict
from core.common import pg_conn

import sqlalchemy


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
        with Session(engine) as session:
            return session.execute(select(chat_messages).where(chat_messages.chatbot_id == app_key).where(
                chat_messages.user_ref == user_ref).order_by(chat_messages.c.createdat.desc()).limit(50)).fetchall()
        return self.db.fetch_all(
                """
                SELECT * FROM chat_messages where chatbot_id = %s and user_ref = %s
                ORDER BY createdat DESC
                LIMIT 50
                """,
                (app_key, user_ref),
            ).fetchall()
