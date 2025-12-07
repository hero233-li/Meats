import json
import warnings



warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')
import requests
import os
from img2txt.DoubaoConfig import  AIConfig


class DBAIClient:
    def __init__(self,config:AIConfig):
        self.config=config
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.doubao.api_key}"
        }
    def send_message(self, messages):
        payload = {
            "model":self.config.doubao.model,
            "messages":messages,
            "stream":False,
        }
        try:
            response = requests.post(
                url=self.config.doubao.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.config.doubao.timeout
            )
            # print(payload)
            if response.status_code != 200:
                print(f"⚠️ API 请求异常！状态码: {response.status_code}")
                print(f"⚠️ 返回内容: {response.text}")  # 打印出来看看是不是报错信息
                response.raise_for_status()
            try:
                return response.json()['choices'][0]['message']['content'].strip()
            except Exception as json_err:
                print(f"⚠️ JSON 解析失败！原始返回内容如下:\n{response.text}")
                raise json_err
        except requests.exceptions.RequestException as e:
            print(e)
