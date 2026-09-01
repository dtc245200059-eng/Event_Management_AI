# 🌟 EventAI Pro - Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (AI-Augmented SDLC)

Dự án **Hệ Thống Quản Lý Sự Kiện Tích Hợp AI** được thiết kế, phát triển, kiểm thử và tài liệu hóa toàn diện theo quy trình **AI-Augmented Software Development Life Cycle (AI-Augmented SDLC)** kết hợp mô hình kiểm soát con người (**Human-in-the-loop: Human Gate 1, 2, 3**). Hệ thống đáp ứng trọn vẹn tiêu chuẩn chất lượng và tài liệu hướng dẫn thực hành AI-Augmented SDLC.

---

## 📚 Hệ Thống Tài Liệu Kỹ Thuật Đầy Đủ (`docs/`)

Hệ thống sở hữu bộ tài liệu kỹ thuật hoàn chỉnh 20 tài liệu phân bổ qua 8 giai đoạn SDLC:

| Giai Đoạn SDLC | Tài Liệu Kỹ Thuật | Mô Tả Trọng Tâm |
| :--- | :--- | :--- |
| **1. Requirements Engineering** | [customer-requirement.md](file:///d:/Event_Management_AI/docs/customer-requirement.md) | Yêu cầu bài toán ban đầu từ khách hàng & 4 điểm nghẽn vận hành. |
| | [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md) | Đặc tả SRS (FR-01..08, FR-AI-01..04, NFR-01..09, Business Rules). |
| | [user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md) | Toàn bộ User Stories định dạng chuẩn `As a... I want... so that...`. |
| | [acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md) | Tiêu chí chấp nhận `Given - When - Then` cho tất cả các tính năng. |
| | [requirements-issues.md](file:///d:/Event_Management_AI/docs/requirements-issues.md) | Báo cáo phát hiện mơ hồ, giả định kỹ thuật & Biên bản Human Gate 1. |
| **2. Architecture Design** | [architecture.md](file:///d:/Event_Management_AI/docs/architecture.md) | Kiến trúc 3-Tier + AI Service Layer, Component Decomposition, Sequence Diagrams. |
| | [architecture-decisions.md](file:///d:/Event_Management_AI/docs/architecture-decisions.md) | Hồ sơ 8 quyết định kiến trúc cốt lõi (ADR-001 đến ADR-008). |
| | [chatbot-architecture.md](file:///d:/Event_Management_AI/docs/chatbot-architecture.md) | Kiến trúc chuyên sâu phân hệ RAG Chatbot & Dual-Engine (Live/Mock). |
| | [chatbot-data-flow.md](file:///d:/Event_Management_AI/docs/chatbot-data-flow.md) | Sơ đồ luồng dữ liệu DFD (Mức 0, Mức 1, Mức 2) cho AI pipeline. |
| **3. Database Design** | [database-design.md](file:///d:/Event_Management_AI/docs/database-design.md) | Thiết kế CSDL 9 bảng chuẩn 3NF, ERD, Data Dictionary, Human Gate 3. |
| | [schema.sql](file:///d:/Event_Management_AI/database/schema.sql) | Tệp DDL SQL thuần tạo bảng, khóa chính, khóa ngoại, indexes. |
| **4. Implementation & AI** | [question-analysis.md](file:///d:/Event_Management_AI/docs/question-analysis.md) | Phân tích 5 nhóm Intent & Entity Extraction cho RAG Assistant. |
| **5. Testing & QA** | [test-plan.md](file:///d:/Event_Management_AI/docs/test-plan.md) | Chiến lược kiểm thử, phạm vi, môi trường và ma trận ca kiểm thử. |
| | [test-report.md](file:///d:/Event_Management_AI/docs/test-report.md) | Báo cáo thực thi Pytest đạt **100% PASSED (11/11 tests)** và Test Evidence. |
| **6. Code Review** | [code-review.md](file:///d:/Event_Management_AI/docs/code-review.md) | Báo cáo thẩm định chất lượng mã nguồn theo 8 tiêu chuẩn kỹ thuật. |
| **7. Security Review** | [security-review.md](file:///d:/Event_Management_AI/docs/security-review.md) | Kiểm toán an ninh bảo mật theo chuẩn OWASP Top 10 Web & OWASP LLM. |
| **8. Delivery & Operations** | [api.md](file:///d:/Event_Management_AI/docs/api.md) | Đặc tả toàn bộ RESTful API và các endpoint AI. |
| | [deployment.md](file:///d:/Event_Management_AI/docs/deployment.md) | Hướng dẫn triển khai môi trường Virtualenv, Docker và Docker Compose. |
| | [user-guide.md](file:///d:/Event_Management_AI/docs/user-guide.md) | Cẩm nang hướng dẫn sử dụng cho Admin, Staff, Attendee và Chatbot AI. |
| | [traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md) | Ma trận truy vết 2 chiều kết nối Yêu cầu -> Kiến trúc -> CSDL -> Code -> Test. |

---

## 🏛️ Kiến Trúc Hệ Thống (3-Tier + AI Service Layer)

```
[ Client Layer (Browser) ]
       │  HTML5, CSS3 Glassmorphism, Vanilla JS, Chart.js, HTML5-QRCode
       ▼
[ Business Layer (Flask Blueprint Factory) ]
       │  auth, events, tickets, checkin, admin, ai_routes
       ├── Business Services (EventService, TicketService, CheckinService)
       ├── AI Services (RAG Engine, Content Generator, Recommendations, Predictive, Sentiment)
       └── Rate Limiter & Offline Fallback Mock Engine
       ▼
[ Data Layer (SQLAlchemy ORM + SQLite / PostgreSQL 3NF) ]
       └── 9 Tables: users, events, speakers, venues, schedules, attendees, tickets, registrations, ai_chat_history
       ▼
[ External AI Layer ]
       └── Google Gemini API (2.0 Flash / google-genai SDK)
```

---

## 🚀 4 Điểm Chạm AI Nổi Bật (AI Touchpoints)

1. **AI RAG Chatbot (Cửa sổ Chat Widget nổi)**:
   - Truy xuất có cấu trúc dữ liệu sự kiện, lịch trình, diễn giả, giá vé từ CSDL.
   - Ghép Context động vào System Prompt Template với **quy tắc nghiêm ngặt chống Hallucination**.
   - Hỗ trợ **Offline Fallback Mock Engine** tự động kích hoạt khi mất mạng hoặc không có API Key.
2. **AI Event Content Generator (Form Quản trị)**:
   - Tự động sinh bài viết giới thiệu sự kiện hấp dẫn, chuyên nghiệp và tối ưu tỷ lệ chuyển đổi.
3. **AI Recommendation Engine (Trang Chủ)**:
   - Sử dụng **TF-IDF & Cosine Similarity** so khớp sở thích của Attendee với các thẻ, chủ đề của sự kiện để xếp hạng sự kiện phù hợp nhất (% Match).
4. **Predictive & Sentiment Analytics (Dashboard Admin)**:
   - **Predictive Attendance**: Dự báo tỷ lệ tham dự thực tế (% Show-up Rate) và khuyến nghị số ghế / teabreak.
   - **Sentiment Analysis**: Phân loại cảm xúc phản hồi người tham dự (Positive, Neutral, Negative).

---

## 🧠 Hệ Thống 12 AI Skills (`.agents/skills/`)

Hệ thống được tổ chức với **12 Skills chuyên môn hóa** đặt trong thư mục `.agents/skills/` theo chuẩn huấn luyện AI Agent:

| STT | Tên Skill | Vị Trí Lưu Trữ | Vai Trò & Nhiệm Vụ Trong SDLC |
| :---: | :--- | :--- | :--- |
| 1 | `requirements-analysis` | `.agents/skills/requirements-analysis/SKILL.md` | Phân tích 4 điểm nghẽn, sinh User Stories, Acceptance Criteria, Human Gate 1. |
| 2 | `architecture-design` | `.agents/skills/architecture-design/SKILL.md` | Thiết kế kiến trúc 3 tầng, phân rã Component, DFD, Sequence và ADRs. |
| 3 | `database-design` | `.agents/skills/database-design/SKILL.md` | Chuẩn hóa CSDL 9 bảng 3NF, quan hệ PK-FK và sinh `schema.sql`. |
| 4 | `implementation` | `.agents/skills/implementation/SKILL.md` | Lập trình có kỷ luật, đọc đặc tả, hiện thực hóa Flask Blueprints & Models. |
| 5 | `testing` | `.agents/skills/testing/SKILL.md` | Xây dựng chiến lược kiểm thử tự động, chạy Pytest và xuất báo cáo. |
| 6 | `code-review` | `.agents/skills/code-review/SKILL.md` | Thẩm định chất lượng mã nguồn độc lập theo 8 tiêu chuẩn kỹ thuật. |
| 7 | `security-review` | `.agents/skills/security-review/SKILL.md` | Kiểm toán an ninh mạng OWASP Top 10 và OWASP Top 10 for LLMs. |
| 8 | `question-analysis` | `.agents/skills/question-analysis/SKILL.md` | Phân tích ý định (Intent) và trích xuất thực thể từ câu hỏi Chatbot. |
| 9 | `event-retrieval` | `.agents/skills/event-retrieval/SKILL.md` | Truy xuất dữ liệu có cấu trúc từ CSDL phục vụ RAG Grounded Context. |
| 10 | `context-builder` | `.agents/skills/context-builder/SKILL.md` | Định dạng và làm giàu Grounded Context chèn vào Prompt. |
| 11 | `rag-prompt` | `.agents/skills/rag-prompt/SKILL.md` | Thiết kế Prompt 5 thành phần có quy tắc chống Hallucination. |
| 12 | `documentation` | `.agents/skills/documentation/SKILL.md` | Duy trì bộ tài liệu kỹ thuật trong `docs/` và Ma trận truy vết RTM. |

---

## 👥 Danh Sách Tài Khoản Mẫu Đăng Nhập Mặc Định

| Vai trò | Tên đăng nhập | Mật khẩu | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@123` | Toàn quyền quản trị, xem Dashboard biểu đồ Analytics, quản lý Users. |
| **Staff** | `staff` | `Staff@123` | Vận hành quét mã QR Check-in bằng Camera Web hoặc nhập mã thủ công. |
| **Attendee 1** | `attendee1` | `User@123` | Đã đặt vé VIP Vietnam AI Summit 2026, đã thanh toán và đã check-in. |
| **Attendee 2** | `attendee2` | `User@123` | Đã đăng ký vé Miễn phí, chưa check-in, sở hữu mã QR vé điện tử. |
| **Attendee 3** | `attendee3` | `User@123` | Đã đặt vé Cloud TechDay, có thể trải nghiệm gửi feedback đánh giá. |

---

## 💻 Hướng Dẫn Cài Đặt & Chạy Cục Bộ

### 1. Cài đặt môi trường Python & Dependencies
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Khởi tạo Cơ sở dữ liệu 9 bảng chuẩn 3NF & Dữ liệu mẫu
```powershell
python seed.py
```

### 3. Chạy Server Flask
```powershell
python run.py
```
> Truy cập trình duyệt tại: **http://127.0.0.1:5000**

---

## 🧪 Chạy Bộ Kiểm Thử Tự Động (Pytest)

Chạy 11 test cases tự động bao quát toàn bộ logic xác thực, phân quyền RBAC, kiểm soát Quota vé, ngăn chặn check-in lặp lại và dịch vụ AI:
```powershell
.venv\Scripts\python.exe -m pytest -v
```

---

## 🐳 Triển Khai Với Docker & Docker Compose

```powershell
docker compose up -d --build
```
Truy cập: **http://localhost:5000**
