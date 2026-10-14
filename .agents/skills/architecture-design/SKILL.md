---
name: architecture-design
description: Skill thiết kế kiến trúc hệ thống 3 tầng (3-Tier) tích hợp Dual-Engine AI Service Layer, phân rã component, luồng dữ liệu DFD, sequence diagrams và tài liệu hóa quyết định kiến trúc ADR.
---

# Architecture Design Skill

## 1. Purpose

Skill này hướng dẫn AI Agent phân tích, thiết kế và duy trì kiến trúc kỹ thuật của hệ thống `EventAI Pro`. Đảm bảo hệ thống tuân thủ mô hình 3 Tầng Mở rộng (Extended 3-Tier Enterprise Architecture), phân định ranh giới rõ ràng giữa Tầng Giao diện (Presentation), Tầng Nghiệp vụ (Application/Business) và Tầng Dữ liệu (Data/Persistence), đồng thời tích hợp phân hệ Trí tuệ Nhân tạo Kép (Dual-Engine AI Gateway) và hệ thống Đa tác tử (Multi-Agent Ensemble).

## 2. Scope

- Thiết kế và phân rã các module theo mô hình Application Factory Pattern của Flask.
- Xác lập ranh giới (Boundaries), trách nhiệm (Responsibilities) và luồng phụ thuộc (Dependency Direction) của 8 Blueprints: `main`, `auth`, `events`, `tickets`, `checkin`, `admin`, `ai`, `notifications`.
- Thiết kế luồng dữ liệu (Data Flow Diagrams - DFD Level 0, Level 1) cho phân hệ Chatbot AI và Multi-Agent.
- Thiết kế Sequence Diagrams mô tả tương tác giữa người dùng, Controller, AI Service, LLM Gateway và CSDL.
- Tài liệu hóa các quyết định kiến trúc quan trọng thông qua Architecture Decision Records (ADR).
- Kiểm soát kiến trúc không bị xói mòn (Architecture Drift Detection).

## 3. Non-Scope

- Không đi sâu vào thiết kế chi tiết bảng CSDL và khóa ngoại (thuộc skill `database-design`).
- Không trực tiếp viết mã chi tiết logic hàm (thuộc skill `implementation` hoặc `frontend-development`).
- Không thực thi bộ test benchmark AI (thuộc skill `ai-evaluation`).

## 4. When to Use

- Khi thêm mới một phân hệ, Blueprint hoặc dịch vụ AI vào hệ thống.
- Khi cần tái cấu trúc (refactor) luồng dữ liệu giữa Frontend và Backend.
- Khi cần ghi nhận một quyết định kỹ thuật lớn (ADR) như chọn thư viện, thay đổi cơ chế caching, gateway AI.
- Khi thẩm định tính toàn vẹn của ranh giới các tầng trong hệ thống.

## 5. When NOT to Use

- Khi chỉ thay đổi giao diện CSS/HTML nhỏ không ảnh hưởng cấu trúc luồng dữ liệu (dùng `frontend-development`).
- Khi chỉ thực hiện truy vấn dữ liệu đơn lẻ (dùng `event-retrieval`).
- Khi viết các test case đơn vị (dùng `testing`).

## 6. Required Context

Agent cần nắm vững:

- Cấu trúc thư mục chuẩn của Flask: `app/__init__.py`, `app/routes/`, `app/models/`, `app/services/`, `app/agents/`.
- 8 Blueprints hiện có trong hệ thống và danh mục 66 endpoints.
- Cơ chế AI Gateway Kép: Google GenAI SDK (`gemini-2.0-flash` / `gemini-3.6-flash`) kết hợp Local Grounded Mock Engine khi không có API key.
- Phân hệ Multi-Agent với 7 tác tử: `Orchestrator`, `Requirement`, `Retrieval`, `Critic`, `Response`, `Knowledge`, `Recommendation` cùng Message Bus.
- Quy chuẩn đánh giá Human Gate 2 (Architecture Verification).

## 7. Source Files to Inspect

Trước khi thiết kế hoặc thay đổi kiến trúc, Agent PHẢI kiểm tra các tệp sau:

