import {FetchResult, HttpClient} from "../common/HttpClient";
import {Command, CommandName} from "./Common";
import {SessionManager} from "../session/SessionManager";
import { ChatController } from "../../components/Chat";

export interface CommandExecResult {
    status: number
    data?: any
    error?: any
}

type File = any; // should be DOM File object

export class CommandExecution {
    private httpClient: HttpClient;
    private session: SessionManager;
    private chatCtl: ChatController;
    private files: {
        [id: string]: File[] // array, because multiple files can be opened from a single file dialog and have the same ID
    }

    // Add one file or multiple files uploaded together.
    addFiles(id: string, files: File[]) {
        // Currently, as a quick hack for reducing the amount of data held in memory, we only keep the last file:
        for (const key of Array.from(Object.keys(this.files))) { // `Array.from` is necessary to prevent modificatio while iterating.
            delete this.files[key];
        }
        this.files[id] = files;
    }

    constructor(httpClient: HttpClient, session: SessionManager, chatCtl: ChatController) {
        this.httpClient = httpClient;
        this.session = session;
        this.chatCtl = chatCtl;
        this.files = {};
    }

    async executeCommand(command: Command, commandData: any): Promise<CommandExecResult> {
        if (command.name === CommandName.BROWSE_WEBSITE) {
            let url = command.args.url.split('?')[0];
            url += "?" + Object.keys(commandData).map((key) => {
                return key + "=" + commandData[key];
            }).join("&");
            window.open(url, '_blank');
            return {status: 200};
        }
        if (command.name === CommandName.SEND_EMAIL) {
            return await this.sendEmail(command, commandData);
        }

        if (command.name === CommandName.API_CALL) {
            const resp = await this.apiCall(command, commandData);
            console.log(resp)
            return {
                status: resp.status,
                data: resp.data,
                error: resp.error
            };
        }
        if (command.name === CommandName.JAVASCRIPT && command.function?.code) {
            try {
                const fn = command.function.name + "(" + JSON.stringify(command.function.param) + ")"
                const fn_body = extractFnBody(command.function.code);
                console.log(fn)
                console.log(fn_body)
                eval(fn_body)
            } catch (e) {
                console.log(e)
            }
        }
        if (command.name === CommandName.UPLOAD) {
            // TODO: correct?
            await this.chatCtl.setActionRequest({
                type: 'file',
                accept: '*/*',
                multiple: true,
            });
        }
        return {status: 200};
    };

    private async sendEmail(command: Command, commandData: any) {
        const resp = await this.apiCall({
            ...command,
            args: {
                data_request: commandData,
                url: "http://localhost:8880/api/v1/send-email",
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer ' + SessionManager.getInstance().getSessionData().token
                }
            },
        }, commandData);
        console.log(resp)
        return {
            status: resp.status,
            data: resp.data,
            error: resp.error
        };
    }

    private async apiCall(command: Command, commandData: any): Promise<FetchResult<any>> {
        console.log(command)
        this.prepareCommand(command, commandData);
        return await this.httpClient.makeRequest(command.args.url, {
            method: command.args.method,
            headers: command.args.headers,
            body: commandData
        });
    }

    private handleAppKeySession(command: Command, commandData) {
        if (command.args.url.indexOf("user/session") >= 0) {
            this.session.setAppKey(commandData.app_key)
        }
        if (command.args.url.indexOf("{app_key}") >= 0) {
            command.args.url = command.args.url.replace(
                "{app_key}",
                this.session.getSessionData().app
            );
        }
        if (command.args.url.indexOf("<YOUR-APP-KEY>") >= 0) {
            command.args.url = command.args.url.replace(
                "<YOUR-APP-KEY>",
                this.session.getSessionData().app
            );
        }
    }

    private handleAuthToken(command: Command) {
        if (!command.args.headers) {
            return
        }
        Object.keys(command.args.headers).forEach((key) => {
            // Github app demo
            if (command.args.headers[key].indexOf("<YOUR-TOKEN>") >= 0 && command.args.url.indexOf("api.github.com") > 0) {
                command.args.headers[key] = "Bearer " + localStorage.getItem("github-token") ?? "";
                return
            }

            if (command.args.headers[key].indexOf("<YOUR-TOKEN>") >= 0) {
                command.args.headers[key] = "Bearer " + SessionManager.getInstance().getSessionData().token;
            }
        });
    }

    private prepareCommand(command: Command, commandData:any) {
        if (typeof (command.args.headers) == "string") {
            command.args.headers = JSON.parse(command.args.headers);
        }
        if (process.env.NODE_ENV === "production") {
            command.args.url = command.args.url.replace("http://localhost:8880", "https://apps.newaisolutions.com");
        }

        // Replace file references by File objects:
        const newCommandData = {}; // should use Map instead of object?
        for (const [key, value] of Object.entries(commandData)) {
            if ((value as any).type === 'attachment') {
                // TODO: Display error message if file with this ID is not found.
                newCommandData[key] = this.files[(value as any).fileId]; // a blob of type `File`
            } else {
                newCommandData[key] = value;
            }
        }
        for (const [key, value] of Object.entries(newCommandData)) {
            commandData[key] = value;
        }

        this.handleAppKeySession(command, commandData);
        this.handleAuthToken(command);
    }
}

export function extractFnBody(fn: string): string {
    if (fn.indexOf("function") < 0) {
        return fn;
    }
    return fn.split('{')
        .slice(1)
        .join('{')
        .split('}')
        .slice(0, -1)
        .join('}')
}
