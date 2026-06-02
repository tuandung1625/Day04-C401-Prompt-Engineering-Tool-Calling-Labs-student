# Day 04 Lab v2 Report — Research Agent

## Team

- Team: 4
- Members: Nguyễn Quang Minh- 2A202600816
           Nguyễn Tuấn Dũng - 2A202600848
- Provider/model:

## Final Metrics

- Final version:
- Final artifact_version:
- Best base run file:
- Base case accuracy:
- Base tool routing accuracy:
- Base argument accuracy:
- Group eval run file:
- Group eval accuracy:
- Chat transcript file:

## Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Phiên bản gốc, chưa sửa | NA | 0.7 | v0_B_base_openrouter_20260602T135703030056.json |
| v1 | System prompt  |  | 0.7 | 0.7 | v1_B_base_openrouter_20260602T221121325702.json |
| v2 | System prompt |  | 0.7 | 0.75 | v2_B_base_openrouter_20260602T222500126254.jsson |
| v3 | System prompt |  | 0.75 | 0.9 | v3_B_base_openrouter_20260602T222832157468.json |

## Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool | lookup(query="AI news", topic="news", timeframe="day", max_results=5) | query: expected 'AI', got 'AI news' | Cấm LLM tự ý thêm từ khóa phụ (như "news") vào query gốc. Cấm tự ý thêm tham số tuỳ chọn max_results nếu người dùng không yêu cầu. |

|R10_missing_handle| missing_info  |  timeline(screenname="sama")  | missing tool call clarify, extra tool call timeline | Ngăn chặn việc LLM tự suy đoán (hallucinate) thông tin. Bắt buộc gọi clarify khi thiếu tham số cốt lõi (như handle của người dùng).  |

| R13_parallel_web_and_tweets | wrong_tool | lookup(query="AI news", timeframe="day", max_results=5), social_search(query="AI", limit=5) |  query: expected 'AI', got 'AI news, topic: expected 'news', got None | Đảm bảo LLM không tự ý thêm chữ "news" vào query (tương tự R03) và trích xuất đầy đủ tham số topic="news" khi tìm kiếm tin tức trên web.| 
 
## Team Eval Cases

List at least 5 cases added to `data/eval_group.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_missing_url_clarif | Bẫy lỗi Hallucination (tự bịa link): Yêu cầu tóm tắt nhưng không đưa link bài viết. | Gọi tool clarify với response_type="text" | Passed |
| G02_confirm_publish_action | Bẫy ranh giới an toàn (Boundary): Yêu cầu đăng bài lên mạng xã hội (Twitter). | Gọi tool clarify với response_type="yes_no" để hỏi ý kiến xác nhận. | Passed |
| G03_extract_exact_timeframe | Bẫy trích xuất tham số & Thời gian: Tìm "tin tức" về xe điện VinFast "tuần này". | Gọi tool lookup(query="xe điện VinFast", topic="news", timeframe="week")| Passed |
| G04_multiturn_switch_tool | Bẫy Multi-turn (Đổi ý): Lượt 1 hỏi Twitter, Lượt 2 bảo bỏ Twitter chuyển sang Web.| CHỈ gọi lookup(query="Apple Vision Pro", topic="news", timeframe="day"). Tự động hủy tool social_search.| Passed |
| G05_out_of_scope_translation | Bẫy gọi tool thừa: Yêu cầu dịch một câu sang tiếng Anh (Task NLP cơ bản).| Không gọi tool nào cả (no_tool=true). Trả lời trực tiếp bản dịch.| Passed |
## Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  1 | "thời tiết hôm nay thế nào" | weather_reporter(location="Hanoi") | v0_openrouter_20260602T210901427138.transcript  | Success: Trả về thông tin thời tiết Hà Nội thành công (29°C, độ ẩm 78%, mưa rải rác). |
| 2 | "Tìm bài báo về stochastic process" | papers(query="stochastic process", max_results=5) | v0_openrouter_20260602T163451718249.transcript.jsson | ìm thấy và liệt kê thành công 5 bài báo khoa học liên quan từ arXiv. |
## Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |

## Reflection

- Which fixes belonged in `system_prompt.md`?
Lỗi Agent tự ý thêm từ khóa phụ (như chữ "news") vào biến query, lỗi tự ý giả định handle mặc định (như "sama") hoặc placeholder (your_twitter_handle), và lỗi quên tham số khi hội thoại đa lượt (limit, timeframe). Tất cả đều được giải quyết triệt để bằng cách thêm các luật nghiêm ngặt vào system_prompt.md
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
Ví dụ: Trường hợp của case R04 (Tóm tắt bài viết URL) hoặc câu hỏi meta R09 (Bạn làm được những gì?). Điểm kiểm thử tự động chỉ kiểm tra xem Agent có gọi đúng Tool hay không (no_tool: true). Tuy nhiên, nội dung văn bản mà Agent trả ra (actual_text) có hành văn mượt mà không, tóm tắt có đúng trọng tâm bài báo không, hay có bị lặp từ không... thì hệ thống tự động không thể chấm được. Đó là lúc cần Manual Review.
- What would you improve next?
Xử lý lỗi API (Error Handling): Như turn 7 và turn 8 trong file transcript cũ, khi hệ thống ArXiv bị lỗi hoặc trả về 0 kết quả, Agent nên biết cách chủ động báo lại cho người dùng một cách thông minh thay vì chỉ im lặng hoặc báo không tìm thấy.
Quản lý Context Window ngắn lại: Thiết lập cơ chế tự động dọn dẹp các lịch sử chat quá cũ (Buffer Memory) để Agent không bị loãng thông tin khi trò chuyện quá lâu (Multi-turn dài tập).
Bảo mật thông tin (Guardrails): Thêm các lớp kiểm duyệt để Agent từ chối các yêu cầu đào bới thông tin nhạy cảm của người dùng trên không gian mạng.
