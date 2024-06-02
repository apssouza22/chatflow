import redis.asyncio as redis

from core.common.config import REDIS_URL, REDIS_HOST

_redis_conn = None
_pg_conn = None


def get_redis_instance():
    """ Static access method. """
    global _redis_conn

    if _redis_conn is None:
        print("REDIS_URL", REDIS_HOST)
        _redis_conn = redis.from_url(REDIS_URL)
    return _redis_conn

