# BÁO CÁO ĐIỂM CHUẨN AN TOÀN DỰ ÁN (PROJECT SAFETY & BASELINE AUDIT)
**Mã tài liệu:** AUD-BASE-2026-001  
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Thư mục làm việc:** `D:\Event_Management_AI`  
**Ngày thực hiện:** 27/10/2026  
**Trạng thái kiểm tra:** VERIFIED & BASELINE SECURED  

---

## 1. Xác Minh Thư Mục Làm Việc & Tính Toàn Vẹn Hệ Thống
- **Đường dẫn thư mục tuyệt đối:** `D:\Event_Management_AI` (Chính xác 100% không gian làm việc của dự án).
- **Hệ điều hành:** Windows (PowerShell 7/Windows PowerShell).
- **Môi trường ảo Python:** `d:\Event_Management_AI\.venv` (Python 3.14.2, Pytest 9.1.1, Flask 3.1.0).

---

## 2. Kiểm Tra Trạng Thái Git & Nhánh Làm Việc (Git Inspection)
- **Nhánh hiện tại:** `main` (Đồng bộ với `origin/main` tại commit `73c8a00`).
- **Remote:** `origin` liên kết tới kho chứa GitHub của đề tài (`dtc245200059-eng/Event_Management_AI.git`).
  *(Lưu ý an ninh: URL remote chứa token xác thực tạm thời; hệ thống tuân thủ nghiêm ngặt nguyên tắc không hiển thị hay ghi đè thông tin xác thực này).*
- **Các tệp tin có thay đổi chưa commit:**
  - Cập nhật backend & phân quyền: `app/models/user.py`, `app/routes/admin.py`, `app/routes/checkin.py`, `app/routes/events.py`.
  - Cập nhật AI Service: `app/services/gemini_service.py`, `app/services/rag_service.py`, `app/services/sentiment_service.py`.
  - Cập nhật Prompts: `app/prompts/feedback_summary.txt`, `app/prompts/notification_generator.txt`.
  - Cập nhật Templates: `app/templates/admin/dashboard.html`, `app/templates/admin/users.html`, `app/templates/events/manage.html`, `app/templates/events/schedules.html`.
  - Cập nhật Tài liệu & Skills: `README.md`, `docs/test-report.md`, các tệp `SKILL.md` phục vụ chuẩn hóa metadata.
- **Cam kết an toàn Git:**
  - Không thực hiện bất kỳ lệnh hủy hoại nào (`git reset --hard`, `git clean -fd`, `git checkout -- .`).
  - Không tự động merge hoặc force-push.
  - Bảo toàn 100% mã nguồn và dữ liệu kiểm thử hiện có.

---

## 3. Ngăn Xếp Công Nghệ Thực Tế (Actual Technology Stack)
Hệ thống **EventAI Pro** được xây dựng dựa trên ngăn xếp ứng dụng web chuẩn mực và tinh gọn, không sử dụng framework nặng không cần thiết:

| Tầng Hệ Thống | Công Nghệ / Thư Viện Sử Dụng | Phiên Bản | Mục Đích Sử Dụng |
| :--- | :--- | :---: | :--- |
| **Giao diện (Frontend)** | HTML5, CSS3 Glassmorphism Apple Tokens, Vanilla JavaScript | Chuẩn W3C | Giao diện chuẩn Apple Liquid Glass, hỗ trợ Light/Dark mode, Responsive. |
| **Thư viện UI phụ trợ** | Bootstrap, FontAwesome 6, Chart.js, HTML5-QRCode, Marked.js | 5.3.3 / 4.4 | Dựng layout lưới, biểu đồ thống kê, quét QR qua Web Camera, render Markdown. |
| **Tầng Ứng Dụng (Backend)** | Python, Flask (Application Factory), Werkzeug | 3.14.2 / 3.1.0 | Điều phối 8 Blueprints, RESTful API endpoints, phân quyền RBAC. |
| **Cơ Sở Dữ Liệu (ORM & DB)** | Flask-SQLAlchemy, SQLite (mặc định) / PostgreSQL | 3.1.0 / 3.42+ | Quản lý 11 bảng chuẩn 3NF, 13 B-Tree indexes, giao dịch nguyên tử (ACID). |
| **Xác Thực & Phiên** | Flask-Login | 0.6.3 | Quản lý phiên đăng nhập an toàn, session cookie bảo vệ. |
| **Dịch Vụ AI (Cloud LLM)** | Google GenAI SDK (`google-genai`), Gemini 3.8 Flash | 1.0.0+ | Xử lý ngôn ngữ tự nhiên, tóm tắt phản hồi, soạn thảo email. |
| **Dịch Vụ AI (Local Engine)** | Scikit-learn (TF-IDF Cosine), Local Grounded Fallback | 1.4.0+ | Gợi ý sự kiện, phân loại cảm xúc, tự động fallback offline dưới 20ms. |
| **Kiểm Thử Tự Động** | Pytest, Requests | 9.1.1 / 2.31 | Bộ 42 ca kiểm thử tự động toàn diện và benchmark prompt 14 kịch bản. |

---

## 4. Các Điểm Vào Ứng Dụng (Application Entry Points)
1. **Khởi chạy ứng dụng Web cục bộ:**
   - `python run.py` (Khởi chạy máy chủ phát triển tại cổng 5000: `http://127.0.0.1:5000`).
   - `app.py` / `wsgi.py` (Cổng nạp cho máy chủ sản xuất WSGI Gunicorn: `gunicorn run:app`).
2. **Khởi tạo dữ liệu và cấu trúc bảng CSDL:**
   - `python seed.py` (Khởi tạo CSDL SQLite tại `instance/event_management.db` với 11 bảng và dữ liệu mẫu chuẩn).
   - `database/schema.sql` (Kịch bản SQL DDL độc lập phục vụ triển khai RDBMS khác).
3. **Thực thi kiểm thử tự động:**
   - `.\.venv\Scripts\pytest.exe -v` (Chạy toàn bộ 42 ca kiểm thử tự động).
   - `python eval_prompts.py` (Chạy framework đánh giá 14 kịch bản so sánh 3 phiên bản Prompt V1, V2, V3).
4. **Kiểm tra danh mục Kỹ năng Agent Skills:**
   - `npx skills list -a antigravity` (Liệt kê và kiểm tra trạng thái toàn bộ Skills cục bộ).

---

## 5. Quản Lý Thông Tin Nhạy Cảm & An Ninh Cấu Hình
- **Cấu hình môi trường:** Được lưu trữ độc lập tại tệp `.env` (đã khai báo trong `.gitignore`, không đẩy lên Git).
- **Mã bí mật API Key:** Biến `GEMINI_API_KEY` và `SECRET_KEY` được nạp qua `python-dotenv`. Nếu thiếu key, hệ thống tự động kích hoạt **Local Grounded Knowledge Engine** mà không gây sập ứng dụng.
- **Nguyên tắc Zero-PII:** Tuyệt đối không lưu trữ mật khẩu dạng plain-text, không gửi danh bạ email/sđt của khách mời lên API bên ngoài, không in token trong log.

---

## 6. Chiến Lược Khôi Phục & Bảo Toàn An Toàn (Restoration Strategy)
1. Cơ sở dữ liệu SQLite tại `instance/event_management.db` có thể tái tạo bất kỳ lúc nào thông qua `seed.py`.
2. Mọi can thiệp mã nguồn phải tuân thủ nguyên tắc thay đổi nhỏ nhất (Minimal Surgical Changes), kiểm thử ngay sau khi sửa và xác nhận không phát sinh lỗi hồi quy (No regression).
