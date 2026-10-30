# EventAI Pro — SEO Evidence Map & Findings Prioritization

**Ngày lập:** 29/10/2026  
**Phương pháp:** Kiểm toán tĩnh mã nguồn thực tế (Static Source Code Audit)  
**Phân loại mức độ nghiêm trọng:**
- **P0 — Critical (Khẩn cấp):** Ảnh hưởng nghiêm trọng đến bảo mật, rò rỉ thông tin xác thực hoặc tê liệt khả năng thu thập dữ liệu của bot tìm kiếm.
- **P1 — High (Quan trọng):** Thiếu hụt các thành phần SEO cốt lõi (Schema Event, Meta động, Canonical, Social Tags, Cấu trúc thẻ tiêu đề).
- **P2 — Medium (Trung bình):** Tối ưu hóa hiệu năng tải trang, Core Web Vitals (LCP, CLS), lãng phí tài nguyên CPU/mạng.
- **P3 — Low (Thấp):** Các cải tiến nhỏ về khả năng tiếp cận (Accessibility), văn bản thay thế hình ảnh (Alt text), nhãn breadcrumb.

---

## BẢNG MA TRẬN BẰNG CHỨNG PHÁT HIỆN TOÀN BỘ HỆ THỐNG

| ID | Danh mục | Mức độ | Tệp nguồn & Vị trí | Tuyến đường / Template | Tình trạng kiểm toán |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **SEO-FND-001** | Security / Privacy | **P0** | `app/templates/auth/login.html#L16-L21` | `/auth/login` | **Confirmed Defect** |
| **SEO-FND-002** | Technical Crawl | **P0** | `app/routes/main.py`, Root | `/robots.txt`, `/sitemap.xml` | **Confirmed Defect** |
| **SEO-FND-003** | Schema Structured Data | **P1** | `app/templates/main/event_detail.html` | `/events/<int:event_id>` | **Confirmed Defect** |
| **SEO-FND-004** | Security / Privacy | **P1** | `app/__init__.py#L28`, `app/routes/tickets.py#L16-L26` | `/static/qr_codes/*.svg` | **Confirmed Defect** |
| **SEO-FND-005** | Metadata / Indexing | **P1** | `app/templates/base.html#L24-L28` | Toàn bộ ứng dụng | **Confirmed Defect** |
| **SEO-FND-006** | Social Sharing | **P1** | `app/templates/base.html#L26-L31` | Toàn bộ ứng dụng | **Confirmed Defect** |
| **SEO-FND-007** | Content Hierarchy | **P1** | `app/templates/main/event_detail.html#L32`, `events.html#L9` | `/events`, `/events/<id>` | **Confirmed Defect** |
| **SEO-FND-008** | Indexability Policy | **P1** | `app/routes/main.py#L89-L113` | `/events/<int:event_id>` | **Confirmed Defect** |
| **SEO-FND-009** | Performance / CWV | **P2** | `app/templates/main/event_detail.html#L21`, `index.html#L60` | `/`, `/events/<id>` | **Confirmed Defect** |
| **SEO-FND-010** | Performance / CPU | **P2** | `app/static/js/main.js#L171-L186` | `/` (Trang chủ) | **Confirmed Defect** |
| **SEO-FND-011** | Performance / CSS | **P2** | `app/templates/base.html#L33-L35` | Toàn bộ ứng dụng | **Confirmed Defect** |
| **SEO-FND-012** | Performance / JS | **P2** | `app/templates/base.html#L616` | Toàn bộ ứng dụng | **Confirmed Defect** |
| **SEO-FND-013** | Technical / Crawl | **P2** | `app/templates/main/index.html#L241-L256` | `/` (Trang chủ) | **Confirmed Defect** |
| **SEO-FND-014** | A11y / Images | **P3** | `app/templates/main/event_detail.html#L120` | `/events/<id>` | **Confirmed Defect** |
| **SEO-FND-015** | Technical Robots | **P3** | `app/templates/errors/*.html` | `/errors/*` (400, 403, 404, 500) | **Confirmed Defect** |

