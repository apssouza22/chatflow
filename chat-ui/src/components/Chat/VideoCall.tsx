import {ChatController} from "./ChatController";
import {ActionRequest} from "./chat-types";
import * as React from "react";
import {useCallback} from "react";
import {Box, Button} from '@chakra-ui/react';
import {MdVideoCall} from "react-icons/md";

export function VideoCall({
                       chatController,
                       actionRequest,
                   }: {
    chatController: ChatController;
    actionRequest: ActionRequest;
}) {
    const chatCtl = chatController;

    const setResponse = useCallback((): void => {
        const res = {type: 'custom', value: 'Good!'};
        chatCtl.setActionResponse(actionRequest, res);
    }, [actionRequest, chatCtl]);

    return (
        <Box
            padding="0 20px"
            flex="1"
        >
            <Box
                flex="1 1 auto"
                display="flex"
                css={{
                    '& > *': {
                        flex: '1 1 auto',
                        minWidth: '0',
                    },
                    '& > * + *': {
                        marginLeft: '1',
                    },
                }}
            >
                <Button
                            type="button"
                            onClick={setResponse}
                            variant="solid"
                            colorScheme="red"
                            mr={2}
                            mb={2}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="button"
                            onClick={setResponse}
                            variant="solid"
                            colorScheme="green"
                            leftIcon={<MdVideoCall/>}
                        >
                            Call
                        </Button>

            </Box>
            <Box>
                <video
                    autoPlay
                    style={{
                        border: '1px solid #cddfe7',
                        width: '100%',
                        boxShadow: '0px 3px 6px rgba(0, 0, 0, 0.2)',
                    }}
                    id="remote-video"
                />
                <video
                    autoPlay
                    muted
                    style={{
                        border: '1px solid #cddfe7',
                        width: '300px',
                        boxShadow: '0px 3px 6px rgba(0, 0, 0, 0.2)',
                        borderRadius: '5px',
                        marginTop: '20px', marginBottom: '20px'
                    }}
                    id="local-video"
                />
                <audio autoPlay id="remote-audio" />
            </Box>
        </Box>
    );
}

