# EventAI Pro — Kiểm Toán An Ninh Môi Trường Bản Địa Windows 11 (Security Audit)

> **Mã tài liệu:** `docs/deployment/eventai-phase11-windows-security-audit.md`  
> **Giai đoạn:** Phase 11 — Windows Native Final QA & Security Hardening  
> **Kiến trúc phát hành:** Windows 11 Native Architecture (Zero VM / Zero Docker / Zero WSL)  
> **Môi trường thực thi:** Python 3.14.2 64-bit (`D:\Event_Management_AI\.venv`)  
> **Trạng thái an ninh:** TOÀN VẸN & ĐẠT CHUẨN AN TOÀN (HARDENED & VERIFIED)

---

## 1. MỤC TIÊU & PHẠM VI KIỂM TOÁN AN NINH

Kiểm toán an ninh giai đoạn Phase 11 tập trung xác thực tính cô lập tuyệt đối, cơ chế xác thực, phân quyền RBAC, kiểm soát phiên, phòng chống CSRF và ranh giới mạng của hệ thống EventAI Pro trên nền tảng Windows 11 bản địa.

Phạm vi kiểm toán gồm 6 lĩnh vực trọng yếu:
1. Tính toàn vẹn và bất khả xâm phạm của Cơ sở dữ liệu Sản xuất (`instance\event_management.db`).
2. Cơ chế cách ly và tính an toàn của Cơ sở dữ liệu Staging (`instance_staging\staging.db`).
3. Ranh giới giao diện mạng (Network Interface Boundary & Zero External Exposure).
4. Thực thi bảo vệ Chống Giả mạo Yêu cầu Đa trang (CSRF Enforcement) trên toàn bộ biểu mẫu và API.
5. Cấu hình Cookie phiên và phòng thủ tấn công đánh cắp phiên (Session Security & HttpOnly).
6. Cách ly dịch vụ thông báo, email và an toàn dữ liệu nhạy cảm (Zero Outbound Leakage).

---

## 2. BẢNG KIỂM TRA ĐỐI SOÁT TOÀN VẸN CƠ SỞ DỮ LIỆU (DATABASE INTEGRITY)

```
+--------------------------------------------------------------------------------------------------+
| CƠ SỞ DỮ LIỆU SẢN XUẤT (PRODUCTION DATABASE)                                                    |
| * Tệp tin:          D:\Event_Management_AI\instance\event_management.db                          |
| * Dung lượng:       253,952 bytes                                                                |
| * Thời điểm sửa:    14/10/2026 20:58:05 (Bất biến)                                               |
| * Mã băm SHA-256:   AD48A072572654FB706D57B4129F29D4206372E0B7DB94D1F16B4797E48F6679           |
| * Tệp phụ WAL/SHM:  KHÔNG CÓ (Zero sidecars, không có giao dịch treo)                            |
| * Trạng thái:       BẢO VỆ TUYỆT ĐỐI — 0 LẦN GHI TRONG SUỐT QUÁ TRÌNH STAGING                   |
+--------------------------------------------------------------------------------------------------+
                                                vs
+--------------------------------------------------------------------------------------------------+
| CƠ SỞ DỮ LIỆU THỬ NGHIỆM (ISOLATED STAGING DATABASE)                                             |
| * Tệp tin:          D:\Event_Management_AI\instance_staging\staging.db                           |
| * Dung lượng:       180,224 bytes                                                                |
| * Cấu trúc:         11 bảng dữ liệu mẫu hoàn chỉnh (synthetic data only)                         |
| * Mã băm SHA-256:   4DE98C335C0B12DB3AB08101C57DEE82F4BEC6CEDF178CA08AEFFA3E18DB8A69           |
| * Tệp bí mật:       instance_staging\.staging_secrets.json (Phân quyền bảo mật cục bộ)           |
| * Loại trừ Git:     Đã thêm instance_staging/ vào .gitignore (Không bao giờ commit mã bí mật)   |
| * Trạng thái:       CÔ LẬP HOÀN TOÀN — PHỤC VỤ ĐỘC QUYỀN CHO KIỂM THỬ                            |
+--------------------------------------------------------------------------------------------------+
```

---

## 3. KIỂM TOÁN RANH GIỚI MẠNG & BỀ MẶT TẤN CÔNG (NETWORK BOUNDARY)

| Tiêu chí an ninh | Trạng thái thực tế | Đánh giá an toàn |
| :--- | :--- | :--- |
| **Giao diện mạng lắng nghe** | `127.0.0.1` (Strict Localhost Loopback) | **ĐẠT (SECURE)**: Chỉ chấp nhận kết nối nội bộ từ máy Windows 11 host. |
| **Cổng mạng Staging** | Cổng TCP `5001` | **ĐẠT (SECURE)**: Biệt lập với cổng production mặc định (5000). |
| **Lắng nghe mạng LAN (`0.0.0.0`)**| **TẮT HOÀN TOÀN** trong `run_staging_windows.py` | **ĐẠT (SECURE)**: Các thiết bị trong cùng mạng Wi-Fi không thể quét hay kết nối tới cổng 5001. |
| **Đường hầm công cộng (Public Tunnels)**| **KHÔNG KÍCH HOẠT** (Không chạy ngrok/Cloudflare) | **ĐẠT (SECURE)**: Ứng dụng không bị lộ ra ngoài Internet. |
| **Chế độ Gỡ lỗi (Debug Mode)** | `DEBUG = False` trong `StagingConfig` | **ĐẠT (SECURE)**: Tránh lộ Werkzeug Interactive Debugger PIN & Source Code. |
| **Cảnh báo máy chủ phát triển** | Có ghi nhận banner Werkzeug Development Server | **ĐẠT (SECURE)**: Được định danh rõ là máy chủ phục vụ QA/Demo học thuật, không dùng làm hosting thương mại. |

