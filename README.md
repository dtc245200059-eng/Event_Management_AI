# 🌟 EventAI Pro - Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (AI-Augmented SDLC)

Dự án **Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (EventAI Pro)** được thiết kế, phát triển, kiểm thử và tài liệu hóa toàn diện theo quy trình **AI-Augmented Software Development Life Cycle (AI-Augmented SDLC)** kết hợp mô hình kiểm soát con người (**Human-in-the-loop: Human Gate 1, 2, 3**). Hệ thống đáp ứng trọn vẹn tiêu chuẩn chất lượng của Đề tài 09 (Th.S Nguyễn Đình Dũng, ICTU) và bài thực hành Agentic AI Architecture.

---

## 📚 Hệ Thống Tài Liệu Kỹ Thuật Chuẩn Hóa (`docs/`)

Hệ thống sở hữu bộ tài liệu kỹ thuật hoàn chỉnh phân bổ qua các giai đoạn SDLC:

| Giai Đoạn SDLC | Tài Liệu Kỹ Thuật | Trạng Thái | Mô Tả Trọng Tâm |
| :--- | :--- | :---: | :--- |
| **1. Requirements** | [customer-requirement.md](docs/customer-requirement.md) | `[IMPLEMENTED]` | Yêu cầu bài toán ban đầu từ khách hàng & 4 điểm nghẽn vận hành. |
| | [requirements.md](docs/requirements.md) | `[IMPLEMENTED]` | Đặc tả SRS (FR-01..09, FR-AI-01..07, NFR-01..09, Business Rules). |
| | [user-stories.md](docs/user-stories.md) | `[IMPLEMENTED]` | 20 User Stories định dạng chuẩn `As a... I want... so that...`. |
| | [acceptance-criteria.md](docs/acceptance-criteria.md) | `[IMPLEMENTED]` | Tiêu chí chấp nhận `Given - When - Then` cho tất cả các tính năng. |
| | [requirements-issues.md](docs/requirements-issues.md) | `[RESOLVED]` | Báo cáo phát hiện mơ hồ, giả định kỹ thuật & Biên bản Human Gate 1. |
| **2. Architecture** | [architecture.md](docs/architecture.md) | `[IMPLEMENTED]` | Kiến trúc 3-Tier + Dual-Engine AI, Component Decomposition, Sequence. |
| | [architecture-decisions.md](docs/architecture-decisions.md) | `[IMPLEMENTED]` | Hồ sơ 8 quyết định kiến trúc cốt lõi (ADR-001 đến ADR-008). |
| | [chatbot-architecture.md](docs/chatbot-architecture.md) | `[IMPLEMENTED]` | Kiến trúc chuyên sâu phân hệ RAG Chatbot & Dual-Engine (Live/Mock). |
| | [chatbot-data-flow.md](docs/chatbot-data-flow.md) | `[IMPLEMENTED]` | Sơ đồ luồng dữ liệu DFD (Mức 0, Mức 1, Mức 2) cho AI pipeline. |
| | [multi-agent-architecture.md](docs/multi-agent-architecture.md) | `[IMPLEMENTED]` | Kiến trúc 7-Agent Ensemble, MessageBus, Critic Guardrail, Retry Loop. |
| | [multi-agent-benchmark-report.md](docs/multi-agent-benchmark-report.md) | `[IMPLEMENTED]` | Báo cáo đánh giá thực nghiệm 10 ca kiểm thử so sánh Single vs Multi-Agent. |
| **3. Database** | [database-design.md](docs/database-design.md) | `[IMPLEMENTED]` | Thiết kế CSDL 11 bảng chuẩn 3NF, ERD, 13 B-Tree indexes, Human Gate 3. |
| | [schema.sql](database/schema.sql) | `[IMPLEMENTED]` | Tệp DDL SQL thuần tạo bảng, khóa chính, khóa ngoại, indexes. |
| **4. Implementation & AI** | [question-analysis.md](docs/question-analysis.md) | `[IMPLEMENTED]` | Phân tích 5 nhóm Intent & Entity Extraction cho RAG Assistant. |
| **5. Testing & QA** | [test-plan.md](docs/test-plan.md) | `[IMPLEMENTED]` | Chiến lược kiểm thử, phạm vi, môi trường và 5 test suites. |
| | [test-report.md](docs/test-report.md) | `[IMPLEMENTED]` | Báo cáo thực thi Pytest đạt **100% PASSED (36/36 tests)** và Test Evidence. |
| **6. Code Review** | [code-review.md](docs/code-review.md) | `[IMPLEMENTED]` | Báo cáo thẩm định chất lượng mã nguồn theo 8 tiêu chuẩn kỹ thuật. |
| **7. Security Review** | [security-review.md](docs/security-review.md) | `[IMPLEMENTED]` | Kiểm toán an ninh mạng OWASP Top 10 Web & OWASP Top 10 LLM. |
| **8. Delivery & Operations** | [api.md](docs/api.md) | `[IMPLEMENTED]` | Đặc tả đầy đủ **67 RESTful Endpoints** và phân quyền RBAC. |
| | [deployment.md](docs/deployment.md) | `[IMPLEMENTED]` | Hướng dẫn triển khai Virtualenv, Docker, Docker Compose và Gunicorn. |
| | [user-guide.md](docs/user-guide.md) | `[IMPLEMENTED]` | Cẩm nang 12 luồng nghiệp vụ cho Admin, Organizer, Staff, Attendee. |
| | [traceability-matrix.md](docs/traceability-matrix.md) | `[IMPLEMENTED]` | Ma trận truy vết 2 chiều kết nối Yêu cầu -> Kiến trúc -> CSDL -> Code -> Test. |

