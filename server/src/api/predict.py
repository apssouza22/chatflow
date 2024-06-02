import typing as t

import sseclient
from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.factory import agent, apps, cost_service, llm_service
from api.user import User, get_current_user
from core.agent.agent_service import UserInputDto
from core.app.app_dao import App

predict_router = r = APIRouter()

class CompletionRequest(BaseModel):
    question: str
    context: str



@r.post("/chat/completions", response_model=t.Dict)
async def think(
        question_request: CompletionRequest,
        request: Request,
        current_user: User = Depends(get_current_user),
) -> t.Dict:
    user_input_req = get_request_dto(current_user, question_request, request)

    if cost_service.has_allowance_exceeded(current_user.email, user_input_req.app.app_key):
        raise HTTPException(status_code=402, detail="You have exceeded the free allowance for this app")

    # return get_fake_command()
    commands = await agent.handle_user_input(user_input_req)
    print(commands)
    return commands


@r.post('/chat/completions/stream')
async def stream_completion(
        question_request: CompletionRequest,
        request: Request,
        current_user: User = Depends(get_current_user),
):
    user_input_req = get_request_dto(current_user, question_request, request)

    if cost_service.has_allowance_exceeded(current_user.email, user_input_req.app.app_key):
        raise HTTPException(status_code=402, detail="You have exceeded the free allowance for this app")

    user_history = agent.user_history_process(user_input_req)
    prompts, _ = llm_service.get_question_prompts(user_input_req.app, user_history, user_input_req.question)
    return StreamingResponse(
        get_completion_stream(prompts, user_input_req.app.app_model, user_input_req.app.app_temperature),
        media_type='text/event-stream'
    )


def get_request_dto(current_user, question_request, request):
    get_user_ip(request)
    is_plugin_mode = request.headers.get("pluginmode") == "true"
    session_id = request.headers.get("sessionid") or current_user.email
    app = apps.get_by_id(current_user.email, request.headers.get("appkey"))
    if app is None:
        app = App(app_name="chat", app_description="admin app", app_key="chat")

    user_input_req = UserInputDto(**{
        "question": question_request.question,
        "context": question_request.context,
        "user": current_user,
        "app": app,
        "is_plugin_mode": is_plugin_mode,
        "session_id": session_id
    })
    return user_input_req


def get_completion_stream(prompts, model, temperature):
    response = llm_service.get_completions_stream(prompts, model, temperature)
    client = sseclient.SSEClient(response)
    for event in client.events():
        if event.data != '[DONE]':
            yield 'event: message\n'
            yield "data:" + event.data + '\n\n'


def get_user_ip(request):
    """Get the user's IP address from the request"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        client_host = x_forwarded_for.split(',')[0]  # Take the first IP if there's a list
    else:
        client_host = request.client.host
    return client_host



def get_fake_command():
    pass
    # return {
    #     "plan":{
    #         "thoughts": {
    #             "reasoning": "I will use the 'api_call' command to create a new private repository named 'test repo' and allow squash merge",
    #             "speak": "I will create a new private repository named 'test repo' and allow squash merge"
    #         },
    #         "command": {
    #             "name": "api_call",
    #             "args": {
    #                 "url": "https://api.github.com/user/repos",
    #                 "method": "POST",
    #                 "data_request": "{\"name\":\"test repo\",\"private\":true,\"allow_squash_merge\":true}",
    #                 "headers": {
    #                     "Accept": "application/vnd.github+json",
    #                     "Authorization": "Bearer <YOUR-TOKEN>",
    #                     "X-GitHub-Api-Version": "2022-11-28"
    #                 }
    #             }
    #         }
    #     }
    # }
