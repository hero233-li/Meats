from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import yaml


@dataclass
class NBS_MEMU_CONFIG:
    name:str
    dbcode:str
    key: str = ""

    def to_frontend_json(self) -> Dict:
        """
        核心方法：对象自己决定怎么展示给前端。
        这样 Class 依然紧紧管理着数据，没有断开关联。
        """
        return {
            # 优先用配置里的 short_id，如果没有配置，就回退用 key (monthly)
            "name": self.name,
            "hasChild": True  # 固定逻辑也可以封装在这里
        }
@dataclass
class PRO_CONFIG:
    nbs_config:Dict[str, NBS_MEMU_CONFIG]
    @classmethod
    def get_config_url(cls,config_file:str):
        # 判断内容，如果为空，则直接抛出异常
        config_markers=''
        if config_file== '':
            print(f"传入config_file为空，当前值为{config_file}")
            return ''
        # 找到当前目录，我会根据.gitignore 找到根目录，然后从根目录开始遍历，找到对应的文件
        currentPath = Path(__file__)
        markers = [
            '.git',  # Git 仓库
            'pyproject.toml',  # Python 项目配置
            'setup.py',  # Python 包设置
            'requirements.txt',  # Python 依赖
            '.project',  # 通用项目文件
            'README.md',  # 项目说明文件
            'LICENSE',  # 许可证文件
            'Makefile'  # 构建文件
        ]
        for path in [currentPath] + list(currentPath.parents):
            for marker in markers:
                # print(path/marker)
                if(path/marker).exists():
                    root_path= path
                    print(root_path)
                    break
        #如果当前传过来字符串，就转为数组，否则直接返回
        if isinstance(config_file, str):config_markers=[config_file]
        # 开始遍历目录，找到当前的文件
        for marker in config_markers:
            found_files=list(root_path.rglob(marker))
            if found_files:
                return found_files[0]
                # print(found_files[0])
            else:
                print(f"在项目目录 {root_path} 中未找到文件: {marker}")
        return None

    @classmethod
    def get_menu_config(cls,config_file:str):
       config_path= cls.get_config_url(config_file=config_file)
       try:
           with open(config_path,'r') as f:
               raw_config=yaml.safe_load(f)
               nbs_config=raw_config.get("NBS_MEMU",{})
               parsed_mbs={}
               for key,item in nbs_config.items():
                   parsed_mbs[key]=NBS_MEMU_CONFIG(
                    key=key,
                    name=item.get("name",""),
                    dbcode=item.get("dbcode",""),
                   )
               print(parsed_mbs)
               return cls(nbs_config=parsed_mbs)


       except FileNotFoundError:
            raise RuntimeError(f"Config file {config_path} not found")
       except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

