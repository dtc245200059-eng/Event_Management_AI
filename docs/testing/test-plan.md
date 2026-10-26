# KẾ HOẠCH KIỂM THỬ TOÀN DIỆN HỆ THỐNG (SYSTEM TEST PLAN)
**Mã tài liệu:** TST-PLAN-2026-001  
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Phương pháp:** AI-Augmented SDLC Automated Test Strategy  
**Ngày lập:** 27/10/2026  
**Trạng thái phê duyệt:** ĐÃ PHÊ DUYỆT (APPROVED)  

---

## 1. Mục Tiêu & Phạm Vi Kiểm Thử (Objectives & Scope)

### 1.1. Mục Tiêu
- Đảm bảo 100% các yêu cầu nghiệp vụ cốt lõi và 5 workstreams mở rộng của Giảng viên hướng dẫn hoạt động chính xác, tin cậy và an toàn.
- Ngăn chặn hoàn toàn hiện tượng bán vé vượt hạn mức (Quota Overflow) và soát vé lặp lại (Duplicate Check-in).
- Triệt tiêu nguy cơ ảo giác (Hallucination), rò rỉ dữ liệu cá nhân (PII) và tấn công Prompt Injection đối với phân hệ Trí tuệ Nhân tạo.

### 1.2. Phạm Vi Kiểm Thử (Scope)
- **Tầng Xác thực & Phân quyền:** 4 vai trò (`Attendee`, `Organizer`, `CheckInStaff`, `Admin`).
- **Tầng Quản lý Sự kiện:** CRUD sự kiện, lịch trình (ràng buộc `start_at < end_at`), diễn giả, địa điểm.
- **Tầng Vé & Soát vé:** Đăng ký vé miễn phí, cấp mã QR, cập nhật giao dịch nguyên tử, từ chối vé đã dùng (HTTP 409).
- **Tầng Đánh giá & Phản hồi:** Thu thập đánh giá sao, tổng hợp phản hồi và phân tích cảm xúc.
- **Tầng AI & RAG:** Chuỗi RAG 8 bước kèm Step 8 Response Validation, soạn thảo email AI, tóm tắt ý kiến.

---

## 2. Chiến Lược Kiểm Thử 5 Cấp Độ (Multi-Level Test Strategy)

```
[ Cấp độ 1: Unit Testing (Đơn vị) ]
      └── Model validation, password hashing, time logic, PII sanitization regex
[ Cấp độ 2: Integration Testing (Tích hợp) ]
      └── Route-to-DB, Session-to-RBAC, Ticket-to-Checkin, Retrieval-to-RAG
[ Cấp độ 3: End-to-End Testing (Quy trình hoàn chỉnh) ]
      └── Kịch bản 12 bước: Đăng ký vé -> Nhận QR -> Check-in -> Thống kê -> Feedback -> AI
[ Cấp độ 4: Security Testing (An ninh mạng) ]
      └── OWASP Top 10 Web (SQLi, XSS, CSRF, IDOR) & OWASP Top 10 LLM (Injection, PII)
[ Cấp độ 5: Performance & Anti-Hallucination Testing ]
      └── Benchmark độ trễ, khả năng chịu tải, so sánh 3 chiến lược Prompt V1/V2/V3
```

---

## 3. Cấu Trúc Các Bộ Kiểm Thử Tự Động (Test Suites Structure)

| Suite File | Mục Tiêu Kiểm Thử | Số Lượng Tests | Ràng Buộc Nghiệp Vụ Cốt Lõi |
| :--- | :--- | :---: | :--- |
| `tests/test_auth.py` | Xác thực, băm mật khẩu, phân quyền | 7 | Mật khẩu băm PBKDF2, chặn attendee vào admin (403), quản lý role. |
| `tests/test_tickets_and_quota.py` | Đặt vé, quota, hủy vé, mã QR, check-in | 6 | Chống vượt quota, hoàn trả quota khi hủy, sinh QR SVG, chống check-in lặp. |
| `tests/test_notifications_and_feedback.py` | Hộp thư thông báo, gửi phản hồi | 4 | Organizer gửi thông báo theo phân khúc, tính điểm cảm xúc feedback. |
| `tests/test_ai_services.py` | RAG service, fallback, gợi ý, dự báo | 9 | Fallback offline dưới 20ms, phân tích intent, TF-IDF cosine recommender. |
| `tests/test_multi_agent.py` | Hệ thống đa tác tử, MessageBus, Critic | 10 | Giao thức MessageBus, Critic Guardrail chặn sự kiện giả, retry loop. |
| `tests/test_upgrade_requirements.py` | Các yêu cầu mở rộng mới của Giảng viên | 6 | Phân quyền CheckInStaff, start_at < end_at, check-in nguyên tử, Step 8 RAG. |

---

## 4. Tiêu Chuẩn Nghiệm Thu & Ngưỡng Chất Lượng (Quality Gates)
- **Tỷ lệ vượt qua (Pass Rate):** Bắt buộc **100.0% (42/42 Tests PASSED)**.
- **Tuyên bố không căn cứ (Hallucination Rate):** **0.0%** đối với Prompt V3.
- **Rò rỉ PII khách mời:** **0.0%** — Tuyệt đối không gửi email/sđt lên AI.
- **Độ trễ phản hồi API nội bộ:** **< 50 ms** trên môi trường kiểm thử.
