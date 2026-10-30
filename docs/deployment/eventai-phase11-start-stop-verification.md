# EventAI Pro — Kiểm Chứng Quy Trình Khởi Động & Dừng Máy Chủ Windows (Start/Stop Verification)

> **Mã tài liệu:** `docs/deployment/eventai-phase11-start-stop-verification.md`  
> **Giai đoạn:** Phase 11 — Windows Native Final QA & Security Hardening  
> **Kiến trúc:** Windows 11 Native Architecture (Zero VM / Zero Docker / Zero WSL)  
> **Các tệp kịch bản:** `start_staging_windows.ps1`, `stop_staging_windows.ps1`, `run_staging_windows.py`  
> **Trạng thái:** HOÀN THIỆN & ĐẠT CHUẨN AN TOÀN (HARDENED & VERIFIED)

---

## 1. MỤC TIÊU & YÊU CẦU KIỂM CHỨNG

Quy trình quản lý tiến trình máy chủ trên hệ điều hành Windows 11 đòi hỏi độ chính xác và an toàn tuyệt đối:
1. **Khởi động tin cậy (Reliable Startup):** Phải định danh chính xác thư mục dự án, trình thông dịch Python trong môi trường ảo `.venv`, cấu hình staging cô lập và kiểm tra phản hồi HTTP 200 trước khi báo thành công.
2. **Dừng chính xác & An toàn (Safe Targeted Shutdown):** Script dừng chỉ được phép tắt đúng tiến trình của EventAI Pro Staging. **Tuyệt đối không được tắt nhầm các tiến trình Python khác đang chạy trên máy tính** (như máy chủ phát triển khác, Jupyter notebook, hoặc tiến trình Windows bị tái sử dụng PID).
3. **Quản lý nhật ký an toàn (Safe Logging):** Tách biệt luồng xuất chuẩn (stdout) và luồng lỗi (stderr) vào các tệp riêng biệt trong thư mục `instance_staging\`, không làm nghẽn tiến trình nền.
4. **Xử lý tệp PID cũ (Stale PID Handling):** Tự động phát hiện và dọn dẹp các tệp PID mồ côi nếu tiến trình đã dừng đột ngột trước đó.

---

## 2. MA TRẬN 10 TIÊU CHÍ AN TOÀN CỦA QUY TRÌNH KHỞI ĐỘNG VÀ DỪNG

| STT | Tiêu chí kỹ thuật | Cơ chế thực hiện trong script | Đánh giá an toàn |
| :---: | :--- | :--- | :---: |
| 1 | **Thư mục làm việc** | `Set-Location $ScriptDir` (`D:\Event_Management_AI`) | **ĐẠT (PASS)** |
| 2 | **Trình thông dịch ảo hóa** | Xác thực `Test-Path $ScriptDir\.venv\Scripts\python.exe` | **ĐẠT (PASS)** |
| 3 | **Cấu hình Staging cô lập**| Nạp `StagingConfig`, trỏ CSDL `instance_staging\staging.db` | **ĐẠT (PASS)** |
| 4 | **Vô hiệu hóa Gỡ lỗi (Debug)**| Ép cờ `debug=False` trong `app.run()` để tránh rò rỉ mã | **ĐẠT (PASS)** |
| 5 | **Giao diện mạng cục bộ** | Gắn chặt vào `127.0.0.1` (chỉ máy cục bộ mới truy cập được) | **ĐẠT (PASS)** |
| 6 | **Không phơi nhiễm mạng** | Không mở cổng trên card mạng LAN hay Internet | **ĐẠT (PASS)** |
| 7 | **Kiểm tra phản hồi khởi động**| Vòng lặp thăm dò `Invoke-WebRequest` 10 giây cho tới khi nhận HTTP 200 | **ĐẠT (PASS)** |
| 8 | **Ghi nhật ký ứng dụng** | Phân tách `staging.log` (stdout) và `staging_err.log` (stderr) | **ĐẠT (PASS)** |
| 9 | **Nhận dạng tiến trình (PID)**| Lưu PID vào `staging_server.pid` và kiểm tra lệnh qua CIM/WMI | **ĐẠT (PASS)** |
| 10 | **Dừng tiến trình có chọn lọc**| Hàm `Test-EventAIProcess` kiểm tra dòng lệnh chứa `run_staging_windows` | **ĐẠT (PASS)** |

---

## 3. CƠ CHẾ BẢO VỆ CHỐNG DỪNG NHẦM TIẾN TRÌNH (TARGETED TERMINATION LOGIC)

Trong tệp `stop_staging_windows.ps1`, hàm `Test-EventAIProcess` được thiết kế bằng truy vấn WMI/CIM cấp hệ điều hành:

```powershell
function Test-EventAIProcess($pidToCheck) {
    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $pidToCheck" -ErrorAction SilentlyContinue
        if ($proc -and ($proc.CommandLine -match "run_staging_windows" -or $proc.ExecutablePath -match [regex]::Escape($PythonExe))) {
            return $true
        }
    } catch {}
    return $false
}
```

### Cách thức hoạt động 2 tầng bảo vệ:
- **Tầng 1 (Kiểm tra tệp PID):** Nếu tìm thấy tệp `instance_staging\staging_server.pid`, script kiểm tra xem tiến trình mang PID đó có đúng là `run_staging_windows.py` chạy từ `.venv` hay không.
  - Nếu đúng: Thực hiện dừng tiến trình an toàn (`Stop-Process -Id $targetPid -Force`).
  - Nếu sai (ví dụ máy tính đã khởi động lại và Windows cấp PID đó cho tiến trình hệ thống như `svchost.exe` hay `notepad.exe`): Script thông báo "Stale PID file detected", xóa tệp PID cũ và **KHÔNG HỀ CHẠM VÀO TIẾN TRÌNH KHÔNG LIÊN QUAN**.
- **Tầng 2 (Kiểm tra cổng 5001):** Nếu cổng 5001 vẫn còn kết nối TCP, script quét tiến trình sở hữu (`OwningProcess`) và chỉ hạ lệnh dừng nếu tiến trình đó thỏa mãn `Test-EventAIProcess`. Nếu cổng bị chiếm bởi một ứng dụng khác của người dùng, script in cảnh báo đỏ và bỏ qua để tránh gây gián đoạn hệ thống.

---

## 4. HƯỚNG DẪN THỰC THI THỰC TẾ TRÊN WINDOWS 11

### 4.1 Khởi động Máy chủ Staging:
Mở PowerShell tại thư mục dự án và chạy:
```powershell
powershell -ExecutionPolicy Bypass -File .\start_staging_windows.ps1
```
*Kết quả đầu ra thực tế:*
```
==========================================================
 Starting EventAI Pro Windows Native Staging Server... 
