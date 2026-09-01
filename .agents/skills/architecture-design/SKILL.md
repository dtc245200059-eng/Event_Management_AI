---
name: architecture-design
description: Skill thiết kế kiến trúc hệ thống 3 tầng (3-Tier) tích hợp AI Service Layer, phân rã component, luồng dữ liệu DFD, sequence diagrams và tài liệu hóa quyết định kiến trúc ADR.
---

# Architecture Design Skill

## Objective
Chuyển hóa tài liệu yêu cầu nghiệp vụ đã được phê duyệt ở Human Gate 1 thành kiến trúc phần mềm mạch lạc, bền vững, phân tách trách nhiệm rõ ràng giữa Presentation - Business Logic - Data Access và AI Orchestration Service Layer.

## Inputs
Đọc các tài liệu requirements đã được phê duyệt:
- `docs/customer-requirement.md`
- `docs/requirements.md`
- `docs/user-stories.md`
- `docs/acceptance-criteria.md`

## Process / Workflow
1. **Lựa chọn Mô hình Kiến trúc (Architectural Pattern)**:
   - Mô hình 3-Tier kinh điển (Presentation Layer, Business Logic Layer, Data Access Layer) kết hợp AI Service Layer và Factory Application Pattern của Flask.
2. **Phân rã Components & Xác định Trách nhiệm**:
   - **Presentation Layer**: HTML5/CSS3 Glassmorphic UI, Jinja2 Server-side rendering, Vanilla JavaScript AJAX/Fetch API, Chart.js, HTML5-QRCode Scanner.
   - **Business Logic Layer**: EventService, TicketService (Transactions & Anti-overselling), CheckinService (Anti-duplicate validation), AuthService (RBAC Decorators & Password Hashing), SurveyService.
   - **AI Service Layer**: Question Analyzer, Event Retrieval Engine, Context Builder, RAG Prompt Engine, Gemini 2.0 Client, Offline Fallback Mock Engine, Content Generator Engine, Recommendation Engine (TF-IDF/Cosine), Predictive & Sentiment Analytics Engine.
   - **Data Access Layer**: SQLAlchemy ORM kết nối SQLite (môi trường phát triển/kiểm thử) và PostgreSQL/MySQL (môi trường sản xuất).
3. **Thiết lập Ranh giới An toàn Dữ liệu (Data Barrier)**:
   - AI Service tuyệt đối KHÔNG truy cập trực tiếp vào CSDL hoặc nhận chuỗi SQL thô từ phía Client.
   - Dữ liệu đi qua Business Layer -> Sanitization -> Parameterized Query -> Data Framing -> Context Injection -> LLM.
4. **Mô hình hóa Luồng Dữ liệu (DFD)**:
   - DFD Mức 0 (Context Diagram), DFD Mức 1 (System Decomposition) và DFD Mức 2 (AI RAG Pipeline).
5. **Thiết kế Sequence Diagrams**:
   - Sơ đồ tuần tự cho Đăng ký & Mua vé an toàn (Transactional Ticket Booking).
   - Sơ đồ tuần tự cho Quét mã QR Check-in thời gian thực.
   - Sơ đồ tuần tự cho AI RAG Assistant kèm cơ chế tự động chuyển đổi Offline Fallback.
6. **Ghi nhận Quyết định Kiến trúc (ADR - Architectural Decision Records)**:
   - ADR-001: Sử dụng Flask Framework và Blueprint Modular Pattern.
   - ADR-002: Lựa chọn CSDL Quan hệ chuẩn 3NF với SQLAlchemy ORM.
   - ADR-003: Kiến trúc RAG 4 bước (Analyze -> Retrieve -> Grounded Context -> Prompt) thay vì gửi toàn bộ CSDL.
   - ADR-004: Cơ chế Offline Fallback Mock Engine đảm bảo High Availability khi mất mạng hoặc API Key lỗi.
   - ADR-005: Sử dụng TF-IDF & Cosine Similarity cho Personalized Recommendations thay vì phụ thuộc Vector DB nặng nề.
   - ADR-006: Mã hóa vé SVG Vector QR độc lập, không dùng thư viện đám mây bên thứ ba.
   - ADR-007: Xác thực mật khẩu chuẩn PBKDF2 với Salt và phân quyền RBAC đa tầng.
   - ADR-008: Giao diện Glassmorphism CSS thuần tối ưu hiệu năng không dùng thư viện ngoài cồng kềnh.

## Rules & Constraints
- Không triển khai mã nguồn chi tiết trong pha này.
- Không tự ý thay đổi hoặc bỏ bớt các yêu cầu chức năng đã được phê duyệt.
- Mọi quyết định công nghệ quan trọng phải có Rationale (lý do & đánh giá trade-off).

## Outputs
Khởi tạo hoặc cập nhật các tài liệu:
- `docs/architecture.md`
- `docs/architecture-decisions.md`
- `docs/chatbot-architecture.md`
- `docs/chatbot-data-flow.md`

## Verification (Human Gate 2)
Người kiểm duyệt (Human Gatekeeper) kiểm tra và ký duyệt:
- [ ] 100% Functional Requirements (FR-01..08, FR-AI-01..04) được đáp ứng bởi ít nhất một Component kiến trúc.
- [ ] Ranh giới an toàn của AI Service được thiết lập rõ ràng, không để lộ dữ liệu nhạy cảm PII.
- [ ] Hồ sơ ADR giải trình đầy đủ lý do chọn công nghệ và đánh giá rủi ro.
- [ ] Sơ đồ DFD và Sequence Diagrams thể hiện đầy đủ các luồng xử lý chính.
- **Trạng thái**: [APPROVED / REJECTED]
