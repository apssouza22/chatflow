import {FetchResult, HttpClient} from "../common/HttpClient";
import {Command, CommandName} from "./Common";
import {SessionManager} from "../session/SessionManager";

export interface CommandExecResult {
    status: number
    data?: any
    error?: any
}

export class CommandExecution {
    private httpClient: HttpClient;
    private session: SessionManager;

    constructor(httpClient: HttpClient, session: SessionManager) {
        this.httpClient = httpClient;
        this.session = session;
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
        // Enable the user to set token to be used for external API calls
        if (command.args.url.indexOf(localStorage.getItem("external-url")) > 0 && localStorage.getItem("external-token")) {
            console.log("External token set")
            command.args.headers["Authorization"] = "Bearer " + localStorage.getItem("external-token") ?? "";
            return
        }
        command.args.headers["Authorization"] = "Bearer " + SessionManager.getInstance().getSessionData().token;
    }

    private prepareCommand(command: Command, commandData:any) {
        if (typeof (command.args.headers) == "string") {
            command.args.headers = JSON.parse(command.args.headers);
        }
        if (process.env.NODE_ENV === "production") {
            command.args.url = command.args.url.replace("http://localhost:8880", "https://apps.newaisolutions.com");
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
