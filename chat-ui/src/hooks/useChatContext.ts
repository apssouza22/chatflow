import {ChatContext, ChatState} from "../context/ChatContext"
import {useContext} from "react"

export const useChatContext = (): ChatState => {
    const context = useContext<ChatState>(ChatContext)

    if (!context) {
        throw Error('useChatContext must be used inside an ChatContextProvider')
    }

    return context
}
