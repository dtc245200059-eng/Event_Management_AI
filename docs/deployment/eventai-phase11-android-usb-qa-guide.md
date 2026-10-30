# EventAI Pro — Hướng Dẫn Kiểm Thử Camera Quét QR Trên Điện Thoại Android Qua Cáp USB (Android USB QA Guide)

> **Mã tài liệu:** `docs/deployment/eventai-phase11-android-usb-qa-guide.md`  
> **Giai đoạn:** Phase 11 — Windows Native Final QA & Security Hardening  
> **Phương thức kết nối:** Android Debug Bridge (ADB) Reverse Port Forwarding qua cáp USB  
> **Thiết bị mục tiêu:** Điện thoại Android vật lý + Trình duyệt Google Chrome  
> **Trạng thái kiểm thử:** SẴN SÀNG QUY TRÌNH (PROPOSED / AWAITING PHYSICAL DEVICE AUTHORIZATION)

---

## 1. TỔNG QUAN GIẢI PHÁP & NGUYÊN TẮC AN TOÀN

Phương pháp kiểm thử qua cáp USB (ADB Reverse) là giải pháp tối ưu nhất để kiểm thử camera thực tế trên thiết bị di động mà **hoàn toàn không cần máy ảo, không cần mạng Internet và không cần chứng chỉ SSL**:

```
[Điện thoại Android Vật lý]                      [Máy tính Windows 11 Host]
Trình duyệt Google Chrome                        EventAI Pro Staging Server
http://localhost:5001/checkin/ <== Cáp USB ==>   127.0.0.1:5001 (Flask App)
(Mở Camera Quét QR)            (adb reverse)     (instance_staging\staging.db)
```

### Tại sao phương pháp này hoạt động?
Theo tiêu chuẩn bảo mật W3C và Chromium:
- Trên điện thoại Android, địa chỉ `http://localhost` được trình duyệt Chrome tự động xếp loại là **Nguồn An Toàn Bản Địa (Potentially Trustworthy Origin / Secure Context)**.
- Khi đó, biến `window.isSecureContext === true`, cho phép hàm `navigator.mediaDevices.getUserMedia()` kích hoạt trực tiếp camera phần cứng của điện thoại để quét mã QR mà không bị trình duyệt chặn!

### Báo cáo Hiện Trạng Tiền Kiểm (Pre-flight Status):
- **Công cụ ADB trên máy host:** Đã kiểm tra và xác nhận **chưa được cài đặt trong PATH** của hệ điều hành Windows 11 hiện tại.
- **Tuân thủ quy tắc an toàn:**
  * Antigravity **KHÔNG TỰ Ý CÀI ĐẶT ADB** khi chưa có sự phê duyệt rõ ràng từ người dùng.
  * Antigravity **KHÔNG TỰ BẬT USB DEBUGGING** trên bất kỳ thiết bị nào.
  * Antigravity **KHÔNG TỰ TẠO ĐƯỜNG HẦM CỔNG** khi chưa kết nối thiết bị thực tế.

---

## 2. QUY TRÌNH 12 BƯỚC KIỂM THỬ THỰC TẾ CHI TIẾT (STEP-BY-STEP RUNBOOK)

Khi người dùng quyết định thực hiện kiểm thử trên điện thoại Android thực tế, vui lòng thực hiện theo quy trình chuẩn sau:

### Bước 1: Chuẩn bị công cụ ADB trên Windows 11
1. Tải bộ công cụ chính thức từ Google: `Android SDK Platform-Tools for Windows` (khoảng 12MB, dạng tệp `.zip` giải nén trực tiếp, không cần cài đặt).
2. Giải nén vào thư mục, ví dụ: `C:\platform-tools\`.

### Bước 2: Bật Gỡ lỗi USB (USB Debugging) trên điện thoại Android
1. Trên điện thoại Android, vào **Cài đặt** -> **Thông tin điện thoại** (About Phone).
2. Chạm liên tục 7 lần vào mục **Số bản dựng** (Build Number) cho đến khi xuất hiện thông báo *"Bạn đã là nhà phát triển"*.
3. Quay lại **Cài đặt** -> **Hệ thống** -> **Tùy chọn nhà phát triển** (Developer Options).
4. Bật công tắc **Gỡ lỗi USB** (USB Debugging).

### Bước 3: Kết nối và Ủy quyền thiết bị (ADB Authorization)
1. Cắm cáp USB nối điện thoại với cổng USB của máy tính Windows 11.
2. Mở PowerShell trên Windows và chạy lệnh:
   ```powershell
   C:\platform-tools\adb.exe devices
   ```
3. Màn hình điện thoại sẽ hiện hộp thoại: *"Cho phép gỡ lỗi USB từ máy tính này?"*. Tích chọn *"Luôn cho phép"* và bấm **OK**.
4. Chạy lại lệnh trên; thiết bị sẽ hiển thị trạng thái `device` (hợp lệ).

### Bước 4: Thiết lập chuyển tiếp cổng ngược (Localhost Port Forwarding)
Khởi động máy chủ Staging trên Windows bằng `.\start_staging_windows.ps1`, sau đó chạy:
```powershell
C:\platform-tools\adb.exe reverse tcp:5001 tcp:5001
```
*Lệnh này gắn cổng 5001 trên điện thoại trực tiếp vào cổng 5001 của máy tính Windows.*

### Bước 5: Xác thực Môi trường An toàn (Secure Context Verification)
1. Mở ứng dụng **Google Chrome** trên điện thoại Android.
2. Nhập thanh địa chỉ: `http://localhost:5001/`
3. Mở Console (hoặc kiểm tra tính năng): Xác nhận trang chủ EventAI Pro tải mượt mà.

