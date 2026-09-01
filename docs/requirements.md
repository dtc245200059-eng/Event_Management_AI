# Software Requirements Specification (SRS)
**Hệ Thống**: Quản Lý Sự Kiện Có Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
**Phiên Bản**: 2.0 (AI-Augmented SDLC Standard)  
**Tài Liệu Tham Chiếu**: `docs/customer-requirement.md`

---

## 1. Giới Thiệu & Phạm Vi

### 1.1. Mục đích
Tài liệu Đặc tả Yêu cầu Phần mềm (SRS) này xác định toàn bộ các yêu cầu chức năng (Functional Requirements), yêu cầu phi chức năng (Non-Functional Requirements), quy tắc nghiệp vụ (Business Rules) và các điểm kiểm soát của Hệ thống Quản lý Sự kiện Tích hợp AI.

### 1.2. Phạm vi Dự án (Project Scope)
- **Trong phạm vi (In-Scope)**:
  1. Xác thực người dùng và phân quyền 3 vai trò (Admin, Staff, Attendee).
  2. Quản lý vòng đời sự kiện (CRUD), danh mục, diễn giả, phòng họp và lịch trình timeline.
  3. Phát hành vé đa hạng (Free, Standard, VIP), thiết lập quota và mô phỏng giao dịch thanh toán.
  4. Tạo mã QR vector SVG định danh và soát vé trực tiếp bằng Camera Web với cơ chế chống quét trùng.
  5. Đánh giá khảo sát sau sự kiện và Dashboard thống kê doanh thu / check-in thời gian thực.
  6. Phân hệ 4 chức năng AI: RAG Chatbot Assistant (Offline Fallback), Tự động sinh nội dung sự kiện, Gợi ý sự kiện cá nhân hóa (TF-IDF), Dự báo tỷ lệ tham dự & Phân tích cảm xúc.
- **Ngoài phạm vi (Out-of-Scope)**:
  - Cổng thanh toán quốc tế Visa/Mastercard thực (chỉ hỗ trợ mô phỏng giao dịch nội bộ).
  - Phần cứng máy in vé nhiệt hoặc thẻ từ RFID chuyên dụng.
  - Hệ thống Live streaming video trực tiếp.

---

## 2. Các Tác Nhân Hệ Thống (Actors)
1. **Quản trị viên (Admin)**: Người quản lý toàn bộ hệ thống, tạo và duyệt sự kiện, quản lý diễn giả/vé, cấu hình AI và xem báo cáo phân tích nâng cao.
2. **Nhân viên soát vé (Staff)**: Người vận hành giao diện quét mã QR tại cổng sự kiện, kiểm tra tính hợp lệ của vé và xác nhận check-in.
3. **Người tham dự (Attendee)**: Khách hàng tìm kiếm sự kiện, đặt vé, thanh toán, quản lý vé điện tử, nhận mã QR, trò chuyện với AI Chatbot và gửi đánh giá.
4. **Hệ thống AI Ngoại vi (External AI / Gemini API)**: Dịch vụ trí tuệ nhân tạo cung cấp năng lực sinh ngôn ngữ tự nhiên và phân tích thông minh.

---

## 3. Danh Sách Yêu Cầu Chức Năng (Functional Requirements)

### 3.1. Nhóm Quản Lý Cốt Lõi (8 Modules)

| ID | Tên Yêu Cầu Chức Năng | Mô Tả Chi Tiết |
| :--- | :--- | :--- |
| **FR-01** | **Xác thực & Phân quyền (Auth & RBAC)** | Cho phép người dùng đăng ký, đăng nhập, đăng xuất. Mật khẩu được băm an toàn bằng PBKDF2 với Salt. Hệ thống phân quyền chặt chẽ 3 vai trò: *Admin, Staff, Attendee* thông qua Decorators. |
| **FR-02** | **Quản lý Sự kiện (Event CRUD)** | Admin/Staff có thể thêm, sửa, xóa, duyệt và xem danh sách sự kiện; phân loại danh mục, cập nhật ảnh banner, thời gian và số lượng người tham dự tối đa. |
| **FR-03** | **Quản lý Diễn giả & Lịch trình (Speaker & Schedule)** | Quản lý hồ sơ diễn giả (tên, chức danh, tiểu sử, ảnh đại diện), địa điểm phòng hội thảo (venue) và lịch trình từng phiên thảo luận (timeline). |
| **FR-04** | **Quản lý Hạng vé & Quota (Ticketing & Quotas)** | Thiết lập nhiều hạng vé (Free, Standard, VIP), định giá tiền, quy định hạn ngạch (quota) và tự động khóa vé khi `sold_count >= quota`. |
| **FR-05** | **Đăng ký & Thanh toán Mô phỏng (Booking & Payment)** | Người dùng chọn hạng vé và thực hiện đăng ký; xử lý thanh toán mô phỏng tạo mã giao dịch duy nhất, cập nhật số lượng vé an toàn qua Database Transactions. |
| **FR-06** | **Soát vé QR Thời gian thực (QR Check-in)** | Sinh mã QR định danh dạng vector SVG cho từng vé. Nhân viên quét mã bằng Camera Web; hệ thống xác thực tức thì và **chặn đứng tuyệt đối hành vi check-in trùng lặp** (trả về mã 409 Conflict). |
| **FR-07** | **Khảo sát & Phản hồi (Feedback & Survey)** | Người tham dự sau khi tham gia sự kiện có thể gửi điểm đánh giá (1-5 sao) và nhận xét; hệ thống lưu trữ và tổng hợp phản hồi. |
| **FR-08** | **Thống kê & Báo cáo (Dashboard Analytics)** | Cung cấp bảng điều khiển trực quan hiển thị tổng doanh thu, số vé đã phát hành, tỷ lệ check-in thực tế và biểu đồ phân bổ danh mục. |

