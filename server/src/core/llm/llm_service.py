from typing import List

from pydantic import BaseModel

from core.llm.openapi_client import OpenAIClient


class Usage(BaseModel):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    model: str


class LLMResponse(BaseModel):
    usage: List[Usage]
    message: str


class LLMService:

    def __init__(self, cheap_model: OpenAIClient, expensive_model: OpenAIClient):
        self.cheap_model = cheap_model
        self.expensive_model = expensive_model

    def _use_cheap(self, prompts, temperature=0.1) -> LLMResponse:
        response = self.cheap_model.predict(prompts, temperature=temperature)
        return self._model_response(response)

    def _use_expensive(self, prompts: List[dict], temperature=0.1) -> LLMResponse:
        response = self.expensive_model.predict(prompts, temperature=temperature)
        return self._model_response(response)

    def _model_response(self, response):
        usage = response["usage"]
        usage["model"] = response["model"]
        return LLMResponse(
            usage=[Usage(**usage)],
            message=response["choices"][0]["message"]["content"]
        )

    def embed_text(self, text: str) -> List[list]:
        return self.cheap_model.create_embeddings([text])

    def get_prediction(self, prompts: List[dict], model: str = "cheap", temperature: float = 0.1) -> LLMResponse:
        if model == "cheap":
            return self._use_cheap(prompts, temperature)
        else:
            return self._use_expensive(prompts, temperature)


def llm_service_factory(app_key: str, gpt3_model: str, gpt4_model: str) -> LLMService:
    return LLMService(
        OpenAIClient(app_key, gpt3_model),
        OpenAIClient(app_key, gpt4_model),
    )