---

## 🏛️ Kiến Trúc Hệ Thống (3-Tier + Dual-Engine AI Service Layer)

```
[ Client Layer (Browser) ]
       │  HTML5, CSS3 Glassmorphism Apple Tokens, Vanilla JS, Chart.js, HTML5-QRCode
       ▼
[ Business Layer (Flask Blueprint Application Factory - 8 Blueprints) ]
       │  main, auth, events, tickets, checkin, admin, notifications, ai
       ├── Business Services (EventService, TicketService, CheckinService, NotificationService)
       ├── Dual-Engine AI Service Layer:
       │     ├── Engine 1: Single-Agent RAG Assistant (RAG Pipeline + Offline Fallback Mock Engine)
       │     └── Engine 2: Multi-Agent Ensemble (7 Agents, MessageBus, Critic Guardrail, Retry Loop)
       └── Auxiliary AI (Content Generator, TF-IDF Recommender, Show-up Predictor, Sentiment)
       ▼
[ Data Layer (SQLAlchemy ORM + SQLite / PostgreSQL 3NF) ]
       └── 11 Bảng: users, speakers, venues, events, schedules, attendees,
                    tickets, registrations, ai_chat_history, notifications, event_faqs
       └── 13 B-Tree Indexes tối ưu hóa truy vấn thời gian thực
       ▼
[ External AI Layer ]
       └── Google Gemini API (gemini-2.0-flash / google-genai SDK)
```

---

## 🚀 Các Điểm Chạm AI Nổi Bật (AI Touchpoints)

1. **AI RAG Chatbot (Widget nổi & Trang chuyên biệt `/ai/workspace`)**:
   - Truy xuất có cấu trúc dữ liệu sự kiện, lịch trình, diễn giả, giá vé và FAQs từ CSDL.
   - Ghép Context động vào System Prompt Template với **quy tắc nghiêm ngặt chống Hallucination**.
   - Hỗ trợ **Offline Fallback Mock Engine** tự động kích hoạt khi mất mạng hoặc không có API Key.
2. **Multi-Agent Decision Advisory (Hệ Thống 7 Agent Chuyên Trách)**:
   - Phối hợp: `Orchestrator`, `Requirement`, `Retrieval SQL Tool`, `Knowledge Vector Tool`, `Recommendation`, `Critic Guardrail`, `Response Agent`.
   - **Critic Guardrail**: Độc lập kiểm duyệt chéo CSDL, chặn đứng 100% ảo giác (Hallucination rate: 0.0%).
   - **Retry Loop**: Tự động sửa lỗi tối đa 2 lần trước khi phản hồi người dùng.
3. **AI Soạn Thảo Email & Thông Báo Tự Động (`/api/ai/draft-notification`)**:
   - Soạn thảo thư mời, nhắc lịch, cảm ơn, cập nhật khẩn cấp theo chuẩn Đề tài 09, tuyệt đối không truyền PII người dùng vào prompt.
4. **AI Tóm Tắt Ý Kiến Phản Hồi (`/api/ai/summarize-feedback`)**:
   - Phân loại phản hồi thành 4 nhóm (Nội dung, Vận hành, Hậu cần, Lịch trình) và trích xuất Actionable Takeaways.
