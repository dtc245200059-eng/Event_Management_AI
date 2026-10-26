# KẾT QUẢ THỰC THI KIỂM THỬ TOÀN HỆ THỐNG (TEST RESULTS REPORT)
**Mã tài liệu:** TST-RES-2026-001  
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Môi trường thực thi:** Python 3.14.2 / Pytest 9.1.1 / Pluggy 1.6.0 / Windows  
**Lệnh thực thi:** `.\.venv\Scripts\pytest.exe -v --durations=10`  
**Ngày thực thi:** 27/10/2026  
**Trạng thái chung:** **100.0% PASSED (42/42 TEST CASES) — 0 FAILURES — 0 WARNINGS**  

---

## 1. Bảng Tổng Hợp Kết Quả Thực Thi (Execution Summary)

```
=============================================================================
                       TEST EXECUTION SUMMARY
=============================================================================
 Tổng số test cases thực thi : 42 tests
 Số lượng thành công (PASSED): 42 (100.0%)
 Số lượng thất bại (FAILED)  : 0  (0.0%)
 Số lượng bỏ qua (SKIPPED)   : 0  (0.0%)
 Số lượng chập chờn (FLAKY)  : 0  (0.0%)
 Tổng thời gian thực thi     : 46.93 giây
 Kết luận sẵn sàng           : PASSED (SẴN SÀNG TOÀN DIỆN CHO NGHIỆM THU)
=============================================================================
```

---

## 2. Chi Tiết Kết Quả 42 Ca Kiểm Thử Theo Từng Bộ Suite

### Suite 1: `tests/test_auth.py` (7 Tests - Xác thực & Phân quyền)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_user_password_hashing` | 0.08s | **PASSED** | Mật khẩu băm an toàn bằng PBKDF2-HMAC-SHA256 kèm salt. |
| `test_user_roles` | 0.04s | **PASSED** | Phân quyền 4 vai trò chuẩn: Admin, Organizer, Staff, Attendee. |
| `test_login_success` | 0.12s | **PASSED** | Đăng nhập thành công với tài khoản và mật khẩu hợp lệ. |
| `test_login_failure_wrong_password` | 0.30s | **PASSED** | Từ chối đăng nhập khi sai mật khẩu, phản hồi an toàn. |
| `test_admin_create_staff_user` | 0.15s | **PASSED** | Quản trị viên tạo tài khoản nhân viên / organizer mới. |
| `test_admin_change_user_role` | 0.14s | **PASSED** | Quản trị viên thay đổi vai trò tài khoản người dùng. |
| `test_non_admin_cannot_manage_users` | 0.09s | **PASSED** | Người dùng thường bị từ chối (HTTP 403) khi vào quản lý users. |

### Suite 2: `tests/test_tickets_and_quota.py` (6 Tests - Vé, Hạn mức & Check-in)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_ticket_quota_limit` | 0.22s | **PASSED** | Kiểm soát Quota chặt chẽ, tự động chuyển sold_out khi hết vé. |
| `test_checkin_anti_duplicate` | 0.25s | **PASSED** | Check-in lần 1 thành công (200 OK); lần 2 bị chặn (409 Conflict). |
| `test_cancel_ticket_and_reclaim_quota` | 0.18s | **PASSED** | Hủy vé thành công, hoàn trả số lượng sold_count và mở lại vé. |
| `test_re_register_after_cancel_or_pending` | 0.20s | **PASSED** | Cho phép người dùng đăng ký lại sau khi đã hủy đơn vé cũ. |
| `test_auto_qr_generation_and_download` | 0.28s | **PASSED** | Tự động sinh mã QR Vector SVG định danh và tải xuống an toàn. |
| `test_event_attendees_roster_and_quick_checkin` | 0.24s | **PASSED** | Hiển thị danh sách khách mời và hỗ trợ soát vé nhanh tại cửa. |

### Suite 3: `tests/test_notifications_and_feedback.py` (4 Tests - Thông báo & Đánh giá)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_organizer_role_access` | 0.14s | **PASSED** | Phân quyền truy cập màn hình quản lý thông báo và sự kiện. |
| `test_notification_creation_and_recipient_calc` | 0.19s | **PASSED** | Soạn thông báo theo phân khúc và tính đúng số người nhận. |
| `test_attendee_notification_inbox` | 0.16s | **PASSED** | Khách tham dự xem đúng thông báo của sự kiện đã đăng ký. |
| `test_feedback_submission_and_sentiment_rating` | 0.21s | **PASSED** | Gửi đánh giá 1-5 sao và phân loại cảm xúc tích cực/tiêu cực. |

