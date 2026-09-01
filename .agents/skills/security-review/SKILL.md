---
name: security-review
description: Skill kiểm toán bảo mật ứng dụng web và an toàn AI theo chuẩn OWASP Top 10 Web và OWASP Top 10 for LLMs (SQLi, XSS, CSRF, RBAC, Secret Management, PII Protection, Prompt Injection, Rate Limiting).
---

# Security Review Skill

## Objective
Thực hiện kiểm toán an ninh mạng toàn diện cho cả tầng ứng dụng Web truyền thống và tầng Dịch vụ Trí tuệ Nhân tạo (AI/LLM), bảo vệ dữ liệu định danh cá nhân (PII) và triệt tiêu các bề mặt tấn công.

## Inputs
Đọc và quét mã nguồn:
- Toàn bộ thư mục `app/`
- Tệp `.env` và `.env.example`
- Thư mục prompt `app/prompts/`
- Cấu hình mạng và API routes

## Checklist Kiểm Toán An Ninh (10 Điểm Cốt Lõi)
1. **SQL Injection (SQLi)**:
   - Đảm bảo 100% truy vấn CSDL sử dụng SQLAlchemy ORM hoặc Parameterized Queries, tuyệt đối không nối chuỗi SQL (`f"SELECT... WHERE id={user_input}"`).
2. **Cross-Site Scripting (XSS)**:
   - Jinja2 auto-escaping được bật; dữ liệu đầu vào người dùng trong template và AJAX render được lọc sạch.
3. **Cross-Site Request Forgery (CSRF)**:
   - Các form và API có kiểm tra nguồn gốc, phân tách GET (chỉ đọc) và POST/PUT/DELETE (thay đổi trạng thái).
4. **Authentication & Password Storage**:
   - Sử dụng thuật toán băm chuẩn công nghiệp PBKDF2/bcrypt có Salt thông qua `werkzeug.security`. Tuyệt đối không lưu mật khẩu dạng plain text hoặc MD5/SHA1 lỗi thời.
5. **Authorization & RBAC Access Control**:
   - Kiểm tra các decorator phân quyền (`@login_required`, `@admin_required`, `@staff_required`). Ngăn chặn lỗ hổng IDOR (Insecure Direct Object References) khi người dùng tra cứu vé hoặc đơn hàng của người khác.
6. **Secrets & API Key Protection**:
   - `GEMINI_API_KEY`, `SECRET_KEY` được lưu trong tệp biến môi trường `.env`, không bao giờ được hardcode hoặc đẩy lên Git.
7. **PII Masking & Privacy**:
   - Lọc bỏ email cá nhân, số điện thoại, mật khẩu trước khi đưa dữ liệu vào Context gửi tới LLM đám mây bên ngoài.
8. **Prompt Injection Defense**:
   - Thiết lập System Prompt cách ly nghiêm ngặt giữa System Instructions và User Input, không cho phép User Prompt ghi đè quy tắc bảo mật hệ thống.
9. **Rate Limiting & DoS Protection**:
   - Giới hạn tần suất gọi API AI để tránh cạn kiệt hạn ngạch token hoặc làm treo server.
10. **Anti-Hallucination & Offline Fallback**:
    - Cơ chế kiểm chứng dữ liệu thực tế (Grounding) buộc LLM chỉ trả lời dựa trên CSDL, tự động kích hoạt Fallback Mock an toàn khi gặp sự cố kết nối.

## Rules & Constraints
- Không tự ý sửa code trong quá trình đánh giá.
- Mỗi phát hiện bảo mật phải kèm theo bằng chứng (Evidence), mức độ nghiêm trọng (Severity) và giải pháp khắc phục triệt để.

## Outputs
Khởi tạo hoặc cập nhật:
- `docs/security-review.md`

## Verification
- Hệ thống đạt mức đánh giá An toàn (PASSED), không tồn tại lỗ hổng cấp độ CRITICAL hoặc HIGH chưa được xử lý.
