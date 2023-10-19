import {
    ActionRequest,
    ActionResponse,
    ChatOption,
    Message,
    MessageContent,
    OnActionChanged,
    OnActionResponsed,
    OnMessagesChanged,
} from './index';
import {AVATAR_IMG} from "../../pages/chatflow/inputs";
import {FlowController} from "../../domain/common/FlowController";
import {FileActionResponse} from "../../components/Chat/chat-types";
import { CommandService } from '../../domain/command/CommandService';

interface ChatState {
    option: ChatOption;
    messages: Message<MessageContent>[];
    action: Action;
    actionHistory: Action[];
    onMessagesChanged: OnMessagesChanged[];
    onActionChanged: OnActionChanged[];
}

interface Action {
    request: ActionRequest;
    responses: ActionResponse[];
    onResnponsed: OnActionResponsed[];
}
export const defaultMsgObj = {
    type: 'text',
    content: "",
    self: false,
    avatar: AVATAR_IMG,
    className: "msg-bot"
};


export class ChatController {
    private state: ChatState;
    private commandService: CommandService;

    private defaultOption: ChatOption = {
        delay: 300,
    };

    private emptyAction: Action = {
        request: {type: 'empty'},
        responses: [],
        onResnponsed: [],
    };

    private defaultActionRequest = {
        always: false,
        addMessage: true,
    };
    private flowController: FlowController;

    constructor(flowController: FlowController, option?: ChatOption) {
        this.flowController = flowController
        this.state = {
            option: {...this.defaultOption, ...option},
            messages: [],
            action: this.emptyAction,
            actionHistory: [],
            onMessagesChanged: [],
            onActionChanged: [],
        };
    }

    public setCommandService(commandService: CommandService) {
        this.commandService = commandService
    }

    getFlowController() {
        return this.flowController
    }

    addMessage(message: Message<MessageContent>): Promise<number> {
        return new Promise((resolve) => {
            setTimeout(() => {
                const len = this.state.messages.push(message);
                const idx = len - 1;
                this.state.messages[idx].createdAt = new Date();
                this.callOnMessagesChanged();

                resolve(idx);
            }, this.state.option.delay);
        });
    }

    updateMessage(index: number, message: Message<MessageContent>): void {
        if (message !== this.state.messages[index]) {
            const {createdAt} = this.state.messages[index];
            this.state.messages[index] = message;
            this.state.messages[index].createdAt = createdAt;
        }

        this.state.messages[index].updatedAt = new Date();
        this.callOnMessagesChanged();
    }

    removeMessage(index: number): void {
        this.state.messages[index].deletedAt = new Date();
        this.callOnMessagesChanged();
    }

    getMessages(): Message<MessageContent>[] {
        return this.state.messages;
    }

    setMessages(messages: Message<MessageContent>[]): void {
        this.clearMessages();
        this.state.messages = [...messages];
        this.callOnMessagesChanged();
    }

    clearMessages(): void {
        this.state.messages = [];
        this.callOnMessagesChanged();
    }

    private callOnMessagesChanged(): void {
        this.state.onMessagesChanged.map((h) => h(this.state.messages));
    }

    addOnMessagesChanged(callback: OnMessagesChanged, index = null): void {
        this.state.onMessagesChanged = updateArray(this.state.onMessagesChanged, callback, index);
    }

    removeOnMessagesChanged(callback: OnMessagesChanged): void {
        const idx = this.state.onMessagesChanged.indexOf(callback);
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        this.state.onActionChanged[idx] = (): void => {
        };
    }

    setActionRequest<T extends ActionRequest>(
        request: T,
        onResponse?: OnActionResponsed,
    ): Promise<ActionResponse> {
        const action: Action = {
            request: {...this.defaultActionRequest, ...request},
            responses: [],
            onResnponsed: [],
        };

        // See setActionResponse method
        return new Promise((resolve, reject) => {
            if (!request.always) {
                const returnResponse = (response: ActionResponse): void => {
                    if (!response.error) {
                        resolve(response);
                    } else {
                        reject(response.error);
                    }
                };
                action.onResnponsed.push(returnResponse);
            }

            if (onResponse) {
                action.onResnponsed.push(onResponse);
            }

            this.state.action = action;
            this.state.actionHistory.push(action);
            this.callOnActionChanged(action.request);

            if (request.always) {
                resolve({type: 'text', value: 'dummy'});
            }
        });
    }

    cancelActionRequest(): void {
        this.state.action = this.emptyAction;
        this.callOnActionChanged(this.emptyAction.request);
    }

    getActionRequest(): ActionRequest | undefined {
        const {request, responses} = this.state.action;
        if (!request.always && responses.length > 0) {
            return undefined;
        }

        return request;
    }

    async setActionResponse(
        request: ActionRequest,
        response: ActionResponse,
    ): Promise<void> {
        const {request: origReq, responses, onResnponsed} = this.state.action;
        if (request !== origReq) {
            throw new Error('Invalid action.');
        }
        if (!request.always && onResnponsed.length === 0) {
            throw new Error('onResponsed is not set.');
        }

        if (request.type === 'file') {
            this.commandService.addFiles((response as FileActionResponse).id, (response as FileActionResponse).files)
        }
        responses.push(response);

        if (request.addMessage) {
            await this.addMessage({
                type: 'text',
                content: response.value,
                self: true,
            });
        }
        this.callOnActionChanged(request, response);

        onResnponsed.map((h) => h(response));
    }

    getActionResponses(): ActionResponse[] {
        return this.state.action.responses;
    }

    private callOnActionChanged(
        request: ActionRequest,
        response?: ActionResponse,
    ): void {
        this.state.onActionChanged.map((h) => h(request, response));
    }

    addOnActionChanged(callback: OnActionChanged, index = null): void {
        this.state.onActionChanged = updateArray(this.state.onActionChanged, callback, index);
    }

    removeOnActionChanged(callback: OnActionChanged): void {
        const idx = this.state.onActionChanged.indexOf(callback);
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        this.state.onActionChanged[idx] = (): void => {
        };
    }

    getOption(): ChatOption {
        return this.state.option;
    }
}

function updateArray(list, callback, index = null) {
    if (index === null || list.length === 0) {
        list.push(callback);
        return list;
    }

    if (index < 0) {
        throw new Error("Invalid index. Index should greater than or equal to 0.");
    }
    const newArray = [...list];

    // Move existing items one index up to make space for the new record
    for (let i = newArray.length - 1; i >= index; i--) {
        newArray[i + 1] = newArray[i];
    }

    newArray[index] = callback;
    return newArray;
}
