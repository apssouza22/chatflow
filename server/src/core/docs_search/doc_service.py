import typing

import numpy as np

from core.common import config, conn
from core.common.utils import filter_content
from core.cost.cost_dao import Cost
from core.cost.cost_service import CostService
from core.docs_search.dtos import SearchRequest
from core.docs_search.entities import ItemEntity
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
        results_text = await self._search_text(search_req, translated_text)

        results = _combine_scores(results_vector, results_text)
        entities = [await _map_doc_response(p) for p in results]
        contents = [p.get("item_metadata").get("text") for p in entities]

        if search_req.app_key != "3261034":  # disabled Connexled app
            option = self.llm_service.pick_best_doc(contents, translated_text)
            self._update_cost(option.usage, search_req.user_email, search_req.app_key)
            contents = filter_content(contents, option.message)

        return {
            'total': total.total,
            'entities': entities,
            'docs': contents
        }

    def _update_cost(self, usages: [Usage], user_email: str, app_key: str):
        for usage in usages:
            self.cost_service.put_cost(Cost(**usage.dict()), user_email, app_key)

    async def _search_text(self, search_req, translated_text) -> list:
        return []

        resp = self.llm_service.get_keywords(translated_text)
        self._update_cost(resp.usage, search_req.user_email, search_req.app_key)
        print("gpt keywords", resp.message)
        keywords = resp.message.split(",")
        return [item.strip() for item in keywords]
        text = "|".join(keywords)
        try:
            results_text = await self.text_search.search_text(text, search_req.tags)
        except:
            results_text = None
        return results_text

    async def get_metadata_by_app(self, app: str):
        return await self.text_search.get_by_tag(app)

    async def get_vector_docs_by_app(self, app: str) -> typing.Dict[str, typing.Any]:
        total = await self.vector_search.count_by_tag(app)
        results = await self.vector_search.search_by_tag(app)
        return {
            "total": total.total,
            "docs": results.docs
        }


def _combine_scores(results_vector, results_text):
    text_results = {}
    if results_text:
        for doc in results_text.docs:
            pk = doc.id.split(":")[-1]
            text_results[pk] = doc.score

    score_sum = sum(text_results.values())
    for index, score in text_results.items():
        text_results[index] = _normalize_score(score, score_sum)
    results = []

    for doc in results_vector.docs:
        text_score = text_results[doc.item_pk] if text_results.get(doc.item_pk) else 0
        results.append({
            "id": doc.id,
            "pk": doc.item_pk,
            # "combined_score": (0.8 * float(doc.vector_score)) - (0.2 * float(text_score)),
            "combined_score": float(doc.vector_score),
            "vector_score": doc.vector_score,
            "text_score": text_score
        })
    return sorted(results, key=lambda obj: obj['combined_score'], reverse=False)


def _normalize_score(number, max_number):
    if max_number < 0:
        raise ValueError("max_number must be greater or equal 0")

    normalized = number / max_number
    return normalized if 0 <= normalized <= 1 else 1.0 if normalized > 1 else 0.0


async def _map_doc_response(p):
    item = await ItemEntity.get(p["pk"])
    item_dict = item.dict()
    try:
        item_dict['similarity_score'] = p["vector_score"]
        item_dict['combined_score'] = p["combined_score"]
        item_dict['text_score'] = p["text_score"]
    except Exception as _:
        return item.dict()
    return item_dict


def factory_doc_search_service(llm_service: LLMService, cost_service: CostService) -> DocSearchService:
    redis_client = conn.get_redis_instance()
    metadata_index = config.INDEX_NAME + "_text"
    return DocSearchService(
        llm_service,
        cost_service,
        DocVectorSearch(redis_client, config.INDEX_NAME),
        TextSearch(redis_client, metadata_index),
    )
