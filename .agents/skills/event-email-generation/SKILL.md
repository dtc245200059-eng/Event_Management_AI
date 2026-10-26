---
name: event-email-generation
description: "Kỹ năng hỗ trợ sinh bản thảo email truyền thông sự kiện (thư mời, nhắc lịch, cảm ơn), bắt buộc sử dụng placeholder {attendee_name} và {event_name}, bảo vệ PII, tách rời sinh nội dung với phát hành và yêu cầu con người phê duyệt."
---

# KỸ NĂNG: SINH BẢN THẢO EMAIL TRUYỀN THÔNG (EVENT EMAIL GENERATION)

## 1. MỤC TIÊU (OBJECTIVE)
Kỹ năng này hướng dẫn Agent hỗ trợ ban tổ chức soạn thảo các bản thảo email truyền thông chuẩn xác, lịch thiệp cho 3 loại thông điệp chính: (1) Thư mời tham dự (invitation), (2) Nhắc lịch sự kiện (reminder), (3) Thư cảm ơn sau sự kiện (thank_you), hoàn toàn dựa trên dữ liệu sự kiện đã được phê duyệt và tuân thủ nghiêm ngặt quy định bảo vệ dữ liệu cá nhân.

## 2. ĐẦU VÀO (INPUTS)
- `event_id`: ID sự kiện áp dụng.
- `notification_type`: Loại email (`'invitation'`, `'reminder'`, `'thank_you'`, `'update'`).
- `target_audience`: Nhóm người nhận (Tất cả người đăng ký, Đã check-in, Chưa check-in, Khách VIP).
- Thông tin sự kiện đã được khử trùng PII (Tên sự kiện, thời gian, hình thức, địa điểm, diễn giả tiêu biểu).

## 3. QUY TRÌNH THỰC HIỆN (PROCEDURE)
1. **Trích xuất thông tin sự kiện sạch:**
   - Đọc tên sự kiện, mã sự kiện, thời gian bắt đầu/kết thúc, địa điểm/link trực tuyến và danh sách diễn giả.
   - **Tuyệt đối không gửi** danh sách email, số điện thoại hay thông tin cá nhân của người tham gia cho mô hình AI.
2. **Lắp ráp Prompt Template (notification_generator.txt):**
   - Đưa thông tin sự kiện vào biến `{{event_info}}`.
   - Thiết lập loại email và phân khúc đối tượng nhận.
   - Ràng buộc mô hình bắt buộc sử dụng placeholder `{attendee_name}` và `{event_name}`.
3. **Gọi AI sinh bản thảo:**
   - Yêu cầu đầu ra định dạng JSON gồm `subject` và `content`.
   - Nếu ở chế độ ngoại tuyến, kích hoạt bộ sinh bản thảo mẫu nội bộ có cấu trúc chuẩn.
4. **Quy trình Phê duyệt của Con người (Human-in-the-Loop Approval):**
   - Đổ bản thảo vào giao diện soạn thảo (`notifications/create.html`).
   - Người tổ chức xem trước (Preview), chỉnh sửa câu chữ (Edit draft).
   - Chỉ khi người tổ chức chủ động bấm nút "Phát Hành Thông Báo Ngay", hệ thống mới lưu vào CSDL và phát hành vào Hộp thư cá nhân (`/notifications/inbox`).
5. **Tách rời mô-đun:**
   - Quá trình sinh nội dung (Content Generation) và quá trình gửi email vật lý (Email Delivery) là hai mô-đun hoàn toàn độc lập.
   - Không tự động gửi email nếu chưa có cấu hình SMTP nhà cung cấp được duyệt; lưu trữ nội bộ vào Hộp thư sự kiện để người tham dự xem trực tuyến.

## 4. NGUYÊN TẮC RÀNG BUỘC (RULES)
- **Anti-Hallucination:** Không bao giờ tự ý thêm địa điểm, thời gian hoặc chính sách không có trong thông tin sự kiện.
- **Privacy:** Không bao giờ truyền danh bạ người tham gia tới API bên ngoài.
- **Template Placeholders:** Luôn sử dụng `{attendee_name}` thay cho tên người nhận thực tế để tạo bản mẫu có thể tái sử dụng.
- **No Fake Delivery:** Nếu chưa cấu hình máy chủ gửi thư thực tế, không thông báo giả mạo là email đã được gửi tới hòm thư cá nhân của người dùng.

## 5. ĐẦU RA (OUTPUTS)
Đối tượng JSON bản thảo:
```json
{
  "subject": "[Nhắc Lịch] Sắp diễn ra sự kiện Vietnam AI Summit 2026 - Hướng dẫn Check-in",
  "content": "Kính gửi {attendee_name},\n\nChỉ còn ít ngày nữa, sự kiện {event_name} sẽ chính thức diễn ra...\n\nTrân trọng,\nBan Tổ Chức {event_name}"
}
```

## 6. KIỂM CHỨNG (VERIFICATION)
- Kiểm tra nội dung sinh ra có chứa đúng `{attendee_name}` và `{event_name}`.
- Xác nhận không có địa chỉ email thực tế của người dùng nào bị rò rỉ trong câu lệnh gọi AI.
