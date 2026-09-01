---
name: code-review
description: Skill thẩm định chất lượng mã nguồn độc lập, kiểm tra tính tuân thủ yêu cầu và kiến trúc, phát hiện code smells, duplicate code và đánh giá mức độ rủi ro (CRITICAL, HIGH, MEDIUM, LOW).
---

# Code Review Skill

## Objective
Thẩm định và đánh giá toàn diện chất lượng mã nguồn của hệ thống theo 8 chiều kích tiêu chuẩn kỹ thuật chuyên nghiệp, phát hiện sớm các khiếm khuyết, vi phạm kiến trúc hoặc nguy cơ suy giảm hiệu năng trước khi chuyển sang giai đoạn vận hành.

## Inputs
Đọc và rà soát toàn bộ dự án:
- Mã nguồn trong thư mục `app/`, `seed.py`, `run.py`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/database-design.md`
- `docs/test-report.md`

## 8 Tiêu Chuẩn Đánh Giá Mã Nguồn
1. **Tính Đúng Đắn (Correctness)**:
   - Code có xử lý đúng logic nghiệp vụ không? Có bắt trọn vẹn các ngoại lệ (try...except) không?
2. **Tuân Thủ Yêu Cầu (Requirements Compliance)**:
   - Code có hiện thực hóa đầy đủ 8 module quản lý cốt lõi và 4 module AI đã cam kết trong SRS không?
3. **Tuân Thủ Kiến Trúc (Architecture Compliance)**:
   - Có tuân thủ mô hình 3 tầng và tách biệt Route - Service - Model không? AI Service có bị lộ kết nối trực tiếp CSDL không?
4. **Chất Lượng Mã Nguồn & Tính Dễ Bảo Trì (Maintainability & Clean Code)**:
   - Tên biến, hàm có mang tính gợi nhớ theo chuẩn PEP 8 không? Độ dài hàm có hợp lý không?
5. **Trùng Lặp Mã (Duplication Analysis)**:
   - Các logic chung (format ngày tháng, render JSON response, kiểm tra quyền) có được tái sử dụng qua helper/decorator không?
6. **Xử Lý Lỗi & Truy Cập CSDL (Error Handling & Database Access)**:
   - Có sử dụng Parameterized Query / ORM không? Các thao tác nhạy cảm có transaction rollback không?
7. **Chất Lượng Kiểm Thử (Test Quality)**:
   - Bộ test có bao phủ các trường hợp biên và ngoại lệ không? Test có độc lập không?
8. **Rủi Ro An Toàn & Bảo Mật (Security & Risk Evaluation)**:
   - Có rò rỉ API key, băm mật khẩu sai cách hoặc thiếu kiểm tra quyền không?

## Phân Loại Mức Độ Rủi Ro (Severity Levels)
- `CRITICAL`: Lỗi nghiêm trọng đe dọa trực tiếp an ninh hệ thống, làm sập ứng dụng hoặc mất mát dữ liệu (Bắt buộc phải sửa ngay).
- `HIGH`: Vi phạm kiến trúc cốt lõi, sai lệch logic nghiệp vụ hoặc thiếu transaction rollback khi mua vé.
- `MEDIUM`: Code smell, thiếu tối ưu hiệu năng, truy vấn N+1 hoặc thiếu log ghi nhận lỗi.
- `LOW`: Vấn đề định dạng mã nguồn, cảnh báo DeprecationWarning, chính tả hoặc thiếu docstring.

## Rules & Constraints
- Không tự ý sửa code trong quá trình review.
- Mọi nhận xét phải chỉ rõ đường dẫn tệp (file path), số dòng (line numbers) và đưa ra mã code đề xuất khắc phục cụ thể.

## Outputs
Khởi tạo hoặc cập nhật:
- `docs/code-review.md`

## Verification
- Báo cáo Code Review cung cấp cái nhìn khách quan, minh bạch và có bảng tổng hợp hành động khắc phục cụ thể (Action Items).