---

## HỒ SƠ CHI TIẾT TỪNG PHÁT HIỆN KIỂM TOÁN

---

### [SEO-FND-001] Lộ Mật khẩu Quản trị trên Trang Đăng nhập Công khai Không có Noindex
- **Danh mục:** An ninh thông tin & Quyền riêng tư (Security / Privacy)
- **Mức độ:** **P0 — Critical**
- **Tệp nguồn ảnh hưởng:** `app/templates/auth/login.html` (Dòng 16–21)
- **Bằng chứng trích xuất từ mã nguồn:**
  ```html
  <!-- Quick Accounts Hint for Demo -->
  <div class="p-3 mb-4 rounded-3 small" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular);">
      <strong class="text-primary d-block mb-1"><i class="fa-solid fa-key me-1"></i> Tài khoản Demo có sẵn:</strong>
      <div>• <strong>Admin:</strong> <code>admin</code> / <code>Admin@123</code></div>
      <div>• <strong>Staff Check-in:</strong> <code>staff1</code> / <code>Staff@123</code></div>
      <div>• <strong>Khách mời:</strong> <code>attendee1</code> / <code>User@123</code></div>
  </div>
  ```
- **Tại sao đây là vấn đề nghiêm trọng:**
  Trang `/auth/login` không có chỉ thị `noindex` và chưa được chặn trong `robots.txt`. Đoạn văn bản chứa tài khoản quản trị `admin / Admin@123` sẽ bị Google thu thập và xuất hiện trực tiếp trong thẻ mô tả kết quả tìm kiếm (Google Snippet), cho phép bất kỳ ai cũng có thể đăng nhập vào hệ thống quản trị.
- **Biện pháp khắc phục khuyến nghị:**
  1. Bổ sung `<meta name="robots" content="noindex, nofollow">` vào `auth/login.html`.
  2. Bọc khối gợi ý demo bằng điều kiện `{% if config.DEBUG %}...{% endif %}` để tự động ẩn khi triển khai môi trường sản xuất.
- **Lợi ích SEO đạt được:** Ngăn chặn khủng hoảng an ninh thông tin, loại bỏ nội dung rác khỏi trang chỉ mục tìm kiếm.
- **Độ phức tạp hiện thực:** Thấp (15 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-002] Không Tồn Tại `robots.txt` và `sitemap.xml` (Trả về HTTP 404)
- **Danh mục:** Thu thập dữ liệu kỹ thuật (Technical Crawlability)
- **Mức độ:** **P0 — Critical**
- **Tệp nguồn ảnh hưởng:** `app/routes/main.py`, thư mục gốc dự án
- **Bằng chứng:**
  Kiểm tra hệ thống tệp và bảng định tuyến cho thấy không có bất kỳ tệp tĩnh hay route nào cho `/robots.txt` và `/sitemap.xml`. Khi crawler truy cập, hàm `register_error_handlers(app)` trả về giao diện lỗi `errors/404.html` kèm HTTP 404.
- **Tại sao đây là vấn đề nghiêm trọng:**
  - Googlebot không có tệp hướng dẫn ranh giới thu thập dữ liệu.
  - Các sự kiện mới được thêm vào CSDL không thể được phát hiện tự động nếu không có `sitemap.xml` động.
- **Biện pháp khắc phục khuyến nghị:**
  Tạo 2 routes tĩnh/động trong `app/routes/main.py`:
  - Route `/robots.txt`: Trả về nội dung chính sách text thuần.
  - Route `/sitemap.xml`: Truy vấn các sự kiện published từ `Event` model và sinh XML chuẩn với `lastmod`.
