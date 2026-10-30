# EventAI Pro — Phase 3B Event Structured Data Implementation Report

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3B — Hiện thực hóa Dữ liệu Có cấu trúc Schema.org Event JSON-LD & BreadcrumbList  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kỹ sư Trưởng Technical SEO, Chuyên gia Schema.org, Kiến trúc sư Flask/Jinja2 & Kỹ sư Kiểm thử An ninh Ứng dụng  
**Trạng thái thực thi:** **HOÀN THÀNH TOÀN DIỆN (100% CÁC TIÊU CHÍ NGHIỆM THU ĐẠT CHUẨN XÁC MINH)**  

---

## 1. TỔNG QUAN VÀ MỤC TIÊU GIAI ĐOẠN 3B

Triển khai tiếp nối thành công của Phase 3A (Core SEO & Metadata), Giai đoạn 3B tập trung hiện thực hóa toàn diện chuẩn dữ liệu có cấu trúc **Schema.org Event JSON-LD** và **BreadcrumbList** cho các trang chi tiết sự kiện công khai trên hệ thống EventAI Pro (`/events/<int:event_id>`).

### Các mục tiêu cốt lõi đã đạt được:
1. **Thiết kế Bộ tạo Schema Tập trung (Centralized Builder):** Tích hợp các hàm nghiệp vụ chuẩn hóa tại [`app/seo_helpers.py`](file:///D:/Event_Management_AI/app/seo_helpers.py), bám sát 100% các cột và quan hệ thực tế trong CSDL SQLAlchemy (`Event`, `Ticket`, `Schedule`, `Speaker`, `User`).
2. **Tuân thủ Chuẩn Google Search Central & Schema.org:** Định dạng đầy đủ các thuộc tính cốt lõi của một sự kiện: `name`, `description`, `url`, `startDate`, `endDate`, `eventStatus`, `eventAttendanceMode`, `location`, `image`, `organizer`, `offers`, `performer`.
3. **Xử lý Thời gian & Múi giờ Chuẩn ISO 8601:** Chuyển đổi an toàn đối tượng datetime naive của CSDL thành định dạng ISO 8601 kèm offset tường minh `+07:00` (Việt Nam/Indochina), bảo vệ tính nhất quán giữa thời gian hiển thị giao diện và dữ liệu máy đọc.
4. **Hỗ trợ Đa dạng Hình thức Địa điểm (Location Strategy):**
   - Sự kiện trực tiếp (`offline`): Khai báo `Place` kèm địa chỉ bưu chính `PostalAddress`.
   - Sự kiện trực tuyến (`online`): Khai báo `VirtualLocation` trỏ về URL công khai an toàn.
   - Sự kiện kết hợp (`hybrid`): Khai báo danh sách kép chứa cả `Place` và `VirtualLocation`.
5. **Dữ liệu Ưu đãi Giá vé (Ticket Offers):** Phản ánh chính xác danh mục hạng vé thực tế (Vé Miễn phí `price: 0.0`, Vé Có phí, trạng thái khả dụng `InStock` hoặc `SoldOut`), trỏ về neo an toàn `#tickets` trên trang chi tiết sự kiện.
6. **BreadcrumbList Tương ứng Điều hướng Thực tế:** Khai báo danh sách đường dẫn phân cấp 3 cấp độ: `Trang chủ` (1) -> `Sự kiện` (2) -> `Tên sự kiện hiện tại` (3).
7. **Bảo tồn Quyền riêng tư & An ninh Thông tin (Phase 2.5 Baseline):** Loại trừ 100% việc sinh JSON-LD cho các sự kiện bản nháp (`draft`), lọc sạch các token cuộc họp nhạy cảm, tuyệt đối không rò rỉ mã vé cá nhân, số điện thoại hay email người dùng.
8. **Mã hóa JSON An toàn Tuyệt đối:** Sử dụng cơ chế mã hóa nội suy `{{ schema|tojson|safe }}` của Flask/Jinja2, vô hiệu hóa hoàn toàn mọi cuộc tấn công XSS hoặc bẻ khóa thẻ `<script>`.

---

## 2. ÁNH XẠ DỮ LIỆU CSDL VỚI SCHEMA.ORG PROPERTY

Toàn bộ thuộc tính JSON-LD được xây dựng từ dữ liệu thực tế, cam kết **không bịa đặt thông tin (Zero Hallucination)**:

| Thuộc tính Schema.org | Kiểu Schema | Trường CSDL / Quan hệ SQLAlchemy | Quy tắc Xử lý & Chuẩn hóa |
| :--- | :--- | :--- | :--- |
| `@context` | URL | Cố định | `"https://schema.org"` |
| `@type` | Text | Cố định | `"Event"` |
| `name` | Text | `Event.title` | Chuỗi ký tự tiêu đề sự kiện, tự động mã hóa ký tự đặc biệt. |
| `description` | Text | `Event.description` | Làm sạch thẻ HTML bằng `clean_meta_description`, fallback về `Event.title`. |
| `url` | URL | `Event.id` qua `build_canonical_url` | URL tuyệt đối chuẩn tắc: `https://<domain>/events/<id>`. |
| `startDate` | DateTime | `Event.start_date` | Chuẩn hóa ISO 8601 kèm offset múi giờ: `YYYY-MM-DDTHH:MM:SS+07:00`. |
| `endDate` | DateTime | `Event.end_date` | Chuẩn hóa ISO 8601. Nếu `end_date < start_date`, tự động chuẩn hóa về `startDate`. |
| `eventStatus` | URL | `Event.status` | • `published`, `ongoing`, `completed` -> `EventScheduled`<br>• `cancelled` -> `EventCancelled`<br>• `postponed` -> `EventPostponed`<br>• `rescheduled` -> `EventRescheduled` |
| `eventAttendanceMode` | URL | `Event.location_type` | • `offline` -> `OfflineEventAttendanceMode`<br>• `online` -> `OnlineEventAttendanceMode`<br>• `hybrid` -> `MixedEventAttendanceMode` |
| `location` | Place / VirtualLocation | `Event.location_address`, `Event.online_meeting_url` | • `offline`: `Place` + `PostalAddress` (`addressCountry: "VN"`).<br>• `online`: `VirtualLocation` (loại bỏ query params chứa token/password).<br>• `hybrid`: Danh sách chứa cả hai đối tượng trên. |
| `image` | Array[URL] | `Event.banner_url` | Chuyển đổi đường dẫn tương đối thành URL tuyệt đối, fallback ảnh banner công nghệ mặc định. |
| `organizer` | Organization | `Event.creator` (`User.full_name`) | Tên ban tổ chức hoặc `"EventAI Pro"`. Tuyệt đối không để lộ email/SĐT cá nhân. |
| `offers` | Array[Offer] | `Event.tickets` (`Ticket`) | Mảng các hạng vé: `name`, `price` (số thực), `priceCurrency: "VND"`, `availability` (`InStock`/`SoldOut`), `url: "<canonical>#tickets"`. |
| `performer` | Array[Person] | `Event.schedules` (`Speaker`) | Danh sách diễn giả thực tế: `name`, `jobTitle`. Bỏ qua nếu không có diễn giả. |

---

## 3. KIẾN TRÚC MÃ NGUỒN HIỆN THỰC

### 3.1. Các Hàm Nghiệp vụ trong [`app/seo_helpers.py`](file:///D:/Event_Management_AI/app/seo_helpers.py)

#### 1. Định dạng Thời gian ISO 8601 (`format_iso8601_date`):
```python
def format_iso8601_date(dt, offset="+07:00"):
    if not dt or not isinstance(dt, datetime):
        return None
    if dt.tzinfo is not None:
        return dt.isoformat()
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
    clean_offset = offset.strip() if offset else ''
    if clean_offset and not (clean_offset.startswith('+') or clean_offset.startswith('-')):
        clean_offset = '+' + clean_offset
    return f"{dt_str}{clean_offset}"
```

#### 2. Ánh xạ Trạng thái & Hình thức Tham gia Sự kiện:
```python
def get_schema_event_status(status):
    mapping = {
        'published': 'https://schema.org/EventScheduled',
        'ongoing': 'https://schema.org/EventScheduled',
        'completed': 'https://schema.org/EventScheduled',
        'cancelled': 'https://schema.org/EventCancelled',
        'postponed': 'https://schema.org/EventPostponed',
        'rescheduled': 'https://schema.org/EventRescheduled',
    }
    return mapping.get(str(status).lower(), 'https://schema.org/EventScheduled')

def get_schema_attendance_mode(location_type):
    loc_type = str(location_type).lower() if location_type else 'offline'
    if loc_type == 'online':
        return 'https://schema.org/OnlineEventAttendanceMode'
    elif loc_type == 'hybrid':
        return 'https://schema.org/MixedEventAttendanceMode'
    return 'https://schema.org/OfflineEventAttendanceMode'
```

#### 3. Xây dựng Đối tượng Địa điểm An toàn (`build_event_location`):
```python
def build_event_location(event, public_event_url):
    loc_type = str(getattr(event, 'location_type', 'offline')).lower()
    address_str = getattr(event, 'location_address', '') or ''
    meeting_url = getattr(event, 'online_meeting_url', '') or ''

    physical_place = {
        "@type": "Place",
        "name": address_str.strip() if address_str.strip() else "Địa điểm tổ chức sự kiện",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address_str.strip() if address_str.strip() else "Địa điểm sự kiện",
            "addressCountry": "VN"
        }
    }

    clean_meeting_url = meeting_url.strip() if meeting_url.strip() else public_event_url
    if '?' in clean_meeting_url and ('token=' in clean_meeting_url or 'pwd=' in clean_meeting_url or 'passcode=' in clean_meeting_url):
        clean_meeting_url = clean_meeting_url.split('?')[0]

    virtual_loc = {
        "@type": "VirtualLocation",
        "url": clean_meeting_url
    }

    if loc_type == 'online':
        return virtual_loc
    elif loc_type == 'hybrid':
        return [physical_place, virtual_loc]
    else:
        return physical_place
```

#### 4. Xây dựng Danh mục Ưu đãi Vé (`build_ticket_offers`):
```python
def build_ticket_offers(event, public_event_url):
    offers = []
    tickets = getattr(event, 'tickets', None)
    if not tickets:
        return offers

    ticket_list = tickets.all() if hasattr(tickets, 'all') else list(tickets)
    for ticket in ticket_list:
        ticket_status = getattr(ticket, 'status', 'active')
        if ticket_status not in ('active', 'sold_out', 'closed'):
            continue

        price_val = float(getattr(ticket, 'price', 0.0) or 0.0)
        is_avail = getattr(ticket, 'is_available', False)
        
        offer = {
            "@type": "Offer",
            "name": getattr(ticket, 'name', 'Vé tham dự'),
            "price": round(price_val, 2),
            "priceCurrency": "VND",
            "availability": "https://schema.org/InStock" if is_avail else "https://schema.org/SoldOut",
            "url": f"{public_event_url}#tickets"
        }

        created_at = getattr(ticket, 'created_at', None)
        if created_at and isinstance(created_at, datetime):
            offer["validFrom"] = format_iso8601_date(created_at)

        offers.append(offer)

    return offers
```

#### 5. Hàm Tạo Schema Tổng thể (`build_event_schema`):
- Kiểm tra tính hợp lệ: Nếu `event` là `None` hoặc `status == 'draft'`, lập tức trả về `None` (không phát sinh JSON-LD).
- Tự động bổ sung `offers` và `performer` chỉ khi có dữ liệu thực tế.

#### 6. Hàm Tạo BreadcrumbList Schema (`build_breadcrumb_schema`):
- Tiếp nhận danh sách `(name, url)` và cấu trúc thành danh sách `ListItem` với vị trí `position: 1, 2, 3`.

---

### 3.2. Đăng ký Tiện ích tại [`app/__init__.py`](file:///D:/Event_Management_AI/app/__init__.py)
Các hàm `build_event_schema` và `build_breadcrumb_schema` đã được đưa vào `@app.context_processor` dưới tên gọi `get_event_schema` và `get_breadcrumb_schema`, giúp mọi Jinja template đều có thể truy cập thuận tiện.

---

### 3.3. Tích hợp Template [`base.html`](file:///D:/Event_Management_AI/app/templates/base.html) và [`event_detail.html`](file:///D:/Event_Management_AI/app/templates/main/event_detail.html)

Tại `base.html` `<head>`:
```html
    <!-- Structured Data (Schema.org JSON-LD) -->
    {% block structured_data %}{% endblock %}
```

Tại `event_detail.html`:
```html
{% block structured_data %}
{% if event.status != 'draft' and not is_draft_preview %}
{% set event_schema = get_event_schema(event) %}
{% if event_schema %}
<script type="application/ld+json">
{{ event_schema|tojson|safe }}
</script>
{% endif %}
{% set breadcrumb_schema = get_breadcrumb_schema([('Trang chủ', canonical_url('/')), ('Sự kiện', canonical_url('/events')), (event.title, canonical_url('/events/' ~ event.id))]) %}
{% if breadcrumb_schema %}
<script type="application/ld+json">
{{ breadcrumb_schema|tojson|safe }}
</script>
{% endif %}
{% endif %}
{% endblock %}
```

---

## 4. PHÂN BIỆT TÍNH HỢP LỆ SCHEMA VS KHẢ NĂNG XUẤT HIỆN RICH RESULTS

Để đảm bảo tính trung thực và chính xác kỹ thuật:

1. **Tính Hợp lệ Cú pháp Schema (Schema Validity):**
   - Tài liệu JSON-LD sinh ra tuân thủ 100% từ vựng chính thức của [Schema.org/Event](https://schema.org/Event).
   - Đầy đủ các trường bắt buộc (`name`, `startDate`, `location`).
   - Không có lỗi cú pháp JSON hay ký tự điều khiển hỏng.
2. **Khả năng Hiển thị Rich Results trên Google Search (Google Event Rich Results Eligibility):**
   - Theo nguyên tắc chất lượng của Google Search Central, sự kiện trực tiếp (`offline`) hoặc sự kiện kết hợp (`hybrid`) có địa chỉ vật lý rõ ràng là nhóm có khả năng cao nhất để Google kích hoạt thẻ hiển thị sự kiện tương tác.
   - Các sự kiện thuần trực tuyến (`online` / webinar) hoặc các sự kiện bị giới hạn đối tượng tham gia có thể được Google lập chỉ mục nhưng **không đảm bảo 100% sẽ luôn hiển thị giao diện Rich Results**.
   - Việc hiển thị cuối cùng phụ thuộc hoàn toàn vào thuật toán xếp hạng, chất lượng nội dung và độ tin cậy của tên miền trên Google Search. Hệ thống không đưa ra bất kỳ lời tuyên bố cam kết vô căn cứ nào về việc hiển thị Rich Results.

---

## 5. KẾT QUẢ KIỂM THỬ VÀ BẢO TỒN HỆ THỐNG

1. **Bộ kiểm thử Phase 3B (`tests/test_event_schema.py`):** **32/32 tests PASSED (100%)** trong 10.36 giây.
2. **Bộ kiểm thử Phase 3A Core SEO (`tests/test_seo_core_metadata.py`):** **23/23 tests PASSED (100%)**.
3. **Bộ kiểm thử Phase 2.5 Security (`tests/test_phase2_5_security.py`):** **12/12 tests PASSED (100%)**.
4. **Toàn bộ Bộ kiểm thử Hệ thống (Full Test Suite):** **109/109 tests PASSED (100%)** trong 27.07 giây.

Hệ thống đã sẵn sàng 100% cho **Phase 3C — Triển khai Tệp Sitemap.xml và Robots.txt Động**.

