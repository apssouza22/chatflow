import unittest

from core.common import conn
from core.docs_search.utils import remove_content_between_backticks

redis_client = conn.get_redis_instance()


class TestUtils(unittest.TestCase):
    def test_remove_content(self):
        input = "Edit application with the following: `app_name=APP_NAME; app_description=APP_DESC; app_key=11788285; app_user=apssouza22@gmail.com; app_model=`"
        text = remove_content_between_backticks(input)
        print(text)
