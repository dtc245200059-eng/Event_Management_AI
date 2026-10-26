# YÊU CẦU THAY ĐỔI PHẠM VI DỰ ÁN (SCOPE CHANGE REQUEST - SCR)
**Mã tài liệu:** SCR-2026-001  
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Người yêu cầu:** Giảng viên hướng dẫn (Th.S Nguyễn Đình Dũng, ICTU)  
**Nhóm thực hiện:** Nhóm 2 thành viên (Member 1: Front-end & Event Ops; Member 2: Data, Security & AI)  
**Ngày lập:** 27/10/2026  
**Trạng thái phê duyệt:** ĐÃ PHÊ DUYỆT (APPROVED)  

---

## 1. Bối cảnh và Lý do Thay đổi

Trong quá trình bảo vệ và nghiệm thu đồ án, Giảng viên hướng dẫn đã mở rộng các tiêu chí đánh giá và chuẩn đầu ra cho hệ thống EventAI Pro nhằm đáp ứng chuẩn công nghiệp và quy trình phát triển phần mềm có AI hỗ trợ (AI-Augmented SDLC). Các yêu cầu mới tập trung vào tính an toàn dữ liệu, kiểm soát truy cập đa vai trò chặt chẽ, chống trùng lặp vé trong điều kiện tranh chấp đồng thời, và đặc biệt là năng lực chống ảo giác (Anti-Hallucination) của mô hình ngôn ngữ lớn (LLM).

Nhóm cam kết tuân thủ quy tắc bảo toàn: nâng cấp tương thích ngược (Backward Compatibility), không đập đi xây lại các module đã hoàn thiện, không làm gián đoạn lịch sử Git, và kế thừa tối đa hệ thống giao diện chuẩn Apple Liquid Glass.

---

## 2. Bảng Phân Tích Phạm Vi Thay Đổi (Scope Delta Matrix)

