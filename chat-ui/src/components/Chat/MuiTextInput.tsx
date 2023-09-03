import {Box, Button, Icon, Input} from "@chakra-ui/react";


import {ChatController} from './index';
import {TextActionRequest, TextActionResponse} from './index';
import {ReactElement, useCallback, useEffect, useState} from "react";
import {AiOutlineSend} from "react-icons/ai";

export function MuiTextInput({
                                 chatController,
                                 actionRequest,
                             }: {
    chatController: ChatController;
    actionRequest: TextActionRequest;
}): ReactElement {
    const chatCtl = chatController;
    const [value, setValue] = useState(actionRequest.defaultValue);

    useEffect(() => {
        setValue(actionRequest.defaultValue);
    }, [actionRequest.defaultValue]);

    const setResponse = useCallback((): void => {
        const vars = extractContentBetweenBraces(value)
        if (vars != "") {
            alert(`Please replace the ${vars} with the expected value`)
            return
        }
        if (value) {
            const res: TextActionResponse = {type: 'text', value};
            chatCtl.setActionResponse(actionRequest, res);
            setValue('');
        }
    }, [actionRequest, chatCtl, value]);

    const handleKeyDown = useCallback(
        // @ts-ignore
        (e: KeyboardEvent<HTMLTextAreaElement>): void => {
            if (e.nativeEvent.isComposing) {
                return;
            }

            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                setResponse();
            }
        },
        [setResponse],
    );

    const sendButtonText = actionRequest.sendButtonText
        ? actionRequest.sendButtonText
        : 'Send';

    return (
        <Box
            sx={{
                flex: '1 1 auto',
                display: 'flex',
                '& > *': {
                    flex: '1 1 auto',
                    minWidth: 0,
                },
                '& > * + *': {
                    ml: 1,
                },
                '& :last-child': {
                    flex: '0 1 auto',
                },
            }}
        >
            <Input
                placeholder={actionRequest.placeholder}
                value={value}
                onChange={(e) => setValue(e.target.value)}
                autoFocus
                resize="vertical"
                onKeyDown={handleKeyDown}
                variant="outline"
                maxH="10rem"
            />
            <Button
                type="button"
                onClick={setResponse}
                disabled={!value}
                variant="solid"
                color="primary"
                leftIcon={<AiOutlineSend/>}
            >
                {sendButtonText}
            </Button>
        </Box>
    );
}
function extractContentBetweenBraces(inputString) {
    const regex = /{{{(.*?)}}}/g;
    const matches = [];
    let match;

    while ((match = regex.exec(inputString)) !== null) {
        matches.push("{{{" + match[1] + "}}}");
    }

    return matches.join(",");
}
