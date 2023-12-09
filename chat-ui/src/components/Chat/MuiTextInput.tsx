import {Box, Button, Icon, Input} from "@chakra-ui/react";


import {AudioActionResponse, ChatController, FileActionResponse} from './index';
import {TextActionRequest, TextActionResponse} from './index';
import {ReactElement, useCallback, useEffect, useState} from "react";
import {AiOutlineSend} from "react-icons/ai";
import { GoUpload} from "react-icons/go";
import IconBox from "../Icons/IconBox";
import * as React from "react";
import {AVATAR_IMG} from "../../pages/chatflow/inputs";
import {MdKeyboardVoice, MdVideoCall} from "react-icons/md";
import {VideoCallComponent} from "../../domain/videocall";

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

    let loadUploadComponent = async () => {
        const file = (await chatCtl.setActionRequest({
            type: 'file',
            accept: '*',
            multiple: true,
        })) as FileActionResponse;

        await chatCtl.setActionRequest({
                type: 'text',
                placeholder: 'Please enter your text.',
                always: true,
            },
        );
        // the result is in the Factory.tsx

    };
    let loadVideoChatComponent = async () => {
        const videoCall = await chatCtl.setActionRequest({
            type: 'custom',
            Component: VideoCallComponent,
        });
        // the result is in the Factory.tsx
    };


    let loadAudioComponent = async () => {
        await chatCtl.addMessage({
            type: 'text',
            content: `Please enter your voice.`,
            self: false,
            avatar: AVATAR_IMG
        });
        const audio = (await chatCtl
            .setActionRequest({
                type: 'audio',
            })
            .catch(() => ({
                type: 'audio',
                value: 'Voice input failed.',
                avatar: AVATAR_IMG
            }))) as AudioActionResponse;

        // the result is in the Factory.tsx

    };
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
            <IconBox {...{
                onClick: loadUploadComponent,
                color: "black",
                className: "bt-upload",
                cursor: "pointer",
                padding: "0.5rem",
                title: "Upload file",
                _hover: {
                    bg: "gray.200"
                }
            }} >
                <GoUpload/>
            </IconBox>
            <IconBox {...{
                onClick: loadAudioComponent,
                color: "black",
                className: "bt-mic",
                cursor: "pointer",
                padding: "0.5rem",
                title: "Microphone",
                _hover: {
                    bg: "gray.200"
                }
            }} >
                <MdKeyboardVoice/>
            </IconBox>
            <IconBox {...{
                onClick: loadVideoChatComponent,
                color: "black",
                className: "bt-video",
                cursor: "pointer",
                padding: "0.5rem",
                title: "Video call",
                _hover: {
                    bg: "gray.200"
                }
            }} >
                <MdVideoCall/>
            </IconBox>
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
