import {Box} from '@chakra-ui/react';

import {
    ActionRequest,
    AudioActionRequest,
    CustomActionRequest,
    FileActionRequest,
    MultiSelectActionRequest,
    SelectActionRequest,
    TextActionRequest,
} from './chat-types';

import {MuiAudioInput} from './index';
import {MuiFileInput} from './index';
import {MuiMessage} from './index';
import {MuiMultiSelectInput} from './index';
import {MuiSelectInput} from './index';
import {MuiTextInput} from './index';
import {ChatController} from "./index";
import {FC, PropsWithChildren, ReactElement, useCallback, useEffect, useMemo, useRef, useState} from "react";
import * as dayjs from "dayjs";

type MuiChatParams = {
    chatController: ChatController;
};

export function MuiChat({chatController}: PropsWithChildren<MuiChatParams>): ReactElement {
    const chatCtl = chatController;
    const [messages, setMessages] = useState(chatCtl.getMessages());
    const [actReq, setActReq] = useState(chatCtl.getActionRequest());

    const msgRef = useRef<HTMLDivElement>(null);
    const scroll = useCallback((): void => {
        setTimeout(() => {
            if (msgRef.current) {
                msgRef.current.scrollTop = msgRef.current.scrollHeight + 50;
            }
        }, 100);
    }, [msgRef]);

    useEffect(() => {
        function handleMassagesChanged(): void {
            setMessages([...chatCtl.getMessages()]);
            scroll();
        }

        function handleActionChanged(): void {
            setActReq(chatCtl.getActionRequest());
            scroll();
        }

        chatCtl.addOnMessagesChanged(handleMassagesChanged,0);
        chatCtl.addOnActionChanged(handleActionChanged,0);
    }, [chatCtl, scroll]);

    type CustomComponentType = FC<{
        chatController: ChatController;
        actionRequest: ActionRequest;
    }>;
    const CustomComponent = useMemo((): CustomComponentType => {
        if (!actReq || actReq.type !== 'custom') {
            return null as unknown as CustomComponentType;
        }
        return (actReq as CustomActionRequest)
            .Component as unknown as CustomComponentType;
    }, [actReq]);

    const unknownMsg = {
        type: 'text',
        content: 'Unknown message.',
        self: false,
    };

    let prevDate = dayjs(0);
    let prevTime = dayjs(0);

    return (
        <Box
            bg='gray.100'
            height="100%"
            width="100%"
            p={1}
            display="flex"
            flexDirection="column"
            css={{
                "& > *": {maxWidth: '100%'},
                '& > * + *': {
                    mt: 1,
                }
            }}

        >
            <Box
                className={"chat-messages"}
                flex="1 1 0%"
                overflowY="auto"
                display="flex"
                flexDirection="column"
                css={{"& > *": {maxWidth: '100%'}}}
                ref={msgRef}
            >
                {messages.map((msg): ReactElement => {
                    let showDate = false;
                    let showTime = !!chatCtl.getOption().showDateTime;
                    if (!!chatCtl.getOption().showDateTime && !msg.deletedAt) {
                        const current = dayjs(
                            msg.updatedAt ? msg.updatedAt : msg.createdAt,
                        );

                        if (current.format('YYYYMMDD') !== prevDate.format('YYYYMMDD')) {
                            showDate = true;
                        }
                        prevDate = current;

                        if (current.diff(prevTime) < 60_000) {
                            showTime = false;
                        } else {
                            prevTime = current;
                        }
                    }
                    if (msg.type === 'text' || msg.type === 'jsx' || msg.type === 'file') {
                        return (
                            <MuiMessage
                                key={messages.indexOf(msg)}
                                id={`cu-msg-${messages.indexOf(msg) + 1}`}
                                message={msg}
                                showDate={showDate}
                                showTime={showTime}
                            />
                        );
                    }
                    return (
                        <MuiMessage
                            key={messages.indexOf(msg)}
                            id={`cu-msg-${messages.indexOf(msg) + 1}`}
                            message={unknownMsg}
                            showDate={showDate}
                            showTime={showTime}
                        />
                    );
                })}
            </Box>
            <Box
                flex="0 1 auto"
                display="flex"
                alignContent="flex-end"
            >
                {actReq && actReq.type === 'text' && (
                    <MuiTextInput
                        chatController={chatCtl}
                        actionRequest={actReq as TextActionRequest}
                    />
                )}
                {actReq && actReq.type === 'select' && (
                    <MuiSelectInput
                        chatController={chatCtl}
                        actionRequest={actReq as SelectActionRequest}
                    />
                )}
                {actReq && actReq.type === 'multi-select' && (
                    <MuiMultiSelectInput
                        chatController={chatCtl}
                        actionRequest={actReq as MultiSelectActionRequest}
                    />
                )}
                {actReq && actReq.type === 'file' && (
                    <MuiFileInput
                        chatController={chatCtl}
                        actionRequest={actReq as FileActionRequest}
                    />
                )}
                {actReq && actReq.type === 'audio' && (
                    <MuiAudioInput
                        chatController={chatCtl}
                        actionRequest={actReq as AudioActionRequest}
                    />
                )}
                {actReq && actReq.type === 'custom' && (
                    <CustomComponent
                        chatController={chatCtl}
                        actionRequest={actReq as CustomActionRequest}
                    />
                )}
            </Box>
        </Box>
    );
}
