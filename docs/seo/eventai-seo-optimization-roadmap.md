# EventAI Pro — SEO Optimization Implementation Roadmap

**Phiên bản kế hoạch:** 1.0.0  
**Ngày lập:** 29/10/2026  
**Đơn vị thực hiện:** Nhóm Kỹ sư Trưởng Full-Stack & Chuyên gia Tối ưu hóa SEO  
**Mục tiêu:** Cung cấp lộ trình hành động chi tiết theo 5 giai đoạn tuần tự nhằm giải quyết triệt để 15 khiếm khuyết SEO đã được ghi nhận trong `docs/seo/eventai-seo-evidence-map.md`.  
**Lưu ý quan trọng:** Đây là tài liệu quy hoạch kiến trúc cho các giai đoạn tiếp theo; **tuyệt đối không thực thi sửa đổi mã nguồn ứng dụng trong Giai đoạn 2 này**.

---

## TỔNG QUAN LỘ TRÌNH 5 GIAI ĐOẠN

```
┌─────────────────────────────────────────────────────────────────────────┐
│               EVENTAI PRO SEO OPTIMIZATION ROADMAP                      │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 3A: Sửa Lỗi Siêu Dữ Liệu Cốt Lõi & Lập Chỉ Mục (Core Meta Fixes)  │
│ Phase 3B: Tích Hợp Dữ Liệu Có Cấu Trúc Schema.org Event (JSON-LD)      │
│ Phase 3C: Xây Dựng robots.txt & Dynamic XML Sitemap Tự Động            │
│ Phase 3D: Tối Ưu Hóa Hiệu Năng Ảnh, DOM & Di Động (Core Web Vitals)     │
│ Phase 3E: Kiểm Thử Tự Động Hóa Toàn Diện & Đánh Giá Hồi Quy (Pytest)   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## GIAI ĐOẠN 3A — SỬA LỖI SIÊU DỮ LIỆU CỐT LÕI & LẬP CHỈ MỤC (CORE METADATA & INDEXING FIXES)

### 1. Mục tiêu trọng tâm:
- Khắc phục lỗi bảo mật P0: Gán `noindex` cho `/auth/login` và ẩn mật khẩu demo ở môi trường sản xuất.
- Xóa bỏ tình trạng trùng lặp Meta Description trên toàn bộ website bằng cách hỗ trợ các khối block động trong Jinja2.
- Chuẩn hóa cấu trúc thẻ Heading: Bổ sung thẻ `<h1>` duy nhất cho từng trang và sửa thứ bậc heading (`h1 -> h2 -> h3`).
- Bổ sung thẻ Canonical Link và bộ siêu dữ liệu mạng xã hội (Open Graph & Twitter Cards).

### 2. Các tệp tin dự kiến can thiệp:
- `app/templates/base.html` (Thêm blocks `meta_description`, `canonical`, `og_tags`, `robots_meta`)
- `app/templates/main/index.html` (Bổ sung meta description riêng và Open Graph trang chủ)
- `app/templates/main/events.html` (Thêm thẻ `<h1>Tất Cả Sự Kiện</h1>` và meta description danh mục)
- `app/templates/main/event_detail.html` (Đổi tiêu đề sự kiện thành `<h1>`, đưa trích đoạn mô tả sự kiện vào meta description và og:image)
- `app/templates/auth/login.html` & `register.html` (Gán `noindex, nofollow`, điều kiện ẩn tài khoản demo)
- `app/templates/errors/*.html` (Gán `noindex, nofollow`)

### 3. Phụ thuộc (Dependencies): Không có.

### 4. Yêu cầu kiểm thử (Testing Requirements):
- Kiểm tra render template không phát sinh lỗi cú pháp Jinja2.
- Kiểm tra HTML xuất ra chứa đúng thẻ `<title>`, `<meta name="description">`, `<link rel="canonical">`.
- Kiểm tra trang `/auth/login` và các trang lỗi chứa `<meta name="robots" content="noindex, nofollow">`.

### 5. Rủi ro hồi quy (Regression Risks):
- Xung đột CSS nếu việc đổi thẻ `<h2 class="mb-4">` thành `<h1 class="h2 mb-4">` làm thay đổi khoảng cách dòng hoặc cỡ chữ. Cần giữ nguyên class styling của Apple Design System.

### 6. Ràng buộc an ninh (Security Constraints):
- Tuyệt đối mã hóa chuỗi khi đưa vào thẻ thuộc tính (`html.escape` hoặc Jinja2 autoescape) để tránh Attribute-based XSS.

### 7. Tiêu chí nghiệm thu (Acceptance Criteria):
- 100% trang công khai có tiêu đề và mô tả duy nhất, không trùng lặp.
- 100% trang quản trị, đăng nhập và trang lỗi có chỉ thị `noindex`.
- Xem trước liên kết trên mạng xã hội (Facebook, Zalo, Twitter) hiển thị đầy đủ ảnh, tiêu đề và tóm tắt.

---

## GIAI ĐOẠN 3B — TÍCH HỢP SCHEMA.ORG EVENT JSON-LD (EVENT STRUCTURED DATA)

### 1. Mục tiêu trọng tâm:
- Tích hợp dữ liệu có cấu trúc chuẩn Schema.org Event và BreadcrumbList vào trang chi tiết sự kiện `event_detail.html`.
- Ánh xạ chính xác 100% từ các trường dữ liệu thực tế của CSDL SQLite (`Event`, `Ticket`, `Speaker`, `Schedule`, `Venue`).

### 2. Các tệp tin dự kiến can thiệp:
- `app/templates/main/event_detail.html` (Tích hợp khối JSON-LD theo thiết kế trong `eventai-event-schema-assessment.md`)
- `app/templates/base.html` (Bổ sung khối `{% block structured_data %}{% endblock %}`)

### 3. Phụ thuộc (Dependencies):
- Phụ thuộc Giai đoạn 3A (cần khối block `structured_data` tại `base.html`).

### 4. Yêu cầu kiểm thử (Testing Requirements):
- Phân tích cú pháp JSON hợp lệ, không có lỗi dấu phẩy thừa (trailing comma) hay ký tự xuống dòng chưa escape.
- Kiểm tra tính đầy đủ của các trường bắt buộc của Google: `name`, `startDate`, `location`.
- Kiểm tra các trường mở rộng: `offers` (danh sách vé), `performer` (diễn giả), `eventStatus`, `eventAttendanceMode`.

### 5. Rủi ro hồi quy (Regression Risks):
- Nếu dữ liệu sự kiện bị khuyết (ví dụ: sự kiện chưa có lịch trình hoặc chưa có vé), template không được phát sinh lỗi `NoneType` hoặc sinh ra khối JSON không hợp lệ. Phải có kiểm tra điều kiện `{% if tickets %}`, `{% if schedules %}`.

### 6. Ràng buộc an ninh (Security Constraints):
- **Bắt buộc sử dụng bộ lọc `|tojson`** cho mọi trường văn bản để chống XSS Injection phá vỡ khối `<script type="application/ld+json">`.

### 7. Tiêu chí nghiệm thu (Acceptance Criteria):
- Khối JSON-LD hợp lệ 100% theo tiêu chuẩn của Google Rich Results Validator.
- Không tồn tại dữ liệu giả định; mọi thuộc tính đều tương ứng với nội dung trực quan trên trang.

---

## GIAI ĐOẠN 3C — XÂY DỰNG ROBOTS.TXT & DYNAMIC XML SITEMAP TỰ ĐỘNG

### 1. Mục tiêu trọng tâm:
- Xây dựng endpoint `@main_bp.route('/robots.txt')` trả về chính sách thu thập dữ liệu chuẩn hóa, chặn các vùng nhạy cảm (`/admin/`, `/checkin/`, `/tickets/`, `/static/qr_codes/`).
- Xây dựng endpoint `@main_bp.route('/sitemap.xml')` sinh XML động từ CSDL, chỉ bao gồm các sự kiện hợp lệ (`published`, `ongoing`, `completed`) kèm thời gian `lastmod` chuẩn xác.

### 2. Các tệp tin dự kiến can thiệp:
- `app/routes/main.py` (Khai báo route `robots_txt()` và `sitemap_xml()`)
- `app/templates/sitemap.xml` (Template Jinja2 sinh XML hợp lệ)
- `app/__init__.py` (Bổ sung header `X-Robots-Tag` cho tệp mã QR tĩnh trong `@app.after_request`)

### 3. Phụ thuộc (Dependencies): Không có.

### 4. Yêu cầu kiểm thử (Testing Requirements):
- Kiểm tra truy cập `GET /robots.txt` trả về mã HTTP 200, Content-Type `text/plain`.
- Kiểm tra truy cập `GET /sitemap.xml` trả về mã HTTP 200, Content-Type `application/xml`.
- Xác minh sự kiện bản nháp (`draft`) và sự kiện đã hủy (`cancelled`) không xuất hiện trong sitemap.
- Xác minh tệp ảnh tĩnh `/static/qr_codes/*.svg` trả về tiêu đề `X-Robots-Tag: noindex, nofollow`.

### 5. Rủi ro hồi quy (Regression Risks):
- Hiệu năng truy vấn CSDL: Cần sử dụng truy vấn tối ưu `.with_entities(Event.id, Event.updated_at, Event.status)` thay vì tải toàn bộ đối tượng lớn để tránh nghẽn RAM khi số lượng sự kiện tăng cao.

### 6. Ràng buộc an ninh (Security Constraints):
- Không đưa bất kỳ URL nào chứa mã vé, mã đơn hàng hoặc tham số định danh người tham dự vào sitemap.

### 7. Tiêu chí nghiệm thu (Acceptance Criteria):
- Tệp `sitemap.xml` được các công cụ phân tích XML kiểm tra hợp lệ, không chứa URL 404 hoặc URL chuyển hướng.
- `robots.txt` chỉ dẫn chính xác vị trí của `sitemap.xml`.

---

## GIAI ĐOẠN 3D — TỐI ƯU HÓA HIỆU NĂNG ẢNH, DOM & DI ĐỘNG (CORE WEB VITALS)

### 1. Mục tiêu trọng tâm:
- Khắc phục hiện tượng dịch chuyển bố cục (CLS): Bổ sung tỷ lệ khung hình `aspect-ratio` hoặc kích thước `width/height` cho toàn bộ thẻ ảnh sự kiện.
- Tối ưu hóa Largest Contentful Paint (LCP): Gán cờ `fetchpriority="high"` cho ảnh banner chính trên trang chi tiết sự kiện.
- Tối ưu hóa Interaction to Next Paint (INP) và tiết kiệm CPU: Sử dụng `IntersectionObserver` trong `main.js` để chỉ chạy vòng lặp cuộn tự động 60fps khi thanh trượt thực sự hiển thị trên màn hình.
- Thêm gợi ý kết nối mạng (`preconnect`) cho CDN FontAwesome bên ngoài.

### 2. Các tệp tin dự kiến can thiệp:
- `app/templates/base.html` (Thêm `<link rel="preconnect">` cho cdnjs và jsdelivr)
- `app/templates/main/index.html` (Thêm `loading="lazy"` cho thẻ sự kiện)
- `app/templates/main/event_detail.html` (Thêm `fetchpriority="high"` cho ảnh banner LCP)
- `app/static/js/main.js` (Bọc vòng lặp `requestAnimationFrame` bằng `IntersectionObserver`)

### 3. Phụ thuộc (Dependencies): Không có.

### 4. Yêu cầu kiểm thử (Testing Requirements):
- Kiểm tra bằng kiểm thử tĩnh và kiểm thử giao diện: Các ảnh hiển thị đúng tỷ lệ, không bị méo hình.
- Kiểm tra slider AI vẫn hoạt động trơn tru khi cuộn tới và tự động tạm dừng khi cuộn qua để giải phóng CPU.
- Đảm bảo giữ nguyên thẩm mỹ Liquid Glass và Apple Minimalism theo hướng dẫn trong `AGENTS.md`.

### 5. Rủi ro hồi quy (Regression Risks):
- Phá vỡ bố cục giao diện responsive nếu tỷ lệ khung hình ảnh bị cố định sai. Cần sử dụng CSS `object-fit: cover`.

### 6. Ràng buộc an ninh (Security Constraints):
- Không thay đổi mã logic bảo mật hay các chức năng JavaScript tương tác cốt lõi.

### 7. Tiêu chí nghiệm thu (Acceptance Criteria):
- Toàn bộ thẻ ảnh có đầy đủ thuộc tính kích thước hoặc tỷ lệ khung hình.
- Vòng lặp animation không chạy ngầm lãng phí tài nguyên khi nằm ngoài màn hình.

---

## GIAI ĐOẠN 3E — KIỂM THỬ TỰ ĐỘNG HÓA TOÀN DIỆN & ĐÁNH GIÁ HỒI QUY (PYTEST SUITE)

### 1. Mục tiêu trọng tâm:
- Xây dựng bộ kiểm thử tự động chuyên biệt `tests/test_seo_implementation.py` (sử dụng Flask Test Client chuẩn).
- Kiểm chứng toàn bộ 15 tiêu chí SEO mà không cần kết nối mạng hay công cụ quét ngoài.

### 2. Các tệp tin dự kiến can thiệp:
- `tests/test_seo_implementation.py` (Tạo mới bộ test kiểm tra SEO)

### 3. Phụ thuộc (Dependencies): Hoàn thành Phases 3A, 3B, 3C, 3D.

### 4. Danh mục kịch bản kiểm thử bắt buộc:
1. `test_robots_txt_exists_and_blocks_sensitive_routes`: Kiểm tra mã 200 và các quy tắc Disallow.
2. `test_sitemap_xml_contains_only_published_events`: Kiểm tra cú pháp XML và lọc trạng thái sự kiện.
3. `test_event_detail_json_ld_schema_validity`: Kiểm tra cấu trúc JSON-LD Event và BreadcrumbList.
4. `test_meta_descriptions_are_dynamic_and_unique`: Kiểm tra không bị trùng lặp meta description giữa các trang.
5. `test_canonical_url_consistency`: Kiểm tra URL canonical đúng chuẩn.
6. `test_auth_pages_have_noindex`: Kiểm tra `/auth/login` và `/auth/register` có `noindex`.
7. `test_error_pages_have_noindex`: Kiểm tra các trang lỗi 404/500 có `noindex`.
8. `test_qr_code_static_header_noindex`: Kiểm tra header `X-Robots-Tag` trên tệp mã QR.
9. `test_heading_hierarchy_has_single_h1`: Kiểm tra sự tồn tại của đúng 1 thẻ `<h1>` trên các trang công khai.
10. `test_draft_events_not_accessible_publicly`: Kiểm tra sự kiện draft không bị rò rỉ.

### 5. Tiêu chí nghiệm thu (Acceptance Criteria):
- Đạt tỷ lệ vượt qua **100% (Pass 10/10 test cases)**.
- Không gây ảnh hưởng hay xung đột với bất kỳ bài kiểm thử chức năng sẵn có nào của EventAI Pro.

