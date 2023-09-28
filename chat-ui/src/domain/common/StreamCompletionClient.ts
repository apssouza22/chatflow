
export class StreamCompletionClient {
    private readonly baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async call(context:string, prompt:string, callback: (data)=> void): Promise<void> {
        const response = await fetch(`${this.baseUrl}/chat/completions/stream`, {
            method: 'POST',
            headers: {
                'Accept': 'text/event-stream',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "question": prompt,
                "context": context
            })
        })
        const reader = response.body.pipeThrough(new TextDecoderStream()).getReader()
        async function streamListener() {
            const {value, done} = await reader.read();
            console.log('Received =>', value);
            if (value.includes('data:')) {
                let data = value.replace('data:', '');
                data = data.replace('event: message', '');
                console.log("data =>", data)
                const item = JSON.parse(data);

                callback(item)

                console.log(item.choices[0]);
                if (item.choices[0].finish_reason === "stop") {
                    console.log("Finished");
                    return
                }
            }
            requestAnimationFrame(streamListener);
        }
        streamListener();
    }
}
