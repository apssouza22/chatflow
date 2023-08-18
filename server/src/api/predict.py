import typing as t

from fastapi import Depends, Request, APIRouter, HTTPException
from api.factory import agent, apps, cost_service
from api.user import User, get_current_user
from core.agent.agent_service import UserInputDto
from core.app.app_dao import App
from core.docs_search.dtos import (
    CompletionRequest
)

predict_router = r = APIRouter()


@r.post("/chat/completions", response_model=t.Dict)
async def think(
        question_request: CompletionRequest,
        request: Request,
        current_user: User = Depends(get_current_user),
) -> t.Dict:
    await get_user_ip(request)
    is_plugin_mode = request.headers.get("pluginmode") == "true"
    app = apps.get_by_id(current_user.email, request.headers.get("appkey"))
    if app is None:
        app = App(app_name="chat", app_description="admin app", app_key="chat")

    if cost_service.has_allowance_exceeded(current_user.email, app.app_key):
        raise HTTPException(status_code=402, detail="You have exceeded the free allowance for this app")

    user_input_req = UserInputDto(**{
        "question": question_request.question,
        "context": question_request.context,
        "user": current_user,
        "app": app,
        "is_plugin_mode": is_plugin_mode
    })
    # return get_fake_command()
    commands = agent.handle_user_input(user_input_req)
    print(commands)
    return commands


async def get_user_ip(request):
    """Get the user's IP address from the request"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        client_host = x_forwarded_for.split(',')[0]  # Take the first IP if there's a list
    else:
        client_host = request.client.host
    print(client_host)
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
