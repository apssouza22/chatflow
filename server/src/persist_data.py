import json

import redis
from redis.commands.search.field import (
    VectorField,
    TagField,
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

from core.common import config
from core.common.config import INDEX_NAME
from prepare_data import prepare_data

redis_conn = redis.from_url(config.REDIS_URL)


def persist_data(vectors, metadata):
    for vector in vectors:
        key = "chatflow_doc:" + str(vector["item_id"])
        item_metadata = metadata[vector["item_id"]]["metadata"]
        mapping = {
            "item_id": vector["item_id"],
            "title": item_metadata["title"],
            "text": item_metadata["text"],
            "app": item_metadata["app"],
        }
        redis_conn.hset(key, mapping=mapping)


def read_vector_data():
    with open("data/vectors.json", "r") as f:
        return json.load(f)


def read_metadata_data():
    with open("data/metadata.json", "r") as f:
        data = json.load(f)
        return {item["item_id"]: item for item in data}


def create_index():
    try:
        print("Dropping existing index")
        redis_conn.ft(INDEX_NAME).dropindex()
    except Exception as e:
        print("Index does not exist")

    vector_field = VectorField(
        "text_vector",
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": "COSINE",
            "INITIAL_CAP": 100,
        }
    )
    app_field = TagField("app")
    redis_conn.ft(INDEX_NAME).create_index(
        fields=[vector_field, app_field],
        definition=IndexDefinition(
            prefix=["chatflow_doc"],
            index_type=IndexType.HASH,
        )
    )


def load_data():
    if redis_conn.dbsize() > 5000:
        print("Data already loaded")
        return None

    vector_data = read_vector_data()
    metadata_data = read_metadata_data()
    persist_data(vector_data, metadata_data)
    create_index()


if __name__ == "__main__":
    prepare_data()
    load_data()
