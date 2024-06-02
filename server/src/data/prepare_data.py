import json
import os

import numpy as np
import pandas as pd

from core.common.config import OPENAI_API_KEY_GPT3
# from sentence_transformers import SentenceTransformer  # for creating semantic (text-based) vector embeddings

from core.llm.openapi_client import OpenAIClient

source_file = os.path.join("./", "data/source_data.json")
data_source = pd.read_json(source_file)
openai = OpenAIClient(OPENAI_API_KEY_GPT3)


def _generate_text_vectors_local_model(data_df):
    """Generate text vectors using a local model."""
    # bert variant to create text embeddings
    # Both all-mpnet-base-v2 and all-distilroberta-v1 models are suitable for generating sentence embeddings and can be used for various NLP tasks such as semantic similarity, clustering, or classification. The choice between the two models depends on your specific requirements:
    # If you need a more efficient model with lower computational requirements, you might prefer the all-distilroberta-v1 model.
    # If you prioritize performance and accuracy over computational efficiency, you might choose the all-mpnet-base-v2 model.

    # model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    # model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

    text_vectors = {}
    for index, row in data_df.iterrows():
        if index % 1000 == 0:
            print(f"Creating text vectors. Page: {str(index)}")
        # text_vectors[row["item_id"]] = model.encode(row["text"]).astype(np.float32)

    return text_vectors


def _generate_openai_text_vectors(data_df):
    all_text_vectors = {}
    text_batch = []
    item_ids = []

    for index, row in data_df.iterrows():
        text_batch.append(row)
        if index % 1000 == 0:
            text_vectors = _get_openai_embeddings(text_batch)
            all_text_vectors.update(text_vectors)
            text_batch.clear()
            item_ids.clear()

    # Add any remaining rows to row_count
    if len(text_batch) > 0:
        text_vectors = _get_openai_embeddings(text_batch)
        all_text_vectors.update(text_vectors)

    print(len(data_df), len(all_text_vectors))

    return all_text_vectors


def _get_openai_embeddings(text_list: list[dict]):
    texts = []
    item_ids = []
    text_vectors = {}
    for index, row in enumerate(text_list):
        texts.append(row["text"])
        item_ids.append(row["item_id"])

    data = openai.create_embeddings(texts)
    for index, _ in enumerate(text_list):
        text_list[index]["text_embedding"] = data[index]
        text_vectors[item_ids[index]] = data[index]

    print(f"Processed {len(text_list)} item text fields")
    return text_vectors


def _combine_vector_dicts(items, openai_txt_vectors=None, local_txt_vectors=None):
    """Combine text vectors from local and openai models."""
    data_vectors = []
    for _, row in items.iterrows():
        try:
            _id = row["item_id"]
            openai_vector = openai_txt_vectors[_id]
            # text_vector = local_txt_vectors[_id].tolist()
            vector_dict = {
                # "text_vector": text_vector,
                "text_vector": [],
                "item_id": _id,
                "openai_text_vector": openai_vector,
            }
            data_vectors.append(vector_dict)
        except Exception as e:
            print(f"Combine vector error: {e}")
            continue
    return data_vectors


def _write_vectors_json(vector_dict):
    data_vector_json = json.dumps(vector_dict)
    with open("./data/data_vectors.json", "w") as f:
        f.write(data_vector_json)


def _create_metadata(data_df):
    data_metadata = []
    for index, row in data_df.iterrows():
        try:
            item = {
                "item_id": row["item_id"],
                "item_metadata": {
                    "title": row["title"],
                    "text": row["text"],
                    "article_type": row["article_type"],
                    "application": row["application"],
                }
            }
            data_metadata.append(item)
        except KeyError:
            continue
    data_vector_json = json.dumps(data_metadata)
    with open("./data/data_metadata.json", "w") as f:
        f.write(data_vector_json)


def prepare_data():
    """Prepare data to be imported into the database."""
    local_txt_vectors = _generate_text_vectors_local_model(data_source)
    openai_text_vectors = _generate_openai_text_vectors(data_source)
    vector_dict = _combine_vector_dicts(data_source, openai_text_vectors, local_txt_vectors)
    _write_vectors_json(vector_dict)
    _create_metadata(data_source)


if __name__ == "__main__":
    prepare_data()