- **Lợi ích SEO đạt được:** Tăng tốc độ lập chỉ mục sự kiện mới, định hướng chính xác crawl budget của bot tìm kiếm.
- **Độ phức tạp hiện thực:** Trung bình (1–2 giờ).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-003] Hoàn Toàn Vắng Bóng Dữ Liệu Có Cấu Trúc Schema.org Event
- **Danh mục:** Rich Snippets & Dữ liệu có cấu trúc (Schema Markup)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/templates/main/event_detail.html`
- **Bằng chứng:**
  Tìm kiếm thẻ `<script type="application/ld+json">` trong toàn bộ thư mục `app/templates/` trả về kết quả 0.
- **Tại sao đây là vấn đề:**
  Google Search cung cấp giao diện hiển thị chuyên biệt cho Sự kiện (Event Rich Results) với ngày giờ, bản đồ địa điểm và nút mua vé nổi bật trên di động. Việc thiếu Schema khiến các sự kiện của EventAI Pro mất toàn bộ lợi thế hiển thị nổi bật trước đối thủ cạnh tranh.
- **Biện pháp khắc phục khuyến nghị:**
  Tích hợp khối JSON-LD chuẩn hóa sử dụng dữ liệu thực tế từ `Event`, `Ticket`, `Schedule`, `Speaker` vào `event_detail.html` (kèm bộ lọc an toàn `|tojson`).
- **Lợi ích SEO đạt được:** Đạt điều kiện xuất hiện trên hộp tìm kiếm Event Carousels của Google, nâng cao tỷ lệ nhấp chuột tự nhiên (CTR).
- **Độ phức tạp hiện thực:** Trung bình (2 giờ).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-004] Thư Mục Chứa Ảnh Mã QR Vé SVG Có Thể Truy Cập Công Khai Không Xác Thực
- **Danh mục:** An ninh thông tin & Quyền riêng tư (Security / Privacy)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/__init__.py#L28`, `app/routes/tickets.py#L16-L26`, `app/routes/checkin.py#L213`
- **Bằng chứng mã nguồn:**
  `os.makedirs(os.path.join(app.static_folder, 'qr_codes'), exist_ok=True)`  
  Tệp SVG mã QR vé cá nhân (`TCK-001-...svg`) và thanh toán (`pay_REG-...svg`) được lưu trực tiếp vào thư mục tĩnh `static/qr_codes/`.
- **Tại sao đây là vấn đề:**
  Trình phục vụ tệp tĩnh của Flask không yêu cầu phiên đăng nhập. Nếu bot tìm kiếm hoặc kẻ tấn công quét thư mục này, dữ liệu vé có thể bị index lên Google Images hoặc bị lạm dụng để check-in giả mạo.
- **Biện pháp khắc phục khuyến nghị:**
  - Chặn ngay trong `robots.txt`: `Disallow: /static/qr_codes/`.
  - Gắn tiêu đề `X-Robots-Tag: noindex, nofollow` cho mọi yêu cầu tới `/static/qr_codes/*`.
- **Lợi ích SEO đạt được:** Ngăn chặn rò rỉ dữ liệu vé và bảo vệ uy tín nền tảng sự kiện.
- **Độ phức tạp hiện thực:** Thấp (30 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-005] Thẻ Meta Description Bị Hardcode Tĩnh và Thiếu Thẻ Canonical Link
- **Danh mục:** Siêu dữ liệu trang (Metadata & Crawling)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/templates/base.html#L24-L28`
- **Bằng chứng mã nguồn:**
  ```html
  <title>{% block title %}{{ app_title }}{% endblock %}</title>
  <meta name="description" content="Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo EventAI Pro.">
  ```
  Không có khối `{% block meta_description %}` và hoàn toàn không có thẻ `<link rel="canonical">`.
