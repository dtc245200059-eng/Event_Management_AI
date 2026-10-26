---
name: event-context-builder
description: "Kỹ năng xây dựng ngữ cảnh xác thực (Grounded Context Builder) từ kết quả truy xuất cơ sở dữ liệu SQLite, kiểm soát Token Budgeting, định dạng bảng Markdown và chuẩn hóa liên kết điều hướng."
---

# KỸ NĂNG: XÂY DỰNG NGỮ CẢNH TRUY XUẤT (EVENT CONTEXT BUILDER)

## 1. MỤC TIÊU (OBJECTIVE)
Định dạng, cấu trúc hóa và làm giàu dữ liệu sự kiện đã trích xuất từ cơ sở dữ liệu thành khối văn bản Markdown chuẩn (Ground Truth Context), giúp mô hình ngôn ngữ lớn (Gemini) có đầy đủ dữ kiện xác thực trước khi sinh phản hồi, loại bỏ hoàn toàn ảo giác.

## 2. ĐẦU VÀO (INPUTS)
- `events`: Danh sách các đối tượng thực thể `Event` được truy xuất từ SQLAlchemy ORM.
- `target_event_id` (nếu có): Sự kiện trọng tâm người dùng đang quan tâm.
- `token_budget`: Giới hạn dung lượng token cho phép (mặc định 2,500 từ/tokens).

## 3. QUY TRÌNH THỰC HIỆN (PROCEDURE)
1. **Khởi tạo khối dữ liệu gốc:**
   - Đặt tiêu đề rõ ràng: `=== DANH SÁCH DỮ LIỆU SỰ KIỆN TRUY XUẤT TỪ CSDL (GROUND TRUTH) ===`.
2. **Duyệt qua từng sự kiện (Event Formatting):**
   - Header sự kiện: `### [SỰ KIỆN ID {id}]: {title}`.
   - Thông tin cơ bản: Mã sự kiện, trạng thái, danh mục, thời gian bắt đầu/kết thúc, hình thức, địa điểm cụ thể.
   - Bảng hạng vé & giá tiền: Liệt kê tên hạng vé, giá (0đ hoặc có phí), quota còn lại và tình trạng mở bán.
   - Lịch trình các phiên (Agenda): Khung giờ, tên phiên, diễn giả chủ trì, phòng hội thảo.
   - Quy định & FAQ: Các câu hỏi thường gặp liên quan đến sự kiện.
3. **Bổ sung liên kết điều hướng chuẩn (Action Links):**
   - Tạo đường dẫn chuẩn: `[👉 Xem chi tiết & Đặt vé ngay](/events/<id>#ticketSection)`.
4. **Bổ sung quy trình chuẩn hệ thống:**
   - Thêm tóm tắt quy trình đặt vé, check-in mã QR tại quầy và quy trình hủy vé hoàn quota.
5. **Xử lý trạng thái rỗng (Empty State):**
   - Nếu `events` rỗng, trả về chuỗi thông báo chuẩn: `"KHÔNG TÌM THẤY DỮ LIỆU SỰ KIỆN PHÙ HỢP TRONG CƠ SỞ DỮ LIỆU HỆ THỐNG."`

## 4. NGUYÊN TẮC BẢO MẬT & CHỐNG ẢO GIÁC (RULES)
- **Zero-Invention:** Tuyệt đối không tự suy diễn thêm thời gian, địa điểm, sức chứa không có trong đối tượng Event.
- **Privacy:** Tuyệt đối không đưa danh sách người đăng ký hoặc email người tham dự vào khối ngữ cảnh này.

## 5. ĐẦU RA (OUTPUTS)
Khối chuỗi văn bản Markdown hoàn chỉnh `context_str` dùng để thay thế placeholder `{{retrieved_context}}` trong prompt template.

## 6. KIỂM CHỨNG (VERIFICATION)
- Kiểm tra tính đầy đủ của các trường thông tin (thời gian, địa điểm, bảng giá vé).
- Đảm bảo các liên kết URL đều đúng định dạng nội bộ của EventAI Pro.
