# Software Requirements Specification (SRS)

> **Hệ Thống:** Quản Lý Sự Kiện Có Tích Hợp Trí Tuệ Nhân Tạo (Event Management AI System)  
> **Phiên Bản:** 3.1 (Đã Đồng Bộ & Xác Minh Với Toàn Bộ Mã Nguồn Thực Tế)  
> **Trạng thái tổng thể:** `[IMPLEMENTED]` (9/9 Core Modules, 6/6 AI Features, 4/4 Roles RBAC)  
> **Tài Liệu Tham Chiếu:** [customer-requirement.md](file:///d:/Event_Management_AI/docs/customer-requirement.md), [user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md), [acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md), [traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md), [api.md](file:///d:/Event_Management_AI/docs/api.md)  
> **Kỹ năng liên quan:** [requirements-analysis](file:///d:/Event_Management_AI/.agents/skills/requirements-analysis/SKILL.md), [testing](file:///d:/Event_Management_AI/.agents/skills/testing/SKILL.md)  
> **Kiểm thử liên quan:** [tests/test_event_flows.py](file:///d:/Event_Management_AI/tests/test_event_flows.py), [tests/test_ai_agent.py](file:///d:/Event_Management_AI/tests/test_ai_agent.py), [tests/test_multi_agent.py](file:///d:/Event_Management_AI/tests/test_multi_agent.py) (36/36 passed)

---

## 1. Giới Thiệu & Phạm Vi

### 1.1. Mục đích
Tài liệu Đặc tả Yêu cầu Phần mềm (SRS) này chuẩn hóa toàn bộ các yêu cầu chức năng (Functional Requirements), yêu cầu phi chức năng (Non-Functional Requirements), quy tắc nghiệp vụ (Business Rules) và các điểm kiểm soát an toàn AI của **Hệ thống Quản lý Sự kiện Tích hợp Trí tuệ Nhân tạo (Đề tài 09)**.

### 1.2. Phạm vi Dự án (Project Scope)
- **Trong phạm vi (In-Scope)**:
  1. Xác thực người dùng và phân quyền 4 vai trò: Quản trị viên (`admin`), Ban tổ chức (`organizer`), Nhân viên soát vé (`staff` / `checkin_staff`), Khách tham dự (`attendee`).
  2. Quản lý toàn diện sự kiện (CRUD), lịch trình các phiên (Schedules/Timeline), thông tin diễn giả (Speakers), địa điểm (Venues).
  3. Quản lý hạng vé (Tickets) với hạn ngạch số lượng (Quota), xử lý đăng ký, hủy vé và mô phỏng thanh toán an toàn.
  4. Tạo mã QR vé định danh (Vector SVG) và giao diện quét mã QR qua Web Camera để soát vé thời gian thực, ngăn chặn tuyệt đối quét trùng (chống gian lận vé).
  5. Mô-đun Truyền thông & Gửi Thông báo (Notifications): Phân loại thư mời, nhắc lịch, cảm ơn, cập nhật khẩn cấp theo đối tượng phân khúc (Tất cả, Đã check-in, Chưa check-in, VIP); Hộp thư đến (Attendee Inbox) và thống kê tỷ lệ gửi.
  6. Thu thập đánh giá khảo sát sau sự kiện (1-5 sao kèm nhận xét định tính).
  7. Bảng điều khiển (Dashboard) thống kê thời gian thực: số vé, doanh thu, tỷ lệ check-in, phân tích tổng thể.
  8. Phân hệ Trí tuệ Nhân tạo (AI Core Modules theo Đề tài 09):
     - **RAG Chatbot Tra cứu Sự kiện & FAQ**: Tích hợp kho dữ liệu sự kiện và câu hỏi thường gặp (`EventFAQ`), kiểm chứng chống bịa đặt (Anti-Hallucination) và cơ chế dự phòng ngoại tuyến (Offline Fallback Mock Engine).
     - **AI Soạn thảo Thông báo & Email Tự động**: Tự động sinh bản thảo email thư mời, nhắc nhở, tri ân và thông báo khẩn cấp dựa trên dữ liệu sự kiện chuẩn xác, cấm rò rỉ dữ liệu cá nhân (PII).
     - **AI Tóm tắt Ý kiến Phản hồi**: Tự động gom nhóm phản hồi thành 4 nhóm ý kiến cốt lõi (Nội dung & Diễn giả, Check-in & Vận hành, Hội trường & Hậu cần, Lịch trình & Thời lượng) và trích xuất Hành động Cải tiến (Actionable Takeaways).
     - **Bộ công cụ AI phụ trợ**: Tự động sinh nội dung mô tả sự kiện (AI Description Generator), Gợi ý sự kiện cá nhân hóa (TF-IDF Cosine Similarity), Dự báo tỷ lệ tham dự (% Show-up) và Phân tích Cảm xúc (Sentiment Analysis).
- **Ngoài phạm vi (Out-of-Scope)**:
  - Cổng thanh toán quốc tế Visa/Mastercard trực tiếp (hỗ trợ mô phỏng giao dịch nội bộ và quản lý trạng thái thanh toán).
  - Phần cứng máy in vé vật lý tại chỗ.

---

## 2. Các Tác Nhân Hệ Thống (Actors)
1. **Quản trị viên (Admin)**: Toàn quyền quản trị hệ thống, quản lý tài khoản người dùng, phân quyền vai trò, cấu hình hệ thống, xem toàn bộ báo cáo doanh thu và AI Dashboard.
2. **Ban tổ chức (Organizer)**: Đơn vị chủ trì tạo lập và quản lý sự kiện, điều phối lịch trình, diễn giả, quản lý hạng vé và hạn ngạch, soạn thảo và gửi thông báo truyền thông (sử dụng AI Email Generator), phân tích báo cáo ý kiến phản hồi (AI Feedback Summary).
3. **Nhân viên soát vé (Staff / Check-in Staff)**: Người vận hành quầy tiếp đón tại cổng sự kiện, quét mã QR từ điện thoại hoặc vé in của khách tham dự, xác minh tính hợp lệ và chặn đứng vé đã sử dụng hoặc không hợp lệ.
4. **Khách tham dự (Attendee)**: Tìm kiếm, lọc sự kiện, đặt vé tham dự, nhận mã QR vé cá nhân, nhận thông báo trong Hộp thư đến (Inbox), gửi đánh giá phản hồi sau sự kiện và tương tác với Trợ lý RAG Chatbot.
5. **Hệ thống Mô hình Ngôn ngữ Lớn (LLM / Gemini API & Local Fallback Engine)**: Cung cấp năng lực suy luận ngôn ngữ tự nhiên, trích xuất dữ liệu và sinh văn bản có kiểm chứng.

---

## 3. Danh Sách Yêu Cầu Chức Năng (Functional Requirements)

### 3.1. Nhóm Quản Lý Vận Hành Cốt Lõi (8 Modules Nghiệp Vụ)

| ID | Tên Chức Năng | Trạng Thái | Mô Tả Chi Tiết | Minh Chứng Mã Nguồn & Test |
| :--- | :--- | :---: | :--- | :--- |
| **FR-01** | **Xác thực & Phân quyền (Auth & RBAC)** | `[IMPLEMENTED]` | Cho phép đăng ký, đăng nhập, đăng xuất, cập nhật hồ sơ cá nhân. Mật khẩu băm an toàn PBKDF2. Phân quyền chặt chẽ 4 vai trò: `admin`, `organizer`, `staff`, `attendee` bằng Decorators. | `app/routes/auth.py`, `tests/test_auth_rbac.py` (10 passed) |
| **FR-02** | **Quản lý Sự kiện (Event CRUD)** | `[IMPLEMENTED]` | Ban tổ chức và Admin có thể thêm, sửa, xóa, duyệt và xuất bản sự kiện; quản lý danh mục, hình ảnh banner, thời gian bắt đầu/kết thúc, số lượng người tham dự tối đa. | `app/routes/events.py`, `tests/test_event_flows.py` |
| **FR-03** | **Quản lý Lịch trình & Diễn giả (Schedules & Speakers)** | `[IMPLEMENTED]` | Quản lý hồ sơ diễn giả (tên, chức vụ, học vị, tiểu sử, ảnh); thiết lập chi tiết lịch trình phiên họp (timeline sessions), phân công diễn giả và phòng hội thảo. | `app/routes/events.py`, `app/models.py` |
| **FR-04** | **Quản lý Hạng vé & Hạn ngạch (Tickets & Quota)** | `[IMPLEMENTED]` | Thiết lập đa dạng hạng vé (Free, Standard, VIP), cấu hình số lượng phát hành (Quota); tự động khóa hoặc đổi trạng thái khi `sold_count >= quota`. | `app/routes/tickets.py`, `tests/test_event_flows.py::test_ticket_quota_limit` |
| **FR-05** | **Đăng ký & Thanh toán Mô phỏng (Booking & Payment)** | `[IMPLEMENTED]` | Khách tham dự đặt vé, xử lý giao dịch an toàn qua Database Transactions; đảm bảo khôi phục lại vé nếu giao dịch thất bại hoặc người dùng hủy vé. | `app/routes/tickets.py`, `tests/test_event_flows.py::test_cancel_registration_restores_quota` |
| **FR-06** | **Soát vé QR Thời gian thực (QR Check-in)** | `[IMPLEMENTED]` | Tự động tạo mã QR định danh duy nhất cho từng vé. Nhân viên soát vé quét mã qua Camera Web; hệ thống xác thực tức thì và **chặn đứng tuyệt đối hành vi quét trùng** (trả về mã 409 Conflict). | `app/routes/checkin.py`, `tests/test_event_flows.py::test_duplicate_checkin_prevented` |
| **FR-07** | **Truyền thông & Gửi Thông báo (Notifications)** | `[IMPLEMENTED]` | Ban tổ chức gửi thông báo/email theo phân khúc: Tất cả người đăng ký, Đã check-in, Chưa check-in, VIP. Cung cấp Hộp thư đến (Inbox) cho khách tham dự và đếm số lượng người nhận. | `app/routes/notifications.py`, `tests/test_event_flows.py::test_organizer_send_notification` |
| **FR-08** | **Khảo sát & Phản hồi (Feedback & Reviews)** | `[IMPLEMENTED]` | Khách đã tham dự gửi điểm đánh giá (1-5 sao) và bình luận chất lượng dịch vụ sau sự kiện; lưu vết thời gian gửi. | `app/routes/events.py`, `app/models.py::Feedback` |
| **FR-09** | **Thống kê & Báo cáo (Dashboard Analytics)** | `[IMPLEMENTED]` | Bảng điều khiển trực quan hiển thị tổng doanh thu, số vé đã bán, tỷ lệ check-in thực tế (% show-up), phân bổ loại vé và thống kê cảm xúc người tham gia. | `app/routes/admin.py`, `app/templates/admin/` |

---

### 3.2. Nhóm Phân Hệ Trí Tuệ Nhân Tạo Tích Hợp (AI Modules)

| ID | Tên Phân Hệ AI | Trạng Thái | Mô Tả Chi Tiết & Ràng Buộc Kỹ Thuật | Minh Chứng Mã Nguồn & Test |
| :--- | :--- | :---: | :--- | :--- |
| **FR-AI-01** | **Trợ lý RAG Chatbot Tra cứu Sự kiện & FAQ** | `[IMPLEMENTED]` | Trợ lý ảo trả lời câu hỏi tự nhiên về sự kiện, thời gian, địa điểm, diễn giả, lịch trình và chính sách quy định (Event FAQs). Áp dụng kỹ thuật RAG Grounding: Chỉ trả lời dựa trên dữ liệu thật, từ chối khi không có dữ liệu (Anti-Hallucination). Tự động kích hoạt Offline Fallback Mock Engine khi mất mạng. | `app/services/rag_service.py`, `tests/test_ai_agent.py` |
| **FR-AI-02** | **AI Soạn thảo Thông báo & Email Tự động (Draft Generator)** | `[IMPLEMENTED]` | Tự động soạn thảo nội dung thông báo/email theo 4 loại: Thư mời (`invitation`), Nhắc nhở trước giờ G (`reminder`), Lời cảm ơn sau sự kiện (`thank_you`), Thông báo cập nhật (`update`). Đảm bảo độ chính xác theo sự kiện đã chọn, **tuyệt đối không gửi PII người dùng (email, sđt) vào Prompt của AI**. | `app/services/gemini_service.py`, `tests/test_ai_agent.py` |
| **FR-AI-03** | **AI Tóm tắt Ý kiến Phản hồi theo Nhóm Chủ đề (Feedback Summarizer)** | `[IMPLEMENTED]` | Tự động phân loại và tóm tắt phản hồi của người tham gia thành 4 nhóm ý kiến: (1) Nội dung & Diễn giả, (2) Check-in & Vận hành, (3) Hội trường & Hậu cần, (4) Lịch trình & Thời lượng. Tự động đề xuất các hành động cải tiến cụ thể (Actionable Takeaways) cho Ban tổ chức. | `app/services/gemini_service.py`, `tests/test_ai_agent.py` |
| **FR-AI-04** | **AI Sinh Mô tả Sự kiện (AI Event Description Generator)** | `[IMPLEMENTED]` | Tự động sinh nội dung giới thiệu, agenda tóm lược và điểm nổi bật của sự kiện dựa trên tiêu đề, danh mục và từ khóa mục tiêu, hỗ trợ Ban tổ chức tạo sự kiện nhanh chóng. | `app/services/gemini_service.py`, `app/routes/ai.py` |
| **FR-AI-05** | **Gợi ý Cá nhân hóa (Personalized Recommendations)** | `[IMPLEMENTED]` | Phân tích sở thích người dùng và nội dung sự kiện bằng thuật toán xử lý ngôn ngữ tự nhiên (TF-IDF & Cosine Similarity) để đề xuất danh sách sự kiện phù hợp nhất. | `app/services/vector_service.py`, `app/routes/ai.py` |
| **FR-AI-06** | **Dự báo Tỷ lệ Tham dự & Phân tích Cảm xúc** | `[IMPLEMENTED]` | Mô hình dự báo xác suất khách tham dự thực tế (% show-up rate) dựa trên loại vé, thời gian đăng ký và phân loại cảm xúc phản hồi (Positive, Neutral, Negative). | `app/services/gemini_service.py`, `app/routes/ai.py` |
| **FR-AI-07** | **Multi-Agent Advisory & Decision Support** | `[IMPLEMENTED]` | Hệ thống 7 Agent chuyên trách phối hợp suy luận đa tiêu chí, kiểm duyệt chéo CSDL với Critic Guardrail và vòng lặp tự sửa lỗi (Retry Loop) chống Hallucination 100%. | `app/agents/`, `tests/test_multi_agent.py` (9 passed) |

---

## 4. Danh Sách Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

| ID | Tiêu Chí | Yêu Cầu Chi Tiết |
| :--- | :--- | :--- |
| **NFR-01** | **Hiệu năng (Performance)** | Tải trang Web < 1.5s; Phản hồi soát vé QR < 500ms; Phản hồi AI Assistant qua Streaming/Cache < 3s. |
| **NFR-02** | **Bảo mật (Security)** | Tuân thủ OWASP Top 10 Web & LLM: Mã hóa mật khẩu PBKDF2-SHA256; Parameterized SQL Query ngăn chặn SQLi; XSS sanitization; CSRF protection; Bảo vệ khóa bí mật `.env`; Cấm truyền dữ liệu nhận dạng cá nhân (PII) cho AI. |
| **NFR-03** | **Độ tin cậy (Reliability)** | Độ sẵn sàng 99.9%. Tích hợp cơ chế Fallback Mock Engine tự hành 100% khi ngắt kết nối Gemini API. Giao dịch vé bảo toàn nguyên tắc ACID. |
| **NFR-04** | **Tính khả dụng (Usability)** | Giao diện hiện đại phong cách Dark/Light Theme, hiệu ứng Glassmorphism sắc nét, chuẩn Responsive tương thích hoàn toàn trên Desktop, Tablet và Mobile. |
| **NFR-05** | **Toàn vẹn Dữ liệu (Data Integrity)** | Cơ sở dữ liệu chuẩn hóa 3NF, ràng buộc khóa ngoại (Foreign Keys), khóa duy nhất (Unique Constraints) ngăn chặn đăng ký trùng lặp hoặc mồ côi dữ liệu. |
| **NFR-06** | **Chống Bịa Đặt Dữ Liệu (Anti-Hallucination)** | System Prompt kiểm soát chặt chẽ: chỉ trả lời trong phạm vi Context cung cấp. Trả lời từ chối lịch sự nếu nội dung không thuộc cơ sở tri thức sự kiện. |
| **NFR-07** | **Khả năng kiểm thử (Testability)** | Độ bao phủ kiểm thử tự động (Pytest) đạt 100% cho các luồng nghiệp vụ: Đăng ký vé, Hạn ngạch Quota, Chống quét trùng QR, Phân quyền Ban tổ chức, Gửi thông báo và Sinh tóm tắt AI. |

---

## 5. Quy Tắc Nghiệp Vụ (Business Rules)
- **BR-01**: Mỗi sự kiện phải có ít nhất một hạng vé hợp lệ và lịch trình xác định trước khi mở đăng ký.
- **BR-02**: Một khách tham dự (`attendee`) chỉ được phép có 1 bản ghi đăng ký hợp lệ duy nhất cho mỗi sự kiện để tránh tình trạng giữ chỗ hàng loạt.
- **BR-03**: Khi số lượng vé bán ra (`sold_count`) chạm hạn ngạch (`quota`), hạng vé phải tự động khóa đăng ký (`sold_out`).
- **BR-04**: Khi người dùng hủy vé trước giờ khai mạc, hạn ngạch `sold_count` phải được hoàn trả lại ngay lập tức cho cộng đồng.
- **BR-05**: Mỗi mã vé QR chỉ được phép Check-in duy nhất một lần. Mọi thao tác quét lại sau đó đều bị chặn và trả về cảnh báo vi phạm (HTTP 409 Conflict).
- **BR-06**: Tài khoản `admin` có toàn quyền hệ thống; Tài khoản `organizer` quản lý sự kiện, vé, diễn giả, lịch trình, thông báo và xem phân tích ý kiến; Tài khoản `staff` chỉ được sử dụng chức năng quét vé Check-in.
- **BR-07**: Khách tham dự chỉ có thể gửi đánh giá phản hồi sau khi đã check-in hoặc khi sự kiện đã diễn ra.
- **BR-08**: Khi sử dụng AI sinh bản thảo email hoặc tóm tắt phản hồi, hệ thống chỉ gửi dữ liệu ngữ cảnh sự kiện và nội dung ẩn danh, cấm đưa danh sách email/sđt người dùng vào Prompt của LLM.
