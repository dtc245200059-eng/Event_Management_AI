---
name: documentation
description: Skill tổng hợp và duy trì hệ thống tài liệu kỹ thuật của dự án (Requirements, Architecture, Database, Testing, Security, User Manual, API Guide, Traceability Matrix).
---

# Documentation Skill

## Objective
Tổng hợp, chuẩn hóa và duy trì toàn bộ hệ thống tài liệu kỹ thuật của dự án, đảm bảo tính liên kết xuyên suốt, nhất quán và phản ánh chính xác 100% hiện trạng mã nguồn thực tế của hệ thống.

## Inputs
Đọc toàn bộ kết quả của các giai đoạn phát triển:
- `docs/customer-requirement.md`
- `docs/requirements.md`
- `docs/user-stories.md`
- `docs/acceptance-criteria.md`
- `docs/requirements-issues.md`
- `docs/architecture.md`
- `docs/architecture-decisions.md`
- `docs/chatbot-architecture.md`
- `docs/chatbot-data-flow.md`
- `docs/database-design.md`
- `docs/test-plan.md`
- `docs/test-report.md`
- `docs/code-review.md`
- `docs/security-review.md`

## Process / Workflow
1. **Xây dựng Tài liệu API (API Specification)**:
   - Đặc tả chuẩn OpenAPI/RESTful cho toàn bộ các endpoint Web và AI: Method, URL, Header, Request Body, Response JSON, Status Codes (`docs/api.md`).
2. **Xây dựng Hướng dẫn Triển khai (Deployment Guide)**:
   - Hướng dẫn cài đặt môi trường cục bộ (Python venv), thiết lập biến môi trường `.env`, hướng dẫn đóng gói và chạy Docker / Docker Compose (`docs/deployment.md`).
3. **Xây dựng Cẩm nang Sử dụng (User Guide)**:
   - Cẩm nang thao tác trực quan từng bước cho Quản trị viên (Admin), Nhân viên soát vé (Staff) và Người tham dự (Attendee) kèm hướng dẫn khai thác Trợ lý AI (`docs/user-guide.md`).
4. **Xây dựng Ma trận Truy vết (Traceability Matrix)**:
   - Thiết lập bảng ánh xạ liên kết 2 chiều từ Yêu cầu Nghiệp vụ (FR/NFR) -> User Stories -> Kiến trúc -> Bảng CSDL -> Mã nguồn Service/Route -> Ca kiểm thử Pytest -> Kết quả Đánh giá (`docs/traceability-matrix.md`).
5. **Cập nhật Tổng quan Dự án (`README.md`)**:
   - Cập nhật mô tả hệ thống, kiến trúc tổng quát, danh mục skills, hướng dẫn khởi chạy nhanh và cấu trúc thư mục chuẩn.

## Rules & Constraints
- Tài liệu phải phản ánh đúng 100% mã nguồn thực tế đang hoạt động.
- Tuyệt đối không mô tả các tính năng chưa được hiện thực hóa (No phantom documentation).

## Outputs
Khởi tạo và duy trì:
- `README.md`
- `docs/api.md`
- `docs/deployment.md`
- `docs/user-guide.md`
- `docs/traceability-matrix.md`
