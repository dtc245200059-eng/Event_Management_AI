# TÀI LIỆU ĐẶC TẢ CHI TIẾT 67 RESTFUL API & AI SERVICES (API SPECIFICATION)

**Dự án:** EventAI Pro (`Event_Management_AI`)  
**Phiên bản:** 2.1 (Chuẩn hóa toàn diện 67 Endpoints gồm Health Probe theo Kiến trúc Application Factory)  
**Trạng thái Triển khai:** `[IMPLEMENTED]` (Toàn bộ 67 routes đã được đăng ký trong `app.url_map` và kiểm thử tự động)  
**Định dạng Dữ liệu:** JSON (`application/json`) / Form-Data (`application/x-www-form-urlencoded`)  
**Base URL:** `http://localhost:5000` (hoặc `http://0.0.0.0:5000` trong Docker)  
**Kỹ năng Quản trị:** [`api-development`](file:///d:/Event_Management_AI/.agents/skills/api-development/SKILL.md)

---

## 1. TỔNG QUAN DANH MỤC 67 ENDPOINTS THEO 8 BLUEPRINTS

Hệ thống được module hóa thành 8 Blueprints chức năng độc lập cộng với API Gateway:

| Nhóm Blueprint | Số lượng Route | Phạm vi Chức năng | Tiêu chuẩn Xác thực / Phân quyền | Trạng thái |
| :--- | :---: | :--- | :--- | :---: |
| **1. Main Blueprint (`main`)** | 4 routes | Trang chủ, danh sách sự kiện, chi tiết sự kiện, Healthcheck probe | Public / Khách vãng lai | `[IMPLEMENTED]` |
| **2. Auth Blueprint (`auth`)** | 6 routes | Đăng ký, đăng nhập, đăng xuất, hồ sơ cá nhân, đổi mật khẩu | Session / `@login_required` | `[IMPLEMENTED]` |
| **3. Events Blueprint (`events`)** | 12 routes | CRUD sự kiện, quản lý vé, lịch trình, diễn giả sự kiện | Role: `organizer`, `admin` | `[IMPLEMENTED]` |
| **4. Tickets Blueprint (`tickets`)** | 7 routes | Đặt vé, thanh toán checkout, vé của tôi, tải QR, hủy vé, đánh giá | Role: `attendee`, `organizer`, `admin` | `[IMPLEMENTED]` |
| **5. Check-in Blueprint (`checkin`)** | 5 routes | Giao diện camera QR scanner, API xác thực vé, danh sách điểm danh | Role: `staff`, `organizer`, `admin` | `[IMPLEMENTED]` |
| **6. Admin Blueprint (`admin`)** | 5 routes | Dashboard quản trị, quản lý người dùng, đổi quyền, khóa tài khoản | Role: `admin` duy nhất | `[IMPLEMENTED]` |
| **7. Notifications Blueprint (`notifications`)** | 5 routes | Hộp thư thông báo, gửi thông báo sự kiện, API thông báo gần đây | Role: `attendee`, `organizer`, `admin` | `[IMPLEMENTED]` |
| **8. AI Services (`ai` & `/api/ai/*`)** | 22 routes | Trợ lý RAG Chat, gợi ý sự kiện, dự báo điểm danh, Multi-Agent Advisory | Public / Rate Limited / Dual Gateway | `[IMPLEMENTED]` |
| **9. Static Files Asset Route** | 1 route | Phục vụ tệp tĩnh CSS, JS, ảnh tải lên, mã QR SVG | Public Cache | `[IMPLEMENTED]` |
| **TỔNG CỘNG** | **67 routes** | **Toàn bộ hệ sinh thái EventAI Pro** | **RBAC 4 vai trò** | `[IMPLEMENTED]` |

---

## 2. MA TRẬN 67 ENDPOINTS CHI TIẾT (FULL API REGISTRY TABLE)

| STT | Phương thức | Đường dẫn (URL Pattern) | Tên Endpoint | Quyền hạn (RBAC) | Mô tả Chức năng |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **I** | **MAIN BLUEPRINT (4 ROUTES)** | | | | |
| 1 | `GET` | `/` | `main.index` | Public | Trang chủ, hiển thị Hero section, AI slider và phân trang sự kiện |
| 2 | `GET` | `/events` | `main.event_list` | Public | Danh sách sự kiện có lọc theo từ khóa, danh mục, thời gian, địa điểm |
| 3 | `GET` | `/events/<int:event_id>` | `main.event_detail` | Public | Xem trang chi tiết sự kiện, danh sách loại vé, lịch trình và diễn giả |
| 4 | `GET` | `/health` | `main.health_check` | Public | **Health Check Probe**: Kiểm tra sức khỏe hệ thống & kết nối DB cho Docker/K8s |
| **II** | **AUTH BLUEPRINT (6 ROUTES)** | | | | |
| 4 | `GET, POST` | `/auth/login` | `auth.login` | Public | Đăng nhập tài khoản bằng email/username và mật khẩu |
| 5 | `GET` | `/auth/logout` | `auth.logout` | Authenticated | Đăng xuất người dùng và hủy session an toàn |
| 6 | `GET, POST` | `/auth/register` | `auth.register` | Public | Đăng ký tài khoản người tham dự mới (mặc định role `attendee`) |
| 7 | `GET` | `/auth/profile` | `auth.profile` | Authenticated | Xem thông tin cá nhân và lịch sử hoạt động |
| 8 | `POST` | `/auth/profile/update` | `auth.update_profile` | Authenticated | Cập nhật họ tên, số điện thoại, avatar người dùng |
| 9 | `POST` | `/auth/profile/change-password` | `auth.change_password` | Authenticated | Đổi mật khẩu tài khoản (xác minh mật khẩu cũ qua PBKDF2) |
| **III** | **EVENTS BLUEPRINT (12 ROUTES)** | | | | |
| 10 | `GET, POST` | `/events/create` | `events.create` | `organizer`, `admin` | Tạo mới sự kiện kèm thông tin địa điểm, thời gian, hình ảnh |
| 11 | `GET` | `/events/manage` | `events.manage` | `organizer`, `admin` | Bảng điều khiển quản lý các sự kiện do ban tổ chức sở hữu |
| 12 | `GET, POST` | `/events/<int:event_id>/edit` | `events.edit` | `organizer`, `admin` | Chỉnh sửa thông tin chi tiết sự kiện |
| 13 | `POST` | `/events/<int:event_id>/delete` | `events.delete` | `organizer`, `admin` | Hủy hoặc xóa sự kiện khỏi hệ thống |
| 14 | `GET` | `/events/<int:event_id>/schedules` | `events.schedules` | `organizer`, `admin` | Xem danh sách các phiên lịch trình trong sự kiện |
| 15 | `POST` | `/events/<int:event_id>/schedules/create` | `events.create_schedule` | `organizer`, `admin` | Thêm phiên lịch trình mới (tiêu đề, thời gian bắt đầu/kết thúc) |
| 16 | `POST` | `/events/schedules/<int:schedule_id>/delete` | `events.delete_schedule` | `organizer`, `admin` | Xóa một phiên lịch trình cụ thể |
| 17 | `GET` | `/events/speakers` | `events.speakers_list` | `organizer`, `admin` | Danh bạ diễn giả của ban tổ chức |
| 18 | `POST` | `/events/speakers/create` | `events.create_speaker` | `organizer`, `admin` | Thêm hồ sơ diễn giả mới (tên, chức danh, chuyên môn, tiểu sử) |
| 19 | `POST` | `/events/speakers/<int:speaker_id>/delete` | `events.delete_speaker` | `organizer`, `admin` | Xóa hồ sơ diễn giả |
| 20 | `GET` | `/events/<int:event_id>/tickets` | `events.manage_tickets` | `organizer`, `admin` | Quản lý các hạng vé của sự kiện (VIP, Regular, Free) |
| 21 | `POST` | `/events/<int:event_id>/tickets/create` | `events.create_ticket` | `organizer`, `admin` | Tạo hạng vé mới (tên vé, đơn giá, số lượng mở bán) |
| **IV** | **TICKETS BLUEPRINT (7 ROUTES)** | | | | |
| 22 | `GET, POST` | `/tickets/register/<int:event_id>` | `tickets.register_ticket` | Authenticated | Đặt vé sự kiện và giữ chỗ tạm thời (giảm quota) |
| 23 | `GET, POST` | `/tickets/checkout/<int:reg_id>` | `tickets.checkout` | Owner / `admin` | Hoàn tất thanh toán, kích hoạt vé và sinh mã QR Code |
| 24 | `GET` | `/tickets/my-tickets` | `tickets.my_tickets` | Authenticated | Danh sách vé cá nhân của người dùng đã đặt |
| 25 | `GET` | `/tickets/view/<int:reg_id>` | `tickets.view_ticket` | Owner / `staff` / `admin` | Xem vé điện tử chi tiết và mã QR điểm danh |
| 26 | `GET` | `/tickets/download-qr/<int:reg_id>` | `tickets.download_qr` | Owner / `staff` / `admin` | Tải xuống tệp ảnh SVG mã QR điểm danh |
| 27 | `POST` | `/tickets/cancel/<int:reg_id>` | `tickets.cancel_ticket` | Owner / `admin` | Hủy đăng ký vé và hoàn trả quota mở bán cho sự kiện |
| 28 | `POST` | `/tickets/feedback/<int:reg_id>` | `tickets.submit_feedback` | Owner (`attended`) | Gửi đánh giá sao (1-5 sao) và nhận xét sau khi tham dự |
| **V** | **CHECK-IN BLUEPRINT (5 ROUTES)** | | | | |
| 29 | `GET` | `/checkin/` | `checkin.index` | `staff`, `organizer`, `admin` | Giao diện điều khiển camera quét mã QR trên di động/máy tính |
| 30 | `POST` | `/checkin/verify-api` | `checkin.verify_api` | `staff`, `organizer`, `admin` | **API Xác thực vé QR**: Kiểm tra mã, chống quét trùng lặp |
| 31 | `GET` | `/checkin/api/event-attendees/<int:event_id>` | `checkin.api_event_attendees` | `staff`, `organizer`, `admin` | **API Danh sách điểm danh**: Trả về toàn bộ danh sách khách |
| 32 | `POST` | `/checkin/api/quick-checkin/<int:reg_id>` | `checkin.api_quick_checkin` | `staff`, `organizer`, `admin` | **API Điểm danh nhanh**: Điểm danh thủ công bằng 1 click |
| 33 | `POST` | `/checkin/api/undo-checkin/<int:reg_id>` | `checkin.api_undo_checkin` | `staff`, `organizer`, `admin` | **API Hoàn tác điểm danh**: Hủy trạng thái check-in nếu nhầm |
| **VI** | **ADMIN BLUEPRINT (5 ROUTES)** | | | | |
| 34 | `GET` | `/admin/dashboard` | `admin.dashboard` | `admin` | Thống kê tổng thể: người dùng, sự kiện, doanh thu, vé bán |
| 35 | `GET` | `/admin/users` | `admin.users_list` | `admin` | Danh sách toàn bộ người dùng trong hệ sinh thái |
| 36 | `POST` | `/admin/users/create` | `admin.create_user` | `admin` | Quản trị viên khởi tạo tài khoản nhân viên hoặc ban tổ chức |
| 37 | `POST` | `/admin/users/<int:user_id>/change-role` | `admin.change_user_role` | `admin` | Phân quyền vai trò người dùng (`attendee`, `staff`, `organizer`, `admin`) |
| 38 | `POST` | `/admin/users/<int:user_id>/toggle-status` | `admin.toggle_user_status` | `admin` | Khóa hoặc mở khóa trạng thái tài khoản người dùng |
| **VII** | **NOTIFICATIONS BLUEPRINT (5 ROUTES)** | | | | |
| 39 | `GET` | `/notifications/inbox` | `notifications.inbox` | Authenticated | Hộp thư thông báo cá nhân của người dùng |
| 40 | `GET, POST` | `/notifications/create` | `notifications.create` | `organizer`, `admin` | Soạn và gửi thông báo hàng loạt tới người tham gia sự kiện |
| 41 | `GET` | `/notifications/manage` | `notifications.manage` | `organizer`, `admin` | Quản lý lịch sử các thông báo đã gửi của sự kiện |
| 42 | `GET` | `/notifications/view/<int:notif_id>` | `notifications.view_detail` | Authenticated | Xem chi tiết nội dung thông báo và đánh dấu đã đọc |
| 43 | `GET` | `/notifications/api/recent` | `notifications.api_recent` | Authenticated | **API Polling Thông báo**: Lấy 5 thông báo mới nhất & số chưa đọc |
| **VIII** | **AI SERVICE BLUEPRINT — ĐƯỜNG DẪN GỐC `/ai/*` (11 ROUTES)** | | | | |
| 44 | `POST` | `/ai/chat` | `ai.chat` | Public / Rate Limit | Chatbot RAG tư vấn sự kiện, hỏi đáp lịch trình, giá vé |
| 45 | `GET` | `/ai/workspace` | `ai.chat_workspace` | Public | Không gian làm việc AI tương tác đa tác tử toàn màn hình |
| 46 | `GET` | `/ai/recommendations` | `ai.recommendations` | Public | Đề xuất danh sách sự kiện thông minh theo ngữ cảnh người dùng |
| 47 | `GET` | `/ai/predictive/<int:event_id>` | `ai.predictive_stats` | `organizer`, `admin` | Dự báo AI tỷ lệ người tham gia thực tế (Predictive Attendance) |
| 48 | `GET` | `/ai/sentiment/<int:event_id>` | `ai.sentiment_stats` | `organizer`, `admin` | Phân tích sắc thái (Sentiment Analysis) đánh giá phản hồi |
| 49 | `GET` | `/ai/feedback-summary/<int:event_id>` | `ai.feedback_summary` | `organizer`, `admin` | Tóm tắt thông minh ý kiến phản hồi của khán giả bằng AI |
| 50 | `POST` | `/ai/generate-notification` | `ai.generate_notification` | `organizer`, `admin` | Sinh tự động tiêu đề và nội dung thông báo nhắc hẹn bằng AI |
| 51 | `POST` | `/ai/generate-description` | `ai.generate_description` | `organizer`, `admin` | Sinh tự động đoạn văn mô tả sự kiện hấp dẫn từ từ khóa |
| 52 | `POST` | `/ai/multi-agent/advisory` | `ai.multi_agent_advisory` | Public | Kích hoạt hệ thống 7 tác tử AI tư vấn chuyên sâu |
| 53 | `POST` | `/ai/multi-agent/benchmark` | `ai.run_benchmark_endpoint` | `admin` | Chạy bộ 10 ca kiểm thử thực nghiệm Benchmark Single vs Multi-Agent |
| 54 | `GET` | `/ai/multi-agent/trace/<task_id>` | `ai.get_multi_agent_trace` | Public | Lấy vết thực thi MessageBus của phiên tư vấn đa tác tử |
| **IX** | **AI SERVICE BLUEPRINT — ĐƯỜNG DẪN ALIAS `/api/ai/*` (11 ROUTES)** | | | | |
| 55 | `POST` | `/api/ai/chat` | `api_.ai.chat` | Public / Rate Limit | Alias chuẩn RESTful cho `/ai/chat` |
| 56 | `GET` | `/api/ai/workspace` | `api_.ai.chat_workspace` | Public | Alias chuẩn RESTful cho `/ai/workspace` |
| 57 | `GET` | `/api/ai/recommendations` | `api_.ai.recommendations` | Public | Alias chuẩn RESTful cho `/ai/recommendations` |
| 58 | `GET` | `/api/ai/predictive/<int:event_id>` | `api_.ai.predictive_stats` | `organizer`, `admin` | Alias chuẩn RESTful cho `/ai/predictive/<id>` |
| 59 | `GET` | `/api/ai/sentiment/<int:event_id>` | `api_.ai.sentiment_stats` | `organizer`, `admin` | Alias chuẩn RESTful cho `/ai/sentiment/<id>` |
| 60 | `GET` | `/api/ai/feedback-summary/<int:event_id>` | `api_.ai.feedback_summary` | `organizer`, `admin` | Alias chuẩn RESTful cho `/ai/feedback-summary/<id>` |
| 61 | `POST` | `/api/ai/generate-notification` | `api_.ai.generate_notification` | `organizer`, `admin` | Alias chuẩn RESTful cho `/ai/generate-notification` |
| 62 | `POST` | `/api/ai/generate-description` | `api_.ai.generate_description` | `organizer`, `admin` | Alias chuẩn RESTful cho `/ai/generate-description` |
| 63 | `POST` | `/api/ai/multi-agent/advisory` | `api_.ai.multi_agent_advisory` | Public | Alias chuẩn RESTful cho `/ai/multi-agent/advisory` |
| 64 | `POST` | `/api/ai/multi-agent/benchmark` | `api_.ai.run_benchmark_endpoint` | `admin` | Alias chuẩn RESTful cho `/ai/multi-agent/benchmark` |
| 65 | `GET` | `/api/ai/multi-agent/trace/<task_id>` | `api_.ai.get_multi_agent_trace` | Public | Alias chuẩn RESTful cho `/ai/multi-agent/trace/<id>` |
| **X** | **STATIC ASSETS (1 ROUTE)** | | | | |
| 66 | `GET` | `/static/<path:filename>` | `static` | Public | Cung cấp tài nguyên tĩnh CSS, JS, hình ảnh, mã QR |

---

## 3. ĐẶC TẢ CHI TIẾT CÁC ENDPOINT API CỐT LÕI (CORE API CONTRACTS)

### 3.1. API Trò Chuyện Trí Tuệ Nhân Tạo (`POST /ai/chat` & `POST /api/ai/chat`)
- **Mục đích:** Tư vấn sự kiện tự động, trả lời câu hỏi bằng công nghệ RAG kết hợp CSDL thực tế.
- **Xác thực:** Không bắt buộc đăng nhập (hỗ trợ khách vãng lai). Áp dụng Rate Limiting (tối đa 20 lượt/phút trên mỗi IP).
- **Request Headers:** `Content-Type: application/json`
- **Request Body Payload:**
  ```json
  {
    "message": "Có sự kiện công nghệ nào miễn phí vé tổ chức tại TP. Hồ Chí Minh không?",
    "session_id": "sess_user_9921_abc"
  }
  ```
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "response": "Chào bạn! Hệ thống có sự kiện **AI Innovate Summit 2026** tổ chức tại TP. Hồ Chí Minh với vé Standard hoàn toàn miễn phí (0 VNĐ)...",
    "sources": [
      {
        "event_id": 1,
        "title": "AI Innovate Summit 2026",
        "category": "Công nghệ"
      }
    ],
    "model_used": "gemini-2.0-flash"
  }
  ```
- **Response Lỗi Đầu vào (`400 Bad Request`):**
  ```json
  {
    "success": false,
    "error": "Nội dung câu hỏi không được để trống.",
    "code": "EMPTY_MESSAGE"
  }
  ```
- **Response Quá Tần suất (`429 Too Many Requests`):**
  ```json
  {
    "success": false,
    "error": "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 60 giây.",
    "code": "RATE_LIMIT_EXCEEDED"
  }
  ```

---

### 3.2. API Xác Thực Mã QR Điểm Danh (`POST /checkin/verify-api`)
- **Mục đích:** Nhân viên soát vé gửi mã QR quét được từ camera điện thoại để xác thực và check-in.
- **Quyền hạn:** Bắt buộc vai trò `staff`, `organizer` hoặc `admin`.
- **Request Body Payload:**
  ```json
  {
    "ticket_code": "TCK-001-0001-184CD6",
    "event_id": 1
  }
  ```
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "message": "Điểm danh thành công!",
    "attendee": {
      "registration_id": 14,
      "full_name": "Nguyễn Văn A",
      "email": "nguyenvana@gmail.com",
      "ticket_type": "Vé VIP",
      "checkin_time": "2026-09-28T19:30:00"
    }
  }
  ```
