import {Drawer, DrawerBody, DrawerCloseButton, DrawerContent, DrawerHeader, DrawerOverlay, List, ListItem, Text} from "@chakra-ui/react";
import {ChatController} from "../../components/Chat";
import {CommandService} from "../../domain/command/CommandService";

interface CommandHistoryDrawer {
    isOpen: boolean;
    chatCtl: ChatController;
    commandService: CommandService
    onClose(): void;
    onOpen(): void;
}

export function CommandHistoryDrawer(props: CommandHistoryDrawer) {
    const {isOpen, onClose, chatCtl, commandService} = props
    return (
        <Drawer
            isOpen={isOpen}
            placement='right'
            onClose={onClose}
        >
            <DrawerOverlay/>
            <DrawerContent>
                <DrawerCloseButton/>
                <DrawerHeader>Command history</DrawerHeader>

                <DrawerBody>
                    <List spacing={1}>
                        {
                            chatCtl.getFlowController().getCommands().map((command, index) => {
                                return (
                                    <ListItem className={"prompt"} key={index} onClick={async () => {
                                        await commandService.handleCommand(command)
                                        onClose()
                                    }}>
                                        <Text>{command.chat}</Text>
                                    </ListItem>
                                )
                            })
                        }

                    </List>
                </DrawerBody>
            </DrawerContent>
        </Drawer>
    )
}
