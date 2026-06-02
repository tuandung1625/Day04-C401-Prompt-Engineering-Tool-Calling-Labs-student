import os
import requests
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def image_analyzer(image_url: str, query: str = "Mô tả chi tiết nội dung bức ảnh này.") -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "Thiếu OPENROUTER_API_KEY trong file .env"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://vinai.edu.vn", # OpenRouter khuyến khích có Header này
        "X-Title": "Research Agent Lab"
    }

    # Cấu trúc payload chuẩn cho Vision trên OpenRouter
    payload = {
        "model": "openai/gpt-4o-mini", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        
        # Nếu vẫn lỗi, in ra response.text để debug
        if response.status_code != 200:
            return {"error": f"Lỗi từ OpenRouter: {response.text}"}
            
        data = response.json()
        return {
            "tool": "image_analyzer",
            "analysis_result": data["choices"][0]["message"]["content"]
        }
    except Exception as e:
        return {"error": f"Lỗi hệ thống: {str(e)}"}