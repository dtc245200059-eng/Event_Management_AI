# AI Chatbot Data Flow Diagram (DFD) Specification
**Hệ Thống**: Phân Hệ Trợ Lý Ảo RAG Sự Kiện (Event AI Assistant Subsystem)  
**Tài Liệu Tham Chiếu**: `docs/chatbot-architecture.md`, `docs/architecture.md`  
**Giai Đoạn**: Architecture Design

---

## 1. Sơ Đồ Luồng Dữ Liệu Mức 0 (DFD Level 0 - Context Diagram)

Sơ đồ ngữ cảnh thể hiện ranh giới tương tác giữa các thực thể ngoại vi (Attendee, External Gemini API) và Hệ thống Quản lý Sự kiện Tích hợp AI.

```
                  ┌─────────────────────────────────────────┐
                  │          NGƯỜI THAM DỰ (ATTENDEE)       │
                  └────────────────────┬────────────────────┘
                                       │ (1) Câu hỏi ngôn ngữ tự nhiên
                                       │ (6) Câu trả lời Grounded Response
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │                 HỆ THỐNG                │
                  │         QUẢN LÝ SỰ KIỆN TÍCH HỢP AI     │
                  │        (EVENT MANAGEMENT AI SYSTEM)     │
                  └───────┬─────────────────────────┬───────┘
                          │                         │
            (3) SQL Query │ (4) DB Records          │ (5) Final Prompt
            (Parameterized)                         │ (6) Generated Text
                          ▼                         ▼
            ┌───────────────────────┐     ┌───────────────────────┐
            │   CSDL QUAN HỆ 3NF    │     │   GOOGLE GEMINI 2.0   │
            │ (SQLITE / POSTGRESQL) │     │      FLASH API        │
            └───────────────────────┘     └───────────────────────┘
```

---

## 2. Sơ Đồ Luồng Dữ Liệu Mức 1 (DFD Level 1 - Chatbot Subsystem Decomposition)

Phân rã luồng xử lý bên trong phân hệ Chatbot thành 4 tiến trình chính.

```
                                  [ NGƯỜI THAM DỰ ]
                                          │
                     1. Câu hỏi tự nhiên  │ 8. Câu trả lời hoàn chỉnh
                                          ▼
                               ┌─────────────────────┐
                               │ 1.0 Tiếp Nhận &     │
                               │ Phân Tích Ý Định    │
                               │ (Question Analyzer) │
                               └──────────┬──────────┘
                                          │
                                          │ 2. Structured Intent IR
                                          ▼
                               ┌─────────────────────┐
                               │ 2.0 Truy Xuất Dữ    │◄──────── (D1) CSDL Sự Kiện:
                               │ Liệu Cốt Lõi        │            - events
                               │ (Event Retriever)   │─────────►  - schedules
                               └──────────┬──────────┘            - speakers, venues
                                          │                       - tickets
                                          │ 3. Raw Data Records
                                          ▼
                               ┌─────────────────────┐
                               │ 3.0 Xây Dựng Khối   │
                               │ Ngữ Cảnh & Prompt   │
                               │ (Context & Prompt)  │
                               └──────────┬──────────┘
                                          │
                                          │ 4. Grounded Prompt
                                          ▼
                               ┌─────────────────────┐
                    ┌─────────►│ 4.0 Sinh Câu Trả Lời│◄─────────┐
                    │          │ (Inference Engine)  │          │
                    │          └─────────────────────┘          │
                    │ 5. API Call            │                  │ 7. Template Matching
                    ▼ 6. Text Response       │                  │    (No Internet)
          [ GOOGLE GEMINI API ]              │         [ OFFLINE FALLBACK MOCK ]
             (Online Engine)                 │              (Offline Engine)
                                             │
                                             ▼
                                  (D2) Lịch Sử Chatbot:
                                   - ai_chat_history
```

---

## 3. Sơ Đồ Luồng Dữ Liệu Mức 2 (DFD Level 2 - Detailed RAG Pipeline)

Mô tả chi tiết sự biến đổi của gói tin dữ liệu qua từng bước xử lý.

```
[BƯỚC 1: INPUT NGƯỜI DÙNG]
User Question: "Có phiên hội thảo nào về AI vào sáng mai không?"
     │
     ▼
[BƯỚC 2: TIẾN TRÌNH 1.0 - QUESTION ANALYZER]
Output Intent JSON:
{
  "intent": "schedule_query",
  "event_id": 1,
  "entities": {
    "keywords": ["AI", "hội thảo"],
    "time_filter": "sáng mai"
  }
}
     │
     ▼
[BƯỚC 3: TIẾN TRÌNH 2.0 - EVENT RETRIEVER]
SQL Query Thực Thi:
SELECT s.title, s.start_time, s.end_time, sp.name, v.room_name 
FROM schedules s 
JOIN speakers sp ON s.speaker_id = sp.id 
JOIN venues v ON s.venue_id = v.id 
WHERE s.event_id = 1 AND s.title LIKE '%AI%';
     │
     ▼
[BƯỚC 4: TIẾN TRÌNH 3.0 - CONTEXT & PROMPT BUILDER]
Retrieved Context String:
"LỊCH TRÌNH: Phiên 'Workshop GenAI' diễn ra lúc 09:00 - 11:30 | Diễn giả: TS. Lê Quang Dũng | Phòng: Hội trường A"

Formatted Final Prompt:
"HÃY ĐÓNG VAI: Event Assistant.
CONTEXT: [Dữ liệu trích xuất ở trên]
CONSTRAINTS: Chỉ trả lời dựa trên CONTEXT, không tự bịa thông tin.
CÂU HỎI: Có phiên hội thảo nào về AI vào sáng mai không?"
     │
     ▼
[BƯỚC 5: TIẾN TRÌNH 4.0 - DUAL-ENGINE INFERENCE]
- Chế độ Online: Gemini 2.0 tổng hợp câu văn tự nhiên và lịch sự.
- Chế độ Offline Fallback: Trích xuất trực tiếp câu trả lời từ Context String.
     │
     ▼
[BƯỚC 6: OUTPUT TRẢ VỀ CLIENT]
JSON Response:
{
  "answer": "Vào sáng mai có phiên 'Workshop GenAI' diễn ra từ 09:00 đến 11:30 tại Hội trường A do TS. Lê Quang Dũng trình bày.",
  "mode": "live",
  "latency": 1.45
}
```
