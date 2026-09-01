---
name: database-design
description: Skill thiết kế mô hình dữ liệu quan hệ (ERD), chuẩn hóa 3NF, xác lập khóa chính/khóa ngoại PK-FK, ràng buộc toàn vẹn, đánh index và sinh mã SQL Schema DDL.
---

# Database Design Skill

## Objective
Thiết kế cấu trúc cơ sở dữ liệu quan hệ đạt chuẩn dạng chuẩn 3 (3NF) gồm 9 bảng thực thể, đảm bảo tính toàn vẹn dữ liệu, triệt tiêu các dị thường dữ liệu (anomalies), hỗ trợ các giao dịch ACID an toàn khi đặt vé và tối ưu hóa hiệu năng truy vấn cho AI RAG Retriever.

## Inputs
Đọc các tài liệu requirements và architecture đã được phê duyệt:
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/user-stories.md`

## Process / Workflow
1. **Trích xuất Thực thể (Entities Extraction)**:
   - 9 thực thể chính: `users`, `attendees`, `events`, `speakers`, `venues`, `schedules`, `tickets`, `registrations`, `ai_chat_history`.
2. **Xác định Mối quan hệ & Lực lượng (Cardinality & Relationships)**:
   - `users (1) ── (1) attendees`
   - `events (1) ── (N) schedules`
   - `events (1) ── (N) tickets`
   - `events (1) ── (N) registrations`
   - `speakers (1) ── (N) schedules`
   - `venues (1) ── (N) schedules`
   - `tickets (1) ── (N) registrations`
   - `attendees (1) ── (N) registrations`
   - `users (1) ── (N) ai_chat_history`
3. **Chuẩn hóa Dữ liệu theo 3 Dạng Chuẩn (Normalization to 3NF)**:
   - **1NF**: Mọi thuộc tính là nguyên tử (Atomic), mỗi bảng có Khóa chính (Primary Key) xác định duy nhất từng bản ghi.
   - **2NF**: Đạt 1NF và mọi thuộc tính không khóa phụ thuộc hàm đầy đủ vào toàn bộ Khóa chính (loại bỏ phụ thuộc từng phần).
   - **3NF**: Đạt 2NF và không có thuộc tính không khóa nào phụ thuộc bắc cầu vào Khóa chính (loại bỏ phụ thuộc bắc cầu).
4. **Thiết lập Ràng buộc Toàn vẹn (Constraints & Business Rules)**:
   - Khóa chính (PK): `id INTEGER PRIMARY KEY AUTOINCREMENT`.
   - Khóa ngoại (FK) kèm hành vi tham chiếu (`ON DELETE CASCADE`, `ON DELETE SET NULL`, `ON DELETE RESTRICT`).
   - Ràng buộc duy nhất (UNIQUE): `users(username)`, `users(email)`, `events(event_code)`, `tickets(ticket_code)`, `registrations(registration_code)`, `registrations(ticket_number)`, `registrations(event_id, attendee_id)`.
   - Ràng buộc NOT NULL và Default values.
5. **Chiến lược Đánh Chỉ mục (Index Strategy)**:
   - Index trên các trường lọc và tìm kiếm thường xuyên: `events(event_code)`, `events(category)`, `events(status)`, `tickets(ticket_code)`, `registrations(ticket_number)`, `registrations(checked_in)`.
6. **Xây dựng Data Dictionary (Từ điển Dữ liệu 9 Bảng)**.
7. **Sinh mã DDL SQL Schema (`database/schema.sql`)**.

## Rules & Constraints
- Không viết code Flask Route trong pha này.
- Mọi bảng bắt buộc phải có timestamp (`created_at`, `updated_at`).
- Bảng `registrations` bắt buộc phải có ràng buộc chống đăng ký trùng lặp trên cặp `(event_id, attendee_id)`.
- Mật khẩu trong bảng `users` luôn lưu dạng chuỗi băm (hash), không bao giờ lưu plain-text.

## Outputs
Khởi tạo hoặc cập nhật các tài liệu:
- `docs/database-design.md`
- `database/schema.sql`

## Verification (Human Gate 3)
Người kiểm duyệt (Human Gatekeeper) kiểm tra và ký duyệt:
- [ ] Tất cả 9 bảng đều đạt chuẩn 3NF không vi phạm dị thường thêm/xóa/sửa.
- [ ] Khóa ngoại PK-FK được định nghĩa đầy đủ với kiểu dữ liệu tương thích.
- [ ] Ràng buộc UNIQUE trên `ticket_number` và `(event_id, attendee_id)` đã được kích hoạt.
- [ ] Tệp `database/schema.sql` thực thi thành công không có lỗi cú pháp.
- **Trạng thái**: [APPROVED / REJECTED]
