import { Box, Button } from "@chakra-ui/react";

import { ChatController } from './index';
import { SelectActionRequest, SelectActionResponse } from './index';
import {ReactElement, useCallback} from "react";

export function MuiSelectInput({
  chatController,
  actionRequest,
}: {
  chatController: ChatController;
  actionRequest: SelectActionRequest;
}): ReactElement {
  const chatCtl = chatController;

  const setResponse = useCallback(
    (value: string): void => {
      const option = actionRequest.options.find((o) => o.value === value);
      if (!option) {
        throw new Error(`Unknown value: ${value}`);
      }
      const res: SelectActionResponse = {
        type: 'select',
        value: option.text,
        option,
      };
      chatCtl.setActionResponse(actionRequest, res);
    },
    [actionRequest, chatCtl],
  );

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
          type="button"
          value={o.value}
          onClick={(e): void => setResponse(e.currentTarget.value)}
          colorScheme="blue"
        >
          {o.text}
        </Button>
      ))}
    </Box>
  );
}
