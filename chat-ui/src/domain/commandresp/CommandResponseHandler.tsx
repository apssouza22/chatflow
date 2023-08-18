import {ChatController, defaultMsgObj} from "../../components/./Chat/ChatController";
import {isRenderChart} from "../command/Common";
import {MessageExpander} from "./MessageExpander";
import {RenderChart} from "./RenderChart";
import {RenderDataTable} from "./RenderDataTable";
import * as React from "react";
import {SessionManager} from "../session/SessionManager";
import {CommandExecResult} from "../command/CommandExecution";

export class CommandResponseHandler {
    private readonly chatCtl: ChatController;

    constructor(chatCtl: ChatController) {
        this.chatCtl = chatCtl;
    }

    async handle(resp: CommandExecResult) {
        let displayText = "Action executed successfully.";
        if (resp.status >= 400) {
            displayText = "Action failed.";
        }
        setAccessToken(resp.data)

        await this.chatCtl.addMessage({
            ...defaultMsgObj,
            type: "jsx",
            content: (
                    <MessageExpander
                        content={this.getContent(resp.data)}
                        btnText={"Show response"}
                        displayText={displayText}
                    />)
        })
    }

    private getContent(resp){
        if(isRenderChart() && Array.isArray(resp)){
            return <RenderChart data={resp}/>
        }
        return <RenderDataTable data={resp} chatCtl={this.chatCtl}/>
    }
}

function setAccessToken(data: any) {
    if (typeof (data) != "object") {
        return data;
    }
    let dataObj = data as { [x: string]: string };
    Object.keys(dataObj).forEach((key) => {
        if (key === "access_token") {
            SessionManager.getInstance().setToken(dataObj[key]);
        }
    });
}
