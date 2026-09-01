# Acceptance Criteria Specification
**Dự Án**: Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)  
**Tài Liệu Tham Chiếu**: `docs/user-stories.md`, `docs/requirements.md`  
**Tiêu Chuẩn Định Dạng**: `Given - When - Then` (Gherkin syntax)

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

### AC-AI-02: Gợi Ý Sự Kiện Cá Nhân Hóa (Liên kết: `US-ATT-09`, `FR-AI-03`)
- **AC-AI-02.1 (Matching theo Sở Thích & Nội Dung)**:
  - **Given**: CSDL có Sự kiện 1 (Chủ đề: *Trí tuệ nhân tạo, GenAI, Machine Learning*) và Sự kiện 2 (Chủ đề: *Đầu tư Bất động sản*).
  - **When**: Người dùng tìm kiếm hoặc có sở thích *"Tôi muốn tìm hiểu về Trí tuệ nhân tạo và Python"*.
  - **Then**: Thuật toán TF-IDF & Cosine Similarity tính toán điểm tương đồng và xếp hạng Sự kiện 1 ở vị trí ưu tiên số 1 (Similarity score cao nhất).

---

### AC-AI-03: Dự Báo Tham Dự & Phân Tích Cảm Xúc (Liên kết: `US-ADM-06`, `FR-AI-04`)
- **AC-AI-03.1 (Dự Báo Số Người Tham Dự Thực Tế)**:
  - **Given**: Sự kiện có 100 vé đã đăng ký, tỷ lệ check-in lịch sử và thời gian diễn ra sự kiện.
  - **When**: Admin mở Dashboard phân tích của sự kiện.
  - **Then**: Hệ thống tính toán và hiển thị: `expected_attendance` (ước lượng người đến), `predicted_showup_rate` (tỷ lệ % dự báo) kèm gợi ý điều chỉnh hội trường.
- **AC-AI-03.2 (Phân Loại Cảm Xúc Phản Hồi)**:
  - **Given**: Người tham dự gửi phản hồi: *"Sự kiện rất tuyệt vời, diễn giả chia sẻ sâu sắc!"*.
  - **When**: Hệ thống tiếp nhận phản hồi.
  - **Then**: Phản hồi được gán nhãn cảm xúc `POSITIVE` và tổng hợp vào biểu đồ phân bổ tâm lý người tham gia trên Dashboard Admin.
