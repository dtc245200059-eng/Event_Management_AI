# MA TRẬN PHÂN QUYỀN TRUY CẬP (ROLE-BASED ACCESS CONTROL - RBAC)
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Chuẩn:** NIST RBAC Model / OWASP Access Control Guidelines  
**Phiên bản:** 2.0 (Cập nhật 4 vai trò theo yêu cầu Giảng viên hướng dẫn)  
**Ngày cập nhật:** 27/10/2026  

---

## 1. Định Nghĩa 4 Vai Trò Nghiệp Vụ Chuẩn

1. **Attendee (Khách tham dự):**
   - Đăng ký tài khoản, quản lý hồ sơ cá nhân (`AttendeeProfile`).
   - Tìm kiếm, lọc và xem thông tin chi tiết sự kiện, lịch trình, diễn giả, địa điểm.
   - Đăng ký tham gia sự kiện, nhận vé điện tử kèm mã QR và số vé duy nhất.
   - Hủy đăng ký vé khi chưa tham dự.
   - Gửi đánh giá sao (1 - 5 sao) và nhận xét sau khi đã check-in hoặc kết thúc sự kiện.
   - Tương tác với Trợ lý AI Concierge để hỏi đáp thông tin sự kiện.
   - Xem thông báo cá nhân (Thư mời, Lời nhắc, Cảm ơn).

2. **Organizer (Ban tổ chức / Quản lý sự kiện):**
   - Kế thừa toàn bộ quyền hạn nghiệp vụ của vai trò `Staff` trước đây.
   - Tạo mới, cập nhật, chỉnh sửa và đóng/mở sự kiện được phân công (`Event.created_by`).
   - Quản lý lịch trình sự kiện: thêm, sửa, xóa các phiên hội thảo với ràng buộc `start_at < end_at`.
   - Quản lý danh mục diễn giả (`Speaker`) và địa điểm tổ chức (`Venue`).
   - Thiết lập số lượng và hạn mức phát hành các hạng vé (`Ticket.quota`).
   - Soạn thảo và duyệt nội dung email AI (Mời, Nhắc nhở, Cảm ơn) với các placeholder `{attendee_name}`, `{event_name}`.
   - Xem thống kê, đánh giá và tóm tắt AI về phản hồi của người tham dự (`/events/<id>/feedback`).

3. **CheckInStaff (Nhân viên soát vé tại cửa):**
   - Vai trò chuyên biệt mới được bổ sung theo yêu cầu mở rộng của Giảng viên.
   - Truy cập giao diện soát vé tại cửa `/checkin/`.
   - Sử dụng camera điện thoại/máy tính quét mã QR của vé hoặc nhập thủ công mã vé/mã đăng ký.
   - Thực hiện thao tác check-in nguyên tử (Atomic Check-in) trên CSDL chia sẻ:
     - Chấp nhận vé hợp lệ lần đầu.
     - Từ chối ngay lập tức vé đã qua sử dụng (HTTP 409) kèm cảnh báo gian lận hoặc quét lặp.
   - Tra cứu danh sách khách mời của sự kiện được giao để hỗ trợ soát vé dự phòng.
   - **Ràng buộc an ninh:** CheckInStaff *tuyệt đối không được phép* truy cập bảng điều khiển Admin (`/admin/dashboard`), không được sửa sự kiện hoặc xem log hệ thống.

4. **Admin (Quản trị viên toàn hệ thống):**
   - Toàn quyền truy cập và kiểm soát hệ thống.
   - Quản lý người dùng: phân quyền và thay đổi vai trò giữa các tài khoản (`/admin/users`).
   - Bảng điều khiển quản trị tổng thể với 8 chỉ số phân tích thực tế (`/admin/dashboard`).
   - Xem toàn bộ nhật ký truy vấn RAG và thông điệp MessageBus của hệ thống đa tác tử.
   - Cấu hình các tham số AI, API key và cơ chế phòng thủ Critic Guardrail.

---

## 2. Ma Trận Phân Quyền Chi Tiết (Permission Matrix)

