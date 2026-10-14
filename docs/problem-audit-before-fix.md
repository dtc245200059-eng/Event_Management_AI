# BÁO CÁO KIỂM TOÁN VẤN ĐỀ TRƯỚC KHI KHẮC PHỤC (PROBLEM AUDIT BEFORE FIX)

**Dự án:** EventAI Pro (`Event_Management_AI`)  
**Thời điểm thực hiện:** 2026-09-28 18:45:00 +07:00  
**Vai trò:** Senior Software Engineer, Software Architect, AI Engineer & QA Engineer  
**Trạng thái hệ thống trước sửa:** Build Pass | Server Starts | 36/36 Tests Pass | 14 Warnings | 8 Problems Identified  

---

## 1. TỔNG QUAN SỐ LƯỢNG VẤN ĐỀ (PROBLEM INVENTORY)

| Phân loại theo Mức độ nghiêm trọng | Số lượng | Mô tả chi tiết |
| :--- | :---: | :--- |
| **P0 - Blocker** | **0** | Không có lỗi làm sập toàn bộ hệ thống hoặc chặn build |
| **P1 - Critical** | **0** | Không có lỗi hỏng auth, mất dữ liệu hay sập runtime cốt lõi |
| **P2 - High** | **1** | Cấu hình model Gemini thiếu fallback cho GA model `gemini-2.0-flash` |
| **P3 - Medium** | **5** | 13 LegacyAPIWarnings trong SQLAlchemy 2.0; 12 Skills thiếu cấu trúc chuẩn; thiếu 6 Skills năng lực cốt lõi; thư mục asset duplicate (`prompts/`); upstream warning Python 3.14 |
| **P4 - Low** | **2** | 20 hardcoded `file:///` links trong `README.md`; thiếu hệ thống tài liệu quản trị Skill (`skills-index`, `dependency-map`, v.v.) |
| **TỔNG CỘNG** | **8** | **8 nhóm vấn đề được xác định chính xác nguyên nhân gốc rễ** |

### Thống kê theo phân hệ kỹ thuật:
- **Build / Compile errors:** 0
- **Runtime errors:** 0
- **Test failures:** 0 (36/36 passed)
- **Warnings:** 14 (13 LegacyAPIWarnings từ SQLAlchemy `Query.get()`, 1 Upstream DeprecationWarning từ `google.genai`)
- **Documentation errors:** 2 (Hardcoded absolute links, thiếu bộ tài liệu Skill Governance)
- **Skill errors:** 2 (12 Skills cũ thiếu schema chuẩn 17 mục, thiếu 6 Skills năng lực quan trọng)

---

## 2. BẢNG PHÂN LOẠI & CHI TIẾT CÁC VẤN ĐỀ ĐƯỢC PHÁT HIỆN

