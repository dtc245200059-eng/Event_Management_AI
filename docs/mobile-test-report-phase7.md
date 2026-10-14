# BÁO CÁO KIỂM THỬ ĐÁP ỨNG THIẾT BỊ DI ĐỘNG GIAI ĐOẠN 7 (PHASE 7 MOBILE & RESPONSIVE TEST REPORT)

**Dự án:** EventAI Pro — Nền tảng Quản trị & Điều hành Sự kiện Toàn diện Tích hợp Đa tác tử AI  
**Hệ thống thiết kế:** Apple Human Interface Guidelines Design Tokens & Glassmorphism  
**Ngày kiểm thử:** 28/09/2026  
**Công cụ kiểm thử:** DOM Inspection, CSS Viewport Emulation, CSS Z-index Context Auditor  

---

## 1. TIÊU CHUẨN THIẾT KẾ & MA TRẬN VIEWPORT BẮT BUỘC

Kiểm thử giao diện đáp ứng (Responsive Mobile) được thực hiện nghiêm ngặt trên 9 độ phân giải màn hình đại diện từ điện thoại kích thước nhỏ đến màn hình máy tính để bàn mở rộng:

1. **320px** — iPhone SE (1st Gen), Màn hình siêu nhỏ.
2. **360px** — Samsung Galaxy tiêu chuẩn, Android phổ thông.
3. **375px** — iPhone X / XS / 11 Pro / SE (2nd Gen).
4. **390px** — iPhone 12 / 13 / 14 / 15 tiêu chuẩn.
5. **414px** — iPhone XR / 11 / 8 Plus.
6. **430px** — iPhone 14 Pro Max / 15 Pro Max.
7. **768px** — iPad Mini, Máy tính bảng chế độ dọc (Portrait Tablet).
8. **1024px** — iPad Pro, Laptop nhỏ (Landscape Tablet / Small Desktop).
9. **1440px** — Màn hình Desktop tiêu chuẩn (Full Desktop).

---

## 2. BẢNG KẾT QUẢ KIỂM THỬ THEO VIEWPORT & TÍNH NĂNG CHI TIẾT

| Viewport | Thành phần / Tính năng | Hành vi Kỳ vọng (Expected) | Trạng thái Thực tế (Actual) | Kết quả | Ghi chú Kỹ thuật (Notes) |
|---|---|---|---|:---:|---|
| **320px** | Header & Navbar | Ẩn desktop navbar, hiển thị nút toggle menu rút gọn | Navbar thu gọn mượt mà, không tràn thanh cuộn ngang (No horizontal overflow) | **PASS** | `overflow-x: hidden` toàn trang hoạt động chính xác. |
| **320px** | Mobile Bottom Nav | 5 tabs hiển thị co giãn chuẩn, icon vừa vặn | 5 tabs phân bổ đều với `flex: 1`, khoảng cách chạm tối thiểu 44px | **PASS** | Chiều cao cố định 64px, padding đáy an toàn. |
| **320px** | Event Cards | Thẻ sự kiện xếp chồng 1 cột, hình ảnh hiển thị tỷ lệ 16:9 | Thẻ hiển thị dạng dọc, nút 'Xem chi tiết' hiển thị rõ ràng | **PASS** | Grid tự động nhảy về `grid-template-columns: 1fr`. |
| **360px** | Mobile Drawer (Open) | Drawer trượt từ cạnh phải ra với backdrop làm mờ | Trượt mượt với transition 0.3s cubic-bezier, nền blur 20px | **PASS** | `z-index: 1045`, backdrop `z-index: 1040`. |
| **360px** | Mobile Drawer (Closed) | Drawer trượt về bên phải, gỡ bỏ hoàn toàn backdrop | Drawer ẩn, con trỏ chuột tương tác bình thường với trang bên dưới | **PASS** | `pointer-events: auto` được phục hồi toàn trang. |
| **375px** | AI Assistant Widget (Open)| Cửa sổ chat mở chiếm vừa màn hình di động, phím gõ không che ô input | Khung chat neo đáy chuẩn, chiều cao thích ứng `calc(100vh - 80px)` | **PASS** | `position: fixed`, z-index 1055 cao nhất hệ thống. |
| **375px** | AI Assistant (Closed) | Nút tròn mở AI thu gọn ở góc phải phía trên thanh bottom nav | Nút Floating Action Button (FAB) nổi bật với hiệu ứng phát sáng | **PASS** | Tọa độ `bottom: 80px; right: 16px`. |
| **390px** | Form Đăng ký Sự kiện | Input fields co giãn 100%, bàn phím ảo không che nút Submit | Các trường Họ tên, Email, SĐT xếp dọc rõ ràng, chạm focus mượt | **PASS** | Font-size 16px ngăn chặn hiện tượng tự động zoom trên iOS Safari. |
| **390px** | Check-in Camera Scanner | Khung quét camera QR tỷ lệ vuông 1:1 căn giữa | Khung quét hiển thị chuẩn giữa màn hình, viền bo góc Apple glass | **PASS** | Khung viewfinder 260x260px có thanh quét laser động. |
| **414px** | Modal Đặt Vé & VietQR | Modal hiển thị giữa màn hình kèm mã QR thanh toán | Mã QR 240x240px hiển thị rõ nét, nút tải ảnh QR và sao chép số tài khoản hoạt động tốt | **PASS** | Modal có thanh cuộn nội bộ khi nội dung dài. |
| **430px** | Bảng Lịch trình (Agenda)| Dòng thời gian hiển thị dọc với dấu chấm mốc thời gian nối liền | Timeline mốc thời gian hiển thị cân đối, tên phiên và diễn giả rõ ràng | **PASS** | `border-left: 2px solid var(--apple-blue)`. |
| **768px** | Tablet Event Catalog | Danh mục sự kiện hiển thị lưới 2 cột | Grid tự động chia 2 cột đều nhau, bộ lọc danh mục nằm ở hàng ngang trên cùng | **PASS** | `grid-template-columns: repeat(2, 1fr)`. |
| **768px** | Bottom Nav & Header | Bottom nav vẫn hiển thị cho tablet cầm tay, drawer hoạt động nhạy | Trải nghiệm cầm nắm bằng 2 tay thuận tiện, bottom nav vẫn active | **PASS** | Breakpoint `d-lg-none` hoạt động tới 991px. |
| **1024px** | Desktop Header Navbar | Chuyển sang thanh điều hướng ngang trên cùng, ẩn bottom nav | Thanh header kính mờ (Glassmorphism) xuất hiện, bottom nav ẩn hoàn toàn | **PASS** | `display: none` được kích hoạt cho `#appleBottomNav`. |
| **1024px** | Event Grid Desktop | Lưới sự kiện hiển thị 3 cột | 3 cột cân xứng, card hover nổi khối 3D mượt mà | **PASS** | `grid-template-columns: repeat(3, 1fr)`. |
| **1440px** | Full Desktop & Admin | Giao diện toàn màn hình, dashboard quản trị 4 cột số liệu | Toàn bộ dữ liệu hiển thị tối ưu với `max-width: 1400px` căn giữa | **PASS** | Không bị giãn vỡ nội dung trên màn hình siêu rộng (Ultra-wide). |

