// React component
import {Button} from "@chakra-ui/react"
import {Command} from "./Common";
import {useState} from "react";
import {ChatController} from "../../components/Chat";

type BtnProceedProps = {
    command: Command;
    commandData: any
    chatCtl:ChatController
};


export function BtnProceed(props: BtnProceedProps) {
    const [loading, setLoading] = useState(false)

    async function execute() {
        setLoading(true)
        await props.chatCtl.getFlowController().callOnCommandTriggered({
            command: props.command,
            args: props.commandData,
            callback: setLoading
        })
    }

    return (
        <Button onClick={execute}
                width={"200px"}
                mt={"5px"}
                alignSelf={"end"}>
            {!loading && "Click to proceed"}
            {loading && "Processing..."}
        </Button>
    )
}
