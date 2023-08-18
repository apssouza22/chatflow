import re


def remove_content_between_backticks(input_string):
    return re.sub(r'`.*?`', '', input_string)
