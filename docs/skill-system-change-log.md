# SKILL SYSTEM CHANGE LOG — NHẬT KÝ THAY ĐỔI HỆ THỐNG KỸ NĂNG

**Dự án:** EventAI Pro (`Event_Management_AI`)  
**Giai đoạn:** Phase 3 — Update & Repair Existing Skills  
**Thời điểm ghi nhận:** 2026-09-28 19:05:00 +07:00  

---

## BẢNG NHẬT KÝ THAY ĐỔI TOÀN BỘ 12 SKILLS HIỆN CÓ

### 1. `requirements-analysis`
- **Before:** Tệp sơ sài theo bài giảng môn học (7 mục: `Objective`, `Inputs`, `Process`, `Rules`, `Outputs`, `Verification`). Không có đường dẫn mã nguồn thực tế.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục (`Purpose`, `Scope`, `Non-Scope`, `When to Use`, `Source Files to Inspect`, `Workflow 5 bước`, `Validation`, `Failure Handling`, `Security`). Bổ sung quy trình Human Gate 1.
- **Reason:** Chuẩn hóa theo quy chuẩn vận hành của Agent; hướng dẫn Agent cách bóc tách SRS, User Story và AC chuẩn Gherkin.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `docs/customer-requirement.md`, `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md`, `docs/requirements-issues.md`, `docs/traceability-matrix.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 2. `architecture-design`
- **Before:** Mô tả lý thuyết kiến trúc 3 tầng chung chung; không tham chiếu tới 8 Blueprints, Application Factory, AI Gateway của dự án.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; gắn kết chặt chẽ với `app/__init__.py`, `app/routes/`, `app/services/gemini_service.py`, `app/agents/`; bổ sung quy trình viết bản ghi ADR và vẽ sơ đồ DFD/Sequence bằng Mermaid.
- **Reason:** Đảm bảo Agent hiểu đúng kiến trúc thực tế của repo và không làm xói mòn ranh giới các tầng (Architecture Drift).
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/__init__.py`, `app/config.py`, `app/extensions.py`, `app/routes/`, `app/services/gemini_service.py`, `app/services/rag_service.py`, `app/agents/orchestrator_agent.py`, `docs/architecture.md`, `docs/architecture-decisions.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 3. `database-design`
- **Before:** Bản tóm tắt môn học 4KB; chưa phản ánh đủ 11 bảng 3NF thực tế (thiếu bảng `notifications` và `event_faqs`); thiếu danh mục 13 B-Tree indexes.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; đồng bộ 100% với 11 ORM Models trong `app/models/`, `database/schema.sql`, 13 indexes, hàm thời gian `utc_now()`, cú pháp SQLAlchemy 2.0 `db.session.get()` và `db.get_or_404()`.
- **Reason:** Đảm bảo Agent nắm vững toàn bộ thực thể CSDL và không bao giờ sửa đổi schema mà thiếu kiểm soát an toàn.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `database/schema.sql`, `app/models/*.py`, `app/extensions.py`, `seed.py`, `docs/database-design.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 4. `implementation`
- **Before:** Chứa các đường dẫn giả định không có trong repo (`event_service.py`, `checkin_service.py`, `ticket_service.py`, `ai_routes.py`).
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; sửa đổi 100% đường dẫn thành các file có thật: `app/routes/events.py`, `app/routes/tickets.py`, `app/routes/checkin.py`, `app/routes/ai.py`; bổ sung quy chuẩn giao dịch `try...except...rollback()`.
- **Reason:** Loại bỏ hoàn toàn ảo giác về cấu trúc thư mục, chỉ dẫn Agent can thiệp đúng các tệp controller và service thực tế.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/routes/*.py`, `app/models/*.py`, `app/services/*.py`, `app/extensions.py`, `tests/*.py`, `docs/requirements.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 5. `code-review`
- **Before:** Lý thuyết review chung; thiếu danh sách tệp inspect thực tế; thiếu checklist thẩm định theo kiến trúc Flask.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; thiết lập bảng checklist 8 tiêu chuẩn cốt lõi (Correctness, Architecture, Security, Performance, Maintainability, Test Coverage, Error Handling, API Contract) và phân loại 4 mức độ rủi ro (CRITICAL, HIGH, MEDIUM, LOW).
- **Reason:** Cung cấp cho Agent quy trình đánh giá mã nguồn độc lập, chặt chẽ trước khi merge hoặc deploy.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/routes/*.py`, `app/models/*.py`, `app/services/*.py`, `tests/*.py`, `docs/code-review.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 6. `testing`
- **Before:** Chỉ liệt kê 4 tệp test cũ; thiếu `test_multi_agent.py` và `test_notifications_and_feedback.py`; không hướng dẫn lệnh chạy chuẩn.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; cập nhật đầy đủ 5 test suites (36 test cases); hướng dẫn lệnh chuẩn `python -m pytest -v`; bổ sung quy trình xử lý lỗi kiểm thử: `FAILURE → ROOT CAUSE → CLASSIFY → FIX → RE-RUN → VERIFY`.
- **Reason:** Giúp Agent tự chạy và đánh giá kết quả kiểm thử tự động một cách độc lập và chính xác.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `tests/conftest.py`, `tests/test_*.py`, `docs/test-plan.md`, `docs/test-report.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 7. `security-review`
- **Before:** Chỉ có checklist 10 điểm chung; thiếu hướng dẫn kiểm tra thuật toán băm mật khẩu PBKDF2, decorator `@role_required` và rate limiting.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; tích hợp đầy đủ chuẩn OWASP Top 10 Web và OWASP Top 10 for LLMs; gắn với `app/models/user.py`, `app/routes/auth.py`, `app/services/gemini_service.py`, `app/routes/checkin.py`.
- **Reason:** Đảm bảo hệ thống đạt chuẩn bảo mật doanh nghiệp, ngăn ngừa rò rỉ dữ liệu cá nhân (PII) và lạm dụng tài nguyên AI.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/routes/auth.py`, `app/routes/admin.py`, `app/routes/checkin.py`, `app/services/gemini_service.py`, `app/models/user.py`, `docs/security-review.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 8. `documentation`
- **Before:** Chứa 4 relative links bị lỗi do đóng ngoặc sai cú pháp (`docs/deployment.md`).`); thiếu quy chuẩn gắn nhãn trạng thái triển khai.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; sửa toàn bộ các broken links; bổ sung quy chuẩn 4 nhãn trạng thái (`IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, `PLANNED`, `DEPRECATED`); bổ sung quy trình đồng bộ Code ↔ Docs.
- **Reason:** Biến kho tài liệu thành Single Source of Truth đáng tin cậy cho toàn bộ đội ngũ và Agent.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** Toàn bộ tệp trong `docs/*.md`, `README.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 9. `question-analysis`
- **Before:** Chứa broken link `docs/question-analysis.md.`; thiếu liên kết với hàm mã nguồn thực tế `extract_question_intent`.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; sửa broken link; liên kết trực tiếp hàm `extract_question_intent` và `remove_accents`; phân loại rõ ràng 6 ý định chuẩn (`schedule`, `ticket`, `speaker`, `venue`, `faq`, `general`).
- **Reason:** Giúp Agent nắm bắt thuật toán phân loại ý định tiếng Việt có dấu/không dấu và xử lý câu hỏi mơ hồ.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/services/rag_service.py`, `app/services/gemini_service.py`, `tests/test_ai_services.py`, `docs/question-analysis.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 10. `event-retrieval`
- **Before:** Chỉ có mô tả câu truy vấn lý thuyết; không tham chiếu tới mã nguồn trong `app/services/rag_service.py` hay `database_service.py`.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; gắn kết trực tiếp với các hàm truy vấn thực tế; hướng dẫn sử dụng Parameterized Queries an toàn; xử lý trạng thái rỗng sạch sẽ (loại trừ `[object Object]` hay `null`).
- **Reason:** Đảm bảo Agent biết cách trích xuất dữ liệu có cấu trúc an toàn, phục vụ làm đầu vào cho Context Builder.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/services/rag_service.py`, `app/services/multi_agent/database_service.py`, `app/models/*.py`, `tests/test_ai_services.py`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 11. `context-builder`
- **Before:** Nội dung rất ngắn (1.9KB); hoàn toàn thiếu các ví dụ cấu trúc ngữ cảnh thực tế; không đề cập đến bảng `event_faqs`.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; gắn với hàm `build_rag_context` trong `app/services/rag_service.py`; thiết lập cấu trúc phân tầng Markdown chuẩn mực; bổ sung chỉ dẫn neo thực chứng chống ảo giác.
- **Reason:** Đảm bảo khối ngữ cảnh nạp vào LLM súc tích, đầy đủ dữ kiện sự thật, tối ưu hóa token và độ trễ.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/services/rag_service.py`, `app/agents/knowledge_agent.py`, `tests/test_ai_services.py`, `docs/chatbot-architecture.md`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

### 12. `rag-prompt`
- **Before:** Chứa broken path `app/prompts/.`; thiếu ranh giới giữa Prompt và Retrieval; chưa gắn với Dual-Engine AI Gateway.
- **After:** Nâng cấp cấu trúc chuẩn 16 mục; sửa đường dẫn chuẩn `app/prompts/chatbot_system.txt`; định hình cấu trúc 5 thành phần (Instructions, Context, Constraints, Few-shot Examples, Output Format); phòng vệ Prompt Injection.
- **Reason:** Cung cấp cẩm nang thiết kế prompt chuyên nghiệp, giúp LLM trả lời chuẩn xác và trình bày Markdown đẹp mắt.
- **GAP liên quan:** `GAP-003`.
- **Files referenced:** `app/prompts/*.txt`, `app/services/rag_service.py`, `app/services/gemini_service.py`, `tests/test_ai_services.py`.
- **Validation:** Đạt chuẩn 16 mục, 0 broken links.

---

## BẢNG NHẬT KÝ KHỞI TẠO 6 SKILLS MỚI TẠI PHASE 4

### 13. `frontend-development`
- **Capability:** Phát triển Giao diện Web (Frontend Web Development)
- **GAP liên quan:** `GAP-004`
- **Reason:** Dự án sở hữu 27 Jinja2 templates, hệ sinh thái Apple Design System với hơn 3,000 dòng CSS custom properties, Light/Dark/System theme toggle và các tương tác DOM phức tạp nhưng hoàn toàn chưa có Skill chuyên trách hướng dẫn Agent.
- **Related Existing Skills:** `requirements-analysis`, `implementation`, `responsive-mobile`, `api-development`, `testing`
- **Dependencies:** `requirements-analysis`, `implementation`
- **Files Created:** `.agents/skills/frontend-development/SKILL.md`
- **Source References:** `app/templates/base.html`, `app/templates/main/index.html`, `app/templates/main/events.html`, `app/templates/main/event_detail.html`, `app/templates/ai/chat_workspace.html`, `app/static/css/style.css`, `app/static/js/main.js`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước (READ -> ANALYZE -> PLAN -> MODIFY -> TEST -> VERIFY -> DOCUMENT), 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

---

### 14. `responsive-mobile`
- **Capability:** Giao diện Di động & Responsive (Responsive Mobile & Touch Interactions)
- **GAP liên quan:** `GAP-004`
- **Reason:** Ứng dụng yêu cầu tính tương thích cao trên thiết bị di động (320px–768px), điều khiển Apple Mobile Drawer, Apple iOS Bottom Nav, khóa cuộn trang `mobile-drawer-open`, xử lý z-index stacking context và tích hợp phần cứng Camera quét mã QR điểm danh qua `Html5Qrcode`.
- **Related Existing Skills:** `frontend-development`, `implementation`, `api-development`, `testing`
- **Dependencies:** `frontend-development`
- **Files Created:** `.agents/skills/responsive-mobile/SKILL.md`
- **Source References:** `app/static/css/style.css`, `app/static/js/main.js`, `app/templates/base.html`, `app/templates/checkin/index.html`, `app/templates/ai/chat_workspace.html`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước, 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

---

### 15. `api-development`
- **Capability:** Phát triển & Quản trị API (API Development & RESTful Contracts)
- **GAP liên quan:** `GAP-004`, `GAP-005`
- **Reason:** Hệ thống có 66 endpoints đăng ký trên 8 Blueprints nhưng thiếu quy chuẩn thống nhất về JSON Response Schema (`success`, `data`, `error`, `code`), mã trạng thái HTTP ngữ nghĩa, phân quyền RBAC và kiểm duyệt dữ liệu đầu vào.
- **Related Existing Skills:** `implementation`, `architecture-design`, `security-review`, `testing`, `frontend-development`
- **Dependencies:** `implementation`, `architecture-design`
- **Files Created:** `.agents/skills/api-development/SKILL.md`
- **Source References:** `app/routes/auth.py`, `app/routes/events.py`, `app/routes/tickets.py`, `app/routes/checkin.py`, `app/routes/admin.py`, `app/routes/ai.py`, `app/routes/notifications.py`, `app/routes/main.py`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước, 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

---

### 16. `ai-agent`
- **Capability:** Điều phối Đa tác tử (Multi-Agent Orchestration & Guardrails)
- **GAP liên quan:** `GAP-004`
- **Reason:** Hệ thống sở hữu kiến trúc Multi-Agent tân tiến với 7 tác tử chuyên trách (`Orchestrator`, `Requirement`, `Retrieval`, `Critic`, `Response`, `Knowledge`, `Recommendation`), trục truyền tin `MessageBus` và rào chắn `Critic Guardrail` nhưng thiếu Skill định nghĩa message protocol và vòng lặp phản hồi.
- **Related Existing Skills:** `question-analysis`, `event-retrieval`, `context-builder`, `rag-prompt`, `ai-evaluation`, `implementation`
- **Dependencies:** `implementation`, `rag-prompt`
- **Files Created:** `.agents/skills/ai-agent/SKILL.md`
- **Source References:** `app/agents/*.py`, `app/services/multi_agent/message_bus.py`, `app/services/multi_agent/agent_llm.py`, `app/services/multi_agent/database_service.py`, `app/services/multi_agent/vector_service.py`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước, 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

---

### 17. `ai-evaluation`
- **Capability:** Đánh giá & Benchmark AI (AI Evaluation & Benchmarking Framework)
- **GAP liên quan:** `GAP-004`
- **Reason:** Dự án đã xây dựng bộ kiểm thử thực nghiệm 10 ca chuẩn hóa (`TC-01` đến `TC-10`) so sánh Single-Agent vs Multi-Agent về Accuracy, Hallucination, Latency và LLM Calls nhưng chưa có cẩm nang hướng dẫn Agent đo lường và thẩm định kết quả.
- **Related Existing Skills:** `ai-agent`, `testing`, `rag-prompt`, `question-analysis`, `code-review`
- **Dependencies:** `testing`, `ai-agent`
- **Files Created:** `.agents/skills/ai-evaluation/SKILL.md`
- **Source References:** `app/services/multi_agent/benchmark_service.py`, `tests/test_multi_agent.py`, `app/agents/critic_agent.py`, `app/agents/orchestrator_agent.py`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước, 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

---

### 18. `deployment`
- **Capability:** Đóng gói & Triển khai Hệ thống (DevOps Deployment & Containerization)
- **GAP liên quan:** `GAP-004`, `GAP-009`
- **Reason:** Ứng dụng đã có Dockerfile, docker-compose.yml, Procfile và script seed.py nhưng thiếu Skill hướng dẫn Agent kiểm tra biến môi trường an toàn, tối ưu hóa layer caching, quản trị volumes bền vững và kiểm tra sức khỏe hệ thống.
- **Related Existing Skills:** `testing`, `security-review`, `database-design`, `implementation`, `documentation`
- **Dependencies:** `testing`, `security-review`
- **Files Created:** `.agents/skills/deployment/SKILL.md`
- **Source References:** `Dockerfile`, `docker-compose.yml`, `Procfile`, `requirements.txt`, `run.py`, `seed.py`, `app/config.py`
- **Validation:** Đạt chuẩn 20/20 mục tiêu chuẩn, quy trình 7 bước, 0 broken links (PASS).
- **Date / Status:** 2026-09-28 / **ACTIVE**