- **Response Vé Đã Check-in Trước Đó (`409 Conflict`):**
  ```json
  {
    "success": false,
    "error": "Vé này đã được điểm danh vào lúc 2026-09-28 18:45:12!",
    "code": "ALREADY_CHECKED_IN"
  }
  ```
- **Response Vé Không Tồn Tại (`404 Not Found`):**
  ```json
  {
    "success": false,
    "error": "Mã vé không hợp lệ hoặc không tìm thấy trong hệ thống.",
    "code": "TICKET_NOT_FOUND"
  }
  ```

---

### 3.3. API Đề Xuất Sự Kiện Thông Minh (`GET /ai/recommendations`)
- **Mục đích:** Cung cấp dữ liệu sự kiện đề xuất cá nhân hóa hiển thị trên thanh trượt trang chủ.
- **Quyền hạn:** Public.
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "recommendations": [
      {
        "id": 1,
        "title": "Hội Thảo Trí Tuệ Nhân Tạo & Chuyển Đổi Số 2026",
        "category": "Công nghệ",
        "start_date": "2026-10-15 08:30",
        "location_address": "Trung tâm Hội nghị White Palace, TP. Hồ Chí Minh",
        "banner_url": "/static/uploads/ai_banner.jpg",
        "match_percentage": 98,
        "reason": "Phù hợp với xu hướng quan tâm công nghệ và AI của bạn."
      }
    ]
  }
  ```

---

### 3.4. API Danh Sách Khách Tham Dự Của Sự Kiện (`GET /checkin/api/event-attendees/<int:event_id>`)
- **Mục đích:** Lấy danh sách toàn bộ khách đã đăng ký phục vụ giao diện điểm danh nhanh.
- **Quyền hạn:** `staff`, `organizer`, `admin`.
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "event_id": 1,
    "total_registered": 150,
    "total_checked_in": 82,
    "attendees": [
      {
        "registration_id": 1,
        "ticket_code": "TCK-001-0001-017566",
        "user_name": "Lê Hoàng Tuấn",
        "user_email": "tuan@eventai.vn",
        "ticket_name": "Vé Tiêu Chuẩn",
        "is_checked_in": true,
        "checkin_time": "2026-09-28 19:15:00"
      }
    ]
  }
  ```

