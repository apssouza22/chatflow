# from core.common.encode import encode_to_base64, decode_from_base64
from core.common import conn


# TODO: Why were there used base64 encodings?
#       Experiments show that it receives binary strings as arguments and works fine.
class PredictCache:
    def __init__(self, redis):
        self.redis = redis

    async def put(self, key, value: str):
        # k = encode_to_base64(key)
        await self.redis.hset("predict_cache:" + key, "value", value)

    async def get(self, key):
        # k = encode_to_base64(key)
        return await self.redis.hget("predict_cache:" + key, "value")

    async def exists(self, key) -> bool:
        # k = encode_to_base64(key)
        return await self.redis.exists("predict_cache:" + key)