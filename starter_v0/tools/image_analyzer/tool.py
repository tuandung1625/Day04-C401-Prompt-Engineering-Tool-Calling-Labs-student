import os
import requests
from typing import Any

def image_analyzer(image_url: str, query: str = "Mô tả chi tiết nội dung bức ảnh này.") -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "Thiếu OPENROUTER_API_KEY trong file .env để chạy công cụ Vision."}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Sử dụng model hỗ trợ xử lý ảnh (vision)
    payload = {
        "model": "openai/gpt-4o-mini", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        return {
            "tool": "image_analyzer",
            "image_url": image_url,
            "analysis_result": data["choices"][0]["message"]["content"]
        }
    except Exception as e:
        return {"error": f"Lỗi khi phân tích ảnh: {str(e)}"}