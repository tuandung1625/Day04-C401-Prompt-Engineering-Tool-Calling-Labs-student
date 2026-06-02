import os
import requests
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def text_summarizer(text: str, max_sentences: int = 5) -> dict[str, Any]:
    """
    Sử dụng công cụ này để tóm tắt các đoạn văn bản dài, bài báo hoặc tài liệu nghiên cứu thành một bản tóm tắt ngắn gọn.

    Các trường hợp BẮT BUỘC phải dùng:
    - Người dùng cung cấp một đoạn văn bản dài và yêu cầu tóm tắt, rút gọn hoặc lấy ý chính.
    - Cần cô đọng nội dung sau khi đọc dữ liệu thô.

    Args:
        text (str): Nội dung văn bản thô cần tóm tắt.
        max_sentences (int): Số lượng câu tối đa mong muốn trong bản tóm tắt (mặc định là 5).

    Returns:
        dict: Chứa văn bản đã được tóm tắt hoặc thông báo lỗi.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "Thiếu OPENROUTER_API_KEY trong file .env"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Hãy tóm tắt đoạn văn bản sau đây một cách súc tích trong tối đa {max_sentences} câu:\n\n{text}"

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=20)
        if response.status_code != 200:
            return {"error": f"Lỗi API: {response.text}"}
        
        data = response.json()
        return {
            "tool": "text_summarizer",
            "summary": data["choices"][0]["message"]["content"]
        }
    except Exception as e:
        return {"error": f"Lỗi hệ thống: {str(e)}"}