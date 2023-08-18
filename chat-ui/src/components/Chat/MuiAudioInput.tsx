import { Box, Button, Icon } from "@chakra-ui/react";

import { AudioMediaRecorder } from './AudioMediaRecorder';
import { AudioActionRequest, AudioActionResponse } from './chat-types';
import {ReactElement, useCallback, useState} from "react";
import {ChatController} from "./ChatController";
import {MdKeyboardVoice} from "react-icons/md";
import {FaStopCircle} from "react-icons/fa";
import {AiOutlineSend} from "react-icons/ai";

export function MuiAudioInput({
  chatController,
  actionRequest,
}: {
  chatController: ChatController;
  actionRequest: AudioActionRequest;
}):ReactElement {
  const chatCtl = chatController;
  const [audioRec] =useState(AudioMediaRecorder.getInstance());
  const [stopped, setStopped] =useState(true);
  const [audio, setAudio] =useState<Blob | undefined>();

  const handleError =useCallback(
    (error: Error): void => {
      const value: AudioActionResponse = {
        type: 'audio',
        value: error.message,
        error,
      };
      chatCtl.setActionResponse(actionRequest, value);
    },
    [actionRequest, chatCtl],
  );

  const handleStart =useCallback(async (): Promise<void> => {
    try {
      await audioRec.initialize();
      await audioRec.startRecord();
      setStopped(false);
    } catch (error) {
      handleError(error as Error);
    }
  }, [audioRec, handleError]);

  const handleStop =useCallback(async (): Promise<void> => {
    try {
      const a = await audioRec.stopRecord();
      setAudio(a);
      setStopped(true);
    } catch (error) {
      handleError(error as Error);
    }
  }, [audioRec, handleError]);

  const sendResponse =useCallback((): void => {
    if (audio) {
      const value: AudioActionResponse = {
        type: 'audio',
        value: 'Audio',
        audio,
      };
      chatCtl.setActionResponse(actionRequest, value);
      setAudio(undefined);
    }
  }, [actionRequest, audio, chatCtl]);

  const sendButtonText = actionRequest.sendButtonText
    ? actionRequest.sendButtonText
    : 'Send';

  return (
      <Box
          flex="1 1 auto"
          display="flex"
          css={{
            '& > *': {
              flex: '1 1 auto',
              minWidth: '0',
            },
            '& > * + *': {
              marginLeft: '1',
            },
          }}
      >
        {stopped && (
            <Button
                type="button"
                onClick={handleStart}
                isDisabled={!stopped}
                variant="solid"
                colorScheme="blue"
                leftIcon={<MdKeyboardVoice/>}
            >
              Rec start
            </Button>
        )}
        {!stopped && (
            <Button
                type="button"
                onClick={handleStop}
                isDisabled={stopped}
                variant="solid"
                colorScheme="blue"
                leftIcon={<FaStopCircle/>}
            >
              Rec stop
            </Button>
        )}
        <Button
            type="button"
            onClick={sendResponse}
            isDisabled={!audio}
            variant="solid"
            colorScheme="blue"
            leftIcon={<AiOutlineSend/>}
        >
          {sendButtonText}
        </Button>
      </Box>
  );
}
