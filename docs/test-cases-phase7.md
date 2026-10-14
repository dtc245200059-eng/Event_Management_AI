# BẢNG ĐẶC TẢ TEST CASES KIỂM THỬ GIAI ĐOẠN 7 (PHASE 7 TEST CASES SPECIFICATION)

**Dự án:** EventAI Pro — Nền tảng Quản trị & Điều hành Sự kiện Toàn diện Tích hợp Đa tác tử AI  
**Phiên bản kiểm thử:** v2.4.0-hardened  
**Môi trường:** Python 3.14.2, Flask 3.1.0, SQLite (In-Memory / Test DB), Pytest 9.0.2  
**Ngày cập nhật:** 28/09/2026  
**Chuẩn tham chiếu:** ISO/IEC/IEEE 29119-3:2021 Software Testing Standards  

---

## MỤC LỤC

1. [TC-BUILD: Kiểm thử Môi trường & Khởi động Build](#1-tc-build-kiểm-thử-môi-trường--khởi-động-build)
2. [TC-API: Kiểm thử Tích hợp API & Endpoint Khế ước](#2-tc-api-kiểm-thử-tích-hợp-api--endpoint-khế-ước)
3. [TC-DB: Kiểm thử Cơ sở dữ liệu, Ràng buộc Toàn vẹn & Rollback](#3-tc-db-kiểm-thử-cơ-sở-dữ-liệu-ràng-buộc-toàn-vẹn--rollback)
4. [TC-AUTH: Kiểm thử Xác thực & Phân quyền RBAC](#4-tc-auth-kiểm-thử-xác-thực--phân-quyền-rbac)
5. [TC-WORKFLOW: Kiểm thử Quy trình Nghiệp vụ Cốt lõi](#5-tc-workflow-kiểm-thử-quy-trình-nghiệp-vụ-cốt-lõi)
6. [TC-AI: Kiểm thử Hệ thống AI & Gemini Integration](#6-tc-ai-kiểm-thử-hệ-thống-ai--gemini-integration)
7. [TC-AI-ASSISTANT: Kiểm thử Trợ lý Ảo AI Assistant](#7-tc-ai-assistant-kiểm-thử-trợ-lý-ảo-ai-assistant)
8. [TC-MOBILE: Kiểm thử Giao diện Đáp ứng Responsive & Di động](#8-tc-mobile-kiểm-thử-giao-diện-đáp-ứng-responsive--di-động)
9. [TC-A11Y: Kiểm thử Khả năng Tiếp cận (Accessibility)](#9-tc-a11y-kiểm-thử-khả-năng-tiếp-cận-accessibility)
10. [TC-SEC: Kiểm thử An toàn & Bảo mật](#10-tc-sec-kiểm-thử-an-toàn--bảo-mật)
11. [TC-PERF: Kiểm thử Hiệu năng & Độ trễ](#11-tc-perf-kiểm-thử-hiệu-năng--độ-trễ)
12. [TC-E2E: Kiểm thử Luồng Trực tiếp Toàn trình (End-to-End)](#12-tc-e2e-kiểm-thử-luồng-trực-tiếp-toàn-trình-end-to-end)

---

## 1. TC-BUILD: KIỂM THỬ MÔI TRƯỜNG & KHỞI ĐỘNG BUILD

### TC-BUILD-001: Khởi động Application Factory & Định tuyến URL (Route Registration)
- **Category:** Environment & Build Validation
- **Preconditions:** Virtual environment kích hoạt (`.venv`), biến môi trường `FLASK_ENV=testing` đã nạp.
- **Steps:**
  1. Khởi tạo `app = create_app('testing')`.
  2. Duyệt qua `app.url_map.iter_rules()`.
  3. Đếm tổng số route endpoints đã đăng ký trong bảng routing table.
- **Expected Result:** Toàn bộ 67 URL rules (bao gồm `/health` mới) được đăng ký thành công mà không có xung đột endpoint.
- **Actual Result:** 67 routes đã được đăng ký chính xác, không phát sinh lỗi khởi tạo hoặc circular imports.
- **Status:** PASS
- **Evidence:** `len(list(app.url_map.iter_rules())) == 67`
- **Related GAP:** GAP-04, GAP-11

### TC-BUILD-002: Khởi tạo Metadata Cơ sở dữ liệu In-Memory
- **Category:** Environment & Build Validation
- **Preconditions:** Khởi tạo `app` với `SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'`.
- **Steps:**
  1. Kích hoạt `with app.app_context():`.
  2. Thực thi `db.create_all()`.
  3. Kiểm tra danh sách tables trong `db.metadata.tables`.
- **Expected Result:** Đủ 11 bảng quan hệ (`users`, `attendees`, `events`, `speakers`, `venues`, `schedules`, `tickets`, `registrations`, `notifications`, `event_faqs`, `ai_chat_history`) được sinh DDL hợp lệ.
- **Actual Result:** 11/11 tables được tạo thành công trong SQLite memory.
- **Status:** PASS
- **Evidence:** `len(db.metadata.tables) == 11`
- **Related GAP:** GAP-05, GAP-06

---

## 2. TC-API: KIỂM THỬ TÍCH HỢP API & ENDPOINT KHẾ ƯỚC

### TC-API-HEALTH-001: Probe Kiểm tra Sức khỏe Hệ thống (`GET /health`)
- **Category:** API Integration
- **Preconditions:** App đang chạy ở test client.
- **Steps:**
  1. Gửi HTTP GET tới `/health`.
  2. Đọc HTTP Status Code và nội dung JSON.
- **Expected Result:** HTTP Status 200 OK, JSON schema `{"status": "healthy", "service": "EventAI Pro", "database": "connected", "routes_count": 67}`.
- **Actual Result:** HTTP Status 200 OK, payload đầy đủ theo chuẩn Microservice Liveness Probe.
- **Status:** PASS
- **Evidence:** `res.status_code == 200 and res.json['status'] == 'healthy'` (Latency: 0.38ms)
- **Related GAP:** GAP-04

### TC-API-MAIN-001: Tải Trang Chủ Hệ thống (`GET /`)
- **Category:** API Integration
- **Preconditions:** Database có dữ liệu mẫu sự kiện.
- **Steps:**
  1. Gửi HTTP GET tới `/`.
  2. Kiểm tra mã phản hồi HTTP và các thẻ nhận diện (AI Carousel, Navbar, Search Bar).
- **Expected Result:** HTTP Status 200 OK, render HTML `main/index.html` hoàn chỉnh.
- **Actual Result:** HTTP Status 200 OK, thời gian phản hồi đạt 2.64ms.
- **Status:** PASS
- **Evidence:** `res.status_code == 200`
- **Related GAP:** N/A

### TC-API-EVENT-001: Xem Chi tiết Sự kiện Hợp lệ (`GET /events/<id>`)
- **Category:** API Integration
- **Preconditions:** Event ID = 1 tồn tại trong CSDL với trạng thái `published`.
- **Steps:**
  1. Gửi HTTP GET tới `/events/1`.
  2. Kiểm tra mã phản hồi và nội dung chi tiết.
- **Expected Result:** HTTP Status 200 OK, hiển thị tiêu đề sự kiện, lịch trình, bảng vé và diễn giả.
- **Actual Result:** HTTP Status 200 OK, tải đầy đủ bảng vé và lịch trình phiên thảo luận.
- **Status:** PASS
- **Evidence:** `res.status_code == 200`
- **Related GAP:** GAP-01

### TC-API-EVENT-002: Xử lý Truy vấn Sự kiện Không tồn tại (`GET /events/999999`)
- **Category:** API Integration / Negative Test
- **Preconditions:** Sự kiện ID = 999999 không có trong CSDL.
- **Steps:**
  1. Gửi HTTP GET tới `/events/999999`.
- **Expected Result:** HTTP Status 404 Not Found được kích hoạt bởi `db.get_or_404(Event, id)`.
- **Actual Result:** HTTP Status 404 trả về chính xác, trang 404 thân thiện hiển thị.
- **Status:** PASS
- **Evidence:** `res.status_code == 404`
- **Related GAP:** GAP-01

### TC-API-AUTH-001: Chặn Truy cập Tuyến được Bảo vệ khi Chưa Đăng nhập (`GET /admin/dashboard`)
- **Category:** Authentication & Authorization
- **Preconditions:** Client chưa đăng nhập (Session trống).
- **Steps:**
  1. Gửi HTTP GET tới `/admin/dashboard`.
- **Expected Result:** HTTP Status 302 Redirect về tuyến đăng nhập `/auth/login?next=%2Fadmin%2Fdashboard`.
- **Actual Result:** HTTP Status 302 chuyển hướng chuẩn xác theo khế ước Flask-Login.
- **Status:** PASS
- **Evidence:** `res.status_code == 302 and '/auth/login' in res.location`
- **Related GAP:** GAP-02

---

## 3. TC-DB: KIỂM THỬ CƠ SỞ DỮ LIỆU, RÀNG BUỘC TOÀN VẸN & ROLLBACK

### TC-DB-UNIQUE-001: Ràng buộc Duy nhất Cặp `(event_id, attendee_id)` Trên Bảng `registrations`
- **Category:** Database Testing
- **Preconditions:** Người tham dự A đã đăng ký vé cho sự kiện E (Bản ghi `reg1` đã commit).
- **Steps:**
  1. Cố ý tạo bản ghi `reg2` với cùng `event_id` và `attendee_id`.
  2. Thực hiện `db.session.add(reg2)` và `db.session.commit()`.
  3. Bắt ngoại lệ `sqlalchemy.exc.IntegrityError`.
- **Expected Result:** Cơ sở dữ liệu từ chối giao dịch, ném `IntegrityError`, không sinh bản ghi trùng.
- **Actual Result:** Bắt được `IntegrityError`, giao dịch bị chặn hoàn toàn, kho dữ liệu nguyên vẹn.
- **Status:** PASS
- **Evidence:** `pytest.raises(IntegrityError)`
- **Related GAP:** GAP-05

### TC-DB-ROLLBACK-001: Cơ chế Phục hồi Session Tự động (Atomic Rollback Resilience)
- **Category:** Database Testing
- **Preconditions:** Giao dịch trước vừa gặp lỗi `IntegrityError`.
- **Steps:**
  1. Gọi lệnh `db.session.rollback()`.
  2. Thực thi một truy vấn SELECT đơn giản `User.query.count()`.
- **Expected Result:** Session được phục hồi trạng thái sạch (clean session state), câu lệnh tiếp theo thực thi thành công.
- **Actual Result:** Session phục hồi hoàn hảo, đếm đúng số người dùng trong CSDL.
- **Status:** PASS
- **Evidence:** Truy vấn kế tiếp trả về kết quả chính xác, không gặp lỗi `PendingRollbackError`.
- **Related GAP:** GAP-03, GAP-05

---

## 4. TC-AUTH: KIỂM THỬ XÁC THỰC & PHÂN QUYỀN RBAC

### TC-AUTH-001: Đăng nhập Người dùng Hợp lệ
- **Category:** Authentication
- **Preconditions:** Người dùng `eval_user` tồn tại với mật khẩu `User@123`.
- **Steps:**
  1. Gửi POST tới `/auth/login` với form `{username: 'eval_user', password: 'User@123'}`.
- **Expected Result:** HTTP Status 302 Redirect về `/`, session cookie thiết lập.
- **Actual Result:** Đăng nhập thành công, flash message chào mừng người dùng.
- **Status:** PASS
- **Evidence:** `res.status_code == 302`
- **Related GAP:** N/A

### TC-AUTH-002: Từ chối Đăng nhập khi Sai Mật khẩu
- **Category:** Authentication / Negative Test
- **Preconditions:** Người dùng `eval_user` tồn tại.
- **Steps:**
  1. Gửi POST tới `/auth/login` với form `{username: 'eval_user', password: 'WrongPassword'}`.
- **Expected Result:** HTTP Status 200 OK (Render lại login form), flash message cảnh báo sai mật khẩu.
- **Actual Result:** Giữ nguyên form đăng nhập, hiển thị thông báo lỗi 'Tên đăng nhập hoặc mật khẩu không chính xác'.
- **Status:** PASS
- **Evidence:** `b'kh\xc3\xb4ng ch\xc3\xadnh x\xc3\xa1c' in res.data`
- **Related GAP:** N/A

### TC-AUTH-RBAC-001: Người dùng Thường (Attendee) Bị Chặn Khỏi Quản trị (`GET /admin/dashboard`)
- **Category:** Authorization / RBAC
- **Preconditions:** Đăng nhập dưới quyền `eval_user` (role='attendee').
- **Steps:**
  1. Gửi GET tới `/admin/dashboard`.
- **Expected Result:** HTTP Status 403 Forbidden do vi phạm `@admin_required`.
- **Actual Result:** HTTP Status 403 trả về ngay lập tức.
- **Status:** PASS
- **Evidence:** `res.status_code == 403`
- **Related GAP:** GAP-02

### TC-AUTH-RBAC-002: Nhân viên (Staff) Bị Chặn Khỏi Quản trị Cấp Cao (`GET /admin/dashboard`)
- **Category:** Authorization / RBAC
- **Preconditions:** Đăng nhập dưới quyền `eval_staff` (role='staff').
- **Steps:**
  1. Gửi GET tới `/admin/dashboard`.
- **Expected Result:** HTTP Status 403 Forbidden.
- **Actual Result:** HTTP Status 403 trả về chính xác.
- **Status:** PASS
- **Evidence:** `res.status_code == 403`
- **Related GAP:** GAP-02

### TC-AUTH-RBAC-003: Quản trị viên (Admin) Truy cập Thành công Dashboard (`GET /admin/dashboard`)
- **Category:** Authorization / RBAC
- **Preconditions:** Đăng nhập dưới quyền `eval_admin` (role='admin').
- **Steps:**
  1. Gửi GET tới `/admin/dashboard`.
- **Expected Result:** HTTP Status 200 OK, tải đầy đủ biểu đồ phân tích và thống kê hệ thống.
- **Actual Result:** HTTP Status 200 OK.
- **Status:** PASS
- **Evidence:** `res.status_code == 200`
- **Related GAP:** GAP-02

---

## 5. TC-WORKFLOW: KIỂM THỬ QUY TRÌNH NGHIỆP VỤ CỐT LÕI

### TC-WORKFLOW-CHECKIN-001: Thực hiện Check-in Lần đầu Qua API Nhân viên
- **Category:** Core Business Workflow (Check-in)
- **Preconditions:** Đăng nhập tài khoản Staff, vé hợp lệ ở trạng thái `paid`.
- **Steps:**
  1. Gửi POST tới `/checkin/api/quick-checkin/<reg_id>`.
- **Expected Result:** Phản hồi JSON `{"success": true, "message": "Check-in thành công..."}`, cập nhật trường `checked_in=True`, `checked_in_at=now`.
- **Actual Result:** Check-in thành công trong 1 chạm, trả về tên khách và mã vé.
- **Status:** PASS
- **Evidence:** `data['success'] is True`
- **Related GAP:** N/A

### TC-WORKFLOW-CHECKIN-002: Ngăn chặn Check-in Trùng lặp (Anti-duplicate Scan Defense)
- **Category:** Core Business Workflow (Check-in) / Edge Case
- **Preconditions:** Vé vừa được check-in ở bước trước.
- **Steps:**
  1. Gửi lại request POST tới `/checkin/api/quick-checkin/<reg_id>`.
- **Expected Result:** HTTP Status 409 Conflict, JSON `{"success": false, "message": "Vé đã được check-in lúc..."}`.
- **Actual Result:** Bị từ chối với mã 409 Conflict, ghi nhận đúng thời gian và nhân viên đã quét trước đó.
- **Status:** PASS
- **Evidence:** `res.status_code == 409`
- **Related GAP:** N/A

### TC-WORKFLOW-FEEDBACK-001: Đánh giá Sự kiện & Phân tích Cảm xúc Tự động (Sentiment Analysis)
- **Category:** Core Business Workflow (Feedback)
- **Preconditions:** Khách hàng sở hữu vé hợp lệ đã tham gia sự kiện.
- **Steps:**
  1. Gửi POST tới `/tickets/feedback/<reg_id>` với `feedback_rating=5` và nội dung khen ngợi.
- **Expected Result:** Bản ghi cập nhật `feedback_rating=5`, AI service tự động gán nhãn `sentiment='positive'`.
- **Actual Result:** Lưu phản hồi thành công, gán nhãn `positive` chuẩn xác.
- **Status:** PASS
- **Evidence:** `reg.feedback_rating == 5 and reg.sentiment == 'positive'`
- **Related GAP:** GAP-03

---

## 6. TC-AI: KIỂM THỬ HỆ THỐNG AI & GEMINI INTEGRATION

### TC-AI-INTENT-001: Phân loại Ý định Người dùng (Question Intent Analysis)
- **Category:** AI Engine 1 (RAG)
- **Preconditions:** Module `rag_service.analyze_question` sẵn sàng.
- **Steps:**
  1. Phân tích câu hỏi: *"Sự kiện AI Summit bắt đầu lúc mấy giờ?"*.
- **Expected Result:** Ý định `is_schedule_query` được kích hoạt (`True`).
- **Actual Result:** Nhận diện chính xác `is_schedule_query: True`.
- **Status:** PASS
- **Evidence:** `intent_data['is_schedule_query'] is True`
- **Related GAP:** N/A

### TC-AI-RAG-CONTEXT-001: Trích xuất Ngữ cảnh Có cấu trúc (Ground Truth Context Builder)
- **Category:** AI Engine 1 (RAG)
- **Preconditions:** CSDL có dữ liệu sự kiện AI Summit.
- **Steps:**
  1. Gọi `build_retrieved_context("AI Summit")`.
- **Expected Result:** Chuỗi ngữ cảnh trả về có tiêu đề sự kiện, giá vé, lịch trình và tiêu đề định danh `=== DANH SÁCH DỮ LIỆU SỰ KIỆN TRUY XUẤT TỪ CSDL (GROUND TRUTH) ===`.
- **Actual Result:** Trích xuất ngữ cảnh hoàn chỉnh với token budgeting an toàn.
- **Status:** PASS
- **Evidence:** `'GROUND TRUTH' in ctx`
- **Related GAP:** N/A

### TC-AI-RAG-001: Động cơ Dự phòng Cục bộ (Offline Grounded Mock Engine)
- **Category:** AI Engine 1 (RAG) / Fallback
- **Preconditions:** Khóa `GEMINI_API_KEY` trống hoặc môi trường offline.
- **Steps:**
  1. Gọi `call_gemini("Giá vé hội thảo là bao nhiêu?")`.
- **Expected Result:** Hệ thống không sụp đổ, tự động kích hoạt `mock` engine, trả về phản hồi hữu ích với latency < 1ms.
- **Actual Result:** Phản hồi mượt mà, `mode='mock'`, độ trễ 0.04ms.
- **Status:** PASS
- **Evidence:** `mode == 'mock' and len(answer) > 20`
- **Related GAP:** N/A

### TC-AI-PII-001: Cơ chế Làm sạch Dữ liệu Nhạy cảm (PII Sanitization Defense)
- **Category:** AI Safety & Security
- **Preconditions:** Module `sanitize_pii` kích hoạt.
- **Steps:**
  1. Truyền chuỗi chứa thông tin nhạy cảm: *"Tài khoản của tôi pass: Secret123 và cccd: 0123456789"*.
- **Expected Result:** Mật khẩu và thông tin định danh bị thay thế bằng nhãn bảo vệ `[PROTECTED]`.
- **Actual Result:** Chuỗi nhạy cảm bị che giấu hoàn toàn trước khi nạp vào LLM prompt.
- **Status:** PASS
- **Evidence:** `'[PROTECTED]' in sanitized and 'Secret123' not in sanitized`
- **Related GAP:** N/A

### TC-AI-RATELIMIT-001: Bộ Giới hạn Tần suất Yêu cầu Token Bucket (Rate Limiting)
- **Category:** AI Resilience & DoS Protection
- **Preconditions:** Cấu hình giới hạn 2 requests / phút.
- **Steps:**
  1. Gửi liên tiếp 3 requests từ cùng 1 IP.
- **Expected Result:** Request 1: Cho phép (True), Request 2: Cho phép (True), Request 3: Từ chối (False).
- **Actual Result:** Cơ chế Token Bucket chặn đứng request thứ 3 chính xác.
- **Status:** PASS
- **Evidence:** `[True, True, False]`
- **Related GAP:** GAP-02

### TC-AI-BENCHMARK-10CASES: Benchmark Định lượng 10 Ca Kiểm thử Single-Agent vs Multi-Agent
- **Category:** AI Engine 2 (Multi-Agent System)
- **Preconditions:** Đủ 10 ca kiểm thử định lượng trong `BENCHMARK_CASES`.
- **Steps:**
  1. Thực thi `run_benchmark_suite(quick_mode=False)`.
  2. Đo lường tỷ lệ ảo giác (Hallucination Rate) và độ chính xác (Accuracy).
- **Expected Result:** Multi-Agent đạt tỷ lệ ảo giác = 0.0% và độ chính xác cao hơn Single-Agent.
- **Actual Result:** Multi-Agent: Độ chính xác 95.7%, Ảo giác 0.0% (Single-Agent: Độ chính xác 70.0%, Ảo giác 0.0%).
- **Status:** PASS
- **Evidence:** `summary['multi_agent']['hallucination_rate'] == 0.0`
- **Related GAP:** N/A

---

## 7. TC-AI-ASSISTANT: KIỂM THỬ TRỢ LÝ ẢO AI ASSISTANT

### TC-AI-CHAT-API-001: Gọi API Chatbot Đa lượt (`POST /api/ai/chat`)
- **Category:** AI Assistant
- **Preconditions:** Client gửi payload JSON hợp lệ.
- **Steps:**
  1. Gửi POST tới `/api/ai/chat` với `{"message": "Hội thảo có những sự kiện nào?"}`.
- **Expected Result:** HTTP Status 200 OK, trả về trường `response` chứa câu trả lời định dạng Markdown có link điều hướng.
- **Actual Result:** HTTP Status 200 OK, câu trả lời chi tiết, latency 3.8ms.
- **Status:** PASS
- **Evidence:** `res.status_code == 200 and 'response' in res.json`
- **Related GAP:** GAP-02

---

## 8. TC-MOBILE: KIỂM THỬ GIAO DIỆN ĐÁP ỨNG RESPONSIVE & DI ĐỘNG

### TC-MOBILE-VIEWPORT-001: Thẻ Meta Viewport Hỗ trợ Tai thỏ (Safe Area / Viewport-fit=cover)
- **Category:** Mobile Responsiveness
- **Preconditions:** HTML template gốc `base.html`.
- **Steps:**
  1. Kiểm tra thuộc tính `viewport` trong thẻ `<head>`.
- **Expected Result:** Chứa thuộc tính `viewport-fit=cover` để hiển thị tràn viền chuẩn thiết bị Apple/Android.
- **Actual Result:** Thẻ `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">` hiện diện.
- **Status:** PASS
- **Evidence:** Khớp cú pháp trong DOM `base.html`.
- **Related GAP:** N/A

### TC-MOBILE-DRAWER-001: Khung Điều hướng Rút gọn Apple Mobile Drawer
- **Category:** Mobile Responsiveness
- **Preconditions:** Tải trang trên mobile viewport.
- **Steps:**
  1. Kiểm tra sự tồn tại của phần tử Drawer trong DOM.
- **Expected Result:** Phần tử `#appleMobileDrawer` hiện diện với lớp phủ overlay Backdrop Glassmorphism.
- **Actual Result:** Container hiện diện với cấu trúc chuẩn.
- **Status:** PASS
- **Evidence:** `id="appleMobileDrawer"` hiện diện trong DOM.
- **Related GAP:** N/A

### TC-MOBILE-NAV-001: Thanh Điều hướng Đáy Apple Mobile Bottom Navigation
- **Category:** Mobile Responsiveness
- **Preconditions:** Viewport `< 992px` (d-lg-none).
- **Steps:**
  1. Kiểm tra phần tử navigation đáy trong DOM.
- **Expected Result:** `<nav class="apple-bottom-nav d-lg-none" id="appleBottomNav">` hiện diện với 5 tab điều hướng chính (Home, Events, AI Center, Role Tab, Menu).
- **Actual Result:** Thanh bottom navigation hiện diện đầy đủ 5 tab điều hướng chuẩn công thái học ngón tay cái.
- **Status:** PASS
- **Evidence:** `id="appleBottomNav"` hiện diện trong DOM.
- **Related GAP:** N/A

---

## 9. TC-A11Y: KIỂM THỬ KHẢ NĂNG TIẾP CẬN (ACCESSIBILITY)

### TC-A11Y-ARIA-001: Thuộc tính Nhãn ARIA Label & Phím Tắt Khả Tiếp cận
- **Category:** Accessibility (A11y)
- **Preconditions:** DOM `base.html` được render.
- **Steps:**
  1. Kiểm tra các nút bấm mở menu, nút trợ lý AI, và các thành phần tương tác.
- **Expected Result:** Các nút chỉ có icon đều được trang bị `aria-label` chi tiết (e.g. `aria-label="Mở Trợ lý AI EventAI"`).
- **Actual Result:** 100% các nút điều hướng di động đều có nhãn `aria-label` phục vụ Screen Readers.
- **Status:** PASS
- **Evidence:** `aria-label="Mở Trợ lý AI EventAI"`, `aria-label="Mobile Bottom Navigation"`.
- **Related GAP:** N/A

---

## 10. TC-SEC: KIỂM THỬ AN TOÀN & BẢO MẬT

### TC-SEC-SQLI-001: Kháng Tấn công Tiêm mã SQL (SQL Injection Defense)
- **Category:** Security Testing
- **Preconditions:** Endpoint tìm kiếm `/events?search=...`.
- **Steps:**
  1. Gửi chuỗi độc hại kinh điển: `' OR '1'='1`.
- **Expected Result:** SQLAlchemy xử lý dưới dạng Parameterized Query an toàn, không rò rỉ toàn bộ CSDL hoặc ném lỗi cú pháp SQL.
- **Actual Result:** HTTP Status 200 OK, tìm kiếm chuỗi văn bản thuần, không xảy ra SQLi.
- **Status:** PASS
- **Evidence:** `res.status_code == 200`
- **Related GAP:** N/A

### TC-SEC-XSS-001: Kháng Tấn công Chèn mã Kịch bản Chéo (Cross-Site Scripting - XSS)
- **Category:** Security Testing
- **Preconditions:** Gửi chuỗi kịch bản qua tham số truy vấn: `<script>alert('XSS')</script>`.
- **Steps:**
  1. Gửi GET tới `/events?search=<script>alert('XSS')</script>`.
  2. Kiểm tra mã HTML render.
- **Expected Result:** Trình biên dịch Jinja2 tự động escape chuỗi thành `&lt;script&gt;`, ngăn chặn mã thực thi trong trình duyệt.
- **Actual Result:** Thẻ `<script>` hoàn toàn không xuất hiện ở dạng unescaped thô trong HTML.
- **Status:** PASS
- **Evidence:** Chuỗi được auto-escaped an toàn bởi Jinja2.
- **Related GAP:** N/A

### TC-SEC-CSRF-001: Bảo vệ Chống Giả mạo Yêu cầu Chéo Trang (CSRF Defense)
- **Category:** Security Testing
- **Preconditions:** Trang HTML tải về máy người dùng.
- **Steps:**
  1. Kiểm tra thẻ `<meta name="csrf-token">` trong thẻ `<head>`.
  2. Kiểm tra hàm `window.getCsrfToken()` trong `main.js`.
- **Expected Result:** Token CSRF được nạp vào DOM và các hàm fetch AJAX tự động đính kèm header `X-CSRFToken`.
- **Actual Result:** Thẻ `<meta name="csrf-token">` hiện diện và được `main.js` tiêu thụ tự động.
- **Status:** PASS
- **Evidence:** `TC-FE-CSRF-001: PASS`
- **Related GAP:** GAP-04

---

## 11. TC-PERF: KIỂM THỬ HIỆU NĂNG & ĐỘ TRỄ

### TC-PERF-001: Đo lường Độ trễ Các Tuyến Quan trọng (Latency Benchmarking)
- **Category:** Performance Testing
- **Preconditions:** Client nội bộ thực hiện 10 lượt đo liên tiếp cho mỗi endpoint.
- **Steps:**
  1. Đo lường thời gian đáp ứng trung bình (Average Latency) và phân vị P95 (95th Percentile) cho `/health`, `/`, `/events`, `/events/1`, `/api/ai/recommendations`.
- **Expected Result:** Mọi endpoint nội bộ đều có độ trễ trung bình < 10ms trên môi trường kiểm thử.
- **Actual Result:**
  - `GET /health`: 0.38ms (P95: 0.45ms)
  - `GET /`: 2.64ms (P95: 2.72ms)
  - `GET /events`: 3.43ms (P95: 4.07ms)
  - `GET /events/1`: 2.69ms (P95: 3.88ms)
  - `GET /api/ai/recommendations`: 0.84ms (P95: 1.25ms)
- **Status:** PASS
- **Evidence:** Dữ liệu đo lường thực nghiệm ghi trong `scratch/phase7_eval_results.json`.
- **Related GAP:** N/A

---

## 12. TC-E2E: KIỂM THỬ LUỒNG TRỰC TIẾP TOÀN TRÌNH (END-TO-END)

### TC-E2E-001: Toàn trình Khách hàng (User Journey)
- **Category:** End-to-End Workflow
- **Steps:** Đăng ký tài khoản -> Đăng nhập -> Duyệt danh sách sự kiện -> Xem chi tiết sự kiện -> Đặt vé thành công -> Mở Trợ lý AI hỏi thông tin lịch trình -> Nhận câu trả lời grounding -> Điểm danh sự kiện -> Gửi đánh giá Feedback -> Đăng xuất.
- **Expected Result:** Luồng giao dịch liền mạch, dữ liệu liên kết nhất quán giữa 6 bảng liên quan.
- **Actual Result:** Đạt 100% tiêu chí chấp nhận.
- **Status:** PASS
- **Evidence:** Các unit & integration test phối hợp xác nhận thành công.
- **Related GAP:** All GAPs
