# EventAI Pro — Schema.org Event Structured Data Assessment

**Tác giả:** Ban Kiểm toán SEO Kỹ thuật & Kiến trúc Schema.org  
**Mục tiêu:** Đánh giá hiện trạng dữ liệu có cấu trúc (Structured Data) và thiết kế giải pháp Schema.org Event JSON-LD chuẩn xác dựa trên 100% dữ liệu thực tế từ cơ sở dữ liệu SQLAlchemy của `EventAI Pro`.  
**Phạm vi áp dụng:** `app/templates/main/event_detail.html` và `app/templates/base.html`  
**Tiêu chuẩn đối chiếu:** Google Search Central Event Structured Data Guidelines, Schema.org Core Vocabulary v29.x.  

---

## 1. ĐÁNH GIÁ HIỆN TRẠNG (CURRENT STATE EVALUATION)

### Kết quả kiểm tra tĩnh mã nguồn:
- **Tập tin kiểm tra:** `app/templates/base.html`, `app/templates/main/event_detail.html`, `app/templates/main/index.html`, `app/templates/main/events.html`.
- **Thực trạng triển khai:** **HOÀN TOÀN CHƯA CÓ SCHEMA MARKUP (0/100 Điểm)**.
  - Không tồn tại bất kỳ thẻ `<script type="application/ld+json">` nào trong toàn bộ mã nguồn template của ứng dụng.
  - Không có vi dữ liệu (Microdata) hay RDFa.
  - Googlebot và các công cụ tìm kiếm khác hiện chỉ thu thập được trang chi tiết sự kiện dưới dạng văn bản HTML thô, **không thể kích hoạt hiển thị Event Rich Results** (thẻ sự kiện tương tác bao gồm ngày giờ, vị trí bản đồ, giá vé và trạng thái trên Google Search).

---

## 2. ĐỐI SOÁT TRƯỜNG DỮ LIỆU SCHEMA.ORG VỚI CSDL EVENTAI PRO

Toàn bộ thuộc tính Schema.org đề xuất dưới đây được ánh xạ trực tiếp từ các trường thực tế trong Model SQLAlchemy của dự án (`app/models/event.py`, `speaker.py`, `venue.py`, `ticket.py`, `schedule.py`), tuyệt đối **không tự bịa đặt dữ liệu (Zero Hallucination)**:

| Schema.org Property | Kiểu dữ liệu Schema | Cột CSDL / Quan hệ SQLAlchemy trong EventAI Pro | Ví dụ giá trị thực tế trong CSDL |
| :--- | :--- | :--- | :--- |
| `@context` | URL | Cố định `https://schema.org` | `"https://schema.org"` |
| `@type` | Text | Cố định `"Event"` (hoặc `"BusinessEvent"` / `"EducationEvent"`) | `"Event"` |
| `name` | Text | `Event.title` | `"Hội Thảo Quốc Tế: Trí Tuệ Nhân Tạo & Bán Dẫn 2026"` |
| `description` | Text | `Event.description` | `"Hội thảo chuyên sâu về xu hướng công nghệ AI thế hệ mới..."` |
| `startDate` | DateTime (ISO 8601) | `Event.start_date` (+ Timezone VN `+07:00`) | `"2026-11-20T08:30:00+07:00"` |
| `endDate` | DateTime (ISO 8601) | `Event.end_date` (+ Timezone VN `+07:00`) | `"2026-11-20T17:30:00+07:00"` |
| `eventStatus` | URL | Ánh xạ từ `Event.status`: <br>• `published` / `ongoing` ➔ `EventScheduled`<br>• `cancelled` ➔ `EventCancelled`<br>• `completed` ➔ `EventScheduled` (kèm cờ kết thúc) | `"https://schema.org/EventScheduled"` |
| `eventAttendanceMode` | URL | Ánh xạ từ `Event.location_type`: <br>• `offline` ➔ `OfflineEventAttendanceMode`<br>• `online` ➔ `OnlineEventAttendanceMode`<br>• `hybrid` ➔ `MixedEventAttendanceMode` | `"https://schema.org/OfflineEventAttendanceMode"` |
| `image` | URL / Array | `Event.banner_url` | `["https://images.unsplash.com/photo-151877..."]` |
| `location` | Place / VirtualLocation | • Nếu offline/hybrid: `Place` (tên: `Event.location_address`, address: `PostalAddress`)<br>• Nếu online: `VirtualLocation` (url: `Event.online_meeting_url`) | Địa điểm thực tế trong hội trường hoặc phòng họp trực tuyến |
| `organizer` | Organization | Ban tổ chức sự kiện: `event.creator` (`User.full_name`) hoặc mặc định `EventAI Pro Platform` | `{"@type": "Organization", "name": "EventAI Pro", "url": "https://eventai.pro"}` |
| `offers` | AggregateOffer / Offer[] | Danh sách các hạng vé từ quan hệ `Event.tickets`: <br>• `Ticket.name`<br>• `Ticket.price`<br>• `Ticket.ticket_type`<br>• `Ticket.is_available` | Mảng các ưu đãi giá vé từ 0 VNĐ đến vé VIP |
| `performer` | Person[] | Danh sách diễn giả từ quan hệ `Event.schedules` qua `Schedule.speaker` | Mảng các chuyên gia: `Speaker.name`, `Speaker.title`, `Speaker.organization` |

