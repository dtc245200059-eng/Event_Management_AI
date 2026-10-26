# NHẬT KÝ LỜI NHẮC AI-AUGMENTED SDLC (PROMPT LOG)
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Phương pháp luận:** AI-Augmented Software Development Life Cycle (AI-Augmented SDLC)  
**Quy tắc an ninh:** Tuyệt đối không lưu trữ API Key, mật khẩu, thông tin liên lạc (PII) hoặc dữ liệu nhạy cảm của khách hàng trong nhật ký.  
**Ngày lập:** 27/10/2026  

---

## 1. Nguyên Tắc Quản Trị Prompt Trong Quy Trình Phát Triển

Mỗi tác vụ phát triển trong dự án được hướng dẫn thông qua các Skill chuyên trách (`.agents/skills/`), thực thi qua lời nhắc có cấu trúc 5 thành phần (Instructions, Context, Constraints, Few-shot Examples, Output Format), và bắt buộc trải qua cổng thẩm định con người (Human Verification Gate) trước khi tích hợp vào nhánh mã nguồn chính.

---

## 2. Bảng Nhật Ký Thực Thi Chi Tiết (Traceable Prompt Log)

### Tác Vụ 1: Phân Tích Khoảng Trống Yêu Cầu (Gap Analysis)
- **ID Lời nhắc:** PRM-2026-001  
- **Tác vụ:** Rà soát hiện trạng mã nguồn, đối chiếu 5 luồng yêu cầu mở rộng của Giảng viên hướng dẫn.  
- **Skill sử dụng:** `requirements-analysis`, `code-review`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Phân tích cấu trúc thư mục hiện tại của EventAI Pro, kiểm tra các model, route và skill. Đối chiếu với 5 nhóm yêu cầu mở rộng: 4 vai trò RBAC, check-in nguyên tử, validation lịch trình, AI email drafts với placeholder, AI feedback summarization, 8-step RAG chatbot và benchmark 3 phiên bản prompt. Xuất báo cáo docs/upgrade-gap-analysis.md."*  
- **Tệp thay đổi / Tạo mới:** `docs/upgrade-gap-analysis.md`  
- **Đầu ra AI:** Tài liệu phân tích khoảng trống 24KB bao gồm kiến trúc hiện tại, khoảng trống chức năng, đánh giá an ninh và lộ trình 7 giai đoạn.  
- **Kết quả Kiểm thử / Thẩm định:** Con người xác nhận phân tích chính xác, không ghi đè module đang chạy tốt.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

### Tác Vụ 2: Cập Nhật Bộ Biểu Đồ Thiết Kế Hệ Thống PlantUML
- **ID Lời nhắc:** PRM-2026-002  
- **Tác vụ:** Thiết kế và chuẩn hóa 8 biểu đồ PlantUML mô tả chính xác 4 vai trò nghiệp vụ, 11 thực thể CSDL và chuỗi xử lý RAG 8 bước.  
- **Skill sử dụng:** `architecture-design`, `database-design`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Tạo 8 biểu đồ PlantUML hoàn chỉnh trong docs/diagrams/: use_case_diagram.puml (4 vai trò: Attendee, Organizer, CheckInStaff, Admin), erd_diagram.puml (11 thực thể có PK-FK và Index), activity_checkin_flow.puml (check-in nguyên tử chống quét lặp), activity_feedback_flow.puml (tổng hợp feedback và AI tóm tắt), seq_rag_chat_8_steps.puml (luồng RAG 8 bước kèm Guardrail Step 8), seq_ticket_registration_checkin.puml, class_diagram.puml, component_diagram.puml, deployment_diagram.puml và overall_architecture.puml."*  
- **Tệp thay đổi / Tạo mới:** Toàn bộ 10 tệp trong `docs/diagrams/`.  
- **Đầu ra AI:** Bộ mã nguồn PlantUML chuẩn, nhất quán 100% giữa các thực thể và quy tắc nghiệp vụ.  
- **Kết quả Kiểm thử / Thẩm định:** Kiểm tra cú pháp PlantUML hợp lệ, không có mâu thuẫn giữa các tác nhân.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

### Tác Vụ 3: Bổ Sung 6 Domain Skills Cho Hệ Thống AI Agent
- **ID Lời nhắc:** PRM-2026-003  
- **Tác vụ:** Tạo 6 Skill nghiệp vụ mới theo định dạng `SKILL.md` để hướng dẫn AI Agent trong vòng đời phát triển.  
- **Skill sử dụng:** `ai-agent`, `agy-customizations`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Tạo 6 thư mục Skill trong .agents/skills/: event-question-analysis, event-context-builder, event-prompt-builder, event-answering, event-feedback-analysis, event-email-generation. Mỗi SKILL.md phải có YAML frontmatter chuẩn, mô tả mục tiêu, đầu vào, quy trình từng bước, nguyên tắc chống ảo giác và tiêu chí nghiệm thu."*  
- **Tệp thay đổi / Tạo mới:**  
  - `.agents/skills/event-question-analysis/SKILL.md`  
  - `.agents/skills/event-context-builder/SKILL.md`  
  - `.agents/skills/event-prompt-builder/SKILL.md`  
  - `.agents/skills/event-answering/SKILL.md`  
  - `.agents/skills/event-feedback-analysis/SKILL.md`  
  - `.agents/skills/event-email-generation/SKILL.md`  
- **Đầu ra AI:** 6 tài liệu hướng dẫn kỹ thuật chuẩn hóa, phân định rõ ràng giữa hướng dẫn phát triển AI Agent và logic ứng dụng triển khai.  
- **Kết quả Kiểm thử / Thẩm định:** Đã kiểm tra metadata YAML và đường dẫn liên kết.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

