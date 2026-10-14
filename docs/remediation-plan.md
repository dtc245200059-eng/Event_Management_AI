# MASTER REMEDIATION PLAN — KẾ HOẠCH KHẮC PHỤC TỔNG THỂ HỆ THỐNG

**Dự án:** EventAI Pro (`Event_Management_AI`)  
**Giai đoạn:** Phase 2 — Gap Analysis  
**Mục tiêu:** Định tuyến chi tiết toàn bộ 12 Gaps và các vấn đề kỹ thuật vào các Giai đoạn Thực thi (Phase 3 đến Phase 8) theo thứ tự phụ thuộc nghiêm ngặt.

---

## 1. NGUYÊN TẮC THỰC THI (EXECUTION PRINCIPLES)

1. **Sửa theo thứ tự phụ thuộc (Dependency Order):**
   - Không sửa UI trước khi backend đang có cảnh báo/lỗi.
   - Không cập nhật tài liệu khi kiến trúc hoặc mã nguồn chưa ổn định.
   - Sửa từng nhóm nhỏ, kiểm tra thực nghiệm và verify ngay sau mỗi bước.
2. **Bảo toàn chức năng hiện tại (Preserve Working Code):**
   - Tuyệt đối không xóa bỏ các tính năng đang hoạt động bình thường.
   - Không tự ý refactor code ngoài phạm vi nguyên nhân gốc rễ đã xác định.
3. **Chuẩn hóa hệ thống Kỹ năng Agent:**
   - Đảm bảo 100% Skills có cấu trúc chuẩn 17 mục và chỉ rõ quy trình `ĐỌC → PHÂN TÍCH → SỬA → TEST`.

---

## 2. ÁNH XẠ KHOẢNG CÁCH VÀO CÁC GIAI ĐOẠN KHẮC PHỤC (GAP-TO-PHASE MAPPING)

| Giai đoạn Thực thi (Phase) | Tên Giai đoạn (Phase Name) | Khoảng cách Được Khắc phục (Mapped Gaps) | Chi tiết Công việc (Detailed Tasks) | Kết quả Đầu ra (Deliverables) |
| :---: | :--- | :---: | :--- | :--- |
| **PHASE 3** | **Cập nhật Kỹ năng Hiện có (Update Existing Skills)** | **GAP-003** [RESOLVED] | Nâng cấp toàn diện 12 skills cũ theo cấu trúc chuẩn 16 mục; sửa các broken links; bổ sung danh mục file inspect thực tế (`app/routes/`, `app/models/`, `app/services/`) | 12 tệp `SKILL.md` chuẩn hóa tại `.agents/skills/*/` (100% PASS) |
| **PHASE 4** | **Bổ sung Kỹ năng Còn thiếu (Create Missing Skills)** | **GAP-004** [RESOLVED] | Xây dựng mới 6 skills theo cấu trúc chuẩn 20 mục: `frontend-development`, `responsive-mobile`, `api-development`, `ai-agent`, `ai-evaluation`, `deployment` | 6 thư mục và tệp `SKILL.md` mới tại `.agents/skills/` (100% PASS) |
| **PHASE 5** | **Cập nhật & Bổ sung Tài liệu (Documentation Sync)** | **GAP-005, GAP-006, GAP-007, GAP-008, GAP-010, GAP-012** | - Cập nhật `docs/api.md` đủ 66 endpoints<br/>- Khởi tạo bộ 5 tài liệu quản trị Skill (`skills-index`, `dependency-map`, v.v.)<br/>- Tạo `docs/frontend-architecture.md`, `docs/responsive-mobile.md`, `docs/known-issues.md`<br/>- Tạo `.agents/skills/README.md`<br/>- Sửa 20 links tuyệt đối trong `README.md`<br/>- Gắn nhãn trạng thái `IMPLEMENTED` trong các docs | Bộ tài liệu hệ thống đồng bộ 100% với mã nguồn |
| **PHASE 6** | **Khắc phục Mã nguồn & Cấu hình (Fix Implementation & Config)** | **GAP-001, GAP-002, GAP-009, GAP-011** | - Thay thế 13 lệnh `Model.query.get_or_404(id)` bằng `db.get_or_404(Model, id)` trong 6 route files<br/>- Bổ sung `gemini-2.0-flash` vào `candidate_models` trong `app/services/gemini_service.py`<br/>- Bổ sung route `/health` kiểm tra trạng thái CSDL và API<br/>- Tạo `pytest.ini` thiết lập `pythonpath = .` | Mã nguồn sạch cảnh báo, tối ưu model AI, hỗ trợ healthcheck và test runner chuẩn |
| **PHASE 7** | **Kiểm thử Toàn diện & Hồi quy (Testing & Regression)** | *Tất cả các Gaps* | - Chạy kiểm thử đơn vị, kiểm thử tích hợp, kiểm thử đa tác tử qua `pytest -v`<br/>- Xác minh 36/36 test cases pass sạch 100%<br/>- Xác nhận 13 `LegacyAPIWarning` đã biến mất hoàn toàn | Báo cáo kiểm thử không lỗi hồi quy |
| **PHASE 8** | **Kiểm toán Nhất quán Cuối cùng (Final Validation & Change Log)** | *Tất cả các Gaps* | - Rà soát chéo 8 chiều: Code ↔ Test ↔ DB ↔ API ↔ UI ↔ Mobile ↔ Skills ↔ Docs<br/>- Tạo `docs/skill-system-change-log.md`<br/>- Tạo `docs/problem-fix-report.md` | Báo cáo nghiệm thu hoàn tất bàn giao |

---

## 3. LỊCH TRÌNH THỰC THI CHI TIẾT (STEP-BY-STEP SCHEDULE)

