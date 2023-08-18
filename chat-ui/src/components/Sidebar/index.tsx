import {Button, Flex, List, ListItem, Text} from "@chakra-ui/react"
import {LogoutIcon} from "../Icons/Icons";
import "./style.css"
import {useChatContext} from "../../hooks/useChatContext";
import {PropsWithChildren, useEffect, useState} from "react";
import {ChatController} from "../Chat";

type MuiChatParams = {
    chatController?: ChatController;
    isHome?: boolean;
};

const homePrompts = [
    "Why make the interface so different?",
    "What is the potential of natural language interfaces?",
    "Can the chatbot help me automate complex tasks?",
    "Do you only sell chatbots?",
    "How much do the chatbots cost?",
    "Open chatbot",
    "Help me send an email",
    "Add document",
]

const adminPrompts = [
    "Register a new admin user as follow: alex; 123; alex@gmail.com",
    "Create a new application",
    "List my applications",
    "List docs for the app {{app_key}}",
    "Update user session with app {{app_key}}",
    "Add new documentation",
    "Create a new address with the following: Camac crescent, Co. Dublin, Dublin, Ireland, D08f9g9",
    "++ Please return the same command but set addressLine2=Inchicore",
    "Help me to book a free class to my son",
    "Help me to book a free class for tomorrow"
    // "create a new private repository name=test repo and allow squash merge",
    // "++ return the same command but this time include all the available fields option",
    // list my repositories
    // ++ sort by created asc
    // ++ display as a chart with the fields: full_name and forks_count

]
export default function Sidebar({chatController, isHome}: PropsWithChildren<MuiChatParams>) {
    const {dispatch} = useChatContext()
    const [prompts, _] = useState(isHome ? homePrompts : adminPrompts);

    //https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28

    function setPrompt(prompt: string) {
        if (!chatController) {
            dispatch({type: "SET_PROMPT", payload: prompt})
            return
        }
        chatController.setActionRequest({
            type: 'text',
            always: true,
            defaultValue: prompt
        })
    }

    return (
        <Flex direction={"column"}
              grow="1"
              align="start"
              p={"100px 30px 30px 30px"}
        >
            <List spacing={1} w={"100%"}>
                {prompts.map((prompt, index) => (
                    <ListItem className={"prompt"} key={index} onClick={() => {
                        setPrompt(prompt)
                    }}>
                        <Text>{prompt}</Text>
                    </ListItem>
                ))}
            </List>

            <Button
                leftIcon={<LogoutIcon/>}
                alignSelf={"center"}
                size="md"
                variant="ghost"
                height={"50px"}
                borderTop={"1px solid #E2E8F0"}
                width={"100%"}
                marginTop={"auto"}
            >
                Logout
            </Button>
        </Flex>
    )
}
