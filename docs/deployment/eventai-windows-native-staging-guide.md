# EventAI Pro — Sổ Tay Vận Hành Môi Trường Staging Bản Địa Windows 11 (Windows Native Staging Guide)

> **Tài liệu tham chiếu DevSecOps & QA:** `docs/deployment/eventai-windows-native-staging-guide.md`  
> **Phiên bản kiến trúc:** Windows 11 Native Architecture (Zero VM / Zero Docker / Zero WSL)  
> **Môi trường thực thi:** Python 3.14.2 64-bit (`D:\Event_Management_AI\.venv`)  
> **Cơ sở dữ liệu Staging:** `instance_staging\staging.db` (Cách ly 100% với CSDL gốc)  
> **Trạng thái:** SẴN SÀNG VẬN HÀNH (OPERATIONAL)

---

## 1. TỔNG QUAN & QUYẾT ĐỊNH LOẠI BỎ HOÀN TOÀN MÁY ẢO (NO-VM DECISION)

Theo quyết định chỉ đạo từ người dùng, toàn bộ các phương án sử dụng máy ảo và container hóa bao gồm:
- VMware Workstation / Player
- VirtualBox
- Ubuntu Virtual Machines (Ubuntu Server 24.04 LTS)
- Windows Subsystem for Linux (WSL2)
- Docker Desktop cho Windows

**ĐÃ BỊ HỦY BỎ HOÀN TOÀN KHỎI DỰ ÁN EVENTAI PRO.**

Hệ thống EventAI Pro được chuẩn hóa và vận hành **trực tiếp như một ứng dụng Windows 11 bản địa (Native Windows Application)** trên nền tảng Python 3.14.2 chuyên dụng tại thư mục dự án `D:\Event_Management_AI`.

### Lợi thế của Kiến trúc Windows Bản địa:
1. **Hiệu năng tối đa & Không tiêu hao tài nguyên ảo hóa:** Loại bỏ gánh nặng phân bổ 4GB-8GB RAM và CPU ảo hóa của hypervisor; ứng dụng khởi động tức thì trong 1.5 giây.
2. **Không xung đột phần cứng:** Không gặp vấn đề chia sẻ cổng mạng (NAT/Bridged Network), không tranh chấp thiết bị USB hay driver camera ảo.
3. **Cách ly dữ liệu tuyệt đối:** Sử dụng cây thư mục biệt lập `instance_staging\` cho database kiểm thử, đảm bảo cơ sở dữ liệu gốc `instance\event_management.db` không bao giờ bị ghi đè hay thay đổi thuộc tính.
4. **Tích hợp trình duyệt bản địa:** Tận dụng trực tiếp Microsoft Edge Core v156 (Blink engine) có sẵn trên Windows 11 để thực hiện kiểm thử E2E trung thực 100%.

---

## 2. KIẾN TRÚC & MÔ HÌNH CÔ LẬP MÔI TRƯỜNG (ISOLATION ARCHITECTURE)

```
+-------------------------------------------------------------------------------+
|                             WINDOWS 11 HOST (64-BIT)                          |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  |                      D:\Event_Management_AI                             |  |
|  |                                                                         |  |
|  |  +--------------------------+           +----------------------------+  |  |
|  |  |   MÔI TRƯỜNG PRODUCTION   |           |    MÔI TRƯỜNG STAGING NATIVE|  |  |
|  |  |                          |           |                            |  |  |
|  |  | * Config: Production     |           | * Config: StagingConfig    |  |  |
|  |  | * DB: instance/          |           | * DB: instance_staging/    |  |  |
|  |  |   event_management.db    |           |   staging.db (180 KB)      |  |  |
|  |  |   (253 KB - BẢO VỆ TUYỆT |           | * Port: 127.0.0.1:5001     |  |  |
|  |  |    ĐỐI, KHÔNG CHẠM)      |           | * Runner: run_staging_     |  |  |
|  |  +--------------------------+           |   windows.py               |  |  |
|  |                                         +----------------------------+  |  |
|  |                                                       ^                 |  |
|  +-------------------------------------------------------|-----------------+  |
|                                                          |                    |
|             +--------------------------------------------+                    |
|             |                                                                 |
|  +---------------------+   +---------------------+   +---------------------+  |
|  | Microsoft Edge v156 |   | 14 E2E Workflows    |   | 218 Pytest Baseline |  |
|  | (Blink Headless)    |   | (verify_staging.py) |   | (tests/ - 100% PASS)|  |
|  +---------------------+   +---------------------+   +---------------------+  |
+-------------------------------------------------------------------------------+
```

### Bảng Đối Soát An Toàn Cơ Sở Dữ Liệu:

| Thông số | Cơ sở dữ liệu Sản xuất (Production) | Cơ sở dữ liệu Staging (Windows Native) |
| :--- | :--- | :--- |
| **Đường dẫn tệp** | `D:\Event_Management_AI\instance\event_management.db` | `D:\Event_Management_AI\instance_staging\staging.db` |
| **Kích thước tệp** | `253,952 bytes` | `180,224 bytes` |
| **Thời điểm sửa đổi cuối** | `2026-10-14 20:58:05` (Bất biến) | Sinh mới & reseed định kỳ |
| **Cơ chế bảo vệ** | Bất khả xâm phạm; Runner staging không trỏ URI vào đây | Phục vụ toàn bộ dữ liệu mẫu (synthetic data) |
| **Biến môi trường URI**| `sqlite:///instance/event_management.db` | `sqlite:///D:/Event_Management_AI/instance_staging/staging.db` |

