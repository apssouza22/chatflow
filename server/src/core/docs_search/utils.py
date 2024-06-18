import re


def remove_content_between_backticks(input_string):
    """
    Remove content between backticks from a string.
    :param input_string: The input string.
    """
    return re.sub(r'`.*?`', '', input_string)
