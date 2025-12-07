import hashlib

from ai_name_generator.Cache import SimpleCache
from ai_name_generator.client import AIClient


class NamingService:
    """业务逻辑层 专注于代码命名这个具体逻辑的业务场景"""
    def __init__(self,client:AIClient,cache: SimpleCache):
        self.client=client
        self.cache = cache
    def get_suggestions(self, description:str, category:str, system_prompt:str)->str:
        """核心业务"""
        # 1. 生成缓存 Key (比如用 MD5)
        raw_key = f"{category}:{description}"
        cache_key = hashlib.md5(raw_key.encode()).hexdigest()
        # 2. 查缓存：如果有，直接返回！耗时 0.001s
        cached_result = self.cache.get(cache_key)
        if cached_result:
            print("[来自本地缓存 ⚡️]")
            return cached_result
        system_prompt=system_prompt
        user_prmpt=f"类型{category}\n 描述{description}"
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prmpt}
        ]
        try:
            result = self.client.send_message(messages)
            self.cache.set(cache_key, result)
            return result
        except ConnectionError as e:
            return f"获取建议失败{e}"
