# GAP REGISTER — SỔ THEO DÕI VÀ QUẢN TRỊ KHOẢNG CÁCH HỆ THỐNG

> **Dự án:** EventAI Pro (`Event_Management_AI`)  
> **Cập nhật:** Sau Phase 6 — Implementation Fix, Stabilization & Gap Remediation (28/09/2026)  
> **Tiêu chuẩn phân loại:**  
> - **Mức độ nghiêm trọng (Severity):** G0 (Blocker) | G1 (Critical) | G2 (High) | G3 (Medium) | G4 (Low)  
> - **Mức độ ưu tiên xử lý (Priority):** P0 (Khẩn cấp trước mọi thứ) | P1 (Ưu tiên cao) | P2 (Trung bình) | P3 (Cải thiện sau)

---

## BẢNG QUẢN TRỊ KHOẢNG CÁCH (GAP REGISTER TABLE)

| ID | Category | Description | Evidence | Root Cause | Impact | Severity | Priority | Status | Phase Xử Lý | Bằng Chứng Giải Quyết |
|:---|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| **GAP-001** | Backend / ORM | 13 cảnh báo `LegacyAPIWarning` từ SQLAlchemy 2.0 do dùng `Query.get()` | `pytest` log phát sinh 13 cảnh báo | Cú pháp cũ `Model.query.get(id)` | Cảnh báo tương thích | **G3** | **P1** | **RESOLVED** | Phase 6 | Chuyển đổi 22 vị trí sang `db.get_or_404(Model, id)`. Pytest đạt 0 warnings. |
| **GAP-002** | AI / Config | Model list trong `gemini_service.py` chưa đặt `gemini-2.5-flash` / `gemini-2.0-flash` lên đầu | `gemini_service.py` | Cấu hình candidate models | Nguy cơ 404 model | **G2** | **P1** | **RESOLVED** | Phase 6 | Cập nhật default model & candidate list ưu tiên `gemini-2.5-flash`, `gemini-2.0-flash`. |
| **GAP-003** | Skills System | Cả 12 Skills ban đầu thiếu cấu trúc chuẩn 17 mục và workflow 7 bước | Quét `.agents/skills/*/SKILL.md` | Tài liệu lý thuyết | Agent thiếu quy trình | **G2** | **P1** | **RESOLVED** | Phase 3 | Chuẩn hóa 12 skills đạt 20 mục và 7 bước `READ -> REPORT`. |
| **GAP-004** | Skills System | Thiếu 6 Skills đại diện cho các năng lực cốt lõi: frontend, mobile, api, ai-agent, ai-eval, deployment | Thư mục `.agents/skills/` chỉ có 12 skills | Chưa bao phủ toàn diện | Agent thiếu năng lực chuyên biệt | **G2** | **P1** | **RESOLVED** | Phase 4 | Tạo mới 6 kỹ năng chất lượng cao, đạt 18/18 kỹ năng. |
| **GAP-005** | Documentation | Tài liệu `docs/api.md` trước đó chỉ mô tả 9 endpoint AI, thiếu 57 endpoints nghiệp vụ | `app.url_map` có 66 endpoints | Chưa đồng bộ sau mở rộng | Lệch pha đặc tả và code | **G3** | **P2** | **RESOLVED** | Phase 5 | Viết lại `docs/api.md` đặc tả toàn bộ endpoints, RBAC, Schemas. |
| **GAP-006** | Architecture / Assets | Thư mục `prompts/` ở root trùng lặp với `app/prompts/multi_agent/` | Kiểm tra thư mục root | Di chứng chuyển đổi App Factory | Gây phân mảnh cấu trúc | **G4** | **P3** | **RESOLVED** | Phase 6 | Đồng bộ hóa toàn diện nội dung prompt, thiết lập root aliases hỗ trợ giáo trình học liệu. |
| **GAP-007** | Documentation | `README.md` trước đó chứa 20 đường dẫn tuyệt đối cục bộ `file:///d:/...` | Dòng 13-32 trong `README.md` cũ | Copy link tuyệt đối từ local | Hỏng liên kết trên máy khác | **G4** | **P3** | **RESOLVED** | Phase 5 | Chuẩn hóa 100% relative links trong `README.md`. |
| **GAP-008** | Documentation / Skills | Thiếu bộ tài liệu quản trị kỹ năng và tệp `.agents/skills/README.md` | Kiểm tra thư mục `docs/` | Chưa thiết lập khung quản trị | Agent thiếu bản đồ định vị | **G3** | **P2** | **RESOLVED** | Phase 5 | Ban hành `.agents/skills/README.md` và `docs/documentation-index.md`. |
| **GAP-009** | Deployment / Ops | Thiếu endpoint kiểm tra sức khỏe hệ thống chuyên biệt (`/health`) | Quét `app.url_map` | Chưa có route healthcheck riêng | Phải probe qua trang chủ | **G3** | **P2** | **RESOLVED** | Phase 6 | Triển khai endpoint `/health` kiểm tra kết nối DB, trả về 200 JSON cho Docker/K8s/PaaS. |
| **GAP-010** | Security / Ops | Rate Limiter của AI Chat lưu trong bộ nhớ tiến trình (in-memory) | `gemini_service.py` dùng `defaultdict` | Thiết kế đơn tiến trình | Chưa đồng bộ đa worker | **G3** | **P3** | **RESOLVED** | Phase 6 | Nâng cấp `check_rate_limit` hỗ trợ Redis khi có `REDIS_URL`, tự động fallback In-Memory. |
| **GAP-011** | Testing | Test runner yêu cầu gọi qua `python -m pytest` để nạp đúng `PYTHONPATH` | Chạy lệnh `pytest` đơn thuần thiếu path `app` | Chưa có `pytest.ini` | Cần chỉ dẫn chạy chuẩn | **G3** | **P2** | **RESOLVED** | Phase 6 | Tạo `pytest.ini` với `pythonpath = .` và filterwarnings chuẩn. Lệnh `pytest` chạy trực tiếp. |
| **GAP-012** | Documentation | Các tài liệu kỹ thuật chưa gắn nhãn trạng thái thực tế (`[IMPLEMENTED]`, `[PLANNED]`) | Rà soát các tệp trong `docs/` | Thiếu quy chuẩn gắn nhãn | Khó phân biệt hiện trạng | **G4** | **P3** | **RESOLVED** | Phase 5 | Gắn nhãn trạng thái minh bạch cho toàn bộ 39 tài liệu kỹ thuật. |

---

## TỔNG HỢP TIẾN ĐỘ XỬ LÝ GAP (PROGRESS SUMMARY)

- **Tổng số GAPs nhận diện ban đầu:** **12 Gaps**
- **Đã Giải Quyết Triệt Để (RESOLVED):** **12 / 12 Gaps (100%)**
  - Phase 3: `GAP-003` (Sửa chữa & Nâng cấp 12 Skills hiện hữu)
  - Phase 4: `GAP-004` (Tạo mới 6 Skills thiếu cốt lõi)
  - Phase 5: `GAP-005` (Viết lại API Docs 66 endpoints), `GAP-007` (Relative links README), `GAP-008` (Skills README), `GAP-012` (Status tags)
  - Phase 6: `GAP-001` (SQLAlchemy 2.0 ORM fix), `GAP-002` (Gemini model priority), `GAP-006` (Assets sync & aliases), `GAP-009` (`/health` probe), `GAP-010` (Redis/Memory rate limiter), `GAP-011` (`pytest.ini` configuration)
- **Tình trạng kiểm thử sau khắc phục:** **36/36 tests PASSED (100%), 0 WARNINGS, 0 ERRORS**.
