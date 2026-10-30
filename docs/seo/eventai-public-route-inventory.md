# EventAI Pro — Public Route Inventory & Indexability Classification

**Phiên bản:** 1.0.0  
**Ngày lập:** 29/10/2026  
**Phạm vi kiểm toán:** Toàn bộ hệ thống định tuyến (Routing & Blueprints) của ứng dụng `EventAI Pro`  
**Phương pháp:** Phân tích tĩnh mã nguồn mã nguồn Flask (`app/__init__.py`, `app/routes/*.py`)  
**Môi trường:** Python 3.14 / Flask 3.x / Jinja2  

---

## 1. TỔNG QUAN HỆ THỐNG ĐỊNH TUYẾN

Ứng dụng `EventAI Pro` được cấu trúc theo mô hình Application Factory (`create_app` tại `app/__init__.py`) với **8 Blueprints** chính và 1 tập hợp tài nguyên tĩnh:

1. `main_bp` (`app/routes/main.py`) — Tiền tố: Không có (Root `/`)
2. `auth_bp` (`app/routes/auth.py`) — Tiền tố: `/auth`
3. `events_bp` (`app/routes/events.py`) — Tiền tố: `/events`
4. `tickets_bp` (`app/routes/tickets.py`) — Tiền tố: `/tickets`
5. `checkin_bp` (`app/routes/checkin.py`) — Tiền tố: `/checkin`
6. `admin_bp` (`app/routes/admin.py`) — Tiền tố: `/admin`
7. `ai_bp` (`app/routes/ai.py`) — Tiền tố: `/ai` và bí danh `/api/ai`
8. `notifications_bp` (`app/routes/notifications.py`) — Tiền tố: `/notifications`
9. `static` (Flask built-in static handler) — Tiền tố: `/static`

Tổng cộng hệ thống quản lý **44 endpoints** chức năng.

---

## 2. PHÂN LOẠI 6 NHÓM ĐỊNH TUYẾN (ROUTE CLASSIFICATION)

Dựa trên tiêu chuẩn Google Search Essentials và nguyên tắc bảo mật thông tin, toàn bộ các tuyến đường được phân loại thành 6 nhóm:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      EVENTAI PRO ROUTE TAXONOMY                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Public & Potentially Indexable        (Trang sự kiện công khai)     │
│ 2. Public but Intentionally Non-Indexable (Đăng nhập, Chatbot tool)    │
│ 3. Authentication-Required               (Vé của tôi, Hồ sơ cá nhân)   │
│ 4. Private / Sensitive / Administrative  (Quản trị, Soát vé, Thống kê) │
│ 5. API Endpoints                         (REST / JSON API)             │
│ 6. Static Assets                         (CSS, JS, Uploads, QR Codes)  │
└────────────────────────────────────────────────────────────────────────┘
```

---

### NHÓM 1: CÔNG KHAI VÀ CẦN ĐƯỢC LẬP CHỈ MỤC (PUBLIC & POTENTIALLY INDEXABLE)

Đây là các trang đóng vai trò cốt lõi cho SEO, tiếp cận người dùng từ công cụ tìm kiếm (Google, Bing), cần có Meta Tags, Canonical Link và Schema.org Event đầy đủ:

| Route Path | Method | Endpoint Handler | File Nguồn & Dòng | Mục đích nghiệp vụ | Chỉ thị Robot mục tiêu |
| :--- | :---: | :--- | :--- | :--- | :---: |
| `/` | GET | `main.index` | `app/routes/main.py#L11-L32` | Trang chủ: Banner sự kiện nổi bật, thống kê, slider AI gợi ý | `index, follow` |
| `/events` | GET | `main.event_list` | `app/routes/main.py#L34-L87` | Danh mục khám phá toàn bộ sự kiện, tìm kiếm và phân trang | `index, follow` (Canonical chuẩn) |
| `/events/<int:event_id>` | GET | `main.event_detail` | `app/routes/main.py#L89-L113` | Chi tiết sự kiện: lịch trình, diễn giả, địa điểm, bảng giá vé | `index, follow` (Nếu published) |