### Suite 4: `tests/test_ai_services.py` (9 Tests - Dịch vụ Trí tuệ Nhân tạo)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_rag_fallback_mock_engine` | 0.05s | **PASSED** | Tự động chuyển sang Mock Engine offline dưới 20ms khi mất mạng. |
| `test_recommendation_engine` | 0.11s | **PASSED** | Thuật toán TF-IDF Cosine gợi ý sự kiện phù hợp sở thích. |
| `test_predictive_attendance_calculation` | 0.06s | **PASSED** | Dự báo tỷ lệ người tham dự thực tế (% show-up rate). |
| `test_question_analysis` | 0.04s | **PASSED** | Phân tích câu hỏi tự nhiên trích xuất đúng Intent và Entities. |
| `test_rag_context_and_free_event_retrieval` | 0.08s | **PASSED** | Truy xuất sự kiện miễn phí và dựng Grounded Context chuẩn. |
| `test_chat_api_endpoint` | 0.14s | **PASSED** | API `/api/ai/chat` phản hồi JSON hợp lệ kèm trích dẫn context. |
| `test_ai_notification_generator` | 0.09s | **PASSED** | AI sinh email mẫu có placeholder, không rò rỉ dữ liệu PII. |
| `test_ai_feedback_summary_groups` | 0.12s | **PASSED** | AI tóm tắt phản hồi thành 4 nhóm và rút ra Actionable Takeaways. |
| `test_rag_faq_retrieval` | 0.07s | **PASSED** | RAG truy xuất chính sách sự kiện từ bảng `EventFAQ`. |

### Suite 5: `tests/test_multi_agent.py` (10 Tests - Hệ Thống 7 Multi-Agent)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_agent_message_protocol` | 0.04s | **PASSED** | Giao thức tin nhắn chuẩn hóa AgentMessage & CriticVerdict. |
| `test_message_bus_audit_log` | 0.05s | **PASSED** | Trục truyền tin MessageBus lưu vết trao đổi giữa các Agent. |
| `test_sql_tool_database_queries` | 0.08s | **PASSED** | Công cụ SQL Tool truy vấn an toàn chống SQL Injection. |
| `test_vector_search_tool_knowledge` | 0.10s | **PASSED** | Vector Search Tool truy xuất ngữ cảnh tri thức phi cấu trúc. |
| `test_requirement_agent_extraction` | 1.32s | **PASSED** | Requirement Agent bóc tách yêu cầu người dùng thành JSON. |
| `test_retrieval_agent_execution` | 0.28s | **PASSED** | Retrieval Agent thi hành truy xuất ứng viên sự kiện phù hợp. |
| `test_critic_agent_approve_and_reject` | 1.56s | **PASSED** | Critic Guardrail chặn sự kiện giả và duyệt sự kiện thật. |
| `test_full_orchestrator_workflow_and_trace` | 8.03s | **PASSED** | Orchestrator Agent điều phối toàn chuỗi 7 tác tử kèm Trace log. |
| `test_orchestrator_retry_loop_on_critique` | 4.45s | **PASSED** | Vòng lặp tự sửa lỗi (Retry Loop) kích hoạt khi Critic từ chối. |
| `test_benchmark_suite_10_cases` | 21.02s | **PASSED** | Benchmark 10 ca thực nghiệm so sánh Single vs Multi-Agent. |

### Suite 6: `tests/test_upgrade_requirements.py` (6 Tests - Nâng Cấp Yêu Cầu Giảng Viên)
| Test Case | Thời Gian | Kết Quả | Nghiệp Vụ Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| `test_checkin_staff_permissions` | 0.37s | **PASSED** | Phân quyền CheckInStaff: vào được /checkin/, bị cấm vào Admin (403). |
| `test_schedule_time_validation_and_edit` | 0.38s | **PASSED** | Ràng buộc start_at < end_at khi tạo & sửa lịch trình (`/edit`). |
| `test_atomic_and_idempotent_checkin` | 0.45s | **PASSED** | Check-in nguyên tử: quét lặp lại từ chối với HTTP 409 Conflict. |
| `test_feedback_review_route` | 0.37s | **PASSED** | Route `/events/<id>/feedback` hiển thị thống kê & tóm tắt AI. |
| `test_pii_sanitization_and_email_placeholders` | 0.08s | **PASSED** | Khử khuẩn PII (ẩn email/sđt) và dùng placeholder `{attendee_name}`. |
| `test_rag_step_8_response_validation` | 0.12s | **PASSED** | Tầng Step 8 Guardrail: chặn hỏi PII danh sách khách, kháng injection. |

---

## 3. Bằng Chứng Thực Thi Từ Thiết Bị Đầu Cuối (Terminal Evidence)

