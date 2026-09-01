---
name: event-retrieval
description: Skill truy xuất dữ liệu có cấu trúc từ CSDL (bảng events, schedules, speakers, venues, tickets) dựa trên ý định câu hỏi và bộ lọc sự kiện bằng Parameterized Queries an toàn.
---

# Event Retrieval Skill

## Objective
Truy vấn dữ liệu liên quan từ Cơ sở dữ liệu quan hệ nội bộ thông qua SQLAlchemy ORM / Parameterized Queries an toàn để cung cấp nguồn tri thức chuẩn xác (Ground Truth), làm cơ sở tạo Grounded Context cho mô hình LLM.

## Inputs
- Cấu trúc Intent & Entities từ `question-analysis`.
- CSDL quan hệ SQLite / MySQL thông qua SQLAlchemy Models.

## Process / Workflow
1. **Truy vấn Dữ liệu Sự kiện Cốt lõi (`events`)**:
   - Tiêu đề, mã sự kiện, mô tả, danh mục, thời gian bắt đầu/kết thúc, địa điểm.
2. **Truy vấn Lịch trình & Diễn giả (`schedules`, `speakers`, `venues`)**:
   - Danh sách phiên thảo luận, thời gian từng phiên, diễn giả phụ trách, phòng hội thảo.
3. **Truy vấn Hạng vé & Quota (`tickets`)**:
   - Loại vé, tên vé, giá tiền (VNĐ), số lượng vé còn lại (`quota - sold_count`), trạng thái mở bán.
4. **Lọc Dữ liệu Theo Ngữ cảnh Câu hỏi**:
   - Chỉ lấy các bản ghi liên quan trực tiếp đến sự kiện và ý định của người dùng để tối ưu kích thước Context và tiết kiệm token.

## Rules & Constraints
- Tuyệt đối không sử dụng nối chuỗi SQL thô (chống triệt để SQL Injection).
- Tuyệt đối không gửi toàn bộ CSDL hoặc toàn bộ các bản ghi sự kiện khác cho LLM.
- Tuyệt đối không truy xuất dữ liệu định danh cá nhân nhạy cảm của người dùng khác (PII).
- Nếu không tìm thấy kết quả phù hợp trong CSDL: Trả về danh sách rỗng `[]`, không được tự ý bịa dữ liệu.

## Outputs
- Danh sách Python Dictionaries / ORM Objects chứa dữ liệu thực tế chuyển sang `context-builder`.
