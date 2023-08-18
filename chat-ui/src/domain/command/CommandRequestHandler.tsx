import {CommandName, formatText, TaskCommand} from "./Common";
import {ChatController, defaultMsgObj} from "../../components/Chat";
import {Flex, Text} from "@chakra-ui/react";
import {FieldValueTable} from "./FieldValueTable";
import {BtnProceed} from "./BtnProceed";
import * as React from "react";

export class CommandRequestHandler {
    private readonly chatCtl: ChatController;

    constructor(chatCtl: ChatController) {
        this.chatCtl = chatCtl;
    }

    async handleCommand(taskCommand: TaskCommand){
        if (taskCommand.command.name === CommandName.CHAT_QUESTION) {
            await this.handleChatQuestion(taskCommand)
            return
        }
        this.renderTaskCommand(taskCommand);
    }

    private  setJsxMessages(content) {
        this.chatCtl.addMessage({
            ...defaultMsgObj,
            type: 'jsx',
            content: content
        });
    }

    private renderTaskCommand(task: TaskCommand) {
        let dataUpdate = task.dataUpdate;
        let command = task.command;
        const speak = task.speak;

        if (this.hasFields(dataUpdate)) {
            this.setJsxMessages((
                <Flex direction={"column"}>
                    <Text m={"10px"}>{speak}</Text>
                    <FieldValueTable
                        chatCtl={this.chatCtl}
                        command={command}
                        requestRender={task.command.request_render}
                        data={dataUpdate}
                    />
                </Flex>))
            return
        }
        this.setJsxMessages((
            <Flex direction={"column"}>
                <Text m={"10px"}>{speak}</Text>
                <BtnProceed command={command} commandData={dataUpdate} chatCtl={this.chatCtl}/>
            </Flex>
        ))
    }

    private hasFields(dataUpdate) {
        return dataUpdate !== undefined && Object.values(dataUpdate).length > 0;
    }

    private async handleChatQuestion(taskCommand: TaskCommand) {
        let answer =  formatText(taskCommand.speak)
        await this.chatCtl.addMessage({...defaultMsgObj, content: answer});
    }
}
