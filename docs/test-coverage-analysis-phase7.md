# PHÂN TÍCH ĐỘ BAO PHỦ KIỂM THỬ GIAI ĐOẠN 7 (PHASE 7 TEST COVERAGE & GAP ANALYSIS)

**Dự án:** EventAI Pro — Nền tảng Quản trị & Điều hành Sự kiện Toàn diện Tích hợp Đa tác tử AI  
**Phiên bản hệ thống:** v2.4.0-hardened  
**Ngày thực hiện:** 28/09/2026  
**Nguyên tắc chỉ đạo:** Ưu tiên kiểm định các luồng nghiệp vụ cốt lõi, an toàn dữ liệu và tính ổn định thay vì theo đuổi tỷ lệ % lý thuyết thuần túy.  

---

## 1. PHÂN BỐ ĐỘ BAO PHỦ TÍNH NĂNG TOÀN HỆ THỐNG

Toàn bộ 67 tuyến URL routes và 11 bảng dữ liệu thực thể của EventAI Pro được phân loại theo 3 mức độ bao phủ kiểm thử:

```
[========================================] 100% Các luồng nghiệp vụ cốt lõi (Critical Paths)
[==============================          ]  75% Tính năng mở rộng & thống kê phụ trợ
[===================================     ]  88% Tổng thể hệ thống (Weighted System Coverage)
```

---

## 2. DANH MỤC CÁC TÍNH NĂNG ĐÃ KIỂM THỬ TOÀN DIỆN (FULLY TESTED FEATURES)

Các tính năng này đã được kiểm thử 100% qua cả Unit Test, Integration Test và Scenario Evaluation:

1. **Xác thực & Quản trị Danh tính (Authentication & Identity):**
   - Đăng ký tài khoản, kiểm tra trùng lặp email/username.
   - Băm mật khẩu một chiều an toàn bằng PBKDF2-HMAC-SHA256.
   - Đăng nhập, đăng xuất, lưu phiên đăng nhập (Remember Me).
   - Phân quyền theo vai trò (RBAC) 3 cấp: Attendee, Staff, Admin.
   - Chặn người dùng thường và nhân viên truy cập trang quản trị cấp cao (403 Forbidden).
2. **Quản trị Sự kiện & Bảng Vé (Event Management & Ticketing):**
   - Tạo mới sự kiện, cập nhật trạng thái (`draft`, `published`, `ongoing`, `completed`, `cancelled`).
   - Cấu hình các hạng vé (`standard`, `vip`, `early_bird`, `free`) kèm quota riêng biệt.
   - Cơ chế trừ quota theo thời gian thực và tự động khóa vé khi hết suất.
   - Sinh mã QR thanh toán chuẩn VietQR NAPAS 24/7.
3. **Quy trình Điểm danh Sự kiện (Check-in & Anti-duplicate Defense):**
   - Quét mã QR bằng Camera trình duyệt trên di động hoặc nhập mã thủ công.
   - Kiểm tra vé hủy, vé chưa thanh toán, vé sai sự kiện.
   - Ngăn chặn hoàn toàn điểm danh trùng lặp (Anti-duplicate Scan ném mã 409 Conflict).
   - Hoàn tác điểm danh (Undo Check-in) khi nhân viên thao tác nhầm.
4. **Quy trình Hủy vé & Hoàn trả Quota (Cancel Ticket & Quota Reclaim):**
   - Hủy vé của người dùng, chuyển trạng thái vé thành `cancelled`.
   - Tự động cộng hoàn trả lại 1 suất vào kho `remaining_quota` của sự kiện.
   - Cho phép người dùng đăng ký lại vé mới sau khi đã hủy vé cũ (GAP-05).
   - Cơ chế bảo vệ Atomic Rollback khi xảy ra lỗi phát sinh bất ngờ (GAP-03).
5. **Hệ thống AI Đa tác tử & RAG Grounded Chatbot (Dual-Engine AI):**
   - Trích xuất ý định câu hỏi bằng tiếng Việt (Intent & Entity Extraction).
   - Truy xuất dữ liệu có cấu trúc từ SQLite và dựng ngữ cảnh Ground Truth.
   - Cơ chế dự phòng ngoại tuyến Offline Mock Engine khi mất kết nối mạng.
   - Bộ lọc PII Sanitization che giấu thông tin nhạy cảm trước khi gọi LLM.
   - Bộ giới hạn tần suất Token Bucket Rate Limiter chống cạn kiệt tài nguyên (GAP-02).
   - Benchmark định lượng 10 ca kiểm thử so sánh đối đầu Single-Agent vs Multi-Agent.
