# Bộ Test Cases — Check-in & Thanh toán

> **File:** `tc_checkin_payment.md`
> **Chuyên gia đề xuất:** Senior BA
> **Mục tiêu bổ sung:** Sprint 3/4 — Kiểm thử Check-in QR & Payment Integration
> **Phạm vi:** Check-in QR, Check-in trùng, Payment Gateway callback, Reconciliation

---

## 1. Kịch bản kiểm thử: Check-in QR Code

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-CI-001 | Check-in QR thành công (vé Free) | 1. Staff mở /checkin/scan<br>2. Quét QR "TKT-2026-00100"<br>3. Kiểm tra kết quả | ticket_number="TKT-2026-00100", event_id=12, ticket_type="free" | - HTTP 200<br>- checked_in = true<br>- checked_in_at = timestamp<br>- checked_in_by = staff username<br>- Màn hình xanh + tên attendee | N/A |
| TC-CI-002 | Check-in QR thành công (vé Paid đã thanh toán) | 1. Vé Paid, payment_status='paid'<br>2. Quét QR | payment_status="paid", registration_status="confirmed" | - Check-in thành công<br>- Hiển thị loại vé "Paid"<br>- Hiển thị tên + đơn vị | N/A |
| TC-CI-003 | Check-in QR thành công (vé VIP) | 1. Vé VIP, đã thanh toán<br>2. Quét QR | ticket_type="vip", payment_status="paid" | - Check-in thành công<br>- Hiển thị badge "VIP"<br>- Ghi nhận timestamp | N/A |
| TC-CI-004 | Check-in trùng (vé đã quét) | 1. Vé đã checked_in = true<br>2. Quét lại QR | checked_in=true, checked_in_at="09:15:23" | - HTTP 409<br>- "Vé đã check-in lúc 09:15:23"<br>- Hiển thị tên staff đã quét trước<br>- Màn hình đỏ | N/A |
| TC-CI-005 | QR code không hợp lệ | 1. Quét QR với mã ngẫu nhiên không tồn tại | ticket_number="INVALID-XYZ" | - HTTP 404<br>- "Mã vé không tồn tại"<br>- Màn hình vàng cảnh báo | N/A |
| TC-CI-006 | Vé thuộc sự kiện khác | 1. Đang check-in Event #12<br>2. Quét vé thuộc Event #15 | event_id_scan=12, ticket_event_id=15 | - HTTP 400<br>- "Vé này thuộc sự kiện khác: [tên sự kiện #15]"<br>- KHÔNG check-in | N/A |
| TC-CI-007 | Vé đã bị hủy | 1. Registration status='cancelled'<br>2. Quét QR | registration_status="cancelled" | - HTTP 400<br>- "Vé đã bị hủy. Không thể check-in."<br>- Màn hình đỏ | N/A |
| TC-CI-008 | Vé chưa thanh toán (Paid ticket) | 1. Payment_status='unpaid'<br>2. Quét QR | payment_status="unpaid", ticket_type="paid" | - HTTP 402<br>- "Vé chưa thanh toán. Số tiền: 200.000₫"<br>- Hướng dẫn thanh toán tại quầy | N/A |
| TC-CI-009 | Check-in khi sự kiện chưa bắt đầu | 1. Event start_date = ngày mai<br>2. Quét QR hôm nay | event_start > NOW() + 2h | - Cho phép check-in (early check-in OK)<br>- Hoặc warning "Sự kiện chưa bắt đầu" tuỳ config | N/A |
| TC-CI-010 | Check-in concurrent (2 staff quét cùng QR) | 1. 2 thiết bị quét cùng QR đồng thời | Same ticket_number, concurrent | - CHỈ 1 request thành công<br>- Request còn lại: HTTP 409<br>- Atomic UPDATE đảm bảo nhất quán | N/A |

