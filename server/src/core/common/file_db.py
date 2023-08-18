import json
import os
import pickle

class FileDB:
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


if __name__ == "__main__":
    cache = FileDB('/Users/alexsouza/projects/my/opensource/chat-commander/file_db')
    cache.put('test.json', json.dumps({'test_key1': 'test', 'test_key2': 'test'}).encode('utf-8'))
    cache.put('test2.json', json.dumps([{'test_key1': 'test', 'test_key2': 'test'}]).encode('utf-8'))
    print(json.loads(cache.get('test')))
    print(cache.get('test2'))
    print(cache.get('test3'))
