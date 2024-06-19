import json
import os.path

import pandas as pd

from core.common.config import OPENAI_API_KEY
from core.llm.openapi_client import OpenAIClient

openai_client = OpenAIClient(OPENAI_API_KEY)


def read_data():
    data_file = os.path.join("./", "data/source_data.json")
    return pd.read_json(data_file)


def get_openai_embeddings(docs_batch: list[dict]):
    texts = []
    ids = []
    results = {}
    for doc in docs_batch:
        texts.append(doc["text"])
        ids.append(doc["item_id"])

    embeddings = openai_client.get_embeddings(texts)
    for index, doc in enumerate(docs_batch):
        results[ids[index]] = embeddings[index]

    return results


def generate_vectors(data):
    all_vectors = {}
    text_batch = []
    item_ids = []
    for index, row in data.iterrows():
        text_batch.append(row)
        if index % 100 == 0:
            text_vectors = get_openai_embeddings(text_batch)
            all_vectors.update(text_vectors)
            text_batch.clear()
            item_ids.clear()

    #         add any remaining rows to row_count
    if len(text_batch) > 0:
        text_vectors = get_openai_embeddings(text_batch)
        all_vectors.update(text_vectors)

    print(len(data), len(all_vectors))
    return all_vectors


def save_vectors_to_json(doc_data, vectors):
    data_vectors = []
    for index, row in doc_data.iterrows():
        data_vectors.append({
            "item_id": row["item_id"],
            "text_vector": vectors[row["item_id"]]
        })
    data_json = json.dumps(data_vectors, indent=4)
    with open("data/vectors.json", "w") as f:
        f.write(data_json)


def save_metadata_to_json(data):
    metadata_list = []
    for index, row in data.iterrows():
        metadata_list.append({
            "item_id": row["item_id"],
            "metadata": {
                "title": row["title"],
                "text": row["text"],
                "app": row["application"],
                "article_type": row["article_type"]
            }
        })

    metadata_json = json.dumps(metadata_list, indent=4)
    with open("data/metadata.json", "w") as f:
        f.write(metadata_json)


def prepare_data():
    data = read_data()
    vectors = generate_vectors(data)
    save_vectors_to_json(data, vectors)
    save_metadata_to_json(data)


if __name__ == "__main__":
    prepare_data()
