from core.common.config import OPENAI_API_KEY, OPENAI_API_MODEL_GPT3
from core.llm.openapi_client import LLMClientInterface, OpenAIClient


class LLMService:

    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client

    def infer(self, messages: list[dict]):
        return self.llm_client.predict(messages)

    def create_embedding(self, text):
        return self.llm_client.get_embeddings(text)


def llm_service_factory() -> LLMService:
    return LLMService(OpenAIClient(OPENAI_API_KEY, OPENAI_API_MODEL_GPT3))
