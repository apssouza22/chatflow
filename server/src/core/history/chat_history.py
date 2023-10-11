from typing import List, Dict

from pydantic import BaseModel

from core.common.cache import CacheMemory
from core.common.pg import DBConnection
from core.history.history_dao import HistoryDao
from core.llm.prompt_handler import MessageCompletion, MessageRole
from core.common import conn


class AddMessageDto(BaseModel):
    user_email: str
    app_key: str
    session_id: str
    message: MessageCompletion


# TODO: Explain in a comment, why we use both HistoryDAO and Redis persistence.
class ChatHistoryService:
    def __init__(self, dao: HistoryDao, redis):
        self.dao = dao
        self.redis = redis

    async def add_message(self, req: AddMessageDto):
        user_email = req.user_email
        app_key = req.app_key
        session_id = req.session_id

        list_len = await self.redis.llen("chat_history_cache:" + key)
        self.redis.hset("chat_history_cache:" + key, list_len, message)  # add to the end of the list

        self.persist_message(user_email, app_key, req.message)

    async def get_history(self, key):
        return await self.redis.hgetall("chat_history_cache:" + key)

    def persist_message(self, user_email, app_key, message):
        is_bot_replay = message.role == MessageRole.ASSISTANT
        msg = message.response if is_bot_replay else message.query
        self.dao.persist_message(user_email, app_key, msg, is_bot_replay)

    def get_latest_messages(self, user_email: str, app_key: str, page: int) -> List[Dict]:
        return self.dao.get_latest_messages(user_email, app_key, page)


def factory_chat_history(pg_conn: DBConnection):
    dao = HistoryDao(pg_conn)
    return ChatHistoryService(dao, conn.get_redis_instance())
