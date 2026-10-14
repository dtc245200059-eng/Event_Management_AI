---
name: database-design
description: Skill thiết kế mô hình dữ liệu quan hệ (ERD), chuẩn hóa 3NF, xác lập khóa chính/khóa ngoại PK-FK, ràng buộc toàn vẹn, đánh index và sinh mã SQL Schema DDL đồng bộ với SQLAlchemy ORM Models.
---

# Database Design Skill

## 1. Purpose

Skill này hướng dẫn AI Agent phân tích, thiết kế, chuẩn hóa và duy trì mô hình cơ sở dữ liệu quan hệ của hệ thống `EventAI Pro`. Đảm bảo toàn bộ 11 bảng dữ liệu tuân thủ chuẩn 3NF (Third Normal Form), toàn vẹn tham chiếu (Referential Integrity), ràng buộc khóa ngoại (Foreign Keys), xóa xếp tầng (Cascade Deletes), và đánh chỉ mục B-Tree tối ưu hiệu năng truy vấn cho cả tác vụ CRUD và truy xuất RAG Grounded Context.

## 2. Scope

- Thiết kế sơ đồ quan hệ thực thể (ERD) bằng cú pháp Mermaid.
- Chuẩn hóa các bảng dữ liệu đạt chuẩn 3NF (không phụ thuộc bắc cầu, không lặp nhóm thuộc tính).
- Định nghĩa chi tiết thuộc tính, kiểu dữ liệu, ràng buộc (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `DEFAULT`, `CHECK`).
- Đánh chỉ mục (Indexes) trên các trường lọc thường xuyên (`event_id`, `attendee_id`, `status`, `start_date`, `created_at`).
- Đồng bộ tuyệt đối hai chiều giữa:
  - Bản đặc tả thiết kế [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md).
  - Tệp định nghĩa DDL [database/schema.sql](file:///d:/Event_Management_AI/database/schema.sql).
  - Các lớp mô hình ORM trong [app/models/](file:///d:/Event_Management_AI/app/models/).
  - Dữ liệu mẫu khởi tạo trong [seed.py](file:///d:/Event_Management_AI/seed.py).
- Kiểm soát an toàn di chuyển dữ liệu (Migration Safety).

## 3. Non-Scope

- Không trực tiếp viết các câu truy vấn nghiệp vụ trong route/service (thuộc skill `event-retrieval` hoặc `implementation`).
- Không cấu hình sao lưu vật lý hay phân mảnh CSDL phân tán.

## 4. When to Use

- Khi thêm mới một thực thể nghiệp vụ (ví dụ: thêm bảng khảo sát, bảng chứng chỉ tham dự).
- Khi bổ sung cột dữ liệu mới hoặc thay đổi kiểu dữ liệu của bảng hiện có.
- Khi thêm hoặc tối ưu hóa các chỉ mục B-Tree để giảm thời gian phản hồi truy vấn.
- Khi kiểm toán tính nhất quán giữa ORM Models, Schema DDL và CSDL SQLite thực tế.

## 5. When NOT to Use

- Khi chỉ thực hiện câu truy vấn `SELECT` đọc dữ liệu trong controller (dùng `event-retrieval`).
- Khi chỉ định dạng dữ liệu trả về cho client JSON API (dùng `api-development`).

## 6. Required Context

Agent cần nắm vững:

- Hệ quản trị CSDL: SQLite (`instance/event_management.db` / `event_management.db`).
- Framework ORM: Flask-SQLAlchemy 3.0+ / SQLAlchemy 2.0 (sử dụng cú pháp hiện đại `db.session.get()`, `db.get_or_404()`, hàm thời gian `utc_now()`).
- Danh mục 11 bảng hiện tại: `users`, `speakers`, `venues`, `events`, `schedules`, `attendees`, `tickets`, `registrations`, `ai_chat_history`, `notifications`, `event_faqs`.
- Danh mục 13 B-Tree indexes đã được thiết lập trong `database/schema.sql`.
- Quy chuẩn thẩm định Human Gate 3 (Database Design Approval).

## 7. Source Files to Inspect

Trước khi thiết kế hoặc can thiệp CSDL, Agent PHẢI kiểm tra các tệp sau:

- [database/schema.sql](file:///d:/Event_Management_AI/database/schema.sql): Tệp DDL chuẩn của toàn bộ 11 bảng và các indexes.
- [app/models/](file:///d:/Event_Management_AI/app/models/): Toàn bộ 11 tệp ORM Model:
  - `user.py`, `speaker.py`, `venue.py`, `event.py`, `schedule.py`, `attendee.py`, `ticket.py`, `registration.py`, `ai_chat.py`, `notification.py`, `faq.py`.
- [app/extensions.py](file:///d:/Event_Management_AI/app/extensions.py): Đối tượng `db = SQLAlchemy()` và helper `utc_now()`.
- [seed.py](file:///d:/Event_Management_AI/seed.py): Dữ liệu mẫu khởi tạo phục vụ kiểm thử.
- [instance/event_management.db](file:///d:/Event_Management_AI/instance/event_management.db): Tệp CSDL SQLite thực tế.

## 8. Related Documentation

- [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md): Tài liệu đặc tả CSDL quan hệ chính thức.
- [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md): Kiến trúc tầng dữ liệu.
- [docs/requirements.md](file:///d:/Event_Management_AI/docs/requirements.md): Các yêu cầu dữ liệu (DR - Data Requirements).

## 9. Related Skills

- `requirements-analysis`: Tiếp nhận yêu cầu về trường dữ liệu và ràng buộc nghiệp vụ.
- `architecture-design`: Đảm bảo tầng CSDL phù hợp ranh giới kiến trúc 3 tầng.
- `implementation`: Sử dụng các ORM Models để lập trình nghiệp vụ.
- `event-retrieval`: Sử dụng cấu trúc bảng để viết câu truy vấn SQL an toàn.
- `testing`: Viết test cases kiểm chứng ràng buộc toàn vẹn mô hình (`test_models.py`).

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Đọc cấu trúc hiện tại)

1. Đọc [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md) để hiểu mô hình dữ liệu lý thuyết.
2. Đọc [database/schema.sql](file:///d:/Event_Management_AI/database/schema.sql) để kiểm tra DDL thực tế.
3. Đọc tệp ORM Model tương ứng trong [app/models/](file:///d:/Event_Management_AI/app/models/).

### Bước 2: ANALYZE (Phân tích thực thể và ràng buộc)

1. **Kiểm tra chuẩn hóa 3NF**:
   - 1NF: Mọi thuộc tính đều mang giá trị nguyên tố (Atomic values), có khóa chính xác định duy nhất mỗi hàng.
   - 2NF: Đạt 1NF và không có thuộc tính nào phụ thuộc một phần vào khóa chính phức hợp.
   - 3NF: Đạt 2NF và không có thuộc tính không khóa nào phụ thuộc bắc cầu vào khóa chính.
2. **Kiểm tra toàn vẹn tham chiếu**:
   - Khóa ngoại có trỏ đúng bảng và cột khóa chính không (`ON DELETE CASCADE` khi xóa cha thì con bị xóa; hoặc `ON DELETE SET NULL` khi cần giữ lịch sử).
   - Kiểm tra kiểu dữ liệu khớp nhau giữa PK và FK (ví dụ: `INTEGER`).
3. **Phân tích hiệu năng đánh chỉ mục (Index Analysis)**:
   - Các cột thường xuyên xuất hiện trong mệnh đề `WHERE`, `JOIN`, `ORDER BY` phải được đánh chỉ mục.
   - Tránh đánh chỉ mục bừa bãi trên các cột có độ chọn lọc quá thấp (như cột boolean ít giá trị).

### Bước 3: PLAN (Lập kế hoạch thay đổi)

1. Soạn thảo mã DDL mới cho bảng hoặc cột.
2. Soạn thảo mã ORM Model tương ứng kế thừa từ `db.Model`.
3. Lập kế hoạch bảo toàn dữ liệu hiện có (Migration Strategy) nếu bảng đã có dữ liệu sản xuất.

### Bước 4: MODIFY (Thực hiện cập nhật đồng bộ 3 nơi)

1. **Cập nhật ORM Model** trong `app/models/`: Định nghĩa các cột, relationships, properties.
2. **Cập nhật DDL** trong `database/schema.sql`: Bổ sung câu lệnh `CREATE TABLE` hoặc `ALTER TABLE` kèm `CREATE INDEX`.
3. **Cập nhật Tài liệu** [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md): Cập nhật bảng thuộc tính, kiểu dữ liệu, giải thích nghiệp vụ và sơ đồ Mermaid ERD.
4. **Cập nhật Seed Data** trong `seed.py` nếu thuộc tính mới là bắt buộc (`NOT NULL`).

### Bước 5: VERIFY (Kiểm chứng Human Gate 3)

1. Kiểm tra CSDL thực tế bằng cách chạy script kiểm tra đối chiếu (ví dụ: `scratch/check_db_schema_discrepancy.py`).
2. Chạy test suite mô hình dữ liệu:

   ```powershell
   .venv\Scripts\python -m pytest tests/test_models.py -v
   ```

3. Đảm bảo toàn bộ quan hệ 1-N, N-N, khóa ngoại và ràng buộc unique hoạt động chính xác.

## 11. Validation

Agent phải kiểm tra các tiêu chí sau:

- [ ] 100% bảng có Khóa chính (`PRIMARY KEY`) rõ ràng.
- [ ] Mọi khóa ngoại đều có chỉ định hành vi `ON DELETE` an toàn.
- [ ] Khớp 100% giữa Schema DDL, SQLAlchemy ORM Models và tài liệu thiết kế CSDL.
- [ ] Các trường thời gian sử dụng hàm chuẩn `utc_now` (tránh lỗi deprecation của `utcnow`).
- [ ] Không có cột nào vi phạm chuẩn 3NF.

## 12. Failure Handling

- **Khi khóa ngoại bị vi phạm toàn vẹn**: Rà soát thứ tự tạo bảng trong `schema.sql` (bảng cha phải được tạo trước bảng con).
- **Khi xung đột schema giữa ORM và SQLite**: Sử dụng script kiểm tra PRAGMA để tìm chính xác cột bị thiếu hoặc sai kiểu dữ liệu, áp dụng lệnh sửa đổi có kiểm soát.

## 13. Security Considerations

- Mật khẩu người dùng trong bảng `users` PHẢI lưu dạng băm an toàn qua PBKDF2-HMAC-SHA256 (`password_hash`), không bao giờ lưu plain text.
- Dữ liệu PII của người tham dự (`email`, `phone` trong `attendees` và `users`) phải được kiểm soát truy cập theo vai trò.
- Tất cả truy vấn tương tác với CSDL phải thông qua ORM hoặc Parameterized Queries để triệt tiêu hoàn toàn SQL Injection.

## 14. Expected Output

1. Tệp ORM Model hoàn chỉnh trong [app/models/](file:///d:/Event_Management_AI/app/models/).
2. Tệp DDL đồng bộ trong [database/schema.sql](file:///d:/Event_Management_AI/database/schema.sql).
3. Bản cập nhật tài liệu [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md) với sơ đồ Mermaid ERD.
4. Kết quả kiểm thử thành công qua `test_models.py`.

## 15. Completion Criteria

- CSDL đáp ứng đầy đủ yêu cầu lưu trữ cho tính năng mới.
- Đạt nghiệm thu qua Human Gate 3 (Ký duyệt thiết kế CSDL).
- Không phát sinh cảnh báo SQLAlchemy legacy API hay lỗi migration.

## 16. Maintenance Notes

- Cập nhật skill này khi chuyển đổi hệ quản trị CSDL sang PostgreSQL/MySQL trong môi trường Cloud Production.
- Thường xuyên rà soát kích thước chỉ mục B-Tree và hiệu năng câu truy vấn khi dung lượng dữ liệu tăng trưởng.
