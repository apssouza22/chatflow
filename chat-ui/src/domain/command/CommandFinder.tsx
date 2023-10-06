import {Command, CommandName, setRenderInfo, TaskCommand} from "../command/Common";
import {parseUrlParams} from "../common/utils";
import {LOCALHOST_URL} from "../../constants";
import {HttpClient} from "../common/HttpClient";
import {SessionManager} from "../session/SessionManager";
import {StreamCompletionClient} from "../common/StreamCompletionClient";

type DocResp = {
    success: boolean,
    textMessage: string
}

type AnswerType = string
type InputHandledResp = TaskCommand | CommandError | AnswerType;

export class CommandFinder {
    private httpClient: HttpClient;
    private session: SessionManager;
    private sseClient: StreamCompletionClient;

    constructor(httpClient: HttpClient, sseClient: StreamCompletionClient, session: SessionManager) {
        this.sseClient = sseClient;
        this.httpClient = httpClient;
        this.session = session;
    }

    private getHeaders() {
        return {
            "Authorization": "Bearer " + this.session.getSessionData().token,
            "AppKey": this.session.getSessionData().app,
            "PluginMode": this.session.getSessionData().isPluginMode.toString(),
        };
    }

    async getDocumentation(input): Promise<DocResp> {
        if (!input.startsWith("++")) {
            return await this.retrieveSupportingDoc(input)
        }

        return {
            success: true,
            textMessage: "Using the same message documentation."
        };
    }

    private async retrieveSupportingDoc(input): Promise<DocResp> {
        let data = {
            "text": input,
            "app_key": this.session.getSessionData().app,
        };
        let resp = await this.httpClient.post("/docs/search", data, this.getHeaders())
        console.log("documentation response", resp)
        if (resp.status == 402) {
            return {
                success: false,
                textMessage: "You have exceeded the free allowance for this app"
            }
        }
        if (resp.error != null) {
            return {
                success: false,
                textMessage: "Something went wrong. Try again later"
            }
        }
        // @ts-ignore
        let responseData = resp.data.docs;
        if (responseData.length === 0) {
            return {
                success: false,
                textMessage: "Sorry I don't know what you mean"
            }
        }
        return {
            success: true,
            textMessage: responseData[0]
        }
    }

    getAnswerStream(input: string, docContext: string, callback: (event,done: boolean)=> void): void {
        this.sseClient.call(input, docContext,callback);
    }

    async getCommand(input, docContext): Promise<InputHandledResp> {
        let data = {
            "question": input,
            "context": docContext,
        };


        const resp = await this.httpClient.post<Command>(
            "/chat/completions",
            data,
            this.getHeaders()
        )

        console.log("command response", resp)
        if (resp.error != null) {
            return {
                errorCode: resp.status,
                errorMessage: resp.error
            }
        }

        let taskCommand = parseCommandResponse(resp, input);
        taskCommand.dataUpdate = prepareDataUpdate(taskCommand.command, taskCommand.dataUpdate)
        setRenderInfo(taskCommand.command?.response_render)
        console.log("taskCommand", taskCommand)
        return taskCommand;
    }
}


// @ts-ignore
function parseCommandResponse(resp: any, chat: string): TaskCommand {
    let command = resp.data.command as Command;

    if (command.args?.url?.indexOf(LOCALHOST_URL) > -1) {
        command.args.url = command.args.url.replace(LOCALHOST_URL, process.env.REACT_APP_SERVER_URL)
    }
    let speak = resp.data?.thoughts?.speak as string;
    const answer = resp.data?.thoughts?.answer as string;
    command.request_render = resp.data?.request_render ?? command?.request_render;
    command.response_render = resp.data?.response_render ?? command.response_render;
    if (command.name === CommandName.SEND_EMAIL) {
        command.request_render["body"] = {
            "field_type": "textarea",
        }
    }
    let dataUpdate = {}

    return {dataUpdate: dataUpdate, command, speak: answer ?? speak, chat};
}

function prepareDataUpdate(command: Command, taskData: any) {
    let dataUpdate = command?.args?.data_request ?? {};
    if (command.name === CommandName.BROWSE_WEBSITE) {
        dataUpdate = parseUrlParams(command.args.url);
    }
    if (command.name === CommandName.SEND_EMAIL) {
        dataUpdate = command.args
    }
    if (command?.args?.data_request == undefined && command?.args?.url != null) {
        dataUpdate = parseUrlParams(command.args.url);
    }
    if (typeof dataUpdate === 'string') {
        dataUpdate = JSON.parse(dataUpdate);
    }
    if (Object.keys(taskData).length > 0) {
        return {...taskData, ...dataUpdate}
    }
    return dataUpdate
}

export interface CommandError {
    errorCode: number,
    errorMessage: string
}
