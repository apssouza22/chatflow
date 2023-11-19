import {ActionRequest, ChatController} from "../../components/Chat";
import {AVATAR_IMG} from "../../pages/chatflow/inputs";
import {useCallback} from "react";
import {Box, Button, FormControl, FormLabel, Input, VStack} from "@chakra-ui/react";

export async function showCustomField(chatCtl: ChatController) {
    if (localStorage.getItem("displayedForm") !== "true") {
        await showEmailForm(chatCtl)
    }
}

async function showEmailForm(chatCtl: ChatController) {
    localStorage.setItem("displayedForm", "true")
    await chatCtl.addMessage({
        type: 'text',
        content: `Would you like to be contacted by a member of our team?`,
        self: false,
        avatar: AVATAR_IMG
    });
    const sel = await chatCtl.setActionRequest({
        type: 'select',
        options: [
            {
                value: 'yes',
                text: 'Yes',
            },
            {
                value: 'no',
                text: 'No',
            },
        ],
    });
    if (sel.value === 'Yes') {
        const good = await chatCtl.setActionRequest({
            type: 'custom',
            Component: ContactForm,
        });
        return
    }
    await chatCtl.setActionRequest({
            type: 'text',
            placeholder: 'Please enter your text.',
            always: true,
        },
    );
}

function ContactForm(
    {
        chatController,
        actionRequest,
    }: {
        chatController: ChatController;
        actionRequest: ActionRequest;
    }) {
    const chatCtl = chatController;
    const setResponse = useCallback(async () => {
        await chatCtl.addMessage({
            type: 'text',
            content: `Thank you for your email. We will get back to you soon.`,
            self: false,
            avatar: AVATAR_IMG
        });
        await chatCtl.setActionRequest({
                type: 'text',
                placeholder: 'Please enter your text.',
                always: true,
            },
        );
    }, [actionRequest, chatCtl]);
    return (
        <Box bg={"gray.50"} p={4} borderRadius={"md"} width={"md"}>
            <VStack spacing={4}>
                <FormControl id="email" isRequired>
                    <FormLabel>Email address</FormLabel>
                    <Input
                        name={"email"}
                        type="email"
                        placeholder="Enter your email"
                        size="md"
                    />
                </FormControl>
                <FormControl id="name" isRequired>
                    <FormLabel>Name</FormLabel>
                    <Input
                        type="text"
                        placeholder="Enter your name"
                        size="md"
                    />
                </FormControl>
                <Button colorScheme="blue" onClick={setResponse} mt={4}>
                    Send
                </Button>)
            </VStack>
        </Box>
    );
}