### Bước 6: Đăng nhập Nhân viên Soát vé (Staff Authentication)
1. Truy cập `http://localhost:5001/auth/login`.
2. Lấy thông tin đăng nhập từ lệnh:
   ```powershell
   .\.venv\Scripts\python.exe scripts\get_staging_credentials.py
   ```
3. Nhập `staff_staging` và mật khẩu bí mật tương ứng, bấm **Đăng nhập**.

### Bước 7: Mở Giao diện Check-in & Cấp quyền Camera (Camera Permission)
1. Truy cập `http://localhost:5001/checkin/`.
2. Trình duyệt Chrome trên điện thoại sẽ hiển thị thông báo: *"localhost muốn sử dụng máy ảnh của bạn"*.
3. Bấm **Cho phép (Allow)**.

### Bước 8: Chọn Camera Sau (Rear Camera Selection)
1. Giao diện quét QR của EventAI Pro tự động ưu tiên camera sau (`facingMode: "environment"`).
2. Đảm bảo khung hình camera hiển thị hình ảnh thời gian thực, có khả năng lấy nét quang học.

### Bước 9: Quét Check-in Vé Hợp Lệ (Valid Ticket Check-in)
1. Mở vé điện tử mẫu trên màn hình máy tính (mã vé `TCK-001-0001-STG` hoặc tệp SVG trong `app/static/qr_codes/`).
2. Hướng camera điện thoại vào mã QR.
3. **Kết quả mong đợi:**
   - Ứng dụng phát âm thanh beep/rung phản hồi.
   - Hiển thị hộp thoại thông báo màu xanh: `✅ CHECK-IN THÀNH CÔNG CHO KHÁCH HÀNG: Khách Mời Staging`.
   - Trạng thái vé chuyển sang "Đã check-in" và số lượng khách cập nhật tức thì.

### Bước 10: Kiểm thử Chống Gian lận Vé Trùng lặp (Duplicate Rejection)
1. Hướng camera quét lại chính mã QR vừa check-in ở Bước 9.
2. **Kết quả mong đợi:**
   - Hệ thống phản hồi mã cảnh báo màu đỏ/cam: `⛔ CẢNH BÁO: VÉ NÀY ĐÃ ĐƯỢC CHECK-IN LÚC...`.
   - Backend trả về HTTP `409 Conflict`, ngăn chặn triệt để hành vi quay vòng vé.

### Bước 11: Kiểm thử Quét Mã QR Không Hợp Lệ (Invalid QR Rejection)
1. Quét thử một mã QR bất kỳ (như mã Wi-Fi hoặc URL ngẫu nhiên).
2. **Kết quả mong đợi:**
   - Hệ thống hiển thị thông báo lỗi: `❌ MÃ VÉ HOẶC MÃ ĐĂNG KÝ KHÔNG HỢP LỆ`.
   - Không làm crash ứng dụng hay treo camera.

### Bước 12: Dọn dẹp Cổng Chuyển Tiếp (Cleanup)
Sau khi kết thúc phiên kiểm thử:
```powershell
C:\platform-tools\adb.exe reverse --remove tcp:5001
```
*Ngắt kết nối cáp USB và rút thiết bị an toàn.*

---

## 3. LƯU Ý ĐẶC THÙ ĐỐI VỚI THIẾT BỊ APPLE IOS (IPHONE / IPAD)

- Hệ điều hành Apple iOS **không hỗ trợ giao thức ADB reverse qua cáp USB**.
- Để kiểm thử camera trên iPhone Safari mà không dùng máy ảo, người dùng cần sử dụng **Phương án 2 (Đường hầm Cloudflare Tunnel tạm thời)** hoặc **Phương án 3 (Cài đặt Root CA nội bộ mkcert)** theo hướng dẫn tại tài liệu [docs/deployment/eventai-windows-mobile-https-options.md](file:///D:/Event_Management_AI/docs/deployment/eventai-windows-mobile-https-options.md).
- Antigravity sẽ **KHÔNG TỰ ĐỘNG MỞ ĐƯỜNG HẦM CÔNG CỘNG** trừ khi người dùng cấp phép bằng văn bản rõ ràng.

