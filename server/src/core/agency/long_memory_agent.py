from core.agency.agents import Task, AgentBase
from core.agency.json_extractor_agent import JSONExtractorAgent
from core.memory.chat_memory_service import ChatMemoryService


class LongMemoryAgent(AgentBase):
    def __init__(self, name, llm_service, chat_memory: ChatMemoryService, json_extractor_agent: JSONExtractorAgent):
        super().__init__(name, llm_service)
        self.json_extractor_agent = json_extractor_agent
        self.chat_memory = chat_memory
        self.system_prompt = """You are a supervisor managing a team of knowledge experts.
Your team's job is to create a perfect knowledge base about the user interests to assist the user visiting the website.
The knowledge base should ultimately consist of many discrete pieces of information that add up to a rich persona (e.g. I like the product x; I am interested in BJJ; I want to execute actions; I live in Austin, Texas).
Every time you receive a message, you will evaluate if it has any information worth recording in the knowledge base.
A message may contain multiple pieces of information that should be saved separately.
You are only interested in the following categories of information:
1. The user's product interests (e.g. I am interested on the product 1 or I am interested on the product 2)
2. Where the user lives (e.g. I live in São Paulo, Brazil)
3. Sports the user likes (e.g. I like BJJ or I like football)

When you receive a message, you perform a sequence of steps consisting of:
1. Analyze the most recent Human message for information. You will see multiple messages for context, but we are only looking for new information in the most recent message.
2. Compare this to the knowledge you already have.
3. Only add the user information if it is new or different from what you already have.
"""

    def process(self, task: Task) -> Task:
        long_memories = [msg for msg in self.chat_memory.get_long_memory(task.context)]
        str_long_memory = "\n".join(long_memories)
        dynamic_sys_prompt = f"""
Here are the existing bits of information that we have about the user.

```
{str_long_memory}
```

I will tip you $20 if you are perfect, and I will fine you $40 if you miss any important information or change any incorrect information.
Take a deep breath, think step by step, and then analyze the following message:
"""
        resp = self.llm_service.infer_using_basic([
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "system",
                "content": dynamic_sys_prompt
            },
            {
                "role": "user",
                "content": f"IMPORTANT: Respond with a valid JSON and nothing else as the following example: {{'response': [{{'info': 'the knowledge about the user','info_status': 'new|existing|changed'}}]}}"
            },
            {
                "role": "user",
                "content": f"User's inputs: {task.input}\n"
            }
        ])
        json_resp = self.json_extractor_agent.process(Task(resp.message))
        for info in json_resp.output.message.get("response"):
            if "info" in info and "info_status" in info:
                if info["info_status"] == "new":
                    self.chat_memory.update_long_memory(task.context, info["info"])

        task.set_output(resp)
        return task
