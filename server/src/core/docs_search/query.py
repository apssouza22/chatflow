import typing

import numpy as np
import redis
from redis.commands.search.query import Query

from core.common import config
from core.common.config import INDEX_NAME

redis_conn = redis.from_url(config.REDIS_URL)


def search_docs(apps, vector, limit=3) -> dict:
    vector_bytes = np.array(vector, dtype=np.float32).tobytes()
    query = create_query_vector(limit, apps)
    return redis_conn.ft(INDEX_NAME).search(query, query_params={"vec_param": vector_bytes})


def create_query_vector(number_of_results: int, tag: typing.Optional[str] = None) -> dict:
    return_fields = ["item_id", "title", "text", "vector_score"]
    search_type = "KNN"
    vector_field_name = "text_vector"
    tag_query = "*"
    if tag:
        tag_query = f"@app:{{{tag}}}"

    base_query = f'{tag_query}=>[{search_type} {number_of_results} @{vector_field_name} $vec_param AS vector_score]'
    query = (
        Query(base_query)
        .sort_by("vector_score")
        .paging(0, number_of_results)
        .return_fields(*return_fields)
        .dialect(2)
    )
    print(query.query_string())
    return query
