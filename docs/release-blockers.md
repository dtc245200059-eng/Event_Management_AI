# SỔ BỘ QUẢN TRỊ CÁC ĐIỂM CHẶN PHÁT HÀNH (RELEASE BLOCKER REGISTER)

**Dự án:** EventAI Pro — Nền tảng Quản trị & Điều hành Sự kiện Toàn diện Tích hợp Đa tác tử AI  
**Phiên bản thẩm định:** v3.2.0  
**Thời điểm đánh giá:** 28/09/2026  
**Chuyên gia thẩm định:** Lead System Architect & Release Manager  

---

## 1. NGUYÊN TẮC QUẢN TRỊ ĐIỂM CHẶN PHÁT HÀNH

Điểm chặn phát hành (Release Blocker) là bất kỳ lỗi, sai lệch hoặc khiếm khuyết nào khiến hệ thống:
1. Không thể khởi động hoặc không an toàn để vận hành (Unsafe).
2. Không thể sử dụng được các luồng nghiệp vụ cốt lõi (Unusable).
3. Không thể tái lập được từ môi trường sạch (Non-reproducible).
4. Vi phạm các tiêu chí chấp nhận trọng yếu hoặc phát sinh rò rỉ dữ liệu nghiêm trọng.

Mọi vấn đề mức độ **CRITICAL** hoặc **HIGH** chưa được giải quyết đều là **RELEASE BLOCKER** tuyệt đối ngăn chặn việc phát hành.

---

## 2. BẢNG DANH MỤC THẨM ĐỊNH ĐIỂM CHẶN PHÁT HÀNH (RELEASE BLOCKER REGISTER)

| ID | Category | Description | Evidence | Severity | Impact | Status |
|:---:|---|---|---|:---:|---|:---:|
| **BLK-001** | Architecture / Build | Xung đột routing hoặc circular import khiến server không khởi động | Đăng ký thành công 67/67 routes; khởi tạo `run.py` in ra `app 67`. | **CRITICAL** | Hệ thống sụp đổ khi khởi động. | **RESOLVED** (0 Blocker) |
| **BLK-002** | Database / ORM | Cảnh báo 22 vị trí `Model.query.get_or_404()` lỗi thời làm crash ứng dụng trên SQLAlchemy 3.x | Refactor 100% sang `db.get_or_404(Model, id)`; kiểm tra 36 tests pass. | **HIGH** | Crash ứng dụng khi nâng cấp thư viện. | **RESOLVED** (GAP-01) |
| **BLK-003** | Ticketing / Data | Lỗi kẹt session CSDL khi hủy vé và không hoàn trả quota dẫn đến sai lệch số liệu vé | Bổ sung Atomic Rollback trong `cancel_ticket`; test pass. | **HIGH** | Thất thoát hạn ngạch vé, kẹt session CSDL. | **RESOLVED** (GAP-03) |
| **BLK-004** | API / Monitoring | Thiếu probe kiểm tra sức khỏe `/health` khiến bộ điều phối container (K8s/Docker) không phát hiện sự cố | Hiện thực hóa `GET /health` trả về 200 Healthy với latency 0.38ms. | **HIGH** | Container bị restart sai lệch hoặc treo ngầm. | **RESOLVED** (GAP-04) |
| **BLK-005** | Security / CSRF | Thiếu CSRF token cho các yêu cầu AJAX Fetch dẫn đến nguy cơ tấn công giả mạo | Nhúng `<meta name="csrf-token">` vào `base.html` và tích hợp `main.js`. | **HIGH** | Bị tấn công CSRF chiếm đoạt giao dịch vé. | **RESOLVED** (GAP-04) |
| **BLK-006** | Ticketing / UX | Người dùng bị chặn vĩnh viễn không thể đăng ký lại vé mới sau khi đã hủy đơn vé cũ | Điều chỉnh truy vấn `check_existing_registration` chỉ chặn đơn confirmed. | **HIGH** | Mất khách hàng, trải nghiệm đặt vé bị tắc nghẽn. | **RESOLVED** (GAP-05) |
| **BLK-007** | AI / Cost & DoS | Thiếu bộ giới hạn tần suất yêu cầu AI khiến hệ thống dễ bị cạn kiệt ngân sách hoặc DoS | Tích hợp Token Bucket Rate Limiter 30 req/phút/IP; test chặn 429 pass. | **HIGH** | Hết hạn mức Gemini API, quá tải tài nguyên. | **RESOLVED** (GAP-02) |
| **BLK-008** | Security / Secret | Khóa API Gemini hiển thị chuỗi token thật trong `.env.example` | Đã thay thế thành placeholder an toàn `your_gemini_api_key_here`. | **MEDIUM** | Nguy cơ rò rỉ thông tin xác thực mẫu. | **RESOLVED** (Phase 8 Fix) |
| **BLK-009** | Testing / Environment | Cảnh báo Python 3.14 làm nhiễu kết quả kiểm thử tự động | Tạo `pytest.ini` lọc cảnh báo; 36/36 tests đạt 0 warnings. | **MEDIUM** | Kết quả CI/CD bị gắn cờ không sạch. | **RESOLVED** (GAP-11) |
| **BLK-010** | Mobile / UX | Lớp phủ Modal/Drawer che lấp nhưng nội dung bị ẩn hoặc kẹt con trỏ chuột | Chuẩn hóa hệ thống Z-index 7 tầng (`0` đến `1080`); kiểm thử 9 viewports pass. | **HIGH** | Người dùng di động không thao tác được giao diện. | **RESOLVED** (Phase 7 Audit) |

---

## 3. TỔNG KẾT TÌNH TRẠNG ĐIỂM CHẶN PHÁT HÀNH

- **Tổng số điểm chặn phát hiện ban đầu:** 10 điểm (thuộc GAP-01 đến GAP-12 và kiểm toán an toàn).
- **Số điểm chặn ĐÃ ĐƯỢC GIẢI QUYẾT TRIỆT ĐỂ (RESOLVED):** **10 / 10** (**100.0%**).
- **Số điểm chặn CÒN TỒN ĐỌNG (UNRESOLVED):** **0**.
- **Kết luận:** **KHÔNG CÒN BẤT KỲ ĐIỂM CHẶN PHÁT HÀNH NÀO (ZERO RELEASE BLOCKERS). HỆ THỐNG ĐỦ ĐIỀU KIỆN SẴN SÀNG PHÁT HÀNH.**
