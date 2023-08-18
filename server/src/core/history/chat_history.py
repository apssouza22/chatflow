from typing import List, Dict

from psycopg2 import sql

from core.common.cache import CacheMemory
from core.common.pg import DBConnection
from core.history.history_dao import HistoryDao
from core.llm.prompt_handler import MessageCompletion, MessageRole


class ChatHistoryService:
    def __init__(self, dao: HistoryDao):
        self.dao = dao
        self.history = CacheMemory(30)

    def add_message(self, user_email, app_key, message: MessageCompletion):
        key = user_email + "_" + app_key
        if self.history.get(key) is None:
            self.history.put(key, [message])
        else:
            history = self.history.get(key)
            history.append(message)
            self.history.put(key, history)

        self.persist_message(user_email, app_key, message)

    def get_history(self, key):
        return self.history.get(key)

    def persist_message(self, user_email, app_key, message):
        is_bot_replay = message.role == MessageRole.ASSISTANT
        msg = message.response if is_bot_replay else message.query
        self.dao.persist_message(user_email, app_key, msg, is_bot_replay)

    def get_latest_messages(self, user_email: str, app_key: str) -> List[Dict]:
        return self.dao.get_latest_messages(user_email, app_key)


def factory_chat_history(pg_conn: DBConnection):
    dao = HistoryDao(pg_conn)
    return ChatHistoryService(dao)
