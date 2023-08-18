import {Box, Button, Icon, Stack} from "@chakra-ui/react";

import {ReactElement, useCallback, useState} from "react";
import { ChatController } from './index';
import {
  MultiSelectActionRequest,
  MultiSelectActionResponse,
} from './chat-types';
import {AiOutlineSend} from "react-icons/ai";
export function MuiMultiSelectInput({
  chatController,
  actionRequest,
}: {
  chatController: ChatController;
  actionRequest: MultiSelectActionRequest;
}): ReactElement {
  const chatCtl = chatController;
  const [values, setValues] = useState<string[]>([]);

  const handleSelect = useCallback(
    (value: string): void => {
      if (!values.includes(value)) {
        setValues([...values, value]);
      } else {
        setValues(values.filter((v) => v !== value));
      }
    },
    [values],
  );

  const setResponse = useCallback((): void => {
    const options = actionRequest.options.filter((o) =>
      values.includes(o.value),
    );

    const res: MultiSelectActionResponse = {
      type: 'multi-select',
      value: options.map((o) => o.text).toString(),
      options,
    };
    chatCtl.setActionResponse(actionRequest, res);
    setValues([]);
  }, [actionRequest, chatCtl, values]);

  const sendButtonText = actionRequest.sendButtonText
    ? actionRequest.sendButtonText
    : 'Send';

    return (
        <Box
            flex="1 1 auto"
            display="flex"
            flexDirection="column"
            gap={2}
        >
            {actionRequest.options.map((o) => (
                <Button
                    key={actionRequest.options.indexOf(o)}
                    value={o.value}
                    onClick={(e): void => handleSelect(e.currentTarget.value)}
                    variant={!values.includes(o.value) ? 'outline' : 'solid'}
                    colorScheme="blue"
                >
                    {o.text}
                </Button>
            ))}
            <Button
                onClick={setResponse}
                isDisabled={values.length === 0}
                colorScheme="blue"
                leftIcon={<AiOutlineSend/>}
            >
                {sendButtonText}
            </Button>
        </Box>
    );
}
