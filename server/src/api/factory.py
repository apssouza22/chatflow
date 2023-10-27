from core.agent.agent_service import agent_factory
from core.app.app_dao import AppDao
from core.common import config, conn
from core.history.chat_history import ChatHistoryService, factory_chat_history
from core.cost.cost_service import cost_service_factory
from core.docs_search.doc_service import factory_doc_search_service
from core.llm.llm_service import llm_service_factory
from core.user.user_dao import UserDao
from core.user.user_service import UserService

redis_client = conn.get_redis_instance()
pg_conn = conn.get_pg_instance()
cost_service = cost_service_factory()
llm_service = llm_service_factory(config.OPENAI_API_KEY_GPT3, config.OPENAI_API_KEY_GPT4)
doc_search_service = factory_doc_search_service(llm_service, cost_service)
chat_history = factory_chat_history(pg_conn)
agent = agent_factory(chat_history, cost_service, llm_service)
apps = AppDao(pg_conn)
user_service = UserService(UserDao(pg_conn), apps)
current_session = {}