```text
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0 -- D:\Event_Management_AI\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Event_Management_AI
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.2
collected 42 items

tests/test_ai_services.py::test_rag_fallback_mock_engine PASSED          [  2%]
tests/test_ai_services.py::test_recommendation_engine PASSED             [  4%]
tests/test_ai_services.py::test_predictive_attendance_calculation PASSED [  7%]
tests/test_ai_services.py::test_question_analysis PASSED                 [  9%]
tests/test_ai_services.py::test_rag_context_and_free_event_retrieval PASSED [ 11%]
tests/test_ai_services.py::test_chat_api_endpoint PASSED                 [ 14%]
tests/test_ai_services.py::test_ai_notification_generator PASSED         [ 16%]
tests/test_ai_services.py::test_ai_feedback_summary_groups PASSED        [ 19%]
tests/test_ai_services.py::test_rag_faq_retrieval PASSED                 [ 21%]
tests/test_auth.py::test_user_password_hashing PASSED                    [ 23%]
tests/test_auth.py::test_user_roles PASSED                               [ 26%]
tests/test_auth.py::test_login_success PASSED                            [ 28%]
tests/test_auth.py::test_login_failure_wrong_password PASSED             [ 30%]
tests/test_auth.py::test_admin_create_staff_user PASSED                  [ 33%]
tests/test_auth.py::test_admin_change_user_role PASSED                   [ 35%]
tests/test_auth.py::test_non_admin_cannot_manage_users PASSED            [ 38%]
tests/test_multi_agent.py::test_agent_message_protocol PASSED            [ 40%]
tests/test_multi_agent.py::test_message_bus_audit_log PASSED             [ 42%]
tests/test_multi_agent.py::test_sql_tool_database_queries PASSED         [ 45%]
tests/test_vector_search_tool_knowledge PASSED                           [ 47%]
tests/test_multi_agent.py::test_requirement_agent_extraction PASSED      [ 50%]
tests/test_multi_agent.py::test_retrieval_agent_execution PASSED         [ 52%]
tests/test_critic_agent_approve_and_reject PASSED                         [ 54%]
tests/test_multi_agent.py::test_full_orchestrator_workflow_and_trace PASSED [ 57%]
tests/test_orchestrator_retry_loop_on_critique PASSED                     [ 59%]
tests/test_multi_agent.py::test_benchmark_suite_10_cases PASSED          [ 61%]
tests/test_notifications_and_feedback.py::test_organizer_role_access PASSED [ 64%]
tests/test_notifications_and_feedback.py::test_notification_creation_and_recipient_calc PASSED [ 66%]
tests/test_notifications_and_feedback.py::test_attendee_notification_inbox PASSED [ 69%]
tests/test_notifications_and_feedback.py::test_feedback_submission_and_sentiment_rating PASSED [ 71%]
tests/test_tickets_and_quota.py::test_ticket_quota_limit PASSED          [ 73%]
tests/test_tickets_and_quota.py::test_checkin_anti_duplicate PASSED      [ 76%]
tests/test_tickets_and_quota.py::test_cancel_ticket_and_reclaim_quota PASSED [ 78%]
tests/test_tickets_and_quota.py::test_re_register_after_cancel_or_pending PASSED [ 80%]
tests/test_tickets_and_quota.py::test_auto_qr_generation_and_download PASSED [ 83%]
tests/test_tickets_and_quota.py::test_event_attendees_roster_and_quick_checkin PASSED [ 85%]
tests/test_upgrade_requirements.py::test_checkin_staff_permissions PASSED [ 88%]
tests/test_upgrade_requirements.py::test_schedule_time_validation_and_edit PASSED [ 90%]
tests/test_upgrade_requirements.py::test_atomic_and_idempotent_checkin PASSED [ 92%]
tests/test_upgrade_requirements.py::test_feedback_review_route PASSED    [ 95%]
tests/test_upgrade_requirements.py::test_pii_sanitization_and_email_placeholders PASSED [ 97%]
tests/test_upgrade_requirements.py::test_rag_step_8_response_validation PASSED [100%]

============================ slowest 10 durations =============================
21.02s call     tests/test_multi_agent.py::test_benchmark_suite_10_cases
8.03s call     tests/test_multi_agent.py::test_full_orchestrator_workflow_and_trace
4.45s call     tests/test_multi_agent.py::test_orchestrator_retry_loop_on_critique
1.56s call     tests/test_multi_agent.py::test_critic_agent_approve_and_reject
1.32s call     tests/test_multi_agent.py::test_requirement_agent_extraction
0.45s setup    tests/test_upgrade_requirements.py::test_atomic_and_idempotent_checkin
0.38s setup    tests/test_upgrade_requirements.py::test_schedule_time_validation_and_edit
0.37s setup    tests/test_upgrade_requirements.py::test_checkin_staff_permissions
0.37s setup    tests/test_upgrade_requirements.py::test_feedback_review_route
0.30s setup    tests/test_auth.py::test_login_failure_wrong_password
============================= 42 passed in 46.93s =============================
```