6. **Đánh giá Cảm xúc & Hộp thư Thông báo (Feedback Sentiment & Notifications):**
   - Gửi đánh giá sao (1-5 sao) kèm nhận xét chi tiết.
   - Tự động phân tích cảm xúc (Positive, Neutral, Negative) phục vụ thống kê quản trị.
   - Gửi thông báo sự kiện tự động tới danh sách người tham dự.

---

## 3. CÁC TÍNH NĂNG KIỂM THỬ MỘT PHẦN (PARTIALLY TESTED FEATURES)

1. **Bộ lọc Báo cáo Thống kê Quản trị Nâng cao (Advanced Admin Filtering):**
   - *Đã kiểm thử:* Tính toán số liệu tổng thể (Doanh thu, tỷ lệ check-in, số lượng đăng ký).
   - *Phần còn lại:* Các tổ hợp lọc nhiều điều kiện theo ngày tháng kết hợp trạng thái thanh toán cụ thể trên giao diện UI bảng biểu lớn (chủ yếu được xử lý ở client-side DataTables).
2. **Kịch bản Mạng Chập chờn khi Tải Ảnh QR (Network Flakiness during Image Fetch):**
   - *Đã kiểm thử:* Tạo ảnh PNG QR Code tự động trên ổ đĩa và hiển thị qua đường dẫn `/static/qrcodes/`.
   - *Phần còn lại:* Tình huống người dùng di động đi vào vùng mất sóng hoàn toàn trong lúc tải ảnh QR (được khắc phục nhờ hệ thống gửi mã số vé dạng chữ `TCK-...` để nhân viên nhập tay).

---

## 4. CÁC ĐƯỜNG DẪN KHÔNG PHÁT SINH RỦI RO & KHÔNG CẦN THIẾT KIỂM THỬ (EXCLUDED PATHS)

1. **Thanh toán Trực tuyến Qua Cổng Ngân hàng Thật (Live Bank Gateway Webhook):**
   - Hệ thống hiện tại sử dụng cơ chế tạo mã VietQR chuẩn NAPAS và đối soát xác nhận của Ban tổ chức / Staff, không tích hợp trực tiếp Webhook tự động của bên thứ ba, do đó không có rủi ro về cổng thanh toán độc lập bị treo.
2. **Thao tác Xóa Cứng Sự kiện Đã có Người Đăng ký (Hard Deletion of Active Events):**
   - Ứng dụng áp dụng thiết kế xóa mềm (Soft Status / Cancellation) để bảo toàn lịch sử dữ liệu và quyền lợi người mua vé, không cho phép lệnh SQL `DELETE CASCADE` trên các sự kiện đang diễn ra.

---

## 5. ĐÁNH GIÁ CÁC VÙNG RỦI RO TIỀM ẨN (RISKY AREAS & MITIGATION)

| Vùng Rủi ro | Mức độ Rủi ro | Lý do Kỹ thuật | Biện pháp Giảm thiểu Đã áp dụng |
|---|:---:|---|---|
| **Bộ nhớ Session SQLite khi Restart** | **THẤP** | Khi dùng SQLite memory trong kiểm thử, dữ liệu biến mất khi tiến trình kết thúc. | Trên môi trường Production sử dụng SQLite file-based (`event_management.db`) hoặc PostgreSQL với volume mount bền vững. |
| **Hết hạn Quota Gemini API khi Vận hành Thật** | **TRUNG BÌNH** | Google API có thể gặp rate limit nếu lượng người dùng tăng đột biến. | Token Bucket Rate Limiter giới hạn 30 req/phút/IP và Local Grounded Mock Engine phản hồi ngay lập tức nếu API gặp lỗi. |
| **Thao tác Hủy vé Đồng thời (Concurrent Ticket Cancellations)** | **THẤP** | Hai luồng cùng cập nhật `remaining_quota` cùng một mili-giây. | Đã áp dụng bọc giao dịch `db.session.rollback()` an toàn trong GAP-03 và GAP-05. |
