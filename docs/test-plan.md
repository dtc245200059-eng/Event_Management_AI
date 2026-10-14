# Master Test Plan Specification

> **Dự Án:** Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Đã xây dựng và thực thi thành công 36/36 ca kiểm thử)  
> **Tài Liệu Tham Chiếu:** [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md), [user-stories.md](file:///d:/Event_Management_AI/docs/user-stories.md), [acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md), [test-report.md](file:///d:/Event_Management_AI/docs/test-report.md)  
> **Kỹ năng liên quan:** [testing](file:///d:/Event_Management_AI/.agents/skills/testing/SKILL.md), [ai-evaluation](file:///d:/Event_Management_AI/.agents/skills/ai-evaluation/SKILL.md)  
> **Framework Kiểm Thử:** Pytest 9.x + Flask Test Client + In-Memory SQLite  
> **Giai Đoạn:** Testing & Quality Assurance

---

## 1. Mục Tiêu & Chiến Lược Kiểm Thử (Testing Strategy)
Chiến lược kiểm thử phần mềm được thiết kế nhằm đảm bảo hệ thống đạt độ tin cậy tuyệt đối trước khi đưa vào vận hành thực tế. Trọng tâm kiểm thử hướng vào:
1. **Tính Đúng Đắn Nghiệp Vụ (Functional Verification)**: Xác thực các luồng đăng ký, mua vé, phân quyền và hiển thị lịch trình.
2. **Kiểm Soát Giao Dịch & Hạn Ngạch (Concurrency & Quota Integrity)**: Đảm bảo không xảy ra hiện tượng bán vượt quota (Zero Overselling).
3. **Phòng Chống Gian Lận Soát Vé (Fraud & Anti-Duplicate Check-in)**: Chặn đứng 100% các hành vi quét mã QR lặp lại.
4. **Độ Bền Vững & An Toàn AI (AI Resilience & Fallback)**: Đảm bảo phân hệ AI luôn phản hồi chính xác và có cơ chế Offline Fallback an toàn khi mất mạng.
5. **Kiểm Thử Đa Tác Tử & Đánh Giá Thực Nghiệm (Multi-Agent Benchmarking)**: Đánh giá định lượng 10 ca kiểm thử so sánh Single-Agent vs Multi-Agent.

---

## 2. Phạm Vi Kiểm Thử (Test Scope)

### 2.1. Trong Phạm Vi (In-Scope)
- **Unit Tests**: Kiểm thử các hàm tiện ích băm mật khẩu, tính toán tỷ lệ tham dự (% show-up), vector hóa TF-IDF và định dạng context.
- **Integration Tests**: Kiểm thử luồng gọi API đăng nhập, đặt vé qua DB transactions, hủy vé hoàn quota, quét mã QR check-in và gọi RAG AI.
- **Security Tests**: Kiểm thử phân quyền RBAC (Role-Based Access Control), thử nghiệm các cuộc tấn công quét vé lặp lại và nhập mật khẩu sai.
- **Failover / Resilience Tests**: Kiểm thử khả năng tự phục hồi của RAG Chatbot khi không có kết nối tới Google Gemini API.
- **Multi-Agent Benchmarking**: Thực nghiệm so sánh hiệu quả giữa Monolithic Single-Agent và 7-Agent Ensemble.

### 2.2. Ngoài Phạm Vi (Out-of-Scope)
- Kiểm thử tải hàng triệu người dùng đồng thời (Stress Testing) trên môi trường phân tán.
- Kiểm thử tương thích phần cứng máy quét mã vạch laser chuyên dụng.

---

## 3. Môi Trường & Công Cụ Kiểm Thử (Test Environment)
- **Hệ điều hành**: Windows 11 / Linux Ubuntu 22.04 LTS.
- **Ngôn ngữ & Môi trường**: Python 3.14+ (Virtual Environment `.venv`).
- **Framework kiểm thử**: `pytest`, `pytest-mock`, `anyio`.
- **Cơ sở dữ liệu kiểm thử**: SQLite In-Memory (`sqlite:///:memory:`) với cơ chế cô lập trạng thái giữa các bài test (`conftest.py`).

---

## 4. Danh Mục Ma Trận Kịch Bản Kiểm Thử (Test Scenarios Matrix)

| Test Suite | File Kiểm Thử | Số Lượng Tests | Trọng Tâm Nghiệp Vụ |
| :--- | :--- | :---: | :--- |
| **Auth & Security** | `tests/test_auth.py` | 7 Cases | Băm mật khẩu PBKDF2, phân quyền RBAC 4 vai trò, đăng nhập thành công, từ chối mật khẩu sai, admin quản trị user. |
| **Ticketing & Check-in** | `tests/test_tickets_and_quota.py` | 6 Cases | Giới hạn quota vé, chuyển `sold_out`, chặn check-in trùng (409 Conflict), hủy vé hoàn quota, đăng ký lại sau hủy, sinh mã QR. |
| **Notifications & Feedback** | `tests/test_notifications_and_feedback.py` | 4 Cases | Phân quyền truy cập Organizer, gửi thông báo theo phân khúc và tính số người nhận, hòm thư đến cá nhân, khảo sát & gán nhãn cảm xúc. |
| **AI Services & RAG** | `tests/test_ai_services.py` | 9 Cases | RAG Chatbot, Offline Fallback Mock Engine, TF-IDF recommendation, dự báo tham dự, phân tích intent/slots, soạn thảo email AI, tóm tắt phản hồi, FAQ retrieval. |
| **Multi-Agent Ensemble** | `tests/test_multi_agent.py` | 10 Cases | AgentMessage protocol, MessageBus audit trail, SQL/Vector Tools, Requirement/Retrieval/Critic Agents, Orchestrator flow, Retry loop, Benchmark 10 ca kiểm thử. |
| **Tổng Cộng** | **5 Test Files** | **36 Cases** | **Bao phủ 100% các Functional Requirements và Phân hệ AI.** |

---

## 5. Tiêu Chuẩn Đạt / Không Đạt (Pass / Fail Criteria)
- **Tiêu chuẩn PASS (Đạt)**:
  - 100% Test Cases trong bộ Test Suite phải có kết quả `PASSED`.
  - Không có bất kỳ lỗi Unhandled Exception hoặc Server Crash nào phát sinh.
  - Thời gian thực thi toàn bộ Test Suite < 30 giây.
- **Tiêu chuẩn FAIL (Không đạt)**:
  - Có ít nhất 1 Test Case bị `FAILED` hoặc `ERROR`.
  - Phát hiện lỗi bán vượt vé (overselling) hoặc quét mã QR trùng lặp vẫn trả về 200 OK.
  - Phân hệ RAG Chatbot ném lỗi 500 khi mất kết nối mạng thay vì kích hoạt Mock Engine.
