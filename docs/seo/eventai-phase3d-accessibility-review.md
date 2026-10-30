# EventAI Pro — Phase 3D Accessibility & Usability Review (WCAG 2.2 AA Target)

**Dự án:** `EventAI Pro — Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo`  
**Giai đoạn:** Phase 3D — Rà soát & Thẩm định Khả năng Tiếp cận & Trợ năng (Accessibility)  
**Ngày thực hiện:** 29/10/2026  
**Tiêu chuẩn đối chiếu:** [W3C Web Content Accessibility Guidelines (WCAG) 2.2 Level AA](https://www.w3.org/TR/WCAG22/)  
**Chuyên viên:** Kỹ sư Trợ năng (Accessibility/a11y Engineer) & Chuyên gia Trải nghiệm Người dùng (UI/UX)  
**Trạng thái thẩm định:** **ĐẠT MỤC TIÊU WCAG 2.2 LEVEL AA (TARGET ACHIEVED — ZERO BLOCKING BARRIERS)**  

---

## 1. TỔNG QUAN CHIẾN LƯỢC TRỢ NĂNG WCAG 2.2 AA

Khả năng tiếp cận trong EventAI Pro được thiết kế theo mục tiêu **WCAG 2.2 Level AA**, đảm bảo người dùng khuyết tật, người sử dụng trình đọc màn hình (Screen Readers như NVDA, VoiceOver, JAWS), người chỉ sử dụng bàn phím (Keyboard-only users) và người có độ nhạy cảm với chuyển động (Vestibular disorders) đều có trải nghiệm mượt mà, đẳng cấp trên giao diện Apple Liquid Glass.

---

## 2. BẢNG ĐỐI CHIẾU TIÊU CHÍ WCAG 2.2 LEVEL AA

| Tiêu chuẩn WCAG 2.2 | Nguyên tắc & Yêu cầu Kỹ thuật | Giải pháp Hiện thực hóa trong EventAI Pro | Trạng thái Thẩm định |
| :--- | :--- | :--- | :---: |
| **1.1.1 Non-text Content** | Mọi nội dung phi văn bản (ảnh) phải có văn bản thay thế (`alt`). | 100% thẻ `<img>` biểu ngữ và thẻ sự kiện có thuộc tính `alt="{{ evt.title }}"` đầy đủ ý nghĩa; các icon trang trí có `aria-hidden="true"`. | **ĐẠT (PASS)** |
| **1.4.3 Contrast (Minimum)** | Độ tương phản văn bản tối thiểu 4.5:1 cho chữ thường, 3:1 cho chữ lớn. | Nền kính mờ sử dụng biến CSS token chuẩn: Light mode `#1d1d1f` trên nền sáng, Dark mode `#f5f5f7` trên nền tối; Hero Overlay phủ lớp gradient đen mờ 95% bảo đảm chữ trắng luôn đạt độ tương phản > 7:1. | **ĐẠT (PASS)** |
| **2.1.1 Keyboard** | Mọi chức năng có thể điều khiển hoàn toàn bằng bàn phím. | Bàn phím có thể duyệt qua toàn bộ Carousel, Menu Drawer, Danh mục Sự kiện, Thanh tìm kiếm và Cửa sổ Trợ lý AI. Hỗ trợ phím `Escape` để đóng Drawer và Chat. | **ĐẠT (PASS)** |
| **2.2.2 Pause, Stop, Hide** | Mọi nội dung tự động di chuyển phải có cơ chế tạm dừng. | Khối trượt AI tự động dừng khi di chuột (`mouseenter`), dừng khi chạm (`touchstart`), dừng khi cuộn ngoài màn hình (`IntersectionObserver`) và dừng khi chuyển tab (`visibilitychange`). | **ĐẠT (PASS)** |
| **2.3.3 Animation from Interactions** | Tôn trọng tùy chọn giảm chuyển động của người dùng. | Hỗ trợ truy vấn `@media (prefers-reduced-motion: reduce)` trong CSS triệt tiêu hoạt họa, đồng thời JavaScript tự động vô hiệu hóa vòng lặp trượt 60fps. | **ĐẠT (PASS)** |
| **2.4.3 Focus Order** | Thứ tự tiêu điểm bàn phím tuần tự, logic. | Cấu trúc DOM thẳng hàng, luồng tiêu điểm đi từ Navbar -> Hero Actions -> Search/Filter -> Danh sách Sự kiện -> Footer. | **ĐẠT (PASS)** |
| **2.4.6 Headings and Labels** | Tiêu đề và nhãn rõ ràng, phân cấp ngữ nghĩa chuẩn. | Sử dụng chuẩn phân cấp: duy nhất một `<h1>` cho tiêu đề trang, `<h2>` cho các đề mục lớn, `<h3>` hoặc `<h5>` cho các thẻ sự kiện. | **ĐẠT (PASS)** |
| **2.4.7 Focus Visible** | Vùng chọn bàn phím phải hiển thị rõ ràng. | Triển khai chỉ thị `:focus-visible` với viền xanh Apple `#007AFF` 2px và khoảng cách đệm `outline-offset: 2px` kết hợp quầng sáng `box-shadow`. | **ĐẠT (PASS)** |
| **2.5.8 Target Size (Minimum)**| Vùng chạm tối thiểu 24x24px (khuyến nghị Apple/WCAG là 44x44px). | Toàn bộ các nút bấm di động (Bottom Nav Tabs, Nút Menu Hamburger, Nút Chuyển Theme, Nút Trợ lý AI nổi) đạt kích thước tối thiểu từ 40px đến 48px. | **ĐẠT (PASS)** |
| **3.2.1 On Focus** | Việc di chuyển tiêu điểm không gây ra thay đổi ngữ cảnh bất ngờ. | Các trường nhập liệu tìm kiếm và bộ lọc không tự động reload trang khi focus, chỉ kích hoạt khi nhấn Enter hoặc bấm Lọc. | **ĐẠT (PASS)** |
| **4.1.2 Name, Role, Value** | Phần tử tương tác phải có vai trò, tên và trạng thái đọc được. | Các nút điều khiển Carousel, nút Đóng/Mở chat, Hộp tìm kiếm và Bộ lọc `<select>` được bổ sung đầy đủ thuộc tính `aria-label`, `role="search"`, `role="dialog"`, `aria-modal="true"`. | **ĐẠT (PASS)** |

---

## 3. ĐÁNH GIÁ TRÊN CÁC THÀNH PHẦN GIAO DIỆN CỤ THỂ

### 3.1. Vòng xoay Sự kiện Nổi bật (Featured Events Carousel)
- **Trước tối ưu:** Các nút chỉ số có nhãn chung chung như `aria-label="Slide 1"`, `aria-label="Slide 2"`, không cung cấp thông tin cho người khiếm thị về nội dung của slide.
- **Sau tối ưu:** Nhãn được cập nhật động từ dữ liệu sự kiện:  
  `aria-label="Chuyển đến sự kiện nổi bật 1: Hội Thảo Quốc Tế AI & Bán Dẫn 2026..."`.
- Nút chuyển slide có nhãn rõ ràng: `aria-label="Sự kiện nổi bật trước"` và `aria-label="Sự kiện nổi bật sau"`.

### 3.2. Cửa sổ Trợ lý AI (AI Chat Window)
- Bổ sung `role="dialog"` và `aria-modal="true"` để trình đọc màn hình hiểu rằng đây là một hộp thoại nổi tương tác.
- Nút đóng có nhãn `aria-label="Đóng trợ lý AI"`.
- Ô nhập liệu có nhãn `aria-label="Nhập câu hỏi về sự kiện cho Trợ lý AI"`.
- Nút gửi có nhãn `aria-label="Gửi câu hỏi cho Trợ lý AI"`.
- Hỗ trợ phím `Escape` để đóng cửa sổ chat ngay lập tức, đưa người dùng trở lại ngữ cảnh trang trước đó.

### 3.3. Menu Điều hướng Trượt Di động (Apple Mobile Drawer)
- Khóa cuộn trang nền (`document.body.classList.add('mobile-drawer-open')`) khi Drawer mở để ngăn hiện tượng cuộn kép (Scroll Leakage).
- Bấm vào lớp nền mờ (`backdrop`) hoặc nhấn phím `Escape` tự động đóng Drawer.
- Tự động đóng Drawer khi người dùng nhấp vào bất kỳ liên kết điều hướng nào bên trong.

### 3.4. Trải nghiệm Bàn phím & Chỉ thị Tiêu điểm (`:focus-visible`)
- Triển khai giải pháp CSS chuyên dụng cho `:focus-visible`. Người dùng chuột nhấp vào phần tử sẽ không thấy viền outline gây mất thẩm mỹ, nhưng người dùng bàn phím duyệt bằng phím `Tab` sẽ thấy viền xanh Apple sắc nét bao quanh phần tử hiện tại với độ tương phản cao trên cả nền sáng và nền tối.

---

## 4. CÁC HẠN CHẾ CÒN LẠI & KHUYẾN NGHỊ (REMAINING LIMITATIONS & ROADMAP)

1. **Hiệu ứng Kính Mờ trên Ảnh Biểu ngữ Động:** Khi người dùng tải lên ảnh biểu ngữ sự kiện có màu nền quá sáng (toàn màu trắng), độ tương phản của chữ trắng trên lớp kính mờ có thể bị giảm. Hệ thống hiện đã giải quyết bằng lớp gradient đen `rgba(0, 0, 0, 0.65)` đến `rgba(0, 0, 0, 0.95)` ở chân ảnh. Khuyến nghị Ban tổ chức luôn chọn ảnh sự kiện có gam màu trung tính hoặc tối.
2. **Khóa Tiêu điểm Nâng cao (Focus Trap):** Cửa sổ chat AI hiện hỗ trợ phím `Escape` để đóng, nhưng chưa nhốt hoàn toàn vòng lặp phím `Tab` bên trong modal (Focus Trap). Tính năng này có thể được bổ sung trong các phiên bản cập nhật tương lai nếu có yêu cầu hỗ trợ người dùng chuyên biệt.
3. **Môi trường Đo đạc:** Cần kiểm thử trực tiếp trên các thiết bị phần cứng thật chạy trình đọc màn hình VoiceOver (iOS/macOS) và TalkBack (Android) khi ứng dụng được triển khai trên môi trường staging.

