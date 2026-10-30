# EventAI Pro — Phase 3C XML Sitemap & Robots.txt Validation Report

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3C — Thẩm định Cú pháp & Tiêu chuẩn Kỹ thuật XML Sitemap & Robots.txt  
**Ngày thực hiện:** 29/10/2026  
**Tiêu chuẩn đối chiếu:** [Google Search Central Sitemaps Guidelines](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) & [Robots.txt Specifications](https://developers.google.com/search/docs/crawling-indexing/robots/intro)  
**Trạng thái thẩm định:** **100% TUÂN THỦ (PASS — KHÔNG CÓ CẢNH BÁO HOẶC LỖI)**  

---

## 1. THẨM ĐỊNH XML SITEMAP (`/sitemap.xml`)

### 1.1. Bảng Kiểm tra Tiêu chuẩn Kỹ thuật (Technical Specification Checklist)

| Tiêu chuẩn / Đặc tả | Yêu cầu Kỹ thuật Google / Sitemaps.org | Hiện thực hóa trong EventAI Pro | Kết quả Thẩm định | Bằng chứng Xác minh |
| :--- | :--- | :--- | :--- | :--- |
| **Giao thức & Định dạng** | XML 1.0, mã hóa UTF-8 | `<?xml version="1.0" encoding="UTF-8"?>` | **ĐẠT (PASS)** | Header XML hợp lệ ở dòng 1 |
| **Namespace Sitemaps** | `xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"` | Thẻ gốc `<urlset xmlns="...">` | **ĐẠT (PASS)** | Kiểm chứng qua `ElementTree` |
| **Thẻ Gốc (Root Tag)** | `<urlset>` chứa các thẻ con `<url>` | Cấu trúc phân cấp chuẩn `<urlset>` -> `<url>` | **ĐẠT (PASS)** | Phân tích cú pháp thành công |
| **MIME / Content-Type** | `application/xml` hoặc `text/xml` kèm charset UTF-8 | `application/xml; charset=utf-8` | **ĐẠT (PASS)** | `response.headers['Content-Type']` |
| **Bảo mật Header** | Chống đoán định MIME type | `X-Content-Type-Options: nosniff` | **ĐẠT (PASS)** | Đã kiểm thử HTTP header |
| **Bộ nhớ đệm (Cache)** | Cache tối ưu, cho phép CDN/Proxy lưu | `Cache-Control: public, max-age=3600` | **ĐẠT (PASS)** | Thời gian lưu đệm 1 giờ hợp lý |
| **Độ dài & Giới hạn** | Tối đa 50,000 URLs / 50MB dung lượng | Truy vấn `.limit(50000)` an toàn | **ĐẠT (PASS)** | Ngăn chặn quá tải tài nguyên |
| **Định dạng URL (`<loc>`)** | Bắt buộc là URL tuyệt đối có scheme (`http`/`https`) | `https://<domain>/path`, không có path tương đối | **ĐẠT (PASS)** | 100% URLs có scheme và host |
| **Khử Trùng lặp (Deduplication)**| Mỗi URL chỉ xuất hiện duy nhất 1 lần | Cơ chế lọc qua `seen_urls = set()` | **ĐẠT (PASS)** | Số URL bằng số tập hợp duy nhất |
| **Loại bỏ Query Params** | Không chứa tham số theo dõi (`utm_*`, `ref`, v.v.) | URL sạch sẽ, chuẩn tắc | **ĐẠT (PASS)** | 0% URL chứa dấu `?` |
| **Thoát Ký tự XML** | Ký tự `&`, `<`, `>`, `"`, `'` phải mã hóa entity | Tự động hóa qua `xml.sax.saxutils.escape` | **ĐẠT (PASS)** | Không phát sinh lỗi phân tích cú pháp |
| **Định dạng `<lastmod>`** | W3C Datetime format (`YYYY-MM-DD` hoặc ISO 8601) | `YYYY-MM-DD` sử dụng `Event.updated_at` | **ĐẠT (PASS)** | Định dạng đúng chuẩn quốc tế |
| **Tính Trung thực `<lastmod>`** | Không giả mạo ngày giờ hiện tại | Chỉ xuất hiện khi có `updated_at`; trang tĩnh bỏ qua | **ĐẠT (PASS)** | Trang tĩnh và sự kiện rỗng không có lastmod |

### 1.2. Mẫu XML Thực tế Xuất xưởng (Live Response Payload)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://eventai.pro/</loc>
  </url>
  <url>
    <loc>https://eventai.pro/events</loc>
  </url>
  <url>
    <loc>https://eventai.pro/events/1</loc>
    <lastmod>2026-10-15</lastmod>
  </url>
  <url>
    <loc>https://eventai.pro/events/2</loc>
    <lastmod>2026-10-20</lastmod>
  </url>
</urlset>
```

---

## 2. THẨM ĐỊNH TẬP TIN ROBOTS.TXT (`/robots.txt`)

### 2.1. Bảng Kiểm tra Cú pháp & Chỉ thị Bọ tìm kiếm

| Chỉ thị (Directive) | Mục đích Kỹ thuật | Phân tích Tính Hợp lệ theo Chuẩn Googlebot | Trạng thái |
| :--- | :--- | :--- | :--- |
| `User-agent: *` | Định danh nhóm quy tắc áp dụng cho mọi crawler. | Chuẩn xác, tuân thủ RFC 9309. | **HỢP LỆ** |
| `Allow: /` | Cho phép thu thập dữ liệu toàn bộ phần công khai của site. | Tạo đường dẫn mở mặc định cho các trang nội dung. | **HỢP LỆ** |
| `Allow: /static/css/` | Cho phép bọ tải stylesheet để render giao diện đồ họa. | Ngăn ngừa lỗi "Blocked Resources" trên Google Search Console. | **HỢP LỆ** |
| `Allow: /static/js/` | Cho phép bọ tải JavaScript để thực thi các thành phần động. | Cần thiết cho việc đánh giá trải nghiệm trang (Page Experience). | **HỢP LỆ** |
| `Disallow: /admin/` | Ngăn chặn truy cập phân vùng quản trị hệ thống. | Bảo vệ tài nguyên máy chủ, tối ưu ngân sách crawl budget. | **HỢP LỆ** |
| `Disallow: /checkin/` | Ngăn chặn truy cập giao diện quét mã QR vé. | Bảo vệ giao diện điều hành tại chỗ. | **HỢP LỆ** |
| `Disallow: /static/qr_codes/` | Ngăn chặn thu thập và lập chỉ mục ảnh mã QR cá nhân. | Lớp bảo vệ bổ trợ theo chiều sâu (Defense-in-depth). | **HỢP LỆ** |
| `Disallow: /api/` | Ngăn chặn thu thập các API nội bộ không dành cho con người. | Tránh tải dữ liệu thô JSON vô ích lên chỉ mục tìm kiếm. | **HỢP LỆ** |
| `Sitemap: https://eventai.pro/sitemap.xml` | Khai báo URL tuyệt đối của sơ đồ trang web. | Hướng dẫn crawler tự động tìm thấy sitemap mà không cần submit thủ công. | **HỢP LỆ** |

### 2.2. Kiểm tra Nguyên tắc Vàng về Tuyến Xác thực (`/auth/`)
- **Vấn đề thường gặp:** Nhiều lập trình viên thường đặt `Disallow: /auth/` vào robots.txt với suy nghĩ đơn giản là "không muốn trang đăng nhập xuất hiện trên Google".
- **Hậu quả tiêu cực:** Khi bị Disallow trong robots.txt, Googlebot **bị cấm tải trang**, do đó Googlebot **không thể đọc được thẻ `<meta name="robots" content="noindex, nofollow">`**. Nếu trên mạng có backlink trỏ tới `/auth/login`, Googlebot vẫn có thể hiển thị URL trần trụi `/auth/login` trên kết quả tìm kiếm kèm dòng chú thích "No information is available for this page".
- **Giải pháp chuẩn hóa trong EventAI Pro:** Tuyệt đối **KHÔNG đặt `Disallow: /auth/`**. Thay vào đó, để bot tự do truy cập trang `/auth/login` và `/auth/register` để đọc thẻ meta `<meta name="robots" content="noindex, nofollow">` đã hoàn thiện ở Phase 2.5, bảo đảm trang được xóa vĩnh viễn khỏi chỉ mục Google một cách sạch sẽ.

### 2.3. Mẫu Nội dung Robots.txt Thực tế Xuất xưởng
```text
User-agent: *
Allow: /
Allow: /static/css/
Allow: /static/js/

# Administrative & check-in interfaces
Disallow: /admin/
Disallow: /checkin/

# Defense-in-depth: Private QR ticket assets
Disallow: /static/qr_codes/

# Internal API endpoints
Disallow: /api/

Sitemap: https://eventai.pro/sitemap.xml
```

---

## 3. ĐỐI CHIẾU DANH MỤC URL (URL INVENTORY RECONCILIATION)

| Nhóm Tài nguyên Tuyến (Route Group) | Đường dẫn Tuyến | Xuất hiện trong Sitemap? | Chỉ thị Robots.txt | Chỉ thị Thẻ Meta Robots | Ghi chú Phân loại SEO |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Trang chủ** | `/` | **CÓ** | `Allow: /` | `index, follow` | Trang điều hướng trung tâm |
| **Danh mục Sự kiện** | `/events` | **CÓ** | `Allow: /` | `index, follow` | Trang danh mục chính |
| **Chi tiết Sự kiện Phát hành** | `/events/<id>` (`published`) | **CÓ** | `Allow: /` | `index, follow` | Trang chi tiết công khai |
| **Chi tiết Sự kiện Đang diễn ra**| `/events/<id>` (`ongoing`) | **CÓ** | `Allow: /` | `index, follow` | Trang chi tiết công khai |
| **Chi tiết Sự kiện Hoàn thành** | `/events/<id>` (`completed`) | **CÓ** | `Allow: /` | `index, follow` | Trang tư liệu sự kiện |
| **Chi tiết Sự kiện Bản nháp** | `/events/<id>` (`draft`) | **KHÔNG** | `Allow: /` | `noindex, follow` (Preview) / 404 | Sự kiện nội bộ chưa công bố |
| **Chi tiết Sự kiện Đã hủy** | `/events/<id>` (`cancelled`)| **KHÔNG** | `Allow: /` | `noindex, follow` | Thông báo đã hủy, cấm index |
| **Đăng nhập Hệ thống** | `/auth/login` | **KHÔNG** | Không chặn (Allowed) | `noindex, nofollow` | Loại trừ an ninh danh tính |
| **Đăng ký Tài khoản** | `/auth/register` | **KHÔNG** | Không chặn (Allowed) | `noindex, nofollow` | Loại trừ an ninh danh tính |
| **Quản trị Dashboard** | `/admin/*` | **KHÔNG** | `Disallow: /admin/` | N/A (Yêu cầu Login Admin) | Khu vực quản trị tối mật |
| **Quét Mã Check-in** | `/checkin/*` | **KHÔNG** | `Disallow: /checkin/` | N/A (Yêu cầu Login Staff) | Phân vùng kiểm soát vé |
| **Ảnh Mã QR Vé** | `/static/qr_codes/*` | **KHÔNG** | `Disallow: /static/qr_codes/` | N/A | Dữ liệu cá nhân người dùng |
| **Tuyến API Hệ thống** | `/api/*` | **KHÔNG** | `Disallow: /api/` | N/A | Giao tiếp API dữ liệu máy |

---

## 4. KẾT LUẬN THẨM ĐỊNH

Cả hai endpoint `/sitemap.xml` và `/robots.txt` đã được triển khai đạt chuẩn cao nhất của ngành công nghiệp công nghệ thông tin và Technical SEO. Hệ thống giải quyết trọn vẹn sự cân bằng tinh tế giữa **khả năng phát hiện nội dung của cỗ máy tìm kiếm** và **yêu cầu bảo mật an ninh dữ liệu người dùng**.

