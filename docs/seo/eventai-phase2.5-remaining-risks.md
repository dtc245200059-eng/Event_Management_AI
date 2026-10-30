# EventAI Pro — Phase 2.5 Remaining Risks & Operational Advisories

**Ngày báo cáo:** 29/10/2026  
**Đơn vị thực hiện:** Nhóm Kiểm toán An ninh Ứng dụng & Kỹ sư Cấp cao  
**Mục tiêu:** Công khai minh bạch các rủi ro kỹ thuật còn tồn đọng, các hành động đòi hỏi con người phê duyệt (Human Authorization Required), và các khuyến nghị kiến trúc cho môi trường triển khai thực tế.  

---

## 1. NGUYÊN TẮC BẢO MẬT & TÍNH KHÁCH QUAN

> [!IMPORTANT]
> **Tuyên bố an ninh:** Mặc dù Giai đoạn 2.5 đã giải quyết triệt để các lỗ hổng cấp bách nhất (xóa mật khẩu khỏi template công khai, thiết lập rào chắn xác thực cho tệp mã QR tĩnh và khóa quyền truy cập sự kiện bản nháp), **không có hệ thống nào đạt mức độ an toàn tuyệt đối 100%**. Dưới đây là các rủi ro còn tồn tại và các biện pháp giảm thiểu tương ứng.

---

## 2. BẢNG DANH MỤC CÁC RỦI RO KỸ THUẬT CÒN TỒN ĐỌNG

| Mã Rủi Ro | Phân loại | Mức độ | Mô tả chi tiết rủi ro | Biện pháp giảm thiểu hiện tại | Khuyến nghị hành động tiếp theo |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **RSK-01** | Credential Exposure | **MEDIUM** | Mật khẩu tài khoản mẫu (`Admin@123`, `Staff@123`, `User@123`) vẫn tồn tại trong CSDL `event_management.db` và tệp `seed.py`. | Đã xóa khỏi giao diện HTML công khai; bot tìm kiếm không thể thu thập được. | **CẦN CON NGƯỜI PHÊ DUYỆT:** Đổi mật khẩu tài khoản quản trị khi triển khai staging/production. |
| **RSK-02** | Static Asset Serving | **MEDIUM** | Phục vụ mã QR vé qua hook `@app.before_request` trên đường dẫn `/static/qr_codes/`. | Ứng dụng Python/Flask kiểm tra quyền sở hữu vé và vai trò Staff chặt chẽ (HTTP 403 cho người lạ). | Di chuyển tệp QR ra ngoài thư mục `static/` sang `storage/` nếu sử dụng Reverse Proxy Nginx phục vụ static trực tiếp. |
| **RSK-03** | Brute-force Login | **LOW** | Tuyến `/auth/login` chưa tích hợp bộ đếm giới hạn số lần thử đăng nhập sai (Account Lockout / Rate Limiting). | Mật khẩu được băm bằng chuẩn an toàn Werkzeug PBKDF2/scrypt. | Tích hợp thư viện `Flask-Limiter` (giới hạn 5 lần đăng nhập sai/phút) trong Phase 3 hoặc trước khi Go-Live. |
| **RSK-04** | Missing Crawl Directives | **LOW** | Tệp `robots.txt` và `sitemap.xml` vẫn chưa được tạo (trả về HTTP 404). | Các trang nhạy cảm đã có thẻ `<meta name="robots" content="noindex">` và header `X-Robots-Tag`. | Triển khai theo kế hoạch tại **Phase 3C**. |
| **RSK-05** | Lack of Structured Data | **LOW** | Chưa có Schema.org Event JSON-LD cho các sự kiện công khai. | Đã hoàn tất bản thiết kế mẫu chi tiết và kiểm chứng mô hình dữ liệu. | Triển khai theo kế hoạch tại **Phase 3B**. |
| **RSK-06** | Content Security Policy | **LOW** | Chưa thiết lập tiêu đề `Content-Security-Policy` (CSP) toàn diện. | Đã thiết lập `Permissions-Policy: camera=*, microphone=*` cho tính năng quét vé và micro AI. | Bổ sung tiêu đề CSP nghiêm ngặt trong cấu hình môi trường Production. |

---

## 3. CÁC HÀNH ĐỘNG ĐÒI HỎI CON NGƯỜI PHÊ DUYỆT (HUMAN AUTHORIZATION REQUIRED)

### 3.1. Đổi mật khẩu tài khoản Quản trị & Tài khoản Mẫu (Credential Rotation):
- **Bối cảnh:** Mặc dù mật khẩu không còn hiển thị trên giao diện web, chuỗi mật khẩu `Admin@123` đã được ghi nhận trong lịch sử cam kết git cũ và tệp seed dữ liệu `seed.py`.
- **Hành động yêu cầu:** Người vận hành hệ thống (Operator / User) cần tự tay thực hiện đổi mật khẩu tài khoản `admin` thông qua tính năng đổi mật khẩu tại trang Hồ sơ (`/auth/profile`) hoặc chạy lệnh cập nhật băm mật khẩu trong môi trường sản xuất.
- **Lý do AI không tự ý đổi:** AI tuyệt đối không tự động thay đổi mật khẩu quản trị thật của người dùng để tránh nguy cơ khóa tài khoản (Lockout) ngoài ý muốn.

### 3.2. Cấu hình Nginx / Reverse Proxy khi triển khai thực tế (Production Deployment):
- **Bối cảnh:** Hiện tại cơ chế bảo vệ mã QR vé hoạt động thông qua hook `@app.before_request` của Flask. Khi chạy bằng Flask development server hoặc Gunicorn đơn thuần, mọi yêu cầu `/static/qr_codes/*` đều đi qua Python và được bảo vệ 100%.
- **Lưu ý kiến trúc:** Nếu sau này người dùng cấu hình Nginx với chỉ thị:
  ```nginx
  location /static/ {
      alias /path/to/app/static/; # Nginx phục vụ trực tiếp, bỏ qua Flask!
  }
  ```
  Khi đó Nginx sẽ phục vụ tệp trực tiếp từ ổ cứng mà không chạy qua hook `@app.before_request`.
- **Khuyến nghị cấu hình Nginx chuẩn:**
  ```nginx
  # Chặn Nginx phục vụ trực tiếp thư mục qr_codes, chuyển tiếp về Flask để xác thực
  location /static/qr_codes/ {
      proxy_pass http://127.0.0.1:5000;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
  }
  ```

---

## 4. KẾT LUẬN & SẴN SÀNG CHO GIAI ĐOẠN 3A

Hệ thống đã đạt đầy đủ các tiêu chuẩn an toàn cốt lõi:
- **Không có thông tin đăng nhập nào bị rò rỉ.**
- **Không có mã QR vé nào bị truy cập công khai ẩn danh hoặc truy cập chéo.**
- **Không có sự kiện bản nháp nội bộ nào bị người ngoài truy cập.**
- **100% các bài kiểm thử tự động (54/54 tests) đều vượt qua.**

Hệ thống sẵn sàng bước vào **Phase 3A — Tối ưu hóa Siêu dữ liệu Cốt lõi & Chỉ mục Tìm kiếm (Core Metadata & Indexing Fixes)**.

