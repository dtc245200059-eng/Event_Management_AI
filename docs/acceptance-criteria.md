# Acceptance Criteria Specification

> **Dự Án:** Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Đã xác minh và bao phủ bởi 36 test cases tự động)  
> **Tài Liệu Tham Chiếu:** [user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md), [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md), [traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md)  
> **Kỹ năng liên quan:** [requirements-analysis](file:///d:/Event_Management_AI/.agents/skills/requirements-analysis/SKILL.md), [testing](file:///d:/Event_Management_AI/.agents/skills/testing/SKILL.md)  
> **Kiểm thử liên quan:** [tests/test_event_flows.py](file:///d:/Event_Management_AI/tests/test_event_flows.py), [tests/test_auth_rbac.py](file:///d:/Event_Management_AI/tests/test_auth_rbac.py), [tests/test_ai_agent.py](file:///d:/Event_Management_AI/tests/test_ai_agent.py), [tests/test_multi_agent.py](file:///d:/Event_Management_AI/tests/test_multi_agent.py)  
> **Tiêu Chuẩn Định Dạng:** `Given - When - Then` (Gherkin syntax)

---

## 1. Tiêu Chí Chấp Nhận Nhóm Chức Năng Quản Lý Cốt Lõi

### AC-01: Xác thực & Băm Mật Khẩu (Liên kết: `US-ATT-01`, `FR-01`)
- **AC-01.1 (Happy Path - Đăng ký thành công)**:
  - **Given**: Người dùng ở trang `/auth/register` và nhập username, email chưa tồn tại, mật khẩu thỏa mãn độ dài >= 6 ký tự.
  - **When**: Nhấn nút "Đăng Ký".
  - **Then**: Hệ thống băm mật khẩu bằng thuật toán PBKDF2 với Salt, tạo bản ghi mới trong bảng `users` và `attendees`, chuyển hướng tới trang đăng nhập với thông báo thành công.
- **AC-01.2 (Negative Path - Đăng nhập sai mật khẩu)**:
  - **Given**: Người dùng nhập đúng username nhưng sai mật khẩu tại `/auth/login`.
  - **When**: Nhấn nút "Đăng Nhập".
  - **Then**: Hệ thống từ chối đăng nhập, hiển thị thông báo lỗi "Tên đăng nhập hoặc mật khẩu không chính xác", không tiết lộ cụ thể trường nào bị sai.

---

### AC-02: Đặt Vé & Kiểm Soát Hạn Ngạch Quota (Liên kết: `US-ATT-04`, `FR-04`, `FR-05`)

- **AC-02.1 (Happy Path - Đặt vé còn hạn ngạch)**:
  - **Given**: Người dùng đã đăng nhập, sự kiện có hạng vé "Standard" với `sold_count = 5` và `quota = 10`.
  - **When**: Người dùng chọn mua vé Standard và xác nhận đặt vé.
  - **Then**: Hệ thống thực hiện DB Transaction:
    1. Tăng `sold_count` từ 5 lên 6.
    2. Tạo bản ghi `Registration` với `ticket_number` duy nhất (ví dụ: `TCK-202610-A1B2C3D4`).
    3. Sinh mã SVG QR Code cho vé.
    4. Trả về thông báo "Đăng ký vé thành công!".
- **AC-02.2 (Boundary Path - Cháy vé / Sold Out)**:
  - **Given**: Hạng vé có `sold_count = 10` và `quota = 10`.
  - **When**: Một người dùng khác cố gắng gửi yêu cầu mua vé này.
  - **Then**: Hệ thống từ chối giao dịch, trạng thái vé hiển thị `sold_out`, không cho phép submit form, đảm bảo `sold_count` không bao giờ vượt quá `quota` (Zero Overselling).
- **AC-02.3 (Chống Trùng Đăng Ký - Unique Registration)**:
  - **Given**: Người dùng đã có vé hợp lệ của Sự kiện A.
  - **When**: Người dùng cố gắng đăng ký thêm một vé khác của cùng Sự kiện A.
  - **Then**: Hệ thống kiểm tra ràng buộc `(event_id, attendee_id)` và cảnh báo "Bạn đã đăng ký tham gia sự kiện này rồi!".

---

### AC-03: Soát Vé QR & Chống Quét Trùng (Liên kết: `US-STF-02`, `US-STF-03`, `FR-06`)

- **AC-03.1 (Happy Path - Soát vé lần đầu thành công)**:
  - **Given**: Nhân viên (Staff) đã đăng nhập và mở giao diện `/checkin/scanner`. Vé `TCK-NUM-999` có trạng thái `checked_in = False`.
  - **When**: Camera quét mã QR hoặc nhân viên nhập chuỗi `TCK-NUM-999` vào API `/checkin/verify-api`.
  - **Then**: 
    1. Hệ thống cập nhật `checked_in = True` và `checked_in_at = CURRENT_TIMESTAMP`.
    2. API trả về mã HTTP `200 OK` với JSON `{"success": true, "status": "valid", "message": "Check-in thành công!", "attendee_name": "..."}`.
    3. Giao diện hiển thị khung viền xanh lá kèm âm thanh xác nhận.
- **AC-03.2 (Security / Fraud Prevention - Chặn quét vé lặp lại)**:
  - **Given**: Vé `TCK-NUM-999` đã được check-in thành công vào lúc 08:30.
  - **When**: Người khác mang vé đó đến cổng lúc 08:45 và quét lại mã.
  - **Then**: 
    1. Hệ thống phát hiện `checked_in == True`.
    2. API trả về mã HTTP `409 Conflict` với JSON `{"success": false, "status": "duplicate", "message": "CẢNH BÁO: Vé này đã được check-in lúc 08:30!"}`.
    3. Giao diện hiển thị cảnh báo đỏ nổi bật, ngăn chặn hoàn toàn việc vào cổng trùng lặp.

---

### AC-04: Hủy Vé & Hoàn Quota (Liên kết: `US-ATT-06`, `FR-04`)

- **AC-04.1 (Happy Path - Hủy vé thành công)**:
  - **Given**: Người dùng có vé với trạng thái `payment_status = 'paid'` hoặc `'free'`, hạng vé hiện tại có `sold_count = 8`.
  - **When**: Người dùng chọn "Hủy vé" tại trang `/tickets/my-tickets`.
  - **Then**: 
    1. Bản ghi `Registration` cập nhật `payment_status = 'cancelled'`.
    2. `sold_count` của hạng vé tự động giảm từ 8 xuống 7.
    3. Hạng vé chuyển về trạng thái `available` nếu trước đó đang `sold_out`.

---

### AC-05: Truyền Thông & Gửi Thông Báo Theo Phân Khúc (Liên kết: `US-ORG-01`, `US-ATT-10`, `FR-07`)

- **AC-05.1 (Happy Path - Ban tổ chức gửi thông báo)**:
  - **Given**: Ban tổ chức đã đăng nhập và mở form `/notifications/send/<event_id>`. Sự kiện có 15 người đã đăng ký (`all`).
  - **When**: Nhập tiêu đề, nội dung và chọn phân khúc đối tượng `all`, sau đó nhấn "Gửi thông báo".
  - **Then**: Hệ thống tạo 15 bản ghi trong bảng `notifications` tương ứng với từng attendee, trả về mã thông báo flash thành công và cập nhật số lượng người nhận là 15.
- **AC-05.2 (Attendee Inbox - Khách xem thông báo)**:
  - **Given**: Khách tham dự đăng nhập vào tài khoản của mình.
  - **When**: Mở trang `/notifications/inbox`.
  - **Then**: Hệ thống hiển thị danh sách các thông báo riêng cho sự kiện đã đăng ký, đánh dấu trạng thái đã đọc/chưa đọc.

---

## 2. Tiêu Chí Chấp Nhận Nhóm Chức Năng Trí Tuệ Nhân Tạo (AI Modules)

### AC-AI-01: RAG Chatbot Assistant & Chống Hallucination (Liên kết: `US-ATT-08`, `FR-AI-01`)

- **AC-AI-01.1 (Happy Path - Trả lời chuẩn xác theo dữ liệu CSDL)**:
  - **Given**: Sự kiện "Vietnam AI Summit 2026" có trong CSDL với diễn giả "TS. Lê Quang Dũng" trình bày lúc 09:00 tại Phòng Hội trường A.
  - **When**: Người dùng hỏi qua widget: *"Ai là diễn giả và thời gian phiên khai mạc sự kiện Vietnam AI Summit?"*.
  - **Then**: Hệ thống truy xuất CSDL, tạo Context, gọi LLM và trả lời chính xác: Diễn giả là TS. Lê Quang Dũng, phiên khai mạc bắt đầu lúc 09:00 tại Phòng Hội trường A.
- **AC-AI-01.2 (Chống Bịa Đặt - Anti-Hallucination Guardrail)**:
  - **Given**: CSDL không có thông tin về phiên thảo luận "Blockchain 3.0" trong sự kiện.
  - **When**: Người dùng hỏi: *"Phiên Blockchain 3.0 diễn ra lúc mấy giờ?"*.
  - **Then**: Trợ lý AI trả lời rõ ràng rằng không tìm thấy thông tin này trong lịch trình chính thức của Ban tổ chức và hướng dẫn người dùng liên hệ bàn hỗ trợ, tuyệt đối không tự bịa ra giờ hoặc tên diễn giả.
- **AC-AI-01.3 (High Availability - Tự động Fallback Mock khi mất mạng/lỗi API)**:
  - **Given**: Kết nối mạng tới Google Gemini API bị ngắt hoặc `GEMINI_API_KEY` không hợp lệ.
  - **When**: Người dùng gửi bất kỳ câu hỏi nào về sự kiện.
  - **Then**: Hệ thống tự động kích hoạt **Offline Fallback Mock Engine**, trích xuất trực tiếp dữ liệu từ CSDL nội bộ để tạo câu trả lời mạch lạc, trả về `mode: "mock"` với độ trễ < 100ms, không làm gián đoạn trải nghiệm người dùng.

---

### AC-AI-02: AI Soạn Thảo Email & Thông Báo Tự Động (Liên kết: `US-ORG-02`, `FR-AI-02`)

- **AC-AI-02.1 (Tạo bản thảo thông báo không rò rỉ PII)**:
  - **Given**: Ban tổ chức cần gửi thông báo nhắc lịch cho sự kiện.
  - **When**: Gửi yêu cầu tới `/api/ai/draft-notification` với `event_id` và `type: "reminder"`.
  - **Then**: AI tạo bản thảo chuẩn ngữ cảnh (thời gian, địa điểm, chủ đề sự kiện) mà không chứa bất kỳ địa chỉ email, số điện thoại cá nhân nào của người tham dự trong prompt.

---

### AC-AI-03: AI Tóm Tắt Ý Kiến Phản Hồi Theo 4 Nhóm (Liên kết: `US-ORG-03`, `FR-AI-03`)

- **AC-AI-03.1 (Phân nhóm phản hồi và trích xuất Actionable Takeaways)**:
  - **Given**: Sự kiện đã kết thúc và có 20 ý kiến đánh giá khảo sát từ khách tham dự.
  - **When**: Ban tổ chức gọi API `/api/ai/summarize-feedback`.
  - **Then**: Hệ thống phân loại phản hồi thành 4 nhóm (Nội dung & Diễn giả, Check-in & Vận hành, Hội trường & Hậu cần, Lịch trình & Thời lượng) và đề xuất danh sách hành động cải tiến khả thi.

---

### AC-AI-04: Gợi Ý Sự Kiện Cá Nhân Hóa (Liên kết: `US-ATT-09`, `FR-AI-05`)

- **AC-AI-04.1 (Matching theo Sở Thích & Nội Dung)**:
  - **Given**: CSDL có Sự kiện 1 (Chủ đề: *Trí tuệ nhân tạo, GenAI, Machine Learning*) và Sự kiện 2 (Chủ đề: *Đầu tư Bất động sản*).
  - **When**: Người dùng tìm kiếm hoặc có sở thích *"Tôi muốn tìm hiểu về Trí tuệ nhân tạo và Python"*.
  - **Then**: Thuật toán TF-IDF & Cosine Similarity tính toán điểm tương đồng và xếp hạng Sự kiện 1 ở vị trí ưu tiên số 1 (Similarity score cao nhất).

---

### AC-AI-05: Dự Báo Tham Dự & Phân Tích Cảm Xúc (Liên kết: `US-ADM-06`, `FR-AI-06`)

- **AC-AI-05.1 (Dự Báo Số Người Tham Dự Thực Tế)**:
  - **Given**: Sự kiện có 100 vé đã đăng ký, tỷ lệ check-in lịch sử và thời gian diễn ra sự kiện.
  - **When**: Admin mở Dashboard phân tích của sự kiện.
  - **Then**: Hệ thống tính toán và hiển thị: `expected_attendance` (ước lượng người đến), `predicted_showup_rate` (tỷ lệ % dự báo) kèm gợi ý điều chỉnh hội trường.
- **AC-AI-05.2 (Phân Loại Cảm Xúc Phản Hồi)**:
  - **Given**: Người tham dự gửi phản hồi: *"Sự kiện rất tuyệt vời, diễn giả chia sẻ sâu sắc!"*.
  - **When**: Hệ thống tiếp nhận phản hồi.
  - **Then**: Phản hồi được gán nhãn cảm xúc `POSITIVE` và tổng hợp vào biểu đồ phân bổ tâm lý người tham gia trên Dashboard Admin.

---

### AC-AI-06: Multi-Agent Event Advisory Với Critic Guardrail & Retry Loop (Liên kết: `US-ATT-11`, `FR-AI-07`)

- **AC-AI-06.1 (Kiểm duyệt độc lập và chặn đứng Hallucination)**:
  - **Given**: Người dùng hỏi về sự kiện không tồn tại hoặc ngân sách không thỏa mãn.
  - **When**: Gửi yêu cầu qua `/ai/multi-agent/advisory` hoặc `/api/ai/multi-agent/advisory`.
  - **Then**: 7 Agent phối hợp xử lý, Critic Agent phát hiện sai lệch và từ chối cấp phép hoặc yêu cầu Retry; hệ thống trả về phản hồi trung thực đã kiểm chứng với `critic_verdict: {"status": "APPROVE" | "REJECT", "score": float}` và lưu toàn bộ vết vào `MessageBus`.
