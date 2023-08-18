// React component
import {useEffect, useState} from "react";
import {Button, Flex, HStack, Spacer, Text} from "@chakra-ui/react"

type MessageExpanderParams = {
    content: any,
    displayText?: string,
    btnText?: string
    hide?: boolean
};

export function MessageExpander(props: MessageExpanderParams) {
    const [display, setDisplay] = useState(false)
    useEffect(() => {
            setDisplay(!props.hide)
        }, [])
    const showDoc = () => {
        setDisplay(!display)
    }
    return (
        <Flex direction={"column"}>
            <HStack>
                <Text fontWeight={"bold"}>{props.displayText ?? 'Thinking...'}</Text>
                <Spacer width={"300px"}/>
                <Button onClick={showDoc}>{props.btnText ?? 'Show documentation'}</Button>
            </HStack>
            <div className={"response-box"} style={{"display": display? "block": "none"}}>
                {(typeof props.content === 'string' ? <Text whiteSpace={"pre-wrap"}>{props.content}</Text> : <>{props.content}</>)}
            </div>
        </Flex>
    )
}