### Tác Vụ 4: Nâng Cấp Logic Check-in Nguyên Tử, RBAC và Endpoint Lịch Trình
- **ID Lời nhắc:** PRM-2026-004  
- **Tác vụ:** Nâng cấp backend hỗ trợ vai trò `checkin_staff`, check-in nguyên tử chống race condition (HTTP 409), kiểm tra `start_at < end_at` và endpoint sửa phiên lịch trình.  
- **Skill sử dụng:** `api-development`, `security-review`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Cập nhật app/models/user.py hỗ trợ role checkin_staff và is_checkin_staff property. Cập nhật app/routes/checkin.py bóc tách ticket_number và registration_code, thực hiện cập nhật CSDL nguyên tử: Registration.query.filter_by(id=..., checked_in=False).update(...). Cập nhật app/routes/events.py kiểm tra start_at < end_at khi tạo và sửa schedule, bổ sung route POST /schedules/<id>/edit. Bổ sung route GET /events/<id>/feedback cho Organizer xem tổng hợp và tóm tắt AI."*  
- **Tệp thay đổi / Tạo mới:** `app/models/user.py`, `app/routes/checkin.py`, `app/routes/events.py`, `app/routes/admin.py`, `app/templates/events/feedback_list.html`.  
- **Đầu ra AI:** Mã nguồn backend tuân thủ ACID transaction, bẫy lỗi đầy đủ, phản hồi JSON có trạng thái HTTP tương ứng.  
- **Kết quả Kiểm thử / Thẩm định:** Kiểm tra tự động 6 test cases mới trong `tests/test_upgrade_requirements.py` đạt 100%.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

### Tác Vụ 5: Hiện Thực Tầng Step 8 Grounded RAG, Lọc PII và Cảnh Báo Mẫu Nhỏ
- **ID Lời nhắc:** PRM-2026-005  
- **Tác vụ:** Hoàn thiện chuỗi RAG 8 bước với Step 8 Response Validation, hàm khử khuẩn văn bản untrusted feedback (ẩn email/sđt, vô hiệu hóa injection), và cảnh báo `sample_warning` khi số lượng ý kiến < 3.  
- **Skill sử dụng:** `rag-prompt`, `security-review`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Hiện thực sanitize_untrusted_feedback() trong sentiment_service.py: regex nhận diện email, sđt Việt Nam và các cụm từ injection. Cảnh báo sample_warning nếu số ý kiến < 3. Bổ sung validate_and_sanitize_response() và execute_8_step_rag() trong rag_service.py thực hiện Step 8: chặn hỏi PII danh sách khách mời, chặn Prompt Injection và kiểm tra sự kiện không tồn tại. Chuẩn hóa chuyển đổi chữ 'đ'/'Đ' thành 'd' trong remove_accents."*  
- **Tệp thay đổi / Tạo mới:** `app/services/sentiment_service.py`, `app/services/rag_service.py`, `app/services/gemini_service.py`, `app/prompts/feedback_summary.txt`, `app/prompts/notification_generator.txt`.  
- **Đầu ra AI:** Module AI hoạt động grounded, an toàn trước prompt injection, không rò rỉ dữ liệu cá nhân.  
- **Kết quả Kiểm thử / Thẩm định:** Benchmark 14 kịch bản đạt 100% chỉ số an toàn và độ chính xác đối với V3.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

### Tác Vụ 6: Xây Dựng Framework Đánh Giá So Sánh 3 Chiến Lược Prompt (V1, V2, V3)
- **ID Lời nhắc:** PRM-2026-006  
- **Tác vụ:** Xây dựng framework benchmark 14 kịch bản thực nghiệm, thực thi đánh giá tự động trên 3 template prompt và ghi nhận kết quả khoa học.  
- **Skill sử dụng:** `ai-evaluation`, `testing`  
- **Lời nhắc rút gọn (Sanitized Prompt):**  
  > *"Tạo 3 prompt template trong app/prompts/eval/: prompt_v1_basic.txt, prompt_v2_grounded.txt, prompt_v3_validated.txt. Xây dựng eval_prompts.py chạy 14 kịch bản kiểm thử bắt buộc (sự kiện bình thường, thiếu ngày, thiếu địa điểm, sự kiện không tồn tại, hết vé, feedback tiêu cực, ngoài lĩnh vực, yêu cầu PII, injection...). Thu thập số liệu định lượng: Độ chính xác, Số tuyên bố không căn cứ, Xử lý no-match, Kháng injection, Bảo vệ PII, Độ trễ. Xuất kết quả vào docs/ai-prompt-comparison.md."*  
- **Tệp thay đổi / Tạo mới:** `eval_prompts.py`, `app/prompts/eval/*`, `docs/ai-prompt-comparison.md`.  
- **Đầu ra AI:** Báo cáo so sánh chi tiết 24KB, bảng so sánh trực quan, minh chứng khoa học khẳng định ưu thế vượt trội của V3 (Grounded + Validated).  
- **Kết quả Kiểm thử / Thẩm định:** Chạy thực tế thành công 100% không giả lập số liệu.  
- **Phê duyệt con người:** Phê duyệt (Pass).  

---

## 3. Tổng Kết và Cam Kết Tuân Thủ An Ninh
- Toàn bộ các tương tác AI đều được giám sát bởi lập trình viên.
- Không có bất kỳ token hoặc thông tin cá nhân khách mời nào được truyền ra môi trường bên ngoài.
- Dữ liệu đánh giá hoàn toàn có thể tái lập thông qua lệnh `python eval_prompts.py` và `pytest`.
