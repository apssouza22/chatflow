import base64


def encode_to_base64(input_string):
    """Encode a string to base64."""
    bytes_string = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_string)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def decode_from_base64(base64_string):
    """Decode a string from base64."""
    base64_bytes = base64_string.encode('utf-8')
    bytes_string = base64.b64decode(base64_bytes)
    input_string = bytes_string.decode('utf-8')
    return input_string
