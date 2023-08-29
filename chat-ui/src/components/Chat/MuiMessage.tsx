import {Avatar, Box, Fade, Text} from '@chakra-ui/react';

import {Message, MessageContent} from './index';

export function MuiMessage({
                               id,
                               message,
                               showDate,
                               showTime,
                           }: {
    id: string;
    message: Message<MessageContent>;
    showDate: boolean;
    showTime: boolean;
}): React.ReactElement {
    if (message.deletedAt) {
        return <div id={id}/>;
    }

    const dispDate = message.updatedAt ? message.updatedAt : message.createdAt;

    const ChatAvator = (
        <Box
            minWidth={0}
            flexShrink={0}
            ml={message.self ? 1 : 0}
            mr={message.self ? 0 : 1}
        >
           
        </Box>
    );

    const ChatUsername = (
        <Box maxWidth="100%" mx={1}>
            <Text isTruncated textAlign={message.self ? 'right' : 'left'} whiteSpace={"pre-wrap"}>
                {message.username}
            </Text>
        </Box>
    );

    const ChatDate = (
        <Box maxWidth="100%" mx={1}>
            <Text
                isTruncated
                textAlign={message.self ? 'right' : 'left'}
                color="gray.500"
                fontSize={12}
            >
                {dispDate?.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                })}
            </Text>
        </Box>
    );

    return (
        <Fade in className={"chat-message-container"}>
            <Box maxWidth="100%" display="flex" flexDirection="column"  p={2}>
                {showDate && (
                    <Text textAlign="center">
                        {dispDate?.toLocaleDateString(["en-ie"], {})}
                    </Text>
                )}
                <Box
                    id={id}
                    maxWidth="100%"
                    my={1}
                    display="flex"
                    justifyContent={message.self ? 'flex-end' : 'flex-start'}
                    style={{overflowWrap: 'break-word'}}
                >
                    {message.avatar && !message.self && ChatAvator}
                    <Box minWidth={0} bg='gray.100' display="flex" flexDirection="column" className={message.className}>
                        {message.username && ChatUsername}
                        <Box
                            maxWidth="100%"
                            width={message.self ? '100%' : '100vw'}
                            py={1}
                            px={2}
                            bg={message.self ? 'blue.400' : 'gray.100'}
                            color={message.self ? 'white' : 'black'}
                            borderRadius={message.self ? 'md' : '10pt'}
                            shadow={message.self ? 'md' : 'md'}
                            fontSize="md"
                        >
                            {message.type === 'text' && (
                                <Text style={{whiteSpace: 'pre-wrap'}}>
                                    {message.content}
                                </Text>
                            )}
                            {message.type === 'jsx' && <div>{message.content}</div>}
                        </Box>
                        {showTime && ChatDate}
                    </Box>
                    {message.avatar && message.self && ChatAvator}
                </Box>
            </Box>
        </Fade>
    );
}
