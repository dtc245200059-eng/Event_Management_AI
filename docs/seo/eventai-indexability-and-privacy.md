# EventAI Pro — Security-Aware Indexability & Privacy Assessment

**Phân tích bởi:** Chuyên gia Bảo mật Ứng dụng Web & Kỹ sư Trưởng SEO Kỹ thuật  
**Mục tiêu:** Rà soát nguy cơ rò rỉ dữ liệu định danh cá nhân (PII), lộ thông tin xác thực quản trị và cấu hình thu thập dữ liệu (Robots & Sitemap) của ứng dụng `EventAI Pro`.  
**Phạm vi:** Toàn bộ hệ thống định tuyến, các mẫu giao diện Jinja2 và tệp tĩnh trong `app/static/`.  

---

## 1. PHÁT HIỆN LỖ HỔNG BẢO MẬT & QUYỀN RIÊNG TƯ TRỌNG YẾU

### Phát hiện 1 (Mức độ P0 — Nghiêm trọng): Hiển thị thông tin đăng nhập Quản trị viên trong giao diện công khai
- **Vị trí tệp tin:** `app/templates/auth/login.html` (Dòng 16–21)
- **Bằng chứng mã nguồn:**
  ```html
  <!-- Quick Accounts Hint for Demo -->
  <div class="p-3 mb-4 rounded-3 small" style="background: var(--surface-secondary); border: 1px dashed var(--border-regular);">
      <strong class="text-primary d-block mb-1"><i class="fa-solid fa-key me-1"></i> Tài khoản Demo có sẵn:</strong>
      <div>• <strong>Admin:</strong> <code>admin</code> / <code>Admin@123</code></div>
      <div>• <strong>Staff Check-in:</strong> <code>staff1</code> / <code>Staff@123</code></div>
      <div>• <strong>Khách mời:</strong> <code>attendee1</code> / <code>User@123</code></div>
  </div>
  ```
- **Rủi ro SEO & Bảo mật:**
  Trang `/auth/login` hiện là trang công khai. Khi công cụ tìm kiếm (Googlebot, Bingbot) thu thập trang này mà không có chỉ thị chặn (`noindex`), đoạn gợi ý mật khẩu này sẽ **bị lập chỉ mục và hiển thị trực tiếp trong đoạn trích tìm kiếm (Search Snippet)** của Google. Bất kỳ ai tìm kiếm từ khóa `"EventAI Pro" admin` đều có thể thấy ngay tài khoản và mật khẩu quản trị cấp cao.
- **Biện pháp khắc phục bắt buộc:**
  1. Thêm chỉ thị `<meta name="robots" content="noindex, nofollow">` vào khối `<head>` của `auth/login.html` và `auth/register.html`.
  2. Đưa đường dẫn `/auth/` vào danh sách `Disallow` trong `robots.txt`.
  3. Trong môi trường Production, phải ẩn hoàn toàn khối gợi ý mật khẩu demo dựa trên biến cấu hình `DEBUG == False`.

---

### Phát hiện 2 (Mức độ P1 — Rủi ro cao): Mã QR vé SVG lưu trong thư mục `static` có thể truy cập tự do không cần xác thực
- **Vị trí tệp tin:** `app/__init__.py` (Dòng 28), `app/routes/tickets.py` (Dòng 16–26, 89–90), `app/routes/checkin.py` (Dòng 213)
- **Bằng chứng mã nguồn:**
  ```python
  # Trong app/routes/tickets.py
  qr_dir = os.path.join(current_app.static_folder, 'qr_codes')
  filename = f"{ticket_number}.svg"
  filepath = os.path.join(qr_dir, filename)
  ...
  return f"qr_codes/{filename}"
  ```
- **Rủi ro SEO & Bảo mật:**
  Thư mục `app/static/qr_codes/` nằm dưới trình phục vụ tệp tĩnh mặc định của Flask (`/static/...`), vốn **không có lớp kiểm tra xác thực người dùng (`@login_required`)**.
  - Các tệp `.svg` này chứa mã vé bảo mật (`TCK-001-...`) và chuỗi thanh toán ngân hàng (`VIETQR://PAY?...`).
  - Nếu Googlebot quét được một liên kết tĩnh tới mã QR hoặc kẻ xấu thực hiện quét vét (enumeration/scraping), các mã vé điện tử sẽ bị lập chỉ mục trên Google Image Search hoặc bị đánh cắp trước khi chủ vé kịp check-in.
