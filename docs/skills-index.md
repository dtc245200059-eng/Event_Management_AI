# BẢNG CHỈ MỤC KỸ NĂNG CỦA AI AGENT (SKILLS INDEX)

**Dự án:** EventAI Pro (`Event_Management_AI`)  
**Mục tiêu:** Cung cấp danh mục tra cứu tập trung toàn bộ 18 kỹ năng (Skills) của AI Agent, trạng thái hoạt động, mục đích, điều kiện kích hoạt, quan hệ phụ thuộc và khoảng cách nghiệp vụ (GAPs) đã được giải quyết.

---

## BẢNG CHỈ MỤC KỸ NĂNG CHÍNH THỨC (OFFICIAL SKILLS INDEX)

| STT | Skill | Status | Purpose | Trigger | Dependencies | Related GAPs |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: |
| 1 | `requirements-analysis` | **ACTIVE** | Phân tích yêu cầu khách hàng, chuẩn hóa SRS, User Stories, Acceptance Criteria và Human Gate 1 | Khi có tính năng mới, Change Request hoặc yêu cầu từ khách hàng | None | `GAP-003` |
| 2 | `question-analysis` | **ACTIVE** | Phân tích ý định (Intent) và trích xuất thực thể từ câu hỏi ngôn ngữ tự nhiên | Khi nhận tin nhắn người dùng tại `/ai/chat` hoặc giao diện chat | None | `GAP-003` |
| 3 | `context-builder` | **ACTIVE** | Đóng gói dữ liệu CSDL thành khối Grounded Context súc tích, chống ảo giác | Trong pipeline RAG trước khi ghép vào prompt template | `event-retrieval`, `question-analysis` | `GAP-003` |
| 4 | `architecture-design` | **ACTIVE** | Thiết kế kiến trúc 3 tầng, phân rã Blueprints, luồng dữ liệu DFD và quyết định ADR | Khi bổ sung phân hệ, module mới hoặc thay đổi luồng dữ liệu | `requirements-analysis` | `GAP-003` |
| 5 | `database-design` | **ACTIVE** | Thiết kế CSDL quan hệ 3NF, DDL schema, ORM models, indexes và ràng buộc toàn vẹn | Khi thêm thực thể, thêm bảng, đổi cột dữ liệu CSDL | `requirements-analysis`, `architecture-design` | `GAP-003` |
| 6 | `implementation` | **ACTIVE** | Lập trình logic nghiệp vụ Blueprints, Models, Services có kỷ luật và kiểm thử tự động | Khi phát triển tính năng mới, sửa lỗi logic backend | `architecture-design`, `database-design` | `GAP-003` |
| 7 | `event-retrieval` | **ACTIVE** | Truy xuất dữ liệu có cấu trúc từ CSDL bằng Parameterized Queries an toàn | Trong RAG pipeline khi cần lấy dữ liệu sự kiện, vé, lịch trình | `database-design`, `question-analysis` | `GAP-003` |
| 8 | `rag-prompt` | **ACTIVE** | Thiết kế System Prompt và User Prompt 5 thành phần chống Hallucination cho LLM | Khi tối ưu chất lượng trả lời AI, thêm prompt sinh nội dung | `context-builder`, `question-analysis` | `GAP-003` |
| 9 | `testing` | **ACTIVE** | Thiết kế và thực thi kiểm thử tự động (Pytest), ngăn ngừa lỗi hồi quy | Sau mỗi lần sửa code, thêm tính năng mới hoặc pre-release | `implementation` | `GAP-003` |
| 10 | `code-review` | **ACTIVE** | Thẩm định chất lượng mã nguồn độc lập theo 8 tiêu chuẩn và 4 cấp độ rủi ro | Trước khi merge code, sau khi implementation hoàn thành | `implementation`, `architecture-design` | `GAP-003` |
| 11 | `security-review` | **ACTIVE** | Kiểm toán bảo mật theo chuẩn OWASP Top 10 Web và OWASP Top 10 for LLMs | Khi thay đổi logic xác thực, phân quyền RBAC, trước khi deploy | `implementation`, `architecture-design` | `GAP-003` |
| 12 | `documentation` | **ACTIVE** | Tổng hợp và duy trì hệ sinh thái tài liệu kỹ thuật đồng bộ 100% với mã nguồn | Sau mỗi thay đổi về code, schema, API, test cases | Tất cả các kỹ năng | `GAP-003`, `GAP-008` |
| 13 | `frontend-development` | **ACTIVE** | Quản lý Jinja2 templates, CSS tokens, Apple Design system, Dark/Light theme | Khi phát triển hoặc điều chỉnh giao diện Web | `requirements-analysis`, `implementation` | `GAP-004` |
| 14 | `responsive-mobile` | **ACTIVE** | Tối ưu giao diện di động (320px–768px), drawer menu, touch events, camera QR | Khi xử lý màn hình di động, máy tính bảng, camera QR | `frontend-development` | `GAP-004` |
| 15 | `api-development` | **ACTIVE** | Thiết kế, chuẩn hóa và kiểm thử 66 RESTful endpoints, JSON schema đồng nhất | Khi tạo mới, sửa đổi endpoint hoặc cấu trúc dữ liệu API | `implementation`, `architecture-design` | `GAP-004`, `GAP-005` |
| 16 | `ai-agent` | **ACTIVE** | Điều phối hệ thống 7 tác tử, MessageBus audit log, Critic guardrail | Khi vận hành hoặc mở rộng luồng tư vấn đa tác tử | `implementation`, `rag-prompt` | `GAP-004` |
| 17 | `ai-evaluation` | **ACTIVE** | Thực thi và so sánh 10 ca kiểm thử thực nghiệm benchmark Single vs Multi-Agent | Khi đo lường độ trễ, token usage, độ chính xác AI | `testing`, `ai-agent` | `GAP-004` |
| 18 | `deployment` | **ACTIVE** | Đóng gói Docker, docker-compose, Procfile, biến môi trường, seed CSDL | Khi chuẩn bị môi trường chạy thử nghiệm hoặc đưa lên production | `testing`, `security-review` | `GAP-004`, `GAP-009` |

---

## NGUYÊN TẮC QUẢN TRỊ KỸ NĂNG:
1. **Duy nhất một trách nhiệm (Single Responsibility):** Mỗi kỹ năng phụ trách một năng lực chuyên biệt, không có kỹ năng nào bị trùng lặp trách nhiệm.
2. **Khả thi thực tế (Actionable):** 100% kỹ năng đang `ACTIVE` đều tuân thủ cấu trúc chuẩn (16-20 mục) và cung cấp quy trình hành động tuần tự (`READ → ANALYZE → PLAN → MODIFY → TEST → VERIFY → DOCUMENT`).
3. **Độ bao phủ tuyệt đối:** Toàn bộ 18 kỹ năng đã được kiểm chứng tự động đạt chuẩn 100% và sẵn sàng vận hành.
