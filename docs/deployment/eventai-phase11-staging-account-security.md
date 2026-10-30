# EventAI Pro — An Toàn Tài Khoản Mẫu & Quản Lý Mã Bí Mật Staging (Account Security)

> **Mã tài liệu:** `docs/deployment/eventai-phase11-staging-account-security.md`  
> **Giai đoạn:** Phase 11 — Windows Native Final QA & Security Hardening  
> **Kiến trúc:** Windows 11 Native Architecture (Zero VM / Zero Docker / Zero WSL)  
> **Các tệp kịch bản:** `scripts\seed_staging.py`, `scripts\get_staging_credentials.py`  
> **Tệp bí mật:** `instance_staging\.staging_secrets.json` (Loại trừ Git)  
> **Trạng thái:** HOÀN THIỆN & ĐẠT CHUẨN AN TOÀN (HARDENED & VERIFIED)

---

## 1. MỤC TIÊU CẢI TIẾN BẢO MẬT GIAI ĐOẠN PHASE 11

Trong các giai đoạn trước, các tài khoản kiểm thử mẫu thường sử dụng mật khẩu cố định dễ nhớ (như `Admin@123`, `Staff@123`) và được in trực tiếp ra tài liệu báo cáo. Mặc dù các tài khoản này chỉ tồn tại trong cơ sở dữ liệu biệt lập `instance_staging\staging.db`, việc sử dụng mật khẩu cố định tiềm ẩn các rủi ro bảo mật:
1. Nguy cơ người vận hành vô tình áp dụng lại các mật khẩu mẫu này lên môi trường thực tế.
2. Tiết lộ cấu trúc chứng thực trong tài liệu lưu trữ.
3. Thiếu tính ngẫu nhiên và độ phức tạp theo tiêu chuẩn mật khẩu hiện đại.

Trong Phase 11, quy trình khởi tạo dữ liệu mẫu đã được **tái cấu trúc và tăng cường bảo mật toàn diện (Security Hardening)** theo chuẩn mật mã học Python `secrets`.

---

## 2. BẢNG KIỂM TRA ĐỐI SOÁT 9 TIÊU CHÍ AN TOÀN TÀI KHOẢN MẪU

| STT | Tiêu chí an toàn | Hiện thực kỹ thuật trong EventAI Pro | Đánh giá |
| :---: | :--- | :--- | :---: |
| 1 | **Không nhập khẩu tài khoản thực** | Dữ liệu mẫu được sinh mới 100% qua ORM, không kết nối tới production | **ĐẠT (PASS)** |
| 2 | **Không tái sử dụng thông tin thật** | Tên người dùng và email hoàn toàn mang tính định danh giả lập | **ĐẠT (PASS)** |
| 3 | **Không để lọt mật khẩu vào code** | Loại bỏ hoàn toàn chuỗi mật khẩu cứng trong `seed_staging.py` | **ĐẠT (PASS)** |
| 4 | **Phạm vi tài khoản rõ ràng** | Tên miền email mang hậu tố cục bộ: `@staging.eventai.local` | **ĐẠT (PASS)** |
| 5 | **Tính bất biến & Lặp lại (Idempotent)**| Kiểm tra sự tồn tại của dữ liệu trước khi sinh; tái sử dụng mã bí mật | **ĐẠT (PASS)** |
| 6 | **Lưu trữ bí mật cục bộ an toàn** | Lưu tại `instance_staging\.staging_secrets.json` với phân quyền máy host | **ĐẠT (PASS)** |
| 7 | **Loại trừ tuyệt đối khỏi Git** | Thư mục `instance_staging/` đã được bổ sung vào `.gitignore` | **ĐẠT (PASS)** |
| 8 | **Duy trì đầy đủ xác thực & RBAC** | Mật khẩu được băm qua PBKDF2-SHA256; bảo vệ phân quyền 4 vai trò | **ĐẠT (PASS)** |
| 9 | **Vô hiệu hóa gửi thư ra ngoài** | Không cấu hình cổng SMTP ngoài; thông báo chỉ ghi vào CSDL staging | **ĐẠT (PASS)** |