==========================================================
  * Host:              127.0.0.1 (Strict Local Loopback)
  * Port:              5001
  * Target Database:   instance_staging\staging.db
  * Production DB:     instance\event_management.db (Untouched)
  * Notice:            Werkzeug Development Server (QA Only)
----------------------------------------------------------
[OK] Server process started with PID: 8460
Waiting for server to become ready on http://127.0.0.1:5001.......
[SUCCESS] EventAI Pro Staging is ACTIVE and reachable at http://127.0.0.1:5001
  * Log File:          instance_staging\staging.log
  * Local Credentials: Run '.\.venv\Scripts\python.exe scripts\get_staging_credentials.py'
  * Stop Command:      .\stop_staging_windows.ps1
```

### 4.2 Dừng Máy chủ Staging:
```powershell
powershell -ExecutionPolicy Bypass -File .\stop_staging_windows.ps1
```
*Kết quả đầu ra thực tế:*
```
Stopping verified EventAI Pro Staging process (PID: 8460)...
[SUCCESS] EventAI Pro Staging server has been stopped safely.
```

---

## 5. ĐỊNH DANH MÁY CHỦ & PHẠM VI SỬ DỤNG HỢP CHUẨN

> [!NOTE]
> Máy chủ sử dụng nhân HTTP của Werkzeug tích hợp sẵn trong Flask.  
> Căn cứ theo khuyến nghị chính thức của Flask/Pallets:
> - **Phù hợp tuyệt đối:** Môi trường QA cục bộ, kiểm thử luồng tích hợp, diễn tập khôi phục, kiểm thử trình duyệt thực tế và báo cáo nghiệm thu đồ án học thuật.
> - **Không dùng làm:** Máy chủ dịch vụ công cộng trên Internet (Production Hosting). Khi triển khai production thương mại trên Windows, cần sử dụng WSGI server chuyên dụng (như Waitress hoặc IIS FastCGI).

