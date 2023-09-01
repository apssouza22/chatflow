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
            <Grid templateColumns="repeat(6, 1fr)" bg="gray.900" 
             >
                
                {/* sidebar */}
                {!isExpanded && (
                    <GridItem
                        as="aside"
                        colSpan={{base: 6, lg: 1, xl: 1}}
                        bg="gray.900"
                        overflowY="scroll"
                        height={"100vh"}
                        shadow="md"
                        flexGrow={1}
                        sx={{
                            '&::-webkit-scrollbar': {
                              width: '16px',
                              borderRadius: '8px',
                              backgroundColor: 'rgba(0, 0, 0, 0.1)', // Slightly darker background for better contrast
                            },
                            '&::-webkit-scrollbar-thumb': {
                              backgroundColor: 'rgba(128, 128, 128, 0.2)',
                              boxShadow: 'inset 0 0 6px rgba(0,0,0,0.5)', // Inner shadow for a more 3D look
                              transition: 'background-color 0.2s ease-in-out', // Smooth transition for hover effect
                              '&:hover': { // Hover effect
                                backgroundColor: 'rgba(128, 128, 128, 0.5)',
                              },
                            },
                          }}
                          
                    >
                        <Sidebar chatController={chatCtl} isHome={true}/>
                    </GridItem>
                )}

                {/* main content & navbar */}
                <GridItem
                    as="main"
                    colSpan={isExpanded ? {base: 6, lg: 6, xl: 6} : {base: 6, lg: 5, xl: 5}}
                    bg="gray.100"
                    height={"100vh"}
                    flexGrow={3}
                    
                >
                    <Box
                       display="flex"
                       flexDirection="column"
                       height="100%"
                       mx="auto"
                       className={"chat-container"}
                       
                        
                    >
                        <Box flex="1 1 0%" minHeight="0" borderTop={"1px solid #ccc"}
                        > 
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
    await login("apssouza22@gmail.com", "61866002")
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
            <Box pb={"5px"} pl={"0px"} pr={"0px"} > 
                <iframe width={"100%"} height={"500px"} id="embed-iframe-7" 
                        src="https://player.vimeo.com/video/858432033?h=94f08ece33&autoplay=1&loop=1&autopause=0&muted=1&title=0&byline=0&portrait=0&controls=0"
                        allow="autoplay; fullscreen" loading="lazy"
                        data-aid="HEADER_VIDEO_EMBED"></iframe>
            </Box>

        </Box>
    </Center>);
}