- **Biện pháp khắc phục bắt buộc:**
  1. Cấu hình `robots.txt` cấm tuyệt đối bot truy cập thư mục: `Disallow: /static/qr_codes/`.
  2. Bổ sung bộ lọc HTTP Header trong Flask (`@app.after_request`): Nếu đường dẫn bắt đầu bằng `/static/qr_codes/`, tự động gắn tiêu đề `X-Robots-Tag: noindex, nofollow, noarchive`.
  3. Lộ trình dài hạn: Di chuyển việc phân phối ảnh vé sang endpoint bảo mật (`/tickets/download-qr/<reg_id>`) có kiểm tra quyền sở hữu vé thay vì phục vụ trực tiếp qua tệp tĩnh.

---

### Phát hiện 3 (Mức độ P1 — Rủi ro cao): Rò rỉ sự kiện bản nháp (`draft`) và sự kiện bị hủy (`cancelled`)
- **Vị trí tệp tin:** `app/routes/main.py` (Dòng 89–113)
- **Bằng chứng mã nguồn:**
  ```python
  @main_bp.route('/events/<int:event_id>')
  def event_detail(event_id):
      event = db.get_or_404(Event, event_id) # Không lọc theo event.status!
  ```
- **Rủi ro:**
  Trong khi trang danh sách `/events` đã lọc chặt chẽ `Event.status.in_(['published', 'ongoing'])`, trang chi tiết `/events/<id>` lại chấp nhận mọi ID tồn tại trong CSDL.
  - Sự kiện bản nháp (`draft`) hoặc sự kiện đã hủy (`cancelled`) vẫn kết xuất đầy đủ HTML nếu người ngoài đoán được ID.
  - Googlebot có thể lập chỉ mục các sự kiện nội bộ chưa công bố.
- **Biện pháp khắc phục:**
  - Nếu `event.status == 'draft'` và người dùng hiện tại không phải là Admin/Tác giả: Trả về HTTP 404.
  - Nếu `event.status == 'cancelled'`: Trả về tiêu đề `X-Robots-Tag: noindex` hoặc gắn thẻ `<meta name="robots" content="noindex">`.
  - Trong tệp `sitemap.xml`, chỉ đưa các sự kiện có `status in ['published', 'ongoing', 'completed']`.

---

## 2. HIỆN TRẠNG ROBOTS.TXT & SITEMAP.XML

| Thành phần | Hiện trạng trong dự án | Tác động SEO & Bảo mật |
| :--- | :--- | :--- |
| **robots.txt** | **KHÔNG TỒN TẠI (HTTP 404)** | Các crawler (Googlebot, Bingbot, Yandex, GPTBot) không nhận được bất kỳ hướng dẫn hay ranh giới nào. Bot có thể vô tư quét vào các đường dẫn nhạy cảm như `/checkin/`, `/admin/`, `/tickets/`. |
| **sitemap.xml** | **KHÔNG TỒN TẠI (HTTP 404)** | Công cụ tìm kiếm phải tự mò mẫm qua liên kết nội bộ để khám phá sự kiện. Các sự kiện mới công bố sẽ bị lập chỉ mục rất chậm hoặc bị bỏ sót hoàn toàn. |

---

## 3. THIẾT KẾ KIẾN TRÚC ROBOTS.TXT CHUẨN XÁC

> [!IMPORTANT]
> **Nguyên tắc cốt lõi về bảo mật:** `robots.txt` là thỏa thuận công khai hướng dẫn crawler tuân thủ, **không phải là cơ chế kiểm soát truy cập (Access Control)**. Dữ liệu nhạy cảm thực sự phải luôn được bảo vệ bởi lớp phân quyền `@login_required` và RBAC của Flask-Login.