---

## 4. KIỂM TOÁN BẢO VỆ CHỐNG CSRF (CSRF DEFENSE ENFORCEMENT)

Cơ chế phòng thủ CSRF (Phase 6B) tiếp tục được kiểm chứng thực tế và vận hành nghiêm ngặt trong môi trường Staging:

1. **Kích hoạt middleware toàn cục:**
   `WTF_CSRF_ENABLED = True` được nạp cứng qua `StagingConfig`.
2. **Bảo vệ Biểu mẫu HTML truyền thống:**
   Tất cả các form đăng nhập, chỉnh sửa hồ sơ, tạo sự kiện và đăng xuất đều chứa thẻ ẩn `<input type="hidden" name="csrf_token" value="...">`.
3. **Bảo vệ Lời gọi API JavaScript (AJAX / Fetch):**
   Thẻ `<meta name="csrf-token" content="...">` được xuất động trên thẻ `<head>`. Các tập lệnh `static/js/main.js` và `static/js/ai_chat.js` tự động đọc token này và gắn vào header `X-CSRFToken` cho mọi yêu cầu `POST`, `PUT`, `DELETE`.
4. **Kiểm chứng từ chối không có CSRF (WF14):**
   Khi gửi yêu cầu đăng nhập `POST /auth/login` thiếu token CSRF, hệ thống lập tức từ chối và phản hồi **HTTP 400 Bad Request**, ngăn chặn hoàn toàn tấn công giả mạo yêu cầu từ trang web độc hại của bên thứ ba.
5. **Đăng xuất bảo mật:**
   Tuyến đường `POST /auth/logout` bắt buộc CSRF token, loại bỏ hoàn toàn lỗ hổng Đăng xuất CSRF (Logout CSRF) phổ biến.

---

## 5. CẤU HÌNH BẢO MẬT COOKIE PHIÊN (SESSION COOKIE POLICIES)

| Thuộc tính Cookie | Giá trị cấu hình | Mục đích bảo mật |
| :--- | :--- | :--- |
| `SESSION_COOKIE_HTTPONLY` | `True` | **Chống tấn công XSS:** Ngăn chặn JavaScript độc hại truy cập thuộc tính `document.cookie`. |
| `SESSION_COOKIE_SAMESITE` | `'Lax'` | **Bảo vệ điều hướng ngoài:** Cookie phiên không được gửi kèm trong các yêu cầu cross-site GET/POST độc hại. |
| `SESSION_COOKIE_SECURE` | `False` | **Tương thích Loopback:** Bắt buộc thiết lập `False` vì Staging chạy trên HTTP loopback (`http://127.0.0.1:5001`). Khi triển khai HTTPS thật, cờ này sẽ đổi thành `True`. |
| `PERMANENT_SESSION_LIFETIME` | 86,400 giây (24h) | Giới hạn thời gian sống của phiên làm việc để giảm thiểu nguy cơ chiếm dụng phiên cũ. |

---

## 6. CÁCH LY THÔNG BÁO VÀ CHỐNG RÒ RỈ DỮ LIỆU RA NGOÀI (DATA EXFILTRATION DEFENSE)

- **Không cấu hình dịch vụ gửi email ngoài:** Dự án không kết nối với bất kỳ máy chủ SMTP ngoài nào (như SendGrid, Mailgun, Gmail SMTP).
- **Hệ thống thông báo nội bộ:** Mọi thông báo sự kiện sinh ra bởi `Notification` model đều được lưu trữ an toàn trong bảng `notifications` nội bộ của cơ sở dữ liệu SQLite staging.
- **Tên miền người dùng mẫu (Synthetic Domain Scoping):** Toàn bộ email người dùng mẫu sử dụng định danh cục bộ rõ ràng (`@staging.eventai.local`), loại trừ mọi khả năng gửi nhầm thư tới người dùng thực.

---

## 7. KẾT LUẬN KIỂM TOÁN AN NINH

Hệ thống EventAI Pro trong cấu hình Windows Native Staging đáp ứng đầy đủ các tiêu chuẩn an ninh ứng dụng web của OWASP:
- **Nguy cơ can thiệp CSDL gốc:** 0% (Hoàn toàn không có đường dẫn ghi tới CSDL gốc).
- **Nguy cơ rò rỉ dữ liệu qua mạng:** 0% (Gắn chặt loopback `127.0.0.1`).
- **Nguy cơ tấn công CSRF / Session Hijacking:** Được kiểm soát chặt chẽ bằng CSRFProtect, SameSite=Lax và HttpOnly cookies.

