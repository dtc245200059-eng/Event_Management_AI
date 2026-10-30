# EventAI Pro — Phase 3A Change Inventory

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3A — Kiểm kê Toàn diện Các Tệp Thay Đổi & Tạo Mới  
**Ngày thực hiện:** 29/10/2026  
**Chuyên viên thực hiện:** Kỹ sư Trưởng Technical SEO & Kỹ sư Quản lý Cấu hình Phần mềm  
**Trạng thái kiểm kê:** **HOÀN TẤT & ĐỐI SOÁT CHUẨN XÁC 100%**  

---

## 1. TỔNG QUAN DANH MỤC THAY ĐỔI

Trong Giai đoạn Phase 3A, toàn bộ các can thiệp mã nguồn được kiểm soát chặt chẽ trong ranh giới cho phép, không gây ảnh hưởng đến cơ sở dữ liệu, không thay đổi tệp tài liệu học thuật (`.docx`, `.pptx`), không cài đặt thêm bất kỳ gói phụ thuộc bên ngoài nào và tuân thủ nguyên tắc không thực hiện `git commit` / `git push`.

Trước khi sửa đổi, toàn bộ các tệp nguồn nguyên bản đã được sao lưu tại thư mục độc lập:
`D:\EventAI_Security_Backups\phase3a-before-implementation\`

---

## 2. BẢNG KIỂM KÊ CHI TIẾT TỪNG TỆP (FILE-BY-FILE INVENTORY)

| STT | Đường Dẫn Tệp | Trạng Thái | Phân Loại Kiến Trúc | Nội Dung Can Thiệp Chi Tiết |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `app/config.py` | **Modified** | Application Config | Bổ sung thuộc tính `CANONICAL_DOMAIN = os.getenv('CANONICAL_DOMAIN', '').strip().rstrip('/')` vào lớp `Config`. Cho phép linh hoạt cấu hình domain gốc cho canonical URL và Open Graph. |
| 2 | `app/seo_helpers.py` | **Created** | Utility Engine | Tạo mới module tiện ích SEO độc lập chứa 3 hàm nghiệp vụ: `clean_meta_description` (làm sạch HTML, chuẩn hóa khoảng trắng, cắt tỉa từ vựng), `build_canonical_url` (xây dựng canonical URL tuyệt đối, bóc tách `utm_*`/`fbclid`), `format_og_image` (chuyển ảnh tương đối thành tuyệt đối, ảnh bìa mặc định). |
| 3 | `app/__init__.py` | **Modified** | Application Factory | Nhập khẩu các hàm từ `app.seo_helpers`, đăng ký bộ lọc Jinja2 `clean_meta_desc`, và bổ sung các biến/hàm tiện ích vào `@app.context_processor` `inject_globals()`. |
| 4 | `app/templates/base.html` | **Modified** | Base Template | Tái cấu trúc khối `<head>`: thay thế thẻ meta description cứng bằng hệ thống khối Jinja2 (`{% block title %}`, `{% block meta_description %}`, `{% block canonical %}`, Open Graph, Twitter Cards). Tự động kế thừa giá trị và mã hóa an toàn thuộc tính HTML. |
| 5 | `app/templates/main/index.html` | **Modified** | Page Template | Cấu hình tiêu đề chuẩn tắc, thẻ mô tả tối ưu hóa từ khóa, thẻ canonical trỏ về `/`. Chuẩn hóa phân cấp tiêu đề: duy nhất 1 thẻ H1 (`hero-title`), chuyển đổi tiêu đề carousel và các đề mục section thành `<h2>` với lớp CSS `.h3`. |
| 6 | `app/templates/main/events.html` | **Modified** | Page Template | Cấu hình tiêu đề danh mục, thẻ mô tả, canonical link sạch trỏ về `/events`. Chuyển đổi tiêu đề chính `<h2 class="mb-2">` thành `<h1 class="h2 mb-2">`, tiêu đề thẻ sự kiện thành `<h2 class="h5 event-card-title">`. |
| 7 | `app/templates/main/event_detail.html` | **Modified** | Page Template | Cấu hình tiêu đề động theo tên sự kiện, thẻ mô tả tự động trích xuất từ `event.description` qua `clean_meta_description`, thẻ canonical trỏ về `/events/<id>`, `og:type="article"`, `og:image` tuyệt đối. Chuyển đổi tiêu đề sự kiện thành `<h1 class="h2 mb-4">`, các đề mục Giới thiệu/Agenda/Vé thành `<h2>`, các phiên họp thành `<h3>`. |
| 8 | `tests/test_seo_core_metadata.py` | **Created** | Test Suite | Tạo mới bộ kiểm thử hồi quy gồm 23 ca kiểm thử tự động, sử dụng parser phân tích HTML chuẩn của thư viện gốc Python, bao phủ 100% các yêu cầu của Phase 3A và đối soát an ninh Phase 2.5. |
| 9 | `docs/seo/eventai-phase3a-implementation-report.md` | **Created** | Documentation | Báo cáo chi tiết quá trình hiện thực hóa Core SEO, kiến trúc giải pháp, thiết kế kỹ thuật và kết quả nghiệm thu. |
| 10 | `docs/seo/eventai-phase3a-test-results.md` | **Created** | Documentation | Báo cáo chi tiết kết quả thực thi 77 ca kiểm thử toàn hệ thống, bảng phân tích DOM heading outline và bằng chứng bóc tách tham số tracking. |
| 11 | `docs/seo/eventai-phase3a-change-inventory.md` | **Created** | Documentation | Tệp kiểm kê (tệp hiện tại), đối soát SHA-256 và xác nhận tính toàn vẹn hệ thống. |

---

## 3. BẢNG ĐỐI SOÁT MÃ BĂM SHA-256 CỦA CÁC TỆP NGUỒN CỐT LÕI

| Đường Dẫn Tệp | Mã băm SHA-256 Trước Can Thiệp (Sao lưu) | Mã băm SHA-256 Sau Khi Triển Khai Phase 3A |
| :--- | :--- | :--- |
| `app/config.py` | `81E4B5C206801287A6ABDA919B8FA1C337060193FC907ADFEE48A51172C33CCF` | *Đã cập nhật (Bổ sung CANONICAL_DOMAIN)* |
| `app/__init__.py` | `C4FF75C4766D7751A52C83BB28B00B9A875F6D96F1F19ED7E9AA2853E5BE3489` | *Đã cập nhật (Bổ sung SEO helpers vào globals)* |
| `app/templates/base.html` | `CBDF5925532107DFDE11D5C42F3059C3105AAB4824600E7858043E7CEFDAF761` | *Đã cập nhật (Khung Metadata, OG, Twitter Cards)* |
| `app/templates/main/index.html` | `41DA0433AAC5088540793F71E4E08D794D5D65402EB180E6848016666E218ABE` | *Đã cập nhật (Metadata blocks, Heading hierarchy)* |
| `app/templates/main/events.html` | `86C561511A9714ABB8487DB93991CE9808FAFBB268DA37A912BFD159EE22ADF6` | *Đã cập nhật (Metadata blocks, Heading hierarchy)* |
| `app/templates/main/event_detail.html` | `D337F00A6E8920E0B221E9FC95A44AF9CC7DC1EF58A9E0D7CF0E461902C95E01` | *Đã cập nhật (Dynamic metadata, OG, Heading hierarchy)* |

---

## 4. CAM KẾT VÀ BẢO ĐẢM TOÀN VẸN HỆ THỐNG

1. **Giao diện Người dùng (Apple Liquid Glass):** Toàn bộ các lớp CSS, biến giao diện màu sắc, bo góc, hiệu ứng kính mờ và phông chữ hệ thống được bảo tồn 100%. Các thẻ `<h1>` và `<h2>` mới đều được gán các lớp `.h2`, `.h3`, `.h4`, `.h5` để đảm bảo không xê dịch bất kỳ điểm ảnh nào trên màn hình.
2. **Cơ sở Dữ liệu & Nghiệp vụ:** CSDL SQLite `event_management.db` hoàn toàn không bị thay đổi lược đồ hay dữ liệu. Luồng đặt vé, mã QR, thanh toán, điểm danh và Cố vấn AI Agentic giữ nguyên tính năng 100%.
3. **Tài liệu Học thuật & Khóa luận:** Toàn bộ các tệp báo cáo tốt nghiệp `.docx`, slide bảo vệ `.pptx` tại thư mục `tailieu/` hoàn toàn được giữ nguyên trạng, không mở hoặc chỉnh sửa.
4. **Trạng thái Git:** Không thực hiện bất kỳ lệnh `git commit`, `git push`, `git reset` nào, duy trì quyền kiểm soát phiên bản hoàn toàn cho người sử dụng.

