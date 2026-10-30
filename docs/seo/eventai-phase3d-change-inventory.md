# EventAI Pro — Phase 3D Code Change Inventory & Integrity Audit

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3D — Bảng Kiểm kê Thay đổi Mã nguồn & Đối soát Toàn vẹn Tệp tin  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên:** Kiến trúc sư Ứng dụng Flask & Kỹ sư Quản lý Cấu hình Phần mềm  
**Trạng thái kiểm kê:** **CHÍNH XÁC 100% — HOÀN TOÀN KHÔNG CÓ THAY ĐỔI NGOÀI PHẠM VI**  

---

## 1. BẢNG KIỂM KÊ TỔNG THỂ CÁC TỆP TIN THAY ĐỔI

| STT | Đường dẫn Tệp tin | Trạng thái | Mục đích Nghiệp vụ & Kỹ thuật |
| :---: | :--- | :---: | :--- |
| 1 | [`app/routes/main.py`](file:///D:/Event_Management_AI/app/routes/main.py) | **Sửa đổi (Modified)** | Sửa giới hạn truy vấn sitemap: `max_event_entries = max(0, MAX_SITEMAP_URLS - 2)` để tổng số URL sitemap không vượt quá 50,000. |
| 2 | [`app/seo_helpers.py`](file:///D:/Event_Management_AI/app/seo_helpers.py) | **Sửa đổi (Modified)** | Thêm hằng số `MAX_SITEMAP_URLS = 50000`, thêm điều kiện dừng `if len(seen_urls) >= MAX_SITEMAP_URLS: break` trong `build_sitemap_xml`. |
| 3 | [`app/templates/base.html`](file:///D:/Event_Management_AI/app/templates/base.html) | **Sửa đổi (Modified)** | Thêm preconnect/dns-prefetch cho CDN và Unsplash, thêm `defer` cho script, thêm ARIA labels cho Chat và Quick Prompts. |
| 4 | [`app/templates/main/index.html`](file:///D:/Event_Management_AI/app/templates/main/index.html) | **Sửa đổi (Modified)** | Tối ưu LCP slide 1 Carousel (`fetchpriority="high"`), lazy load slide 2-5 và card dưới màn hình, thêm ARIA labels cho điều hướng Carousel và tìm kiếm. |
| 5 | [`app/templates/main/events.html`](file:///D:/Event_Management_AI/app/templates/main/events.html) | **Sửa đổi (Modified)** | Tối ưu lazy load thẻ danh mục, thêm `width`/`height`, bổ sung `role="search"` và `aria-label` cho form lọc và tìm kiếm. |
| 6 | [`app/templates/main/event_detail.html`](file:///D:/Event_Management_AI/app/templates/main/event_detail.html) | **Sửa đổi (Modified)** | Tối ưu LCP biểu ngữ sự kiện (`fetchpriority="high" decoding="async" width="800" height="480"`), không lazy load. |
| 7 | [`app/static/js/main.js`](file:///D:/Event_Management_AI/app/static/js/main.js) | **Sửa đổi (Modified)** | Tích hợp `IntersectionObserver`, `visibilitychange` và kiểm tra `prefers-reduced-motion` dừng vòng lặp trượt AI 60fps khi offscreen/đổi tab. |
| 8 | [`app/static/css/style.css`](file:///D:/Event_Management_AI/app/static/css/style.css) | **Sửa đổi (Modified)** | Bổ sung quy tắc `:focus-visible` độ tương phản cao, tối ưu `will-change` cho GPU compositing, giảm blur kính mờ trên mobile (`@media (max-width: 576px)`). |
| 9 | [`tests/test_seo_sitemap_robots.py`](file:///D:/Event_Management_AI/tests/test_seo_sitemap_robots.py) | **Sửa đổi (Modified)** | Bổ sung test case biên `test_build_sitemap_xml_strictly_caps_at_max_urls` (nâng từ 48 lên 49 tests). |
| 10 | [`tests/test_phase3d_performance.py`](file:///D:/Event_Management_AI/tests/test_phase3d_performance.py) | **Tạo mới (Created)** | Bộ kiểm thử tự động chuyên trách gồm 27 bài kiểm tra toàn diện cho LCP, CLS, INP, ARIA, Focus, GPU và bảo mật. |
| 11 | [`docs/seo/eventai-phase3c-test-reconciliation.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3c-test-reconciliation.md) | **Tạo mới (Created)** | Báo cáo đối soát tính nhất quán số lượng bài kiểm thử Phase 3C và thẩm định giới hạn giao thức sitemap. |
| 12 | [`docs/seo/eventai-phase3d-performance-audit.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3d-performance-audit.md) | **Tạo mới (Created)** | Báo cáo khảo sát điểm nghẽn hiệu năng, phân tích LCP/CLS/INP và so sánh trước/sau. |
| 13 | [`docs/seo/eventai-phase3d-implementation-report.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3d-implementation-report.md) | **Tạo mới (Created)** | Báo cáo chi tiết hiện thực hóa tối ưu hóa mã nguồn frontend, templates và kịch bản. |
| 14 | [`docs/seo/eventai-phase3d-test-results.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3d-test-results.md) | **Tạo mới (Created)** | Báo cáo kết quả kiểm thử tự động toàn dự án (185 tests / 11 files / 100% passed). |
| 15 | [`docs/seo/eventai-phase3d-accessibility-review.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3d-accessibility-review.md) | **Tạo mới (Created)** | Báo cáo thẩm định khả năng tiếp cận và trợ năng người dùng theo chuẩn WCAG 2.2 Level AA. |
| 16 | [`docs/seo/eventai-phase3d-change-inventory.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3d-change-inventory.md) | **Tạo mới (Created)** | Báo cáo kiểm kê thay đổi mã nguồn và đối soát mã băm toàn vẹn SHA-256. |

---

## 2. ĐỐI SOÁT MÃ BĂM TOÀN VẸN (SHA-256 CHECKSUMS)

### 2.1. Tệp tin Mã nguồn Sửa đổi
| Đường dẫn Tệp tin | SHA-256 Trước Phase 3D | SHA-256 Sau Phase 3D | Trạng thái Toàn vẹn |
| :--- | :--- | :--- | :---: |
| `app/routes/main.py` | `3F159601BD7B72B6C0BE8C292EC363AD884A8E408841E3E8C6D0D290A826EC2E` | `54978EA648D0F192A22592C996F6401C303E2B3231EBDD422B65EE52734F67B5` | **Hợp lệ (Verified)** |
| `app/seo_helpers.py` | `77D028B35E6FF3B190218528005A8779763B4FE1E3BD643FFDBE6FE4FF0D30F1` | `F2CD646B96F22199849849FD8DBEC528776A48A535C1FA7357FD9E59765E57B7` | **Hợp lệ (Verified)** |
| `app/templates/base.html` | `AF2B355F17A4671C2C656033C1F0E965DAA5529BE3CB56DEC78750237D26DDEB` | `EFECFA749EB502E71251B6961E37FC737095CDE94276112AA31D4BB99BB2B81E` | **Hợp lệ (Verified)** |
| `app/templates/main/index.html` | `5ED66D2C9D04E70BB4D792F7C72B85BE0560B00A7767F7779A76C93C07D6BE4B` | `A00682786E722463CB7FE667ED05D28C18EA35172B89DF319A9102696B512EF1` | **Hợp lệ (Verified)** |
| `app/templates/main/events.html` | `D8F8CACAA9281FB468668DBB4685EF40955E0B7C7CBA909153D67F59FC0B0FCA` | `7DFD2DFE12DBF3F1921EDBC91C08A624E62680A5AE20A237DBE6A441BA1E8A01` | **Hợp lệ (Verified)** |
| `app/templates/main/event_detail.html` | `EBC8A17804A40865F39E519A23FEB5EDF439CF1CE14854D307C615A041F6C2C0` | `C938409766E3C541B4FAA16BA54C5B73A0A2CD9BF95E53114DC6A4162035194C` | **Hợp lệ (Verified)** |
| `app/static/js/main.js` | `2A31F9C121A4396E39CADEE458329F6FFAB5535018DF1D15C631B6C14342A5D9` | `59D8260AE1A6DE9925D10497F145DDBFC18F99C4670EFDCB7249A2C5A3A995E9` | **Hợp lệ (Verified)** |
| `app/static/css/style.css` | `53F33CEF04C2F38057A2BE10C137519A6F23885AA13F58BD77FE228B04A73593` | `F1FE67825060B874C8323B0056676FBFB32A3988021C3DF55342799D6EDA80B4` | **Hợp lệ (Verified)** |
| `tests/test_seo_sitemap_robots.py` | `CBB92878591BE58BB4E4B36470539DE1BB08365B72B26F273FB2F7297541358D` | `613D8315457E361B6359E50545018FE5E61E6E438E815FA901FE8D5CB175AE83` | **Hợp lệ (Verified)** |

### 2.2. Bản sao Lưu Dự phòng Độc lập Trước Triển khai (Pre-implementation Backup)
Toàn bộ các tệp gốc trước khi thực hiện Phase 3D đã được lưu trữ an toàn tại:
- Thư mục: `D:\EventAI_Security_Backups\phase3d-before-implementation\`
  - `app_routes_main.py.bak`
  - `app_seo_helpers.py.bak`
  - `base.html.bak`
  - `index.html.bak`
  - `events.html.bak`
  - `event_detail.html.bak`
  - `main.js.bak`
  - `style.css.bak`

### 2.3. Tệp tin Kiểm thử Tạo mới
| Đường dẫn Tệp tin | SHA-256 Checksum | Số dòng Code |
| :--- | :--- | :---: |
| `tests/test_phase3d_performance.py` | `7B1396AC13F2E542069FE4E22C36B892698BF5E296104CA141C7DB656CB8F4D9` | 385 dòng |

---

## 3. CAM KẾT & XÁC NHẬN RANH GIỚI BẢO MẬT

1. **Tuyệt đối Không Sửa đổi Cơ sở Dữ liệu:** Không có lệnh DDL thay đổi lược đồ CSDL, không có tệp CSDL SQLite `event_management.db` bị ghi đè.
2. **Tuyệt đối Không Can thiệp Tài liệu Học thuật:** 100% tệp tài liệu `.docx`, bài thuyết trình `.pptx` và tệp trong thư mục `tailieu/` được bảo vệ nguyên trạng.
3. **Tuyệt đối Không Thực hiện Lệnh Git Nguy hiểm:** Không thực hiện bất kỳ lệnh `git commit`, `git push`, `git reset`, `git checkout`, `git clean`, `git stash` nào.
4. **Bảo toàn Bản sắc Giao diện Apple Liquid Glass:** Giữ nguyên vẹn 100% hệ thống màu sắc, kiểu chữ Apple Typography, hiệu ứng xuyên thấu và các luồng tương tác người dùng.

