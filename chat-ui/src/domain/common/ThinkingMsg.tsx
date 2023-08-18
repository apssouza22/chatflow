import {ReactElement, useEffect, useState} from "react";

export function ThinkingMsg(): ReactElement {
    const [msg, setMsg] = useState("Thinking...")
    useEffect(() => {
        const interval = setInterval(() => {
            const text = msgs[Math.floor(Math.random() * msgs.length)]
            setMsg(text)
        }, 3000);
        return () => clearInterval(interval);
    }, [msg]);

    return (<div>{msg}</div>)
}

const msgs = [
    "Hang tight, we're working on it!",
    "Just a moment, almost there...",
    "Your request is being processed.",
    "Hold on, we're crunching the numbers.",
    "Working on your request. This will just take a second.",
    "We're on it! Shouldn't be much longer.",
    "Brewing up something special for you!",
    "Please wait while we gather the information.",
    "Doing the magic behind the scenes...",
    "Getting things ready for you.",
    "Making sure everything is perfect. Hang on!",
    "Almost done, thanks for waiting!",
    "Please bear with us. Your request is important!",
    "We're making it happen! Just a little longer.",
    "Hold on tight! We're almost finished.",
]