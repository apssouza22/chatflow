#!/usr/bin/env python3
import asyncio
import json
import typing as t

import numpy as np
import redis.asyncio as redis
from redis.asyncio import Redis
from redis.commands.search.field import (
    VectorField,
    TagField,
    TextField,
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

from core.common import config
from core.common.config import INDEX_NAME
from data.prepare_data import prepare_data

redis_conn = redis.from_url(config.REDIS_URL)


async def create_hnsw_index(
        redis_conn: Redis,
        number_of_vectors: int,
        prefix: str,
        distance_metric: str = 'COSINE'
):
    """
    Use this type of index for Approximate Nearest Neighbor search. Best for speed.
    :param redis_conn:
    :param number_of_vectors:
    :param prefix:
    :param distance_metric:
    :return:
    """
    openai_text_field = VectorField(
        "openai_text_vector",
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
        })

    application_field = TagField("application")

    # Create index
    await redis_conn.ft(INDEX_NAME).create_index(
        fields=[openai_text_field, application_field],
        definition=IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
    )


def read_items_metadata_json() -> t.List:
    with open(config.DATA_LOCATION + "/data_metadata.json") as f:
        data = json.load(f)
    return data


def read_data_vectors() -> t.List:
    with open(config.DATA_LOCATION + "/data_vectors.json") as f:
        data_vectors = json.load(f)
    return data_vectors


async def persist_data(data_vectors, metadata):
    """Persist data to redis as hash set."""

    for data_vector in data_vectors:
        item_id = data_vector["item_id"]
        key = "data_vector:" + str(item_id)
        item_metadata = metadata[item_id]["item_metadata"]
        mappings = {
            "item_id": item_id,
            "application": item_metadata["application"],
            "text_vector": np.array(data_vector["text_vector"], dtype=np.float32).tobytes(),
            "openai_text_vector": np.array(data_vector["openai_text_vector"], dtype=np.float32).tobytes(),
            "text_raw": item_metadata["text"],
            "title": item_metadata["title"],
        }
        await redis_conn.hset(key, mapping=mappings)


async def load_all_data():
    if await redis_conn.dbsize() > 5000:
        print("Data already loaded")
        return

    items_metadata = read_items_metadata_json()
    metadata_dic = {}
    for item in items_metadata:
        metadata_dic[item["item_id"]] = item
    print("Metadata loaded!")

    print("Loading data vectors")
    vectors = read_data_vectors()
    await persist_data(vectors, metadata_dic)
    print("Data vectors loaded!")

    prefix = "data_vector:"

    try:
        print("Dropping existing index")
        await redis_conn.ft(INDEX_NAME).dropindex()
    except Exception as e:
        print("Index does not exist")

    try:
        print("Creating vector search index")
        await create_hnsw_index(redis_conn, len(items_metadata), prefix=prefix, distance_metric="COSINE")
        print("Creating text search index")
        await create_text_search_index()
    except Exception as e:
        print("Index creation failed. Index already exists")
        # traceback.print_exc()

    print("Search index created")


async def create_text_search_index():
    """Create text search index for text search from metadata fields in hash set."""

    index = INDEX_NAME + "_text"
    search_prefix = ":txtSearch:"
    try:
        print("Dropping existing index")
        await redis_conn.ft(index).dropindex()
    except Exception as e:
        print("Index does not exist")

    application_field = TagField("$.item_metadata.application", as_name="application")
    text_field = TextField("$.item_metadata.text", as_name="text")
    title_field = TextField("$.item_metadata.title", as_name="title")

    await redis_conn.ft(index).create_index(
        fields=[text_field, title_field, application_field],
        definition=IndexDefinition(prefix=[search_prefix], index_type=IndexType.JSON)
    )


if __name__ == "__main__":
    print("Preparing data")
    prepare_data()

    print("Loading data into chat commander App")
    asyncio.run(load_all_data())

    asyncio.run(create_text_search_index())
    print("Data loaded!")
