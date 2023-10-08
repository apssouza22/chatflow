import {SessionManager} from "../session/SessionManager";

export class StreamCompletionClient {
    private readonly baseUrl: string;
    private session: SessionManager;

    constructor(baseUrl: string, session: SessionManager) {
        this.baseUrl = baseUrl;
        this.session = session;
    }

    private getHeaders() {
        return {
            "Authorization": "Bearer " + this.session.getSessionData().token,
            "AppKey": this.session.getSessionData().app,
            "PluginMode": this.session.getSessionData().isPluginMode.toString(),
            "sessionId": this.session.getSessionData().sessionId,
        };
    }

    async call(prompt: string, context: string, callback: (data, done: boolean) => void): Promise<void> {
        const response = await fetch(`${this.baseUrl}/chat/completions/stream`, {
            method: 'POST',
            headers: {
                'Accept': 'text/event-stream',
                'Content-Type': 'application/json',
                ...this.getHeaders()
            },
            body: JSON.stringify({
                "question": prompt,
                "context": context
            })
        })
        const reader = response.body.pipeThrough(new TextDecoderStream()).getReader()
        const self = this;

        async function streamListener() {
            const {value, done} = await reader.read();
            console.log('Received SSE event =>', value);
            let isDone = false;
            if (value && value.includes('data:')) {
                let items = value.split("data:");
                isDone = self.handleItems(items, callback);
            }
            console.log('isDone =>', done)
            if (value == null || isDone) {
                return
            }
            requestAnimationFrame(streamListener);
        }

        streamListener();
    }

    private handleItems(items: string[], callback: (data: any, done: boolean) => void): boolean {
        let done = false;
        for (let data of items) {
            if (data === "") {
                continue
            }

            let jsonData = {
                choices: []
            }
            try {
                data = data.replace(new RegExp('event: message', 'g'), '');
                jsonData = JSON.parse(data);
            } catch (error) {
                console.error("Invalid JSON:", data);
                continue;
            }

            if (jsonData.choices[0].finish_reason === "stop") {
                done = true;
            }
            callback(jsonData, done)
            if (done) {
                return done
            }
        }
        return done
    }
}