| Module & Chức năng | Đường dẫn / Endpoint | Attendee | Organizer | CheckInStaff | Admin |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Trang chủ & Danh sách sự kiện** | `GET /`, `GET /events/` | ✅ | ✅ | ✅ | ✅ |
| **Chi tiết sự kiện & Lịch trình** | `GET /events/<id>`, `GET /events/<id>/schedules` | ✅ | ✅ | ✅ | ✅ |
| **Đăng ký vé sự kiện** | `POST /tickets/register/<id>` | ✅ | ⚠️ (demo) | ⚠️ (demo) | ✅ |
| **Hủy đăng ký vé** | `POST /tickets/cancel/<id>` | ✅ (vé mình) | ❌ | ❌ | ✅ |
| **Xem vé của tôi & Tải QR** | `GET /tickets/my-tickets`, `GET /tickets/download-qr/<id>` | ✅ | ❌ | ❌ | ✅ |
| **Chat với Trợ lý AI Concierge** | `POST /api/ai/chat`, `POST /ai/chat` | ✅ | ✅ | ✅ | ✅ |
| **Gửi phản hồi sự kiện** | `POST /tickets/feedback/<reg_id>` | ✅ (đã checkin) | ❌ | ❌ | ✅ |
| **Tạo sự kiện mới** | `GET/POST /events/create` | ❌ | ✅ | ❌ | ✅ |
| **Chỉnh sửa / Cập nhật sự kiện** | `GET/POST /events/<id>/edit` | ❌ | ✅ (sự kiện mình) | ❌ | ✅ |
| **Thêm / Sửa / Xóa lịch trình** | `POST /events/<id>/schedules/create`, `edit`, `delete` | ❌ | ✅ | ❌ | ✅ |
| **Quản lý diễn giả & Địa điểm** | `GET/POST /events/speakers`, `/events/venues` | ❌ | ✅ | ❌ | ✅ |
| **Soạn thảo Email AI** | `POST /api/ai/generate-email` | ❌ | ✅ | ❌ | ✅ |
| **Xem & Tóm tắt Phản hồi AI** | `GET /events/<id>/feedback` | ❌ | ✅ | ❌ | ✅ |
| **Giao diện Soát vé Check-in** | `GET /checkin/` | ❌ | ✅ | ✅ | ✅ |
| **Thực hiện Check-in Vé (API)** | `POST /checkin/verify-api` | ❌ | ✅ | ✅ | ✅ |
| **Bảng điều khiển Quản trị** | `GET /admin/dashboard` | ❌ | ❌ | ❌ | ✅ |
| **Quản lý Tài khoản & Phân quyền** | `GET /admin/users`, `POST /admin/users/<id>/role` | ❌ | ❌ | ❌ | ✅ |
| **Nhật ký Đa tác tử (Multi-Agent)** | `GET /admin/agent-logs` | ❌ | ❌ | ❌ | ✅ |

*Ghi chú:*  
- ✅ = Được phép truy cập và thực thi.  
- ❌ = Bị từ chối tại tầng API (HTTP 403 Forbidden hoặc HTTP 302 chuyển hướng đăng nhập).  
- ⚠️ = Quyền hạn có điều kiện bảo vệ dữ liệu cá nhân.

---

## 3. Chiến Lược Ánh Xạ và Tương Thích Ngược (Backward Compatibility)

Nhằm đảm bảo không làm gián đoạn các tài khoản và dữ liệu kiểm thử hiện có:
1. Giá trị `role` trong bảng `users` được hỗ trợ: `'admin'`, `'organizer'`, `'staff'`, `'checkin_staff'`, `'attendee'`.
2. Trong mô hình `User` (`app/models/user.py`), các thuộc tính kiểm tra quyền được hiện thực như sau:
   ```python
   @property
   def is_admin(self):
       return self.role == 'admin'

   @property
   def is_organizer(self):
       # Cho phép cả admin, organizer và tài khoản staff cũ quản trị sự kiện
       return self.role in ('admin', 'organizer', 'staff')

   @property
   def is_checkin_staff(self):
       # Cho phép admin, organizer, staff và nhân viên checkin_staff chuyên biệt
       return self.role in ('admin', 'organizer', 'staff', 'checkin_staff', 'CheckInStaff')
   ```
3. Tại tầng route, decorator `@staff_required` bảo vệ toàn bộ chức năng `/checkin/*`, trong khi `@organizer_required` bảo vệ `/events/create`, `/events/schedules/*` và `@admin_required` bảo vệ `/admin/*`.