---

## 3. THÔNG SỐ CẤU HÌNH STAGING (`StagingConfig`)

Trong tệp `config.py`, lớp `StagingConfig` được thiết kế chuyên biệt cho kiểm thử thực tế trên Windows:

```python
class StagingConfig(Config):
    ENV_NAME = 'staging'
    DEBUG = False                   # Tắt debug để kiểm thử trang lỗi 404, 500 thực tế
    TESTING = False                 # Tắt testing để kích hoạt đầy đủ CSRF middleware
    WTF_CSRF_ENABLED = True         # BẮT BUỘC: Kiểm thử toàn diện CSRF token
    SESSION_COOKIE_SECURE = False   # Cho phép HTTP trên loopback 127.0.0.1
    SESSION_COOKIE_HTTPONLY = True  # Chống rò rỉ session qua XSS
    SESSION_COOKIE_SAMESITE = 'Lax' # Bảo vệ điều hướng CSRF tiêu chuẩn OWASP
    ENABLE_AI_FALLBACK_MOCK = True  # Kích hoạt Local AI Fallback Engine
```

> [!IMPORTANT]
> `SESSION_COOKIE_SECURE = False` là bắt buộc khi chạy trên `http://127.0.0.1:5001` (HTTP loopback) để trình duyệt không loại bỏ cookie phiên sau khi đăng nhập. Mọi cơ chế bảo vệ khác (`HttpOnly`, `SameSite=Lax`, `WTF_CSRF_ENABLED`) đều được kích hoạt ở mức nghiêm ngặt nhất.

---

## 4. BỘ KỊCH BẢN ĐIỀU KHIỂN & VẬN HÀNH (OPERATIONAL SCRIPTS)

Dự án cung cấp trọn bộ script tự động hóa trên Windows:

### 4.1 Khởi động Staging Server
Có 2 cách khởi động:

**Cách 1: Khởi động nền bằng PowerShell (Khuyến nghị)**
```powershell
powershell -ExecutionPolicy Bypass -File .\start_staging_windows.ps1
```
*Script sẽ kiểm tra cổng 5001, khởi động tiến trình Python nền, ghi log vào `instance_staging\staging.log`, lưu PID vào `instance_staging\staging_server.pid`, và kiểm tra sức khỏe HTTP 200 trước khi báo thành công.*

**Cách 2: Chạy trực tiếp qua Python trong terminal**
```powershell
.\.venv\Scripts\python.exe run_staging_windows.py
```
*Tự động kiểm tra và sinh cơ sở dữ liệu `instance_staging\staging.db` nếu chưa có, in bảng thông tin tài khoản và lắng nghe yêu cầu trực tiếp.*

