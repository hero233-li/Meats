import base64
import os

from img2txt.client import DBAIClient


class ImageToDoubaoService:
    """只负责发送，需要传递一个client。把信息带入到里面去"""
    def __init__(self,client:DBAIClient):
        self.client = client
    def _encode_image(self,image_path:str):
        """把图片文件读取并转为 Base64 字符串"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片未找到: {image_path}")
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def send_image_to_doubao(self,user_prmpt,system_prompt):
        # 对图片进行编码
        base64_image=self._encode_image(user_prmpt)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": system_prompt
                    },
                ],
            }
        ]
        try:
            print(">>> 正在上传图片并思考中，视觉模型较慢请耐心等待...")
            result = self.client.send_message(messages)
            return result
        except ConnectionError as e:
            return f"识图失败{e}"