> [!WARNING]
> **Lỗ hổng phân quyền trạng thái sự kiện tại `main.event_detail`:**
> Tuyến `/events/<int:event_id>` hiện dùng `db.get_or_404(Event, event_id)` mà **không kiểm tra** `event.status`. Nếu một sự kiện có trạng thái `draft`, `cancelled` hoặc `completed`, người dùng hoặc crawler vẫn có thể truy cập bằng ID. 
> - **Chính sách đề xuất:** 
>   - `status == 'published'` hoặc `'ongoing'`: Cho phép lập chỉ mục (`index, follow`).
>   - `status == 'completed'`: Giữ nội dung, trả về mã 200 kèm cờ `eventStatus: EventScheduled/EventMovedOnline` hoặc `noindex` nếu sự kiện tạm thời.
>   - `status in ['draft', 'cancelled']`: Trả về HTTP 404 cho khách vãng lai/crawler (hoặc `noindex, nofollow` nếu người xem là chủ sở hữu sự kiện).

---

### NHÓM 2: CÔNG KHAI NHƯNG CỐ Ý KHÔNG ĐƯỢC LẬP CHỈ MỤC (PUBLIC BUT INTENTIONALLY NON-INDEXABLE)

Các trang tiện ích hoặc công cụ tương tác công khai không mang giá trị tìm kiếm thông tin sự kiện tĩnh, cần đặt chỉ thị `noindex, nofollow` để tránh lãng phí ngân sách thu thập dữ liệu (Crawl Budget):

| Route Path | Method | Endpoint Handler | File Nguồn & Dòng | Mục đích nghiệp vụ | Chỉ thị Robot mục tiêu |
| :--- | :---: | :--- | :--- | :--- | :---: |
| `/auth/login` | GET, POST | `auth.login` | `app/routes/auth.py#L12-L42` | Đăng nhập tài khoản | `noindex, nofollow` |
| `/auth/register` | GET, POST | `auth.register` | `app/routes/auth.py#L44-L104` | Đăng ký thành viên | `noindex, nofollow` |
| `/ai/workspace` | GET | `ai.chat_workspace` | `app/routes/ai.py#L21-L36` | Studio trò chuyện toàn màn hình với Trợ lý AI | `noindex, nofollow` |
| `/health` | GET | `main.health_check` | `app/routes/main.py#L115-L136` | Health check probe (K8s/Docker) trả về JSON 200/503 | `noindex, nofollow` |

---

### NHÓM 3: YÊU CẦU ĐĂNG NHẬP NGƯỜI DÙNG (AUTHENTICATION-REQUIRED)

Các tuyến đường dành riêng cho người tham dự sau khi đăng nhập, liên quan đến thông tin cá nhân và quản lý vé cá nhân. Tuyệt đối cấm lập chỉ mục:

