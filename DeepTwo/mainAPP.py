
from APPConfig import AppConfig
from DeepTwo.Cache import SimpleCache
from DeepTwo.client import AIClient
from DeepTwo.service import NamingService


def main():
    # 一行代码加载所有的配置
    aicfg=AppConfig.load_from_yaml("config.yaml")
    cache=SimpleCache()
    print(f"当前使用的模型{aicfg.deepseek.model}")
    client = AIClient(aicfg)
    print(f"当前的system_prompt{aicfg}")
    naming_service=NamingService(client,cache)
    print(">>> 正在启动 AI 命名助手 (工程化版)...")
    desc = "判断用户是否已经登录"
    suggestion=naming_service.get_suggestions(desc,category='布尔变量名',systemPrompt=aicfg.naming.prompt)
    print("-" * 30)
    print(suggestion)
    print("-" * 30)

if __name__ == "__main__":
    main()