- [app/__init__.py](file:///d:/Event_Management_AI/app/__init__.py): Khởi tạo Application Factory, đăng ký extensions và 8 Blueprints.
- [app/config.py](file:///d:/Event_Management_AI/app/config.py): Cấu hình môi trường, database URI, Gemini model, rate limits.
- [app/extensions.py](file:///d:/Event_Management_AI/app/extensions.py): Định nghĩa `db`, `login_manager`, hàm `utc_now()`.
- [app/routes/](file:///d:/Event_Management_AI/app/routes/): 8 tệp blueprint controllers định tuyến request.
- [app/services/gemini_service.py](file:///d:/Event_Management_AI/app/services/gemini_service.py): AI Gateway và bộ quản lý rate limit.
- [app/services/rag_service.py](file:///d:/Event_Management_AI/app/services/rag_service.py): Dịch vụ RAG hỏi đáp sự kiện.
- [app/agents/orchestrator_agent.py](file:///d:/Event_Management_AI/app/agents/orchestrator_agent.py): Điều phối Multi-Agent Pipeline.
- [app/models/](file:///d:/Event_Management_AI/app/models/): 11 thực thể dữ liệu quan hệ.

## 8. Related Documentation

- [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md): Tài liệu kiến trúc hệ thống chính thức.
- [docs/architecture-decisions.md](file:///d:/Event_Management_AI/docs/architecture-decisions.md): Danh mục các bản ghi ADR.
- [docs/chatbot-architecture.md](file:///d:/Event_Management_AI/docs/chatbot-architecture.md): Kiến trúc phân hệ Chatbot RAG.
- [docs/chatbot-data-flow.md](file:///d:/Event_Management_AI/docs/chatbot-data-flow.md): Sơ đồ luồng dữ liệu DFD.
- [docs/multi-agent-architecture.md](file:///d:/Event_Management_AI/docs/multi-agent-architecture.md): Kiến trúc hệ thống Đa tác tử.
- [docs/architecture-gap-analysis.md](file:///d:/Event_Management_AI/docs/architecture-gap-analysis.md): Báo cáo phân tích khoảng cách kiến trúc.

## 9. Related Skills

- `requirements-analysis`: Nhận yêu cầu đầu vào từ SRS.
- `database-design`: Phối hợp thiết kế tầng dữ liệu phù hợp kiến trúc.
- `implementation`: Chuyển giao thiết kế thành mã nguồn thực thi.
- `api-development`: Đồng bộ hợp đồng giao tiếp giữa các tầng.
- `documentation`: Cập nhật tài liệu kiến trúc và sơ đồ Mermaid.

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Kiểm tra hiện trạng kiến trúc)

1. Đọc [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md) và [docs/architecture-decisions.md](file:///d:/Event_Management_AI/docs/architecture-decisions.md).
2. Đọc mã nguồn [app/__init__.py](file:///d:/Event_Management_AI/app/__init__.py) để nắm bắt các Blueprints và cấu hình khởi tạo.
3. Rà soát [app/routes/](file:///d:/Event_Management_AI/app/routes/) để kiểm tra sự phân chia trách nhiệm hiện tại của các controllers.

### Bước 2: ANALYZE (Phân tích ranh giới và luồng dữ liệu)

1. **Kiểm tra tính đơn nhiệm (Separation of Concerns)**:
   - Presentation: Chỉ render HTML Jinja2 hoặc trả JSON response; KHÔNG chứa logic nghiệp vụ phức tạp.
   - Application/Service: Thực thi nghiệp vụ, gọi AI Gateway, đóng gói context; KHÔNG trực tiếp truy xuất `request.form` hay render HTML.
   - Data Layer: ORM Models quản lý trạng thái, validation thuộc tính; KHÔNG gọi API bên ngoài.
2. **Kiểm tra luồng phụ thuộc (Dependency Direction)**:
   - Chiều phụ thuộc bắt buộc: `Presentation → Business/Services → Data Layer`.
   - Tuyệt đối không cho phép Data Layer phụ thuộc ngược lên Presentation Layer.
3. **Phát hiện Architecture Drift**: Kiểm tra xem có route nào tự ý gọi trực tiếp LLM mà bỏ qua `gemini_service.py` hoặc tự ý viết SQL thô không an toàn hay không.

### Bước 3: PLAN (Thiết kế giải pháp kiến trúc)

1. Xác định vị trí của thành phần mới (Thuộc Blueprint nào, Service nào).
2. Vẽ sơ đồ luồng dữ liệu DFD (Context level, Level 1) bằng cú pháp Mermaid.
3. Vẽ Sequence Diagram thể hiện tương tác đồng bộ/bất đồng bộ.
4. Soạn thảo bản ghi ADR (Architectural Decision Record) gồm: Bối cảnh (Context), Quyết định (Decision), Hệ quả (Consequences).

### Bước 4: MODIFY (Tài liệu hóa kiến trúc)

1. Cập nhật sơ đồ và mô tả thành phần vào [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md).
2. Thêm bản ghi quyết định mới vào [docs/architecture-decisions.md](file:///d:/Event_Management_AI/docs/architecture-decisions.md).
3. Nếu liên quan đến phân hệ AI, cập nhật tương ứng trong [docs/chatbot-architecture.md](file:///d:/Event_Management_AI/docs/chatbot-architecture.md) hoặc [docs/multi-agent-architecture.md](file:///d:/Event_Management_AI/docs/multi-agent-architecture.md).

### Bước 5: VERIFY (Kiểm chứng Human Gate 2)

1. Kiểm tra tính đóng kín và khả năng kiểm thử (Testability) của thiết kế.
2. Xác nhận tính tương thích với cơ chế Dual-Engine AI (không bị crash khi offline).
3. Đảm bảo tuân thủ nguyên tắc "Minimal Necessary Change" (không thiết kế quá mức cần thiết).

## 11. Validation

Agent phải kiểm tra các tiêu chí sau:

- [ ] Không có circular import giữa các Blueprints và Services.
- [ ] Ranh giới giữa Single-Agent RAG và Multi-Agent Pipeline được phân định rành mạch.
- [ ] Mọi quyết định kỹ thuật quan trọng đều có ADR tương ứng.
- [ ] Toàn bộ sơ đồ Mermaid hiển thị chính xác cú pháp, không bị lỗi render.

## 12. Failure Handling

- **Khi phát hiện circular dependency**: Tách phần phụ thuộc dùng chung vào `app/extensions.py` hoặc tạo module service con độc lập.
- **Khi dịch vụ AI bên ngoài gặp sự cố**: Luôn đảm bảo kiến trúc có cơ chế Fallback sang Local Grounded Mock Engine để hệ thống không bao giờ bị dừng hoạt động.

## 13. Security Considerations

- Tầng Presentation phải có cơ chế lọc CSRF và sanitization input.
- Tầng AI Service phải tích hợp Rate Limiting và cơ chế lọc thông tin nhạy cảm (PII sanitization) trước khi gửi prompt tới LLM.
- Các secret key (`SECRET_KEY`, `GEMINI_API_KEY`) phải được nạp qua biến môi trường thông qua `app/config.py`, không bao giờ hardcode trong mã nguồn.

## 14. Expected Output

1. Bản cập nhật tài liệu kiến trúc [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md).
2. Bản ghi quyết định kiến trúc mới trong [docs/architecture-decisions.md](file:///d:/Event_Management_AI/docs/architecture-decisions.md).
3. Sơ đồ Mermaid mô tả luồng thành phần và tuần tự tương tác.

## 15. Completion Criteria

- Thiết kế kiến trúc giải quyết trọn vẹn yêu cầu từ SRS mà không phá vỡ mô hình 3 tầng hiện tại.
- Được xác nhận đạt chuẩn qua Human Gate 2 (Architecture Approval).
- Cung cấp đầy đủ ranh giới và hợp đồng cho `database-design` và `implementation`.

## 16. Maintenance Notes

- Cập nhật skill này khi dự án chuyển đổi mô hình lưu trữ (ví dụ từ SQLite sang PostgreSQL) hoặc mở rộng thêm cụm microservices.
- Rà soát định kỳ tính khớp nối giữa sơ đồ kiến trúc và các routes thực tế trong `app.url_map`.
