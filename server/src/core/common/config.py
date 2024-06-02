import os
from decouple import config

PROJECT_NAME = "chatux_app"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
INDEX_NAME = "chat_docs"
INDEX_TYPE = os.environ.get("VECSIM_INDEX_TYPE", "HNSW")

OPENAI_BACKOFF = os.environ.get("OPENAI_BACKOFF", 0.5)
OPENAI_MAX_RETRIES = os.environ.get("OPENAI_MAX_RETRIES", 3)

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_API_MODEL_GPT3 = config("OPENAI_API_MODEL_GPT3")
OPENAI_API_MODEL_GPT4 = config("OPENAI_API_MODEL_GPT4")

PGSQL_HOST = config("PGSQL_HOST")
PGSQL_PORT = config("PGSQL_PORT")
PGSQL_PASS = config("PGSQL_PASS")
PGSQL_USER = config("PGSQL_USER")
PGSQL_DB = config("PGSQL_DB")

REDIS_DB = os.environ.get("REDIS_DB", 0)
if REDIS_PASSWORD and REDIS_PASSWORD != "":
    print("REDIS_PASSWORD", REDIS_PASSWORD)
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

os.environ["REDIS_DATA_URL"] = REDIS_URL
os.environ["REDIS_OM_URL"] = REDIS_URL
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "data")
