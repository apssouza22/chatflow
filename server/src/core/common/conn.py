import redis.asyncio as redis

from core.common.config import REDIS_URL, REDIS_HOST, PGSQL_HOST, PGSQL_PASS, PGSQL_USER, PGSQL_DB, PGSQL_PORT
from core.common.pg import DBConnection

_redis_conn = None
_pg_conn = None


def get_redis_instance():
    """ Static access method. """
    global _redis_conn

    if _redis_conn is None:
        print("REDIS_URL", REDIS_HOST)
        _redis_conn = redis.from_url(REDIS_URL)
    return _redis_conn


def get_pg_instance():
    global _pg_conn

    if _pg_conn is None:
        _pg_conn = DBConnection(
            PGSQL_DB,
            PGSQL_USER,
            PGSQL_PASS,
            PGSQL_HOST,
            PGSQL_PORT
        )
    return _pg_conn
