import os
from typing import List

from pydantic import BaseModel

from core.app.app_dao import App
from core.common.utils import filter_content
from core.llm.openapi_client import OpenAI
from core.llm.prompt_handler import build_prompt_answer_questions, build_prompt_command, MessageCompletion, prompt_text_form, get_prompt_objs_from_history, prompt_pick_content


class Usage(BaseModel):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    model: str


class LLMResponse(BaseModel):
    usage: List[Usage]
    message: str


class LLMService:

    def __init__(self, gpt3: OpenAI, gpt4: OpenAI):
        self.openai_api_gpt3 = gpt3
        self.openai_api_gpt4 = gpt4

    def _gpt3(self, prompts, temperature=0.1) -> LLMResponse:
        print("gpt3 prompt", prompts)
        response = self.openai_api_gpt3.get_chat_completions(prompts, temperature=temperature)
        usage = response["usage"]
        usage["model"] = response["model"]
        return LLMResponse(
            usage=[Usage(**usage)],
            message=response["choices"][0]["message"]["content"]
        )

    def _gpt4(self, prompts: List[dict], temperature=0.1) -> LLMResponse:
        print("gpt4 prompt", prompts)
        response = self.openai_api_gpt4.get_chat_completions(prompts, temperature=temperature)
        usage = response["usage"]
        usage["model"] = response["model"]
        return LLMResponse(
            usage=[Usage(**usage)],
            message=response["choices"][0]["message"]["content"]
        )

    def get_task_command(self, history: List[MessageCompletion], app: App) -> LLMResponse:
        prompts = build_prompt_command(history)
        return self._gpt3(prompts, app.app_temperature)

    def get_question_answer(self, user_input: str, app: App, history: List[MessageCompletion]) -> LLMResponse:
        contents, msgs = get_prompt_objs_from_history(history)
        usages = []
        if len(contents) > 1:
            option = self.pick_best_doc(contents, user_input)
            contents = filter_content(contents, option.message)
            usages.append(option.usage[0])

        prompts = build_prompt_answer_questions(app, contents, msgs)

        if app.app_model == "gpt3":
            resp = self._gpt3(prompts, app.app_temperature)
        else:
            resp = self._gpt4(prompts, app.app_temperature)
        usages.append(resp.usage[0])
        return LLMResponse(
            usage=usages,
            message=resp.message
        )

    def pick_best_doc(self, contents, user_input) -> LLMResponse:
        pick_content_prompt = prompt_pick_content(contents, user_input)
        return self._gpt3(pick_content_prompt)

    def get_text_or_form(self, text: str):
        prompt = prompt_text_form(text)
        return self._gpt4(prompt)

    def call_ai_function(self, function, args, description) -> str:
        return self.openai_api_gpt3.call_ai_function(function, args, description)

    def embed_text(self, text: str) -> List[list]:
        return self.openai_api_gpt3.create_openai_embeddings([text])

    def translate(self, text) -> LLMResponse:
        prompt = f"Translate the user input into english. User input: {text} \n\nTranslated:"
        return self._gpt3([{"role": "user", "content": prompt}])

    def get_keywords(self, text: str) -> LLMResponse:
        prompt = f"Extract keywords for a search query from the text provided. " \
                 f"Include synonyms for words where a more common one exists." \
                 f"IMPORTANT: separate the keywords with ',' " \
                 f"\n\nText: {text} \n\nKeywords:"

        return self._gpt3([{"role": "user", "content": prompt}])


def llm_service_factory(app_key_gpt3: str, app_key_gpt4: str) -> LLMService:
    return LLMService(
        OpenAI(app_key_gpt3, "gpt-3.5-turbo-0613"),
        OpenAI(app_key_gpt4, "gpt-4"),
    )
