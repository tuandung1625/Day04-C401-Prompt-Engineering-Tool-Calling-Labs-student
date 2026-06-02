# Tool: text_summarizer

**Tác giả:** [Tên nhóm của bạn]
**Phiên bản:** 1.0

## Chức năng
Công cụ `text_summarizer` cấp khả năng cô đọng tài liệu chuyên sâu cho Agent. Nó giúp Agent xử lý dữ liệu văn bản dung lượng lớn, chia nhỏ đoạn văn để trích xuất các ý chính cốt lõi một cách súc tích mà không gây quá tải hoặc tràn cửa sổ ngữ cảnh (Context Window) của Mô hình Ngôn ngữ Lớn (LLM).

## Trường hợp sử dụng (Routing Hints)
Agent bắt buộc phải gọi công cụ này khi:
- Người dùng cung cấp trực tiếp một đoạn văn bản thô dài (bài viết, email, tài liệu nghiên cứu) và yêu cầu rút gọn, tóm tắt hoặc lấy ý chính.
- Cần rút gọn kết quả thô thu được sau khi thực hiện đọc dữ liệu từ các công cụ khác.

## Tham số đầu vào (Schema Arguments)
- `text` (string, bắt buộc): Toàn bộ nội dung văn bản thô cần xử lý.
- `max_sentences` (integer, tùy chọn): Số lượng câu tối đa mong muốn trong bản tóm tắt kết quả (mặc định là 5).

## Yêu cầu môi trường
- Cần cấu hình chính xác `OPENROUTER_API_KEY` trong tệp `.env`.