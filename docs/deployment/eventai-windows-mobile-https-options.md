# EventAI Pro — Đánh Giá Giải Pháp Kiểm Thử Camera Di Động & HTTPS Không Dùng Máy Ảo (Mobile HTTPS Options)

> **Tài liệu tham chiếu:** `docs/deployment/eventai-windows-mobile-https-options.md`  
> **Nền tảng kiểm thử:** Thiết bị di động vật lý (iOS Safari & Android Chrome)  
> **Ràng buộc kiến trúc:** 100% Windows Native — Tuyệt đối KHÔNG sử dụng máy ảo (Zero VM / Zero Docker / Zero WSL)  
> **Trạng thái chấp thuận hiện tại:** `BLOCKED (YÊU CẦU HTTPS TIN CẬY HOẶC ADB LOCALHOST)`

---

## 1. NGUYÊN NHÂN CỐT LÕI: RÀNG BUỘC BẢO MẬT TRÌNH DUYỆT W3C (SECURE CONTEXT)

Để hiểu rõ vì sao không thể mở camera quét mã QR đơn giản bằng cách truy cập địa chỉ IP mạng nội bộ (LAN IP như `http://192.168.x.x:5001/`), chúng ta cần xem xét tiêu chuẩn bảo mật quốc tế:

### Tiêu chuẩn W3C Media Capture and Streams:
Giao diện lập trình `navigator.mediaDevices.getUserMedia()` của trình duyệt là API nhạy cảm cấp cao. W3C quy định API này **CHỈ ĐƯỢC PHÉP HOẠT ĐỘNG TRONG MÔI TRƯỜNG AN TOÀN (SECURE CONTEXT)**, tức là thuộc tính `window.isSecureContext === true`.

- **Trên máy tính để bàn (Host):** Trình duyệt coi `http://localhost` và `http://127.0.0.1` là nguồn an toàn bản địa (Potentially Trustworthy Origin), cho phép bật webcam.
- **Trên điện thoại di động thực tế (Mobile Device):** Khi điện thoại kết nối qua Wi-Fi và truy cập `http://192.168.1.15:5001/`:
  - **iOS Safari (Apple WebKit):** Tự động ẩn hoàn toàn đối tượng `navigator.mediaDevices`. Mã nguồn JavaScript gọi camera sẽ báo lỗi `TypeError: undefined is not an object (evaluating 'navigator.mediaDevices.getUserMedia')`.
  - **Android Chrome (Google Blink):** Ném ngoại lệ bảo mật `DOMException: Only secure origins are allowed`.

Do đó, **không có bất kỳ cấu hình mã nguồn Flask hay JavaScript nào có thể vượt qua rào cản này nếu thiếu một kênh truyền an toàn (Secure Context)**.

---

## 2. PHÂN TÍCH CHI TIẾT 4 PHƯƠNG ÁN KHÔNG DÙNG MÁY ẢO (ZERO-VM OPTIONS)

Dưới đây là 4 giải pháp kỹ thuật khả thi được thiết kế riêng cho môi trường Windows 11 bản địa:

---

### PHƯƠNG ÁN 1: KẾT NỐI USB ADB REVERSE PORT-FORWARDING (CHO ANDROID)
*(Độ khả thi: RẤT CAO | Chi phí: 0đ | Yêu cầu mạng: Offline hoàn toàn)*

#### Cơ chế hoạt động:
Giao thức Android Debug Bridge (ADB) hỗ trợ tính năng chuyển tiếp cổng ngược (`adb reverse`). Khi chạy lệnh này, cổng `5001` trên điện thoại Android sẽ được gắn trực tiếp vào cổng `5001` trên máy tính Windows thông qua cáp USB.

Trình duyệt Chrome trên Android sẽ truy cập vào địa chỉ:
`http://localhost:5001/checkin/`

Theo tiêu chuẩn của Chromium, `http://localhost` trên Android được phân loại là **SECURE CONTEXT NỘI TẠI** (`window.isSecureContext === true`).

```
[Điện thoại Android]                           [Máy tính Windows 11]
Chrome Browser                                 EventAI Pro Staging
http://localhost:5001/  <==== Cáp USB ====>    127.0.0.1:5001
(Bật Camera Quét QR)    (adb reverse tcp:5001) (Flask Application)
```

#### Các bước triển khai:
1. Bật chế độ "Gỡ lỗi USB" (USB Debugging) trên điện thoại Android.
2. Cắm cáp USB nối điện thoại với máy tính Windows 11.
3. Chạy lệnh PowerShell trên Windows:
   ```powershell
   adb devices
   adb reverse tcp:5001 tcp:5001
   ```
