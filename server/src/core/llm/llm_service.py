from typing import List

from core.app.app_dao import App
from core.common.utils import filter_content
from core.llm.dtos import LLMResponse, Usage
from core.llm.openai_stream import OpenAIStream
from core.llm.openapi_client import OpenAIClient
from core.llm.prompt_handler import build_prompt_answer_questions, build_prompt_command, MessageCompletion, is_text_or_form_prompt, get_prompt_objs_from_history, prompt_pick_content


class LLMService:

    def __init__(self, cheap_model: OpenAIClient, expensive_model: OpenAIClient, completion_stream: OpenAIStream):
        self.completion_stream = completion_stream
        self._cheap_model = cheap_model
        self._expensive_model = expensive_model

    def _use_cheap(self, prompts, temperature=0.1) -> LLMResponse:
        print("gpt3 prompt", prompts)
        response = self._cheap_model.predict(prompts, temperature=temperature)
        print("gpt3 response successfuly")
        return self._handle_model_response(response)

    def _use_expensive(self, prompts: List[dict], temperature=0.1) -> LLMResponse:
        print("gpt4 prompt", prompts)
        response = self._expensive_model.predict(prompts, temperature=temperature)
        return self._handle_model_response(response)

    @staticmethod
    def _handle_model_response(response):
        usage = response["usage"]
        usage["model"] = response["model"]
        return LLMResponse(
            usage=[Usage(**usage)],
            message=response["choices"][0]["message"]["content"]
        )

    def get_completions_stream(self, prompts: List[dict], model, temperature):
        return self.completion_stream.get_chat_completions(prompts, model=model, temperature=temperature)

    def get_task_command(self, history: List[MessageCompletion], app: App) -> LLMResponse:
        prompts = build_prompt_command(history)
        return self._use_cheap(prompts, app.app_temperature)

    def get_question_answer(self, user_input: str, app: App, history: List[MessageCompletion]) -> LLMResponse:
        prompts, usages = self.get_question_prompts(app, history, user_input)

        if app.app_model == "gpt4":
            resp = self._use_expensive(prompts, app.app_temperature)
        else:
            resp = self._use_cheap(prompts, app.app_temperature)
        usages.append(resp.usage[0])
        return LLMResponse(
            usage=usages,
            message=resp.message
        )

    def get_question_prompts(self, app, history, user_input: str):
        contents, msgs = get_prompt_objs_from_history(history)
        usages = []
        if len(contents) > 1:
            option = self.pick_best_doc(contents, user_input)
            contents = filter_content(contents, option.message)
            usages.append(option.usage[0])
        prompts = build_prompt_answer_questions(app, contents, msgs)
        return prompts, usages

    def pick_best_doc(self, contents, user_input: str) -> LLMResponse:
        pick_content_prompt = prompt_pick_content(contents, user_input)
        return self._use_cheap(pick_content_prompt)

    def get_text_or_form(self, text: str):
        prompt = is_text_or_form_prompt(text)
        return self._use_expensive(prompt)

    def call_ai_function(self, function, args, description) -> str:
        return self._cheap_model.call_ai_function(function, args, description)

    def embed_text(self, text: str) -> List[list]:
        return self._cheap_model.create_embeddings([text])

    def audio_to_text(self, audio: str) -> str:
        return self._cheap_model.transcriptions(audio)

    def translate(self, text) -> LLMResponse:
        prompt = f"Translate the user input into english. User input: {text} \n\nTranslated:"
        return self._use_cheap([{"role": "user", "content": prompt}])

    def get_keywords(self, text: str) -> LLMResponse:
        prompt = f"Extract keywords for a search query from the text provided. " \
                 f"Include synonyms for words where a more common one exists." \
                 f"IMPORTANT: separate the keywords with ',' " \
                 f"\n\nText: {text} \n\nKeywords:"

        return self._use_cheap([{"role": "user", "content": prompt}])


def llm_service_factory(app_key: str, gpt3_model: str, gpt4_model: str) -> LLMService:
    return LLMService(
        OpenAIClient(app_key, gpt3_model),
        OpenAIClient(app_key, gpt4_model),
        OpenAIStream(app_key),
    )