---

## 3. THẨM ĐỊNH BỐ CỤC Z-INDEX & TẦNG XẾP CHỒNG (STACKING CONTEXT AUDIT)

Hệ thống token Z-index được chuẩn hóa tuyệt đối theo tài liệu kiến trúc, không phát sinh xung đột hiển thị đè chéo (Z-index fight):

| Tầng (Layer) | Giá trị Token CSS | Thành phần Áp dụng | Trạng thái Kiểm thử |
|---|---|---|:---:|
| **Layer 0 (Base)** | `z-index: 0` | Nội dung văn bản, bảng dữ liệu, nền trang | Chuẩn |
| **Layer 1 (Sticky)** | `z-index: 1020` | Thanh Sticky Header, Breadcrumbs cố định | Chuẩn |
| **Layer 2 (Bottom Nav)** | `z-index: 1030` | Thanh Apple Mobile Bottom Navigation (`#appleBottomNav`) | Chuẩn |
| **Layer 3 (Backdrop)** | `z-index: 1040` | Lớp nền mờ tối màu của Modal & Drawer | Chuẩn |
| **Layer 4 (Drawer)** | `z-index: 1045` | Khung điều hướng trượt Mobile Drawer | Chuẩn |
| **Layer 5 (Modal)** | `z-index: 1050` | Cửa sổ xác nhận VietQR, Hủy vé Modal | Chuẩn |
| **Layer 6 (AI & Toast)** | `z-index: 1055 - 1080` | Widget AI Assistant, Thông báo Toast Notification | Chuẩn |

---

## 4. KẾT LUẬN KIỂM THỬ DI ĐỘNG

1. **Khả năng tương thích:** Hệ thống tương thích 100% trên cả 9 kích thước màn hình kiểm thử.
2. **Trải nghiệm cảm ứng:** Vùng chạm phím bấm tối thiểu đạt 44x44px theo tiêu chuẩn Apple HIG.
3. **Phòng chống lỗi:** Không phát hiện hiện tượng tràn màn hình ngang (horizontal scroll), không có lỗi chớp giao diện (FOUC) khi đổi chế độ sáng/tối (Dark/Light Mode), và không có tình trạng bàn phím ảo che mất nút gửi form.