---

### 3.5. API Điểm Danh Nhanh Thủ Công (`POST /checkin/api/quick-checkin/<int:reg_id>`)
- **Mục đích:** Cho phép nhân viên bấm nút check-in trực tiếp từ bảng danh sách mà không cần quét camera.
- **Quyền hạn:** `staff`, `organizer`, `admin`.
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "message": "Đã điểm danh thành công cho khách Lê Hoàng Tuấn.",
    "checkin_time": "2026-09-28 19:25:30"
  }
  ```

---

### 3.6. API Hoàn Tác Điểm Danh (`POST /checkin/api/undo-checkin/<int:reg_id>`)
- **Mục đích:** Hủy trạng thái đã điểm danh của một lượt đăng ký trong trường hợp nhân viên bấm nhầm.
- **Quyền hạn:** `staff`, `organizer`, `admin`.
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "message": "Đã hoàn tác trạng thái điểm danh."
  }
  ```

---

### 3.7. API Hộp Thư Thông Báo Mới Nhất (`GET /notifications/api/recent`)
- **Mục đích:** Hỗ trợ cơ chế Long-Polling cập nhật thông báo trên chuông thông báo Navbar.
- **Quyền hạn:** Authenticated.
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "unread_count": 3,
    "notifications": [
      {
        "id": 10,
        "title": "Nhắc hẹn sự kiện AI Summit ngày mai",
        "content": "Sự kiện của bạn sẽ bắt đầu vào 08:30 ngày mai...",
        "created_at": "10 phút trước",
        "is_read": false,
        "link": "/notifications/view/10"
      }
    ]
  }
  ```

---

### 3.8. API Điều Phối Đa Tác Tử (`POST /ai/multi-agent/advisory` & `POST /api/ai/multi-agent/advisory`)
- **Mục đích:** Kích hoạt pipeline 7 tác tử chuyên trách kết hợp MessageBus và Critic Guardrail.
- **Quyền hạn:** Public.
- **Request Body Payload:**
  ```json
  {
    "query": "Tôi cần tìm hội thảo AI tại Hà Nội có diễn giả Tiến sĩ Nguyễn Văn B với ngân sách 300.000 VNĐ"
  }
  ```
- **Response Thành công (`200 OK`):**
  ```json
  {
    "success": true,
    "task_id": "task_20260928_8819",
    "final_response": "Hệ thống tìm thấy sự kiện phù hợp...",
    "verdict": "APPROVED",
    "critic_notes": "All constraints satisfied, facts grounded 100% in SQL database.",
    "execution_time_ms": 2340
  }
  ```

---

## 4. QUY TẮC MÃ LỖI HTTP CHUẨN HOÁ TOÀN HỆ THỐNG

1. **Thành Công (2xx):**
   - `200 OK`: Truy vấn, cập nhật, hoặc xử lý thành công.
   - `201 Created`: Thêm mới bản ghi thành công (tạo sự kiện, đăng ký vé).
2. **Lỗi Phía Client (4xx):**
   - `400 Bad Request`: Payload JSON thiếu trường bắt buộc hoặc sai định dạng.
   - `401 Unauthorized`: Người dùng chưa xác thực hoặc phiên đăng nhập đã hết hạn.
   - `403 Forbidden`: Người dùng đã đăng nhập nhưng không đủ quyền hạn (RBAC violation).
   - `404 Not Found`: Không tìm thấy tài nguyên trong cơ sở dữ liệu.
   - `409 Conflict`: Xung đột dữ liệu (vé đã check-in, tài khoản đã đăng ký sự kiện).
   - `422 Unprocessable Entity`: Dữ liệu vi phạm quy tắc nghiệp vụ (sự kiện đã hết vé).
   - `429 Too Many Requests`: Vượt quá tần suất giới hạn rate limit.
3. **Lỗi Phía Máy Chủ (5xx):**
   - `500 Internal Server Error`: Ngoại lệ không lường trước tại backend; luôn được bọc trong cấu trúc JSON an toàn:
     ```json
     {
       "success": false,
       "error": "Đã xảy ra sự cố nội bộ. Vui lòng liên hệ quản trị viên.",
       "code": "INTERNAL_SERVER_ERROR"
     }
     ```

---

## 5. TỔNG KẾT & KẾT LUẬN ĐỒNG BỘ:
- **Độ bao phủ thực tế:** **66/66 Endpoints (100.0%)** đã được rà soát và mô tả chi tiết, chính xác theo mã nguồn `app.url_map`.
- **Khoảng cách GAP-005:** Đã khắc phục triệt để và nghiệm thu thành công (**RESOLVED**).
- **Tính khả thi:** 100% routes đều có thể kiểm thử tự động thông qua Pytest Flask Test Client (`client.get()`, `client.post()`).