- **Tại sao đây là vấn đề:**
  - Mọi trang trong ứng dụng (từ trang chủ, danh sách sự kiện đến từng trang chi tiết sự kiện cụ thể) đều có chung một đoạn meta description giống hệt nhau, gây lỗi Duplicate Meta Descriptions trên diện rộng.
  - Thiếu thẻ Canonical dẫn đến việc các tham số URL như `/events?category=AI&page=1` bị Googlebot xem là các trang trùng lặp nội dung.
- **Biện pháp khắc phục khuyến nghị:**
  Tạo các block Jinja2 linh hoạt trong `base.html`:
  - `{% block meta_description %}` cho phép trang chi tiết đưa trích đoạn mô tả sự kiện thực tế vào.
  - `{% block canonical %}` tự động sinh URL chuẩn hóa với `request.base_url`.
- **Lợi ích SEO đạt được:** Loại bỏ cảnh báo trùng lặp nội dung, cải thiện độ liên quan ngữ nghĩa của từng trang sự kiện trên SERP.
- **Độ phức tạp hiện thực:** Thấp (45 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-006] Vắng Mặt Toàn Bộ Thẻ Chia Sẻ Mạng Xã Hội (Open Graph & Twitter Cards)
- **Danh mục:** Chia sẻ mạng xã hội & Tối ưu hóa lan truyền (Social SEO)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/templates/base.html`
- **Bằng chứng:**
  Không tìm thấy các thẻ `og:title`, `og:description`, `og:image`, `og:url` hay `twitter:card` trong `<head>`.
- **Tại sao đây là vấn đề:**
  Khi người dùng hoặc ban tổ chức sao chép liên kết sự kiện để chia sẻ lên Facebook, Zalo, LinkedIn, Twitter/X hay Telegram, ứng dụng sẽ không hiển thị ảnh banner sự kiện, tiêu đề bị cắt cụt và không có bản xem trước đồ họa (Rich Link Preview).
- **Biện pháp khắc phục khuyến nghị:**
  Bổ sung bộ thẻ Open Graph và Twitter Summary Large Image vào `base.html` và cho phép `event_detail.html` ghi đè ảnh banner thực tế của sự kiện.
- **Lợi ích SEO đạt được:** Tối ưu hóa trải nghiệm chia sẻ viral, tăng tỷ lệ nhấp từ các nền tảng mạng xã hội và tin nhắn.
- **Độ phức tạp hiện thực:** Thấp (45 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-007] Cấu Trúc Phân Cấp Thẻ Tiêu Đề Bị Lỗi (Thiếu Thẻ `<h1>`)
- **Danh mục:** Cấu trúc nội dung ngữ nghĩa (Semantic HTML & Heading Hierarchy)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/templates/main/event_detail.html#L32`, `app/templates/main/events.html#L9`
- **Bằng chứng mã nguồn:**
  - Tại `event_detail.html`: Tiêu đề sự kiện chính được đặt trong thẻ `<h2 class="mb-4" ...>{{ event.title }}</h2>` (Dòng 32). Toàn bộ trang chi tiết sự kiện **không hề có thẻ `<h1>`**. Sau đó nhảy cóc xuống thẻ `<h4>` (Dòng 91, 99) và `<h6>` (Dòng 114).
  - Tại `events.html`: Tiêu đề trang bắt đầu bằng `<h2 class="mb-2">Tất Cả Sự Kiện</h2>` (Dòng 9), thiếu hoàn toàn thẻ `<h1>`.
- **Tại sao đây là vấn đề:**
  Googlebot dựa vào cấu trúc heading từ `<h1>` đến `<h6>` để hiểu chủ đề trọng tâm của trang. Một trang chi tiết sự kiện không có thẻ `<h1>` là khiếm khuyết cơ bản về Semantic HTML.
- **Biện pháp khắc phục khuyến nghị:**
  Chuyển đổi tiêu đề chính của sự kiện trong `event_detail.html` thành thẻ `<h1 class="h2 mb-4">`, giữ nguyên định dạng CSS visual của Apple Design System mà chuẩn hóa ngữ nghĩa HTML.
