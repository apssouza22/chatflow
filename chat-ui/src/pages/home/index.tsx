import {MuiChat} from '../../components/Chat/';
import * as React from "react";
import {ReactElement, useEffect, useState} from "react";
import {ChatController} from "../../components/Chat";
import {Box, Center, Grid, GridItem, Heading, Text, useDisclosure} from "@chakra-ui/react";
import "./index.css"
import {GoSidebarCollapse, GoSidebarExpand} from "react-icons/go";
import Sidebar from "../../components/Sidebar";
import NavBar from "../../components/NavBar";
import IconBox from "../../components/Icons/IconBox";
import {CommandHistoryDrawer} from "../chatflow/CommandHistoryDrawer";
import {chatCtl, commandService} from "../../domain/Factory";
import {getTopRightMenu} from "../chatflow";
import {AVATAR_IMG} from "../chatflow/inputs";
import {HttpClient} from "../../domain/common/HttpClient";
import {SessionManager} from "../../domain/session/SessionManager";


export function HomeFlow(): ReactElement {
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
                        <Sidebar chatController={chatCtl} isHome={true}/>
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


async function start(chatCtl: ChatController): Promise<void> {
    await login("admin@gmail.com", "chat")
    await chatCtl.addMessage({
        type: 'jsx',
        content: getIntro(),
        self: false,
        avatar: AVATAR_IMG,
        className: "chat-intro"
    });

    await chatCtl.setActionRequest({
            type: 'text',
            placeholder: 'Please enter your text.',
            always: true,
        },
    );
}


const login = async (email, app_key) => {
    const endpoint = `/user/${email}/app/${app_key}/auth`
    const client = new HttpClient(process.env.REACT_APP_SERVER_URL)
    const resp = await client.get(endpoint)

    // @ts-ignore
    let accessToken = resp.data?.access_token;
    if (resp.status !== 200 || accessToken == null) {
        alert("Login failed")
        return
    }
    sessionStorage.setItem("token", accessToken);
    const session = SessionManager.getInstance();
    session.setToken(accessToken);
    session.setUser(email);
    session.setAppKey(app_key);
};

function getIntro() {
    return (<Center px={[4, 6, 8]} flexDirection="column" width={"100%"}>
        <Box width={"100%"}>
            <Heading
                as="h2"
                size="xl"
                color="blue.700"
                fontSize={['2xl', '3xl', '4rem']}
                m={"40px"}
            >
                <Text color={"teal.500"}>Watch how it works</Text>
            </Heading>
            <Box pb={"50px"}>
                <iframe width={"100%"} height={"400px"} id="embed-iframe-7"
                        src="https://player.vimeo.com/video/858432033?h=94f08ece33&amp;autoplay=1&amp;loop=1&amp;autopause=0&amp;muted=1&amp;title=0&amp;byline=0&amp;portrait=0&amp;controls=0"
                        allow="autoplay; fullscreen" loading="lazy"
                        data-aid="HEADER_VIDEO_EMBED"></iframe>
            </Box>

        </Box>
    </Center>);
}
