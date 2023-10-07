import {MuiChat,} from '../../components/./Chat/';
import * as React from "react";
import {ReactElement, useEffect, useState} from "react";
import {ChatController} from "../../components/Chat";
import {Box, Grid, GridItem, IconButton, Menu, MenuButton, MenuItem, MenuList, useDisclosure} from "@chakra-ui/react";
import "./index.css"
import {GoSidebarCollapse, GoSidebarExpand} from "react-icons/go";
import Sidebar from "../../components/Sidebar";
import NavBar from "../../components/NavBar";
import {HamburgerIcon} from "@chakra-ui/icons";
import {askIfShouldDemoTheInputs, AVATAR_IMG} from "./inputs";
import IconBox from "../../components/Icons/IconBox";
import {CommandHistoryDrawer} from "./CommandHistoryDrawer";
import {chatCtl, commandService} from "../../domain/Factory";
import {SessionManager} from "../../domain/session/SessionManager";


export function ChatFlow(): ReactElement {
    const [isExpanded, setIsExpanded] = useState(false);
    const {isOpen, onOpen, onClose} = useDisclosure();

    useEffect(() => {
        start(chatCtl);
    }, []);

    const toggleView = () => {
        setIsExpanded(!isExpanded);
    };
    const iconProps = {
        onClick: toggleView,
        color: "black",
        className: "bt-toggle-sidebar",
        position: "fixed",
        top: "62px",
        left: "10px",
        cursor: "pointer"
    }
    return (
        <>
            <NavBar/>
            <IconBox {...iconProps} >
                {isExpanded ? <GoSidebarCollapse/> : <GoSidebarExpand/>}
            </IconBox>
            <Grid templateColumns="repeat(6, 1fr)" bg="gray.50">
                {/* sidebar */}
                {!isExpanded && (
                    <GridItem
                        as="aside"
                        colSpan={{base: 6, lg: 2, xl: 2}}
                        bg="gray.50"
                        overflowY="scroll"
                        height={"100vh"}
                    >
                        <Sidebar chatController={chatCtl}/>
                    </GridItem>
                )}

                {/* main content & navbar */}
                <GridItem
                    as="main"
                    colSpan={isExpanded ? {base: 6, lg: 6, xl: 6} : {base: 6, lg: 4, xl: 4}}
                    bg="white"
                    height={"100vh"}
                >
                    <Box
                        display="flex"
                        flexDirection="column"
                        height="100%"
                        mx="auto"
                        pt={"90px"}
                        className={"chat-container"}
                    >
                        <Box flex="1 1 0%" minHeight="0" borderTop={"1px solid #ccc"}>
                            <MuiChat chatController={chatCtl}/>
                        </Box>
                    </Box>
                </GridItem>
            </Grid>
            {getTopRightMenu(onOpen)}
            <CommandHistoryDrawer
                isOpen={isOpen}
                onClose={onClose}
                onOpen={onOpen}
                chatCtl={chatCtl}
                commandService={commandService}
            />
        </>
    );
}

export function getTopRightMenu(onOpen): ReactElement {
    return (<Menu>
        <MenuButton
            as={IconButton}
            aria-label="List options"
            icon={<HamburgerIcon/>}
            variant="ghost"
            size="sm"
            mr={2}
            ml={2}
            w={"30px"}
            bg="transparent"
            color={"black"}
            position={"fixed"}
            top={"55px"}
            right={"10px"}
        />
        <MenuList>
            <MenuItem onClick={onOpen}>
                Open command history
            </MenuItem>
            <MenuItem onClick={() => {
                document.querySelectorAll(".response-box")
                    .forEach((e) => {
                        // @ts-ignore
                        e.style.display = "none"
                    })
            }}>
                Close all responses
            </MenuItem>
        </MenuList>
    </Menu>)
}

async function start(chatCtl: ChatController): Promise<void> {
    // if (SessionManager.getInstance().getSessionData().app == "chat") {
    //     await askIfShouldDemoTheInputs(chatCtl);
    // }
    await chatCtl.addMessage({
        type: 'text',
        content: `How can I help you today?`,
        self: false,
        avatar: AVATAR_IMG
    });

    await chatCtl.setActionRequest({
            type: 'text',
            placeholder: 'Please enter your text.',
            always: true,
        },
    );
}
