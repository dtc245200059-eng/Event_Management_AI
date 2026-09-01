---
name: question-analysis
description: Skill phân tích ý định (Intent Classification) và trích xuất thực thể (Entity Extraction) từ câu hỏi ngôn ngữ tự nhiên của người dùng về sự kiện, diễn giả, lịch trình hoặc giá vé.
---

# Question Analysis Skill

## Objective
Phân tích câu hỏi tự nhiên bằng tiếng Việt của người dùng thành cấu trúc Intent và Entities chuẩn hóa (Intermediate Representation - IR), làm tiền đề cho việc truy vấn cơ sở dữ liệu chính xác và không bị suy đoán sai lệch.

## Inputs
- Câu hỏi ngôn ngữ tự nhiên của người dùng (Ví dụ: *"Có phiên hội thảo nào về AI vào sáng mai không?"*, *"Giá vé VIP là bao nhiêu?"*).

## Process / Workflow
1. **Phân loại Ý định (Intent Classification)**:
   - `schedule_query`: Hỏi về mốc thời gian, phiên khai mạc, timeline, phòng họp.
   - `speaker_query`: Hỏi về thông tin diễn giả, chức danh, kinh nghiệm, bài chia sẻ.
   - `ticket_query`: Hỏi về các hạng vé, giá vé, số lượng còn lại, cách mua.
   - `venue_query`: Hỏi về địa điểm, phòng hội thảo, vị trí tổ chức, hình thức Online/Offline.
   - `general_query`: Chào hỏi, thông tin chung về ban tổ chức hoặc sự kiện.
2. **Trích xuất Thực thể (Entity Extraction)**:
   - `event_name` / `event_code`: Tên hoặc mã sự kiện (ví dụ: *Vietnam AI Summit 2026*).
   - `speaker_name`: Tên diễn giả (ví dụ: *TS. Lê Quang Dũng*).
   - `ticket_type`: Hạng vé (ví dụ: *VIP*, *Standard*, *Free*).
   - `time_filter`: Thời gian (ví dụ: *sáng mai*, *ngày 15/10*).
   - `keywords`: Từ khóa tìm kiếm trọng tâm.
3. **Chuẩn hóa Đầu ra (Structured Intent JSON)**:
   - Xuất dữ liệu JSON có cấu trúc rõ ràng truyền sang module `event-retrieval`.

## Rules & Constraints
- Không tự ý bịa đặt tên diễn giả, địa điểm hoặc sự kiện không có trong câu hỏi.
- Không tự suy đoán giá vé nếu người dùng chưa hỏi hoặc dữ liệu không tồn tại.
- Nếu câu hỏi mơ hồ, thiết lập `intent = "general_query"` và giữ nguyên từ khóa tìm kiếm.

## Outputs
- Cấu trúc dữ liệu JSON Intent.
- Tài liệu đặc tả `docs/question-analysis.md`.
