# Hệ Thống Kỹ Năng Đa Tác Tử (18 AI Agent Skills Specification)

> **Dự Án:** EventAI Pro (Hệ Thống Quản Lý Sự Kiện Tích Hợp AI)  
> **Tổng Số Kỹ Năng Hoạt Động:** 18/18 Skills (100% Hoạt Động, 0 Broken Links)  
> **Trạng thái kiểm chứng:** Đạt 18/18 bài kiểm tra xác thực tự động (`docs/skill-validation-phase4.md`)  
> **Tài Liệu Tham Chiếu:** [skills-index.md](../../docs/skills-index.md), [skills-dependency-map.md](../../docs/skills-dependency-map.md), [skill-system-change-log.md](../../docs/skill-system-change-log.md)

---

## 1. Mục Đích & Nguyên Tắc Vận Hành Của Hệ Thống Kỹ Năng

Hệ thống kỹ năng (Skills System) tại thư mục `.agents/skills/` được thiết kế nhằm cung cấp hướng dẫn nghiệp vụ chuẩn mực cho AI Coding Assistant khi thao tác trực tiếp trên repository `Event_Management_AI`.

### Nguyên Tắc Tách Biệt Trách Nhiệm (Separation of Concerns):
- **Tài Liệu (`docs/`)**: Giải thích **CÁI GÌ** hệ thống đang có, cấu trúc hệ thống và cách hệ thống hoạt động.
- **Kỹ Năng (`.agents/skills/`)**: Hướng dẫn AI Agent **CÁCH THỨC** đọc mã nguồn, phân tích tác động, sửa đổi, kiểm thử và tài liệu hóa.

---

## 2. Quy Chuẩn Cấu Trúc Kỹ Năng (Standard 20-Section Contract)

Mỗi thư mục kỹ năng `.agents/skills/<skill-name>/` bắt buộc phải chứa tệp `SKILL.md` với phần Frontmatter YAML và tối thiểu 17 đến 20 mục nội dung chuẩn hóa:

1. **YAML Frontmatter**: `name`, `description` súc tích và điều kiện kích hoạt.
2. **Metadata & Status**: Phiên bản, ngày cập nhật, tác giả, trạng thái triển khai.
3. **Mục Đích & Phạm Vi**: Phạm vi áp dụng và giới hạn trách nhiệm.
4. **Trigger Conditions**: Điều kiện kích hoạt tự động khi nhận diện yêu cầu từ người dùng.
5. **Input / Output Specification**: Đầu vào và đầu ra kỳ vọng.
6. **Mã Nguồn Cốt Lõi (Core Source References)**: Đường dẫn chính xác đến các tệp mã nguồn liên quan.
7. **Tài Liệu Kỹ Thuật (Related Docs)**: Đường dẫn đến tài liệu kiến trúc/nghiệp vụ tương ứng trong `docs/`.
8. **Quy Trình 7 Bước Chuẩn (Standard 7-Step Workflow)**:
   - `BƯỚC 1: READ` (Đọc hiểu mã nguồn và tài liệu hiện hữu).
   - `BƯỚC 2: ANALYZE` (Phân tích khoảng cách, phụ thuộc và rủi ro tác động).
   - `BƯỚC 3: PLAN` (Lập kế hoạch thay đổi từng bước).
   - `BƯỚC 4: EXECUTE` (Thực thi chỉnh sửa chuẩn xác).
   - `BƯỚC 5: VERIFY` (Kiểm thử tự động và xác minh không tạo lỗi mới).
   - `BƯỚC 6: DOCUMENT` (Đồng bộ tài liệu kỹ thuật liên quan).
   - `BƯỚC 7: REPORT` (Báo cáo kết quả và minh chứng thực thi).
