from core.common.config import OPENAI_API_KEY, OPENAI_API_MODEL_GPT3, OPENAI_API_MODEL_GPT4
from core.llm.openapi_client import LLMClientInterface, OpenAIClient


class LLMResponse:
    def __init__(self, message, usage, tools=None):
        self.tools = tools
        self.usage = usage
        self.message = message


class LLMService:

    def __init__(self, llm_client: LLMClientInterface, llm_pro: LLMClientInterface):
        self.llm_pro = llm_pro
        self.llm_basic = llm_client

    def infer_using_basic(self, messages: list[dict], functions=None) -> LLMResponse:
        predict = self.llm_basic.predict(messages, functions)
        return self._prepare_response(predict)

    @staticmethod
    def _prepare_response(predict):
        message = predict["choices"][0]["message"]
        tool_calls = message["tool_calls"] if "tool_calls" in message else None
        return LLMResponse(
            tools=tool_calls,
            message=message["content"],
            usage=[predict["usage"]]
        )

    def infer_using_pro(self, messages: list[dict], functions=None) -> LLMResponse:
        predict = self.llm_pro.predict(messages, functions)
        return self._prepare_response(predict)

    def create_embedding(self, text):
        return self.llm_basic.get_embeddings(text)


def llm_service_factory() -> LLMService:
    basic = OpenAIClient(OPENAI_API_KEY, OPENAI_API_MODEL_GPT3)
    pro = OpenAIClient(OPENAI_API_KEY, OPENAI_API_MODEL_GPT4)
    return LLMService(basic, pro)
