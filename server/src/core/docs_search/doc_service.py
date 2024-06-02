import typing

import numpy as np

from core.common import config, conn
from core.docs_search.dtos import SearchRequest
from core.docs_search.text_search import TextSearch
from core.docs_search.utils import remove_content_between_backticks
from core.docs_search.vector_search import DocVectorSearch
from core.llm.llm_service import LLMService


class DocSearchService:
    """Service to search documents using multiple strategies."""

    def __init__(self, llm_service: LLMService, vector_search: DocVectorSearch, text_search: TextSearch):
        self.llm_service = llm_service
        self.text_search = text_search
        self.vector_search = vector_search

    async def full_search(self, search_req: SearchRequest) -> typing.Dict[str, typing.Any]:
        """ Search docs combining multiple strategies"""
        clean_text = remove_content_between_backticks(search_req.text)
        vector = self.llm_service.embed_text(clean_text)[0]
        vector_bytes = np.array(vector, dtype=np.float32).tobytes()

        results_vector = await self.vector_search.search_vectors(search_req.tags, vector_bytes)
        total = await self.vector_search.count_by_tag(search_req.tags)

        results = _filter_invalid_data(results_vector)
        contents = [r.get("text") for r in results]

        return {
            'total': total.total,
            'entities': results,
            'docs': contents
        }


def _filter_invalid_data(results_vector):
    results = []
    for doc in results_vector.docs:
        if not hasattr(doc, 'title'):
            continue
        results.append({
            "id": doc.id,
            "combined_score": float(doc.vector_score),
            "vector_score": doc.vector_score,
            "item_id": doc.item_id,
            "title": doc.title,
            "text": doc.text_raw,
        })
    return results


def factory_doc_search_service(llm_service: LLMService) -> DocSearchService:
    redis_client = conn.get_redis_instance()
    metadata_index = config.INDEX_NAME + "_text"
    return DocSearchService(
        llm_service,
        DocVectorSearch(redis_client, config.INDEX_NAME),
        TextSearch(redis_client, metadata_index),
    )
