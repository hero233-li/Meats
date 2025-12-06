import json
import hashlib
import os


class SimpleCache:
    """
    缓存层：用一个 JSON 文件存结果。
    """

    def __init__(self, filename=".naming_cache.json"):
        self.filename = filename
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        self._save_cache()

