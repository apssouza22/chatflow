import typing

from core.docs_search.query import create_query, count, find_docs_by_tag_query

DEFAULT_RETURN_FIELDS = ["item_id", "vector_score", "title", "text_raw"]


class DocVectorSearch:
    """Use this class to search vectors in the Redis index"""

    def __init__(self, conn, index):
        self.index = index
        self.conn = conn

    async def search_vectors(self, tags, vector, limit=3):
        query = create_query(
            DEFAULT_RETURN_FIELDS,
            "KNN",
            limit,
            vector_field_name="openai_text_vector",
            tag=tags,
        )
        return await self.conn.ft(self.index).search(query, query_params={"vec_param": vector})

    async def count_by_tag(self, tags):
        count_query = count(tags)
        return await self.conn.ft(self.index).search(count_query)

    async def search_by_tag(self, app: str, limit=100):
        query = find_docs_by_tag_query(
            DEFAULT_RETURN_FIELDS,
            limit,
            tag=app,
        )
        return await self.conn.ft(self.index).search(query)
