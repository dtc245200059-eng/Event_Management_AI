---
name: requirements-analysis
description: Skill chuyên môn hóa quy trình phân tích yêu cầu phần mềm, trích xuất điểm nghẽn nghiệp vụ, xây dựng User Stories, Acceptance Criteria, phát hiện mơ hồ và kiểm chứng chống Hallucination theo chuẩn AI-Augmented SDLC.
---

# Requirements Analysis Skill

## 1. Purpose

Skill này hướng dẫn AI Agent tiếp nhận, bóc tách và chuẩn hóa yêu cầu phần mềm từ khách hàng (Customer Requirements) thành tài liệu đặc tả yêu cầu kỹ thuật (SRS), User Stories và Tiêu chí chấp nhận (Acceptance Criteria - AC). Mục tiêu là triệt tiêu sự mơ hồ, phát hiện mâu thuẫn nghiệp vụ và ngăn ngừa ảo giác (Hallucination) ngay tại cửa ngõ đầu vào của dự án (Human Gate 1).

## 2. Scope

- Tiếp nhận và phân tích tài liệu yêu cầu khách hàng (`docs/customer-requirement.md`).
- Chuẩn hóa yêu cầu thành Functional Requirements (FR), Non-Functional Requirements (NFR), Business Rules (BR), Security Rules (SEC) và Data Requirements (DR).
- Xây dựng User Stories theo định dạng Agile (`As a... I want to... So that...`) và AC theo chuẩn Gherkin (`Given... When... Then...`).
- Phát hiện các yêu cầu mơ hồ, mâu thuẫn, thiếu tính khả thi kỹ thuật và ghi nhận vào `docs/requirements-issues.md`.
- Duy trì tính truy vết (Traceability) từ Yêu cầu đến Thiết kế và Kiểm thử.

## 3. Non-Scope

- Không trực tiếp thiết kế kiến trúc hệ thống (thuộc skill `architecture-design`).
- Không thiết kế mô hình cơ sở dữ liệu quan hệ (thuộc skill `database-design`).
- Không viết mã nguồn backend/frontend (thuộc skill `implementation` và `frontend-development`).

## 4. When to Use

- Khi nhận được yêu cầu mới, tính năng mới hoặc thay đổi nghiệp vụ (CR - Change Request).
- Khi rà soát lại tính đầy đủ của tài liệu yêu cầu so với mã nguồn thực tế.
- Khi chuẩn bị bàn giao tài liệu cho giai đoạn thiết kế kiến trúc và CSDL.

## 5. When NOT to Use

- Khi nhiệm vụ chỉ là sửa lỗi cú pháp code nhỏ (Bug fix cục bộ) không làm thay đổi luồng nghiệp vụ.
- Khi thực hiện kiểm thử tự động (sử dụng skill `testing`).
- Khi tiến hành đánh giá mã nguồn tĩnh (sử dụng skill `code-review`).

## 6. Required Context

Agent cần nắm vững:

- Lĩnh vực nghiệp vụ: Quản lý sự kiện thông minh, đăng ký vé, điểm danh QR Code và tư vấn AI.
- 4 vai trò người dùng trong hệ thống: `admin`, `organizer`, `staff`, `attendee`.
- Cấu trúc hệ thống 3 tầng kết hợp AI Service Layer của dự án `EventAI Pro`.
- Quy chế cổng kiểm soát chất lượng con người (Human Gate 1: Requirements Verification).

## 7. Source Files to Inspect

Trước khi phân tích yêu cầu, Agent PHẢI đọc các tệp sau:

