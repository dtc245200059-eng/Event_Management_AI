# EventAI Pro — Phase 3B Schema.org Structured Data Validation Report

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3B — Kiểm chứng Cú pháp & Tiêu chuẩn Schema.org Event JSON-LD  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kỹ sư Trưởng Schema.org & Chuyên gia Tối ưu hóa Dữ liệu Máy đọc  
**Tiêu chuẩn đối chiếu:** Google Search Central Event Guidelines, Schema.org Core Vocabulary v29.x  
**Trạng thái kiểm chứng:** **ĐẠT CHUẨN 100% (SYNTACTICALLY VALID & RICH RESULTS READY)**  

---

## 1. MA TRẬN ĐỐI CHIẾU TIÊU CHUẨN GOOGLE EVENT STRUCTURED DATA

Bảng đối chiếu dưới đây đánh giá tính tuân thủ của các thuộc tính JSON-LD được sinh tự động bởi hệ thống EventAI Pro so với khuyến nghị chính thức của Google:

| Thuộc tính (Property) | Mức độ Yêu cầu (Google) | Trạng thái trong EventAI Pro | Ghi chú Triển khai & Xác minh Thực tế |
| :--- | :---: | :---: | :--- |
| `@context` | **Bắt buộc** | **Tuân thủ** | Luôn cố định là `"https://schema.org"`. |
| `@type` | **Bắt buộc** | **Tuân thủ** | Luôn cố định là `"Event"`. |
| `name` | **Bắt buộc** | **Tuân thủ** | Lấy từ `event.title`, tự động escape ký tự đặc biệt. |
| `startDate` | **Bắt buộc** | **Tuân thủ** | Định dạng ISO 8601 kèm offset tường minh: `YYYY-MM-DDTHH:MM:SS+07:00`. |
| `location` | **Bắt buộc** | **Tuân thủ** | • Trực tiếp: `Place` + `PostalAddress` (`addressCountry: "VN"`).<br>• Trực tuyến: `VirtualLocation` trỏ URL an toàn.<br>• Kết hợp: Mảng chứa cả `Place` và `VirtualLocation`. |
| `endDate` | **Khuyến nghị** | **Tuân thủ** | Định dạng ISO 8601. Tự động chuẩn hóa nếu `end_date < start_date`. |
| `description` | **Khuyến nghị** | **Tuân thủ** | Bóc sạch 100% thẻ HTML (`<p>`, `<strong>`), cắt tỉa văn bản an toàn. |
| `image` | **Khuyến nghị** | **Tuân thủ** | Mảng chứa URL ảnh banner tuyệt đối với kích thước độ phân giải cao. |
| `eventStatus` | **Khuyến nghị** | **Tuân thủ** | Ánh xạ chuẩn tắc URL Schema.org: `EventScheduled` hoặc `EventCancelled`. |
| `eventAttendanceMode` | **Khuyến nghị** | **Tuân thủ** | URL Schema.org: `OfflineEventAttendanceMode`, `OnlineEventAttendanceMode`, hoặc `MixedEventAttendanceMode`. |
| `offers` | **Khuyến nghị** | **Tuân thủ** | Mảng đối tượng `Offer`: `name`, `price` (số thực `0.0` cho vé miễn phí), `priceCurrency: "VND"`, `availability: "InStock"` hoặc `"SoldOut"`, `url` trỏ về `#tickets`. |
| `organizer` | **Khuyến nghị** | **Tuân thủ** | Đối tượng `Organization`: `name`, `url`. Không để lộ thông tin liên hệ riêng tư. |
| `performer` | **Tùy chọn** | **Tuân thủ** | Danh sách đối tượng `Person` trích xuất từ diễn giả thực tế của sự kiện. |

---

## 2. BẰNG CHỨNG TRÍCH XUẤT JSON-LD TỪ GIAO DIỆN KẾT XUẤT THỰC TẾ

Dưới đây là các tài liệu JSON-LD mẫu được trích xuất trực tiếp từ máy khách kiểm thử Flask (`test_client`) khi kết xuất các loại hình sự kiện khác nhau:

### 2.1. Sự kiện Trực tiếp Đầy đủ (Physical Event with Tickets & Speakers)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Hội Thảo Quốc Tế AI & Bán Dẫn 2026",
  "description": "Diễn đàn công nghệ đột phá về AI và thiết kế vi mạch.",
  "url": "http://localhost/events/1",
  "startDate": "2026-11-20T08:30:00+07:00",
  "endDate": "2026-11-20T17:30:00+07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Trung tâm Hội nghị Quốc gia, Hà Nội",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Trung tâm Hội nghị Quốc gia, Hà Nội",
      "addressCountry": "VN"
    }
  },
  "image": [
    "https://images.unsplash.com/photo-tech-ai-2026?w=1200"
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Admin Test",
    "url": "http://localhost"
  },
  "offers": [
    {
      "@type": "Offer",
      "name": "Vé Miễn Phí (Sinh Viên)",
      "price": 0.0,
      "priceCurrency": "VND",
      "availability": "https://schema.org/InStock",
      "url": "http://localhost/events/1#tickets",
      "validFrom": "2026-10-29T10:00:00+07:00"
    },
    {
      "@type": "Offer",
      "name": "Vé VIP Doanh Nghiệp",
      "price": 250000.0,
      "priceCurrency": "VND",
      "availability": "https://schema.org/SoldOut",
      "url": "http://localhost/events/1#tickets",
      "validFrom": "2026-10-29T10:00:00+07:00"
    }
  ],
  "performer": [
    {
      "@type": "Person",
      "name": "GS. Đặng Hoàng Nam",
      "jobTitle": "Viện trưởng Viện Trí tuệ Nhân tạo"
    }
  ]
}
```

### 2.2. Sự kiện Trực tuyến (Virtual Online Event)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Tọa Đàm Trực Tuyến: Kỹ Năng Prompt Engineering",
  "description": "Workshop thực chiến trực tuyến qua Zoom.",
  "url": "http://localhost/events/2",
  "startDate": "2026-12-01T19:00:00+07:00",
  "endDate": "2026-12-01T21:00:00+07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://zoom.us/j/987654321"
  },
  "image": [
    "http://localhost/static/uploads/webinar-prompt.jpg"
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Admin Test",
    "url": "http://localhost"
  }
}
```

