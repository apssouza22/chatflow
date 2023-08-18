import {ActionRequest, AudioActionResponse, ChatController, FileActionResponse} from "../../components/Chat";
import {useCallback} from "react";
import {Button} from "@chakra-ui/react";
import * as React from "react";
export const AVATAR_IMG = "/chat-commander-ui/img/geek-bot.jpeg"
export async function askIfShouldDemoTheInputs(chatCtl: ChatController) {
    await chatCtl.addMessage({
        type: 'text',
        content: `Hi there! Can I show you all the input types available?`,
        self: false,
        avatar: AVATAR_IMG
    });
    const showAllTypes = await chatCtl.setActionRequest({
        type: 'select',
        options: [
            {
                value: 'yes',
                text: 'Yes',
            },
            {
                value: 'no',
                text: 'No',
            }
        ],
    });
    await chatCtl.addMessage({
        type: 'text',
        content: `You have selected ${showAllTypes.value}.`,
        self: false,
        avatar: AVATAR_IMG,
    });

    if (showAllTypes.value === 'Yes') {
        await allTypesNavigation(chatCtl);
    }
}

async function allTypesNavigation(chatCtl: ChatController): Promise<void> {

    await chatCtl.addMessage({
        type: 'text',
        content: `What is your gender?`,
        self: false,
        avatar: AVATAR_IMG
    });
    const sel = await chatCtl.setActionRequest({
        type: 'select',
        options: [
            {
                value: 'man',
                text: 'Man',
            },
            {
                value: 'woman',
                text: 'Woman',
            },
            {
                value: 'other',
                text: 'Other',
            },
        ],
    });
    await chatCtl.addMessage({
        type: 'text',
        content: `You have selected ${sel.value}.`,
        self: false,
        avatar: AVATAR_IMG
    });

    await chatCtl.addMessage({
        type: 'text',
        content: `What is your favorite fruit?`,
        self: false,
        avatar: AVATAR_IMG
    });
    const mulSel = await chatCtl.setActionRequest({
        type: 'multi-select',
        options: [
            {
                value: 'apple',
                text: 'Apple',
            },
            {
                value: 'orange',
                text: 'Orange',
            },
            {
                value: 'none',
                text: 'None',
            },
        ],
    });
    await chatCtl.addMessage({
        type: 'text',
        content: `You have selected '${mulSel.value}'.`,
        self: false,
        avatar: AVATAR_IMG
    });

    await chatCtl.addMessage({
        type: 'text',
        content: `What is your favorite picture?`,
        self: false,
        avatar: AVATAR_IMG
    });
    const file = (await chatCtl.setActionRequest({
        type: 'file',
        accept: 'image/*',
        multiple: true,
    })) as FileActionResponse;
    await chatCtl.addMessage({
        type: 'jsx',
        content: (
            <div>
                {file.files.map((f) => (
                    <img
                        key={file.files.indexOf(f)}
                        src={window.URL.createObjectURL(f)}
                        alt="File"
                        style={{width: '100%', height: 'auto'}}
                    />
                ))}
            </div>
        ),
        self: false,
        avatar: AVATAR_IMG
    });

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

    await (audio.audio
        ? chatCtl.addMessage({
            type: 'jsx',
            content: (
                <a href={window.URL.createObjectURL(audio.audio)}>Audio downlaod</a>
            ),
            self: false,
            avatar: AVATAR_IMG
        })
        : chatCtl.addMessage({
            type: 'text',
            content: audio.value,
            self: false,
            avatar: AVATAR_IMG
        }));

    await chatCtl.addMessage({
        type: 'text',
        content: `Please press the button.`,
        self: false,
        avatar: AVATAR_IMG
    });

    const good = await chatCtl.setActionRequest({
        type: 'custom',
        Component: GoodInput,
    });
    await chatCtl.addMessage({
        type: 'text',
        content: `You have pressed the ${good.value} button.`,
        self: false,
        avatar: AVATAR_IMG
    });
}

function GoodInput({
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
        <div>
            <Button
                type="button"
                onClick={setResponse}
                variant="solid"
                color="primary"
            >
                Good!
            </Button>
        </div>
    );
}
