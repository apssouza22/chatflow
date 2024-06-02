from core.common import config, conn
from core.docs_search.doc_service import factory_doc_search_service
from core.llm.llm_service import llm_service_factory

redis_client = conn.get_redis_instance()
llm_service = llm_service_factory(config.OPENAI_API_KEY, config.OPENAI_API_MODEL_GPT3, config.OPENAI_API_MODEL_GPT4)
doc_search_service = factory_doc_search_service(llm_service)
