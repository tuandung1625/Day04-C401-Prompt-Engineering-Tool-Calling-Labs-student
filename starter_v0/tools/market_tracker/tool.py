import requests
from typing import Any

def market_tracker(symbol: str) -> dict[str, Any]:
    """
    Sử dụng công cụ này để tra cứu dữ liệu giá cổ phiếu, tiền tệ hoặc tiền điện tử theo thời gian thực.
    
    Các trường hợp BẮT BUỘC phải dùng:
    - Người dùng hỏi về giá hiện tại của một mã chứng khoán (ví dụ: AAPL, TSLA).
    - Người dùng muốn tra cứu tỷ giá hoặc giá tiền điện tử (ví dụ: BTC-USD).

    Args:
        symbol (str): Mã chứng khoán hoặc mã tiền điện tử cần tra cứu.

    Returns:
        dict: Chứa thông tin giá hiện tại của mã được yêu cầu hoặc thông báo lỗi nếu mã không hợp lệ.
    """
    try:
        # Sử dụng public endpoint của Yahoo Finance (không cần API key cho các truy vấn cơ bản)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Trích xuất giá hiện tại và loại tiền tệ
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        currency = data['chart']['result'][0]['meta']['currency']
        
        return {
            "tool": "market_tracker",
            "symbol": symbol,
            "price": price,
            "currency": currency
        }
    except Exception as e:
        return {"error": f"Không thể lấy dữ liệu cho mã {symbol}. Hãy đảm bảo mã này hợp lệ. Lỗi: {str(e)}"}