| Workstream | Phạm vi Ban đầu (Baseline) | Phạm vi Mở rộng (Instructor Requirements) | Tác động Kỹ thuật & Giải pháp |
| :--- | :--- | :--- | :--- |
| **Task 1: Phân tích & Thiết kế** | Biểu đồ phân tán, chưa đồng bộ giữa các tác tử và mô hình dữ liệu thực tế. | Cập nhật bộ 8 biểu đồ PlantUML chuẩn: Use Case, ERD, Activity, Sequence, Class, Component, Deployment, Overall Architecture. | Hoàn thiện 100% mã nguồn `.puml` trong thư mục `docs/diagrams/`, đồng nhất 4 vai trò và 11 thực thể. |
| **Task 2A: Phân quyền RBAC** | 3 vai trò: `Attendee`, `Staff`, `Admin`. Chưa có vai trò CheckInStaff chuyên biệt. | 4 vai trò rõ ràng: `Attendee`, `Organizer`, `CheckInStaff`, `Admin`. Kế thừa `Staff` thành Organizer/CheckInStaff tương thích ngược. | Cập nhật `app/models/user.py`, bổ sung thuộc tính `@property is_checkin_staff` và `@property is_organizer`. Bổ sung decorator `@staff_required`. |
| **Task 2B & 2C: Lịch trình & Sự kiện** | CRUD sự kiện cơ bản, thêm phiên lịch trình chưa kiểm tra chặt chẽ giờ bắt đầu/kết thúc. | Xác thực chặt chẽ `start_at < end_at`, hỗ trợ endpoint sửa phiên (`/schedules/<id>/edit`), xóa phiên. | Bổ sung xác thực thời gian tại `app/routes/events.py` cho cả 2 thao tác Tạo và Sửa lịch trình. |
| **Task 2D & 2E: Vé & Check-in** | Check-in qua QR và mã vé nhưng chưa cam kết nguyên tử (atomic transaction) trên CSDL chia sẻ. | Check-in nguyên tử (Atomic / Idempotent), chống race condition khi quét đồng thời, hỗ trợ cả `ticket_number` và `registration_code`. | Thực thi `Registration.query.filter_by(id=..., checked_in=False).update(...)` trả về `rows_updated == 0` -> HTTP 409 từ chối vé đã dùng. |
| **Task 2F: Đánh giá & Phản hồi** | Lưu feedback của người tham dự nhưng chưa có trang tổng hợp chuyên biệt cho Organizer. | Endpoint `/events/<id>/feedback` hiển thị thống kê sao, cảm xúc, danh sách ý kiến và tóm tắt AI. | Tạo route chuyên biệt tại `app/routes/events.py` và template `app/templates/events/feedback_list.html`. |
| **Task 2G: Thống kê Dashboard** | Thống kê số lượng cơ bản, thiếu một số chỉ số định lượng. | Dashboard hiển thị đầy đủ 8 chỉ số thực: Tổng sự kiện, đăng ký, vé phát hành, check-in, tỷ lệ tham dự, sức chứa còn lại, số phản hồi, điểm TB. Có empty states. | Cập nhật truy vấn thực tế tại `app/routes/admin.py` và giao diện Apple Liquid Glass tại `app/templates/admin/dashboard.html`. |
| **Task 3.1: Soạn Email AI** | Tạo thông báo tự do, nguy cơ gửi email tự động và lộ dữ liệu PII. | 3 loại email (Mời, Nhắc nhở, Cảm ơn), bắt buộc dùng placeholder `{attendee_name}`, `{event_name}`, cấm gửi PII lên AI, bắt buộc phê duyệt bởi con người. | Cập nhật prompt `notification_generator.txt` và bộ lọc tại `gemini_service.py`. |
| **Task 3.2: Tóm tắt Phản hồi AI** | Phân tích cảm xúc TextBlob đơn giản. | Tóm tắt ý kiến định tính: Điểm khen ngợi lặp lại, khiếu nại phổ biến, lỗi tổ chức, kiến nghị cải tiến; lọc PII, cảnh báo mẫu nhỏ (<3). | Hiện thực hàm `sanitize_untrusted_feedback()` và `summarize_event_feedback_groups()` trong `sentiment_service.py`. |
| **Task 3.3: AI Chatbot Trợ lý** | RAG 7 bước, chưa có tầng kiểm duyệt Step 8 độc lập. | Chuỗi xử lý 8 bước có Step 8 Response Validation: lọc ảo giác, chặn PII, vô hiệu hóa Prompt Injection, phản hồi tiếng Việt chuẩn khi không tìm thấy. | Hiện thực `execute_8_step_rag()` và `validate_and_sanitize_response()` trong `rag_service.py`. |
| **Task 4: Đánh giá & So sánh Prompt** | Chưa có framework so sánh định lượng các phiên bản prompt. | Bộ benchmark 14 kịch bản thực nghiệm so sánh 3 chiến lược: V1 Basic, V2 Grounded, V3 Grounded + Validated. Lưu vào `ai-prompt-comparison.md`. | Xây dựng script `eval_prompts.py` và 3 file template prompt chuyên biệt. |
| **Task 5: Kế hoạch & Trách nhiệm Nhóm** | Chưa phân định chi tiết trách nhiệm theo từng luồng nghiệp vụ. | Ma trận phân công trách nhiệm 2 thành viên cụ thể, kịch bản demo 12 bước có thể tái lập 100%. | Lập bảng RACI Matrix và hướng dẫn thực thi trong tài liệu bàn giao. |

---

## 3. Đánh Giá Rủi Ro và Biện Pháp Kiểm Soát

1. **Rủi ro vỡ giao diện hệ thống:**
   - *Kiểm soát:* Nghiêm ngặt tuân thủ `AGENTS.md`, kế thừa CSS custom properties trong `app/static/css/style.css`, sử dụng đúng màu Apple Blue `#007AFF`.
2. **Rủi ro mất dữ liệu hoặc lỗi migration CSDL:**
   - *Kiểm soát:* Không xóa bảng hay cột hiện có; các thuộc tính RBAC được mở rộng thông qua các property helper trên model `User`.
3. **Rủi ro LLM timeout hoặc rò rỉ khóa API:**
   - *Kiểm soát:* Thiết lập `http_options={'timeout': 10000}`, cơ chế fallback deterministic Local Grounded Knowledge Engine hoạt động offline 100%, không bao giờ log API key hay dữ liệu người dùng.

---

## 4. Phê Duyệt và Ký Nhận
- **Đại diện Nhóm Phát Triển:** Member 1 & Member 2 — *Đã ký và cam kết thực hiện đúng tiến độ*.  
- **Giảng viên Hướng dẫn:** Th.S Nguyễn Đình Dũng — *Đã phê duyệt thông qua đề cương và yêu cầu kỹ thuật*.
