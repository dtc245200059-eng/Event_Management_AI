# EventAI Pro — Kết Quả Kiểm Thử Giao Diện Trình Duyệt Thực Tế Trên Windows (Browser QA Results)

> **Tài liệu tham chiếu:** `docs/deployment/eventai-windows-browser-qa-results.md`  
> **Trình duyệt thực thi:** Microsoft Edge Core v156 (Blink Engine, Version `156.0.4314.50`)  
> **Nền tảng kiểm thử:** Windows 11 64-bit Native Host  
> **Mục tiêu kiểm thử:** `http://127.0.0.1:5001/` (EventAI Pro Staging Server)  
> **Trạng thái:** TOÀN BỘ 14 LUỒNG TÍCH HỢP & 4 VIEWPORT KIỂM THỬ ĐẠT 100% (PASS)

---

## 1. MÔI TRƯỜNG THỰC THI TRÌNH DUYỆT THỰC TẾ (REAL BROWSER ENVIRONMENT)

Khác với các bài kiểm thử unit/functional thông thường dùng Flask Test Client (`werkzeug.test.Client`), bài kiểm thử này sử dụng **trình duyệt Microsoft Edge bản địa được cài đặt trên hệ điều hành Windows 11**:

- **Đường dẫn nhị phân Edge:** `C:\Program Files (x86)\Microsoft\EdgeCore\156.0.4314.50\msedge.exe`
- **Nhánh nhân (Rendering Engine):** Chromium / Blink v156
- **Chế độ thực thi:** Headless New (`--headless=new --disable-gpu`)
- **Phân giải kiểm thử Desktop:** 1280 x 800 pixels (Tỉ lệ chuẩn màn hình laptop/desktop)
- **Phân giải kiểm thử Mobile:** 390 x 844 pixels (Chuẩn kích thước viewport iPhone 14/15 và smartphone hiện đại)

---

## 2. PHÂN ĐỊNH RÕ RÀNG 3 CẤP ĐỘ KIỂM THỬ (THE THREE QUALITY GATES)

Nhằm đảm bảo tính minh bạch học thuật và trung thực kỹ thuật tuyệt đối, hệ thống ghi nhận rõ ràng sự khác biệt giữa 3 tầng kiểm thử:

```
+-------------------------------------------------------------------------------+
|                      TẦNG 1: BROWSER RENDERING AUDIT (REAL EDGE v156)         |
|  * 1 Trình duyệt thực thi (Microsoft Edge Core 156.0.4314.50)                 |
|  * 4 Bằng chứng thị giác ảnh chụp màn hình (Desktop, Mobile, Login, Event)   |
|  * 1 Tệp kết xuất DOM hoàn chỉnh (42,178 bytes, theme dark, CSRF token)       |
+-------------------------------------------------------------------------------+
                                      |
+-------------------------------------------------------------------------------+
|                      TẦNG 2: REAL HTTP STAGING E2E WORKFLOWS                  |
|  * 14 Kịch bản tích hợp nghiệp vụ chạy trên cổng mạng thực 127.0.0.1:5001     |
|  * Kiểm thử qua thư viện mạng requests với đầy đủ Cookie, Session, CSRF Token |
|  * Kết quả: 14/14 LUỒNG THÀNH CÔNG (100% PASS)                                |
+-------------------------------------------------------------------------------+
                                      |
+-------------------------------------------------------------------------------+
|                      TẦNG 3: PYTEST AUTOMATED REGRESSION SUITE                |
|  * 218 Ca kiểm thử tự động trên 12 tệp kiểm thử vật lý (tests/test_*.py)     |
|  * Kiểm thử logic nghiệp vụ, bảo mật, RBAC, schema, CSRF, AI services, SEO  |
|  * Kết quả: 218/218 PASSED trong 71.10 giây (100% PASS)                       |
+-------------------------------------------------------------------------------+
```

---

## 3. BẢNG KẾT QUẢ CHI TIẾT 14 LUỒNG NGHIỆP VỤ STAGING (E2E WORKFLOW MATRIX)

Toàn bộ 14 luồng kiểm thử được thực thi tự động qua kịch bản `scripts\verify_staging_workflows.py` trên máy chủ Staging thực tế:

