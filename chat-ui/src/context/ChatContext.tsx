import {createContext, PropsWithChildren, useReducer} from 'react'
import {TaskCommand} from "../domain/command/Common";

export interface ChatState {
    commands: Array<TaskCommand>
    prompt: string
    user: string
    dispatch: React.Dispatch<Action>
}

export interface Action {
    type: string
    payload: any
}

let defaultValue = {
    commands: Array<TaskCommand>(),
    prompt: '',
    user: '',
    dispatch: () => {}
}

export const ChatContext = createContext<ChatState>(defaultValue)

const chatReducer = (state: ChatState, action: Action) => {
    switch (action.type) {
        case 'LOGIN':
            return {...state, user: action.payload}
        case 'SET_PROMPT':
            return {...state, prompt: action.payload}
        case 'SET_COMMAND':
            if (!state.commands.includes(action.payload)) {
                state.commands.push(action.payload);
            }
            return {...state}
        default:
            return state
    }
}

export const ChatContextProvider = ({children}: PropsWithChildren) => {
    const [state, dispatch] = useReducer(chatReducer, defaultValue)

    return (
        <ChatContext.Provider value={{...state, dispatch}}>
            {children}
        </ChatContext.Provider>
    )

}
