import time

from ai_name_generator.fetch_names_via_deepseek import format_time
from img2txt.DoubaoConfig import AIConfig
from img2txt.client import DBAIClient
from img2txt.doubao_service import ImageToDoubaoService


def doubao_ocr_pipeline():
    config=AIConfig.load_doubao_config("doubao.yaml")
    desc = "发送图片给豆包，让豆包转文字"
    user_prmpt = "ark_demo_img_1.png"# 放图片路径
    print(f"当前使用的模型:{config.doubao.model}")
    print(">>> 正在启动 智能识图助手[豆包识图] (工程化版)...")
    client = DBAIClient(config)
    service = ImageToDoubaoService(client)
    startTime = time.time()
    result= service.send_image_to_doubao(user_prmpt=user_prmpt,system_prompt=config.igt.prompt)
    endTime = time.time()
    elapsed = endTime - startTime
    print("-" * 30)
    print(f"本次执行耗时: {format_time(elapsed)}")
    print(result)
    print("-" * 30)

if __name__=="__main__":
    doubao_ocr_pipeline()