## 2. Kịch bản kiểm thử: Payment Gateway Integration

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-PY-001 | Tạo Payment URL thành công | 1. Registration Paid created<br>2. System gọi Payment Gateway<br>3. Nhận payment_url | amount=200000, order_id="REG-2026-00123" | - payment_url trả về<br>- payment_ref lưu vào DB<br>- Redirect user đến Gateway | N/A |
| TC-PY-002 | IPN Callback — Thành công | 1. Payment Gateway gửi POST IPN<br>2. status=success, amount match | txn_ref="VNP-123", status="success", amount=200000 | - payment_status='paid'<br>- registration_status='confirmed'<br>- QR Code sinh<br>- Response to Gateway: 200 OK | N/A |
| TC-PY-003 | IPN Callback — Thất bại | 1. Payment Gateway gửi POST IPN<br>2. status=failed | status="failed" | - payment_status='failed'<br>- registration_status vẫn 'pending'<br>- QR KHÔNG sinh | N/A |
| TC-PY-004 | IPN Callback — Amount mismatch | 1. Expected 200000<br>2. IPN gửi amount=100000 | expected=200000, actual=100000 | - KHÔNG confirm payment<br>- Log: "Amount mismatch"<br>- Đánh dấu cần đối soát thủ công | N/A |
| TC-PY-005 | IPN Callback — Duplicate (gọi 2 lần) | 1. IPN success gửi 2 lần<br>2. Cùng txn_ref | Same IPN payload, sent twice | - Lần 1: Xử lý bình thường<br>- Lần 2: Bỏ qua (idempotent)<br>- payment_status vẫn 'paid' | N/A |
| TC-PY-006 | Payment timeout — 15 phút | 1. Registration created<br>2. Không có IPN trong 15 phút | No callback within 15 min | - payment_status='expired'<br>- registration_status='cancelled'<br>- sold_count rollback -= 1 | N/A |
| TC-PY-007 | Hoàn tiền — Request success | 1. Registration confirmed, paid<br>2. > 24h trước event<br>3. Gửi refund request | days_before_event > 1 | - Gọi Payment Gateway refund API<br>- refund_status='refunded'<br>- registration_status='cancelled'<br>- sold_count -= 1 | N/A |
| TC-PY-008 | Hoàn tiền — Gateway lỗi | 1. Gửi refund request<br>2. Payment Gateway trả error | Gateway returns 500 | - refund_status='failed'<br>- Đánh dấu cần xử lý thủ công<br>- Log error chi tiết | N/A |

## 3. Kịch bản kiểm thử: Thống kê Check-in (Dashboard)

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-DS-001 | Tỷ lệ check-in realtime | 1. 100 registrations cho Event #12<br>2. 60 đã check-in<br>3. Xem Dashboard | checked_in: 60/100 | - Tỷ lệ check-in: 60%<br>- Bar chart hiển thị đúng<br>- Cập nhật khi refresh | N/A |
| TC-DS-002 | Check-in timeline | 1. Check-in lúc 8:00, 8:15, 8:30...<br>2. Xem biểu đồ timeline | Multiple check-ins over time | - Line chart hiển thị check-in theo thời gian<br>- Peak hours highlighted | N/A |
| TC-DS-003 | Check-in by ticket type | 1. Free: 40 check-in<br>2. Paid: 15 check-in<br>3. VIP: 5 check-in | Mixed ticket types | - Pie chart chia theo loại vé<br>- Free: 67%, Paid: 25%, VIP: 8% | N/A |

## 4. Kịch bản kiểm thử: Bảo mật Check-in

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback |
|-------|---------------|-------------------|-------------------|-------------------|-------------|
| TC-SC-001 | Staff không có quyền check-in | 1. User role='attendee' (không phải staff)<br>2. Truy cập /checkin/scan | role="attendee" | - HTTP 403<br>- "Bạn không có quyền check-in" | N/A |
| TC-SC-002 | Check-in không đăng nhập | 1. Không có session<br>2. POST /checkin/verify | No auth session | - HTTP 401<br>- Redirect đến /auth/login | N/A |
| TC-SC-003 | Brute force ticket_number | 1. Gửi 100 requests với random ticket_number<br>2. Trong 1 phút | 100 invalid ticket_numbers | - Tất cả trả 404 (not found)<br>- Rate limit kick in sau N requests<br>- Log suspicious activity | N/A |
