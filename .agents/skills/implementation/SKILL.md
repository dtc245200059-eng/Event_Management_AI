---
name: implementation
description: Skill hướng dẫn quy trình lập trình có kỷ luật, đọc kỹ đặc tả, hiện thực hóa Flask Blueprint, Models, Services, Giao diện Jinja2, tích hợp AI Orchestration và kiểm tra tự động.
---

# Implementation Skill

## Objective
Hiện thực hóa mã nguồn hệ thống một cách có cấu trúc, tuân thủ chặt chẽ tài liệu Requirements, Architecture và Database Design đã duyệt ở các Human Gates, đảm bảo tính mô-đun hóa, nguyên tắc Clean Code và khả năng mở rộng.

## Inputs
Đọc các tài liệu thiết kế đã duyệt:
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/database-design.md`
- `docs/acceptance-criteria.md`
- `database/schema.sql`

## Process / Workflow
1. **Đọc và Hiểu Đặc tả (Specification Mastery)**:
   - Nắm vững Input/Output, validation rules và edge cases trước khi gõ dòng code đầu tiên.
2. **Cấu hình Môi trường & Extensions**:
   - `app/config.py`, `app/extensions.py`, `.env` và factory `create_app()`.
3. **Hiện thực hóa Data Models**:
   - Khởi tạo SQLAlchemy models trong `app/models/` với kiểu dữ liệu, quan hệ quan hệ backref, cascade và helper methods.
4. **Hiện thực hóa Business Services**:
   - Tách riêng toàn bộ logic nghiệp vụ vào `app/services/` (`event_service.py`, `ticket_service.py`, `checkin_service.py`, `rag_service.py`, `recommendation_service.py`, `predictive_service.py`, `gemini_service.py`).
5. **Hiện thực hóa Routes / Controllers**:
   - Tổ chức theo Flask Blueprints trong `app/routes/` (`auth.py`, `events.py`, `tickets.py`, `checkin.py`, `ai_routes.py`, `admin.py`).
   - Sử dụng các Decorators phân quyền (`@login_required`, `@admin_required`, `@staff_required`).
6. **Xây dựng Giao diện (Presentation Layer)**:
   - Jinja2 templates kế thừa `base.html`, thiết kế Glassmorphism CSS hiện đại, Responsive UI, Vanilla JS fetch API.
7. **Kiểm tra Cú pháp & Static Analysis**:
   - Đảm bảo mã nguồn không có lỗi import, deprecation unhandled hoặc runtime syntax error.
8. **Chạy Kiểm thử Tự động (Automated Verification)**:
   - Chạy Pytest để đảm bảo các tính năng mới không làm gãy các tính năng hiện hữu (Regression prevention).

## Rules & Constraints
- Tuyệt đối không tự ý thay đổi Requirements hoặc Architecture khi lập trình.
- **Nguyên tắc Agent Biết Dừng (Stop-and-Ask Rule)**: Nếu phát hiện đặc tả bị thiếu, mâu thuẫn hoặc không đủ thông tin để cài đặt, AI Agent phải DỪNG LẠI và báo cáo cho con người (Human Gate) thay vì tự ý suy đoán bừa bãi.
- Tuyệt đối không hardcode API Keys, Secret Keys hoặc mật khẩu trong mã nguồn.
- Mọi thao tác ghi dữ liệu nhạy cảm (đặt vé, trừ quota, cập nhật trạng thái) phải nằm trong DB Transaction (`db.session.commit()`) với khối `try...except db.session.rollback()`.

## Outputs
- Mã nguồn hoàn chỉnh trong các thư mục `app/`, `run.py`, `seed.py`.
- Danh sách các tệp đã thêm/sửa đổi.

## Verification
- Chạy hệ thống trên môi trường cục bộ hoặc container không phát sinh lỗi.
- Toàn bộ các route trả về đúng mã trạng thái HTTP chuẩn (200, 201, 400, 401, 403, 404, 409, 500).
