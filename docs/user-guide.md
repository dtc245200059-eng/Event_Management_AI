# Comprehensive User Manual & Operations Guide
**Hệ Thống**: Quản Lý Sự Kiện Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
**Phiên Bản**: 2.0 (AI-Augmented SDLC Standard)  
**Đối Tượng Sử Dụng**: Quản Trị Viên (Admin), Nhân Viên Soát Vé (Staff), Khách Tham Dự (Attendee)

---

## 1. Cẩm Nang Dành Cho Người Tham Dự (Attendee Guide)

### 1.1. Đăng Ký & Đăng Nhập Tài Khoản
1. Truy cập trang chủ `http://127.0.0.1:5000` và chọn **"Đăng Ký"** ở góc phải thanh điều hướng.
2. Nhập họ tên, email, username và mật khẩu -> Nhấn **"Tạo Tài Khoản"**.
3. Đăng nhập với tài khoản vừa tạo để bắt đầu trải nghiệm.

### 1.2. Tìm Kiếm & Đặt Vé Sự Kiện
1. Tại trang chủ hoặc danh mục **"Sự Kiện"**, sử dụng thanh tìm kiếm hoặc bộ lọc danh mục (Công nghệ, Kinh doanh, Giáo dục,...).
2. Nhấp vào sự kiện quan tâm để xem chi tiết: Giới thiệu, Lịch trình từng phiên, Danh sách diễn giả và Bản đồ địa điểm.
3. Cuộn xuống phần **"Hạng Vé & Đăng Ký"**: Chọn hạng vé (*Miễn phí, Tiêu chuẩn, VIP*) -> Nhấn **"Đặt Vé Ngay"**.
4. Hệ thống xử lý giao dịch an toàn và chuyển hướng bạn đến trang **"Vé Của Tôi"**.

### 1.3. Quản Lý Vé Điện Tử & Mã QR Vào Cổng
1. Truy cập mục **"Vé Của Tôi"** trên thanh menu.
2. Tại đây, mỗi vé đã đăng ký sẽ hiển thị đầy đủ thông tin: Tên sự kiện, Thời gian, Hạng vé, Trạng thái thanh toán và **Mã QR Vector sắc nét**.
3. Bạn có thể mở mã QR này trên màn hình điện thoại khi đến địa điểm sự kiện để nhân viên soát vé quét nhanh chóng.
4. Nếu có việc bận không thể tham gia, bạn có thể nhấn **"Hủy Vé"** để trả lại hạn ngạch cho người khác.

### 1.4. Trò Chuyện & Hỏi Đáp Với Trợ Lý Ảo AI
1. Nhấp vào biểu tượng **Chatbot hình robot** nổi ở góc dưới bên phải màn hình.
2. Đặt câu hỏi tự nhiên bằng tiếng Việt:
   - *"Lịch trình sự kiện có những phiên nào?"*
   - *"Diễn giả chính là ai?"*
   - *"Vé VIP bao nhiêu tiền và còn chỗ không?"*
3. Trợ lý AI sẽ trích xuất thông tin thực tế từ CSDL và giải đáp tức thì cho bạn 24/7.

---

## 2. Cẩm Nang Dành Cho Nhân Viên Soát Vé (Staff Guide)

### 2.1. Đăng Nhập & Mở Trình Quét Mã QR
1. Đăng nhập bằng tài khoản Staff (Mặc định: `staff` / `Staff@123`).
2. Trên thanh menu, chọn mục **"Soát Vé (Check-in Scanner)"** hoặc truy cập `/checkin/scanner`.

### 2.2. Vận Hành Quét Mã Tại Cửa Sự Kiện
1. Cấp quyền truy cập Camera trình duyệt khi có thông báo nhắc nhở.
2. Hướng khung Camera vào mã QR trên điện thoại của khách tham dự.
3. **Phản Hồi Hệ Thống**:
   - **Màn hình Xanh Lá + Âm báo Hợp lệ (200 OK)**: Vé hợp lệ, lần đầu vào cổng. Hệ thống hiển thị Tên khách, Sự kiện và Hạng vé -> Mời khách vào.
   - **Màn hình Đỏ + Cảnh Báo Gian Lận (409 Conflict)**: Vé đã được quét check-in trước đó kèm mốc thời gian cụ thể -> Giữ khách lại kiểm tra.
   - **Màn hình Đỏ (404 Not Found)**: Mã vé không tồn tại hoặc bị làm giả.
4. Trong trường hợp Camera điện thoại của khách bị mờ hoặc vỡ màn hình, nhân viên có thể **nhập mã vé thủ công** vào ô bên cạnh và nhấn "Xác Thực".

---

## 3. Cẩm Nang Dành Cho Quản Trị Viên (Admin Guide)

### 3.1. Tạo & Quản Lý Sự Kiện
1. Đăng nhập tài khoản Admin (Mặc định: `admin` / `Admin@123`).
2. Truy cập **"Quản Trị Sự Kiện"** -> Nhấn **"Thêm Sự Kiện Mới"**.
3. Điền các thông tin: Tên sự kiện, Danh mục, Thời gian bắt đầu/kết thúc, Địa điểm, Sức chứa.
4. **Sử Dụng AI Copywriter**: Nhấn nút **"Sinh Mô Tả Bằng AI"**, nhập một vài từ khóa trọng tâm, hệ thống sẽ tự động viết một bài mô tả sự kiện thu hút và chuẩn SEO.

### 3.2. Cấu Hình Lịch Trình, Diễn Giả & Hạng Vé
1. Trong trang chi tiết quản trị sự kiện:
   - Thêm hồ sơ Diễn giả và phòng họp.
   - Thiết lập các mốc Lịch trình timeline (phiên khai mạc, keynote, workshop).
   - Thiết lập các Hạng vé với mức giá và Hạn ngạch (Quota) tối đa để chống bán vượt vé.

### 3.3. Theo Dõi Báo Cáo Thống Kê & Dự Báo AI (Analytics Dashboard)
1. Truy cập mục **"Dashboard Báo Cáo"**:
   - Xem tổng doanh thu bán vé, tổng số người đăng ký và tỷ lệ check-in thực tế theo thời gian thực.
   - Xem biểu đồ dự báo số người đến tham dự thực tế (% show-up forecast) được tính toán bởi thuật toán máy học để chuẩn bị teabreak và phòng họp hợp lý.
   - Xem biểu đồ phân tích cảm xúc (Sentiment Analysis) tổng hợp từ các bài đánh giá của người tham gia.