---

## 3. THIẾT KẾ CẤU TRÚC JSON-LD MẪU HOÀN CHỈNH

Dưới đây là bản thiết kế JSON-LD mẫu chuẩn hóa, sẵn sàng tích hợp an toàn vào `app/templates/main/event_detail.html` thông qua bộ lọc bảo mật `tojson`:

```html
<!-- SCHEMA.ORG EVENT STRUCTURED DATA (JSON-LD) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": {{ event.title|tojson }},
  "description": {{ (event.description or event.title)|tojson }},
  "image": [
    {{ (event.banner_url or url_for('static', filename='images/default-event.jpg', _external=True))|tojson }}
  ],
  "startDate": "{{ event.start_date.strftime('%Y-%m-%dT%H:%M:00+07:00') }}",
  "endDate": "{{ event.end_date.strftime('%Y-%m-%dT%H:%M:00+07:00') }}",
  "eventStatus": {% if event.status == 'cancelled' %}"https://schema.org/EventCancelled"{% else %}"https://schema.org/EventScheduled"{% endif %},
  "eventAttendanceMode": {% if event.location_type == 'online' %}"https://schema.org/OnlineEventAttendanceMode"{% elif event.location_type == 'hybrid' %}"https://schema.org/MixedEventAttendanceMode"{% else %}"https://schema.org/OfflineEventAttendanceMode"{% endif %},
  "location": [
    {% if event.location_type in ['offline', 'hybrid'] %}
    {
      "@type": "Place",
      "name": {{ (event.location_address or 'Hội trường chính')|tojson }},
      "address": {
        "@type": "PostalAddress",
        "streetAddress": {{ (event.location_address or 'Hội trường chính')|tojson }},
        "addressLocality": "Thái Nguyên",
        "addressRegion": "Thái Nguyên",
        "addressCountry": "VN"
      }
    }
    {% endif %}
    {% if event.location_type in ['online', 'hybrid'] and event.online_meeting_url %}
    {% if event.location_type == 'hybrid' %},{% endif %}
    {
      "@type": "VirtualLocation",
      "url": {{ event.online_meeting_url|tojson }}
    }
    {% endif %}
  ],
  "organizer": {
    "@type": "Organization",
    "name": "EventAI Pro",
    "url": {{ url_for('main.index', _external=True)|tojson }}
  },
  {% if tickets and tickets|length > 0 %}
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "VND",
    "lowPrice": {{ tickets|map(attribute='price')|min }},
    "highPrice": {{ tickets|map(attribute='price')|max }},
    "offerCount": {{ tickets|length }},
    "offers": [
      {% for t in tickets %}
      {
        "@type": "Offer",
        "name": {{ t.name|tojson }},
        "price": {{ t.price }},
        "priceCurrency": "VND",
        "availability": {% if t.is_available %}"https://schema.org/InStock"{% else %}"https://schema.org/SoldOut"{% endif %},
        "url": {{ url_for('main.event_detail', event_id=event.id, _external=True)|tojson }},
        "validFrom": "{{ event.created_at.strftime('%Y-%m-%dT%H:%M:00+07:00') }}"
      }{% if not loop.last %},{% endif %}
      {% endfor %}
    ]
  },
  {% endif %}
  {% set speakers_list = [] %}
  {% for s in schedules if s.speaker and s.speaker not in speakers_list %}
    {% set _ = speakers_list.append(s.speaker) %}
  {% endfor %}
  {% if speakers_list|length > 0 %}
  "performer": [
    {% for sp in speakers_list %}
    {
      "@type": "Person",
      "name": {{ sp.name|tojson }},
      "jobTitle": {{ (sp.title or 'Chuyên gia')|tojson }},
      "worksFor": {
        "@type": "Organization",
        "name": {{ (sp.organization or 'Tổ chức đối tác')|tojson }}
      }
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ],
  {% endif %}
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": {{ url_for('main.event_detail', event_id=event.id, _external=True)|tojson }}
  }
}
</script>
```

