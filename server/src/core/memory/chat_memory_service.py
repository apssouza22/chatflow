from core.cache.memory_cahce import MemoryCache


class ChatMemoryService:

    def __init__(self, short_memory: MemoryCache, long_memory: MemoryCache):
        self.long_memory = long_memory
        self.short_memory = short_memory

    def get_short_memory(self, key) -> list[dict]:
        memory = self.short_memory.get(key)
        return memory if memory else []

    def get_long_memory(self, key) -> list[str]:
        memory = self.long_memory.get(key)
        return memory if memory else []

    def update_short_memory(self, key, value):
        if self.short_memory.get(key) is None:
            self.short_memory.put(key, [value])
            return
        self.short_memory.get(key).append(value)

    def update_long_memory(self, key, value):
        if self.long_memory.get(key) is None:
            self.long_memory.put(key, [value])
            return
        self.long_memory.get(key).append(value)


def factory_chat_memory():
    return ChatMemoryService(MemoryCache(10), MemoryCache(30))
