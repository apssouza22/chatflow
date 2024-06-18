import typing as t

from fastapi import APIRouter
from pydantic import BaseModel

from api.factory import llm_service
from core.llm.dtos import MessageDict, MessageRole

predict_router = r = APIRouter()


class CompletionRequest(BaseModel):
    question: str
    context: str


@r.post("/chat/completions", response_model=t.Dict)
async def think(
        question_request: CompletionRequest
) -> t.Dict:
#     system_msg = """You are an AI responsible for identifying users intent.  Your goal is to analyze the user input and determine if the user requires either text or form as the response \n
# If the user input is understood as a question automatically, the response should be a "text". Example: explain me how to add a new address;  tell me what to do; how much does it cost? \n
# If the user input is understood as a greeting, the response should be "text".   Example:  How are you; Hi; Oi; Como você está? \n
# If the input requires an action, the response should be "form". Example: help me to send an email; book me a class; add a new address;  calculate the distance; help me to buy it \n
# If you are unsure about the answer say "text" \n
# VERY IMPORTANT: Respond with either "text" or "form".
# """
    prompts = []
    prompts.append(MessageDict(role=MessageRole.SYSTEM, content=question_request.context))
    prompts.append(MessageDict(role=MessageRole.USER, content=f'User input: {question_request.question}'))
    resp = llm_service.get_prediction(prompts)

    print(resp)
    return resp

