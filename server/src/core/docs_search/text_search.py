from core.docs_search.query import create_text_query


class TextSearch:
    def __init__(self, conn, index):
        self.conn = conn
        self.index = index

    async def get_by_tag(self, tag: str, limit=100):
        query_text = create_text_query(
            ["title", "text"],
            text_search="",
            tag=tag,
            number_of_results=limit,
        )

        return await self.conn.ft(self.index).search(query_text)

    async def search_text(self, text, tag, limit=3) -> list:
        query_text = create_text_query(
            ["title", "text"],
            text_search=text,
            tag=tag,
            number_of_results=limit,
        )
        return await self.conn.ft(self.index).search(query_text)
