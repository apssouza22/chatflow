import typing

import numpy as np
import redis
from redis.commands.search.query import Query

from core.common import config
from core.common.config import INDEX_NAME

redis_conn = redis.from_url(config.REDIS_URL)


class DocQuery:

    def __init__(self, db_conn):
        self.return_fields = ["item_id", "title", "text", "vector_score"]
        self.app = "*"
        self.limit = None
        self.vector_field = None
        self.vector = None
        self.db_conn = db_conn

    def with_vector(self, vector_field: str, vector: str):
        vector_bytes = np.array(vector, dtype=np.float32).tobytes()
        self.vector = vector_bytes
        self.vector_field = vector_field
        return self

    def with_limit(self, limit: int):
        self.limit = limit
        return self

    def with_app(self, app: str):
        self.app = f'@app:{{{app}}}'
        return self

    def with_return_fields(self, *fields: list[str]):
        self.return_fields = fields
        return self

    def _query(self):
        if self.vector:
            base_query = f'{self.app}=>[KNN {self.limit} @{self.vector_field} $vec_param AS vector_score]'
        else:
            base_query = f''

        query_builder = Query(base_query).paging(0, self.limit).return_fields(*self.return_fields)

        if self.vector:
            query_builder.sort_by("vector_score")

        return (
            query_builder
            .dialect(2)
        )

    def search(self) -> dict:
        query = self._query()
        print(query.query_string())
        params = {}
        if self.vector:
            params = {"vec_param": self.vector}
        return self.db_conn.ft(INDEX_NAME).search(query, query_params=params)


def search_docs(apps, vector, limit=3) -> dict:
    return (DocQuery(redis_conn)
            .with_app(apps)
            .with_vector("text_vector", vector)
            .with_limit(limit)
            .search())

