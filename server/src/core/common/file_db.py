import json
import os
import pickle

class FileDB:
    """Implementation of a file based key-value store."""

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get(self, key):
        try:
            with open(os.path.join(self.cache_dir, key), 'rb') as f:
                return pickle.load(f, encoding='utf-8')
        except Exception:
            return None

    def put(self, key, value):
        with open(os.path.join(self.cache_dir, key), 'wb') as f:
            pickle.dump(value, f)
