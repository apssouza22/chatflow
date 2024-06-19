class OpenAIError:

    def __init__(self, message: str):
        self.message = message


class OpenAIRateLimitError(OpenAIError):
    pass
