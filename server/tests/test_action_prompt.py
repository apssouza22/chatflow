import unittest

from core.app.app_dao import App
from core.llm.prompt_handler import build_prompt_command,build_prompt_answer_questions, MessageCompletion


class TestPrompts(unittest.TestCase):
    def test_build_prompt_command(self):
        history = [
            MessageCompletion("user", "context 1", "query 1", ""),
            MessageCompletion("assistant", "context 1", "query", "response"),
            MessageCompletion("user", "context 1", "query 2", ""),
        ]
        build_prompt_command(history)

    def test_build_prompt_answer_questions_replace_existing_context(self):
        history = [
            MessageCompletion("user", "context 1", "query 1", ""),
            MessageCompletion("assistant", "", "query", "response"),
            MessageCompletion("user", "", "query 2", ""),
            MessageCompletion("assistant", "", "query", "response"),
            MessageCompletion("user", "context 1", "query 3", ""),
        ]

        prompt = build_prompt_answer_questions(history, App(**{
            "app_name": "test",
            "app_description": "test",
            "app_key": "test",
        }))

        self.assertTrue(prompt)

    def test_build_prompt_answer_questions_max_two_context(self):
        history = [
            MessageCompletion("user", "context 1", "query 1", ""),
            MessageCompletion("assistant", "", "", "response 1"),
            MessageCompletion("user", "contex 2", "query 2", ""),
            MessageCompletion("assistant", "", "", "response 2"),
            MessageCompletion("user", "context 3", "query 3", ""),
        ]

        prompt = build_prompt_answer_questions(history, App(**{
            "app_name": "test",
            "app_description": "test",
            "app_key": "test",
        }))

        self.assertTrue(prompt)
