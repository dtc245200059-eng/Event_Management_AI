# Frontend Architecture & Design System Specification

> **Dự Án:** EventAI Pro (Hệ Thống Quản Lý Sự Kiện Tích Hợp AI)  
> **Phiên Bản:** 1.0.0  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (27 Jinja2 Templates, 3,048 dòng Apple CSS Tokens, Vanilla JS)  
> **Tài Liệu Tham Chiếu:** [architecture.md](file:///d:/Event_Management_AI/docs/architecture.md), [responsive-mobile.md](file:///d:/Event_Management_AI/docs/responsive-mobile.md), [user-guide.md](file:///d:/Event_Management_AI/docs/user-guide.md)  
> **Kỹ năng liên quan:** [frontend-development](file:///d:/Event_Management_AI/.agents/skills/frontend-development/SKILL.md), [responsive-mobile](file:///d:/Event_Management_AI/.agents/skills/responsive-mobile/SKILL.md)  
> **Mã nguồn cốt lõi:** [app/templates/base.html](file:///d:/Event_Management_AI/app/templates/base.html), [app/static/css/style.css](file:///d:/Event_Management_AI/app/static/css/style.css), [app/static/js/main.js](file:///d:/Event_Management_AI/app/static/js/main.js)

---

## 1. Mục Đích & Phạm Vi
Tài liệu này đặc tả toàn diện tầng hiển thị người dùng (Presentation Layer) của hệ thống EventAI Pro:
- Cấu trúc cây thư mục Template Engine Jinja2 (27 tệp HTML).
- Hệ thống biến chuẩn thiết kế (Apple Design System Tokens) và cơ chế chuyển đổi giao diện Dark/Light/Auto.
- Kỹ thuật triệt tiêu chớp màn hình (Flash of Unstyled Content - FOUC).
- Kiến trúc JavaScript tương tác phía Client (State, Fetch API, DOM manipulation).

---

## 2. Cấu Trúc Thư Mục Giao Diện (Jinja2 Templates)

Hệ thống phân rã 27 templates thành các thư mục ngữ cảnh theo đúng Flask Blueprints:

```
app/templates/
├── base.html                     # Layout khung gốc (Navbar, Drawer, Footer, Bottom Nav, AI Widget)
├── main/                         # Giao diện công khai
│   ├── index.html                # Trang chủ (Hero, Featured Events, AI Recommendation Carousel)
│   ├── about.html                # Giới thiệu nền tảng & Đề tài 09
│   └── contact.html              # Liên hệ ban tổ chức
├── auth/                         # Xác thực tài khoản
│   ├── login.html                # Đăng nhập (Session cookie)
│   ├── register.html             # Đăng ký tài khoản Attendee
│   └── profile.html              # Cập nhật hồ sơ cá nhân
├── events/                       # Nghiệp vụ sự kiện
│   ├── list.html                 # Danh sách sự kiện & bộ lọc đa tiêu chí
│   ├── detail.html               # Chi tiết sự kiện, agenda timeline, diễn giả, vé
│   ├── create.html               # Form tạo sự kiện (kèm AI Description Generator)
│   ├── edit.html                 # Form chỉnh sửa sự kiện
│   └── manage.html               # Bảng quản trị sự kiện dành cho Organizer
├── tickets/                      # Quản lý vé
│   ├── book.html                 # Đặt vé & xác nhận giao dịch an toàn
│   └── my_tickets.html           # Vé của tôi, hiển thị mã QR vector SVG & nút Hủy vé
├── checkin/                      # Phân hệ soát vé
│   ├── scanner.html              # Quét mã QR qua Web Camera (HTML5-QRCode)
│   ├── manual.html               # Soát vé bằng mã thủ công
│   └── attendees.html            # Danh sách người tham dự & check-in nhanh
├── notifications/                # Phân hệ truyền thông
│   ├── send.html                 # Gửi thông báo phân khúc (kèm AI Draft Generator)
│   ├── inbox.html                # Hộp thư đến cá nhân của Attendee
│   └── manage.html               # Quản lý lịch sử thông báo đã gửi
├── admin/                        # Phân hệ quản trị hệ thống
│   ├── dashboard.html            # Analytics Dashboard, doanh thu, % show-up, sentiment
│   ├── users.html                # Quản lý người dùng & phân quyền RBAC
│   └── events.html               # Quản lý & duyệt sự kiện toàn sàn
├── ai/                           # Phân hệ Trí tuệ Nhân tạo
│   ├── chat_workspace.html       # Không gian tư vấn chuyên sâu Multi-Agent (/ai/workspace)
│   └── benchmark.html            # Bảng thực nghiệm 10 ca kiểm thử định lượng
└── errors/                       # Trang xử lý lỗi HTTP chuẩn hóa
    ├── 403.html                  # Lỗi từ chối quyền truy cập (Forbidden)
    ├── 404.html                  # Lỗi không tìm thấy trang (Not Found)
    └── 500.html                  # Lỗi máy chủ nội bộ (Internal Server Error)
```

---

## 3. Hệ Thống Design Tokens (Apple Design System)

Tệp `app/static/css/style.css` (3,048 dòng) định nghĩa tập tokens CSS phân cấp sắc nét dựa trên bảng màu Apple HSL:

### 3.1. Bảng Màu Theme Tự Động (Light & Dark Mode)
```css
:root {
  /* Surface Tokens */
  --bg-primary: #f5f5f7;
  --bg-surface: rgba(255, 255, 255, 0.8);
  --bg-card: #ffffff;
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --border-color: rgba(0, 0, 0, 0.08);

  /* Apple Accent Colors */
  --accent-blue: #0071e3;
  --accent-purple: #af52de;
  --accent-green: #34c759;
  --accent-orange: #ff9500;
  --accent-red: #ff3b30;

  /* Glassmorphism */
  --backdrop-blur: blur(20px);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
}

[data-theme="dark"] {
  --bg-primary: #000000;
  --bg-surface: rgba(28, 28, 30, 0.8);
  --bg-card: #1c1c1e;
  --text-primary: #f5f5f7;
  --text-secondary: #a1a1a6;
  --border-color: rgba(255, 255, 255, 0.12);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}
```

### 3.2. Chống Hiện Tượng Chớp Màn Hình (FOUC Prevention)
Để loại bỏ 100% hiện tượng chớp trắng/đen khi người dùng chuyển trang, mã JavaScript nạp theme đồng bộ ngay trong `<head>` của `base.html` trước khi trình duyệt dựng DOM:

```html
<script>
  (function() {
    const savedTheme = localStorage.getItem('eventai_theme') || 'auto';
    if (savedTheme === 'dark' || (savedTheme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  })();
</script>
```

---

## 4. Tương Tác Phía Client (Vanilla JavaScript)

### 4.1. Theme Controller (`main.js`)
Hỗ trợ 3 trạng thái: `light`, `dark`, `auto`. Tự động lắng nghe sự kiện thay đổi của hệ điều hành qua `window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change')`.

### 4.2. Khung Chat AI Assistant Nổi (`chat.js`)
- Mở/đóng mượt mà bằng CSS Transitions (`transform: translateY(...)`, `opacity`).
- Tự động cuộn xuống cuối khi có tin nhắn mới (`scrollTop = scrollHeight`).
- Hỗ trợ định dạng cú pháp Markdown cơ bản (in đậm, danh sách, khối mã code).
- Cơ chế Fallback hiển thị thông báo lỗi thân thiện khi API quá tải.

### 4.3. Quét Mã QR Camera (`scanner.html`)
- Sử dụng thư viện `html5-qrcode`.
- Tự động phát hiện camera sau (environment facing) trên điện thoại thông minh.
- Độ trễ phản hồi soát vé: `< 500ms`.
- Tự động ngắt quét tạm thời 2 giây sau mỗi lần đọc để tránh gửi request dồn dập.

---

## 5. Kết Luận & Tiêu Chuẩn Thẩm Mỹ
Giao diện EventAI Pro đạt chuẩn thẩm mỹ cao cấp, tối ưu hóa kích thước tải trang, không phụ thuộc framework CSS nặng nề (như Tailwind hay Bootstrap), đem lại cảm giác mượt mà và trực quan trên cả máy tính lẫn thiết bị di động.