| Route Path | Method | Endpoint Handler | File Nguồn & Dòng | Mục đích nghiệp vụ | Chỉ thị Robot mục tiêu |
| :--- | :---: | :--- | :--- | :--- | :---: |
| `/auth/logout` | GET | `auth.logout` | `app/routes/auth.py#L106-L111` | Đăng xuất người dùng | `noindex, nofollow` |
| `/auth/profile` | GET | `auth.profile` | `app/routes/auth.py#L113-L121` | Xem hồ sơ cá nhân và lịch sử đăng ký | `noindex, nofollow` |
| `/auth/profile/update` | POST | `auth.update_profile` | `app/routes/auth.py#L123-L167` | Cập nhật hồ sơ và sở thích AI | `noindex, nofollow` |
| `/auth/profile/change-password` | POST | `auth.change_password` | `app/routes/auth.py#L169-L192` | Đổi mật khẩu tài khoản | `noindex, nofollow` |
| `/tickets/my-tickets` | GET | `tickets.my_tickets` | `app/routes/tickets.py#L212-L221` | Danh sách vé điện tử của người dùng | `noindex, nofollow` |
| `/tickets/register/<int:event_id>` | GET, POST | `tickets.register_ticket` | `app/routes/tickets.py#L48-L160` | Đặt vé / Giữ chỗ sự kiện | `noindex, nofollow` |
| `/tickets/checkout/<int:reg_id>` | GET, POST | `tickets.checkout` | `app/routes/tickets.py#L176-L210` | Thanh toán vé qua cổng trực tuyến | `noindex, nofollow` |
| `/tickets/view/<int:reg_id>` | GET | `tickets.view_ticket` | `app/routes/tickets.py#L223-L230` | Chi tiết thẻ vé điện tử kèm mã QR SVG | `noindex, nofollow` |
| `/tickets/download-qr/<int:reg_id>` | GET | `tickets.download_qr` | `app/routes/tickets.py#L232-L246` | Tải xuống tệp SVG mã QR vé | `noindex, nofollow` |
| `/tickets/cancel/<int:reg_id>` | POST | `tickets.cancel_ticket` | `app/routes/tickets.py#L248-L283` | Hủy vé tham dự | `noindex, nofollow` |
| `/tickets/feedback/<int:reg_id>` | POST | `tickets.submit_feedback` | `app/routes/tickets.py#L285-L325` | Gửi đánh giá sao & nhận xét sự kiện | `noindex, nofollow` |
| `/notifications/inbox` | GET | `notifications.inbox` | `app/routes/notifications.py#L124-L142` | Hộp thư thông báo của người tham dự | `noindex, nofollow` |
| `/notifications/view/<int:notif_id>` | GET | `notifications.view_detail` | `app/routes/notifications.py#L144-L149` | Xem chi tiết thông báo | `noindex, nofollow` |

---

### NHÓM 4: NỘI BỘ, NHẠY CẢM VÀ QUẢN TRỊ (PRIVATE / SENSITIVE / ADMINISTRATIVE)

Các trang dành riêng cho Ban tổ chức (Organizer), Nhân viên soát vé (Staff) và Quản trị viên (Admin). Bắt buộc phải bảo vệ bằng `@login_required` và phân quyền RBAC, đồng thời phải đưa vào cấu hình cấm thu thập của `robots.txt`:

