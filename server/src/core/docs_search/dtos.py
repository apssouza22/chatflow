from pydantic import BaseModel

DEFAULT_RETURN_FIELDS = ["item_id", "item_pk", "vector_score"]


class SearchRequest(BaseModel):
    text: str
    app_key: str = ""
    tags: str = ""
    user_email: str = ""


class AddDocRequest(BaseModel):
    text: str
    title: str
    app_key: str


class CompletionRequest(BaseModel):
    question: str
    context: str