### 3.2. Nhóm Phân Hệ Trí Tuệ Nhân Tạo (4 AI Modules)

| ID | Tên Yêu Cầu Chức Năng AI | Mô Tả Chi Tiết |
| :--- | :--- | :--- |
| **FR-AI-01** | **Trợ lý RAG Chatbot (Event AI Assistant)** | Trợ lý ảo trả lời câu hỏi tự nhiên về sự kiện dựa trên dữ liệu CSDL nội bộ với cơ chế Grounding chống Hallucination; tự động chuyển sang **Offline Fallback Mock Engine** khi mất kết nối. |
| **FR-AI-02** | **Tự động Sinh Mô tả Sự kiện (AI Event Generator)** | Tự động tạo nội dung mô tả sự kiện hấp dẫn, chuyên nghiệp và chuẩn SEO dựa trên tên sự kiện, danh mục và từ khóa gợi ý. |
| **FR-AI-03** | **Gợi ý Cá nhân hóa (Personalized Recommendations)** | Phân tích sở thích của người dùng hoặc sự kiện đang xem để đề xuất các sự kiện liên quan bằng thuật toán TF-IDF và Cosine Similarity. |
| **FR-AI-04** | **Dự báo Tham dự & Phân tích Cảm xúc (Predictive & Sentiment)** | Dự báo tỷ lệ tham dự thực tế (% show-up rate) dựa trên dữ liệu vé và phân loại cảm xúc phản hồi người tham dự (Positive, Neutral, Negative). |

---

## 4. Danh Sách Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

| ID | Nhóm Yêu Cầu | Tiêu Chuẩn & Chỉ Số Đo Lường |
| :--- | :--- | :--- |
| **NFR-01** | **Hiệu năng (Performance)** | Thời gian phản hồi trang Web < 1.5s; thời gian phản hồi AI Assistant < 3s; thời gian xác thực QR Check-in < 500ms. |
| **NFR-02** | **Bảo mật (Security)** | Tuân thủ OWASP Top 10; băm mật khẩu PBKDF2; lưu trữ API Key trong `.env`; lọc sạch dữ liệu định danh cá nhân (PII Masking). |
| **NFR-03** | **Độ tin cậy (Reliability)** | Độ sẵn sàng đạt 99.9%; cơ chế Fallback Mock hoạt động 100% khi mất mạng; giao dịch đặt vé tuân thủ nguyên tắc ACID (Rollback khi lỗi). |
| **NFR-04** | **Tính khả dụng (Usability)** | Giao diện hiện đại phong cách Glassmorphism, hỗ trợ Dark/Light Theme, Responsive 100% trên thiết bị di động. |
| **NFR-05** | **Toàn vẹn Dữ liệu (Data Integrity)** | CSDL quan hệ chuẩn 3NF, ràng buộc khóa chính/khóa ngoại nghiêm ngặt, không để xảy ra hiện tượng dữ liệu mồ côi (orphaned records). |
| **NFR-06** | **Khả năng mở rộng (Scalability)** | Kiến trúc 3-Tier phân tách rõ ràng, sẵn sàng chuyển đổi từ SQLite sang MySQL / PostgreSQL mà không sửa code nghiệp vụ. |
| **NFR-07** | **Tính di động (Portability)** | Hỗ trợ đóng gói Docker và triển khai nhất quán qua `docker-compose.yml` trên mọi hệ điều hành. |
| **NFR-08** | **Khả năng bảo trì (Maintainability)** | Tuân thủ chuẩn Clean Code (PEP 8), cấu trúc Blueprint rõ ràng, độ bao phủ kiểm thử tự động đạt trên 85%. |
| **NFR-09** | **Chống Bịa Đặt Dữ Liệu (Anti-Hallucination)** | Mô hình AI bắt buộc phải trả lời dựa trên Grounded Context; nếu không có dữ liệu phải thông báo từ chối lịch sự, không được tự bịa. |

---

## 5. Quy Tắc Nghiệp Vụ (Business Rules)
- **BR-01**: Mỗi sự kiện phải có ít nhất 1 hạng vé hợp lệ trước khi được chuyển sang trạng thái `published`.
- **BR-02**: Một người dùng (Attendee) chỉ được đăng ký tối đa 1 vé cho cùng một sự kiện để chống đầu cơ.
- **BR-03**: Khi số lượng vé bán ra (`sold_count`) đạt bằng hạn ngạch (`quota`), hạng vé phải tự động chuyển sang trạng thái `sold_out`.
- **BR-04**: Khi người dùng hủy vé thành công, số lượng `sold_count` phải được hoàn trả lại ngay lập tức và trạng thái vé chuyển về `available`.
- **BR-05**: Mỗi mã vé QR chỉ được phép Check-in duy nhất 1 lần. Mọi lần quét tiếp theo đều bị từ chối với mã lỗi 409.
- **BR-06**: Quản trị viên (Admin) có toàn quyền trên hệ thống; Nhân viên (Staff) chỉ được thao tác trên sự kiện và chức năng Soát vé.
- **BR-07**: Khách hàng vãng lai (Chưa đăng nhập) chỉ được xem danh sách sự kiện và hỏi chatbot chế độ cơ bản.
