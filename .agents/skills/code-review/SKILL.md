---
name: code-review
description: Skill thẩm định chất lượng mã nguồn độc lập, kiểm tra tính tuân thủ yêu cầu và kiến trúc, phát hiện code smells, duplicate code và đánh giá mức độ rủi ro (CRITICAL, HIGH, MEDIUM, LOW).
---

# Code Review Skill

## 1. Purpose

Skill này hướng dẫn AI Agent thực hiện thẩm định chất lượng mã nguồn độc lập (Independent Code Review) trong hệ thống `EventAI Pro`. Agent đóng vai trò là Senior Code Reviewer rà soát mã nguồn trước khi merge hoặc deploy, đảm bảo tính tuân thủ kiến trúc, tối ưu hiệu năng truy vấn, loại trừ rủi ro bảo mật OWASP, phát hiện mã trùng lặp (DRY) và các điểm thắt cổ chai tiềm ẩn.

## 2. Scope

- Rà soát toàn bộ các thay đổi mã nguồn trong [app/routes/](file:///d:/Event_Management_AI/app/routes/), [app/models/](file:///d:/Event_Management_AI/app/models/), [app/services/](file:///d:/Event_Management_AI/app/services/), [app/agents/](file:///d:/Event_Management_AI/app/agents/) và [tests/](file:///d:/Event_Management_AI/tests/).
- Đánh giá mã nguồn theo 8 tiêu chuẩn cốt lõi: Tính đúng đắn (Correctness), Tuân thủ kiến trúc (Architecture), An toàn bảo mật (Security), Hiệu năng (Performance), Khả năng bảo trì (Maintainability), Độ bao phủ kiểm thử (Test Coverage), Xử lý lỗi (Error Handling) và Hợp đồng API (API Contracts).
- Phân loại mức độ rủi ro của từng phát hiện thành 4 cấp độ: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- Lập báo cáo thẩm định mã nguồn chi tiết và đưa ra hướng dẫn khắc phục cụ thể.

## 3. Non-Scope

- Không trực tiếp sửa đổi mã nguồn trong phiên review (việc sửa đổi do skill `implementation` thực hiện).
- Không thay thế việc chạy kiểm thử tự động (thuộc skill `testing`).

## 4. When to Use

- Sau khi hoàn thành một tính năng mới hoặc một lượt sửa lỗi mã nguồn từ `implementation`.
- Trước khi thực hiện release hoặc merge vào nhánh chính (`main`).
- Khi tiến hành audit chất lượng định kỳ cho toàn bộ repository.

## 5. When NOT to Use

- Khi yêu cầu tính năng còn chưa được chốt (phải dùng `requirements-analysis`).
- Khi chỉ kiểm tra lỗi chính tả trong file markdown (dùng `documentation`).

## 6. Required Context

Agent cần nắm vững:

- Phong cách lập trình Python (PEP 8), nguyên tắc SOLID và Clean Code.
- Các quy chuẩn cụ thể của dự án:
  - Cú pháp SQLAlchemy 2.0 (`db.session.get()`, `db.get_or_404()`).
  - Hàm thời gian `utc_now()`.
  - Phân quyền RBAC 4 vai trò qua `@role_required`.
  - Fallback an toàn của AI Gateway (`gemini_service.py`).
- 10 lỗ hổng bảo mật phổ biến nhất của OWASP Web và OWASP for LLMs.

## 7. Source Files to Inspect

Trong mỗi phiên review, Agent PHẢI kiểm tra:

- Tệp mã nguồn có thay đổi (Git Diff hoặc danh sách tệp được chỉ định).
- [app/routes/](file:///d:/Event_Management_AI/app/routes/): Kiểm tra controller logic, xác thực quyền và định dạng response.
- [app/models/](file:///d:/Event_Management_AI/app/models/): Kiểm tra relationships, nullability, cascading.
- [app/services/](file:///d:/Event_Management_AI/app/services/): Kiểm tra thuật toán, gọi API LLM, xử lý timeout.
- [tests/](file:///d:/Event_Management_AI/tests/): Kiểm tra test case đi kèm có thực sự verify được hành vi không.

## 8. Related Documentation

- [docs/code-review.md](file:///d:/Event_Management_AI/docs/code-review.md): Báo cáo thẩm định mã nguồn độc lập của dự án.
- [docs/architecture.md](file:///d:/Event_Management_AI/docs/architecture.md): Ranh giới kiến trúc 3 tầng chuẩn.
- [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md): Chuẩn mô hình 3NF.
- [docs/security-review.md](file:///d:/Event_Management_AI/docs/security-review.md): Ma trận kiểm toán an ninh.

## 9. Related Skills

- `implementation`: Nhận mã nguồn cần review và gửi lại phản hồi sửa đổi.
- `security-review`: Phối hợp rà soát sâu các lỗ hổng an ninh ứng dụng.
- `testing`: Xác minh các ca kiểm thử hồi quy tương ứng.
- `documentation`: Ghi nhận kết quả review vào báo cáo.

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Đọc diff và ngữ cảnh)

1. Đọc git diff hoặc nội dung tệp vừa thay đổi.
2. Đọc file tests tương ứng để xem tác giả đã kiểm tra những kịch bản nào.
3. Đọc User Story / AC liên quan để đối chiếu mục tiêu nghiệp vụ.

### Bước 2: ANALYZE (Thẩm định theo 8 tiêu chuẩn cốt lõi)

1. **Tính đúng đắn (Correctness)**:
   - Logic có xử lý đúng mọi luồng chính và luồng nhánh (if/else) không?
   - Có rủi ro chia cho 0, null pointer (NoneType), hoặc chỉ số vượt mảng không?
2. **Tuân thủ Kiến trúc (Architecture)**:
   - Route có bị "béo phì" (Fat Controller) chứa quá nhiều logic tính toán không?
   - Có vi phạm ranh giới tầng không?
3. **An toàn Bảo mật (Security)**:
   - Có câu lệnh nối chuỗi SQL thô nào không?
   - Route có decorator bảo vệ phân quyền không?
   - Có dữ liệu PII bị in thô vào log không?
4. **Hiệu năng & ORM (Performance)**:
   - Có lỗi N+1 Query trong vòng lặp không? (Dùng `joinedload` nếu cần).
   - Có sử dụng phương thức legacy `Model.query.get()` gây cảnh báo không?
5. **Xử lý Ngoại lệ (Error Handling)**:
   - Khối `try...except` có bắt exception quá rộng (`except: pass`) làm nuốt lỗi không?
   - Đã có `db.session.rollback()` khi ghi CSDL thất bại chưa?
6. **Kiểm thử (Tests)**:
   - Đã có test case cho cả kịch bản thành công lẫn thất bại (Edge Cases) chưa?
   - Test có kiểm tra assertion thực tế không hay chỉ gọi hàm?

### Bước 3: PLAN (Xếp hạng mức độ nghiêm trọng)

- **CRITICAL**: Lỗ hổng bảo mật nghiêm trọng (SQLi, bypass RBAC), làm sập server, rò rỉ API key, làm hỏng dữ liệu.
- **HIGH**: Logic nghiệp vụ sai lệch, mất mát giao dịch, lỗi N+1 query trên tập dữ liệu lớn, thiếu rollback.
- **MEDIUM**: Code smells, vi phạm DRY, thiếu validate đầu vào, sử dụng deprecated API (`Query.get`).
- **LOW**: Đặt tên biến chưa chuẩn, thiếu docstring, định dạng mã nguồn không nhất quán.

### Bước 4: MODIFY (Lập báo cáo thẩm định mã nguồn)

1. Tổng hợp các phát hiện thành bảng đánh giá chi tiết:
   `| STT | Vị trí (File:Line) | Mức độ | Tiêu chuẩn | Vấn đề phát hiện | Khuyến nghị khắc phục |`

2. Cập nhật vào [docs/code-review.md](file:///d:/Event_Management_AI/docs/code-review.md).
3. Đưa ra kết luận rõ ràng: **APPROVED** hoặc **CHANGES_REQUESTED**.

### Bước 5: VERIFY (Xác nhận khắc phục)

1. Sau khi developer sửa theo khuyến nghị, Agent review lại lần 2.
2. Chạy lại test suite để đảm bảo mã nguồn đạt chuẩn 100%.

## 11. Validation

Báo cáo Review phải thỏa mãn:

- [ ] Mọi nhận xét đều chỉ rõ tệp (`File`), dòng code (`LineNumber`) và đoạn mã cụ thể.
- [ ] Mọi khuyến nghị đều đưa ra giải pháp thay thế cụ thể (kèm code snippet ví dụ).
- [ ] Không có nhận xét chung chung vô căn cứ như "code chưa tối ưu" mà không nêu rõ vì sao.
- [ ] Đạt chuẩn phê duyệt không còn bất kỳ phát hiện mức `CRITICAL` hay `HIGH` nào.

## 12. Failure Handling

- **Khi tác giả không đồng ý với nhận xét**: Mở thảo luận dựa trên bằng chứng kỹ thuật (chạy benchmark đo thời gian, chứng minh bằng test case tái hiện bug). Nếu không thống nhất, ghi nhận thành `UNRESOLVED CONFLICT`.

## 13. Security Considerations

- Reviewer có quyền phủ quyết (VETO) đối với bất kỳ thay đổi nào làm suy yếu cơ chế RBAC, để lộ secret key hoặc cho phép input chưa lọc đi vào truy vấn SQL hay prompt LLM.

## 14. Expected Output

1. Báo cáo đánh giá mã nguồn chi tiết trong [docs/code-review.md](file:///d:/Event_Management_AI/docs/code-review.md).
2. Danh sách các action items cụ thể cho giai đoạn `implementation`.

## 15. Completion Criteria

- 100% các dòng code thay đổi được rà soát.
- 0 lỗi `CRITICAL` và `HIGH` tồn đọng.
- Quyết định phê duyệt (APPROVED) được ban hành chính thức.

## 16. Maintenance Notes

- Cập nhật checklist review khi dự án bổ sung công nghệ mới (ví dụ: caching Redis, message broker RabbitMQ).
- Rà soát định kỳ các lỗi thường gặp trong đội ngũ để đưa vào checklist tự động hóa.