| ID | Mức độ | Phân loại | Tệp / Thành phần ảnh hưởng | Nguyên nhân gốc rễ (Root Cause) | Tác động hệ thống |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **PRB-01** | **P2** | AI / Config | [app/services/gemini_service.py](file:///d:/Event_Management_AI/app/services/gemini_service.py), [.env](file:///d:/Event_Management_AI/.env) | `candidate_models` trong `call_gemini` chứa `gemini-3.6-flash`, `gemini-2.5-flash`, `gemini-1.5-flash` nhưng **bỏ sót model GA chính thức `gemini-2.0-flash`**. Nếu API key không hỗ trợ experimental model 3.6, request có thể bị gián đoạn trước khi fallback. | Rủi ro gọi Gemini API thất bại khi dùng API key thông thường |
| **PRB-02** | **P3** | Backend / ORM | [app/routes/admin.py](file:///d:/Event_Management_AI/app/routes/admin.py), [tickets.py](file:///d:/Event_Management_AI/app/routes/tickets.py), [events.py](file:///d:/Event_Management_AI/app/routes/events.py), [checkin.py](file:///d:/Event_Management_AI/app/routes/checkin.py), [notifications.py](file:///d:/Event_Management_AI/app/routes/notifications.py), [main.py](file:///d:/Event_Management_AI/app/routes/main.py) | Các route sử dụng `Model.query.get_or_404(id)`. Trong Flask-SQLAlchemy 3.0 / SQLAlchemy 2.0, phương thức `Query.get_or_404` gọi ngầm `Query.get()`, gây ra **13 `LegacyAPIWarning`** khi chạy test suite. | Gây 13 cảnh báo suy giảm hiệu năng và nguy cơ lỗi thời trong SQLAlchemy 2.1+ |
| **PRB-03** | **P3** | Skills System | [.agents/skills/](file:///d:/Event_Management_AI/.agents/skills/) (12 skills) | Cả 12 Skills hiện có được biên soạn dưới dạng tài liệu tóm tắt môn học (`## Objective`, `## Inputs`, `## Outputs`), **thiếu toàn bộ 17 phần chuẩn hóa** (`Purpose`, `Scope`, `When to Use`, `When NOT to Use`, `Required Context`, `Project Files to Inspect`, `Validation`, `Failure Handling`, v.v.). Đặc biệt thiếu hướng dẫn Agent `ĐỌC GÌ → PHÂN TÍCH GÌ → THAY ĐỔI GÌ → KIỂM TRA GÌ`. | AI Agent không thể đọc hiểu và thực thi các thao tác lập trình/kiểm toán tự động trên repo |
| **PRB-04** | **P3** | Skills System | [.agents/skills/](file:///d:/Event_Management_AI/.agents/skills/) | Thiếu 6 Skills đại diện cho các năng lực cốt lõi đã chạy thực tế trong mã nguồn: `frontend-development`, `responsive-mobile`, `api-development`, `ai-agent`, `ai-evaluation`, `deployment`. | Agent thiếu quy trình chuẩn khi can thiệp vào giao diện di động, API contracts, Multi-Agent hay Docker |
| **PRB-05** | **P3** | Code Structure | `prompts/` (root), `agents/`, `models/`, `services/` | Thư mục `prompts/` ở root là bản sao chép thừa thãi của `app/prompts/multi_agent/`. Các thư mục `agents/`, `models/`, `services/` ở root là các shim alias từ giai đoạn đầu phát triển. | Gây nhầm lẫn về cấu trúc thư mục chuẩn của Flask Application Factory |
| **PRB-06** | **P3** | Python 3.14 Runtime | `google/genai/types.py` (Upstream) | Khi chạy `test_requirement_agent_extraction`, thư viện `google-genai` sinh `DeprecationWarning: '_UnionGenericAlias' is deprecated and slated for removal in Python 3.17` do Python 3.14 thay đổi typing internals. | Cảnh báo tương thích runtime của bên thứ ba, không ảnh hưởng chức năng |
| **PRB-07** | **P4** | Documentation | [README.md](file:///d:/Event_Management_AI/README.md) | Dòng 13-32 trong `README.md` sử dụng đường dẫn tuyệt đối cục bộ `file:///d:/Event_Management_AI/docs/...` thay vì markdown relative links (`docs/...`). | Broken link khi xem trên GitHub hoặc trên các máy tính khác |
| **PRB-08** | **P4** | Documentation / Skills | `docs/` & `.agents/skills/` | Chưa có bộ tài liệu quản trị kỹ năng: `docs/skills-index.md`, `docs/skill-capability-matrix.md`, `docs/skills-dependency-map.md`, `docs/skill-validation-report.md`, `docs/skill-system-change-log.md` và `.agents/skills/README.md`. | Khó theo dõi ma trận phụ thuộc giữa các Skills và tài liệu hệ thống |

---

## 3. THỰC TRẠNG KIỂM THỬ TRƯỚC KHI KHẮC PHỤC

Kết quả thực thi tự động qua Pytest 9.1.1:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Event_Management_AI
collected 36 items

tests/test_ai_services.py .........                                     [ 25%]
tests/test_auth.py .......                                               [ 44%]
tests/test_multi_agent.py ..........                                     [ 72%]
tests/test_notifications_and_feedback.py ....                            [ 83%]
tests/test_tickets_and_quota.py ......                                   [100%]

============================== warnings summary ===============================
tests/test_auth.py: 1 warning (LegacyAPIWarning: Query.get())
tests/test_notifications_and_feedback.py: 3 warnings (LegacyAPIWarning: Query.get())
tests/test_tickets_and_quota.py: 9 warnings (LegacyAPIWarning: Query.get())
tests/test_multi_agent.py: 1 warning (DeprecationWarning: _UnionGenericAlias in google.genai)

====================== 36 passed, 14 warnings in 40.32s =======================
```

---

## 4. KẾT LUẬN & CAM KẾT HÀNH ĐỘNG
- **Hiện trạng:** Hệ thống đang hoạt động ổn định về mặt chức năng chính (36/36 tests pass), không có crash runtime P0/P1. Tuy nhiên, tồn tại **1 vấn đề High (P2)** về cấu hình fallback model AI, **5 vấn đề Medium (P3)** về cảnh báo ORM, chuẩn hóa Skills, thiếu Skills năng lực, tệp trùng lặp, và **2 vấn đề Low (P4)** về tài liệu.
- **Cam kết:** Giữ nguyên trạng thái mã nguồn và CHƯA SỬA CODE cho đến khi hoàn thành báo cáo này theo đúng chỉ thị.
