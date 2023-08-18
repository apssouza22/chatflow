import json
import logging
import re
from typing import Dict, Union, Any

from core.llm.llm_service import LLMService

logger = logging.getLogger(__name__)

JSON_SCHEMA = """
{
    "command": {
        "name": "command name",
        "args": {
            "arg name": "value"
        }
    },
    "thoughts":
    {
        "reasoning": "reasoning",
        "speak": "thoughts summary to say to user"
    }
}
"""


class OpenAIResponseHandler:

    def __init__(self, llm: LLMService):
        self.llm = llm
        self.sanitizers = [
            extract_longest_curly_braces_content,
            replace_single_quotes_to_value_with_objects,
            add_quotes_to_property_names,
            replace_invalid_colon
        ]

    def extract_json_schema(self, assistant_reply):
        """ Extract the expected json response from the OpenAI response """
        try:
            assistant_reply_json = json.loads(assistant_reply)
        except json.JSONDecodeError as e:
            logger.error("Error: Invalid JSON returned from GPT trying to fix it\n", assistant_reply)
            assistant_reply_json = self.fix_and_parse_json(assistant_reply)
        return assistant_reply_json

    def fix_and_parse_json(self, json_str: str) -> Union[str, Dict[Any, Any]]:
        """Fix and parse JSON string"""
        json_str = json_str.replace("\t", "")
        for sanitize in self.sanitizers:
            json_str = sanitize(json_str)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        ai_fixed_json = self.fix_json_using_gpt(json_str, JSON_SCHEMA)
        return json.loads(ai_fixed_json)



    def fix_json_using_gpt(self, json_str: str, schema: str) -> str:
        """Fix the given JSON string to make it parseable and fully compliant with the provided schema."""
        function_string = "def fix_json(json_str: str, schema:str=None) -> str:"
        args = [f"'''{json_str}'''", f"'''{schema}'''"]
        description_string = (
            "Fixes the provided JSON string to make it parseable"
            " and fully compliant with the provided schema.\n If an object or"
            " field specified in the schema isn't contained within the correct"
            " JSON, it is omitted.\n This function is brilliant at guessing"
            " when the format is incorrect."
        )

        # If it doesn't already start with a "`", add one:
        if not json_str.startswith("`"):
            json_str = "```json\n" + json_str + "\n```"
        result_string = self.llm.call_ai_function(
            function_string, args, description_string
        )
        logger.debug("------------ JSON FIX ATTEMPT ---------------")
        logger.debug(f"Original JSON: {json_str}")
        logger.debug("-----------")
        logger.debug(f"Fixed JSON: {result_string}")
        logger.debug("----------- END OF FIX ATTEMPT ----------------")

        try:
            json.loads(result_string)  # just check the validity
            return result_string
        except:  # noqa: E722
            return "failed"



def add_quotes_to_property_names(json_string: str) -> str:
    """
    Add quotes to property names in a JSON string.

    Args:
        json_string (str): The JSON string.

    Returns:
        str: The JSON string with quotes added to property names.
    """

    def replace_func(match: re.Match) -> str:
        return f'"{match[1]}":{match[2]}'

    # It matches any word followed by : and then an space or ", { or [
    property_name_pattern = re.compile(r"(\w+):( ?[\"\{\[])")
    corrected_json_string = property_name_pattern.sub(replace_func, json_string)

    return corrected_json_string


def replace_single_quotes_to_value_with_objects(json_string: str) -> str:
    """
    Add quotes to property names in a JSON string.

    Args:
        json_string (str): The JSON string.

    Returns:
        str: The JSON string with quotes added to property names.
    """

    def replace_func(match: re.Match) -> str:
        return f':{{{match[1]}}}'

    property_name_pattern = re.compile(r": '\{(.+)\}'")
    corrected_json_string = property_name_pattern.sub(replace_func, json_string)

    return corrected_json_string


def extract_longest_curly_braces_content(s):
    """Extract the longest content between valid curly braces in a string."""
    stack = []
    start = -1
    result = ''
    longest_len = 0
    longest_content = ''
    for i in range(len(s)):
        if s[i] == '{':
            stack.append(i)
        elif s[i] == '}':
            if len(stack) == 0:
                start = i
            else:
                start = stack.pop()
                if len(stack) == 0:
                    content = s[start + 1:i]
                    content_len = len(content)
                    if content_len > longest_len:
                        longest_len = content_len
                        longest_content = content
    return f"{{{longest_content}}}"


# Replace invalid :
def replace_invalid_colon(json_string):
    # Find the Response: string
    json_string = json_string.replace(":,", ",")
    json_string = json_string.replace(":}", "}")
    return json_string
