import time

import openai


def completion():
    start_time = time.time()

    # send a ChatCompletion request to count to 100
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': 'Count to 100, with a comma between each number and no newlines. E.g., 1, 2, 3, ...'}
        ],
        temperature=0,
        stream=True  # again, we set stream=True
    )

    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        collected_messages.append(chunk_message)  # save the message
        print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text

    # print the time delay and text received
    print(f"Full response received {chunk_time:.2f} seconds after request")
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    print(f"Full conversation received: {full_reply_content}")


# OpenAI API http client
import json
from typing import List

import requests

from core.common.config import OPENAI_BACKOFF, OPENAI_MAX_RETRIES
from core.common.http_retry import retry_with_exponential_backoff
from core.common.utils import EnumEncoder
from core.llm.openai_errors import OpenAIRateLimitError, OpenAIError


class OpenAIStream:

    def __init__(self, api_key, model="gpt-3"):
        self.model = model
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
    def get_chat_completions(self, messages: List[dict], max_tokens=500, temperature=0.1):
        """
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