| Route Path | Method | Endpoint Handler | File Nguồn & Dòng | Vai trò yêu cầu |
| :--- | :---: | :--- | :--- | :---: |
| `/admin/dashboard` | GET | `admin.dashboard` | `app/routes/admin.py#L22-L83` | Admin |
| `/admin/users` | GET | `admin.users_list` | `app/routes/admin.py#L85-L104` | Admin |
| `/admin/users/create` | POST | `admin.create_user` | `app/routes/admin.py#L106-L172` | Admin |
| `/admin/users/<int:user_id>/change-role` | POST | `admin.change_user_role` | `app/routes/admin.py#L174-L200` | Admin |
| `/admin/users/<int:user_id>/toggle-status` | POST | `admin.toggle_user_status` | `app/routes/admin.py#L203-L215` | Admin |
| `/events/manage` | GET | `events.manage` | `app/routes/events.py#L24-L32` | Organizer, Admin |
| `/events/create` | GET, POST | `events.create` | `app/routes/events.py#L34-L102` | Organizer, Admin |
| `/events/<int:event_id>/edit` | GET, POST | `events.edit` | `app/routes/events.py#L104-L137` | Organizer, Admin |
| `/events/<int:event_id>/delete` | POST | `events.delete` | `app/routes/events.py#L139-L150` | Organizer, Admin |
| `/events/<int:event_id>/schedules` | GET | `events.schedules` | `app/routes/events.py#L155-L174` | Organizer, Admin |
| `/events/<int:event_id>/schedules/create` | POST | `events.create_schedule` | `app/routes/events.py#L176-L219` | Organizer, Admin |
| `/events/schedules/<int:schedule_id>/edit` | POST | `events.edit_schedule` | `app/routes/events.py#L221-L261` | Organizer, Admin |
| `/events/schedules/<int:schedule_id>/delete` | POST | `events.delete_schedule` | `app/routes/events.py#L263-L276` | Organizer, Admin |
| `/events/speakers` | GET | `events.speakers_list` | `app/routes/events.py#L282-L287` | Organizer, Admin |
| `/events/speakers/create` | POST | `events.create_speaker` | `app/routes/events.py#L289-L320` | Organizer, Admin |
| `/events/speakers/<int:speaker_id>/delete` | POST | `events.delete_speaker` | `app/routes/events.py#L322-L333` | Admin |
| `/events/<int:event_id>/tickets` | GET | `events.manage_tickets` | `app/routes/events.py#L338-L346` | Organizer, Admin |
| `/events/<int:event_id>/tickets/create` | POST | `events.create_ticket` | `app/routes/events.py#L348-L381` | Organizer, Admin |
| `/events/<int:event_id>/feedback` | GET | `events.event_feedback` | `app/routes/events.py#L386-L429` | Organizer, Admin |
| `/checkin/` | GET | `checkin.index` | `app/routes/checkin.py#L23-L42` | Staff, Organizer |
| `/notifications/manage` | GET | `notifications.manage` | `app/routes/notifications.py#L37-L67` | Organizer, Admin |
| `/notifications/create` | GET, POST | `notifications.create` | `app/routes/notifications.py#L69-L122` | Organizer, Admin |

---

### NHÓM 5: ĐẦU MÚT GIAO TIẾP DỮ LIỆU API (API ENDPOINTS)

Các tuyến trả về dữ liệu định dạng JSON cho ứng dụng Single-Page Interactions, Chatbot AI và Camera Scanner:

| Route Path | Method | Endpoint Handler | File Nguồn & Dòng | Quyền truy cập |
| :--- | :---: | :--- | :--- | :---: |
| `/ai/chat` (hoặc `/api/ai/chat`) | POST | `ai.chat` | `app/routes/ai.py#L38-L101` | Mọi người (Có Rate Limit 30 req/min) |
| `/ai/generate-description` | POST | `ai.generate_description` | `app/routes/ai.py#L103-L134` | Organizer, Admin |
| `/ai/recommendations` | GET | `ai.recommendations` | `app/routes/ai.py#L136-L165` | Mọi người |
| `/ai/predictive/<int:event_id>` | GET | `ai.predictive_stats` | `app/routes/ai.py#L167-L175` | Mọi người / Admin |
| `/ai/sentiment/<int:event_id>` | GET | `ai.sentiment_stats` | `app/routes/ai.py#L177-L183` | Mọi người / Admin |
| `/ai/generate-notification` | POST | `ai.generate_notification` | `app/routes/ai.py#L185-L244` | Organizer, Admin |
| `/ai/feedback-summary/<int:event_id>` | GET | `ai.feedback_summary` | `app/routes/ai.py#L246-L253` | Organizer, Admin |
| `/ai/multi-agent/advisory` | POST | `ai.multi_agent_advisory` | `app/routes/ai.py#L259-L330` | Mọi người (Có Rate Limit 25 req/min) |
| `/ai/multi-agent/trace/<task_id>` | GET | `ai.get_multi_agent_trace` | `app/routes/ai.py#L331-L340` | Mọi người |
| `/ai/multi-agent/benchmark` | POST | `ai.run_benchmark_endpoint` | `app/routes/ai.py#L342-L353` | Mọi người |
| `/checkin/verify-api` | POST | `checkin.verify_api` | `app/routes/checkin.py#L73-L175` | Staff, Organizer |
| `/checkin/api/event-attendees/<int:event_id>` | GET | `checkin.api_event_attendees` | `app/routes/checkin.py#L177-L227` | Staff, Organizer |
| `/checkin/api/quick-checkin/<int:reg_id>` | POST | `checkin.api_quick_checkin` | `app/routes/checkin.py#L229-L267` | Staff, Organizer |
| `/checkin/api/undo-checkin/<int:reg_id>` | POST | `checkin.api_undo_checkin` | `app/routes/checkin.py#L269-L283` | Staff, Organizer |
| `/notifications/api/recent` | GET | `notifications.api_recent` | `app/routes/notifications.py#L151-L177` | Login Required |

