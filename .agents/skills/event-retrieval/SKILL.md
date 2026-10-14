---
name: event-retrieval
description: Skill truy xuất dữ liệu có cấu trúc từ CSDL (bảng events, schedules, speakers, venues, tickets, faqs) dựa trên ý định câu hỏi và bộ lọc sự kiện bằng Parameterized Queries an toàn và xử lý trạng thái rỗng tin cậy.
---

# Event Retrieval Skill

## 1. Purpose

Skill này hướng dẫn AI Agent thực hiện truy xuất dữ liệu có cấu trúc từ cơ sở dữ liệu SQLite trong hệ thống `EventAI Pro`. Dựa trên kết quả phân tích ý định từ `question-analysis`, Agent lựa chọn và thực thi các câu truy vấn an toàn (Parameterized Queries hoặc ORM queries) trên các bảng `events`, `schedules`, `speakers`, `venues`, `tickets` và `event_faqs`, đồng thời đảm bảo xử lý trạng thái rỗng (Empty State) một cách chuyên nghiệp, không bao giờ để lọt giá trị rác hoặc lỗi ra ngoài.

## 2. Scope

- Tiếp nhận tham số đầu vào: `event_id`, `intent` (`schedule`, `ticket`, `speaker`, `venue`, `faq`, `general`), từ khóa tìm kiếm và tiêu chí lọc.
- Thực thi truy xuất dữ liệu từ các ORM Models hoặc các hàm truy vấn có tham số trong:
  - [app/services/rag_service.py](file:///d:/Event_Management_AI/app/services/rag_service.py): Truy xuất dữ liệu phục vụ RAG Chatbot.
  - [app/services/multi_agent/database_service.py](file:///d:/Event_Management_AI/app/services/multi_agent/database_service.py): Truy xuất dữ liệu phục vụ Multi-Agent RetrievalAgent.
- Xử lý sắp xếp và giới hạn kết quả (Sorting & Limiting) để tối ưu kích thước ngữ cảnh (Token Optimization).
- Xử lý trạng thái rỗng (Empty States): Trả về thông báo chuẩn xác khi không tìm thấy dữ liệu, loại trừ tuyệt đối các lỗi hiển thị như `[object Object]`, `None`, `null`.

## 3. Non-Scope

- Không trực tiếp gọi API Gemini để sinh văn bản (thuộc skill `rag-prompt`).
- Không phân tích cú pháp ngôn ngữ tự nhiên từ chuỗi thô (thuộc skill `question-analysis`).
- Không thay đổi cấu trúc bảng CSDL (thuộc skill `database-design`).

## 4. When to Use

- Khi dịch vụ RAG `/ai/chat` cần lấy dữ liệu thực tế (Ground Truth) để đưa vào prompt.
- Khi tác tử `RetrievalAgent` trong Multi-Agent Pipeline cần gọi SQL Tool.
- Khi cần kiểm tra tính chính xác và an toàn của các câu truy vấn đọc dữ liệu sự kiện.

## 5. When NOT to Use

- Khi thực hiện các thao tác ghi dữ liệu CSDL (`INSERT`, `UPDATE`, `DELETE`) trong luồng đặt vé hay check-in (dùng `implementation`).
- Khi chỉ tìm kiếm toàn văn phi cấu trúc trên tài liệu ngoài CSDL (dùng Vector Search).

## 6. Required Context

Agent cần nắm vững:

- Cấu trúc 11 bảng CSDL trong [app/models/](file:///d:/Event_Management_AI/app/models/).
- Mối quan hệ giữa các bảng:
  - `Event` 1-N `Schedule`, `Ticket`, `EventFAQ`, `Registration`.
  - `Schedule` N-1 `Speaker`, `Venue`.
- Nguyên tắc an toàn: 100% câu truy vấn phải sử dụng SQLAlchemy ORM hoặc Parameterized Queries (`WHERE id = :event_id`), cấm tuyệt đối nối chuỗi SQL bằng f-string.

## 7. Source Files to Inspect

Trước khi tối ưu hoặc viết hàm truy xuất, Agent PHẢI kiểm tra:

- [app/services/rag_service.py](file:///d:/Event_Management_AI/app/services/rag_service.py): Các hàm đọc dữ liệu sự kiện và FAQs.
- [app/services/multi_agent/database_service.py](file:///d:/Event_Management_AI/app/services/multi_agent/database_service.py): Các hàm `search_events_sql`, `get_event_full_details_sql`.
- [app/models/](file:///d:/Event_Management_AI/app/models/): `event.py`, `schedule.py`, `speaker.py`, `venue.py`, `ticket.py`, `faq.py`.
- [tests/test_ai_services.py](file:///d:/Event_Management_AI/tests/test_ai_services.py): Ca kiểm thử `test_rag_context_and_free_event_retrieval`, `test_rag_faq_retrieval`.

## 8. Related Documentation

- [docs/chatbot-architecture.md](file:///d:/Event_Management_AI/docs/chatbot-architecture.md): Kiến trúc luồng truy xuất dữ liệu RAG.
- [docs/database-design.md](file:///d:/Event_Management_AI/docs/database-design.md): Lược đồ quan hệ và tên cột chuẩn.
- [docs/chatbot-data-flow.md](file:///d:/Event_Management_AI/docs/chatbot-data-flow.md): Sơ đồ luồng dữ liệu DFD.

## 9. Related Skills

- `question-analysis`: Cung cấp ý định và từ khóa lọc dữ liệu.
- `context-builder`: Tiếp nhận dữ liệu đã truy xuất để đóng gói thành văn bản ngữ cảnh.
- `database-design`: Cung cấp cấu trúc schema và khóa ngoại.
- `testing`: Viết test cases kiểm chứng các trường hợp tìm kiếm có dữ liệu và không có dữ liệu.

## 10. Workflow (READ → ANALYZE → PLAN → MODIFY → VERIFY)

### Bước 1: READ (Đọc yêu cầu truy xuất)

1. Xác định tham số đầu vào: `event_id` (có thể cụ thể hoặc `None` để tra cứu toàn bộ sự kiện mở), `intent` từ `question-analysis`.
2. Đọc model tương ứng trong `app/models/` để biết chính xác các cột cần lấy và các quan hệ cần nạp (e.g. `schedules` liên kết với `speaker` và `venue`).

### Bước 2: ANALYZE (Xác định chiến lược truy vấn)

1. **Định tuyến theo Intent**:
   - Nếu `intent == 'ticket'`: Truy vấn bảng `tickets` lọc theo `event_id` và `status != 'cancelled'`, lấy `name`, `price`, `quota`, `sold_count`, tính `remaining_quota`.
   - Nếu `intent == 'schedule'`: Truy vấn bảng `schedules` lọc theo `event_id`, sắp xếp theo `start_at ASC`, nạp thông tin `Speaker` và `Venue`.
   - Nếu `intent == 'speaker'`: Lấy danh sách diễn giả tham gia sự kiện thông qua các phiên lịch trình (`Schedule.speaker`).
   - Nếu `intent == 'faq'`: Truy vấn bảng `event_faqs` khớp câu hỏi tương đồng hoặc theo `category`.
   - Nếu `intent == 'general'` hoặc không có intent cụ thể: Nạp thông tin tổng quan của sự kiện (`title`, `description`, `start_date`, `location_address`, `category`).
2. **Tối ưu hóa hiệu năng**:
   - Sử dụng các cột đã có chỉ mục B-Tree (`event_id`, `status`).
   - Giới hạn số lượng bản ghi tối đa (`limit 20`) để tránh làm tràn context window của LLM.

### Bước 3: PLAN (Xây dựng câu truy vấn an toàn)

1. Áp dụng chuẩn SQLAlchemy ORM:

   ```python
   # Truy xuất vé khả dụng
   tickets = Ticket.query.filter_by(event_id=event_id).filter(Ticket.status != 'cancelled').all()
   ```

2. Hoặc Parameterized Query an toàn:

   ```python
   stmt = text("SELECT id, name, price, quota, sold_count FROM tickets WHERE event_id = :event_id")
   res = db.session.execute(stmt, {'event_id': event_id}).fetchall()
   ```

### Bước 4: MODIFY (Xử lý dữ liệu trả về và Trạng thái rỗng)

1. Chuyển đổi kết quả truy vấn thành cấu trúc từ điển (Dictionary) sạch sẽ, định dạng ngày tháng rõ ràng (ví dụ: `HH:MM DD/MM/YYYY`).
2. **Xử lý triệt để Trạng thái Rỗng (Empty State Handling)**:

   ```python
   if not tickets:
       return {
           'found': False,
           'data': [],
           'message': 'Hiện tại sự kiện chưa mở bán hoặc chưa có thông tin hạng vé.'
       }
   ```

3. Đảm bảo dữ liệu trả về không chứa các giá trị `None` bị chuyển thành chuỗi `"None"`.

### Bước 5: VERIFY (Kiểm chứng kết quả)

1. Chạy test cases kiểm thử truy xuất:

   ```powershell
   .venv\Scripts\python -m pytest tests/test_ai_services.py -k "test_rag_context or test_rag_faq" -v
   ```

2. Kiểm tra với các trường hợp: `event_id` hợp lệ, `event_id` không tồn tại, sự kiện không có lịch trình, sự kiện miễn phí không có vé trả phí.

## 11. Validation

Agent phải kiểm tra các tiêu chí sau:

- [ ] 100% câu truy vấn sử dụng Parameterized Query hoặc ORM, 0 rủi ro SQL Injection.
- [ ] Khi CSDL không có bản ghi phù hợp, trả về cấu trúc rỗng sạch kèm thông báo tiếng Việt lịch sự, không bao giờ trả về lỗi crash hoặc chuỗi rác.
- [ ] Dữ liệu thời gian hiển thị đúng múi giờ và định dạng dễ hiểu.
- [ ] Test cases liên quan chạy pass 100%.

## 12. Failure Handling

- **Khi kết nối CSDL bị lỗi hoặc bảng bị khóa**: Bắt ngoại lệ `SQLAlchemyError`, ghi log cảnh báo qua `current_app.logger.error`, và trả về thông báo lỗi thân thiện: `"Dữ liệu sự kiện tạm thời chưa thể truy xuất, vui lòng thử lại sau."`

## 13. Security Considerations

- Tuyệt đối không để lộ các thông tin quản trị nhạy cảm (như `password_hash`, thông tin thanh toán cá nhân, `payment_ref`) trong dữ liệu truy xuất phục vụ AI.
- Chỉ truy xuất các sự kiện ở trạng thái `published` hoặc `completed` đối với người dùng công cộng; các sự kiện `draft` chỉ truy xuất khi người dùng có quyền ban tổ chức.

## 14. Expected Output

1. Cấu trúc dữ liệu đã được làm sạch và định dạng sẵn sàng cho `context-builder`.
2. Báo cáo kiểm thử xác nhận khả năng xử lý cả trường hợp có dữ liệu và không có dữ liệu.

## 15. Completion Criteria

- Dữ liệu truy xuất chính xác 100% theo đúng thực tế trong CSDL.
- Không phát sinh lỗi runtime khi gặp dữ liệu rỗng hoặc ID không tồn tại.

## 16. Maintenance Notes

- Khi bổ sung bảng dữ liệu mới có liên quan tới sự kiện (ví dụ: bảng nhà tài trợ `sponsors`), bổ sung hàm truy xuất tương ứng vào `rag_service.py` và `database_service.py`.
