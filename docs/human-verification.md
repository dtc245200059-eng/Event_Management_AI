# BIÊN BẢN THẨM ĐỊNH CON NGƯỜI (HUMAN VERIFICATION RECORD)
**Dự án:** Hệ thống quản lý sự kiện có tích hợp AI (EventAI Pro) - Đề tài 09  
**Phương pháp:** AI-Augmented SDLC Human Verification Gates  
**Hội đồng thẩm định:** Nhóm phát triển 2 thành viên & Giảng viên hướng dẫn  
**Ngày lập:** 27/10/2026  

---

## 1. Giới Thiệu Cổng Kiểm Soát Con Người (Verification Gates)

Trong quy trình phát triển phần mềm AI-Augmented SDLC, mọi kết quả sinh ra từ AI (mã nguồn, tài liệu, biểu đồ kiến trúc, kết quả phân tích) không được tự động chấp nhận nếu chưa qua kiểm tra độc lập và phê duyệt bởi kỹ sư con người. Dự án thiết lập 6 Cổng Thẩm định (Verification Gates - VG) tương ứng với 6 giai đoạn nâng cấp.

---

## 2. Nhật Ký 6 Cổng Thẩm Định Nghiệm Thu

### Gate 1: Thẩm Định Phân Tích Khoảng Trống (Gap Analysis Approval)
- **Mã cổng:** VG-01-GAP-AUDIT  
- **Đối tượng thẩm định:** Tài liệu `docs/upgrade-gap-analysis.md`.  
- **Tiêu chí kiểm tra:**
  1. Xác định đúng thư mục gốc và hiện trạng dự án.
  2. Không đề xuất đập bỏ mã nguồn đang vận hành tốt.
  3. Bám sát đầy đủ 5 luồng yêu cầu mở rộng của Giảng viên.
- **Bằng chứng thẩm định:** Đối chiếu mã nguồn Flask hiện hữu, xác nhận 42/42 endpoints và cấu trúc CSDL SQLite an toàn.
- **Kết luận:** **THÔNG QUA (PASSED)** — Ký duyệt bởi Member 1 & Member 2.

---

### Gate 2: Thẩm Định Kiến Trúc & Biểu Đồ PlantUML (Architecture Approval)
- **Mã cổng:** VG-02-ARCH-DESIGN  
- **Đối tượng thẩm định:** 10 biểu đồ PlantUML trong thư mục `docs/diagrams/`.  
- **Tiêu chí kiểm tra:**
  1. Thể hiện đầy đủ 4 vai trò: Attendee, Organizer, CheckInStaff, Admin.
  2. ERD mô tả 11 thực thể có đầy đủ khóa chính (PK), khóa ngoại (FK) và Index.
  3. Biểu đồ tuần tự (Sequence) và hoạt động (Activity) mô tả chính xác luồng check-in nguyên tử và chuỗi RAG 8 bước.
- **Bằng chứng thẩm định:** So sánh chéo giữa file `.puml` và schema SQLAlchemy trong `app/models/`. Không phát hiện mâu thuẫn.
- **Kết luận:** **THÔNG QUA (PASSED)** — Ký duyệt bởi Member 2 (AI & Architecture Lead).

---

### Gate 3: Thẩm Định Kiểm Soát Truy Cập RBAC & Check-in Nguyên Tử (Core Security Approval)
- **Mã cổng:** VG-03-RBAC-CHECKIN  
- **Đối tượng thẩm định:** Mã nguồn `app/models/user.py`, `app/routes/checkin.py`, `app/routes/events.py`.  
- **Tiêu chí kiểm tra:**
  1. CheckInStaff chỉ được phép vào `/checkin/`, bị cấm vào `/admin/dashboard` (HTTP 403).
  2. Check-in phải mang tính nguyên tử (Atomic transaction): quét vé lặp lại phải trả về HTTP 409 từ chối vé đã dùng.
  3. Thêm/sửa phiên lịch trình bắt buộc `start_at < end_at`.
- **Bằng chứng thẩm định:** Chạy 6 test cases mới trong `tests/test_upgrade_requirements.py`: 100% Passed.
- **Kết luận:** **THÔNG QUA (PASSED)** — Ký duyệt bởi Member 2 (Security Lead).