---

### NHÓM 6: TÀI NGUYÊN TĨNH (STATIC ASSETS)

| Thư mục / Mẫu đường dẫn | Nội dung tài nguyên | Rủi ro SEO / Bảo mật | Khuyến nghị Robots |
| :--- | :--- | :--- | :---: |
| `/static/css/style.css` | Tệp CSS chính của hệ thống Apple Liquid Glass | Cần cho Googlebot kết xuất đồ họa giao diện | **Cho phép (Allow)** |
| `/static/js/main.js` | Bộ điều khiển giao diện, cuộn vô tận, chuyển theme | Cần cho Googlebot thực thi JS render | **Cho phép (Allow)** |
| `/static/js/ai_chat.js` | Tệp JS điều khiển cửa sổ chat floating | Tiện ích chat, không ảnh hưởng nội dung trang | Cho phép |
| `/static/uploads/*` | Ảnh banner sự kiện người dùng tải lên | Cần hiển thị trong Google Image Search | **Cho phép (Allow)** |
| `/static/qr_codes/*.svg` | Mã QR vé điện tử và mã QR thanh toán VietQR | **Cực kỳ nhạy cảm! Chứa dữ liệu định danh vé và thanh toán** | **CẤM (Disallow /static/qr_codes/)** |

---

## 3. MA TRẬN CHỈ THỊ ROBOTS & THU THẬP DỮ LIỆU ĐỀ XUẤT

```
┌──────────────────────────────────────────────────────────────┐
│ robots.txt Policy Recommendation                             │
├──────────────────────────────────────────────────────────────┤
│ User-agent: *                                                │
│ Allow: /                                                     │
│ Allow: /events$                                              │
│ Allow: /events?                                              │
│ Allow: /events/                                              │
│ Allow: /static/css/                                          │
│ Allow: /static/js/                                           │
│ Allow: /static/uploads/                                      │
│                                                              │
│ Disallow: /admin/                                            │
│ Disallow: /checkin/                                          │
│ Disallow: /tickets/                                          │
│ Disallow: /notifications/                                    │
│ Disallow: /auth/                                             │
│ Disallow: /ai/                                               │
│ Disallow: /api/                                              │
│ Disallow: /static/qr_codes/                                  │
│                                                              │
│ Sitemap: https://eventai.pro/sitemap.xml                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. KẾT LUẬN TỪ BẢNG KIỂM KÊ

1. **Số lượng trang thực sự cần SEO là gọn gàng và tập trung:** Chỉ gồm Trang chủ (`/`), Danh sách sự kiện (`/events`), và Chi tiết sự kiện (`/events/<int:event_id>`).
2. **Nguy cơ rò rỉ mã QR qua thư mục static:** Các mã QR vé SVG sinh ra tại `app/static/qr_codes/` đang ở chế độ công khai nếu biết tên tệp. Cần cấm triệt để bot thu thập thư mục này qua `robots.txt` và trả về tiêu đề `X-Robots-Tag: noindex`.
3. **Thiếu kiểm soát trạng thái sự kiện:** Tuyến `/events/<int:event_id>` cần được gia cố logic để không xuất hiện các sự kiện bản nháp (`draft`) trên công cụ tìm kiếm.

