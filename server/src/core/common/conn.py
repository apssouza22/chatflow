import redis.asyncio as redis
from os import environ

import sqlalchemy

from core.common.config import REDIS_URL, REDIS_HOST, PGSQL_HOST, PGSQL_PASS, PGSQL_USER, PGSQL_DB, PGSQL_PORT

_redis_conn = None
_pg_conn = None


def get_redis_instance():
    """ Static access method. """
    global _redis_conn

    if _redis_conn is None:
        print("REDIS_URL", REDIS_HOST)
        _redis_conn = redis.from_url(REDIS_URL)
    return _redis_conn


def get_pg_instance() -> sqlalchemy.engine.base.Engine:
    global _pg_conn

    if _pg_conn is None:
        PGSQL_USER = environ.get('PGSQL_USER', "chatux")
        PGSQL_PASS = environ.get('PGSQL_PASS', "postgres")
        PGSQL_HOST = environ.get('PGSQL_HOST', "localhost")
        PGSQL_PORT = environ.get('PGSQL_PORT', "5432")
        PGSQL_DB = environ.get('PGSQL_DB', "postgres")
        _pg_conn = sqlalchemy.create_engine(f"postgresql+psycopg2://{PGSQL_USER}:{PGSQL_PASS}@{PGSQL_HOST}:{PGSQL_PORT}/{PGSQL_DB}")
            
    return _pg_conn