- **Lợi ích SEO đạt được:** Cải thiện điểm số ngữ nghĩa HTML5, truyền tín hiệu từ khóa rõ ràng cho bot tìm kiếm.
- **Độ phức tạp hiện thực:** Rất thấp (15 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-008] Thiếu Kiểm Soát Chỉ Mục Đối Với Sự Kiện Bản Nháp (`draft`) và Đã Hủy (`cancelled`)
- **Danh mục:** Chính sách lập chỉ mục (Indexability Policy)
- **Mức độ:** **P1 — High**
- **Tệp nguồn ảnh hưởng:** `app/routes/main.py#L89-L113`
- **Bằng chứng mã nguồn:**
  `event = db.get_or_404(Event, event_id)` lấy trực tiếp bản ghi từ CSDL mà không kiểm tra trạng thái `event.status`.
- **Tại sao đây là vấn đề:**
  Nếu một sự kiện đang ở trạng thái bản nháp (`draft`) hoặc đã bị ban tổ chức hủy bỏ (`cancelled`), trang vẫn trả về mã 200 kèm nội dung đầy đủ nếu bot quét qua ID.
- **Biện pháp khắc phục khuyến nghị:**
  - Nếu `event.status == 'draft'`: Kiểm tra quyền sở hữu của người dùng hiện tại; nếu là khách vãng lai/bot, trả về HTTP 404.
  - Nếu `event.status == 'cancelled'`: Trả về thẻ `<meta name="robots" content="noindex">` để bot tự động gỡ khỏi chỉ mục.
- **Lợi ích SEO đạt được:** Làm sạch chỉ mục tìm kiếm, tránh đưa người dùng vào các sự kiện không còn hoạt động.
- **Độ phức tạp hiện thực:** Thấp (30 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-009] Thiếu Thuộc Tính Kích Thước Ảnh Gây Dịch Chuyển Bố Cục (CLS) và Thiếu Lazy Loading
- **Danh mục:** Hiệu năng & Trải nghiệm Trang (Core Web Vitals)
- **Mức độ:** **P2 — Medium**
- **Tệp nguồn ảnh hưởng:** `app/templates/main/event_detail.html#L21`, `index.html#L60, L146, L209`
- **Bằng chứng mã nguồn:**
  `<img src="{{ event.banner_url }}" alt="{{ event.title }}" class="w-100 h-100" style="...">`
  Các thẻ `<img>` không khai báo thuộc tính `width` và `height` rõ ràng trong HTML và không có `loading="lazy"` cho các ảnh nằm dưới màn hình đầu tiên (Below-the-fold).
- **Tại sao đây là vấn đề:**
  Trình duyệt không thể dự trù không gian hiển thị trước khi ảnh tải xong, gây hiện tượng nhảy giật khung hình (Cumulative Layout Shift — CLS cao). Ngoài ra, ảnh banner chính của sự kiện (LCP Element) chưa được gán cờ `fetchpriority="high"`.
- **Biện pháp khắc phục khuyến nghị:**
  - Bổ sung tỷ lệ khung hình `aspect-ratio` hoặc `width`/`height` cho các khung chứa ảnh.
  - Gán `fetchpriority="high"` cho banner sự kiện chính trên trang chi tiết.
  - Gán `loading="lazy"` và `decoding="async"` cho toàn bộ danh sách thẻ sự kiện bên dưới.
- **Lợi ích SEO đạt được:** Tối ưu hóa chỉ số Core Web Vitals (LCP và CLS), giúp trang đáp ứng tiêu chuẩn xếp hạng trải nghiệm trang của Google.
- **Độ phức tạp hiện thực:** Thấp (45 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-010] Vòng Lặp Vô Tận 60fps `requestAnimationFrame` Tiêu Tốn CPU Liên Tục
- **Danh mục:** Hiệu năng JavaScript (Performance & Resource Drain)
- **Mức độ:** **P2 — Medium**
- **Tệp nguồn ảnh hưởng:** `app/static/js/main.js` (Dòng 171–186)
- **Bằng chứng mã nguồn:**
  ```javascript
  function loopScroll() {
      if (!isDown && !isHovered) {
          slider.scrollLeft += scrollSpeed;
          ...
      }
      animationFrameId = requestAnimationFrame(loopScroll);
  }
  animationFrameId = requestAnimationFrame(loopScroll);
  ```