### 4.2 Dừng Staging Server
```powershell
powershell -ExecutionPolicy Bypass -File .\stop_staging_windows.ps1
```
*Script sẽ đọc file PID và quét các tiến trình đang lắng nghe trên cổng 5001 để dừng máy chủ một cách an toàn và dọn dẹp tài nguyên.*

### 4.3 Khởi tạo dữ liệu mẫu (Database Seeding)
```powershell
.\.venv\Scripts\python.exe scripts\seed_staging.py
```
*Tạo mới cấu trúc bảng và nạp 4 tài khoản mẫu, 1 địa điểm, 1 sự kiện công nghệ, 1 vé tham dự kèm mã QR SVG, 1 hồ sơ người tham dự, 1 diễn giả, 1 phiên lịch trình và 2 mục câu hỏi thường gặp FAQ.*

### 4.4 Kiểm tra đối soát bảng dữ liệu Staging
```powershell
.\.venv\Scripts\python.exe scripts\verify_staging_db.py
```
*In số lượng bản ghi của toàn bộ 11 bảng trong `instance_staging\staging.db`.*

### 4.5 Thực thi bộ kiểm thử 14 luồng nghiệp vụ Staging
```powershell
.\.venv\Scripts\python.exe scripts\verify_staging_workflows.py
```
*Kiểm thử tự động 14 luồng tích hợp: Đăng nhập Admin/Staff/Attendee, Dashboard, AI Chatbot RAG, Check-in vé, Chống trùng lặp vé (409 Conflict), Đăng xuất POST CSRF, và Từ chối CSRF (400 Bad Request).*

### 4.6 Chụp ảnh kiểm thử giao diện trình duyệt Edge
```powershell
.\.venv\Scripts\python.exe scripts\capture_edge_qa.py
```
*Điều khiển Microsoft Edge Core v156 ở chế độ Headless để render DOM và chụp 4 bức ảnh visual evidence lưu tại thư mục `scratch\`.*

---

## 5. DANH BẠ TÀI KHOẢN MẪU PHỤC VỤ KIỂM THỬ (SYNTHETIC PERSONAS)

Toàn bộ tài khoản kiểm thử đã được nạp sẵn mật khẩu băm an toàn theo chuẩn Werkzeug PBKDF2:

| Vai trò (Role) | Email đăng nhập | Mật khẩu | Quyền hạn trong hệ thống |
| :--- | :--- | :--- | :--- |
| **Quản Trị Viên (Admin)** | `admin@eventai.vn` | `Admin@123` | Toàn quyền quản trị hệ thống, người dùng, sự kiện, thống kê |
| **Nhân Viên Check-in (Staff)** | `staff@eventai.vn` | `Staff@123` | Truy cập bảng điều khiển check-in, quét QR, xác thực vé |
| **Ban Tổ Chức (Organizer)** | `organizer@eventai.vn` | `Organizer@123` | Tạo/chỉnh sửa sự kiện, lịch trình, diễn giả, phát hành vé |
| **Khách Tham Dự (Attendee)** | `attendee@eventai.vn` | `User@123` | Xem sự kiện, xem vé điện tử của tôi (`/tickets/my-tickets`), hỏi đáp AI |

---

## 6. QUY TẮC AN TOÀN VÀ RANH GIỚI BẢO MẬT HỆ THỐNG

1. **Ranh giới Mạng (Network Boundary):** Máy chủ staging được cấu hình gắn chặt vào địa chỉ loopback `127.0.0.1`. Không mở cổng ra mạng bên ngoài hoặc card mạng công cộng (Public IP).
2. **Quyền riêng tư Dữ liệu:** Tuyệt đối không sử dụng dữ liệu thực tế, email cá nhân hay API key thương mại trong môi trường staging.
3. **An toàn Git (Zero Git Pollution):** Thư mục `instance_staging\` và `scratch\` được cấu hình cách ly, không được đưa vào commit hay push lên kho lưu trữ từ xa.

