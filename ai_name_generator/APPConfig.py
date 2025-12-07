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
        # 强制定位到当前文件所在的目录 (ai_name_generator)
        current_dir = Path(__file__).parent
        env_path = current_dir / '.env'

        # 加载 .env
        load_dotenv(dotenv_path=env_path)

        # 获取 Key
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("❌ 未找到 API Key! 请检查 ai_name_generator/.env 文件是否配置正确")
        return key

    @classmethod
    def load_from_yaml(cls,path:str="config.yaml"):
        """
        工程化核心：读取YAML-> 校验数据 -> 映射为对象
        :param path:
        :return:
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, "config.yaml")
        print(f"Loading config from {full_path}")
        try:
            with open(full_path,"r",encoding="utf-8") as f:
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
            count = int(ns_data.get("max_suggestions", 3))
            default_prompt=f"你是一个资深 Python 程序员和命名专家。请根据用户提供的【中文描述】和【命名类型】，提供 {count}个专业的英文命名建议。要求：1. 风格遵循 Python PEP8 规范（如果类型是类名则用驼峰，变量/方法用下划线）。2. 格式严格如下，不要有任何 Markdown 标记，不要有开场白或结束语：name - (中文解释)3. 解释要简短，突出为什么这么命名（如：通俗、准确、动宾结构）。示例输出：calculate_total - (计算总和) 直白清晰，通用。sum_all_items - (求和所有项) 强调是对所有项操作。"
            ns_config=NamingConfig(
                prompt=default_prompt,
            )
            return cls(deepseek=ds_config, naming=ns_config)
        except FileNotFoundError:
            raise RuntimeError(f"Config file {path} not found")
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")