- **Tại sao đây là vấn đề:**
  Hàm cuộn tự động của thanh trượt sự kiện AI chạy liên tục ở tần số 60fps ngay cả khi người dùng đã cuộn xuống cuối trang hoặc chuyển tab. Điều này gây hao pin trên thiết bị di động, làm tăng độ trễ phản hồi (Interaction to Next Paint — INP).
- **Biện pháp khắc phục khuyến nghị:**
  Sử dụng `IntersectionObserver` để chỉ kích hoạt vòng lặp `requestAnimationFrame` khi vùng thanh trượt đang thực sự hiển thị trên khung nhìn màn hình (Viewport).
- **Lợi ích SEO đạt được:** Giảm tải CPU cho thiết bị di động, cải thiện điểm số phản hồi tương tác (INP).
- **Độ phức tạp hiện thực:** Thấp (30 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-011] Tệp CSS FontAwesome Bên Ngoài Gây Chặn Kết Xuất (Render-Blocking)
- **Danh mục:** Hiệu năng tải trang (Network & Critical Path)
- **Mức độ:** **P2 — Medium**
- **Tệp nguồn ảnh hưởng:** `app/templates/base.html` (Dòng 33–35)
- **Bằng chứng mã nguồn:**
  `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">`
- **Tại sao đây là vấn đề:**
  Trình duyệt phải dừng kết xuất để tải toàn bộ tệp CSS và các bộ font icon lớn từ CDN bên ngoài mà không có gợi ý kết nối trước (`rel="preconnect"`).
- **Biện pháp khắc phục khuyến nghị:**
  Thêm thẻ `<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>` và `<link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">` lên đầu `<head>`.
- **Lợi ích SEO đạt được:** Giảm thời gian chờ thiết lập TLS/DNS, tăng tốc First Contentful Paint (FCP).
- **Độ phức tạp hiện thực:** Rất thấp (10 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-012] Nạp Toàn Cục Tệp Thư Viện `marked.min.js` Trên Mọi Trang
- **Danh mục:** Quản lý tài nguyên JS (Bundle Optimization)
- **Mức độ:** **P2 — Medium**
- **Tệp nguồn ảnh hưởng:** `app/templates/base.html` (Dòng 616)
- **Bằng chứng mã nguồn:**
  `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`
- **Tại sao đây là vấn đề:**
  `marked.min.js` (thư viện phân tích Markdown) chỉ thực sự cần thiết khi người dùng mở khung chat AI, nhưng hiện đang bị tải cưỡng bức trên mọi trang, kể cả các trang tĩnh.
- **Biện pháp khắc phục khuyến nghị:**
  Chỉ tải động `marked.min.js` khi người dùng nhấp mở trợ lý AI, hoặc thêm thuộc tính `defer` để không cản trở luồng phân tích cú pháp HTML.
- **Lợi ích SEO đạt được:** Tiết kiệm băng thông, tăng tốc độ hoàn tất phân tích DOM.
- **Độ phức tạp hiện thực:** Thấp (30 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-013] Phân Trang Client-Side Bằng JavaScript Trên Trang Chủ Giấu Sự Kiện Khỏi Bot
- **Danh mục:** Khả năng khám phá liên kết (Crawlability & Internal Links)
- **Mức độ:** **P2 — Medium**
- **Tệp nguồn ảnh hưởng:** `app/templates/main/index.html` (Dòng 241–256) và `app/static/js/main.js` (Dòng 205–260)
- **Bằng chứng:**
  Trên trang chủ, toàn bộ thẻ sự kiện được render nhưng bị JavaScript ẩn đi bằng logic `card.style.display = 'none'` cho các trang ngoài trang 1. Các nút phân trang là thẻ `<button>` điều khiển bằng JS chứ không phải là thẻ liên kết `<a href="...">`.
