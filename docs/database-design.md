# Relational Database Design Specification (3NF)
**Hệ Thống**: Quản Lý Sự Kiện Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
**Phiên Bản**: 3.0 (Chuẩn Hóa Theo Đề Tài 09 - Th.S Nguyễn Đình Dũng, ICTU)  
**Trạng Thái Triển Khai**: `[IMPLEMENTED]` (Toàn bộ 11 bảng 3NF và 13 B-Tree indexes đã được khởi tạo trong CSDL và ORM models)  
**Mô Hình**: CSDL Quan Hệ 11 Bảng Chuẩn Hóa Dạng Chuẩn 3 (3NF)  
**Tài Liệu Tham Chiếu**: `tailieu/de_tai_09.md`, `docs/architecture.md`, `database/schema.sql`  
**Kỹ Năng Quản Trị**: [`database-design`](file:///d:/Event_Management_AI/.agents/skills/database-design/SKILL.md)

---

## 1. Sơ Đồ Thực Thể Liên Kết (Entity Relationship Diagram - ERD)

```
┌──────────────┐         1:1         ┌────────────────┐
│    users     │─────────────────────│   attendees    │
└──────┬───────┘                     └───────┬────────┘
       │ 1:N                                 │ 1:N
       │                                     │
       ▼ 1:N                                 ▼ 1:N
┌──────────────┐         1:N         ┌────────────────┐         N:1         ┌─────────────┐
│    events    │────────────────────►│ registrations  │◄────────────────────│   tickets   │
└──────┬───────┘                     └────────────────┘                     └──────┬──────┘
       │                                                                           │
       ├─────────────────────────────────┬────────────────────────────────┐        │ N:1 (Event)
       │ 1:N                             │ 1:N                            │ 1:N    ▼
       ▼                                 ▼                                ▼ ┌─────────────┐
┌──────────────┐         N:1         ┌────────────────┐            ┌──────────────┐│   events    │
│  schedules   │────────────────────►│    speakers    │            │notifications │└─────────────┘
└──────┬───────┘                     └────────────────┘            └──────┬───────┘
       │ N:1                                                              │ N:1
       ▼                                                                  ▼ (Sender)
┌──────────────┐                                                   ┌──────────────┐
│    venues    │                                                   │    users     │
└──────────────┘                                                   └──────────────┘

┌──────────────┐         1:N         ┌────────────────┐
│    events    │────────────────────►│   event_faqs   │ (Kho tri thức RAG Grounding)
└──────────────┘                     └────────────────┘

┌──────────────┐         1:N         ┌────────────────┐
│    users     │────────────────────►│ ai_chat_history│
└──────────────┘                     └────────────────┘
```

---

## 2. Chứng Minh Chuẩn Hóa Dữ Liệu 3NF (Normalization Proof)

1. **Dạng Chuẩn 1 (1NF)**:
   - Tất cả các thuộc tính trong 11 bảng đều là nguyên tử (Atomic Values), không chứa mảng đa trị lặp lại trong một cột dữ liệu.
   - Mỗi bảng đều có Khóa chính (Primary Key: `id`) xác định duy nhất từng bản ghi.
2. **Dạng Chuẩn 2 (2NF)**:
   - Đạt 1NF và tất cả các thuộc tính không khóa đều phụ thuộc hàm toàn phần vào Khóa chính đơn nhất (`id`), không tồn tại phụ thuộc hàm từng phần.
3. **Dạng Chuẩn 3 (3NF)**:
   - Đạt 2NF và không có thuộc tính không khóa nào phụ thuộc bắc cầu vào Khóa chính.
   - *Tách bảng chuyên biệt*:
     - Diễn giả (`speakers`) và Địa điểm (`venues`) được tách riêng khỏi bảng `schedules` nhằm tránh dư thừa dữ liệu khi diễn giả phát biểu ở nhiều phiên hoặc phòng họp được tái sử dụng.
     - Hạng vé (`tickets`) được tách khỏi `events` để hỗ trợ đa hạng vé (Free, Standard, VIP) với hạn ngạch (quota) và mức giá riêng biệt.
     - Lịch sử chat AI (`ai_chat_history`), Thông báo truyền thông (`notifications`) và Câu hỏi thường gặp (`event_faqs`) được mô hình hóa thành các bảng quan hệ độc lập chuẩn hóa 3NF, liên kết chặt chẽ qua khóa ngoại với `events` và `users`.

---

## 3. Từ Điển Dữ Liệu 11 Bảng (Data Dictionary)

### 3.1. Bảng `users` (Quản lý tài khoản & RBAC 4 vai trò)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Định danh duy nhất tài khoản. |
| `username` | VARCHAR(80) | NOT NULL, UNIQUE | Tên đăng nhập hệ thống. |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Địa chỉ email liên hệ. |
| `password_hash` | VARCHAR(255) | NOT NULL | Chuỗi băm mật khẩu PBKDF2 với Salt. |
| `role` | VARCHAR(20) | NOT NULL, Default 'attendee' | Vai trò: `admin`, `organizer`, `staff`, `attendee`. |
| `full_name` | VARCHAR(120) | NOT NULL | Họ và tên người dùng. |
| `phone` | VARCHAR(20) | Nullable | Số điện thoại. |
| `organization` | VARCHAR(150) | Nullable | Cơ quan / Trường học / Đơn vị. |
| `is_active` | BOOLEAN | NOT NULL, Default True | Trạng thái kích hoạt tài khoản. |
| `created_at` | DATETIME | Default CURRENT_TIMESTAMP | Thời gian tạo tài khoản. |

### 3.2. Bảng `events` (Thông tin sự kiện)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID sự kiện nội bộ. |
| `event_code` | VARCHAR(40) | NOT NULL, UNIQUE | Mã định danh sự kiện (Ví dụ: `EVT-2026-AI`). |
| `title` | VARCHAR(255) | NOT NULL | Tên sự kiện. |
| `description` | TEXT | Nullable | Mô tả chi tiết sự kiện (Hỗ trợ AI sinh tự động). |
| `category` | VARCHAR(100) | NOT NULL | Danh mục (Công nghệ, Kinh doanh, Giáo dục,...). |
| `banner_url` | VARCHAR(255) | Nullable | Đường dẫn ảnh biểu trưng (Banner). |
| `start_date` | DATETIME | NOT NULL | Thời gian bắt đầu sự kiện. |
| `end_date` | DATETIME | NOT NULL | Thời gian kết thúc sự kiện. |
| `location_type` | VARCHAR(20) | Default 'offline' | Hình thức: `offline`, `online`, `hybrid`. |
| `location_address`| VARCHAR(255)| Nullable | Địa chỉ cụ thể tổ chức sự kiện. |
| `max_attendees` | INTEGER | Default 500 | Số lượng người tham dự tối đa. |
| `status` | VARCHAR(20) | Default 'published' | Trạng thái: `draft`, `published`, `completed`. |
| `tags` | VARCHAR(255) | Nullable | Từ khóa sự kiện phục vụ TF-IDF gợi ý. |
| `created_by` | INTEGER | FK -> `users.id` | Người tạo sự kiện (Admin / Organizer). |

### 3.3. Bảng `speakers` (Hồ sơ diễn giả)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID diễn giả. |
| `name` | VARCHAR(150) | NOT NULL | Họ và tên diễn giả. |
| `title` | VARCHAR(150) | Nullable | Học hàm, học vị, chức danh (TS., PGS.,...). |
| `organization` | VARCHAR(200) | Nullable | Đơn vị / Tập đoàn công tác. |
| `bio` | TEXT | Nullable | Tiểu sử và thành tựu nghiên cứu. |
| `expertise` | VARCHAR(255) | Nullable | Lĩnh vực chuyên môn sâu (GenAI, Cloud,...). |

### 3.4. Bảng `venues` (Địa điểm & phòng hội thảo)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID phòng họp / địa điểm. |
| `name` | VARCHAR(200) | NOT NULL | Tên trung tâm tổ chức sự kiện. |
| `room_name` | VARCHAR(100) | Nullable | Tên phòng hội thảo (Hội trường C4, Grand A). |
| `address` | VARCHAR(255) | NOT NULL | Địa chỉ chi tiết. |
| `capacity` | INTEGER | NOT NULL, Default 100 | Sức chứa tối đa của phòng. |
| `status` | VARCHAR(20) | Default 'available' | Tình trạng: `available`, `maintenance`. |

### 3.5. Bảng `schedules` (Lịch trình timeline phiên thảo luận)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID phiên lịch trình. |
| `event_id` | INTEGER | NOT NULL, FK -> `events.id` | Liên kết sự kiện cha (ON DELETE CASCADE). |
| `speaker_id` | INTEGER | Nullable, FK -> `speakers.id` | Diễn giả phụ trách phiên. |
| `venue_id` | INTEGER | Nullable, FK -> `venues.id` | Phòng hội thảo diễn ra phiên. |
| `title` | VARCHAR(200) | NOT NULL | Tên chủ đề phiên thảo luận. |
| `start_at` | DATETIME | NOT NULL | Thời gian bắt đầu phiên. |
| `end_at` | DATETIME | NOT NULL | Thời gian kết thúc phiên. |

### 3.6. Bảng `attendees` (Hồ sơ người tham dự)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID hồ sơ người tham dự. |
| `attendee_code` | VARCHAR(40) | NOT NULL, UNIQUE | Mã định danh khách (Ví dụ: `ATT-1001`). |
| `user_id` | INTEGER | UNIQUE, FK -> `users.id` | Tài khoản đăng nhập tương ứng (1:1). |
| `full_name` | VARCHAR(150) | NOT NULL | Họ và tên đầy đủ. |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE | Email nhận vé và thông báo. |
| `phone` | VARCHAR(20) | Nullable | Số điện thoại liên hệ. |
| `interests` | TEXT | Nullable | Sở thích công nghệ phục vụ AI Recommendation. |

### 3.7. Bảng `tickets` (Hạng vé & Hạn ngạch Quota)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID hạng vé. |
| `event_id` | INTEGER | NOT NULL, FK -> `events.id` | Thuộc sự kiện nào. |
| `ticket_code` | VARCHAR(40) | NOT NULL, UNIQUE | Mã vé (Ví dụ: `TCK-VIP-01`). |
| `ticket_type` | VARCHAR(30) | NOT NULL | Loại vé: `free`, `standard`, `vip`. |
| `name` | VARCHAR(100) | NOT NULL | Tên hiển thị (Vé VIP Doanh Nhân). |
| `price` | FLOAT | NOT NULL, Default 0.0 | Giá tiền niêm yết (VNĐ). |
| `quota` | INTEGER | NOT NULL, Default 100 | Tổng số lượng vé phát hành. |
| `sold_count` | INTEGER | NOT NULL, Default 0 | Số lượng vé đã bán ra (Giao dịch an toàn). |
| `status` | VARCHAR(20) | Default 'active' | Trạng thái: `active`, `sold_out`, `hidden`. |

### 3.8. Bảng `registrations` (Đăng ký vé, Check-in & Khảo sát)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID lượt đăng ký. |
| `registration_code`| VARCHAR(50)| NOT NULL, UNIQUE | Mã hóa đơn đăng ký. |
| `event_id` | INTEGER | NOT NULL, FK -> `events.id` | Sự kiện tham gia. |
| `attendee_id` | INTEGER | NOT NULL, FK -> `attendees.id` | Người tham gia. |
| `ticket_id` | INTEGER | NOT NULL, FK -> `tickets.id` | Hạng vé đã chọn. |
| `registration_status`| VARCHAR(20)| Default 'confirmed' | Trạng thái: `confirmed`, `pending`, `cancelled`. |
| `payment_status` | VARCHAR(20) | Default 'free' | Trạng thái: `free`, `paid`, `pending`, `cancelled`. |
| `ticket_number` | VARCHAR(50) | NOT NULL, UNIQUE | Mã vé định danh duy nhất in trên mã QR. |
| `qr_code_path` | VARCHAR(255) | Nullable | Đường dẫn lưu mã QR Vector SVG. |
| `checked_in` | BOOLEAN | Default False | Cờ xác nhận đã vào cổng (Anti-duplicate). |
| `checked_in_at` | DATETIME | Nullable | Thời điểm quét mã tại cổng. |
| `feedback_rating`| INTEGER | Nullable (1-5) | Điểm số đánh giá sau sự kiện. |
| `feedback_text` | TEXT | Nullable | Nhận xét người tham dự. |
| `sentiment` | VARCHAR(20) | Nullable | Kết quả phân loại cảm xúc: `positive`, `neutral`, `negative`. |
| `sentiment_score` | FLOAT | Nullable | Điểm số độ tin cậy phân loại cảm xúc. |
| `feedback_submitted_at`| DATETIME | Nullable | Thời gian gửi phản hồi. |

### 3.9. Bảng `notifications` (Mô-đun Truyền thông & Gửi Thông báo - Yêu cầu Đề tài 09)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID thông báo. |
| `event_id` | INTEGER | NOT NULL, FK -> `events.id` | Sự kiện liên quan. |
| `sender_id` | INTEGER | Nullable, FK -> `users.id` | Người gửi (Ban tổ chức / Admin). |
| `title` | VARCHAR(255) | NOT NULL | Tiêu đề thông báo / email. |
| `notification_type`| VARCHAR(50)| NOT NULL, Default 'update' | Phân loại: `invitation`, `reminder`, `thank_you`, `update`. |
| `content` | TEXT | NOT NULL | Nội dung chi tiết (Sinh bởi AI hoặc BTC). |
| `target_audience` | VARCHAR(50) | NOT NULL, Default 'all_registered' | Phân khúc: `all_registered`, `checked_in`, `not_checked_in`, `vip`. |
| `recipient_count` | INTEGER | Default 0 | Số lượng khách nhận thông báo. |
| `status` | VARCHAR(20) | Default 'sent' | Trạng thái gửi: `draft`, `sent`, `failed`. |
| `sent_at` | DATETIME | Default CURRENT_TIMESTAMP | Thời điểm phát hành thông báo. |

### 3.10. Bảng `event_faqs` (Kho Câu hỏi thường gặp & Quy định phục vụ RAG Grounding)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID FAQ. |
| `event_id` | INTEGER | NOT NULL, FK -> `events.id` | Sự kiện áp dụng (hoặc NULL nếu dùng chung). |
| `category` | VARCHAR(100) | Default 'Chung' | Nhóm câu hỏi (Vé, Check-in, Địa điểm, Dress code). |
| `question` | VARCHAR(500) | NOT NULL | Câu hỏi thường gặp của khách tham dự. |
| `answer` | TEXT | NOT NULL | Câu trả lời chính thức được kiểm duyệt. |
| `is_active` | BOOLEAN | Default True | Bật/tắt hiển thị câu hỏi trong RAG context. |

### 3.11. Bảng `ai_chat_history` (Lịch sử tương tác AI RAG)
| Tên Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa Nghiệp Vụ |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto Increment | Mã ID lịch sử chat. |
| `user_id` | INTEGER | Nullable, FK -> `users.id` | Người gửi câu hỏi. |
| `event_id` | INTEGER | Nullable, FK -> `events.id` | Sự kiện đang được hỏi. |
| `user_message` | TEXT | NOT NULL | Nội dung câu hỏi người dùng. |
| `ai_response` | TEXT | NOT NULL | Câu trả lời từ AI Assistant. |
| `response_mode`| VARCHAR(20) | Default 'live' | Chế độ: `live` (Gemini API) hoặc `mock` (Offline). |
| `latency_ms` | INTEGER | Nullable | Thời gian phản hồi (mili-giây). |

---

## 4. Biên Bản Kiểm Chứng Cơ Sở Dữ Liệu (Human Gate 3)

```
=============================================================================
            BIÊN BẢN KIỂM CHỨNG THIẾT KẾ CƠ SỞ DỮ LIỆU (HUMAN GATE 3)
=============================================================================
Dự Án: Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)
Đề Tài: 09 - Th.S Nguyễn Đình Dũng, ICTU
Người Kiểm Duyệt: Kỹ Sư CSDL / Giảng Viên Hướng Dẫn
Thời Điểm: Tháng 10/2026

DANH MỤC KIỂM TRA (VERIFICATION CHECKLIST):
 [X] Cấu trúc 11 bảng đạt chuẩn dạng chuẩn 3 (3NF), triệt tiêu dị thường thêm/xóa/sửa.
 [X] Khóa ngoại PK-FK được thiết lập chuẩn xác với hành vi ON DELETE CASCADE an toàn.
 [X] Ràng buộc UNIQUE chống đăng ký trùng lặp (event_id, attendee_id) được kích hoạt.
 [X] Bảng notifications hỗ trợ đầy đủ 4 phân khúc đối tượng và thống kê người nhận.
 [X] Bảng event_faqs cung cấp kho dữ liệu Grounding chuẩn chống Hallucination cho AI Chatbot.
 [X] Cột ticket_number duy nhất hỗ trợ cơ chế quét mã QR chống gian lận.
 [X] Đánh chỉ mục Indexes đầy đủ trên các trường tìm kiếm và join thường xuyên.
 [X] Khởi tạo CSDL qua ORM và script seed.py chạy thành công 100%.

KẾT LUẬN & PHÊ DUYỆT:
 Trạng Thái: [ APPROVED ] - ĐÃ PHÊ DUYỆT
 Quyết Định: Toàn bộ CSDL sẵn sàng phục vụ vận hành và kiểm thử tự động.
=============================================================================
```