- [docs/customer-requirement.md](file:///d:/Event_Management_AI/docs/customer-requirement.md): Yêu cầu thô ban đầu từ khách hàng.
- [docs/requirements.md](file:///d:/Event_Management_AI/docs/requirements.md): Bản đặc tả yêu cầu phần mềm chính thức (SRS).
- [docs/user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md): Danh mục User Stories hiện tại.
- [docs/acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md): Tiêu chí chấp nhận đã định nghĩa.
- [docs/requirements-issues.md](file:///d:/Event_Management_AI/docs/requirements-issues.md): Sổ theo dõi điểm mơ hồ và mâu thuẫn yêu cầu.
- [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md): Ma trận truy vết yêu cầu.

## 8. Related Documentation

- [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md): Kiến trúc hệ thống tổng thể.
- [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md): Mô hình thực thể dữ liệu.
- [docs/api.md](file:///d:/Event_Management_AI/docs/api.md): Hợp đồng giao tiếp API.

## 9. Related Skills

- `question-analysis`: Phân tích ý định câu hỏi người dùng tự nhiên.
- `context-builder`: Đóng gói ngữ cảnh yêu cầu phục vụ thiết kế.
- `architecture-design`: Chuyển hóa yêu cầu thành thiết kế thành phần.
- `database-design`: Chuyển hóa yêu cầu dữ liệu thành mô hình 3NF.
- `documentation`: Cập nhật hệ thống tài liệu SRS và User Stories.

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Đọc tài liệu đầu vào)

1. Đọc kỹ tài liệu yêu cầu thô từ khách hàng [docs/customer-requirement.md](file:///d:/Event_Management_AI/docs/customer-requirement.md).
2. Đọc [docs/requirements.md](file:///d:/Event_Management_AI/docs/requirements.md) để xác định các yêu cầu đã được chuẩn hóa trước đó.
3. Rà soát [docs/requirements-issues.md](file:///d:/Event_Management_AI/docs/requirements-issues.md) để nắm bắt các vấn đề còn tồn đọng.

### Bước 2: ANALYZE (Phân tích chuyên sâu)

1. **Phân loại yêu cầu**: Tách biệt rõ ràng Functional (FR), Non-Functional (NFR), Business Rules (BR) và Security (SEC).
2. **Kiểm tra tính mơ hồ (Ambiguity Check)**:
   - Các từ ngữ định tính: "nhanh", "đẹp", "dễ dùng", "tối ưu" phải được lượng hóa (ví dụ: thời gian phản hồi API < 500ms, độ trễ AI < 2.5s).
   - Kiểm tra các trường hợp biên: Quota vé bằng 0, huỷ vé khi đã thanh toán, điểm danh trùng mã QR, người dùng không nhập tin nhắn chat.
3. **Phát hiện mâu thuẫn**: Đối chiếu yêu cầu mới với các quy tắc nghiệp vụ đã có (ví dụ: BR-04 không cho phép check-in 2 lần với 1 mã vé).
4. Nếu phát hiện yêu cầu không rõ ràng hoặc thiếu thông tin: Đánh dấu rõ ràng là `UNRESOLVED REQUIREMENT` kèm bằng chứng và tác động, tuyệt đối KHÔNG tự suy đoán.

### Bước 3: PLAN (Lập kế hoạch thay đổi)

1. Gán mã định danh ổn định duy nhất (ID): `FR-xx`, `NFR-xx`, `BR-xx`, `SEC-xx`.
2. Soạn thảo User Story tương ứng (`US-xxx`): Xác định Actor, Mục tiêu và Giá trị mang lại.
3. Soạn thảo Tiêu chí chấp nhận (`AC-xxx`) theo chuẩn Gherkin:

   ```gherkin
   Scenario: [Tên kịch bản kiểm thử]
     Given [Tiền điều kiện hệ thống]
     When [Hành động người dùng thực hiện]
     Then [Kết quả mong đợi của hệ thống]
   ```

4. Xác định module mã nguồn và bảng CSDL sẽ chịu ảnh hưởng.

### Bước 4: MODIFY (Cập nhật tài liệu đặc tả)

1. Cập nhật yêu cầu mới vào [docs/requirements.md](file:///d:/Event_Management_AI/docs/requirements.md).
2. Bổ sung User Story vào [docs/user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md).
3. Bổ sung Acceptance Criteria vào [docs/acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md).
4. Ghi nhận các vấn đề phát hiện vào [docs/requirements-issues.md](file:///d:/Event_Management_AI/docs/requirements-issues.md).
5. Cập nhật ma trận truy vết trong [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md).

### Bước 5: VERIFY (Kiểm chứng Human Gate 1)

1. Kiểm tra tính nhất quán chéo giữa SRS, User Story và AC.
2. Kiểm tra không có ID yêu cầu nào bị trùng lặp.
3. Xác nhận tiêu chuẩn SMART (Specific, Measurable, Achievable, Relevant, Time-bound) cho mọi NFR.

## 11. Validation

Agent phải kiểm tra các tiêu chí sau để đánh giá chất lượng tài liệu yêu cầu:

- [ ] 100% yêu cầu chức năng có ID duy nhất (`FR-xx`).
- [ ] 100% User Stories có Acceptance Criteria cụ thể theo cú pháp Gherkin.
- [ ] Mọi quy tắc nghiệp vụ (Business Rules) đều có cơ chế kiểm chứng.
- [ ] Không còn thuật ngữ mơ hồ chưa được định nghĩa.
- [ ] Ma trận truy vết `traceability-matrix.md` được cập nhật đồng bộ.

## 12. Failure Handling

- **Khi yêu cầu bị mâu thuẫn**: Tạo bản ghi xung đột trong `docs/requirements-issues.md`, nêu rõ Source A vs Source B, tạm dừng chuyển sang thiết kế cho đến khi có xác nhận.
- **Khi yêu cầu vượt quá khả năng công nghệ của stack**: Đề xuất giải pháp thay thế dựa trên kiến trúc hiện tại (ví dụ: thay vì full vector database độc lập, dùng SQLite Full-Text / TF-IDF Cosine Similarity tích hợp).

## 13. Security Considerations

- Mọi yêu cầu liên quan đến tài khoản người dùng, mật khẩu, phân quyền phải tuân thủ chuẩn RBAC 4 vai trò.
- Dữ liệu định danh cá nhân (PII) như email, số điện thoại, mật khẩu phải có yêu cầu mã hóa hoặc che giấu (sanitization) trước khi xử lý qua AI.

## 14. Expected Output

1. Bản cập nhật [docs/requirements.md](file:///d:/Event_Management_AI/docs/requirements.md) với các yêu cầu chuẩn hóa.
2. Bản cập nhật [docs/user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md) và [docs/acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md).
3. Biên bản ghi nhận vấn đề yêu cầu [docs/requirements-issues.md](file:///d:/Event_Management_AI/docs/requirements-issues.md).
4. Ma trận truy vết cập nhật [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md).

## 15. Completion Criteria

- Toàn bộ yêu cầu đầu vào được phân rã thành ID chuẩn.
- Đạt tiêu chuẩn nghiệm thu Human Gate 1 (Ký duyệt yêu cầu không còn mơ hồ).
- Đủ thông tin đầu vào cho skill `architecture-design` và `database-design`.

## 16. Maintenance Notes

- Cập nhật skill này khi quy trình thẩm định yêu cầu bổ sung thêm vai trò hoặc chuẩn tài liệu mới.
- Rà soát định kỳ mỗi khi có phiên bản lớn (Major Release) của sản phẩm.
