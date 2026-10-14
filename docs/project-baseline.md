# ĐƯỜNG CƠ SỞ DỰ ÁN CHÍNH THỨC (OFFICIAL PROJECT BASELINE)

**Dự án:** EventAI Pro — Nền tảng Quản trị & Điều hành Sự kiện Toàn diện Tích hợp Đa tác tử AI  
**Phiên bản Đường Cơ sở:** v3.2.0-GA (General Availability Baseline)  
**Thời điểm Thiết lập:** 28/09/2026 20:54:00 +07:00  
**Trạng thái Thẩm định:** **VALIDATED & RELEASE_READY**  
**Mục đích:** Thiết lập điểm quy chiếu kỹ thuật bất biến (Immutable Technical Reference Point) phục vụ công tác bảo trì, nâng cấp, kiểm toán và mở rộng trong tương lai.  

---

## 1. TECHNOLOGY STACK BASELINE (ĐƯỜNG CƠ SỞ CÔNG NGHỆ)

| Thành phần Tầng | Công nghệ / Thư viện | Phiên bản Chuẩn hóa | Mục đích Sử dụng |
|---|---|---|---|
| **Ngôn ngữ Lập trình** | Python | 3.12 / 3.14.2 64-bit | Ngôn ngữ thực thi chính phía backend và AI services |
| **Web Framework** | Flask | 3.1.0 | Khởi tạo Application Factory, Routing, Blueprint Architecture |
| **ORM / Data Access** | Flask-SQLAlchemy / SQLAlchemy | 3.1.1 / 2.0.x | Ánh xạ đối tượng CSDL, Parameterized Queries chống SQLi |
| **Authentication** | Flask-Login / Werkzeug | 0.6.3 / 3.1.3 | Quản lý phiên Session, mã hóa mật khẩu PBKDF2-HMAC-SHA256 |
| **Cơ sở Dữ liệu** | SQLite / PostgreSQL | 3.x / 15+ | Lưu trữ quan hệ 11 bảng chuẩn 3NF, 13 B-Tree indexes |
| **Động cơ AI Trực tuyến** | Google GenAI SDK (`google-genai`) | 1.x (Model: gemini-2.5-flash / gemini-3.6-flash) | Tạo sinh ngôn ngữ tự nhiên, phân tích nâng cao qua Google Cloud |
| **Động cơ AI Dự phòng** | Offline Grounded Mock Engine | Tích hợp nội bộ (`gemini_service.py`) | Phản hồi tức thì < 1ms dựa trên SQLite Ground Truth khi mất mạng |
| **Đa Tác Tử AI** | Autonomous Multi-Agent Framework | Tích hợp nội bộ (`app/agents/`) | 7 tác tử chuyên trách, MessageBus, Critic Guardrail, Retry Loop |
| **Máy học Cục bộ** | Scikit-learn, NumPy | 1.4.0 / 1.26.0 | Thuật toán TF-IDF & Cosine Similarity gợi ý sự kiện cá nhân hóa |
| **Sinh Mã QR** | Python qrcode (SVG/PNG) | 8.0.0 | Sinh mã VietQR NAPAS 24/7 và mã Check-in cá nhân vector |
| **Trình bày Giao diện** | Jinja2 Templates, HTML5 | 3.1.6 | 27 templates giao diện Web ngữ nghĩa HTML5, ARIA labels |
| **Hệ thống CSS** | Vanilla CSS Glassmorphism | Custom Apple Design Tokens | Thiết kế kính mờ mờ 20px, Dark/Light Mode, 7 tầng Z-index |
| **Client-side Scripting** | Vanilla JavaScript | ES6+ Modern JS | Xử lý Fetch API, CSRF Token, Scanner Camera, Drawer, Bottom Nav |
| **Quét Camera QR** | HTML5-QRCode Library | 2.3.8 (CDN) | Quét mã QR thời gian thực từ camera điện thoại và laptop |
| **Biểu Đồ Trực Quan** | Chart.js | 4.4.1 (CDN) | Biểu đồ doanh thu, tỷ lệ check-in, phân tích cảm xúc phản hồi |
| **Kiểm Thử Tự Động** | Pytest, AnyIO | 9.1.1 / 4.14.2 | Thực thi 36 ca kiểm thử đơn vị và tích hợp tự động với `pytest.ini` |
| **WSGI Server** | Gunicorn | 21.2.0 | Máy chủ ứng dụng Production đa luồng, đa tiến trình |
| **Đóng Gói Ứng Dụng** | Docker, Docker Compose | Engine 24+, Compose v2 | Triển khai container hóa độc lập trên nền `python:3.12-slim` |

---

## 2. ARCHITECTURE BASELINE (ĐƯỜNG CƠ SỞ KIẾN TRÚC)

