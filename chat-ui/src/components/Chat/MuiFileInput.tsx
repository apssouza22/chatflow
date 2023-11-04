import {
    Box,
    Button,
    Divider,
    Icon,
    List,
    ListItem,
    Text,
} from "@chakra-ui/react";

import {ChatController} from './index';
import {FileActionRequest, FileActionResponse} from './index';
import {ReactElement, useCallback, useState} from "react";
import {IoIosAttach} from "react-icons/io";
import {AiFillFolderOpen, AiOutlineSend} from "react-icons/ai";

export function MuiFileInput({
                                 chatController,
                                 actionRequest,
                             }: {
    chatController: ChatController;
    actionRequest: FileActionRequest;
}): ReactElement {
    const chatCtl = chatController;
    const [files, setFiles] = useState<File[]>([]);

    const handleFileChange = useCallback(
        (fileList: FileList | null): void => {
            // Convert FileList to File[]
            const fileArray: File[] = [];
            if (fileList) {
                for (let i = 0; i < fileList.length; i += 1) {
                    const file = fileList.item(i);
                    if (file) {
                        fileArray.push(file);
                    }
                }
            }
            setFiles(fileArray);
        },
        [],
    );

    const setResponse = useCallback((): void => {
        if (files.length > 0) {
            const value = files.map((f) => f.name).toString();
            const res: FileActionResponse = {type: 'file', value, files};
            chatCtl.setActionResponse(actionRequest, res);
        }
    }, [actionRequest, chatCtl, files]);

    const sendButtonText = actionRequest.sendButtonText
        ? actionRequest.sendButtonText
        : 'Send';

    function cancelUpload() {
        chatCtl.setActionRequest({
            type: 'text',
            placeholder: 'Please enter your text.',
            always: true,
        });
    }

    return (
        <Box
            flex="1 1 auto"
            maxW="100%"
            display="flex"
            flexDirection="column"
            gap={2}
        >
            <List m={2}>
                {files.map((f) => (
                    <Box key={`${f.name}-${f.size}`}>
                        <Divider/>
                        <ListItem key={f.name} style={{
                            display: "flex",
                            alignItems: "center",
                            textAlign: "left",
                            padding: "8px 16px"
                        }}>
                            <IoIosAttach/>
                            <Text isTruncated minW={0}>
                                {f.name}
                            </Text>
                        </ListItem>
                    </Box>
                ))}
            </List>
            <Box
                display="flex"
                alignItems="center"
                justifyContent="space-between"
                gap={2}
            >
                <Button onClick={cancelUpload} >Cancel</Button>
                <Button
                    isDisabled={false}
                    as="label"
                    variant="outline"
                    colorScheme="blue"
                    leftIcon={<AiFillFolderOpen/>}
                >
                    Select file
                    <input
                        type="file"
                        accept={actionRequest.accept}
                        multiple={actionRequest.multiple}
                        onChange={(e): void => handleFileChange(e.target.files)}
                        style={{display: 'none'}}
                    />
                </Button>
                <Button
                    type="button"
                    onClick={setResponse}
                    isDisabled={files.length === 0}
                    variant="solid"
                    colorScheme="blue"
                    leftIcon={<AiOutlineSend/>}
                >
                    {sendButtonText}
                </Button>
            </Box>
        </Box>
    );
}
