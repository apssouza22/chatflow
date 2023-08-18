import {TaskCommand, Command} from "../command/Common";

export interface OnCommandFound {
    (command: TaskCommand): void;
}

export interface OnCommandTriggered {
    (params: OnCommandTriggeredParams): void;
}
export interface OnCommandTriggeredParams{
    command: Command,
    args: any,
    callback: any
}

interface State {
    commands: TaskCommand[];
    onCommandFound: OnCommandFound[]
    onCommandTriggered: OnCommandTriggered[]
}

export class FlowController {
    private state: State;

    constructor() {
        this.state = {
            commands: [],
            onCommandFound: [],
            onCommandTriggered: []
        };
    }

    public getCommands() {
        return [...this.state.commands]
    }

    async callOnCommandTriggered(params: OnCommandTriggeredParams): Promise<void> {
        this.state.onCommandTriggered.map(async (h) => {
            await h(params)
            // Not waiting if outside the async function
            params.callback(false)
        });
    }

    addOnCommandTriggered(callback: OnCommandTriggered): void {
        this.state.onCommandTriggered.push(callback)
    }

    addCommand(taskCommand: TaskCommand) {
        this.state.commands.push(taskCommand)
    }
}
