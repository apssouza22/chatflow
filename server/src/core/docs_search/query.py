import typing

import numpy as np
import redis
from redis.commands.search.query import Query

from core.common import config
from core.common.config import INDEX_NAME


def create_query(
        number_of_results: int = 20,
        tag: typing.Optional[str] = None
):
    return_fields: list[str] = ["item_id", "title", "text", "vector_score"]
    search_type: str = "KNN"
    vector_field_name: str = "text_vector"
    tag_query = "*"
    if tag:
        tag_query = f"(@app:{{{tag}}})"

    base_query = f'{tag_query}=>[{search_type} {number_of_results} @{vector_field_name} $vec_param AS vector_score]'
    query = (Query(base_query).
             sort_by("vector_score").
             paging(0, number_of_results).
             return_fields(*return_fields).
             dialect(2))
    print(query.get_args())
    print(query.query_string())
    return query


redis_conn = redis.from_url(config.REDIS_URL)


def search_vectors(tags, vector, limit=3):
    query = create_query(limit, tags)
    vector_bytes = np.array(vector, dtype=np.float32).tobytes()
    return redis_conn.ft(INDEX_NAME).search(query, query_params={"vec_param": vector_bytes})