5. **AI Gợi Ý Cá Nhân Hóa & Dự Báo Tham Dự**:
   - Gợi ý sự kiện bằng **TF-IDF & Cosine Similarity** theo sở thích người dùng.
   - Dự báo tỷ lệ tham dự (% Show-up Rate) và phân loại cảm xúc khảo sát (Sentiment Analysis).

---

## 🧠 Hệ Thống 18 AI Skills Hoàn Chỉnh (`.agents/skills/`)

Hệ thống được tổ chức với **18 Skills chuyên môn hóa** đặt trong thư mục `.agents/skills/` tuân thủ nghiêm ngặt hợp đồng cấu trúc chuẩn:

| STT | Tên Skill | Đường Dẫn | Vai Trò & Nhiệm Vụ Trong SDLC |
| :---: | :--- | :--- | :--- |
| 1 | `requirements-analysis` | [.agents/skills/requirements-analysis/SKILL.md](.agents/skills/requirements-analysis/SKILL.md) | Phân tích 4 điểm nghẽn, sinh User Stories, Acceptance Criteria, Human Gate 1. |
| 2 | `architecture-design` | [.agents/skills/architecture-design/SKILL.md](.agents/skills/architecture-design/SKILL.md) | Thiết kế kiến trúc 3 tầng, phân rã Component, DFD, Sequence và ADRs. |
| 3 | `database-design` | [.agents/skills/database-design/SKILL.md](.agents/skills/database-design/SKILL.md) | Chuẩn hóa CSDL 11 bảng 3NF, 13 B-Tree indexes, quan hệ PK-FK và `schema.sql`. |
| 4 | `implementation` | [.agents/skills/implementation/SKILL.md](.agents/skills/implementation/SKILL.md) | Lập trình có kỷ luật, đọc đặc tả, hiện thực hóa Flask Blueprints & Models. |
| 5 | `frontend-development` | [.agents/skills/frontend-development/SKILL.md](.agents/skills/frontend-development/SKILL.md) | Phát triển giao diện Web Jinja2, hệ thống CSS tokens (Apple Design), JavaScript. |
| 6 | `responsive-mobile` | [.agents/skills/responsive-mobile/SKILL.md](.agents/skills/responsive-mobile/SKILL.md) | Tối ưu hóa giao diện di động, mobile drawer, bottom nav, touch swipe, QR scanner. |
| 7 | `api-development` | [.agents/skills/api-development/SKILL.md](.agents/skills/api-development/SKILL.md) | Thiết kế, chuẩn hóa và kiểm thử 66 RESTful endpoints, JSON Schema, RBAC. |
| 8 | `ai-agent` | [.agents/skills/ai-agent/SKILL.md](.agents/skills/ai-agent/SKILL.md) | Vận hành và mở rộng Hệ thống 7 Agent, MessageBus, Critic Guardrail. |
| 9 | `ai-evaluation` | [.agents/skills/ai-evaluation/SKILL.md](.agents/skills/ai-evaluation/SKILL.md) | Đánh giá chất lượng AI, thực thi benchmark 10 ca kiểm thử định lượng. |
| 10 | `event-retrieval` | [.agents/skills/event-retrieval/SKILL.md](.agents/skills/event-retrieval/SKILL.md) | Truy xuất dữ liệu có cấu trúc từ CSDL phục vụ RAG Grounded Context an toàn. |
| 11 | `rag-prompt` | [.agents/skills/rag-prompt/SKILL.md](.agents/skills/rag-prompt/SKILL.md) | Thiết kế Prompt 5 thành phần có quy tắc chống Hallucination. |
| 12 | `context-builder` | [.agents/skills/context-builder/SKILL.md](.agents/skills/context-builder/SKILL.md) | Định dạng và làm giàu Grounded Context chèn vào Prompt. |
| 13 | `question-analysis` | [.agents/skills/question-analysis/SKILL.md](.agents/skills/question-analysis/SKILL.md) | Phân tích ý định (Intent) và trích xuất thực thể từ câu hỏi Chatbot. |
| 14 | `testing` | [.agents/skills/testing/SKILL.md](.agents/skills/testing/SKILL.md) | Xây dựng chiến lược kiểm thử tự động, chạy 36 Pytests và xuất báo cáo. |
| 15 | `code-review` | [.agents/skills/code-review/SKILL.md](.agents/skills/code-review/SKILL.md) | Thẩm định chất lượng mã nguồn độc lập theo 8 tiêu chuẩn kỹ thuật. |
| 16 | `security-review` | [.agents/skills/security-review/SKILL.md](.agents/skills/security-review/SKILL.md) | Kiểm toán an ninh mạng OWASP Top 10 Web & OWASP Top 10 LLM. |
| 17 | `deployment` | [.agents/skills/deployment/SKILL.md](.agents/skills/deployment/SKILL.md) | Đóng gói, cấu hình môi trường Docker, docker-compose, Procfile Gunicorn. |
| 18 | `documentation` | [.agents/skills/documentation/SKILL.md](.agents/skills/documentation/SKILL.md) | Duy trì bộ tài liệu kỹ thuật trong `docs/` và Ma trận truy vết RTM. |