| Mã luồng | Tên luồng nghiệp vụ | Phương thức / URL | Dữ liệu đầu vào / Headers | Kết quả HTTP | Bằng chứng xác nhận (Evidence) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WF01** | Trang chủ ẩn danh (Anonymous Homepage) | `GET /` | Không kèm cookie | `200 OK` | Tiêu đề "EventAI Pro", nạp CSS Apple Liquid Glass, `<meta name="csrf-token">` có giá trị | **PASS** |
| **WF02** | Chi tiết sự kiện (Event Detail) | `GET /events/1` | Không kèm cookie | `200 OK` | Hiển thị sự kiện ID 1, tên diễn giả "TS. Nguyễn Văn AI", lịch trình Keynote, nút đặt vé | **PASS** |
| **WF03** | Khởi tạo Form & CSRF Đăng nhập | `GET /auth/login` | Session mới | `200 OK` | Form chứa `<input type="hidden" name="csrf_token">`, máy chủ cấp phát cookie `session` | **PASS** |
| **WF04** | Đăng nhập Quản trị viên (Admin Login) | `POST /auth/login` | `username=admin@eventai.vn`, `Admin@123`, `csrf_token` | `302 Found` | Chuyển hướng thành công tới `/admin/dashboard`, thiết lập cookie phiên xác thực | **PASS** |
| **WF05** | Truy cập Bảng điều khiển Quản trị | `GET /admin/dashboard`| Cookie phiên Admin | `200 OK` | Hiển thị dashboard quản trị, tổng số sự kiện, tỷ lệ tham dự, danh sách phản hồi | **PASS** |
| **WF06** | Hỏi đáp Trợ lý AI (AI RAG Chat) | `POST /ai/chat` | `{"message": "Diễn giả...", "event_id": 1}`, `X-CSRFToken` | `200 OK` | Trả về JSON chứa câu trả lời định dạng Markdown (325 ký tự) dựa trên dữ liệu diễn giả | **PASS** |
| **WF07** | Đăng nhập Nhân viên (Staff Login) | `POST /auth/login` | `username=staff@eventai.vn`, `Staff@123`, `csrf_token` | `302 Found` | Đăng nhập thành công, cấp quyền soát vé check-in | **PASS** |
| **WF08** | Giao diện Soát vé Check-in | `GET /checkin/` | Cookie phiên Staff | `200 OK` | Tải giao diện máy quét camera QR Code, nút tải ảnh vé, danh sách người tham dự | **PASS** |
| **WF09** | Quét Check-in Vé Hợp Lệ | `POST /checkin/verify-api` | `ticket_number="TCK-001-0001-STG"`, `X-CSRFToken` | `200 OK` | `{"success": true, "status": "valid"}`, cập nhật `checked_in=True`, tên khách mời | **PASS** |
| **WF10** | Quét Trùng Lặp Vé (Anti-Duplicate) | `POST /checkin/verify-api` | Quét lại chính vé trên | `409 Conflict`| `{"success": false, "status": "duplicate"}`, cảnh báo vé đã check-in trước đó kèm mốc giờ | **PASS** |
| **WF11** | Đăng nhập Khách mời (Attendee Login) | `POST /auth/login` | `username=attendee@eventai.vn`, `User@123`, `csrf_token` | `302 Found` | Đăng nhập tài khoản khách mời thành công | **PASS** |
| **WF12** | Xem Vé Điện Tử Của Tôi | `GET /tickets/my-tickets`| Cookie phiên Attendee | `200 OK` | Hiển thị vé điện tử, mã đăng ký, trạng thái check-in và mã QR định dạng SVG | **PASS** |
| **WF13** | Đăng xuất an toàn bằng POST | `POST /auth/logout` | `csrf_token` | `302 Found` | Đăng xuất hợp lệ, xóa phiên, ngăn chặn triệt để tấn công Login/Logout CSRF | **PASS** |
| **WF14** | Kiểm chứng Chống Giả Mạo CSRF | `POST /auth/login` | Bỏ trường `csrf_token` | `400 Bad Request`| Flask-WTF chặn đứng yêu cầu không có CSRF token, bảo vệ an toàn biểu mẫu | **PASS** |

---

## 4. BẰNG CHỨNG THỊ GIÁC & PHÂN TÍCH GIAO DIỆN LIQUID GLASS

