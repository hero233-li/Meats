# from APPConfig import AppConfig
import time

from ai_name_generator.APPConfig import AppConfig
from ai_name_generator.Cache import SimpleCache
from ai_name_generator.client import AIClient
from ai_name_generator.service import NamingService

def format_time(seconds):
    """根据时间大小自动格式化显示"""
    if seconds < 0.001:  # 小于1毫秒
        return f"{seconds*1000000:.2f} 微秒"
    elif seconds < 1:  # 小于1秒
        return f"{seconds*1000:.2f} 毫秒"
    else:  # 大于等于1秒
        return f"{seconds:.4f} 秒"

def fetch_names_via_deepseek(desc:str,category:str):
    # 一行代码加载所有的配置
    app_config=AppConfig.load_from_yaml("config.yaml")
    cache=SimpleCache()
    print(f"当前使用的模型{app_config.deepseek.model}")
    client = AIClient(app_config)
    naming_service=NamingService(client,cache)
    print(">>> 正在启动 AI 命名助手 (工程化版)...")
    # desc = "变量=AppConfig.load_from_yaml(‘config.yaml’)"
    # category='变量名'
    startTime = time.time()
    suggestion = naming_service.get_suggestions(desc, category, system_prompt=app_config.naming.prompt)
    endTime = time.time()
    elapsed = endTime - startTime
    print("-" * 30)
    print(f"本次执行耗时: {format_time(elapsed)}")
    print(suggestion)
    print("-" * 30)

if __name__ == "__main__":
    main()