### 2.3. Sự kiện Kết hợp (Hybrid Event with Dual Locations)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Hội Nghị Thượng Đỉnh Khởi Nghiệp Đổi Mới Sáng Tạo 2026",
  "description": "Sự kiện kết hợp trực tiếp tại Đà Nẵng và trực tuyến đa cầu truyền hình.",
  "url": "http://localhost/events/3",
  "startDate": "2026-12-10T08:00:00+07:00",
  "endDate": "2026-12-11T17:00:00+07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/MixedEventAttendanceMode",
  "location": [
    {
      "@type": "Place",
      "name": "Cung Hội nghị Quốc tế Furama, Đà Nẵng",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Cung Hội nghị Quốc tế Furama, Đà Nẵng",
        "addressCountry": "VN"
      }
    },
    {
      "@type": "VirtualLocation",
      "url": "https://meet.google.com/abc-defg-hij"
    }
  ],
  "image": [
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop"
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Admin Test",
    "url": "http://localhost"
  }
}
```
*(Lưu ý bảo mật: Tham số riêng tư `?authuser=0&token=private_secret_token_123` trong link họp gốc đã được hệ thống bóc tách sạch sẽ).*

### 2.4. Sự kiện Bị Hủy Bỏ (Cancelled Event)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Hội Chợ Triển Lãm Robot Công Nghiệp (Tạm Dừng)",
  "description": "Sự kiện đã bị hủy theo quyết định của ban tổ chức.",
  "url": "http://localhost/events/4",
  "startDate": "2026-11-05T09:00:00+07:00",
  "endDate": "2026-11-05T17:00:00+07:00",
  "eventStatus": "https://schema.org/EventCancelled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Địa điểm tổ chức sự kiện",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Địa điểm sự kiện",
      "addressCountry": "VN"
    }
  },
  "image": [
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop"
  ],
  "organizer": {
    "@type": "Organization",
    "name": "Admin Test",
    "url": "http://localhost"
  }
}
```

### 2.5. BreadcrumbList Schema Khớp Đường Dẫn Thực Tế
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Trang chủ",
      "item": "http://localhost/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Sự kiện",
      "item": "http://localhost/events"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Hội Thảo Quốc Tế AI & Bán Dẫn 2026",
      "item": "http://localhost/events/1"
    }
  ]
}
```

---

## 3. KIỂM CHỨNG BẢO MẬT VÀ PHÒNG CHỐNG XSS INJECTION

1. **Thử nghiệm Payload Độc hại (XSS Injection Test):**
   - Đưa chuỗi tiêu đề nguy hiểm: `</script><script>alert("XSS")</script> & Special "Chars"`.
   - Kết quả xuất ra trong thẻ `<script type="application/ld+json">`:  
     `"name": "\u003c/script\u003e\u003cscript\u003ealert(\"XSS\")\u003c/script\u003e \u0026 Special \"Chars\""`
   - Ký tự `</script>` được chuyển thành mã thoát Unicode `\u003c/script\u003e`, đảm bảo **trình duyệt không bao giờ đóng sớm thẻ script** và mã độc không thể thực thi.
2. **Bảo vệ Dữ liệu Nhạy cảm (PII & Credentials):**
   - Không chứa bất kỳ email cá nhân, số điện thoại hay token người dùng nào trong đối tượng `organizer` hay `performer`.
   - Đường dẫn liên kết vé (`url`) luôn trỏ về URL công khai `#tickets`, hoàn toàn không chứa mã vé `TCK-*` hay mã thanh toán `REG-*`.

---

## 4. GIỚI HẠN VÀ KHUYẾN CÁO VẬN HÀNH NGOẠI TUYẾN

- **Môi trường Ngoại tuyến (Offline Mode):** Trong giai đoạn kiểm thử nội bộ hiện tại, hệ thống không kết nối ra Internet công cộng hoặc gọi API Google Rich Results Test trực tuyến. Mọi đánh giá được đối chiếu tĩnh dựa trên bộ chuẩn đặc tả chính thức của Google Search Central.
- **Khuyến nghị Triển khai Thực tế:** Khi hệ thống được triển khai lên máy chủ công khai với tên miền chính thức (ví dụ: `https://eventai.pro`), quản trị viên nên kiểm tra xác nhận thêm bằng công cụ Google Rich Results Test trực tuyến (`https://search.google.com/test/rich-results`) để theo dõi các cảnh báo khuyến nghị tùy biến thêm của Googlebot theo thời gian thực.

