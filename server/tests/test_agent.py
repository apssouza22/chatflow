import unittest
from unittest.mock import MagicMock, Mock

import pytest

from core.agent.agent_service import AgentService, UserInputDto
from core.app.app_dao import App
from core.scheme import User


class AgentTestCase(unittest.TestCase):

    @pytest.fixture
    def agent_service(self):
        history = Mock()
        cost_service = Mock()
        llm = Mock()
        cache = Mock()
        return AgentService(history, cost_service, llm, cache)

    def test_is_action_with_question_mark(self):
        history = Mock()
        cost_service = Mock()
        llm = Mock()
        cache = Mock()
        agent_service = AgentService(history, cost_service, llm, cache)
        user = User(email="", password="")  # Populate with relevant data
        app = App(app_key="some_key", app_user="", app_model="",app_name="",app_description="")
        req = UserInputDto(user=user, context="", question="Is this a question?", is_plugin_mode=False, app=app)
        assert not agent_service.is_action(req)

    # ... other tests as before

    def test_is_action_with_text_form(self, agent_service):
        agent_service.llm.get_text_or_form.return_value.message = "form"
        user = User()  # Populate with relevant data
        app = App(app_key="some_key")  # Populate with relevant data
        req = UserInputDto(user=user, context="", question="Not a question.", is_plugin_mode=False, app=app)
        assert agent_service.is_action(req)
        agent_service.llm.get_text_or_form.assert_called_once_with(req.question)
        agent_service.update_cost.assert_called_once()  # Add specific call parameters if needed


if __name__ == '__main__':
    unittest.main()