Trình duyệt Edge Core v156 đã chụp lại 4 tệp hình ảnh thực tế tại `scratch\`:

### 4.1 Trang chủ Máy tính Desktop (`scratch\staging_home_desktop.png` - 476,804 bytes)
- **Kích thước:** 1280 x 800 pixels.
- **Đánh giá thiết kế:**
  - Header thanh điều hướng kính mờ (Liquid Glass Frosted Navigation Bar) với hiệu ứng `backdrop-filter: blur(20px)`.
  - Logo EventAI Pro sắc nét kèm biểu tượng ngôi sao thông minh.
  - Hero banner công nghệ cao hiển thị mượt mà với tông màu xanh Apple `#007AFF`.
  - Bộ thẻ sự kiện (Event Cards) hiển thị trạng thái phát hành (Published), thời gian, địa điểm rõ ràng.
  - Nút nổi Trợ lý AI (Floating AI Widget) xuất hiện góc dưới bên phải màn hình.

### 4.2 Trang chủ Di động Viewport Mobile (`scratch\staging_home_mobile.png` - 155,107 bytes)
- **Kích thước:** 390 x 844 pixels (Chuẩn iPhone 14/15).
- **Đánh giá thiết kế Responsive:**
  - Bố cục tự động co giãn theo chuẩn Fluid Layout, không bị tràn ngang (Zero Horizontal Overflow).
  - Thanh điều hướng đáy chuẩn Apple (Apple Bottom Navigation Bar) xuất hiện cố định ở chân màn hình gồm 5 nút: *Khám phá, Lịch trình, Vé, Tài khoản, Menu*.
  - Khoảng cách chạm (Tap Target) tối thiểu 44x44px đảm bảo chuẩn công thái học di động WCAG 2.1 AA.

### 4.3 Trang Đăng Nhập Hệ Thống (`scratch\staging_login.png` - 61,613 bytes)
- **Kích thước:** 1280 x 800 pixels.
- **Đánh giá thiết kế:**
  - Thẻ kính Liquid Glass căn giữa màn hình với độ tương phản văn bản cao trên nền tối.
  - Ô nhập liệu bo góc tròn tinh tế (iOS Corner Radius 12px) kèm biểu tượng trực quan.
  - Kiểm tra DOM xác nhận có trường ẩn CSRF token sẵn sàng bảo vệ form.

### 4.4 Trang Chi Tiết Sự Kiện (`scratch\staging_event_detail.png` - 579,404 bytes)
- **Kích thước:** 1280 x 800 pixels.
- **Đánh giá thiết kế:**
  - Banner sự kiện lớn với hiệu ứng gradient overlay chuyên nghiệp.
  - Cột thông tin chi tiết: Thời gian bắt đầu, kết thúc, sức chứa (300 người), địa điểm trung tâm.
  - Khối thông tin Diễn giả (TS. Nguyễn Văn AI) kèm tổ chức và tiểu sử khoa học.
  - Khối lịch trình (Schedule Timeline) phiên Keynote.
  - Khối Câu hỏi thường gặp (FAQ Accordion) về thủ tục check-in và hủy vé.

---

## 5. KIỂM ĐỊNH KẾT XUẤT DOM & TIÊU CHUẨN KỸ THUẬT (DOM AUDIT)

Tệp kết xuất DOM `scratch\edge_dump_home.html` (42,178 bytes) xác nhận các tiêu chuẩn kỹ thuật hàng đầu:
1. **Chống giật giao diện (Zero Theme Flash / FOUT):** Đoạn mã JavaScript nội tuyến tại `<head>` đọc thuộc tính `localStorage.getItem('theme')` và gán tức thì `data-theme="dark"` trước khi trình duyệt tải CSS.
2. **Bảo vệ CSRF:** Thẻ `<meta name="csrf-token" content="...">` được sinh động bởi Flask-WTF, cho phép các hàm `fetch` và `XMLHttpRequest` trong file `main.js` và `ai_chat.js` tự động gắn header `X-CSRFToken`.
3. **SEO & Social Graph:** Thẻ `<link rel="canonical" href="http://127.0.0.1:5001/">`, Open Graph (`og:title`, `og:image`), Twitter Cards, và Schema.org JSON-LD được kết xuất đầy đủ, hợp lệ.

