from ai_name_generator.fetch_names_via_deepseek import fetch_names_via_deepseek
from img2txt.doubao_ocr_pipeline import doubao_ocr_pipeline

if __name__ == "__main__":
    desc = "发送图片给豆包，让豆包转文字"
    category = 'service层 方法名'
    fetch_names_via_deepseek(desc,category)
# if __name__ == "__main__":
#     doubao_ocr_pipeline()