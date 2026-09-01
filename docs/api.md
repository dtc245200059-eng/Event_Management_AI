# RESTful API & AI Services Specification
**Hệ Thống**: Quản Lý Sự Kiện Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
**Phiên Bản**: 2.0 (AI-Augmented SDLC Standard)  
**Định Dạng Dữ Liệu**: JSON (`application/json`)  
**Base URL**: `http://localhost:5000`

---

## 1. Danh Mục Nhóm API Hệ Thống

```
┌──────────────────────────────────────────────────────────────────────────┐
│                             DANH MỤC API ENDPOINTS                       │
├───────────────────────┬──────────────────────────────────────────────────┤
│ 1. Xác Thực (Auth)    │ POST /auth/register, POST /auth/login            │
│ 2. Sự Kiện (Events)   │ GET /events/, GET /events/<id>, POST /events/new │
│ 3. Đặt Vé (Tickets)   │ POST /tickets/book/<id>, POST /tickets/cancel    │
│ 4. Soát Vé (Check-in) │ POST /checkin/verify-api                         │
│ 5. Trí Tuệ Nhân Tạo   │ POST /api/chat, POST /api/generate-description   │
│                       │ GET /api/recommendations, GET /api/predict-attend│
└───────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Chi Tiết Các Endpoints Quản Lý Cốt Lõi

### 2.1. Xác Thực & Đăng Nhập (`POST /auth/login`)
- **Mô tả**: Xác thực tài khoản người dùng và thiết lập phiên làm việc (Session).
- **Request Headers**: `Content-Type: application/x-www-form-urlencoded` hoặc `application/json`
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "Admin@Password123"
  }
  ```
- **Response (200 OK - Thành công)**:
  ```json
  {
    "success": true,
    "message": "Đăng nhập thành công!",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
  ```
- **Response (401 Unauthorized - Sai thông tin)**:
  ```json
  {
    "success": false,
    "message": "Tên đăng nhập hoặc mật khẩu không chính xác."
  }
  ```

---

### 2.2. Đặt Vé Sự Kiện An Toàn (`POST /tickets/book/<int:event_id>`)
- **Mô tả**: Đặt vé theo hạng vé đã chọn, kiểm soát Quota qua DB Transaction.
- **Yêu cầu Quyền**: Đã đăng nhập (`@login_required`).
- **Request Body**:
  ```json
  {
    "ticket_id": 2
  }
  ```
- **Response (200 OK - Mua vé thành công)**:
  ```json
  {
    "success": true,
    "message": "Đăng ký vé thành công!",
    "registration": {
      "registration_code": "REG-202610-8A1B2C3D",
      "ticket_number": "TCK-202610-XYZ12345",
      "ticket_type": "standard",
      "price": 200000.0,
      "payment_status": "paid",
      "qr_code_url": "/static/qrcodes/TCK-202610-XYZ12345.svg"
    }
  }
  ```
- **Response (400 Bad Request - Hết vé / Sold Out)**:
  ```json
  {
    "success": false,
    "message": "Rất tiếc, hạng vé này đã hết số lượng phát hành (Sold Out)!"
  }
  ```

---

### 2.3. Xác Thực & Soát Vé QR Thời Gian Thực (`POST /checkin/verify-api`)
- **Mô tả**: Quét mã định danh vé QR tại cổng, kiểm tra tính hợp lệ và chống quét trùng.
- **Yêu cầu Quyền**: Nhân viên soát vé (`@staff_required` hoặc `@admin_required`).
- **Request Body**:
  ```json
  {
    "ticket_number": "TCK-202610-XYZ12345"
  }
  ```
- **Response (200 OK - Soát vé thành công lần đầu)**:
  ```json
  {
    "success": true,
    "status": "valid",
    "message": "Check-in thành công!",
    "attendee_name": "Nguyễn Văn A",
    "event_title": "Vietnam AI Summit 2026",
    "ticket_type": "standard",
    "checked_in_at": "2026-10-15 08:30:15"
  }
  ```
- **Response (409 Conflict - Cảnh báo vé đã quét trước đó)**:
  ```json
  {
    "success": false,
    "status": "duplicate",
    "message": "CẢNH BÁO: Vé này đã được check-in lúc 08:30:15 trước đó!",
    "checked_in_at": "2026-10-15 08:30:15"
  }
  ```
- **Response (404 Not Found - Vé không tồn tại)**:
  ```json
  {
    "success": false,
    "status": "invalid",
    "message": "Mã vé không tồn tại trên hệ thống!"
  }
  ```

---

## 3. Chi Tiết Các Endpoints Dịch Vụ Trí Tuệ Nhân Tạo (AI Endpoints)

### 3.1. Trợ Lý Ảo RAG Sự Kiện (`POST /api/chat`)
- **Mô tả**: Tiếp nhận câu hỏi tự nhiên về sự kiện, truy xuất dữ liệu CSDL và trả về câu trả lời chuẩn xác (hoạt động ở 2 chế độ `live` và `mock`).
- **Request Body**:
  ```json
  {
    "question": "Diễn giả chính của sự kiện Vietnam AI Summit là ai và vé VIP giá bao nhiêu?",
    "event_id": 1
  }
  ```
- **Response (200 OK - Phản hồi thành công)**:
  ```json
  {
    "answer": "Diễn giả chính của sự kiện là TS. Lê Quang Dũng (Chuyên gia GenAI). Vé VIP có giá niêm yết là 500.000 VNĐ bao gồm quyền lợi tài liệu độc quyền và chỗ ngồi hàng đầu.",
    "mode": "live",
    "latency": 1.54,
    "event_id": 1
  }
  ```

---

### 3.2. Tự Động Sinh Mô Tả Sự Kiện (`POST /api/generate-description`)
- **Mô tả**: Tự động sinh nội dung bài viết mô tả sự kiện hấp dẫn cho Ban tổ chức dựa trên thông tin tóm tắt.
- **Request Body**:
  ```json
  {
    "title": "Hội Thảo Điện Toán Đám Mây & AI 2026",
    "category": "Technology",
    "keywords": "Cloud Native, Kubernetes, Microservices, Gemini"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "description": "Chào mừng bạn đến với Hội Thảo Điện Toán Đám Mây & AI 2026 - Nơi hội tụ các chuyên gia hàng đầu về Cloud Native, Kubernetes và tích hợp Microservices cùng Gemini AI..."
  }
  ```

---

### 3.3. Gợi Ý Sự Kiện Cá Nhân Hóa (`GET /api/recommendations`)
- **Mô tả**: Gợi ý danh sách sự kiện phù hợp bằng thuật toán TF-IDF & Cosine Similarity.
- **Query Parameters**: `interests=Học hỏi về Trí tuệ nhân tạo &top_n=3`
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "recommendations": [
      {
        "id": 1,
        "event_code": "EVT-2026-AI",
        "title": "Vietnam AI Summit 2026",
        "category": "Technology",
        "similarity_score": 0.88,
        "banner_url": "/static/images/banner_ai.jpg"
      }
    ]
  }
  ```