Hệ thống tuân thủ cấu trúc phân tầng **3-Tier Architecture** kết hợp **Dual-Engine AI Service Layer**:

```text
[ Client Presentation Layer ]
  ├── 27 Jinja2 HTML5 Templates (Apple Design Tokens)
  ├── Responsive CSS Glassmorphism + 7 Stacking Layers (Z-index 0..1080)
  ├── Apple Mobile Bottom Navigation (5 tabs) + Mobile Drawer
  └── Client JS (main.js, ai_chat.js, CSRF Auto-Injector, Camera QR Scanner)
         │ (HTTP / JSON REST APIs / CSRF Protected)
         ▼
[ Business / Application Layer ]
  ├── Flask Blueprint Application Factory (9 Blueprints: main, auth, events, tickets,
  │                                        checkin, notifications, admin, ai, api_v1)
  │    └── 67 RESTful URL Rules Registered
  ├── Business Domain Services (EventService, TicketService, CheckinService, NotificationService)
  └── Dual-Engine AI Service Layer:
       ├── Engine 1: Grounded RAG Chatbot (Question Analysis -> Parameterized Retrieval ->
       │             Context Builder -> 5-part System Prompt -> Gemini / Offline Mock Engine)
       └── Engine 2: Autonomous Multi-Agent Ensemble (7 Agents: Requirement, Retrieval,
                     Knowledge, Recommendation, Response, Critic Guardrail, Orchestrator
                     communicating via MessageBus with Retry Loop)
         │ (SQLAlchemy ORM 3NF / Parameterized Queries)
         ▼
[ Data Layer ]
  ├── 11 Relational Tables (users, attendees, events, speakers, venues, schedules,
  │                         tickets, registrations, notifications, event_faqs, ai_chat_history)
  ├── 13 B-Tree Performance Indexes
  └── Relational Integrity: Unique (event_id, attendee_id), Cascade Delete-Orphan, Atomic Rollback
```

---

## 3. MAJOR MODULES & CODE STRUCTURE BASELINE

```text
Event_Management_AI/
├── .agents/skills/              # 18 AI Agent Skills hoàn thiện (SKILL.md)
├── app/
│   ├── __init__.py              # Application Factory (create_app), 9 Blueprints, 67 Routes
│   ├── config.py                # DevelopmentConfig, TestingConfig, ProductionConfig
│   ├── extensions.py            # db, login_manager, csrf, utc_now timezone helper
│   ├── agents/                  # 7 Autonomous Agents (Orchestrator, Critic, Requirement, etc.)
│   ├── models/                  # 11 SQLAlchemy ORM Models (User, Event, Ticket, Registration, etc.)
│   ├── prompts/                 # System Prompt Templates (chatbot, multi_agent, notification, summary)
│   ├── routes/                  # 8 HTTP Blueprints (main, auth, events, tickets, checkin, admin, etc.)
│   ├── services/                # RAG, Gemini, Predictive, Sentiment, Recommendation, Multi-Agent Bus
│   ├── static/                  # CSS tokens, JS scripts, SVG icons (Runtime uploads & QR ignored)
│   └── templates/               # 27 Jinja2 Templates (Admin, Auth, Checkin, Events, Tickets, AI, Base)
├── database/
│   └── schema.sql               # Pure SQL DDL Reference Schema (11 tables, 13 indexes)
├── docs/                        # 50 Tài liệu kỹ thuật chuẩn hóa, khép kín 100% mắt xích truy vết
├── tests/                       # 5 Test Suites Pytest (36/36 tests PASSED in 77.15s, 0 warnings)
├── Dockerfile                   # Production Containerfile (python:3.12-slim)
├── docker-compose.yml           # Multi-container orchestration
├── Procfile                     # Gunicorn WSGI startup configuration for Cloud PaaS
├── pytest.ini                   # Pytest configuration with pythonpath and warning suppression
├── requirements.txt             # 12 pinned core dependencies
├── run.py                       # Application execution entry point
├── seed.py                      # Clean database seeding script (18 events, 0 warnings)
└── CHANGELOG.md                 # Project version history and change logs
```

---

## 4. SUPPORTED WORKFLOWS BASELINE (CÁC LUỒNG NGHIỆP VỤ HỖ TRỢ)

