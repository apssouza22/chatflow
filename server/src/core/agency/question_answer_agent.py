from core.agency.agents import AgentBase, Task
from core.memory.chat_memory_service import ChatMemoryService


def _prepare_history(short_memory: list[dict]) -> list[dict]:
    history = []
    limit = 5
    count = 0
    for msg in reversed(short_memory):
        if count >= limit:
            break
        if msg["role"] == "user":
            count += 1
        history.append(msg)

    last_msg = history[0]
    for msg in history[1:]:
        if last_msg.get("context") == msg.get("context"):
            msg["context"] = ""

    history.reverse()
    return history


def _build_msg_context(history):
    msgs = []
    contexts = []
    for msg in history:
        if msg["role"] == "user":
            msgs.append("User: " + msg["message"])
            contexts.append(msg.get("context", ""))
            continue
        if msg["role"] == "assistant":
            msgs.append("Assistant: " + msg["message"])
    return msgs, contexts


class QuestionAnswerAgent(AgentBase):

    def __init__(self, name, llm_service, chat_memory: ChatMemoryService):
        super().__init__(name, llm_service)
        self.chat_memory = chat_memory
        self.system_prompt = """You are a sales assistant responsible for helping answer user questions and help him to take the decision of buying the product or service.\n
If you are unsure and the answer is not explicitly written in the documentation, say 
"Sorry, I don't know how to help with that." \n\n
Given the following information from the documentation provide for the user's question using only this information
"""

    def process(self, task: Task) -> Task:
        short_memory = self.chat_memory.get_short_memory(task.context)
        long_memory = self.chat_memory.get_long_memory(task.context)
        history = _prepare_history(short_memory)
        msgs, contexts = _build_msg_context(history)

        str_msgs = "\n\n".join(msgs)
        str_contexts = "\n\n".join(contexts)
        str_contexts += "\n\n".join(long_memory)

        content = f'\n\nHISTORY\n -----------------\n {str_msgs}'
        f'\nRESPONSE: '

        resp = self.llm_service.infer_using_pro([
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "system",
                "content": f"\nDOCUMENTATION\n----------------------------\n\n{str_contexts}\n\n"
            },
            {
                "role": "user",
                "content": "Make sure to always translate your answer to the user's language based on words in the user input. \n"
            },
            {
                "role": "user",
                "content": """
Be friendly. Always make the user feel important. Use your knowledge of effective customer service techniques. \n
End the response with questions to keep the user engaged and achieve your goal which is help the user take the decision about buying the product or service\n 
IMPORTANT: If the given content contains links, make sure you include them in the answer. \n
IMPORTANT: If the given content contains image urls, make sure you include them in the answer.\n 
IMPORTANT: Consider past user message and the assistant responses as context to your response. \n
"""
            },
            {
                "role": "user",
                "content": content
            }
        ])
        task.set_output(resp)
        return task
