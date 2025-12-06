import os
from dataclasses import dataclass
from dotenv import load_dotenv
import yaml
from pathlib import Path
# 1. 加载 .env
load_dotenv()

@dataclass
class DeepSeekConfig:
    """子配置 专门管理DeepSe 相关参数"""
    api_key: str
    api_url: str
    model:str
    timeout:int
@dataclass
class NamingConfig:
    """子配置 专门管理业务相关参数"""
    prompt: str
    count:str
@dataclass
class AppConfig:
    """主配置 聚合所有子配置"""
    deepseek: DeepSeekConfig
    naming:NamingConfig

    @classmethod
    def get_api_key_from_env(cls):
        """
                专门负责去找钥匙的方法
                """
        # 强制定位到当前文件所在的目录 (DeepTwo)
        current_dir = Path(__file__).parent
        env_path = current_dir / '.env'

        # 加载 .env
        load_dotenv(dotenv_path=env_path)

        # 获取 Key
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("❌ 未找到 API Key! 请检查 DeepTwo/.env 文件是否配置正确")
        return key

    @classmethod
    def load_from_yaml(cls,path:str="config.yaml"):
        """
        工程化核心：读取YAML-> 校验数据 -> 映射为对象
        :param path:
        :return:
        """
        print(f"Loading config from {path}")
        try:
            with open(path,"r",encoding="utf-8") as f:
                # 把yaml读取为字典(dictionary)
                raw_config = yaml.safe_load(f)
            # 提取数据并组装对象
            ai_data=raw_config.get("AIModel")
            ds_data=ai_data.get("deepseek",{})
            ns_data=ai_data.get("naming_service",{})
            real_key = cls.get_api_key_from_env()
            # 实例化子配置
            ds_config=DeepSeekConfig(
                api_key=real_key,
                api_url=ds_data.get("api_url"),
                model=ds_data.get("model","deepseek-chat"),
                timeout=ds_data.get("timeout",10),
            )
            ns_config=NamingConfig(
                prompt=ns_data.get("default_prompt",''),
                count=ns_data.get("max_suggestions",3),
            )
            return cls(deepseek=ds_config, naming=ns_config)
        except FileNotFoundError:
            raise RuntimeError(f"Config file {path} not found")
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")