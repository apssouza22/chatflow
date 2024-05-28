import typing

import numpy as np

from core.common import config, conn
from core.common.utils import filter_content
from core.cost.cost_dao import Cost
from core.cost.cost_service import CostService
from core.docs_search.dtos import SearchRequest
from core.docs_search.text_search import TextSearch
from core.docs_search.utils import remove_content_between_backticks
from core.docs_search.vector_search import DocVectorSearch
from core.llm.llm_service import LLMService, Usage


class DocSearchService:
    def __init__(self, llm_service: LLMService, cost_service, vector_search: DocVectorSearch, text_search: TextSearch):
        self.cost_service = cost_service
        self.text_search = text_search
        self.vector_search = vector_search
        self.llm_service = llm_service

    async def full_search(self, search_req: SearchRequest) -> typing.Dict[str, typing.Any]:
        """ Search docs combining multiple strategies"""

        clean_text = remove_content_between_backticks(search_req.text)
        translate_resp = self.llm_service.translate(clean_text)
        self._update_cost(translate_resp.usage, search_req.user_email, search_req.app_key)
        translated_text = translate_resp.message
        vector = self.llm_service.embed_text(translated_text)[0]
        vector_bytes = np.array(vector, dtype=np.float32).tobytes()

        results_vector = await self.vector_search.search_vectors(search_req.tags, vector_bytes)
        total = await self.vector_search.count_by_tag(search_req.tags)

        results = _filter_invalid_data(results_vector)
        contents = [r.get("text") for r in results]

        option = self.llm_service.pick_best_doc(contents, translated_text)
        self._update_cost(option.usage, search_req.user_email, search_req.app_key)
        contents = filter_content(contents, option.message)

        return {
            'total': total.total,
            'entities': results,
            'docs': contents
        }

    def _update_cost(self, usages: [Usage], user_email: str, app_key: str):
        for usage in usages:
            self.cost_service.put_cost(Cost(**usage.dict()), user_email, app_key)

    async def get_metadata_by_app(self, app: str):
        return await self.text_search.get_by_tag(app)

    async def get_vector_docs_by_app(self, app: str) -> typing.Dict[str, typing.Any]:
        total = await self.vector_search.count_by_tag(app)
        results = await self.vector_search.search_by_tag(app)
        return {
            "total": total.total,
            "docs": results.docs
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


def _normalize_score(number, max_number):
    if max_number < 0:
        raise ValueError("max_number must be greater or equal 0")

    normalized = number / max_number
    return normalized if 0 <= normalized <= 1 else 1.0 if normalized > 1 else 0.0


def factory_doc_search_service(llm_service: LLMService, cost_service: CostService) -> DocSearchService:
    redis_client = conn.get_redis_instance()
    metadata_index = config.INDEX_NAME + "_text"
    return DocSearchService(
        llm_service,
        cost_service,
        DocVectorSearch(redis_client, config.INDEX_NAME),
        TextSearch(redis_client, metadata_index),
    )
