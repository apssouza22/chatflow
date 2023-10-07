import json
from typing import List

import requests

from core.common.config import OPENAI_BACKOFF, OPENAI_MAX_RETRIES
from core.common.http_retry import retry_with_exponential_backoff
from core.common.utils import EnumEncoder
from core.llm.openai_errors import OpenAIRateLimitError, OpenAIError


class OpenAIStream:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            'Accept': 'text/event-stream',
        }

    @retry_with_exponential_backoff(
        backoff_in_seconds=OPENAI_BACKOFF,
        max_retries=OPENAI_MAX_RETRIES,
        errors=(OpenAIRateLimitError, OpenAIError),
    )
    def get_chat_completions(self, messages: List[dict], model: str, max_tokens=1000, temperature=0.1):
        str_model = "gpt-3.5-turbo-0613"
        if model == "gpt4":
            str_model = "gpt-4"

        completion_options = {
            "model": str_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1,
            "stream": True,
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            data=json.dumps(completion_options, cls=EnumEncoder),
            stream=True,
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

        return response
