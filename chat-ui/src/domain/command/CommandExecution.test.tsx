import {Command, convertText} from "./Common";
import {CommandExecution, extractFnBody} from "./CommandExecution";
import {HttpClient} from "../common/HttpClient";
import {SessionManager} from "../session/SessionManager";


test("Execute Javascript ", () => {
    const exec = new CommandExecution(new HttpClient(""), SessionManager.getInstance())
    let command: Command = {
        name: "js_func",
        function: {
            name: "openChatbot",
            code: "function openChatbot(){ let script = document.createElement('script'); script.src = 'https://apps.newaisolutions.com/assets/demos/new-bot.js'; document.head.appendChild(script); }",
            param: new Map<string, string>()
        }
    };
    exec.executeCommand(command, {})
})

test("Extract function body", () => {
    const fn = "function openChatbot(){ let script = document.createElement('script'); script.src = 'https://apps.newaisolutions.com/assets/demos/new-bot.js'; document.head.appendChild(script); }"
    const body = extractFnBody(fn)
    expect(body).not.toContain('function openChatbot(){ ')
})

test("Extract function body without function ", () => {
    const fn = "let script = document.createElement('script'); script.src = 'https://apps.newaisolutions.com/assets/demos/new-bot.js'; document.head.appendChild(script); }"
    const body = extractFnBody(fn)
    expect(body).toContain(fn)
})