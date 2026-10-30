# EventAI Pro — Phase 3C Code Change Inventory & Integrity Audit

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3C — Bảng Kiểm kê Thay đổi Mã nguồn & Đối soát Toàn vẹn Tệp tin  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kiến trúc sư Ứng dụng Flask & Kỹ sư Quản lý Cấu hình Phần mềm  
**Trạng thái kiểm kê:** **CHÍNH XÁC 100% — HOÀN TOÀN KHÔNG CÓ THAY ĐỔI NGOÀI PHẠM VI**  

---

## 1. BẢNG KIỂM KÊ TỔNG THỂ CÁC TỆP TIN THAY ĐỔI

| STT | Đường dẫn Tệp tin | Trạng thái | Mục đích Nghiệp vụ |
| :---: | :--- | :---: | :--- |
| 1 | [`app/seo_helpers.py`](file:///D:/Event_Management_AI/app/seo_helpers.py) | **Sửa đổi (Modified)** | Bổ sung hằng số `INDEXABLE_EVENT_STATUSES`, các hàm trợ thủ `is_event_indexable`, `get_trusted_canonical_origin`, `build_sitemap_xml`, `build_robots_txt`. |
| 2 | [`app/routes/main.py`](file:///D:/Event_Management_AI/app/routes/main.py) | **Sửa đổi (Modified)** | Import `Response`, đăng ký hai tuyến endpoint `@main_bp.route('/sitemap.xml')` và `@main_bp.route('/robots.txt')` với đầy đủ headers. |
| 3 | [`tests/test_seo_sitemap_robots.py`](file:///D:/Event_Management_AI/tests/test_seo_sitemap_robots.py) | **Tạo mới (Created)** | Bộ kiểm thử tự động gồm 48 bài kiểm tra chuyên sâu cho XML sitemap, robots.txt, trợ thủ SEO và an ninh chống hồi quy. |
| 4 | [`docs/seo/eventai-phase3c-implementation-report.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3c-implementation-report.md) | **Tạo mới (Created)** | Báo cáo chi tiết kiến trúc, thiết kế kỹ thuật và quy tắc lập chỉ mục Phase 3C. |
| 5 | [`docs/seo/eventai-phase3c-sitemap-validation.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3c-sitemap-validation.md) | **Tạo mới (Created)** | Báo cáo thẩm định cú pháp XML sitemap, chỉ thị robots.txt và đối chiếu danh mục URL. |
| 6 | [`docs/seo/eventai-phase3c-test-results.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3c-test-results.md) | **Tạo mới (Created)** | Báo cáo kết quả kiểm thử tự động và bằng chứng xác minh không hồi quy. |
| 7 | [`docs/seo/eventai-phase3c-change-inventory.md`](file:///D:/Event_Management_AI/docs/seo/eventai-phase3c-change-inventory.md) | **Tạo mới (Created)** | Báo cáo kiểm kê thay đổi mã nguồn và đối soát mã băm toàn vẹn SHA-256. |

---

## 2. ĐỐI SOÁT MÃ BĂM TOÀN VẸN (SHA-256 CHECKSUMS)

### 2.1. Tệp tin Ứng dụng Sửa đổi
| Đường dẫn Tệp tin | SHA-256 Trước Phase 3C | SHA-256 Sau Phase 3C | Trạng thái Toàn vẹn |
| :--- | :--- | :--- | :---: |
| `app/seo_helpers.py` | `8252E84EA9391F3FBEF2627242115CEC52380D4C4C9621E8799FA0ADA44F7BFB` | `77D028B35E6FF3B190218528005A8779763B4FE1E3BD643FFDBE6FE4FF0D30F1` | **Hợp lệ (Verified)** |
| `app/routes/main.py` | `556571C02A86A562873058A1B0C1FDA297B0262C664E69B5EF76DD0ABB022DEE` | `3F159601BD7B72B6C0BE8C292EC363AD884A8E408841E3E8C6D0D290A826EC2E` | **Hợp lệ (Verified)** |

### 2.2. Bản sao Lưu Dự phòng Độc lập Trước Triển khai (Pre-implementation Backup)
Bản sao lưu trước khi thực thi đã được lưu giữ an toàn tại:
- Thư mục: `D:\EventAI_Security_Backups\phase3c-before-implementation\`
  - `app_routes_main.py.bak`: SHA-256 = `556571C02A86A562873058A1B0C1FDA297B0262C664E69B5EF76DD0ABB022DEE`
  - `app_seo_helpers.py.bak`: SHA-256 = `8252E84EA9391F3FBEF2627242115CEC52380D4C4C9621E8799FA0ADA44F7BFB`

### 2.3. Tệp tin Kiểm thử Tạo mới
| Đường dẫn Tệp tin | SHA-256 Checksum | Số dòng Code |
| :--- | :--- | :---: |
| `tests/test_seo_sitemap_robots.py` | `CBB92878591BE58BB4E4B36470539DE1BB08365B72B26F273FB2F7297541358D` | 443 dòng |

---

## 3. CHI TIẾT THAY ĐỔI MÃ NGUỒN (CODE DIFF AUDIT)

### 3.1. `app/seo_helpers.py`
- **Dòng 10:** Thêm import `from xml.sax.saxutils import escape as xml_escape`.
- **Dòng 372-519:** Bổ sung khối mã nguồn:
  - Khai báo hằng số `INDEXABLE_EVENT_STATUSES = ('published', 'ongoing', 'completed')`.
  - Hàm `is_event_indexable(event)`.
  - Hàm `get_trusted_canonical_origin()` với cơ chế phòng vệ tiêm nhiễm Host Injection và CRLF.
  - Hàm `build_sitemap_xml(base_origin, event_records)` với thuật toán tạo XML sitemap, xử lý `<lastmod>` từ `updated_at`, loại trừ trùng lặp URL và mã hóa entity XML.
  - Hàm `build_robots_txt(base_origin)` với mẫu plain-text robots chuẩn mực.

### 3.2. `app/routes/main.py`
- **Dòng 4:** Bổ sung import `Response` từ `flask`.
- **Dòng 126-179:** Đăng ký hai tuyến router:
  - `@main_bp.route('/sitemap.xml')`: Tối ưu truy vấn CSDL lấy `id` và `updated_at`, áp dụng Content-Type `application/xml; charset=utf-8`, header `nosniff`, và `Cache-Control: public, max-age=3600`.
  - `@main_bp.route('/robots.txt')`: Áp dụng Content-Type `text/plain; charset=utf-8`, header `nosniff`, và `Cache-Control: public, max-age=86400`.

---

## 4. CAM KẾT & XÁC NHẬN RANH GIỚI BẢO MẬT

1. **Tuyệt đối Không Sửa đổi Cơ sở Dữ liệu:** Không có lệnh DDL thay đổi lược đồ (schema) CSDL, không có tệp CSDL SQLite tĩnh bị ghi đè dữ liệu.
2. **Tuyệt đối Không Can thiệp Tài liệu Học thuật:** Không có bất kỳ tệp tài liệu `.docx`, bài thuyết trình `.pptx` hoặc tệp nào trong thư mục `tailieu/` bị thay đổi.
3. **Tuyệt đối Không Thực hiện Lệnh Git Nguy hiểm:** Không thực hiện bất kỳ lệnh `git commit`, `git push`, `git reset`, `git checkout`, `git clean`.
4. **Bảo toàn Hệ thống Giao diện Liquid Glass:** 100% tệp mẫu Jinja2 (`app/templates/`) và tệp định kiểu tĩnh (`app/static/css/style.css`) giữ nguyên vẹn phong cách thiết kế Apple tối giản.