### Giai đoạn 3: Cập nhật 12 Skills Hiện có (Phase 3)
1. `requirements-analysis`: Cập nhật cấu trúc chuẩn 17 mục, gắn với `docs/requirements.md`, `docs/traceability-matrix.md`.
2. `architecture-design`: Cập nhật cấu trúc chuẩn 17 mục, gắn với 8 Blueprints trong `app/routes/`, `app/extensions.py`.
3. `database-design`: Cập nhật cấu trúc chuẩn 17 mục, gắn với 11 models trong `app/models/`, `database/schema.sql`.
4. `implementation`: Cập nhật cấu trúc chuẩn 17 mục, sửa các đường dẫn file giả định thành file thực tế trong `app/`.
5. `question-analysis`: Cập nhật cấu trúc chuẩn 17 mục, sửa link `docs/question-analysis.md`, gắn hàm `extract_question_intent`.
6. `event-retrieval`: Cập nhật cấu trúc chuẩn 17 mục, gắn với truy vấn SQL an toàn trong `app/services/rag_service.py`.
7. `context-builder`: Cập nhật cấu trúc chuẩn 17 mục, gắn logic xây dựng Grounded Context và bảng `event_faqs`.
8. `rag-prompt`: Cập nhật cấu trúc chuẩn 17 mục, sửa link `app/prompts/`, gắn template prompt RAG.
9. `testing`: Cập nhật cấu trúc chuẩn 17 mục, bổ sung toàn bộ 5 test files thực tế và lệnh `pytest`.
10. `code-review`: Cập nhật cấu trúc chuẩn 17 mục, bổ sung checklist kiểm tra code smells, SQL injection, ORM query patterns.
11. `security-review`: Cập nhật cấu trúc chuẩn 17 mục, bổ sung checklist kiểm toán PBKDF2, RBAC decorator, rate limiting.
12. `documentation`: Cập nhật cấu trúc chuẩn 17 mục, sửa các relative links, bổ sung checklist đồng bộ Code ↔ Docs.

### Giai đoạn 4: Khởi tạo 6 Skills Mới (Phase 4)
1. `frontend-development`: Jinja2 templates, CSS custom properties, Apple Design system, dark/light theme, components.
2. `responsive-mobile`: Breakpoints di động (320px–768px), drawer menu, z-index, touch events, camera QR scanner (`html5-qrcode`).
3. `api-development`: Thiết kế 66 RESTful endpoints, cấu trúc JSON response, mã lỗi HTTP, tham số query.
4. `ai-agent`: Điều phối 7 Agents, message bus audit log, critic validation guardrail, retry loop.
5. `ai-evaluation`: Thực thi 10 benchmark test cases, đo lường độ trễ, token usage, tỷ lệ ảo giác so sánh single vs multi-agent.
6. `deployment`: Docker, docker-compose, Procfile Gunicorn, cấu hình biến môi trường, seed CSDL.

### Giai đoạn 5: Cập nhật & Bổ sung Tài liệu (Phase 5)
1. Cập nhật `docs/api.md`: Bổ sung toàn bộ 66 endpoints theo 8 phân hệ nghiệp vụ.
2. Cập nhật `docs/database-design.md`: Gắn nhãn `IMPLEMENTED` cho bảng 10 (`notifications`) và bảng 11 (`event_faqs`).
3. Cập nhật `docs/architecture.md`: Phân định rõ luồng dữ liệu Single-Agent RAG vs Multi-Agent Ensemble.
4. Khởi tạo `docs/frontend-architecture.md` & `docs/responsive-mobile.md`.
5. Khởi tạo bộ 5 tài liệu quản trị Skill:
   - `docs/skills-index.md`
   - `docs/skill-capability-matrix.md`
   - `docs/skills-dependency-map.md`
   - `docs/skill-validation-report.md`
   - `docs/skill-system-change-log.md`
6. Khởi tạo `.agents/skills/README.md`.
7. Khởi tạo `docs/known-issues.md`.
8. Cập nhật `README.md`: Sửa 20 links tuyệt đối cục bộ thành relative markdown links.

### Giai đoạn 6: Khắc phục Mã nguồn & Cấu hình (Phase 6)
1. Sửa cảnh báo ORM trong 6 route files:
   - `app/routes/admin.py`: 2 vị trí `Model.query.get_or_404(id)` → `db.get_or_404(Model, id)`.
   - `app/routes/tickets.py`: 6 vị trí.
   - `app/routes/events.py`: 8 vị trí.
   - `app/routes/checkin.py`: 3 vị trí.
   - `app/routes/notifications.py`: 2 vị trí.
   - `app/routes/main.py`: 1 vị trí.
2. Cập nhật `app/services/gemini_service.py`: Thêm `gemini-2.0-flash` vào `candidate_models`.
3. Bổ sung endpoint `/health` trong `app/routes/main.py` trả về trạng thái CSDL và API dưới dạng JSON.
4. Tạo `pytest.ini` với cấu hình `pythonpath = .` để chuẩn hóa lệnh chạy `pytest`.

### Giai đoạn 7: Kiểm thử & Hồi quy (Phase 7)
1. Chạy toàn bộ 36 tests qua lệnh `pytest -v`.
2. Kiểm tra log để xác nhận 13 `LegacyAPIWarning` đã hoàn toàn biến mất.
3. Chạy thử endpoint `/health` và route AI RAG.

### Giai đoạn 8: Nghiệm thu & Báo cáo Cuối cùng (Phase 8)
1. Lập báo cáo tổng kết hoàn tất khắc phục `docs/problem-fix-report.md`.
2. Báo cáo nghiệm thu theo các tiêu chí Definition of Done.
