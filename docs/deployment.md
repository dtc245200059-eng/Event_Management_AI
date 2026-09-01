# Deployment & Operations Guide
**Hệ Thống**: Quản Lý Sự Kiện Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
**Phiên Bản**: 2.0 (AI-Augmented SDLC Standard)  
**Môi Trường Hỗ Trợ**: Môi trường Cục Bộ (Local Virtualenv), Đóng Gói Docker Container, Docker Compose

---

## 1. Yêu Cầu Hệ Thống Tiên Quyết (Prerequisites)
- **Python**: Phiên bản 3.10 trở lên (khuyến nghị Python 3.10 - 3.12).
- **Docker & Docker Compose**: Nếu triển khai bằng Containerization.
- **Git**: Quản lý phiên bản mã nguồn.
- **Google Gemini API Key**: Đăng ký miễn phí tại [Google AI Studio](https://aistudio.google.com/) để kích hoạt chế độ Live Chatbot.

---

## 2. Phương Án 1: Triển Khai Cục Bộ Với Virtual Environment (Khuyến Nghị Cho Dev)

### Bước 1: Clone kho mã nguồn và di chuyển vào thư mục dự án
```bash
git clone https://github.com/your-username/Event_Management_AI.git
cd Event_Management_AI
```

### Bước 2: Khởi tạo môi trường ảo Python và kích hoạt
- **Trên Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **Trên Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt toàn bộ thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình biến môi trường `.env`
Sao chép tệp mẫu và chỉnh sửa cấu hình:
```bash
cp .env.example .env
```
Nội dung tệp `.env`:
```ini
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=event-management-ai-secret-key-2026-super-secure
DATABASE_URL=sqlite:///instance/events.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
AI_OFFLINE_MODE=False
```

### Bước 5: Nạp dữ liệu mẫu ban đầu (Seeding Data)
Hệ thống cung cấp sẵn script nạp đầy đủ các sự kiện, diễn giả, phòng hội thảo và người dùng mẫu:
```bash
python seed.py
```

### Bước 6: Khởi chạy ứng dụng Web
```bash
python run.py
```
Truy cập hệ thống tại: `http://127.0.0.1:5000`

---

## 3. Phương Án 2: Triển Khai Bằng Docker & Docker Compose (Production Ready)

Dự án đã cấu hình sẵn `Dockerfile` và `docker-compose.yml` đạt chuẩn container nhẹ và bảo mật.

### Bước 1: Khởi động hệ thống với 1 lệnh duy nhất
```bash
docker-compose up -d --build
```

### Bước 2: Kiểm tra trạng thái Container
```bash
docker-compose ps
```

### Bước 3: Xem nhật ký hoạt động (Logs)
```bash
docker-compose logs -f web
```

### Bước 4: Dừng hệ thống
```bash
docker-compose down
```

---

## 4. Danh Sách Tài Khoản Mẫu Đăng Nhập Mặc Định

| Tên Đăng Nhập (Username) | Mật Khẩu Mặc Định | Vai Trò (Role) | Chức Năng Khả Dụng |
| :--- | :--- | :--- | :--- |
| `admin` | `Admin@123` | **Quản Trị Viên (Admin)** | Toàn quyền quản lý sự kiện, vé, diễn giả, thống kê và AI Generator. |
| `staff` | `Staff@123` | **Nhân Viên (Staff)** | Truy cập giao diện quét mã QR Soát Vé tại `/checkin/scanner`. |
| `user1` | `User@123` | **Người Tham Dự (Attendee)** | Tìm kiếm sự kiện, đặt vé, xem vé điện tử và trò chuyện với AI. |

---

## 5. Chạy Kiểm Thử Tự Động (Automated Testing)
Để thực thi bộ 11 bài kiểm thử tự động với Pytest:
```bash
python -m pytest -v
```
Toàn bộ kết quả sẽ được hiển thị trên Terminal với tỷ lệ Pass 100%.
