# Comprehensive User Manual & Operations Guide

> **Hệ Thống:** Quản Lý Sự Kiện Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
> **Phiên Bản:** 3.1 (Đã Đồng Bộ & Xác Minh Với 66 Endpoints và 27 Templates)  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Đầy đủ 12 luồng nghiệp vụ trên 4 vai trò người dùng)  
> **Tài Liệu Tham Chiếu:** [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md), [api.md](file:///d:/Event_Management_AI/docs/api.md), [chatbot-architecture.md](file:///d:/Event_Management_AI/docs/chatbot-architecture.md), [multi-agent-architecture.md](file:///d:/Event_Management_AI/docs/multi-agent-architecture.md)  
> **Kỹ năng liên quan:** [frontend-development](file:///d:/Event_Management_AI/.agents/skills/frontend-development/SKILL.md), [responsive-mobile](file:///d:/Event_Management_AI/.agents/skills/responsive-mobile/SKILL.md)  
> **Đối Tượng Sử Dụng:** Quản Trị Viên (Admin), Ban Tổ Chức (Organizer), Nhân Viên Soát Vé (Staff), Khách Tham Dự (Attendee)

---

## 1. Cẩm Nang Dành Cho Khách Tham Dự (Attendee Guide)

### 1.1. Đăng Ký Tài Khoản (`[IMPLEMENTED]`)
1. Truy cập trang chủ `http://127.0.0.1:5000` và nhấn **"Đăng Ký"** (`/auth/register`).
2. Nhập các trường: Họ và tên, Email, Tên đăng nhập (username) và Mật khẩu (tối thiểu 6 ký tự).
3. Nhấn **"Đăng Ký"**. Mật khẩu được băm an toàn qua PBKDF2-SHA256, hệ thống tự động tạo bản ghi `users` và hồ sơ `attendees`, sau đó chuyển hướng đến trang Đăng nhập.

### 1.2. Đăng Nhập & Quản Lý Phiên (`[IMPLEMENTED]`)
1. Truy cập `/auth/login`, nhập Username và Mật khẩu.
2. Hệ thống kiểm tra thông tin, khởi tạo Session cookie an toàn (`HttpOnly`).
3. Nếu nhập sai, hệ thống hiển thị thông báo lỗi bảo mật chung mà không tiết lộ tài khoản có tồn tại hay không.

### 1.3. Khám Phá & Lọc Sự Kiện (`[IMPLEMENTED]`)
1. Tại trang chủ hoặc `/events/`, sử dụng thanh tìm kiếm theo từ khóa.
2. Lọc theo danh mục: *Công nghệ, Kinh doanh, Giáo dục, Nghệ thuật, Thể thao*.
3. Lọc theo hình thức: *Trực tiếp (Offline), Trực tuyến (Online), Kết hợp (Hybrid)*.

### 1.4. Xem Chi Tiết Sự Kiện (`[IMPLEMENTED]`)
1. Nhấp vào thẻ sự kiện tại `/events/<id>`.
2. Giao diện hiển thị banner, ngày giờ, địa điểm tổ chức, đề cương chi tiết từng phiên họp (Schedules/Timeline), thông tin học vị diễn giả (Speakers) và bảng giá các hạng vé.

### 1.5. Đăng Ký Vé & Kiểm Soát Hạn Ngạch (`[IMPLEMENTED]`)
1. Tại phần **"Hạng Vé & Đăng Ký"**, chọn hạng vé mong muốn: *Free, Standard, VIP*.
2. Nhấn nút **"Đăng Ký Vé"** (`/tickets/book/<ticket_id>`).
3. Hệ thống kiểm tra:
   - Nếu vé còn hạn ngạch (`sold_count < quota`), hệ thống tự động tăng `sold_count`, tạo bản ghi `Registration` với mã vé định danh duy nhất (`TCK-...`), sinh mã QR Vector SVG và trả về thông báo thành công.
   - Nếu vé vừa hết (`sold_count >= quota`), hệ thống từ chối giao dịch và chuyển trạng thái vé sang `sold_out`.
   - Nếu bạn đã đăng ký sự kiện này trước đó, hệ thống chặn đăng ký lặp lại (Anti-hoarding).

### 1.6. Quản Lý Vé & Hủy Vé Hoàn Quota (`[IMPLEMENTED]`)
1. Mở trang **"Vé Của Tôi"** (`/tickets/my-tickets`).
2. Mỗi vé hiển thị mã định danh, trạng thái thanh toán và mã QR sắc nét.
3. Nếu không thể tham dự, nhấn **"Hủy Đăng Ký"** (`/tickets/cancel/<id>`). Hệ thống hoàn trả số lượng vé bán ra (`sold_count -= 1`) và mở lại trạng thái `available` cho cộng đồng.

### 1.7. Hộp Thư Đến Nhận Thông Báo (`[IMPLEMENTED]`)
1. Truy cập **"Hộp Thư"** (`/notifications/inbox`).
2. Xem các thông báo gửi từ Ban tổ chức (Thư mời, Nhắc lịch trước giờ G, Cập nhật địa điểm khẩn cấp).

### 1.8. Đánh Giá Khảo Sát Sau Sự Kiện (`[IMPLEMENTED]`)
1. Với sự kiện đã tham dự, gửi điểm đánh giá từ 1 đến 5 sao và nhận xét chi tiết.
2. Hệ thống ghi nhận ý kiến và đưa qua phân tích cảm xúc (Sentiment Analysis).

---

## 2. Luồng Sử Dụng Trợ Lý Ảo AI (AI Assistant Flow)

### 2.1. Trợ Lý RAG Chatbot Tra Cứu Sự Kiện (`[IMPLEMENTED]`)
Quy trình trao đổi câu hỏi:
```
Người Dùng Nhập Câu Hỏi
       │
       ▼
Giao Diện Web Chatbot Widget (`chat.js`)
       │
       ▼ (POST /api/ai/chat)
Backend API Gateway (`app/routes/ai.py`)
       │
       ▼
AI Service Layer (`app/services/rag_service.py`)
       │
       ├─► 1. Phân Tích Ý Định & Slots (Intent: schedule/speaker/ticket/venue)
       ├─► 2. Truy Xuất CSDL Quan Hệ & FAQ (events, schedules, tickets, faqs)
       ├─► 3. Xây Dựng Grounded Context (Sanitized Context không PII)
       │
       ▼
Gọi Google Gemini API (gemini-2.0-flash)
       │
       ├─► Nếu Thành Công: Trả lời tự nhiên dựa trên Context CSDL
       └─► Nếu Mất Mạng/Lỗi API: Tự động kích hoạt Offline Fallback Mock Engine
       │
       ▼
Response Handler định dạng Markdown
       │
       ▼
Hiển Thị Phản Hồi Trực Quan Lên Khung Chat
```

### 2.2. Trợ Lý Multi-Agent Tư Vấn Đa Tiêu Chí (`/ai/workspace`) (`[IMPLEMENTED]`)
1. Truy cập **"AI Advisory Workspace"** tại `/ai/workspace`.
2. Nhập yêu cầu phức tạp (Ví dụ: *"Tìm sự kiện công nghệ tại TP.HCM có giá dưới 500k và có diễn giả về AI"*).
3. Hệ thống kích hoạt **7 Agent chuyên trách**:
   - `OrchestratorAgent`: Khởi tạo phiên làm việc và ghi vết `MessageBus`.
   - `RequirementAgent`: Bóc tách JSON tiêu chí lọc.
   - `RetrievalAgent`: Chạy SQL Tool tham số hóa.
   - `KnowledgeAgent`: Tìm kiếm ngữ nghĩa Vector Search trong FAQ và chính sách.
   - `RecommendationAgent`: Suy luận so sánh trade-offs và lập bản nháp.
   - `CriticAgent`: Kiểm duyệt chéo CSDL; từ chối hoặc kích hoạt Retry Loop nếu phát hiện sai lệch.
   - `ResponseAgent`: Xuất Markdown kèm Critic Badge minh bạch.
4. Người dùng có thể nhấn **"Xem Tiến Trình 7 Agent"** để thấy rõ từng message trao đổi và căn cứ ra quyết định.

---

## 3. Cẩm Nang Dành Cho Ban Tổ Chức (Organizer Guide)

### 3.1. Quản Lý Sự Kiện & Lịch Trình (`[IMPLEMENTED]`)
1. Đăng nhập tài khoản Organizer (`organizer` / `Organizer@123`).
2. Vào **"Quản Trị Sự Kiện"** (`/events/manage`) để thêm mới hoặc chỉnh sửa sự kiện, lịch trình và danh sách diễn giả.

### 3.2. Soạn Thảo Thông Báo Tự Động Với AI (`[IMPLEMENTED]`)
1. Mở trang tạo thông báo `/notifications/send/<event_id>`.
2. Chọn loại thông báo: *Thư mời (Invitation), Nhắc lịch (Reminder), Cảm ơn (Thank You), Cập nhật (Update)*.
3. Nhấn **"Sinh Bản Thảo Bằng AI"** (`/api/ai/draft-notification`). Hệ thống tự động tạo nội dung chuyên nghiệp dựa trên dữ liệu sự kiện mà không gửi bất kỳ thông tin cá nhân (PII) nào của khách cho AI.
4. Chọn phân khúc người nhận: *Tất cả người đăng ký (`all`), Đã check-in (`checked_in`), Chưa check-in (`not_checked_in`), Khách VIP (`vip`)*.
5. Nhấn **"Gửi Thông Báo"**.

### 3.3. Tóm Tắt Ý Kiến Phản Hồi Với AI (`[IMPLEMENTED]`)
1. Sau khi sự kiện diễn ra, mở trang phân tích sự kiện.
2. Nhấn nút **"AI Tóm Tắt Phản Hồi"** (`/api/ai/summarize-feedback`).
3. Hệ thống tự động phân loại ý kiến người tham gia thành 4 nhóm:
   - *Nội dung & Diễn giả*
   - *Check-in & Vận hành*
   - *Hội trường & Hậu cần*
   - *Lịch trình & Thời lượng*
4. Đồng thời trích xuất danh sách **Hành Động Cải Tiến (Actionable Takeaways)** để nâng cao chất lượng sự kiện tiếp theo.

---

## 4. Cẩm Nang Dành Cho Nhân Viên Soát Vé (Staff Guide)

### 4.1. Đăng Nhập & Mở Trình Quét Soát Vé (`[IMPLEMENTED]`)
1. Đăng nhập với tài khoản Staff (`staff` / `Staff@123`).
2. Nhấp vào mục **"Soát Vé (Scanner)"** trên menu hoặc truy cập `/checkin/scanner`.

### 4.2. Vận Hành Soát Vé Tại Cổng (`[IMPLEMENTED]`)
1. Cấp quyền Camera trên trình duyệt Web (hỗ trợ cả camera trước/sau trên điện thoại di động).
2. Hướng camera vào mã QR vé của người tham dự.
3. **Ý Nghĩa Các Trạng Thái Phản Hồi**:
   - **Màn hình Xanh Lá (200 OK)**: Vé hợp lệ. Check-in thành công. Hệ thống cập nhật thời gian check-in.
   - **Màn hình Đỏ (409 Conflict)**: CẢNH BÁO QUÉT TRÙNG. Vé này đã được check-in trước đó. Giữ vé lại để kiểm tra đối soát.
   - **Màn hình Vàng/Đỏ (404 Not Found)**: Mã vé không tồn tại hoặc sai sự kiện.
4. Nếu mã QR bị mờ hoặc điện thoại của khách hết pin, nhân viên có thể tra cứu mã vé thủ công trong danh sách `/checkin/event/<id>/attendees` để bấm Check-in nhanh.

---

## 5. Cẩm Nang Dành Cho Quản Trị Viên Hệ Thống (Admin Guide)

### 5.1. Quản Trị Người Dùng & Phân Quyền RBAC (`[IMPLEMENTED]`)
1. Đăng nhập với tài khoản Admin (`admin` / `Admin@123`).
2. Truy cập `/admin/users` để xem danh sách toàn bộ tài khoản.
3. Thay đổi vai trò người dùng (`attendee`, `organizer`, `staff`, `admin`) hoặc khóa tài khoản vi phạm.

### 5.2. Giám Sát Dashboard & AI Predictive Analytics (`[IMPLEMENTED]`)
1. Mở trang tổng quan `/admin/dashboard`.
2. Theo dõi thời gian thực:
   - Tổng doanh thu bán vé và tỷ lệ lấp đầy hội trường.
   - Tỷ lệ check-in thực tế (% show-up rate).
   - Dự báo tham dự bằng mô hình học máy.
   - Biểu đồ phân bổ cảm xúc (Positive, Neutral, Negative) từ các đánh giá khảo sát.
3. Truy cập `/ai/benchmark` để xem kết quả đánh giá thực nghiệm 10 ca kiểm thử định lượng so sánh kiến trúc Single-Agent vs Multi-Agent.
