---
name: requirements-analysis
description: Skill chuyên môn hóa quy trình phân tích yêu cầu phần mềm, trích xuất điểm nghẽn nghiệp vụ, xây dựng User Stories, Acceptance Criteria, phát hiện mơ hồ và kiểm chứng chống Hallucination theo chuẩn AI-Augmented SDLC.
---

# Requirements Analysis Skill

## Objective
Chuyển đổi bài toán thực tế và yêu cầu kinh doanh của hệ thống quản lý sự kiện thành tài liệu đặc tả yêu cầu phần mềm (SRS), danh sách User Stories chi tiết, Acceptance Criteria có thể kiểm chứng độc lập và báo cáo phát hiện mơ hồ (Requirements Issues).

## Inputs
Đọc và phân tích các tài liệu nghiệp vụ:
- `docs/customer-requirement.md`
- `tailieu/Dự án hệ thống quản lý sự kiện có tích hợp AI (1).docx`
- `tailieu/1_Thuc_hanh_AI_Augmented_SDLC.docx`
- Yêu cầu của các bên liên quan (Stakeholders: Organizer, Staff, Attendee, Speaker, Sponsor)

## Process / Workflow
1. **Nhận diện Vấn đề & 4 Điểm Nghẽn Vận Hành**:
   - Điểm nghẽn 1: Phân mảnh thông tin sự kiện, diễn giả và tài nguyên phòng họp.
   - Điểm nghẽn 2: Đăng ký vé, thanh toán thiếu nhất quán và nguy cơ bán vượt quota (overselling).
   - Điểm nghẽn 3: Điểm nghẽn khu vực Check-in (soát vé thủ công chậm, rủi ro check-in trùng lặp).
   - Điểm nghẽn 4: Thiếu khả năng dự báo số lượng tham dự và không đo lường được cảm xúc phản hồi.
2. **Xác lập Phạm vi**: Phân định rõ `In-Scope` (8 modules quản lý + 4 modules AI) và `Out-of-Scope` (Cổng thanh toán quốc tế thực, phát hành vé cứng RFID, live streaming video).
3. **Trích xuất Actors & Use Cases**:
   - 3 nhóm tác nhân chính: `Admin (Quản trị viên)`, `Staff (Nhân viên soát vé)`, `Attendee (Người tham dự)`.
   - 8 Use Cases cốt lõi: Auth & RBAC (UC01), Event CRUD (UC02), Speaker & Schedule (UC03), Ticketing & Quotas (UC04), Payment Simulation (UC05), Check-in & Scanning (UC06), Feedback & Survey (UC07), User Management (UC08).
   - 4 Use Cases AI: RAG Chatbot Assistant (UC-AI-01), AI Event Description Generator (UC-AI-02), Event Recommendation (UC-AI-03), Attendance Prediction & Sentiment Analytics (UC-AI-04).
4. **Chuẩn hóa Danh mục Yêu cầu Chức năng (FR) & Phi Chức năng (NFR)**:
   - Gán ID duy nhất: `FR-01` đến `FR-08`, `FR-AI-01` đến `FR-AI-04`.
   - Gán ID duy nhất: `NFR-01` đến `NFR-09` (Performance, Security, Reliability, Usability, Data Integrity, Scalability, Portability, Maintainability, Anti-Hallucination).
5. **Xây dựng User Stories**:
   - Định dạng chuẩn: `As a <role>, I want <capability>, so that <benefit>`.
   - Gán mã truy vết: `US-ADM-xx`, `US-STF-xx`, `US-ATT-xx`, `US-AI-xx`.
6. **Xây dựng Acceptance Criteria (AC)**:
   - Định dạng chuẩn `Given - When - Then` cho tất cả các kịch bản bình thường (Happy path), biên (Boundary) và ngoại lệ (Exception).
7. **Phát hiện Mơ hồ (Ambiguity Detection) & Kiểm soát Hallucination**:
   - Liệt kê các điểm yêu cầu chưa rõ, các giả định kỹ thuật (Assumptions).
   - Rà soát chống AI tự bịa tính năng ngoài tài liệu (ví dụ: tự ý thêm cổng thanh toán PayPal quốc tế, thanh toán Crypto, v.v.).

## Rules & Constraints
- Tuyệt đối không viết mã nguồn (source code) trong pha này.
- Tuyệt đối không thiết kế CSDL hay kiến trúc hệ thống trong pha này.
- Không tự ý thêm tính năng không được yêu cầu trong tài liệu khách hàng.
- Mọi Acceptance Criteria phải đo lường hoặc kiểm thử tự động được (testable).
- Phải phân biệt rõ ràng giữa "Yêu cầu thực tế" và "Giả định kỹ thuật".

## Outputs
Khởi tạo hoặc cập nhật các tài liệu:
- `docs/customer-requirement.md`
- `docs/requirements.md`
- `docs/user-stories.md`
- `docs/acceptance-criteria.md`
- `docs/requirements-issues.md`

## Verification (Human Gate 1)
Người kiểm duyệt (Human Gatekeeper: Sinh viên / Kỹ sư / Giảng viên) kiểm tra và ký duyệt:
- [ ] Tất cả các yêu cầu chức năng (FR) đều có ID duy nhất.
- [ ] Tất cả các yêu cầu phi chức năng (NFR) đều có chỉ số đo lường cụ thể.
- [ ] 100% User Stories liên kết truy vết tới Functional Requirements.
- [ ] Mọi Acceptance Criteria đều tuân thủ chuẩn Given-When-Then và có thể kiểm thử.
- [ ] Biên bản `docs/requirements-issues.md` đã làm rõ các điểm mơ hồ và loại trừ AI Hallucination.
- **Trạng thái**: [APPROVED / REJECTED]