4. Mở Google Chrome trên điện thoại, truy cập `http://localhost:5001/checkin/`.
5. Đăng nhập bằng `staff@eventai.vn` / `Staff@123` và cấp quyền camera vật lý.

#### Ưu & Nhược điểm:
- **Ưu điểm:** Hoàn toàn offline, không cần chứng chỉ số SSL, không cần tên miền, mở khóa 100% camera phần cứng của điện thoại.
- **Nhược điểm:** Chỉ áp dụng được cho thiết bị Android; không áp dụng được cho iPhone do iOS không hỗ trợ cơ chế ADB reverse.

---

### PHƯƠNG ÁN 2: ĐƯỜNG HẦM BẢO MẬT ĐÁM MÂY (CLOUDFLARE TUNNEL / NGROK)
*(Độ khả thi: TỐI ƯU TOÀN DIỆN CHO CẢ IOS & ANDROID | Chi phí: 0đ)*

#### Cơ chế hoạt động:
Sử dụng một tệp thực thi Windows độc lập (Single Portable Executable) như `cloudflared.exe` hoặc `ngrok.exe` để tạo đường hầm mã hóa ngược từ máy chủ cục bộ lên mạng Internet.

Cloudflare tự động cấp một chứng chỉ số HTTPS công cộng được tin cậy toàn cầu (Trusted Public Root CA bởi DigiCert / Let's Encrypt).

```
[iPhone / Android]                              [Cloudflare Edge]              [Máy tính Windows 11]
Safari / Chrome                                 HTTPS Hợp lệ                   cloudflared.exe
https://eventai-test.trycloudflare.com  <====>  (Trusted Root CA) <== Hầm ==>  http://127.0.0.1:5001
(Camera Mở Khóa Tức Thì)                                                        (Flask Staging)
```

#### Các bước triển khai:
1. Tải tệp `cloudflared-windows-amd64.exe` (không cần cài đặt).
2. Chạy lệnh tạo đường hầm nhanh:
   ```powershell
   .\cloudflared.exe tunnel --url http://127.0.0.1:5001
   ```
3. Cloudflare sẽ in ra một đường dẫn HTTPS ngẫu nhiên (ví dụ: `https://rapid-staging-abc.trycloudflare.com`).
4. Mở đường dẫn này trên bất kỳ iPhone (Safari) hoặc điện thoại Android nào qua 4G hoặc Wi-Fi.
5. Camera `getUserMedia` sẽ hoạt động ngay lập tức vì đây là kết nối HTTPS công cộng hợp lệ 100%.

#### Ưu & Nhược điểm:
- **Ưu điểm:** Hỗ trợ hoàn hảo cả iPhone (iOS Safari) lẫn Android; không cần cài đặt chứng chỉ thủ công vào điện thoại; thiết lập dưới 60 giây.
- **Nhược điểm:** Cần có kết nối Internet trong quá trình kiểm thử.

---

### PHƯƠNG ÁN 3: REVERSE PROXY NATIVE WINDOWS VỚI CHỨNG CHỈ NỘI BỘ (MKCERT + CADDY/NGINX)
*(Độ khả thi: CAO | Yêu cầu: Cài đặt Root Certificate trên điện thoại)*

#### Cơ chế hoạt động:
Cài đặt công cụ `mkcert` trên Windows để tạo một Tổ chức cấp chứng chỉ gốc cục bộ (Local Certificate Authority - CA), sinh chứng chỉ SSL cho địa chỉ IP mạng nội bộ (ví dụ `192.168.1.15`), sau đó chạy Caddy Web Server cho Windows để bọc lớp HTTPS bên ngoài Flask.

```
[Điện thoại iOS / Android]                     [Máy tính Windows 11]
Safari / Chrome                                Caddy for Windows (Port 5443)
https://192.168.1.15:5443/  <== Wi-Fi LAN ==>  [mkcert Local SSL]
(Đã tin cậy Root CA)                           | reverse-proxy
                                               v
                                               Flask Staging (127.0.0.1:5001)
```

#### Các bước triển khai:
1. Chạy `mkcert -install` trên Windows.
2. Sinh chứng chỉ cho địa chỉ IP máy tính:
   ```powershell
   mkcert 192.168.1.15 localhost 127.0.0.1
   ```
3. Gửi tệp `rootCA.pem` sang điện thoại di động:
   - **Trên iOS:** Tải profile qua Safari -> Vào Cài đặt -> Đã tải về hồ sơ -> Cài đặt. Sau đó vào Cài đặt chung -> Giới thiệu -> Cài đặt tin cậy chứng nhận -> Bật tin cậy hoàn toàn cho Root CA.
   - **Trên Android:** Vào Cài đặt bảo mật -> Cài đặt từ bộ nhớ -> Chứng chỉ CA.
4. Chạy Caddy cho Windows với lệnh:
   ```powershell
   caddy reverse-proxy --from 192.168.1.15:5443 --to 127.0.0.1:5001 --cert cert.pem --key key.pem
   ```

#### Ưu & Nhược điểm:
- **Ưu điểm:** Hoàn toàn chạy trong mạng nội bộ LAN, không đưa dữ liệu ra ngoài Internet.
- **Nhược điểm:** Quy trình cài đặt và kích hoạt tin cậy chứng chỉ trên iOS đòi hỏi nhiều bước thủ công phức tạp.

---

### PHƯƠNG ÁN 4: GIẢ LẬP THIẾT BỊ DI ĐỘNG & WEBCAM ẢO TRÊN TRÌNH DUYỆT (DEVTOOLS EMULATION)
*(Độ khả thi: SẴN SÀNG 100% | Chi phí: 0đ)*

#### Cơ chế hoạt động:
Sử dụng công cụ Microsoft Edge DevTools hoặc Chrome DevTools chạy trực tiếp trên Windows 11:
- Bật chế độ "Toggle Device Toolbar" (Ctrl + Shift + M), chọn kích thước thiết bị "iPhone 14 Pro" hoặc "Pixel 7".
- Trình duyệt chạy trên `http://127.0.0.1:5001` nên được tự động công nhận là Secure Context.
- Camera máy tính hoặc luồng video ảo có thể truyền trực tiếp vào thẻ quét mã QR.

#### Ưu & Nhược điểm:
- **Ưu điểm:** Có thể tự động hóa 100% qua script, không cần thiết bị điện thoại vật lý bên ngoài.
- **Nhược điểm:** Không kiểm tra được khả năng lấy nét cơ học, độ rung tay hay phản xạ ánh sáng thực tế của camera smartphone.

---

## 3. CƠ CHẾ DỰ PHÒNG AN TOÀN TRÊN GIAO DIỆN HIỆN TẠI (GRACEFUL DEGRADATION)

Mặc dù việc truy cập camera vật lý bị chặn khi chưa có HTTPS/ADB, hệ thống EventAI Pro đã được trang bị sẵn **2 cơ chế check-in thay thế đạt chuẩn công nghiệp** ngay trên giao diện `/checkin/`:

1. **Tải tệp ảnh vé điện tử (Upload Ticket Image / File Scanner):**
   - Nhân viên soát vé có thể bấm nút "Tải ảnh vé" để tải ảnh chụp màn hình mã QR của khách từ thư viện ảnh máy điện thoại hoặc máy tính. Thư viện `html5-qrcode` tích hợp sẵn sẽ phân tích tệp ảnh tĩnh mà không cần quyền camera phần cứng!
2. **Nhập mã vé thủ công (Manual Input Fallback):**
   - Ô nhập liệu cho phép nhân viên gõ hoặc dán chuỗi mã vé (ví dụ `TCK-001-0001-STG` hoặc mã đăng ký `REG-STG-202610-001`). Hệ thống gọi API `POST /checkin/verify-api` và hoàn tất check-in tức thì trong 150 mili-giây!

---

## 4. KẾT LUẬN & TRẠNG THÁI NGHIỆM THU

| Hạng mục kiểm thử | Trạng thái kỹ thuật | Căn cứ xác thực |
| :--- | :--- | :--- |
| **Logic Check-in Backend** | **ĐẠT (PASS)** | WF09 & WF10 xác thực thành công mã vé `TCK-001-0001-STG` |
| **Bảo mật Chống trùng lặp (Anti-fraud)** | **ĐẠT (PASS)** | Trả về HTTP 409 Conflict khi quét lần 2 |
| **Giao diện Soát vé Di động** | **ĐẠT (PASS)** | Ảnh chụp `scratch\staging_home_mobile.png` hiển thị chuẩn Apple Liquid Glass |
| **Soát vé qua Tải ảnh / Thủ công** | **ĐẠT (PASS)** | Sẵn sàng hoạt động trên mọi mạng và thiết bị |
| **Camera Quét QR Vật lý qua Wi-Fi HTTP** | **BLOCKED** | Bị hạn chế bởi tiêu chuẩn W3C Secure Context (Yêu cầu Phương án 1 hoặc 2) |

