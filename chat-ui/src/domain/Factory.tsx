import {HttpClient} from "./common/HttpClient";
import {FlowController} from "./common/FlowController";
import {ChatController} from "../components/Chat";
import {SessionManager} from "./session/SessionManager";
import {defaultMsgObj} from "../components/Chat";
import {commandServiceFactory} from "./command/CommandService";
import {ThinkingMsg} from "./common/ThinkingMsg";

const session = SessionManager.getInstance()
const httpClient = new HttpClient(process.env.REACT_APP_SERVER_URL);
const flowCtl = new FlowController()
export const chatCtl = new ChatController(flowCtl, {showDateTime: true});

if (session.getSessionData().app == null) {
    session.setAppKey("chat")
}
console.log("session app", session.getSessionData().app)

const actionListener = async (req, resp) => {
    if (resp == null) {
        return
    }
    await chatCtl.addMessage({...defaultMsgObj, type: "jsx", className: "command-loading", content: <ThinkingMsg/>});
    await commandService.process(resp)
    const msgs = chatCtl.getMessages()
    let loadingMsgIndex =0
    msgs.forEach((v, i)=>{
        if (v.className == "command-loading"){
            loadingMsgIndex = i
        }
    })
    chatCtl.removeMessage(loadingMsgIndex) // remove the "Thinking..." message
}

export const commandService = commandServiceFactory(
    chatCtl,
    session,
    httpClient,
    new HttpClient("")
)

chatCtl.addOnMessagesChanged(() => {
}, 1);

chatCtl.addOnActionChanged(actionListener, 1);