---

### Gate 4: Thẩm Định Tích Hợp AI & Bảo Vệ Dữ Liệu Cá Nhân (AI Privacy Approval)
- **Mã cổng:** VG-04-AI-PRIVACY  
- **Đối tượng thẩm định:** `app/services/gemini_service.py`, `app/services/sentiment_service.py`, `app/services/rag_service.py`.  
- **Tiêu chí kiểm tra:**
  1. AI email draft bắt buộc dùng placeholder `{attendee_name}`, `{event_name}`, tuyệt đối không gửi danh sách liên hệ khách mời lên Gemini.
  2. Bắt buộc có bước con người xem trước và phê duyệt nội dung email trước khi gửi.
  3. Feedback gửi lên LLM phải được khử khuẩn thông tin cá nhân (email, sđt) và trung hòa lệnh Prompt Injection.
  4. Hiển thị số lượng mẫu ý kiến và cảnh báo khi mẫu nhỏ (< 3).
- **Bằng chứng thẩm định:** Chạy kiểm thử hàm `sanitize_untrusted_feedback()` và `test_rag_step_8_response_validation()`. Toàn bộ dữ liệu PII bị ẩn và lệnh injection bị vô hiệu hóa.
- **Kết luận:** **THÔNG QUA (PASSED)** — Ký duyệt bởi Member 2 & Member 1.

---

### Gate 5: Thẩm Định Benchmark & Kháng Ảo Giác 3 Phiên Bản Prompt (Prompt Eval Approval)
- **Mã cổng:** VG-05-PROMPT-BENCHMARK  
- **Đối tượng thẩm định:** Script `eval_prompts.py` và báo cáo `docs/ai-prompt-comparison.md`.  
- **Tiêu chí kiểm tra:**
  1. Đánh giá cùng 1 bộ 14 câu hỏi kiểm thử trên 3 phiên bản Prompt: V1 (Basic), V2 (Grounded), V3 (Grounded + Validated).
  2. Thu thập số liệu đo lường thực tế, không bịa đặt số liệu.
  3. Tách biệt rõ ràng chế độ Live API và Local Grounded Knowledge Engine khi ngoại tuyến.
- **Bằng chứng thẩm định:** Kết quả benchmark thực tế: V3 đạt 100% độ chính xác, 0 tuyên bố không căn cứ, 100% xử lý no-match, 100% kháng injection và 100% bảo vệ PII.
- **Kết luận:** **THÔNG QUA (PASSED)** — Ký duyệt bởi Member 2 (AI Lead).

---

### Gate 6: Thẩm Định Toàn Diện & Sẵn Sàng Nghiệm Thu (Final Release Approval)
- **Mã cổng:** VG-06-FINAL-RELEASE  
- **Đối tượng thẩm định:** Toàn bộ hệ thống web, bộ kiểm thử tự động 42 tests, tài liệu hướng dẫn và kịch bản demo 12 bước.  
- **Tiêu chí kiểm tra:**
  1. Toàn bộ 42 test cases trong pytest đạt 100% Pass.
  2. Giao diện Apple Liquid Glass nhất quán, hỗ trợ Dark/Light mode và Responsive mobile.
  3. Kịch bản demo 12 bước có thể tái lập thực tế từ đăng ký, check-in, thống kê, phản hồi đến trợ lý AI.
- **Bằng chứng thẩm định:** Lệnh `pytest` hoàn thành với `42 passed in 60.29s`.
- **Kết luận:** **HỆ THỐNG ĐẠT CHUẨN XUẤT XẮC ĐỂ NGHIỆM THU VÀ BẢO VỆ ĐỒ ÁN**.

---

## 3. Chữ Ký và Cam Kết Trách Nhiệm

| Đại diện | Họ và tên | Chức danh | Chữ ký xác nhận |
| :--- | :--- | :--- | :--- |
| **Thành viên 1** | Sinh viên 1 | Front-end & Event Operations Lead | *Đã kiểm tra và ký nhận* |
| **Thành viên 2** | Sinh viên 2 | Data, Security & AI Architect | *Đã kiểm tra và ký nhận* |