### Bản thiết kế tệp `robots.txt`:
```txt
# EventAI Pro Robots Policy
# https://eventai.pro/robots.txt

User-agent: *
# 1. Cho phép thu thập các trang công khai cốt lõi
Allow: /
Allow: /events$
Allow: /events?
Allow: /events/
Allow: /static/css/
Allow: /static/js/
Allow: /static/uploads/

# 2. Chặn thu thập các phân hệ xác thực, cá nhân và quản trị
Disallow: /admin/
Disallow: /checkin/
Disallow: /tickets/
Disallow: /notifications/
Disallow: /auth/
Disallow: /ai/
Disallow: /api/

# 3. Chặn thu thập thư mục lưu trữ mã QR nhạy cảm
Disallow: /static/qr_codes/

# 4. Vị trí Sơ đồ trang web
Sitemap: https://eventai.pro/sitemap.xml
```

---

## 4. QUY TẮC THIẾT KẾ XML SITEMAP ĐỘNG

Sơ đồ trang web XML (`sitemap.xml`) cần được tạo tự động bằng một Flask route chuyên trách (`@main_bp.route('/sitemap.xml')`) trả về kiểu nội dung `application/xml`.

### Quy tắc chọn lọc URL (Inclusion Rules):
1. **Trang chủ (`/`):**
   - Priority: `1.0`
   - Changefreq: `daily`
   - Lastmod: Thời gian cập nhật sự kiện mới nhất trên toàn hệ thống.
2. **Trang danh sách sự kiện (`/events`):**
   - Priority: `0.9`
   - Changefreq: `daily`
   - Lastmod: Thời gian hiện tại hoặc ngày sự kiện gần nhất.
3. **Các trang chi tiết sự kiện (`/events/<int:event_id>`):**
   - **Chỉ bao gồm sự kiện có:** `Event.status in ['published', 'ongoing', 'completed']`
   - **Loại trừ tuyệt đối:** `status == 'draft'` hoặc `status == 'cancelled'`
   - Priority: `0.8` (đối với sự kiện sắp diễn ra), `0.5` (đối với sự kiện đã kết thúc)
   - Changefreq: `weekly`
   - Lastmod: Lấy chính xác từ trường `Event.updated_at` (hoặc `Event.created_at`), định dạng ISO 8601 (`YYYY-MM-DD`).

### Bản thiết kế XML mẫu:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Trang chủ -->
  <url>
    <loc>https://eventai.pro/</loc>
    <lastmod>2026-10-29</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  
  <!-- Danh mục sự kiện -->
  <url>
    <loc>https://eventai.pro/events</loc>
    <lastmod>2026-10-29</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>

  <!-- Danh sách sự kiện thực tế từ CSDL -->
  <!-- Lặp qua các sự kiện published trong database -->
  <url>
    <loc>https://eventai.pro/events/1</loc>
    <lastmod>2026-10-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

---

## 5. MA TRẬN PHÂN QUYỀN & CHỈ THỊ LẬP CHỈ MỤC THEO VAI TRÒ

| Phân hệ / Nhóm URL | Phân quyền truy cập | Biện pháp bảo vệ nội dung | Chỉ thị Robot Meta / HTTP Header |
| :--- | :--- | :--- | :--- |
| `/` | Mọi người | Không | `index, follow` |
| `/events` | Mọi người | Không | `index, follow` (Canonical chuẩn) |
| `/events/<id>` (Published) | Mọi người | Không | `index, follow` (Kèm Schema Event) |
| `/events/<id>` (Draft) | Organizer / Admin | Trả về 404 cho Guest | `noindex, nofollow` |
| `/auth/login`, `/register` | Mọi người | Giấu mật khẩu demo ở Prod | `noindex, nofollow` |
| `/auth/profile` | Login Required | Flask-Login `@login_required` | `noindex, nofollow` |
| `/tickets/view/<id>` | Login + Vé chính chủ | So sánh `attendee.user_id` | `noindex, nofollow` |
| `/static/qr_codes/*` | Trình phục vụ tệp tĩnh | Chặn robots.txt & gán header | `X-Robots-Tag: noindex, nofollow` |
| `/admin/*` | Role Admin | RBAC `@admin_required` | `noindex, nofollow` (Disallow) |
| `/checkin/*` | Role Staff / Organizer | RBAC `@staff_required` | `noindex, nofollow` (Disallow) |
| `/api/*` | API Endpoints | Rate Limiting + Auth Check | `noindex, nofollow` (Disallow) |

