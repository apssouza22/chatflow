import asyncio
import unittest

from api.docs import items_from_results
from core.common import conn, config
from core.docs_search.query import find_docs_by_tag_query, count
from core.docs_search.dtos import DEFAULT_RETURN_FIELDS

redis_client = conn.get_redis_instance()

class TestMemoryEmbedder(unittest.TestCase):
    def test_search(self):
        def sort_objects_by_score_desc(objects_list):
            sorted_list = sorted(objects_list, key=lambda obj: obj['score'], reverse=True)
            return sorted_list

        # Example usage:
        objects_list = [
            {'score': 90, 'name': 'Alice'},
            {'score': 75, 'name': 'Bob'},
            {'score': 80, 'name': 'Charlie'},
        ]

        sorted_objects = sort_objects_by_score_desc(objects_list)
        print(sorted_objects)
