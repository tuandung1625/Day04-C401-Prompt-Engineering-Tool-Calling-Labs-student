import requests
from typing import Any

def weather_reporter(location: str) -> dict[str, Any]:
    """
    Sử dụng công cụ này để tra cứu tình hình thời tiết hiện tại của một địa điểm hoặc thành phố cụ thể.

    Các trường hợp BẮT BUỘC phải dùng:
    - Người dùng hỏi về thời tiết hiện tại, nhiệt độ, hoặc dự báo tại một khu vực (ví dụ: Hà Nội, Hồ Chí Minh, Tokyo).

    Args:
        location (str): Tên thành phố hoặc địa danh cần tra cứu thời tiết (nên viết bằng tiếng Anh không dấu, ví dụ: 'Hanoi', 'London').

    Returns:
        dict: Chứa thông tin nhiệt độ, độ ẩm, trạng thái thời tiết hoặc thông báo lỗi.
    """
    try:
        # Sử dụng API thời tiết công khai wttr.in trả về định dạng JSON
        url = f"https://wttr.in/{location}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {"error": f"Không thể tìm thấy thông tin thời tiết cho địa điểm: {location}"}
            
        data = response.json()
        current = data['current_condition'][0]
        
        return {
            "tool": "weather_reporter",
            "location": location,
            "temperature_C": f"{current['temp_C']}°C",
            "humidity": f"{current['humidity']}%",
            "condition": current['lang_vnm'][0]['value'] if 'lang_vnm' in current else current['weatherDesc'][0]['value']
        }
    except Exception as e:
        return {"error": f"Lỗi kết nối hệ thống thời tiết: {str(e)}"}