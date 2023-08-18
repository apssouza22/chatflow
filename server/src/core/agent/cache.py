from core.common.encode import encode_to_base64, decode_from_base64
from core.common.cache import CacheMemory


class PredictCache:
    def __init__(self):
        self.cache = CacheMemory(30)

    def put(self, key, value: str):
        k = encode_to_base64(key)
        v = encode_to_base64(value)
        self.cache.put(k, v)

    def get(self, key):
        k = encode_to_base64(key)
        data = self.cache.get(k)
        if data is not None:
            return decode_from_base64(data)

    def exists(self, k) -> bool:
        return self.get(k) is not None
