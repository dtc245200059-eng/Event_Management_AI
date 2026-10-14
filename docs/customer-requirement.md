# Customer Requirement Document (CRD)

> **Dự Án:** Hệ Thống Quản Lý Sự Kiện Có Tích Hợp Trí Tuệ Nhân Tạo (AI-Powered Event Management System)  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Đã thỏa mãn đầy đủ 4 điểm nghẽn và KPIs)  
> **Khách Hàng / Đơn Vị Yêu Cầu:** Ban Tổ Chức Hội Nghị & Sự Kiện Công Nghệ  
> **Ngày Lập:** Tháng 10/2026 (Phiên bản đồng bộ 3.1)  
> **Tài Liệu Tham Chiếu:** [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md), [user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md), [acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md), [traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md)  
> **Kỹ năng liên quan:** [requirements-analysis](file:///d:/Event_Management_AI/.agents/skills/requirements-analysis/SKILL.md)  
> **Phương Pháp Luận:** AI-Augmented Software Development Life Cycle (AI-Augmented SDLC)

---

## 1. Bối Cảnh & Tính Cấp Thiết
Trong kỷ nguyên số hóa, các sự kiện quy mô vừa và lớn (từ vài trăm đến hàng ngàn người tham dự) thường xuyên đối mặt với những khó khăn nghiêm trọng trong công tác tổ chức, điều phối và chăm sóc khách hàng. Ban tổ chức nhận thấy các quy trình thủ công truyền thống gây tốn kém nhân lực, dễ xảy ra sai sót và không mang lại trải nghiệm tốt cho người tham gia.

Khách hàng yêu cầu xây dựng một **Nền tảng Quản lý Sự kiện Thông minh** kết hợp sức mạnh của **Trí tuệ nhân tạo (AI/LLM)** nhằm tự động hóa toàn diện từ khâu lập kế hoạch, phát hành vé, soát vé đến phân tích sau sự kiện.

---

## 2. Nhận Diện 4 Điểm Nghẽn Vận Hành Cốt Lõi

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   4 ĐIỂM NGHẼN VẬN HÀNH SỰ KIỆN TRUYỀN THỐNG             │
├───────────────────────────────┬──────────────────────────────────────────┤
│ 1. Phân mảnh Thông tin        │ 2. Đăng ký & Bán vé Thiếu Kiểm soát      │
│ - Lịch trình, diễn giả phân   │ - Dễ bán vượt số lượng vé (overselling). │
│   tán qua file PDF, email.    │ - Mất dấu giao dịch & lịch sử vé.        │
│ - Người tham gia khó tra cứu. │ - Rủi ro tranh chấp khi check-in.        │
├───────────────────────────────┼──────────────────────────────────────────┤
│ 3. Ùn tắc Khu vực Check-in    │ 4. Thiếu Dự báo & Thấu hiểu Phản hồi     │
│ - Kiểm soát vé giấy chậm chạp.│ - Không ước lượng được tỷ lệ vắng mặt.   │
│ - Nguy cơ gian lận vé photo   │ - Khó đọc hàng trăm nhận xét rời rạc     │
│   hoặc check-in trùng lặp.    │   sau sự kiện để rút kinh nghiệm.        │
└───────────────────────────────┴──────────────────────────────────────────┘
```

### 2.1. Điểm nghẽn 1: Phân mảnh thông tin sự kiện & tài nguyên
- **Thực trạng**: Thông tin về phiên hội thảo, diễn giả, phòng họp và hạng vé bị phân tán qua nhiều kênh (file PDF, email, mạng xã hội).
- **Yêu cầu**: Cung cấp một cổng thông tin tập trung (Single Source of Truth) kết hợp Trợ lý ảo AI có khả năng giải đáp mọi câu hỏi 24/7 tức thì.

### 2.2. Điểm nghẽn 2: Đăng ký, phát hành vé và thanh toán thiếu nhất quán
- **Thực trạng**: Khi lượng truy cập tăng đột biến, hệ thống cũ thường bị bán vượt quota (overselling) hoặc người dùng bị trùng lặp đơn đăng ký.
- **Yêu cầu**: Kiểm soát số lượng vé theo hạn ngạch thời gian thực với cơ chế Transaction an toàn, tự động khóa khi hết vé và cấp phát mã vé độc nhất.

### 2.3. Điểm nghẽn 3: Điểm nghẽn tại khu vực Check-in
- **Thực trạng**: Soát vé thủ công mất từ 45 - 90 giây/người, dễ xảy ra tình trạng mang 1 vé photo ra check-in nhiều lần.
- **Yêu cầu**: Phát hành mã QR vector định danh cho từng vé, hỗ trợ nhân viên quét mã trực tiếp bằng Camera Web với tốc độ xử lý dưới 500ms và tự động chặn vé đã quét (Anti-duplicate check-in).

### 2.4. Điểm nghẽn 4: Thiếu khả năng dự báo & hiểu phản hồi
- **Thực trạng**: Ban tổ chức không ước lượng được tỷ lệ người đăng ký nhưng không đến (% no-show) dẫn đến lãng phí phòng tiệc, tài liệu; đồng thời khó tổng hợp cảm xúc của hàng ngàn phản hồi.
- **Yêu cầu**: Tích hợp thuật toán học máy dự báo số lượng người tham dự thực tế (% show-up rate) và AI tự động phân tích cảm xúc (Sentiment Analysis) từ các bài khảo sát.

---

## 3. Mục Tiêu Dự Án & KPIs (SMART Goals)
1. **Rút ngắn thời gian tra cứu thông tin**: Giảm 85% thời gian tìm kiếm lịch trình và diễn giả thông qua AI RAG Chatbot.
2. **Loại bỏ hoàn toàn lỗi bán vượt vé (Zero Overselling)**: 100% giao dịch đặt vé được bảo vệ bởi Database Transactions.
3. **Tối ưu tốc độ Check-in**: Giảm thời gian soát vé xuống < 2 giây/người, tỷ lệ ngăn chặn vé giả/trùng lặp đạt 100%.
4. **Độ sẵn sàng cao (High Availability)**: Tích hợp cơ chế Fallback Mock giúp hệ thống AI luôn phản hồi ngay cả khi mất kết nối Internet hoặc lỗi Gemini API Key.

---

## 4. Các Bên Liên Quan (Stakeholders) & Ma Trận RACI

| Stakeholder | Vai trò & Trách nhiệm | R | A | C | I |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ban Tổ Chức (Organizer / Admin)** | Quản lý toàn diện sự kiện, diễn giả, phát hành vé và xem báo cáo phân tích. | **R** | **A** | | |
| **Nhân Viên Soát Vé (Staff)** | Vận hành máy quét mã QR, xác thực vé tại cổng sự kiện. | **R** | | | **I** |
| **Người Tham Dự (Attendee)** | Đăng ký tài khoản, tìm kiếm sự kiện, đặt vé, nhận mã QR và hỏi đáp AI. | | | **C** | **I** |
| **Diễn Giả (Speaker)** | Trình bày các phiên hội thảo theo lịch trình đã sắp xếp. | | | **I** | **I** |
| **Đội Ngũ Kỹ Thuật (Tech Team)** | Phát triển, kiểm thử, triển khai và bảo trì hệ thống AI-Augmented SDLC. | **R** | **A** | | |

*Ghi chú: R = Responsible (Thực hiện), A = Accountable (Chịu trách nhiệm chính), C = Consulted (Tham vấn), I = Informed (Nhận thông tin).*

---

## 5. Ràng Buộc Kỹ Thuật & Công Nghệ
- **Backend**: Python 3.10+, Flask Framework (Blueprint Pattern), SQLAlchemy ORM.
- **Frontend**: HTML5/CSS3 chuẩn hiện đại Glassmorphism, Vanilla JavaScript AJAX/Fetch API, Chart.js, HTML5-QRCode Scanner.
- **Cơ sở dữ liệu**: SQLite (Development / Testing) và MySQL/PostgreSQL (Production).
- **AI & Machine Learning**: Google Gemini 2.0 Flash API, TF-IDF + Cosine Similarity cho Recommendation, Linear Regression cho Dự báo tham dự.
- **Bảo mật**: Chuẩn OWASP Top 10, PBKDF2 Password Hashing, lưu secrets trong file `.env`, chống lộ dữ liệu PII.
