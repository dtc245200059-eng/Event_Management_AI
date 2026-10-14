# 🚀 Hướng Dẫn Khởi Chạy Hệ Thống EventAI Pro

Tài liệu này hướng dẫn chi tiết quy trình cài đặt, cấu hình và khởi chạy ứng dụng **EventAI Pro** từ đầu trên hệ điều hành **Windows** sử dụng **PowerShell**.

---

## 1. Yêu Cầu Môi Trường

Trước khi bắt đầu, đảm bảo máy tính của bạn đã cài đặt các công cụ sau:

- **Hệ điều hành:** Windows 10 hoặc Windows 11 (64-bit).
- **Python:** Phiên bản từ **3.10** đến **3.14** (khuyến nghị Python 3.12 hoặc 3.14).
  - *Lưu ý:* Khi cài đặt Python, bắt buộc tích chọn **"Add python.exe to PATH"**.
- **Git:** Đã cài đặt [Git for Windows](https://git-scm.com/download/win).
- **Cơ sở dữ liệu:** Hệ thống mặc định sử dụng **SQLite** (đã tích hợp sẵn trong Python), không cần cài đặt thêm dịch vụ máy chủ database riêng.
- **Trình duyệt web:** Google Chrome, Microsoft Edge, Brave hoặc Firefox phiên bản mới (hỗ trợ camera HTML5 cho tính năng quét vé QR).
- **Khóa API Google Gemini (Tùy chọn):** Dùng để chạy Trợ lý AI ở chế độ trực tuyến (Live). Nếu không có API Key, hệ thống **tự động chuyển sang chế độ Offline Fallback Mock Engine**, đảm bảo toàn bộ tính năng vẫn hoạt động trơn tru mà không bị gián đoạn.

---

## 2. Mở Thư Mục Dự Án

### Trường hợp 1: Nếu đã có sẵn mã nguồn trên máy
Mở **PowerShell** và di chuyển vào thư mục dự án:
```powershell
cd D:\Event_Management_AI
```

### Trường hợp 2: Nếu tải mới từ kho lưu trữ
```powershell
git clone <URL_KHO_MA_NGUON> D:\Event_Management_AI
cd D:\Event_Management_AI
```

Kiểm tra xác nhận đang ở đúng thư mục gốc của dự án:
```powershell
Get-Location
```
*Kết quả mong đợi:* Đường dẫn hiển thị là `D:\Event_Management_AI`.

---

## 3. Tạo Môi Trường Ảo (Virtual Environment)

Sử dụng môi trường ảo giúp cô lập các thư viện của dự án, tránh xung đột với các phiên bản Python khác trên hệ điều hành.

1. Khởi tạo môi trường ảo có tên `.venv`:
   ```powershell
   python -m venv .venv
   ```
   *(Nếu lệnh `python` không nhận diện được, hãy thử thay bằng `py -m venv .venv`)*.

2. Kích hoạt môi trường ảo:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

> **Mẹo xử lý nếu gặp lỗi ExecutionPolicy:**  
> Nếu PowerShell báo lỗi *"cannot be loaded because running scripts is disabled on this system"*, hãy chạy lệnh sau để cấp quyền cho phiên làm việc hiện tại rồi kích hoạt lại:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> .\.venv\Scripts\Activate.ps1
> ```

*Dấu hiệu kích hoạt thành công:* Bạn sẽ thấy tiền tố `(.venv)` xuất hiện ở đầu dòng lệnh PowerShell.

---

## 4. Cài Đặt Thư Viện Phụ Thuộc (Dependencies)

Sau khi môi trường ảo đã được kích hoạt, thực hiện cài đặt các thư viện được định nghĩa trong file [requirements.txt](file:///D:/Event_Management_AI/requirements.txt):

1. Nâng cấp trình quản lý gói `pip` lên bản mới nhất (khuyến nghị):
   ```powershell
   python -m pip install --upgrade pip
   ```

2. Cài đặt toàn bộ dependencies của dự án:
   ```powershell
   pip install -r requirements.txt
   ```

*Kết quả mong đợi:* Tất cả các gói như `Flask`, `Flask-SQLAlchemy`, `Flask-Login`, `google-genai`, `qrcode`, `scikit-learn`, `pytest`... được tải về và cài đặt hoàn tất không có lỗi màu đỏ.

---

## 5. Cấu Hình Biến Môi Trường (`.env`)

Dự án cung cấp sẵn file mẫu [.env.example](file:///D:/Event_Management_AI/.env.example). Thực hiện sao chép sang file `.env`:

```powershell
Copy-Item .env.example .env
```

Mở file `.env` bằng VS Code, Notepad hoặc trình soạn thảo bất kỳ để kiểm tra:
```powershell
notepad .env
```

### Bảng giải thích chi tiết các biến môi trường:

| Tên biến | Bắt buộc | Giá trị mẫu / Mặc định | Ý nghĩa & Hướng dẫn |
| :--- | :---: | :--- | :--- |
| `FLASK_APP` | **Có** | `run.py` | Tệp khởi chạy chính của ứng dụng Flask. |
| `FLASK_ENV` | **Có** | `development` | Môi trường vận hành (`development` cho phát triển). |
| `FLASK_DEBUG` | **Có** | `1` | Bật chế độ gỡ lỗi và tự động tải lại server khi sửa code. |
| `SECRET_KEY` | **Có** | `event_mgmt_ai_secret_super_key_2026` | Chuỗi ký tự bảo mật phiên đăng nhập của người dùng. |
| `DATABASE_URI` | **Có** | `sqlite:///event_management.db` | Đường dẫn kết nối CSDL SQLite cục bộ. |
| `GEMINI_API_KEY` | *Tùy chọn* | `your_gemini_api_key_here` | Khóa API lấy từ [Google AI Studio](https://aistudio.google.com/). Nếu không có, hãy để nguyên hoặc để trống. |
| `GEMINI_MODEL` | *Tùy chọn* | `gemini-2.5-flash` | Định danh mô hình ngôn ngữ lớn của Gemini. |
| `ENABLE_AI_FALLBACK_MOCK` | **Có** | `True` | Bật chế độ tự động chuyển sang AI Mock Engine khi không có Internet hoặc không có API Key hợp lệ. |
| `RATE_LIMIT_PER_MINUTE` | *Tùy chọn* | `20` | Giới hạn số lượt gọi AI tối đa trên mỗi phút. |

> **Lưu ý an toàn:** Tuyệt đối không commit file `.env` chứa API Key thật hoặc mật khẩu lên GitHub hay các kho lưu trữ công cộng.

---

## 6. Khởi Tạo Cơ Sở Dữ Liệu & Dữ Liệu Mẫu

Cơ sở dữ liệu của EventAI Pro được thiết kế chuẩn 3NF gồm 11 bảng. Dự án có sẵn script [seed.py](file:///D:/Event_Management_AI/seed.py) giúp tự động tạo cấu trúc bảng, nạp 10+ sự kiện công nghệ thực tế, phân bổ vé, lịch trình, diễn giả và sinh sẵn mã QR vé điện tử.

Chạy lệnh nạp dữ liệu:
```powershell
python seed.py
```

*Kết quả mong đợi:*
- Xuất hiện thông báo: `🌱 Đang làm sạch và khởi tạo lại Cơ sở Dữ liệu 9 bảng chuẩn 3NF...`
- Tạo thành công các tài khoản mẫu: `admin`, `organizer`, `staff1`, `attendee1`, `attendee2`, `attendee3`.
- Nạp đầy đủ các sự kiện tiêu biểu, diễn giả, phiên thảo luận, hạng vé và mã QR SVG.
- File `event_management.db` xuất hiện tại thư mục gốc của dự án.

*(Tùy chọn) Nếu chỉ muốn tạo bảng trắng không có dữ liệu mẫu:*
```powershell
python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('Tạo cấu trúc bảng thành công!')"
```

---

## 7. Khởi Chạy Máy Chủ Ứng Dụng

Đảm bảo đang ở thư mục gốc `D:\Event_Management_AI` và môi trường ảo `(.venv)` đang hoạt động. Chạy lệnh:

```powershell
python run.py
```
*(Bạn cũng có thể chạy bằng lệnh alias tương đương: `python app.py`)*.

### Kết quả hiển thị trên màn hình:
```text
 * Serving Flask app 'run.py'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://<địa_chỉ_IP_máy>:5000
Press CTRL+C to quit
```

### Truy cập hệ thống:
Mở trình duyệt web và truy cập vào địa chỉ:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (hoặc `http://localhost:5000`)

*Dấu hiệu kiểm tra hoạt động bình thường:*
- Trang chủ hiển thị giao diện **Apple Liquid Glass** với thanh điều hướng trong suốt.
- Danh sách sự kiện công nghệ và banner nổi bật xuất hiện đầy đủ.
- Nút tròn biểu tượng AI lấp lánh (Sparkles) hiển thị ở góc dưới bên phải màn hình.

---

## 8. Đăng Nhập Và Trải Nghiệm Chức Năng

Hệ thống phân quyền 4 vai trò (RBAC) được cấu hình sẵn các tài khoản demo sau khi chạy `seed.py`:

| Vai Trò | Tên Đăng Nhập | Mật Khẩu | Trang Chức Năng Chính | Mô Tả Trải Nghiệm |
| :--- | :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `Admin@123` | `/admin/dashboard` | Xem bảng điều khiển Analytics, biểu đồ Chart.js, dự báo show-up AI, quản trị phân quyền Users. |
| **Ban tổ chức (Organizer)**| `organizer` | `Organizer@123`| `/events/manage` | Tạo mới sự kiện, cấu hình vé, lịch trình, diễn giả, soạn thảo email AI tại `/notifications/create`. |
| **Nhân viên soát vé (Staff)**| `staff1` | `Staff@123` | `/checkin` | Soát vé bằng Camera Web quét mã QR hoặc nhập mã vé thủ công để ghi nhận check-in thời gian thực. |
| **Người tham dự (Attendee)**| `attendee1` | `User@123` | `/tickets/my-tickets` | Xem danh sách vé đã đặt, mở thẻ vé điện tử boarding pass, tải ảnh QR hoặc in thẻ vé chuẩn A4. |

### Hướng dẫn đăng ký tài khoản mới:
Nếu muốn tạo tài khoản mới từ giao diện:
1. Truy cập: `http://127.0.0.1:5000/auth/register`.
2. Điền Họ tên, Tên đăng nhập, Email, Mật khẩu và bấm **"Đăng Ký"**.
3. Sau khi tạo thành công, hệ thống tự động gán vai trò `attendee` để bạn trải nghiệm đặt vé và trò chuyện với Trợ lý AI.

---

## 9. Dừng Hệ Thống & Thoát Môi Trường Ảo

Khi muốn kết thúc phiên làm việc:

1. **Dừng máy chủ Flask:** Nhấn tổ hợp phím `Ctrl + C` tại cửa sổ PowerShell đang chạy server.
2. **Hủy kích hoạt môi trường ảo:**
   ```powershell
   deactivate
   ```
*Dấu hiệu thành công:* Tiền tố `(.venv)` biến mất khỏi dòng lệnh PowerShell.

---

## 10. Xử Lý Các Sự Cố Thường Gặp (Troubleshooting)

### 1. Lỗi PowerShell không cho kích hoạt môi trường ảo
- **Hiện tượng:** `File .venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`
- **Nguyên nhân:** Chính sách ExecutionPolicy mặc định của Windows PowerShell chặn script ngoại vi.
- **Cách xử lý:** Chạy lệnh sau trong PowerShell trước khi activate:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\.venv\Scripts\Activate.ps1
  ```

### 2. Lỗi cổng 5000 đã bị chiếm dụng (Port Conflict)
- **Hiện tượng:** `OSError: [Errno 10048] Only one usage of each socket address is normally permitted`
- **Nguyên nhân:** Một tiến trình khác (hoặc phiên bản Flask cũ chưa tắt) đang dùng cổng 5000.
- **Cách xử lý:** Đổi sang cổng khác (ví dụ 5001) bằng biến môi trường tạm thời:
  ```powershell
  $env:PORT="5001"
  python run.py
  ```
  Sau đó truy cập qua: `http://127.0.0.1:5001`.

### 3. Lỗi thiếu bảng cơ sở dữ liệu (`no such table`)
- **Hiện tượng:** `sqlite3.OperationalError: no such table: events` hoặc lỗi tương tự khi truy cập trang web.
- **Nguyên nhân:** File CSDL chưa được khởi tạo bảng.
- **Cách xử lý:** Chạy lại lệnh seeder:
  ```powershell
  python seed.py
  ```

### 4. Lỗi Trợ lý AI không phản hồi hoặc báo lỗi API
- **Hiện tượng:** Chatbot trả về thông báo lỗi hoặc không kết nối được tới dịch vụ Gemini.
- **Nguyên nhân:** Chưa cấu hình `GEMINI_API_KEY` hoặc mạng bị chặn.
- **Cách xử lý:** Mở file `.env`, đảm bảo có dòng sau:
  ```ini
  ENABLE_AI_FALLBACK_MOCK=True
  ```
  Hệ thống sẽ ngay lập tức kích hoạt bộ suy luận nội bộ (Mock Engine), phản hồi chính xác dựa trên dữ liệu sự kiện có trong CSDL mà không cần kết nối mạng ra ngoài.

### 5. Trình duyệt không mở được Camera khi vào trang Soát vé (`/checkin`)
- **Hiện tượng:** Màn hình quét QR hiển thị đen hoặc báo *"Permission denied"*.
- **Cách xử lý:** Bấm vào biểu tượng ổ khóa hoặc camera trên thanh địa chỉ URL của trình duyệt, chọn **"Allow" (Cho phép)** quyền truy cập Camera cho địa chỉ `http://127.0.0.1:5000`, sau đó tải lại trang (`F5`).

---

## 11. Kiểm Thử Hệ Thống Tự Động (Tùy Chọn)

Để kiểm tra độ tương thích và tính toàn vẹn của toàn bộ hệ thống sau khi cài đặt, bạn có thể thực thi bộ kiểm thử tự động gồm 36 test cases:

```powershell
pytest -v
```

*Kết quả mong đợi:*
```text
============================= 36 passed in ~56s =============================
```
Mọi test cases liên quan đến phân quyền, hạn ngạch vé, thuật toán AI gợi ý và Multi-Agent đều phải đạt trạng thái `PASSED`.