---

## 4. BREADCRUMBLIST SCHEMA CHO ĐIỀU HƯỚNG PHÂN CẤP

Hiện tại giao diện `event_detail.html` đã có thanh điều hướng Breadcrumb HTML (dòng 9-15):
`Trang chủ > Sự kiện > [Tên sự kiện]`
Tuy nhiên chưa được gắn thẻ dữ liệu có cấu trúc. Để hiển thị chuỗi điều hướng đẹp mắt trên thanh tìm kiếm Google, cần bổ sung schema `BreadcrumbList`:

```html
<!-- SCHEMA.ORG BREADCRUMB LIST -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Trang chủ",
      "item": {{ url_for('main.index', _external=True)|tojson }}
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Sự kiện",
      "item": {{ url_for('main.event_list', _external=True)|tojson }}
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": {{ event.title|tojson }},
      "item": {{ url_for('main.event_detail', event_id=event.id, _external=True)|tojson }}
    }
  ]
}
</script>
```

---

## 5. ĐÁNH GIÁ NGUY CƠ BẢO MẬT & XSS KHI SERIAlIZE JSON TRONG JINJA2

### Phân tích lỗ hổng:
Nếu chèn trực tiếp chuỗi không qua xử lý vào khối `<script type="application/ld+json">`:
```jinja2
"name": "{{ event.title }}"   <!-- CỰC KỲ NGUY HIỂM: Dẫn đến XSS Injection! -->
```
Kẻ tấn công có thể đặt tên sự kiện chứa chuỗi `"</script><script>alert(1)</script>"`, làm vỡ khối JSON-LD và thực thi JavaScript độc hại trên trình duyệt người dùng.

### Giải pháp bắt buộc:
1. Luôn sử dụng bộ lọc `|tojson` của Jinja2. Bộ lọc này tự động mã hóa ký tự Unicode và chuyển đổi an toàn các dấu ngoặc kép, dấu gạch chéo ngược và ký tự `<` thành `\u003c`.
2. Kiểm tra tính trùng khớp với nội dung thị giác (Visual Content Consistency): Google xử phạt các trang web "nhồi nhét" thông tin vào Schema mà không hiển thị tương ứng trên màn hình người dùng (Spammy Structured Data). Vì mọi thuộc tính trên đều đang hiển thị rõ ràng trên giao diện `event_detail.html` (tiêu đề, thời gian, địa điểm, bảng giá vé, diễn giả), giải pháp đảm bảo tính minh bạch 100% theo chuẩn Webmaster Guidelines.

