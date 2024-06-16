from typing import List, Dict

from pydantic import BaseModel

from core.common.cache import CacheMemory
from core.common.pg import DBConnection
from core.history.history_dao import HistoryDao
from core.llm.prompt_handler import MessageCompletion, MessageRole


class AddHistoryDto(BaseModel):
    user_email: str
    app_key: str
    session_id: str
    message: MessageCompletion


class ChatHistoryService:
    def __init__(self, dao: HistoryDao):
        self.dao = dao
        self.history = CacheMemory(30)

    def add_message(self, req: AddHistoryDto):
        user_email = req.user_email
        app_key = req.app_key
        session_id = req.session_id

        if self.history.get(session_id) is None:
            self.history.put(session_id, [req.message])
        else:
            history = self.history.get(session_id)
            history.append(req.message)
            self.history.put(session_id, history)

        self.persist_message(user_email, app_key, req.message)

    def get_history(self, key):
        return self.history.get(key)

    def persist_message(self, user_email, app_key, message):
        is_bot_replay = message.role == MessageRole.ASSISTANT
        msg = message.response if is_bot_replay else message.query
        self.dao.persist_message(user_email, app_key, msg, is_bot_replay)

    def get_latest_messages(self, user_email: str, app_key: str, page: int) -> List[Dict]:
        return self.dao.get_latest_messages(user_email, app_key, page)


def factory_chat_history(pg_conn: DBConnection):
    dao = HistoryDao(pg_conn)
    return ChatHistoryService(dao)
