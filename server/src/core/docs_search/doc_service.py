from core.common import conn
from core.docs_search.query import DocQuery
from core.llm.llm_service import LLMService


class Doc:
    def __init__(self, doc_id, title, text, score):
        self.id = doc_id
        self.title = title
        self.text = text
        self.score = score


class DocService:
    def __init__(self, llm_service: LLMService, db_conn):
        self.db_conn = db_conn
        self.llm_service = llm_service

    def search_docs(self, apps, text) -> list[Doc]:
        vector = self.llm_service.create_embedding(text)
        result = (DocQuery(self.db_conn).with_app(apps).with_vector("text_vector", vector).with_limit(3).search())
        docs = []
        for doc in result.docs:
            docs.append(Doc(doc.id, doc.title, doc.text, doc.vector_score))
        return docs


def doc_service_factory(llm: LLMService, db_conn) -> DocService:
    return DocService(llm, db_conn)
