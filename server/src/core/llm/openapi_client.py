import json
from typing import List

import requests

from core.common.config import OPENAI_BACKOFF, OPENAI_MAX_RETRIES
from core.common.http_retry import retry_with_exponential_backoff
from core.common.utils import EnumEncoder
from core.llm.llm_interface import LLMInterface
from core.llm.openai_errors import OpenAIRateLimitError, OpenAIError


class OpenAIClient(LLMInterface):
    """OpenAI API client."""

    def __init__(self, api_key, model="gpt-3"):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @retry_with_exponential_backoff(
        backoff_in_seconds=OPENAI_BACKOFF,
        max_retries=OPENAI_MAX_RETRIES,
        errors=(OpenAIRateLimitError, OpenAIError),
    )
    def predict(self, messages: List[dict], max_tokens=1000, temperature=0.1):
        """
        Call chatGpt completions.

        :param messages:
        :param max_tokens:
        :param temperature:
        :return:
        """

        completion_options = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1,
            "stream": False,
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            data=json.dumps(completion_options, cls=EnumEncoder),
            timeout=60,
        )
        # if request is unsuccessful and `status_code = 429` then,
        # raise rate limiting error else the OpenAIError
        if not response.ok:
            openai_error: OpenAIError
            if response.status_code == 429:
                openai_error = OpenAIRateLimitError(f"API rate limit exceeded: {response.text}")
            else:
                openai_error = OpenAIError(
                    f"OpenAI returned an error.\n"
                    f"Status code: {response.status_code}\n"
                    f"Response body: {response.text}",
                    status_code=response.status_code,
                )
            raise openai_error

        return response.json()

    def create_embeddings(self, inputs: List[str]) -> List[list]:
        data = {
            'input': inputs,
            'model': 'text-embedding-ada-002'
        }

        response = requests.post(f"{self.base_url}/embeddings", headers=self.headers, data=json.dumps(data))
        if response.status_code != 200:
            raise Exception(response.text)

        response_json = response.json()

        results = []
        for result in response_json['data']:
            results.append(result['embedding'])

        return results
