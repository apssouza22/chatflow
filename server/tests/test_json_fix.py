import json
import unittest

from core.llm.chat_response_handler import replace_single_quotes_to_value_with_objects, add_quotes_to_property_names, extract_longest_curly_braces_content


class TestMemoryEmbedder(unittest.TestCase):

    def test_replace_single_quotes_to_value_with_objects(self):
        result = replace_single_quotes_to_value_with_objects("""{
	"command": {
		"name": "api_call",
		"args": {
			"url": "https://api.github.com/user/repos",
			"method": "POST",
			"data_request": '{"name":"test repo","private":true,"allow_squash_merge":true}',
			"headers": {
				"Accept": "application/vnd.github+json",
				"Authorization": "Bearer <YOUR-TOKEN>",
				"X-GitHub-Api-Version": "2022-11-28"
			}
		}
	}
}
    """)
        d = json.loads(result)
        self.assertEqual(d["command"]["args"]["data_request"], json.loads('{"name":"test repo","private":true,"allow_squash_merge":true}'))


    def test_add_quotes_to_property_names(self):
        result = add_quotes_to_property_names("""{
        "command": {
            name: "api_call",
            "args": {
                "url": "https://api.github.com/user/repos"
            }
        }
    }
        """)
        d = json.loads(result)
        self.assertEqual(d["command"]["args"]["data_request"], json.loads('{"name":"test repo","private":true,"allow_squash_merge":truexx}'))

    def test_add_quotes_to_property_names(self):
        result = extract_longest_curly_braces_content(""" some text before json{
        "command": {
            "name": "api_call",
            "args": {
                "url": "https://api.github.com/user/repos"
            }
        }
    }
        """)
        d = json.loads(result)
        self.assertEqual(json.dumps(d), json.dumps({'command': {'name': 'api_call', 'args': {'url': 'https://api.github.com/user/repos'}}}))


if __name__ == '__main__':
    unittest.main()
