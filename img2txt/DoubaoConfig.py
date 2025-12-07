import os
from dataclasses import dataclass

import yaml
from dotenv import load_dotenv
from pathlib import Path

@dataclass
class DoubaoConfig:
    model:str
    api_url:str
    api_key:str
    timeout:int
@dataclass
class ImageToTextProcessor:
    prompt:str
@dataclass
class AIConfig:
    doubao:DoubaoConfig
    igt:ImageToTextProcessor
    @classmethod
    def find_root_path(cls,markers):
        start_path=Path(__file__)
        if isinstance(markers,str):markers=[markers]
        # print(markers)
        file_path=''
        for parent in [start_path] + list(start_path.parents):
            for marker in markers:
                if(parent/marker).exists():
                    file_path= parent/marker
                    break
        if file_path=='':
            raise ValueError(f"❌ 未找到 {markers}! 请检查 {markers} 文件是否存在")
        return file_path


    @classmethod
    def get_api_key(cls):
        load_dotenv()
        # 1、找到当前执行方法文件的为基准，找到.env文件所在的地方
        current_path = Path(__file__).parent.parent
        env_path= current_path / ".env"
        # 找到文件之后，使用load_dotenv方法加载文件，会把文件中的内容，加载到环境变量中去
        load_dotenv(dotenv_path=env_path)
        # 读取文件
        key = os.getenv("DOUBAO_API_KEY")
        if not key:
            raise ValueError(f"❌ 未找到 API Key! 请检查 {env_path} 文件是否配置正确")
        return key
    @classmethod
    def load_doubao_config(cls,path:str='doubao.yaml'):
        # 继续找到doubao.yaml文件
        config_path=cls.find_root_path(path)
        try:
            with open(config_path,"r") as f:
                raw_config=yaml.safe_load(f)
            # print(raw_config)
            ai_api=raw_config.get("AI_API")
            doubao_api=ai_api.get("doubao",{})
            real_key=cls.get_api_key()
            db_config=DoubaoConfig(
                api_key=real_key,
                api_url=doubao_api.get("api_url"),
                model=doubao_api.get("model","deepseek-chat"),
                timeout=doubao_api.get("timeout",10),
            )
            count = int(3)
            default_prompt=f"请将图片里的文字转写出来，不要包含任何解释性语句。"
            ig_config=ImageToTextProcessor(
                prompt=default_prompt,
            )
            return cls(
                doubao=db_config,
                igt=ig_config,
            )
        except FileNotFoundError:
            raise RuntimeError(f"Config file {path} not found")
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

