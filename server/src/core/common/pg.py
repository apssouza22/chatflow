from typing import List, Dict

import psycopg2


class DBConnection:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("PostgreSQL connection is closed")

    def fetch_all(self, query: str, params=None) -> List[Dict]:
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        # Convert rows to list of dictionaries so they're easier to work with
        cols = [desc[0] for desc in self.cursor.description]
        result = []
        for row in rows:
            result.append(dict(zip(cols, row)))
        return result