9. **Kịch Bản Sử Dụng Điển Hình (Concrete Use Cases)**: Ví dụ thực tế trong dự án.
10. **Quy Tắc An Toàn (Safety Rules & Anti-Patterns)**: Những điều nghiêm cấm (KHÔNG sửa bừa, KHÔNG tạo duplicate).
11. **Xử Lý Sự Cố (Failure Modes & Recovery)**: Hướng dẫn phục hồi khi lệnh hoặc kiểm thử thất bại.
12. **Ma Trận Phụ Thuộc (Dependency Matrix)**: Kỹ năng phụ thuộc trước và kỹ năng kế thừa phía sau.
13. **Tiêu Chuẩn Kiểm Thử (Verification Commands)**: Lệnh chạy kiểm thử hoặc kịch bản kiểm tra.
14. **Bảo Mật & Tuân Thủ (Security Checklist)**: Kiểm soát rủi ro an toàn thông tin.
15. **Nhật Ký Thay Đổi (Changelog)**: Lịch sử các phiên bản nâng cấp của kỹ năng.

---

## 3. Danh Mục 18 Kỹ Năng Chuyên Trách Theo Nhóm Nghiệp Vụ

### Nhóm 1: Kỹ Nghệ Phần Mềm & Kiến Trúc (5 Kỹ Năng)
1. **`requirements-analysis`**: Phân tích 4 điểm nghẽn, sinh User Stories, Acceptance Criteria, Human Gate 1.
2. **`architecture-design`**: Thiết kế kiến trúc 3 tầng, phân rã Component, DFD, Sequence và ADRs.
3. **`database-design`**: Chuẩn hóa CSDL 11 bảng 3NF, 13 B-Tree indexes, quan hệ PK-FK và `schema.sql`.
4. **`implementation`**: Lập trình có kỷ luật, đọc đặc tả, hiện thực hóa Flask Blueprints & Models.
5. **`deployment`**: Đóng gói, cấu hình môi trường Docker, docker-compose, Procfile Gunicorn.

### Nhóm 2: Giao Diện Người Dùng & Di Động (2 Kỹ Năng)
6. **`frontend-development`**: Phát triển giao diện Web Jinja2, hệ thống CSS tokens (Apple Design), JavaScript.
7. **`responsive-mobile`**: Tối ưu hóa giao diện di động, mobile drawer, bottom nav, touch swipe, QR scanner.

### Nhóm 3: Giao Diện Lập Trình Ứng Dụng (1 Kỹ Năng)
8. **`api-development`**: Thiết kế, chuẩn hóa và kiểm thử 66 RESTful endpoints, JSON Schema, RBAC.

### Nhóm 4: Trí Tuệ Nhân Tạo & Đa Tác Tử (6 Kỹ Năng)
9. **`ai-agent`**: Vận hành và mở rộng Hệ thống 7 Agent, MessageBus, Critic Guardrail.
10. **`ai-evaluation`**: Đánh giá chất lượng AI, thực thi benchmark 10 ca kiểm thử định lượng.
11. **`event-retrieval`**: Truy xuất dữ liệu có cấu trúc từ CSDL phục vụ RAG Grounded Context an toàn.
12. **`rag-prompt`**: Thiết kế Prompt 5 thành phần có quy tắc chống Hallucination.
13. **`context-builder`**: Định dạng và làm giàu Grounded Context chèn vào Prompt.
14. **`question-analysis`**: Phân tích ý định (Intent) và trích xuất thực thể từ câu hỏi Chatbot.

### Nhóm 5: Chất Lượng, An Ninh & Quản Trị Tri Thức (4 Kỹ Năng)
15. **`testing`**: Xây dựng chiến lược kiểm thử tự động, chạy 36 Pytests và xuất báo cáo.
16. **`code-review`**: Thẩm định chất lượng mã nguồn độc lập theo 8 tiêu chuẩn kỹ thuật.
17. **`security-review`**: Kiểm toán an ninh mạng OWASP Top 10 Web & OWASP Top 10 LLM.
18. **`documentation`**: Duy trì bộ tài liệu kỹ thuật trong `docs/` và Ma trận truy vết RTM.

---

## 4. Hướng Dẫn Sử Dụng Dành Cho AI Agent

Khi nhận một nhiệm vụ mới, AI Agent phải thực hiện:
1. Tra cứu tệp [docs/skills-index.md](../../docs/skills-index.md) để xác định Skill phù hợp nhất.
2. Đọc tệp `SKILL.md` của kỹ năng đó bằng công cụ `view_file`.
3. Tuân thủ tuần tự 7 bước trong quy trình thực thi của Skill.
4. Chạy kiểm thử tự động để xác nhận kết quả trước khi báo cáo hoàn thành.
