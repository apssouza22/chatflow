from collections import OrderedDict


class CacheMemory:
    """Cache memory class to store the recently read items. LRU algorithm is used to delete the least recent read item."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        else:
            # Move the recently read item to the end of the OrderedDict.
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # Move the updated item to the end of the OrderedDict.
            self.cache.move_to_end(key)
        self.cache[key] = value
        # Check the cache memory capacity to delete the least recent read item.
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