- **Tại sao đây là vấn đề:**
  Bot tìm kiếm không click vào các nút `<button>` để chuyển trang. Bot sẽ chỉ nhìn thấy 6 sự kiện đầu tiên trên trang chủ. Mặc dù trang `/events` đã có phân trang server-side chuẩn, việc trang chủ dùng nút ảo khiến luồng PageRank nội bộ không được phân bổ tối ưu.
- **Biện pháp khắc phục khuyến nghị:**
  Đặt liên kết trỏ thẳng tới trang danh mục đầy đủ: `<a href="/events" class="btn btn-primary">Xem toàn bộ sự kiện</a>` để bot dễ dàng di chuyển sang trang có server-side pagination.
- **Lợi ích SEO đạt được:** Cải thiện cấu trúc liên kết nội bộ (Internal Linking Architecture).
- **Độ phức tạp hiện thực:** Thấp (20 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-014] Văn Bản Thay Thế Hình Ảnh Diễn Giả Bị Đặt Chung Chung (`alt="Speaker"`)
- **Danh mục:** Khả năng tiếp cận & SEO Hình ảnh (A11y & Image SEO)
- **Mức độ:** **P3 — Low**
- **Tệp nguồn ảnh hưởng:** `app/templates/main/event_detail.html` (Dòng 120)
- **Bằng chứng mã nguồn:**
  `<img src="{{ s.speaker.avatar_url ... }}" ... alt="Speaker">`
- **Tại sao đây là vấn đề:**
  `alt="Speaker"` không cung cấp thông tin ngữ nghĩa về tên diễn giả cho trình đọc màn hình cũng như công cụ tìm kiếm hình ảnh.
- **Biện pháp khắc phục khuyến nghị:**
  Đổi thành `alt="Diễn giả {{ s.speaker.name }}"`.
- **Lợi ích SEO đạt được:** Tối ưu hóa SEO hình ảnh người nổi tiếng/diễn giả và tuân thủ chuẩn Web Accessibility (WCAG).
- **Độ phức tạp hiện thực:** Rất thấp (5 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

---

### [SEO-FND-015] Thiếu Thẻ `noindex` Trên Các Trang Lỗi Tùy Chỉnh (400, 403, 404, 500)
- **Danh mục:** Quản lý chỉ mục trang lỗi (Technical Robots)
- **Mức độ:** **P3 — Low**
- **Tệp nguồn ảnh hưởng:** `app/templates/errors/400.html`, `403.html`, `404.html`, `500.html`
- **Bằng chứng:**
  Các tệp trong `app/templates/errors/` mở rộng từ `base.html` nhưng không có thẻ `<meta name="robots" content="noindex, nofollow">`.
- **Tại sao đây là vấn đề:**
  Dù Flask đã trả về đúng mã trạng thái HTTP (404/500), các mạng phân phối nội dung (CDN) hoặc proxy trung gian đôi khi có thể lưu đệm trang lỗi và biến chúng thành soft-404 nếu thiếu thẻ meta chỉ thị rõ ràng.
- **Biện pháp khắc phục khuyến nghị:**
  Gắn thẻ `<meta name="robots" content="noindex, nofollow">` vào khối `<head>` của các trang lỗi.
- **Lợi ích SEO đạt được:** Bảo đảm không có trang lỗi nào bị lưu vết trên chỉ mục công cụ tìm kiếm.
- **Độ phức tạp hiện thực:** Rất thấp (10 phút).
- **Mức độ tự tin:** Đã xác minh 100% từ mã nguồn.