> Xem chi tiết: [Chỉ mục Kỹ năng (skills-index.md)](docs/skills-index.md) và [Bản đồ Phụ thuộc Kỹ năng (skills-dependency-map.md)](docs/skills-dependency-map.md).

---

## 👥 Danh Sách Tài Khoản Mẫu Đăng Nhập Mặc Định (4 Vai Trò Chuẩn)

| Vai trò | Tên đăng nhập | Mật khẩu | Quyền hạn & Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@123` | Toàn quyền quản trị, xem Dashboard với 8 chỉ số thực, quản lý Users, xem Agent logs. |
| **Organizer** | `organizer` | `Organizer@123` | Quản trị sự kiện, vé, diễn giả, lịch trình (start_at < end_at), soạn Email AI, xem & tóm tắt feedback. |
| **CheckInStaff** | `staff` | `Staff@123` | Vận hành soát vé tại cửa `/checkin/` (quét QR / nhập mã), check-in nguyên tử (Atomic), bị chặn vào Admin. |
| **Attendee 1** | `attendee1` | `User@123` | Đã đặt vé VIP Vietnam AI Summit 2026, đã thanh toán và đã check-in, gửi feedback. |
| **Attendee 2** | `attendee2` | `User@123` | Đã đăng ký vé Miễn phí, chưa check-in, sở hữu mã QR vé điện tử. |
| **Attendee 3** | `attendee3` | `User@123` | Đã đặt vé Cloud TechDay, có thể trải nghiệm hủy vé hoặc đặt lại. |

---

## 💻 Hướng Dẫn Cài Đặt & Chạy Cục Bộ

### 1. Cài đặt môi trường Python & Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Khởi tạo Cơ sở dữ liệu 11 bảng chuẩn 3NF & Dữ liệu mẫu
```powershell
python seed.py
```

### 3. Chạy Server Flask
```powershell
python run.py
```
> Truy cập trình duyệt tại: **http://127.0.0.1:5000**

---

## 🧪 Chạy Bộ Kiểm Thử Tự Động (Pytest 42 Tests) & Benchmark Prompt

### Chạy Toàn Bộ 42 Ca Kiểm Thử Pytest Tự Động:
Bao quát xác thực, phân quyền 4 vai trò RBAC, kiểm soát hạn mức vé, check-in nguyên tử chống lặp (HTTP 409), xác thực thời gian lịch trình, bảo vệ PII, và tầng Step 8 Response Validation của RAG:
```powershell
.\.venv\Scripts\pytest.exe -v
```
*(Kết quả: 42 passed in ~60s - 100% Passed, 0 Failures)*

### Chạy Đánh Giá Thực Nghiệm So Sánh 3 Chiến Lược Prompt (V1 vs V2 vs V3):
Thực thi 14 kịch bản kiểm thử bắt buộc (sự kiện bình thường, thiếu ngày, thiếu địa điểm, không tồn tại, hết vé, PII defense, Prompt Injection defense...):
```powershell
python eval_prompts.py
```
*(Báo cáo chi tiết được ghi nhận tại [docs/ai-prompt-comparison.md](docs/ai-prompt-comparison.md))*

---

## 👥 Phân Công Trách Nhiệm Nhóm 2 Thành Viên (RACI Matrix)

- **Thành viên 1 — Phụ trách Giao diện & Nghiệp vụ Sự kiện (Front-end & Event Operations):**
  - Thiết kế và chuẩn hóa giao diện theo chuẩn Apple Liquid Glass (Dark/Light mode, Responsive Mobile).
  - Giao diện quản lý sự kiện, lịch trình (bắt lỗi `start_at < end_at`), diễn giả, địa điểm.
  - Giao diện đăng ký vé, hiển thị vé điện tử, tạo và tải mã QR Vector SVG.
  - Màn hình soát vé Check-in (`/checkin/`) tích hợp Web Camera Scanner và nhập mã dự phòng.
  - Form thu thập ý kiến phản hồi và trang tổng hợp đánh giá `/events/<id>/feedback`.
- **Thành viên 2 — Phụ trách CSDL, An Ninh & Tích Hợp AI (Data, Security & AI Architect):**
  - Cấu trúc CSDL 11 bảng chuẩn 3NF, ràng buộc toàn vẹn, đánh index B-Tree và ACID transactions.
  - Cơ chế kiểm soát truy cập phân quyền 4 vai trò RBAC (`is_admin`, `is_organizer`, `is_checkin_staff`, `is_attendee`).
  - Check-in nguyên tử trên CSDL chia sẻ: `Registration.query.filter_by(id=..., checked_in=False).update(...)`.
  - Tích hợp Gemini API và chuỗi Grounded RAG 8 bước với Step 8 Response Validation.
  - Soạn thảo Email AI dùng placeholder `{attendee_name}`, `{event_name}`, lọc PII và bắt buộc duyệt bởi con người.
  - Tóm tắt phản hồi AI: khử khuẩn untrusted text, trích xuất điểm khen, khiếu nại, cảnh báo mẫu nhỏ (<3).
  - Xây dựng framework benchmark `eval_prompts.py` so sánh 3 chiến lược prompt V1, V2, V3.

---

## 🎬 Kịch Bản Trình Diễn Bắt Buộc (12-Step Demonstration Script)

1. **Khách tham dự chọn sự kiện:** Đăng nhập `attendee2` (`User@123`), vào danh sách sự kiện chọn sự kiện công nghệ.
2. **Đăng ký vé thành công:** Chọn hạng vé Miễn phí, xác nhận đăng ký; hệ thống kiểm tra sức chứa và ghi nhận đơn vé.
3. **Vé điện tử & Mã QR được sinh ra:** Vào trang "Vé Của Tôi" (`/tickets/my-tickets`), xem mã vé duy nhất và mã QR trực quan.
4. **Nhân viên soát vé kiểm tra:** Đăng nhập `staff` (`Staff@123`), truy cập màn hình Soát vé `/checkin/`.
5. **Ghi nhận Check-in thành công:** Quét mã QR hoặc nhập mã vé `TK-...`; hệ thống hiển thị thông báo check-in thành công kèm tên khách và thời gian thực.
6. **Từ chối Check-in quét lặp (Anti-duplicate):** Quét lại cùng mã vé lần thứ 2; hệ thống lập tức từ chối với cảnh báo đỏ HTTP 409: *"Vé này đã được check-in lúc..."*.
7. **Bảng điều khiển Thống kê cập nhật:** Đăng nhập `admin` (`Admin@123`), vào `/admin/dashboard`; 8 chỉ số thực tế (tổng vé, lượt check-in, tỷ lệ tham dự) tự động tăng lên tức thì.
8. **Khách gửi ý kiến phản hồi:** Khách tham dự đã check-in vào trang gửi đánh giá 5 sao kèm nhận xét về khâu tổ chức.
9. **AI Tóm tắt Ý kiến Phản hồi:** Đăng nhập `organizer`, vào `/events/<id>/feedback`; hệ thống khử khuẩn thông tin cá nhân và hiển thị tóm tắt AI: điểm khen ngợi, khiếu nại và khuyến nghị.
10. **Chatbot AI trả lời câu hỏi dựa trên dữ liệu thật:** Mở widget AI Chatbot, hỏi: *"Sự kiện Vietnam AI Summit 2026 diễn ra ở đâu và khi nào?"*; Chatbot trả lời chính xác từ CSDL, không bịa đặt ngày giờ hay địa điểm.
11. **Soạn thảo Email AI (Mời / Nhắc nhở / Cảm ơn):** Organizer vào phân hệ gửi thông báo, chọn loại email, AI sinh bản thảo chứa placeholder `{attendee_name}`; Organizer chỉnh sửa và phê duyệt trước khi gửi.
12. **So sánh 3 Phiên bản Prompt:** Mở báo cáo [docs/ai-prompt-comparison.md](docs/ai-prompt-comparison.md); trình chiếu bảng kết quả thực nghiệm 14 kịch bản chứng minh Prompt V3 đạt 100% độ chính xác, 0% ảo giác và kháng 100% prompt injection.

---

## 🐳 Triển Khai Với Docker & Docker Compose

```powershell
docker compose up -d --build
```
Truy cập: **http://localhost:5000**
