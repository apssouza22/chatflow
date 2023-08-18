import json
import os

import numpy as np
import pandas as pd

from core.common.config import OPENAI_API_KEY_GPT3
# from sentence_transformers import SentenceTransformer  # for creating semantic (text-based) vector embeddings

from core.llm.openapi_client import OpenAI

source_file = os.path.join("./", "data/source_data.json")
data_source = pd.read_json(source_file)
openai = OpenAI(OPENAI_API_KEY_GPT3)

# bert variant to create text embeddings
# Both all-mpnet-base-v2 and all-distilroberta-v1 models are suitable for generating sentence embeddings and can be used for various NLP tasks such as semantic similarity, clustering, or classification. The choice between the two models depends on your specific requirements:

# If you need a more efficient model with lower computational requirements, you might prefer the all-distilroberta-v1 model.
# If you prioritize performance and accuracy over computational efficiency, you might choose the all-mpnet-base-v2 model.

# model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


# model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

def generate_text_vectors(data_df):
    text_vectors = {}
    for index, row in data_df.iterrows():
        if index % 1000 == 0:
            print(f"Creating text vectors. Page: {str(index)}")
        # text_vectors[row["item_id"]] = model.encode(row["text"]).astype(np.float32)

    return text_vectors


def generate_openai_text_vectors(data_df):
    text_vectors = {}
    inputs = []
    item_ids = []
    row_count = 0
    for index, row in data_df.iterrows():
        inputs.append(row["text"])
        item_ids.append(row["item_id"])
        if index % 1000 == 0:
            row_count = _get_embeddings(inputs, item_ids, row_count, text_vectors)
            inputs.clear()
            item_ids.clear()

    # Add any remaining rows to row_count
    if len(inputs) > 0:
        row_count = _get_embeddings(inputs, item_ids, row_count, text_vectors)

    print(row_count, len(data_df), len(text_vectors))

    return text_vectors


def _get_embeddings(inputs, item_ids, row_count, text_vectors):
    row_count += len(inputs)
    data = openai.create_openai_embeddings(inputs)
    for index, input in enumerate(inputs):
        text_vectors[item_ids[index]] = data[index]
    print(f"Processed {len(inputs)} item text fields")
    return row_count


# combine into a single json file
def combine_vector_dicts(items,  openai_txt_vectors=None):
    data_vectors = []
    for _, row in items.iterrows():
        try:
            _id = row["item_id"]
            openai_vector = openai_txt_vectors[_id]
            # text_vector = txt_vectors[_id].tolist()
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


def write_vectors_json(vector_dict):
    data_vector_json = json.dumps(vector_dict)
    with open("./data/data_vectors.json", "w") as f:
        f.write(data_vector_json)


def create_metadata(data_df):
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
    # text_vectors = generate_text_vectors(data_source)
    openai_text_vectors = generate_openai_text_vectors(data_source)
    vector_dict = combine_vector_dicts(data_source, openai_text_vectors)
    create_metadata(data_source)
    write_vectors_json(vector_dict)


if __name__ == "__main__":
    prepare_data()
