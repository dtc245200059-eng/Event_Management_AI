---
name: testing
description: Skill xây dựng chiến lược kiểm thử phần mềm tự động (Pytest), thiết lập Test Scenarios, Test Cases, Unit Tests, Integration Tests, Multi-Agent Benchmarks và xuất Test Report cùng bằng chứng thực thi.
---

# Automated Testing Skill

## 1. Purpose

Skill này hướng dẫn AI Agent thiết kế, triển khai, thực thi và bảo trì bộ kiểm thử tự động (Automated Test Suite) cho dự án `EventAI Pro`. Đảm bảo hệ thống đạt chuẩn chất lượng sản xuất thông qua kiểm thử toàn diện: Unit Tests, Integration Tests, API Contracts, Multi-Agent Workflows, RBAC Security Controls, Atomic Quota Limits và AI RAG Fallback, với mục tiêu đạt tỷ lệ pass 100% không có lỗi hồi quy (Regression).

## 2. Scope

- Quản trị cấu trúc kiểm thử trong thư mục [tests/](file:///d:/Event_Management_AI/tests/):
  - [conftest.py](file:///d:/Event_Management_AI/tests/conftest.py): Thiết lập test fixtures (`app`, `client`, `sample_users`, test db in-memory/temp).
  - [test_auth.py](file:///d:/Event_Management_AI/tests/test_auth.py): Kiểm thử băm mật khẩu PBKDF2, phân quyền 4 vai trò, session đăng nhập.
  - [test_tickets_and_quota.py](file:///d:/Event_Management_AI/tests/test_tickets_and_quota.py): Kiểm thử giới hạn quota vé, hoàn trả quota khi hủy, chống check-in trùng lặp (HTTP 409), sinh mã QR tự động.
  - [test_ai_services.py](file:///d:/Event_Management_AI/tests/test_ai_services.py): Kiểm thử RAG Dual-Engine, FAQ retrieval, gợi ý sự kiện, dự báo điểm danh, sinh thông báo AI.
  - [test_notifications_and_feedback.py](file:///d:/Event_Management_AI/tests/test_notifications_and_feedback.py): Kiểm thử hệ thống thông báo sự kiện, hòm thư người tham dự, đánh giá feedback và phân tích cảm xúc VADER.
  - [test_multi_agent.py](file:///d:/Event_Management_AI/tests/test_multi_agent.py): Kiểm thử giao thức AgentMessage, MessageBus audit log, SQL/Vector Tools, CriticAgent guardrail, Orchestrator loop, và bộ 10 ca kiểm thử benchmark.
- Thực thi kiểm thử tự động và thu thập bằng chứng thực nghiệm (Execution Evidence).
- Lập báo cáo kiểm thử [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md) đồng bộ với [docs/test-plan.md](file:///d:/Event_Management_AI/docs/test-plan.md).

## 3. Non-Scope

- Không trực tiếp sửa mã nguồn chức năng nghiệp vụ (thuộc skill `implementation`).
- Không thực hiện kiểm thử tải nặng (Load/Stress Testing hàng chục nghìn RPS phân tán).

## 4. When to Use

- Sau khi có bất kỳ thay đổi nào về mã nguồn trong `app/routes/`, `app/models/`, `app/services/` hoặc `app/agents/`.
- Khi cần tạo test case mới cho một Acceptance Criteria vừa được bổ sung.
- Trước khi đóng gói triển khai (Release Pre-flight Check).
- Khi điều tra nguyên nhân gốc rễ của một lỗi hồi quy.

## 5. When NOT to Use

- Khi yêu cầu ban đầu còn chưa rõ ràng (phải dùng `requirements-analysis`).
- Khi chỉ tạo tài liệu hướng dẫn sử dụng (dùng `documentation`).

## 6. Required Context

Agent cần nắm vững:

- Framework kiểm thử: Pytest 9.x kết hợp fixture Flask test client.
- Lệnh thực thi kiểm thử chuẩn của dự án:

  ```powershell
  .venv\Scripts\python -m pytest -v
  ```

  *(Luôn dùng `python -m pytest` để đảm bảo `PYTHONPATH` nhận diện đúng module `app` ở root)*.

- Hiện trạng bộ kiểm thử: **36 test cases** phân bổ trên 5 test files, tất cả đang ở trạng thái PASS 100%.
- Cơ chế Mocking: Khi kiểm thử AI, sử dụng Local Grounded Mock Engine để kiểm thử chạy ổn định, nhanh chóng và không phụ thuộc vào kết nối mạng ngoài hay quota API key.

## 7. Source Files to Inspect

Trước khi viết hoặc chạy kiểm thử, Agent PHẢI kiểm tra:

- [tests/conftest.py](file:///d:/Event_Management_AI/tests/conftest.py): Các fixtures dùng chung (`app`, `client`, `sample_users`).
- Tệp test tương ứng trong [tests/](file:///d:/Event_Management_AI/tests/).
- Tệp mã nguồn mục tiêu trong `app/routes/`, `app/models/`, `app/services/` để nắm rõ input/output và exception.
- [docs/test-plan.md](file:///d:/Event_Management_AI/docs/test-plan.md): Kế hoạch kiểm thử tổng thể.
- [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md): Báo cáo kết quả kiểm thử hiện tại.

## 8. Related Documentation

- [docs/test-plan.md](file:///d:/Event_Management_AI/docs/test-plan.md): Đặc tả kế hoạch kiểm thử Master.
- [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md): Báo cáo kết quả kiểm thử thực tế.
- [docs/acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md): Tiêu chí chấp nhận cần kiểm chứng.
- [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md): Ma trận truy vết Yêu cầu ↔ Test Cases.

## 9. Related Skills

- `requirements-analysis`: Cung cấp Acceptance Criteria (AC) làm tiêu chí kiểm thử.
- `implementation`: Cung cấp mã nguồn cần được kiểm chứng.
- `code-review`: Rà soát chất lượng của chính các test cases.
- `documentation`: Cập nhật kết quả vào báo cáo kiểm thử.

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Đọc yêu cầu và test fixtures)

1. Đọc Acceptance Criteria trong [docs/acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md).
2. Đọc [tests/conftest.py](file:///d:/Event_Management_AI/tests/conftest.py) để biết dữ liệu mẫu có sẵn (tài khoản admin, staff, user).
3. Đọc mã nguồn module cần kiểm thử để xác định các nhánh rẽ và điểm có thể lỗi.

### Bước 2: ANALYZE (Xác định kịch bản kiểm thử)

1. **Kiểm thử Luồng Chính (Happy Path)**: Dữ liệu hợp lệ, trả về status code 200 hoặc redirect 302, CSDL cập nhật chính xác.
2. **Kiểm thử Trường hợp Biên (Boundary / Edge Cases)**:
   - Đặt vé khi `quota == 0` (phải từ chối).
   - Check-in cùng một vé lần thứ hai (phải trả về HTTP 409 Conflict).
   - Truy vấn AI với câu hỏi rỗng hoặc chỉ có dấu cách (phải trả HTTP 400).
   - Huỷ vé đã thanh toán (phải hoàn trả lại số lượng vé khả dụng `sold_count -= 1`).
3. **Kiểm thử Bảo mật (Security & RBAC)**:
   - Truy cập trang Admin bằng tài khoản Attendee (phải trả về HTTP 403 Forbidden).
   - Điểm danh bằng tài khoản không có quyền Staff/Admin (phải bị chặn).

### Bước 3: PLAN (Thiết kế Test Case)

1. Đặt tên hàm test rõ ràng theo quy ước: `test_<chức_năng>_<điều_kiện>_<kết_quả_mong_đợi>`.
   Ví dụ: `test_checkin_anti_duplicate`, `test_cancel_ticket_and_reclaim_quota`.

2. Chuẩn bị dữ liệu đầu vào độc lập, không phụ thuộc vào thứ tự chạy của các test khác.

### Bước 4: MODIFY (Viết mã kiểm thử Pytest)

1. Soạn thảo mã kiểm thử trong tệp test tương ứng:

   ```python
   def test_example_scenario(client, sample_users):
       # 1. Arrange: Đăng nhập với vai trò phù hợp
       client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

       # 2. Act: Thực hiện hành động
       res = client.post('/tickets/register/1', data={'ticket_id': 1}, follow_redirects=True)

       # 3. Assert: Kiểm tra kết quả
       assert res.status_code == 200
       assert b'Thanh to\xc3\xa1n' in res.data or b'checkout' in res.data
   ```

### Bước 5: VERIFY (Chạy kiểm thử và thu thập bằng chứng)

1. Chạy tệp test vừa viết:

   ```powershell
   .venv\Scripts\python -m pytest tests/test_tickets_and_quota.py -v
   ```

2. Chạy toàn bộ test suite để đảm bảo không có bất kỳ regression nào:

   ```powershell
   .venv\Scripts\python -m pytest -v
   ```

3. Lưu lại log thực thi (stdout, số lượng tests passed, thời gian chạy).
4. Cập nhật kết quả vào [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md) và [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md).

## 11. Validation

Agent phải kiểm tra các tiêu chí sau:

- [ ] 100% test cases trong toàn bộ test suite đều PASS.
- [ ] Không có test case nào bị bỏ qua (`skip`) hoặc đánh dấu tạm thời mà không có lý do kỹ thuật.
- [ ] Không có assertion giả tạo (ví dụ: `assert True`).
- [ ] Mỗi test case đều xác minh cả HTTP status code lẫn sự biến đổi trạng thái trong CSDL.
- [ ] Số lượng test trong [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md) khớp chính xác với số test chạy qua `pytest`.

## 12. Failure Handling

Khi một test case bị FAIL, Agent áp dụng quy trình bắt buộc:
`FAILURE → TRACE ROOT CAUSE → CLASSIFY (TEST BUG vs PRODUCT BUG) → FIX → RE-RUN → VERIFY`.

- Nếu là **Product Bug**: Báo cáo nguyên nhân cho `implementation` hoặc khắc phục trực tiếp mã nguồn.
- Nếu là **Test Bug** (dữ liệu mock sai, assert nhầm): Căn chỉnh lại test case cho đúng với đặc tả AC.
- Tuyệt đối KHÔNG xóa test case hoặc nới lỏng điều kiện assertion để test pass giả tạo!

## 13. Security Considerations

- Test suite phải kiểm tra xác nhận mật khẩu không bao giờ được lưu plain text.
- Phải kiểm chứng decorator `@role_required` từ chối các yêu cầu trái phép với mã lỗi 403.
- Kiểm tra tính an toàn của token hoặc session khi người dùng đăng xuất (`/auth/logout`).

## 14. Expected Output

1. Tệp test hoàn chỉnh, tuân thủ convention trong thư mục `tests/`.
2. Nhật ký thực thi Pytest ghi nhận 100% test cases passed.
3. Báo cáo kiểm thử cập nhật trong [docs/test-report.md](file:///d:/Event_Management_AI/docs/test-report.md).
4. Ma trận truy vết cập nhật trong [docs/traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md).

## 15. Completion Criteria

- Mọi AC của tính năng đều có ít nhất 1 test case tự động kiểm chứng.
- Bộ kiểm thử 36/36 tests (hoặc nhiều hơn) pass sạch sẽ trong thời gian chấp nhận được (< 60s).
- Không xuất hiện cảnh báo `LegacyAPIWarning` hay lỗi unhandled exception.

## 16. Maintenance Notes

- Cập nhật skill này khi bổ sung công cụ kiểm thử mới (ví dụ: Playwright cho Frontend E2E testing).
- Khi thêm bảng CSDL mới, luôn bổ sung test case kiểm tra quan hệ khóa ngoại và cascade delete vào test suite.
