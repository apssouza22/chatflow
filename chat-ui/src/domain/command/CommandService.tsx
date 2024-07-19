import {CommandRequestHandler} from "./CommandRequestHandler";
import {ActionResponse, ChatController, defaultMsgObj} from "../../components/Chat";
import {formatText, TaskCommand} from "./Common";
import {CommandError, CommandFinder} from "./CommandFinder";
import {OnCommandTriggeredParams} from "../common/FlowController";
import {CommandExecution} from "./CommandExecution";
import {CommandResponseHandler} from "../commandresp/CommandResponseHandler";
import {SessionManager} from "../session/SessionManager";
import {HttpClient} from "../common/HttpClient";
import {showCustomField} from "../common/CustomInputs";
import {StreamCompletionClient} from "../common/StreamCompletionClient";

function isAction(doc: string, input: string) {
    if(input.startsWith("++")) {
        return true
    }
    if (input.endsWith("?")) {
        return false
    }
    return doc && doc.includes("#action");
}

export class CommandService {
    private commandReq: CommandRequestHandler;
    private commandFinder: CommandFinder;
    private chatCtl: ChatController;
    private commandExec: CommandExecution;
    private commandResp: CommandResponseHandler;

    constructor(
        commandReq: CommandRequestHandler,
        commandFinder: CommandFinder,
        commandExec: CommandExecution,
        cmdRespHandler: CommandResponseHandler,
        chatCtl: ChatController
    ) {
        this.commandReq = commandReq;
        this.commandFinder = commandFinder;
        this.commandExec = commandExec;
        this.commandResp = cmdRespHandler;
        this.chatCtl = chatCtl;
        chatCtl.getFlowController().addOnCommandTriggered(this.handleCommandTriggered())
    }


    async handleAnswerStream(input: string, docContext: string) {
        let answer = ""

        let chatCtl = this.chatCtl;
        await chatCtl.addMessage({...defaultMsgObj, content: formatText(answer)})

        this.commandFinder.getAnswerStream(
            input,
            docContext,
            (data: any, done: boolean) => {
                if (this.isStreamFinished(data)) {
                    showCustomField(chatCtl)
                    return
                }
                answer += data.choices[0]?.delta?.content + ""
                const contAnswer = formatText(answer)
                chatCtl.updateMessage(chatCtl.getMessages().length - 1, {...defaultMsgObj, content: contAnswer})
            })
    }

    private isStreamFinished(data: any) {
        return data.choices[0]?.delta?.content == null;
    }

    async process(res: ActionResponse): Promise<void> {
        let docResp = await this.commandFinder.getDocumentation(res.value);
        if (!docResp.success) {
            await this.chatCtl.addMessage({...defaultMsgObj, content: docResp.textMessage});
            return
        }

        if (!isAction(docResp.textMessage, res.value)) {
            await this.handleAnswerStream(res.value, docResp.textMessage)
            return
        }
        const commandResp = await this.commandFinder.getCommand(res.value, docResp.textMessage);

        console.log("task", commandResp)
        // @ts-ignore
        if (commandResp.hasOwnProperty("errorCode") && commandResp.errorCode != null) {
            return this.handleCommandError(commandResp as CommandError);
        }
        const taskCommand = commandResp as TaskCommand
        await this.commandReq.handleCommand(taskCommand)
        this.chatCtl.getFlowController().addCommand(taskCommand)
    }

    async handleCommand(command: TaskCommand) {
        await this.commandReq.handleCommand(command)
    }

    private handleCommandTriggered() {
        const self = this
        return async (params: OnCommandTriggeredParams) => {
            const resp = await self.commandExec.executeCommand(params.command, params.args)
            await self.commandResp.handle(resp)
        }
    }

    private async handleQuestionResponse(task: string) {
        let answer = formatText(task)
        await this.chatCtl.addMessage({...defaultMsgObj, content: answer});
    }

    private async handleCommandError(task: CommandError) {
        console.log("error task", task)
        if (task.errorCode == 402) {
            await this.chatCtl.addMessage({...defaultMsgObj, content: "You have exceeded the free allowance for this app."});
            return
        }
        if (task.errorCode == 200){
            await this.chatCtl.addMessage({...defaultMsgObj, content: task.errorMessage});
            return
        }
        await this.chatCtl.addMessage({...defaultMsgObj, content: "Something went wrong. Please try again later."});
    }
}

export function commandServiceFactory(
    chatCtl: ChatController,
    session: SessionManager,
    httpClient: HttpClient,
    httpClientNoBaseUrl: HttpClient,
    sseClient: StreamCompletionClient
): CommandService {
    const cmdReqHandler = new CommandRequestHandler(chatCtl)
    const cmdRespHandler = new CommandResponseHandler(chatCtl)
    const commandFinder = new CommandFinder(httpClient, sseClient, session)
    const commandExec = new CommandExecution(httpClientNoBaseUrl, session)
    return new CommandService(cmdReqHandler, commandFinder, commandExec, cmdRespHandler, chatCtl)
}