---

## 3. CƠ CHẾ SINH MẬT MÃ MẪU NGẪU NHIÊN CẤP CAO (HIGH-ENTROPY SECRETS GENERATOR)

Trong tệp `scripts/seed_staging.py`, hàm sinh mật khẩu sử dụng module `secrets` (bộ sinh số ngẫu nhiên an toàn cho mật mã của nhân hệ điều hành):

```python
alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
def gen_pwd():
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(18))
        if (any(c.islower() for c in pwd) and
            any(c.isupper() for c in pwd) and
            any(c.isdigit() for c in pwd) and
            any(c in "!@#$%^&*" for c in pwd)):
            return pwd
```

### Đặc tính kỹ thuật của Mật khẩu Mẫu mới:
- **Độ dài:** 18 ký tự (vượt xa chuẩn khuyến nghị 12 ký tự của NIST).
- **Không gian ký tự:** Kết hợp chữ hoa, chữ thường, chữ số và ký tự đặc biệt (`!@#$%^&*`).
- **Entropy tính toán:** $\approx 18 \times \log_2(70) \approx 110.3$ bits entropy (chống tấn công vét cạn brute-force tuyệt đối).

---

## 4. QUY TRÌNH TRUY XUẤT THÔNG TIN ĐĂNG NHẬP CỤC BỘ (SECURE RETRIEVAL RUNBOOK)

> [!CAUTION]
> **Tuân thủ quy tắc bảo mật:** Antigravity **TUYỆT ĐỐI KHÔNG IN MẬT KHẨU HOẶC KHÓA BÍ MẬT RA TÀI LIỆU BÁO CÁO NÀY**.  
> Người vận hành trực tiếp trên máy tính Windows 11 có thể xem thông tin đăng nhập phục vụ kiểm thử theo các bước dưới đây:

### Các bước lấy thông tin đăng nhập:
1. Mở PowerShell tại thư mục dự án `D:\Event_Management_AI`.
2. Thực thi script truy xuất thông tin dành riêng cho máy cục bộ:
   ```powershell
   .\.venv\Scripts\python.exe scripts\get_staging_credentials.py
   ```
3. Màn hình console sẽ hiển thị bảng thông tin đăng nhập của 4 vai trò:
   - **Quản Trị Viên (Admin):** Username `admin_staging` | Email `admin@staging.eventai.local`
   - **Nhân Viên Soát Vé (Staff):** Username `staff_staging` | Email `staff@staging.eventai.local`
   - **Ban Tổ Chức (Organizer):** Username `organizer_staging` | Email `organizer@staging.eventai.local`
   - **Khách Tham Dự (Attendee):** Username `attendee_staging` | Email `attendee@staging.eventai.local`
4. Sử dụng thông tin trên để đăng nhập tại giao diện web:
   `http://127.0.0.1:5001/auth/login`
5. Bộ kịch bản tự động `scripts/verify_staging_workflows.py` tự động đọc tệp `.staging_secrets.json` này để thực thi kiểm thử mà không cần can thiệp thủ công.

---

## 5. THIẾT LẬP LẠI TOÀN BỘ MẬT KHẨU STAGING (CREDENTIALS ROTATION)

Nếu người vận hành muốn thu hồi toàn bộ mật khẩu cũ và sinh mới một bộ thông tin ngẫu nhiên khác:
```powershell
.\.venv\Scripts\python.exe scripts\seed_staging.py --reseed
```
*Script sẽ xóa sạch dữ liệu cũ trong `instance_staging\staging.db`, sinh lại bộ mã bí mật mới vào `instance_staging\.staging_secrets.json` và khởi tạo lại toàn bộ 11 bảng dữ liệu mẫu.*

