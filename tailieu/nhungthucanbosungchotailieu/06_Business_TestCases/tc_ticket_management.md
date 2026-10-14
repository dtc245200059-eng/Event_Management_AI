# Bộ Test Cases — Quản lý Vé (Ticket Management)

> **File:** `tc_ticket_management.md`
> **Chuyên gia đề xuất:** Senior BA
> **Mục tiêu bổ sung:** Sprint 3/4 — Kiểm thử nghiệp vụ vé
> **Phạm vi:** Phát hành vé, kiểm tra quota, đăng ký, hoàn/hủy

---

## 1. Kịch bản kiểm thử: Phát hành & Đăng ký Vé

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-TK-001 | Đăng ký vé Free thành công | 1. Truy cập sự kiện đang Published<br>2. Chọn vé Free<br>3. Nhập thông tin Attendee<br>4. Submit | event_id=12, ticket_type="free", attendee={name, email} | - Registration tạo thành công (status='confirmed')<br>- payment_status='free'<br>- QR Code được sinh<br>- sold_count tăng 1 | N/A |
| TC-TK-002 | Đăng ký vé Paid — chờ thanh toán | 1. Chọn vé Paid (200.000₫)<br>2. Nhập thông tin<br>3. Submit<br>4. KHÔNG thanh toán | ticket_type="paid", price=200000 | - Registration tạo (status='pending')<br>- payment_status='unpaid'<br>- QR Code CHƯA sinh<br>- Chuyển hướng tới Payment Gateway | N/A |
| TC-TK-003 | Đăng ký vé VIP — thanh toán thành công | 1. Chọn vé VIP<br>2. Nhập thông tin<br>3. Thanh toán qua Payment Gateway<br>4. IPN callback success | ticket_type="vip", price=500000, payment_result="success" | - payment_status='paid'<br>- registration_status='confirmed'<br>- QR Code sinh<br>- paid_at != null | N/A |
| TC-TK-004 | Đăng ký khi vé đã hết quota | 1. Thiết lập ticket quota=1, sold_count=1<br>2. Thử đăng ký thêm | quota=1, sold_count=1 | - HTTP 409<br>- Thông báo "Vé đã hết"<br>- Registration KHÔNG được tạo<br>- sold_count vẫn = 1 | N/A |
| TC-TK-005 | Đăng ký trùng (cùng Attendee, cùng Event) | 1. Attendee A đã đăng ký Event 12<br>2. Attendee A thử đăng ký lại Event 12 | attendee_id=15, event_id=12 (đã tồn tại) | - HTTP 409<br>- Thông báo "Bạn đã đăng ký sự kiện này"<br>- Không tạo registration mới | N/A |
| TC-TK-006 | Race condition — 2 user đăng ký vé cuối cùng | 1. Quota=10, sold_count=9 (còn 1 vé)<br>2. User A và User B submit đồng thời | Concurrent requests, quota=10, sold=9 | - CHỈ 1 user đăng ký thành công<br>- User còn lại nhận HTTP 409<br>- sold_count = 10 (không vượt quota)<br>- Transaction rollback cho user thất bại | N/A |

## 2. Kịch bản kiểm thử: Thanh toán

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-TK-007 | Thanh toán thành công — IPN callback | 1. Tạo registration Paid<br>2. Redirect đến Payment Gateway<br>3. Thanh toán thành công<br>4. IPN callback POST | payment_ref="VNP-123", status="success", amount=200000 | - payment_status='paid'<br>- registration_status='confirmed'<br>- paid_at = timestamp<br>- QR Code sinh | N/A |
| TC-TK-008 | Thanh toán thất bại | 1. Tạo registration Paid<br>2. Redirect đến Payment<br>3. Thanh toán thất bại | payment_result="failed" | - payment_status='failed'<br>- registration_status='pending'<br>- QR Code KHÔNG sinh<br>- Hiển thị nút "Thử lại" | N/A |
| TC-TK-009 | Thanh toán timeout (15 phút) | 1. Tạo registration Paid<br>2. KHÔNG thanh toán trong 15 phút | timeout=15min, no_callback | - payment_status='expired'<br>- registration_status='cancelled'<br>- sold_count rollback -= 1 | N/A |
| TC-TK-010 | IPN callback với số tiền không khớp | 1. Tạo registration amount=200000<br>2. IPN callback amount=100000 | expected=200000, received=100000 | - KHÔNG xác nhận payment<br>- Log cảnh báo "Amount mismatch"<br>- Đánh dấu cần đối soát | N/A |

## 3. Kịch bản kiểm thử: Hoàn/Hủy Vé

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-TK-011 | Hủy vé Free | 1. Attendee đã đăng ký vé Free<br>2. Click "Hủy đăng ký" | registration_id=123, ticket_type="free" | - registration_status='cancelled'<br>- sold_count -= 1<br>- refund_status='none' (không cần hoàn) | N/A |
| TC-TK-012 | Hoàn vé Paid — trong thời hạn | 1. Đã thanh toán Paid<br>2. > 24h trước sự kiện<br>3. Yêu cầu hoàn vé | registration_id=123, days_before_event=5 | - refund_status='refunded'<br>- registration_status='cancelled'<br>- sold_count -= 1<br>- Gửi refund request đến Payment Gateway | N/A |
| TC-TK-013 | Hoàn vé Paid — quá thời hạn | 1. Đã thanh toán Paid<br>2. < 24h trước sự kiện<br>3. Yêu cầu hoàn vé | registration_id=123, days_before_event=0.5 | - HTTP 400<br>- Thông báo "Quá hạn hoàn vé"<br>- Không thay đổi trạng thái | N/A |
| TC-TK-014 | Hủy vé đã check-in | 1. Vé đã checked_in = true<br>2. Thử hủy | checked_in=true | - HTTP 400<br>- Thông báo "Không thể hủy vé đã check-in"<br>- Không thay đổi trạng thái | N/A |

## 4. Kịch bản kiểm thử: Validation & Edge Cases

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-TK-015 | Đăng ký với email không hợp lệ | 1. Nhập email sai format<br>2. Submit | email="not-an-email" | - HTTP 400<br>- Lỗi validation: "Email không hợp lệ" | N/A |
| TC-TK-016 | Đăng ký sự kiện Draft (chưa Published) | 1. Truy cập sự kiện status='draft'<br>2. Thử đăng ký | event_status="draft" | - HTTP 403<br>- Thông báo "Sự kiện chưa mở đăng ký" | N/A |
| TC-TK-017 | Đăng ký sự kiện đã Completed | 1. Sự kiện status='completed'<br>2. Thử đăng ký | event_status="completed" | - HTTP 400<br>- Thông báo "Sự kiện đã kết thúc" | N/A |
| TC-TK-018 | Tạo vé với giá âm | 1. Admin tạo Ticket<br>2. Nhập price = -50000 | price=-50000 | - HTTP 400<br>- Lỗi: "Giá vé phải ≥ 0" | N/A |
