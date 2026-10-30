# EventAI Pro — Phase 3B Change Inventory

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3B — Kiểm kê Toàn diện Các Tệp Thay Đổi & Tạo Mới (Event Structured Data)  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kỹ sư Trưởng Schema.org & Kỹ sư Quản lý Cấu hình Phần mềm  
**Trạng thái kiểm kê:** **HOÀN TẤT & ĐỐI SOÁT CHUẨN XÁC 100%**  

---

## 1. TỔNG QUAN DANH MỤC THAY ĐỔI

Trong Giai đoạn Phase 3B, toàn bộ các can thiệp mã nguồn được thực hiện theo đúng chuẩn mực ranh giới an toàn của dự án:
- Không thay đổi cơ sở dữ liệu SQLite (`event_management.db`).
- Không chỉnh sửa các tệp khóa luận tốt nghiệp, bài báo hay slide bảo vệ (`.docx`, `.pptx` tại `tailieu/`).
- Không cài đặt thêm bất kỳ thư viện bên ngoài nào (sử dụng thư viện chuẩn của Python: `re`, `json`, `datetime`, `urllib.parse`, `html.parser`).
- Tuyệt đối không can thiệp lệnh quản trị Git (`git commit`, `git push`, `git reset`, `git checkout`).

Trước khi can thiệp mã nguồn, toàn bộ các tệp nguồn nguyên bản đã được sao lưu tại:
`D:\EventAI_Security_Backups\phase3b-before-implementation\`

---

## 2. BẢNG KIỂM KÊ CHI TIẾT TỪNG TỆP (FILE-BY-FILE INVENTORY)

| STT | Đường Dẫn Tệp | Trạng Thái | Phân Loại Kiến Trúc | Nội Dung Can Thiệp Chi Tiết |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `app/seo_helpers.py` | **Modified** | Utility Engine | Mở rộng module tiện ích SEO với các hàm nghiệp vụ: `format_iso8601_date` (định dạng thời gian ISO 8601 kèm múi giờ), `get_schema_event_status` (ánh xạ trạng thái sự kiện), `get_schema_attendance_mode` (ánh xạ hình thức tham gia), `build_event_location` (địa điểm vật lý Place, trực tuyến VirtualLocation hoặc kết hợp), `build_ticket_offers` (danh mục ưu đãi giá vé Offer), `build_event_schema` (bộ tạo tổng thể Event JSON-LD), `build_breadcrumb_schema` (bộ tạo BreadcrumbList JSON-LD). |
| 2 | `app/__init__.py` | **Modified** | Application Factory | Nhập khẩu các hàm `build_event_schema` và `build_breadcrumb_schema` từ `app.seo_helpers`, đưa vào `@app.context_processor` `inject_globals()` dưới tên `get_event_schema` và `get_breadcrumb_schema`. |
| 3 | `app/templates/base.html` | **Modified** | Base Template | Bổ sung khối `{% block structured_data %}{% endblock %}` vào phần `<head>`, tạo vị trí chuẩn mực để các trang con nhúng mã JSON-LD. |
| 4 | `app/templates/main/event_detail.html` | **Modified** | Page Template | Triển khai khối `{% block structured_data %}`: Gọi `get_event_schema(event)` và `get_breadcrumb_schema(...)`, nhúng qua bộ lọc bảo mật `tojson|safe` cho các sự kiện công khai (loại trừ sự kiện draft và draft preview). |
| 5 | `tests/test_event_schema.py` | **Created** | Test Suite | Tạo mới bộ kiểm thử gồm 32 ca kiểm thử tự động chuyên sâu, bao phủ từ thuộc tính Event cốt lõi, xử lý múi giờ, đa dạng loại hình địa điểm, ưu đãi vé, bảo vệ bản nháp, chống tấn công XSS đến BreadcrumbList. |
| 6 | `docs/seo/eventai-phase3b-implementation-report.md` | **Created** | Documentation | Báo cáo chi tiết quá trình hiện thực hóa dữ liệu có cấu trúc Schema.org, kiến trúc kỹ thuật và kết quả nghiệm thu. |
| 7 | `docs/seo/eventai-phase3b-schema-validation.md` | **Created** | Documentation | Báo cáo kiểm chứng cú pháp JSON-LD thực tế, ma trận tuân thủ tiêu chuẩn Google Search Central và phân biệt Schema validity vs Rich Results eligibility. |
| 8 | `docs/seo/eventai-phase3b-test-results.md` | **Created** | Documentation | Báo cáo kết quả kiểm thử 109 ca toàn hệ thống, bảng chi tiết 32 test case Schema.org và cam kết Zero Regression. |
| 9 | `docs/seo/eventai-phase3b-change-inventory.md` | **Created** | Documentation | Tệp kiểm kê (tệp hiện tại), đối soát mã băm SHA-256 và bảo đảm toàn vẹn hệ thống. |

---

## 3. BẢNG ĐỐI SOÁT MÃ BĂM SHA-256 CỦA CÁC TỆP NGUỒN CỐT LÕI

| Đường Dẫn Tệp | Mã băm SHA-256 Trước Can Thiệp (Sao lưu) | Trạng Thái Sau Khi Triển Khai Phase 3B |
| :--- | :--- | :--- |
| `app/seo_helpers.py` | `F23688F70E7F33C68BA5CFB547E68DC78E201AC2980EE4046ADC7060CAE42459` | *Đã cập nhật (Bổ sung bộ tạo Event Schema & Breadcrumbs)* |
| `app/__init__.py` | `D2E64D79994757CBE81FDD0189E5F98095CEEF821CB89ED584B59F029D4BC0C3` | *Đã cập nhật (Đăng ký schema helpers vào globals)* |
| `app/templates/base.html` | `4894718DBF3F68CA3DF622499005FCB8A64BE5D1952AB3286E403580F16AB452` | *Đã cập nhật (Bổ sung block structured_data)* |
| `app/templates/main/event_detail.html` | `DE05EB4A8CB783FBA36571BD093DAD2A3FD94F9D8B9BA6232CE9D26D9770D35E` | *Đã cập nhật (Nhúng script application/ld+json)* |

---

## 4. CAM KẾT VÀ BẢO ĐẢM TOÀN VẸN HỆ THỐNG

1. **Giao diện Người dùng (Apple Liquid Glass):** Khối `application/ld+json` là mã máy đọc ẩn trong `<head>`, hoàn toàn không gây ảnh hưởng đến giao diện DOM hiển thị, không làm xê dịch bố cục CSS hay hiệu ứng thị giác.
2. **Bảo tồn Nền tảng An ninh Phase 2.5:**
   - Sự kiện bản nháp (`draft`) bị loại trừ 100% khỏi luồng sinh Schema.
   - Quản trị viên xem trước sự kiện nháp (`is_draft_preview`) nhận trang với chỉ thị `noindex, follow` và không có JSON-LD.
   - Ảnh vé tĩnh QR (`/static/qr_codes/*`) tiếp tục bị khóa chặn đối với khách chưa đăng nhập.
3. **Phòng chống Lỗ hổng Tiềm tàng (XSS & Data Leakage):**
   - Cơ chế thoát mã `tojson` bảo vệ 100% trước nguy cơ script injection thông qua tiêu đề sự kiện.
   - Các tham số token bí mật trong URL phòng họp trực tuyến được loại bỏ tự động trước khi xuất bản ra siêu dữ liệu công khai.
4. **Trạng thái Phiên bản Git:** Giữ nguyên trạng thái kiểm soát mã nguồn cục bộ, không thực hiện commit hay push tự động.

