from core.agency.agents import AgentBase, Task


class QuestionAnswerAgent(AgentBase):

    def __init__(self, name, llm_service):
        super().__init__(name, llm_service)
        self.system_prompt = """You are a sales assistant responsible for helping answer user questions and help him to take the decision of buying the product or service.\n
If you are unsure and the answer is not explicitly written in the documentation, say 
"Sorry, I don't know how to help with that." \n\n
Given the following information from the documentation provide for the user's question using only this information
"""

    def process(self, task: Task) -> Task:
        content = f'\n\nHISTORY\n -----------------\n user: {task.input}'
        f'\nRESPONSE: '

        resp = self.llm_service.infer_using_pro([
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "system",
                "content": f"\nDOCUMENTATION\n----------------------------\n\n{task.context}\n\n"
            },
            {
                "role": "user",
                "content": "Make sure to always translate your answer to the user's language based on words in the user input. \n"
            },
            {
                "role": "user",
                "content":"""
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
