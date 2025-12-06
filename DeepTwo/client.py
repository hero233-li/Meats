import json
import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')
import os
# 2. 然后再请客人进门
import requests

from typing import List
from DeepTwo.APPConfig import AppConfig


class AIClient:
    """只负责与AI API 进行HTTP 通信 ，他只会发送消息"""
    def __init__(self,config:AppConfig):
        self.config=config
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.deepseek.api_key}"
        }
    def send_message(self,messages:list):
        # print(messages)
        payload = {
            "model":self.config.deepseek.model,
            "messages":messages,
            "stream":False,
            "max_tokens": 100  # <--- 核心修改：强制模型只准说 100 个 token 的话，说完立刻停
        }
        try:
            response = requests.post(
                url=self.config.deepseek.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.config.deepseek.timeout
            )
            # print(response.json())
            if response.status_code != 200:
                print(f"⚠️ API 请求异常！状态码: {response.status_code}")
                print(f"⚠️ 返回内容: {response.text}")  # 打印出来看看是不是报错信息
                response.raise_for_status()
            try:
                return response.json()['choices'][0]['message']['content'].strip()
            except Exception as json_err:
                print(f"⚠️ JSON 解析失败！原始返回内容如下:\n{response.text}")
                raise json_err
            print(response.json())
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API 链接失败{e}")
