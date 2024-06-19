from typing import List

import requests

from core.common.config import OPENAI_BACKOFF, OPENAI_MAX_RETRIES
from core.common.http_retry import retry_with_exponential_backoff
from core.llm.utils import OpenAIRateLimitError, OpenAIError


class LLMClientInterface:
    def predict(self, messages: List[dict], max_tokens=1000, temperature=0.1):
        raise NotImplementedError

    def get_embeddings(self, input_param: str) -> List[list]:
        raise NotImplementedError


class OpenAIClient(LLMClientInterface):

    def __init__(self, api_key: str, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    @retry_with_exponential_backoff(
        backoff_in_seconds=OPENAI_BACKOFF,
        max_retries=OPENAI_MAX_RETRIES,
        errors=(OpenAIRateLimitError, OpenAIError),
    )
    def predict(self, messages: List[dict], max_tokens=1000, temperature=0.1):
        endpoint = "/chat/completions"
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            json=data,
            timeout=60
        )
        if not response.ok:
            openai_error: OpenAIError
            if response.status_code == 429:
                openai_error = OpenAIRateLimitError(response.text)
            else:
                openai_error = OpenAIError(response.text)

            raise openai_error

        return response.json()

    def get_embeddings(self, input_param: List[str]) -> List[list]:
        endpoint = "/embeddings"
        data = {
            "input": input_param,
            "model": "text-embedding-3-small"
        }
        response = requests.post(self.base_url + endpoint, headers=self.headers, json=data)
        if response.status_code != 200:
            raise Exception(response.text)

        response_json = response.json()
        results = []
        for item in response_json["data"]:
            results.append(item["embedding"])

        return results
