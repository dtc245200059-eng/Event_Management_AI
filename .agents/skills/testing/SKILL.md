---
name: testing
description: Skill xây dựng chiến lược kiểm thử phần mềm tự động (Pytest), thiết lập Test Scenarios, Test Cases, Unit Tests, Integration Tests và xuất Test Report cùng bằng chứng thực thi.
---

# Testing Skill

## Objective
Thiết lập và thực thi tự động chiến lược kiểm thử phần mềm toàn diện, xác thực các yêu cầu chức năng, phi chức năng, kịch bản biên, phòng chống bán vé vượt quota, kiểm soát chống check-in trùng và kiểm thử độ tin cậy của các dịch vụ AI.

## Inputs
Đọc các tài liệu:
- `docs/requirements.md`
- `docs/user-stories.md`
- `docs/acceptance-criteria.md`
- `docs/database-design.md`

## Process / Workflow
1. **Xây dựng Kế hoạch Kiểm thử (Test Plan)**:
   - Xác định phạm vi kiểm thử (Scope), môi trường thử nghiệm (In-Memory SQLite / Test DB), ma trận rủi ro.
2. **Thiết kế Test Scenarios & Test Cases**:
   - Mỗi ca kiểm thử có `Test ID`, `Module`, `Description`, `Pre-conditions`, `Input Steps`, `Expected Output`, `Traceability FR/US`.
   - Bao phủ các kịch bản:
     - Auth: Băm mật khẩu PBKDF2, đăng nhập hợp lệ, từ chối mật khẩu sai, phân quyền 3 roles.
     - Tickets & Quotas: Giới hạn quota, hết vé chuyển `sold_out`, hủy vé hoàn quota, cập nhật trạng thái đồng thời.
     - Check-in: Quét vé hợp lệ lần 1 (200 OK), phát hiện và chặn quét vé lần 2 (409 Conflict - Duplicate check-in).
     - AI Services: RAG Chatbot fallback an toàn khi mất mạng/lỗi API, gợi ý sự kiện (TF-IDF), dự báo tỷ lệ tham dự (% show-up).
3. **Hiện thực hóa Automated Tests với Pytest**:
   - `tests/conftest.py`: Fixtures khởi tạo test app, in-memory database và người dùng mẫu.
   - `tests/test_auth.py`: Kiểm thử Unit & Integration cho module xác thực và RBAC.
   - `tests/test_tickets_and_quota.py`: Kiểm thử mua vé, kiểm soát quota và quét mã QR check-in.
   - `tests/test_ai_services.py`: Kiểm thử RAG Fallback Mock, Recommendation, Predictive Analytics.
4. **Thực thi Kiểm thử & Thu thập Bằng chứng**:
   - Chạy lệnh: `.venv\Scripts\python.exe -m pytest -v`.
   - Ghi nhận thời gian thực thi, số lượng test case Passed/Failed/Skipped.
5. **Đánh giá Độ bao phủ Yêu cầu (Requirements Coverage)**:
   - Đo lường mức độ bao phủ của bộ test so với danh sách Functional Requirements (FR-01..FR-08, FR-AI-01..FR-AI-04).
6. **Lập Báo cáo Kết quả Kiểm thử (Test Report)**.

## Rules & Constraints
- **Quy tắc Vàng**: TUYỆT ĐỐI KHÔNG BAO GIỜ sửa đổi mã kiểm thử (tests) chỉ nhằm mục đích làm cho test pass một cách giả tạo!
- Mọi bài test phải có tính Độc lập (Test Isolation) và Không phụ thuộc trạng thái (Stateless).

## Outputs
Khởi tạo hoặc cập nhật:
- `docs/test-plan.md`
- `docs/test-report.md`
- Toàn bộ test suite trong thư mục `tests/`

## Verification
- 100% test cases trong Test Suite đạt kết quả `PASSED`.
- Báo cáo `docs/test-report.md` chứa đầy đủ bằng chứng thực thi thực tế.
