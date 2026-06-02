# Tool: weather_reporter

## Chức năng
Công cụ `weather_reporter` cung cấp khả năng thu thập dữ liệu động thời gian thực (real-time data acquisition) cho Agent về tình hình khí tượng. Công cụ này kết nối với dịch vụ thời tiết công khai để truy xuất các thông số nhiệt độ, độ ẩm và trạng thái thời tiết tại một địa điểm bất kỳ.

## Trường hợp sử dụng (Routing Hints)
Agent bắt buộc phải gọi công cụ này khi:
- Người dùng hỏi về tình hình thời tiết hiện tại, nhiệt độ, độ ẩm hoặc dự báo khí tượng tại một khu vực hoặc thành phố cụ thể (ví dụ: Hà Nội, Hồ Chí Minh, Tokyo, London).

## Tham số đầu vào (Schema Arguments)
- `location` (string, bắt buộc): Tên thành phố hoặc địa danh cần tra cứu (khuyến khích định dạng tiếng Anh hoặc tiếng Việt không dấu để tối ưu hóa kết quả tìm kiếm của API, ví dụ: 'Hanoi', 'Danang').

## Yêu cầu môi trường
- Không yêu cầu API Key bên thứ ba (sử dụng API dịch vụ công khai qua HTTP request).
- Thiết bị chạy Agent cần có kết nối mạng ổn định để thực hiện truy vấn thời gian thực.