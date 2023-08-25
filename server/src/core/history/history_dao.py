from typing import List, Dict

from psycopg2 import sql

from core.common.pg import DBConnection


class HistoryDao:
    def __init__(self, db: DBConnection):
        self.db = db

    def persist_message(self, user_email, app_key, msg, is_bot_replay):
        #TODO: Disable Postgres integration until we create the script to create the necessary table
        return
        insert_query = sql.SQL(
            """
            INSERT INTO chat_messages(user_id, chatbot_id, message, is_bot_reply)
            VALUES(%s, %s, %s, %s)
            """
        )
        self.db.execute(insert_query, (user_email, app_key, msg, is_bot_replay))

    def get_latest_messages(self, user_email: str, app_key: str) -> List[Dict]:
        #TODO: Disable Postgres integration until we create the script to create the necessary table
        return []
        return self.db.fetch_all(
            """
            SELECT * FROM chat_messages where chatbot_id = %s and user_id = %s
            ORDER BY createdat DESC
            LIMIT 50
            """,
            (app_key, user_email),
        )