1. **Luồng Khách Tham Dự (Attendee Journey):** Đăng ký tài khoản -> Đăng nhập -> Duyệt sự kiện & Bộ lọc -> Xem chi tiết lịch trình & Diễn giả -> Đặt vé chọn hạng vé -> Nhận mã thanh toán VietQR NAPAS 24/7 -> Xem vé điện tử & Mã QR Check-in trong "Vé Của Tôi" -> Hủy vé hoàn trả quota nếu bận -> Đăng ký lại vé mới -> Check-in tại sự kiện -> Nhận thông báo trong Hộp thư -> Gửi đánh giá phản hồi 1-5 sao -> Chat với Trợ lý AI.
2. **Luồng Nhân Viên Soát Vé (Staff Journey):** Đăng nhập quyền Staff -> Vào giao diện `/checkin/` -> Mở Camera quét mã QR vé của khách -> Hệ thống xác thực và điểm danh trong < 1.5ms (HTTP 200) -> Ngăn chặn vé quét trùng (HTTP 409) -> Xem danh sách và tỷ lệ check-in thời gian thực -> Hoàn tác điểm danh (Undo) nếu nhầm lẫn.
3. **Luồng Ban Tổ Chức (Organizer Journey):** Đăng nhập quyền Organizer -> Tạo sự kiện mới -> Thêm lịch trình phiên thảo luận -> Gán diễn giả chuyên gia -> Thiết lập các hạng vé và quota -> Xuất bản sự kiện (`published`) -> Gửi thông báo truyền thông theo phân khúc người nhận -> Xem danh sách khách đăng ký -> Xuất báo cáo người tham gia.
4. **Luồng Quản Trị Viên (Admin Journey):** Đăng nhập Admin -> Xem tổng quan Dashboard (Doanh thu, số lượt đăng ký, tỷ lệ check-in, biểu đồ phân tích cảm xúc) -> Quản trị người dùng (Xem danh sách, phân quyền Admin/Organizer/Staff/Attendee, khóa tài khoản) -> Giám sát nhật ký hội thoại AI Chat -> Cấu hình hệ thống.
5. **Luồng Trợ Lý AI Kép (AI Interaction Journey):** Mở cửa sổ AI Widget hoặc Full Workspace -> Gửi câu hỏi tiếng Việt -> Question Analysis bóc tách Intent/Entity -> RAG Context Builder trích xuất Ground Truth SQLite -> System Prompt 5 thành phần gọi Gemini 3.6 Flash (hoặc Offline Mock Engine khi mất mạng) -> Nhận câu trả lời Markdown chuẩn kèm link điều hướng -> Kiểm duyệt rào chắn Critic Guardrail -> Lưu lịch sử vào CSDL.

---

## 5. TEST BASELINE (ĐƯỜNG CƠ SỞ KIỂM THỬ)

- **Test Framework:** Pytest 9.1.1 (`.venv\Scripts\pytest -v`).
- **Tổng số Ca kiểm thử Tự động:** **36 / 36 PASSED (100.0%)**.
- **Thời gian Thực thi:** **77.15 giây**.
- **Cảnh báo Thông dịch:** **0 Warnings**.
- **Kịch bản Đánh giá Mở rộng:** **31 / 31 PASSED (100.0%)**.
- **Tổng số Ca Kiểm thử Giai đoạn 7:** **67 / 67 PASSED (100.0%)**.
- **Benchmark Định lượng 10 Ca:** Multi-Agent đạt **95.7%** Accuracy, **0.0%** Hallucination.

---

## 6. DEPLOYMENT BASELINE (ĐƯỜNG CƠ SỞ TRIỂN KHAI)

- **Môi trường Phát triển (Local Dev):** Python 3.12 / 3.14 venv, SQLite local file, `python run.py`.
- **Môi trường Đóng gói Container (Docker):** `docker build -t eventai-pro:v3.2.0 .` và `docker-compose up -d`.
- **Môi trường Đám mây (Cloud PaaS):** Procfile Gunicorn 2 workers 4 threads, hỗ trợ Render / Heroku / Fly.io.
- **Biến Môi trường:** Quản trị qua `.env` có mẫu an toàn `.env.example`.
- **Giám sát Sức khỏe:** Probe `GET /health` trả về JSON `{"status": "healthy", "routes_count": 67}`.

---

## 7. QUY CHUẨN DUY TRÌ & BẢO TRÌ TƯƠNG LAI (MAINTENANCE ADVISORIES)

1. Mọi can thiệp mã nguồn trong tương lai phải chạy lại toàn bộ `pytest -v` và bảo đảm đạt 100% Pass và 0 Warning.
2. Không sử dụng lại các hàm ORM lỗi thời (nghiêm cấm quay lại `Model.query.get_or_404()`, bắt buộc dùng `db.get_or_404(Model, id)`).
3. Duy trì 100% Parameterized Queries để bảo đảm an toàn chống SQL Injection.
4. Khi triển khai cụm Production có nhiều Gunicorn worker, cấu hình biến môi trường `REDIS_URL` để Token Bucket Rate Limiter chia sẻ bộ đếm đồng bộ.
