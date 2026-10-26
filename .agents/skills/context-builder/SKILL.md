---
name: context-builder
description: Skill định dạng và làm giàu dữ liệu truy xuất thành Grounded Context có cấu trúc, súc tích và chuẩn hóa để chèn vào Prompt Template của LLM.
---

# Context Builder Skill

## Objective
Chuyển đổi dữ liệu thô truy xuất từ CSDL thành đoạn văn bản ngữ cảnh (Context Block) có cấu trúc súc tích, chuẩn định dạng Markdown, làm sạch thông tin kỹ thuật để LLM trích dẫn chính xác và không bị nhầm lẫn.

## Inputs
- Dữ liệu thô từ `event-retrieval` (Event details, schedules, speakers, tickets, venues).

## Process / Workflow
1. **Chuẩn hóa Thông tin Sự kiện**:
   - `[SỰ KIỆN]: <Tên> (<Mã>) | Thời gian: <Bắt đầu> - <Kết thúc> | Địa điểm: <Địa chỉ>`
2. **Định dạng Danh sách Hạng vé**:
   - `+ <Tên vé> (<Loại>): <Giá tiền> VNĐ | Còn lại: <Số lượng còn>/<Tổng quota>`
3. **Định dạng Timeline Lịch trình**:
   - `+ [<Giờ bắt đầu> - <Giờ kết thúc>]: <Tên phiên> | Diễn giả: <Họ tên> (<Chức danh>) | Phòng: <Tên phòng>`
4. **Kiểm soát Dung lượng Token (Token Budgeting)**:
   - Cắt ngắn mô tả dài dòng không cần thiết để giới hạn ngữ cảnh dưới 1.500 tokens, giúp giảm độ trễ (latency) và chi phí API.

## Rules & Constraints
- Không tự ý thêm bớt các thông số kỹ thuật, giá vé hoặc tên diễn giả không có trong CSDL.
- Tuyệt đối loại bỏ các trường nội bộ (mật khẩu, ID khóa ngoại kỹ thuật, số điện thoại người tham dự).
- Nếu dữ liệu đầu vào rỗng: Trả về chuỗi `"KHÔNG CÓ DỮ LIỆU SỰ KIỆN NÀO ĐƯỢC TÌM THẤY TRONG HỆ THỐNG."`.

## Outputs
- Chuỗi văn bản ngữ cảnh `retrieved_context` sẵn sàng để chèn vào `rag-prompt`.
