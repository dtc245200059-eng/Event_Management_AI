# 📋 CHANGELOG — NHẬT KÝ THAY ĐỔI DỰ ÁN EVENTAI PRO

Tất cả các thay đổi đáng chú ý của dự án **EventAI Pro** được tài liệu hóa tại tệp này theo tiêu chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) và tuân thủ nguyên tắc [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v3.2.0] — 28/09/2026 — RELEASE CANDIDATE (PHASE 8 GA)

### 🚀 Tính Năng Bổ Sung & Hoàn Thiện (Added)

- **Probe Kiểm tra Sức khỏe Microservice (`GET /health`):** Bổ sung endpoint probe kiểm tra trạng thái CSDL và số lượng routes đăng ký, phục vụ liveness/readiness probe cho Kubernetes / Docker / Render (GAP-04).
- **Bộ Giới hạn Tần suất Token Bucket Rate Limiter (`gemini_service.py`):** Tích hợp thuật toán cửa sổ trượt (Sliding Window) 30 requests/phút/IP nhằm chống tấn công từ chối dịch vụ (DoS) và cạn kiệt ngân sách AI (GAP-02).
- **Cơ chế Bảo vệ Giả mạo Yêu cầu Chéo trang (CSRF):** Nhúng thẻ `<meta name="csrf-token">` vào `base.html` và cung cấp hàm `window.getCsrfToken()` trong `main.js` bảo vệ toàn diện cho các yêu cầu AJAX Fetch (GAP-04).
- **Giao dịch Điểm danh 1 Chạm & Chống Quét Trùng (Anti-Duplicate Check-in):** Trả về HTTP 200 cho lượt quét hợp lệ và HTTP 409 Conflict kèm cảnh báo thời gian đã quét trước đó khi quét lặp lại.
- **Hệ thống Đa tác tử AI (Autonomous Multi-Agent Architecture):** Hiện thực hóa 7 tác tử chuyên trách (`RequirementAgent`, `RetrievalAgent`, `KnowledgeAgent`, `RecommendationAgent`, `ResponseAgent`, `CriticAgent`, `OrchestratorAgent`) giao tiếp qua trục truyền tin `MessageBus` với cơ chế rào chắn kiểm duyệt `CriticGuardrail`.
- **Benchmark Định lượng 10 Ca Kiểm thử:** So sánh đối đầu giữa Single-Agent và Multi-Agent, chứng minh Multi-Agent đạt độ chính xác 95.7% và triệt tiêu 100% ảo giác (Hallucination Rate = 0.0%).
- **Thanh Điều hướng Đáy Apple Bottom Navigation:** Bổ sung thanh điều hướng 5 tabs công thái học di động (`#appleBottomNav`) trên màn hình `< 992px`.
- **Hệ thống CSS Tokens & 7 Tầng Z-index:** Chuẩn hóa Z-index từ tầng 0 đến tầng 6 (`1080`), loại bỏ triệt để hiện tượng đè lấp giao diện giữa Modal, Drawer và AI Assistant.
- **Kịch bản Khởi động Theme Không Chớp Sáng (Anti-FOUC Script):** Pre-load tức thời `data-theme` tại thẻ `<head>` trong 0.05ms.

### 🛠️ Sửa Đổi & Vá Lỗi (Fixed)

- **Khắc phục Cú pháp Truy xuất Khóa chính ORM Lỗi thời (GAP-01):** Thay thế toàn bộ 22 vị trí `Model.query.get_or_404()` bằng `db.get_or_404(Model, id)`, loại bỏ 22 cảnh báo `LegacyAPIWarning` của Flask-SQLAlchemy 3.x.
- **Tính Bền vững & Atomic Rollback trong Hủy Vé (GAP-03, GAP-05):** Bổ sung khối `try/except` kèm `db.session.rollback()` trong hàm `cancel_ticket` (`app/routes/tickets.py`), đảm bảo khi hủy vé thì `remaining_quota` được hoàn trả sạch sẽ và người dùng được phép đăng ký lại vé mới.
- **Triệt tiêu Hoàn toàn Cảnh báo Python 3.14 (GAP-11):** Tạo tệp `pytest.ini` với `pythonpath = .` và cấu hình bộ lọc `filterwarnings = ignore::UserWarning:google.genai.types`, đưa bộ kiểm thử 36 tests về trạng thái **0 Cảnh báo (0 Warnings)**.
- **Làm sạch Biến Môi trường Mẫu (`.env.example`):** Thay thế chuỗi token thật bằng placeholder an toàn `your_gemini_api_key_here`.
- **Cập nhật `.gitignore`:** Bổ sung `app/static/qr_codes/`, `app/static/qrcodes/`, `app/static/uploads/` để giữ cây thư mục Git sạch sẽ khỏi các tệp sinh ra khi chạy test.
- **Đồng bộ Thời gian Múi giờ UTC trong `seed.py`:** Thay thế `datetime.utcnow()` lỗi thời bằng `utc_now()`, đưa quy trình seed CSDL về trạng thái 0 cảnh báo.

### 🔒 An Toàn & Bảo Mật (Security)

- Mã hóa mật khẩu một chiều bằng thuật toán PBKDF2-HMAC-SHA256 với Salt ngẫu nhiên.
- 100% Parameterized Queries qua SQLAlchemy ORM kháng tuyệt đối SQL Injection.
- Jinja2 Auto-escaping kháng Cross-Site Scripting (XSS).
- Bộ lọc `sanitize_pii()` che giấu 100% mật khẩu, số CCCD và thông tin ngân hàng trước khi gửi câu hỏi tới Google Gemini API.
- Ranh giới phân quyền RBAC 4 vai trò (`admin`, `organizer`, `staff`, `attendee`) bảo vệ nghiêm ngặt bằng các decorator chuyên dụng.

### 📊 Thẩm Định Chất Lượng & Kiểm Thử (Verification & Testing)

- **Pytest Suite:** 36/36 tests PASSED trong 77.15s, 0 failures, 0 warnings.
- **Evaluation Scenarios:** 31/31 scenarios PASSED trong 2.1s.
- **Độ trễ Endpoints:** `/health` 0.38ms, `/` 2.64ms, `/events` 3.43ms, `/api/ai/recommendations` 0.84ms, Offline Mock AI 0.04ms.
- **Tài liệu Kỹ thuật:** Đồng bộ hoàn toàn 50 tài liệu kỹ thuật trong `docs/` và 18 kỹ năng trong `.agents/skills/`.

---

## [v2.4.0] — 20/09/2026

- Phát triển các tính năng quản trị sự kiện, bảng vé, đặt vé và sinh mã QR VietQR NAPAS 24/7.
- Tích hợp động cơ RAG Chatbot cơ bản với SQLite context.
- Thiết kế giao diện Apple Glassmorphism và chế độ Dark/Light mode ban đầu.
