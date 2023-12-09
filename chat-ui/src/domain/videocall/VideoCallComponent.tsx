import {ActionRequest, ChatController} from "../../components/Chat";
import * as React from "react";
import {useCallback, useEffect, useState} from "react";
import {Box, Button, Menu, MenuButton, MenuItem, MenuList} from '@chakra-ui/react';
import {MdVideoCall} from "react-icons/md";
import {VideoChatApp} from "./index";
import io from "socket.io-client";

let  videoChatApp: VideoChatApp ;
export function VideoCallComponent({
                              chatController,
                              actionRequest,
                          }: {
    chatController: ChatController;
    actionRequest: ActionRequest;
}) {
    const [userList, setUserList] = useState([]);
    const chatCtl: ChatController = chatController;
    useEffect(() => {
        videoChatApp = new VideoChatApp({
            localVideo: document.getElementById("local-video"),
            remoteVideo: document.getElementById("remote-video"),
            // remoteVideo: document.getElementById("remote-audio"), We can use this for audio as well
            socket: io.connect("localhost:4000"),
            userList: setUserList
        });
        videoChatApp.start();
    }, []);

    const startVideoCall = useCallback((user): void => {
        console.log("Starting video call with " + user)
        videoChatApp.callUser(user)
    }, [actionRequest, chatCtl]);


    const cancelVideoCall = useCallback((): void => {
        chatCtl.setActionRequest({
            type: 'text',
            placeholder: 'Please enter your text.',
            always: true,
        })
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
                <Menu>
                    <MenuButton>
                        <Button
                            type="button"
                            onClick={startVideoCall}
                            variant="solid"
                            colorScheme="green"
                            leftIcon={<MdVideoCall/>}
                        >
                            Call
                        </Button>
                    </MenuButton>
                    <MenuList>
                        {userList.map((user, index) => (
                            <MenuItem onClick={() => {
                                startVideoCall(user)
                            }}>
                                {user}
                            </MenuItem>
                        ))}

                    </MenuList>
                </Menu>
                <Button
                    type="button"
                    onClick={cancelVideoCall}
                    variant="solid"
                    colorScheme="red"
                    mr={2}
                    mb={2}
                >
                    Cancel
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
                <audio autoPlay id="remote-audio"/>
            </Box>
        </Box>
    );
}

