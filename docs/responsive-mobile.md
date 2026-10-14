# Responsive & Mobile Architecture Specification

> **Dự Án:** EventAI Pro (Hệ Thống Quản Lý Sự Kiện Tích Hợp AI)  
> **Phiên Bản:** 1.0.0  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Hỗ trợ 100% Mobile Breakpoints, Drawer, iOS Bottom Nav, Camera Scanner)  
> **Tài Liệu Tham Chiếu:** [frontend-architecture.md](file:///d:/Event_Management_AI/docs/frontend-architecture.md), [architecture.md](file:///d:/Event_Management_AI/docs/architecture.md), [user-guide.md](file:///d:/Event_Management_AI/docs/user-guide.md)  
> **Kỹ năng liên quan:** [responsive-mobile](file:///d:/Event_Management_AI/.agents/skills/responsive-mobile/SKILL.md), [frontend-development](file:///d:/Event_Management_AI/.agents/skills/frontend-development/SKILL.md)  
> **Mã nguồn cốt lõi:** [app/templates/base.html](file:///d:/Event_Management_AI/app/templates/base.html), [app/static/css/style.css](file:///d:/Event_Management_AI/app/static/css/style.css), [app/static/js/main.js](file:///d:/Event_Management_AI/app/static/js/main.js)

---

## 1. Mục Đích & Phạm Vi
Tài liệu này quy chuẩn hóa toàn bộ chiến lược tối ưu hóa trải nghiệm người dùng trên thiết bị di động (Mobile-First & Adaptive Responsive Design):
- Hệ thống Breakpoints chuẩn công nghiệp.
- Thanh điều hướng ngăn kéo (Mobile Drawer) và thanh công cụ đáy kiểu iOS (Bottom Navigation Bar).
- Hệ thống phân lớp hiển thị (Z-Index Stacking Context) chống xung đột đè lớp.
- Tối ưu hóa cử chỉ chạm (Touch Tap Targets) và vận hành Camera Web QR Scanner.

---

## 2. Hệ Thống Breakpoints Chuẩn Hóa

| Tên Thiết Bị | Khoảng Kích Thước Màn Hình | Hành Vi Giao Diện |
| :--- | :---: | :--- |
| **Desktop / Laptop** | `> 1024px` | Hiển thị Navbar đầy đủ, ẩn Mobile Drawer và Bottom Nav, lưới 3-4 cột thẻ sự kiện. |
| **Tablet (Ngang & Dọc)** | `768px - 1024px` | Thu gọn Navbar, hiển thị lưới 2 cột, hỗ trợ cả chuột và cảm ứng chạm. |
| **Mobile Standard** | `480px - 767px` | Ẩn Navbar ngang, kích hoạt **Mobile Drawer** và **Bottom Navigation**, lưới 1 cột. |
| **Small Mobile** | `< 480px` | Tối ưu cỡ chữ tiêu đề, co giãn padding an toàn, nút bấm đạt chuẩn tối thiểu `44px x 44px`. |

---

## 3. Thành Phần Điều Hướng Di Động Cốt Lõi

### 3.1. Ngăn Kéo Di Động (Mobile Drawer Navigation)
- **Cấu trúc HTML**: Thẻ `<aside id="mobile-drawer">` nằm trong `base.html` kết hợp lớp phủ mờ `<div id="drawer-backdrop">`.
- **Cơ chế hoạt động**:
  - Trạng thái đóng: `transform: translateX(-100%)`.
  - Trạng thái mở: Thêm class `.drawer-open`, trượt êm ái từ cạnh trái (`transform: translateX(0)` với `cubic-bezier(0.16, 1, 0.3, 1)`).
  - Tự động đóng khi nhấn vào backdrop hoặc nhấn phím `Escape`.

### 3.2. Thanh Điều Hướng Đáy Kiểu iOS (Bottom Navigation Bar)
- **Vị trí**: Cố định ở đáy màn hình (`position: fixed; bottom: 0; left: 0; right: 0`).
- **Hiệu ứng**: Nền kính mờ Glassmorphism (`backdrop-filter: blur(20px)`), viền mỏng phía trên.
- **5 Mục Cốt Lõi**:
  1. *Khám Phá* (Trang chủ `/`)
  2. *Sự Kiện* (`/events/`)
  3. *Vé Của Tôi* (`/tickets/my-tickets`)
  4. *Hộp Thư* (`/notifications/inbox`)
  5. *Tài Khoản / Menu* (Mở Drawer hoặc `/auth/login`)
- **Tương thích Safe Area**: Tự động chèn đệm đáy trên iPhone có tai thỏ/Dynamic Island:
  ```css
  padding-bottom: max(12px, env(safe-area-inset-bottom));
  ```

---

## 4. Hệ Thống Phân Lớp Z-Index (Stacking Context)

Để ngăn chặn tuyệt đối tình trạng widget chat che mất menu hoặc modal bị đè dưới camera scanner, hệ thống quy chuẩn thang điểm Z-index nghiêm ngặt:

```text
Layer 6 [500] : Toast Notifications & Flash Alerts
Layer 5 [400] : Confirm Modals & Dialogs
Layer 4 [301] : Mobile Drawer Content (`#mobile-drawer`)
Layer 3 [300] : Mobile Drawer Backdrop (`#drawer-backdrop`)
Layer 2 [200] : AI Assistant Floating Widget (`#ai-chat-widget`)
Layer 1 [100] : Sticky Top Navbar & Bottom Navigation Bar
Layer 0 [  1] : Main Content & Background Elements
```

---

## 5. Tối Ưu Hóa Camera Soát Vé Trên Thiết Bị Di Động

Giao diện `/checkin/scanner` được thiết kế chuyên biệt cho nhân viên soát vé tại cửa hội thảo:
1. **Lựa chọn Camera tự động**: Ưu tiên gọi camera sau (`facingMode: "environment"`) để quét mã QR dễ dàng.
2. **Khung ngắm cảm ứng**: Khung quét tỉ lệ 1:1 có đèn quét laser hiệu ứng CSS scanline.
3. **Phản hồi tức thì**: Rung haptic (`navigator.vibrate`) kết hợp âm thanh xác nhận khi vé hợp lệ.
4. **Ngăn chặn quét trùng**: Khóa camera 2 giây sau khi đọc thành công để kiểm soát luồng người vào cửa.

---

## 6. Kết Luận
Kiến trúc Mobile của EventAI Pro mang lại trải nghiệm tương đương ứng dụng bản địa (Native-like Web App), hoạt động trơn tru trên mọi dòng máy iOS và Android mà không cần cài đặt từ App Store.
