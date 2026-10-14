# AI Chatbot Subsystem Architecture Specification
**Hệ Thống**: Phân Hệ Trợ Lý Ảo RAG Sự Kiện (Event AI Assistant Subsystem)  
**Trạng Thái Triển Khai**: `[IMPLEMENTED]` (Đã hoàn thiện mã nguồn tại `rag_service.py`, `gemini_service.py`, test pass 100%)  
**Tài Liệu Tham Chiếu**: `docs/architecture.md`, `docs/requirements.md`, `docs/api.md`  
**Kỹ Năng Quản Trị**: [`rag-prompt`](file:///d:/Event_Management_AI/.agents/skills/rag-prompt/SKILL.md), [`context-builder`](file:///d:/Event_Management_AI/.agents/skills/context-builder/SKILL.md), [`question-analysis`](file:///d:/Event_Management_AI/.agents/skills/question-analysis/SKILL.md), [`event-retrieval`](file:///d:/Event_Management_AI/.agents/skills/event-retrieval/SKILL.md)

---

## 1. Tổng Quan Phân Hệ RAG Chatbot

Phân hệ Trợ lý ảo RAG Chatbot đóng vai trò giải quyết **Điểm nghẽn số 1 (Phân mảnh thông tin sự kiện & tài nguyên)** bằng cách cung cấp giao diện hội thoại tự nhiên 24/7 cho người tham dự.

Kiến trúc phân hệ được thiết kế theo nguyên tắc **Retrieval-Augmented Generation (RAG) 4 Tầng** kết hợp cơ chế kiểm soát rủi ro **Dual-Engine (Online Gemini & Offline Fallback Mock)**.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                            NGƯỜI THAM DỰ (ATTENDEE)                      │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Câu hỏi tiếng Việt ("Lịch trình AI Summit?")
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   1. GIAO DIỆN CHATBOT (CHATBOT UI & API)                │
│   - Bottom Sheet di động & Modal nổi (`app/templates/base.html`)         │
│   - Workspace AI toàn màn hình (`app/templates/ai/chat_workspace.html`)  │
│   - Tự động cuộn, trạng thái gõ (Typing Indicator), render thẻ sự kiện   │
│   - Endpoint điều phối: `POST /ai/chat` & `POST /api/ai/chat`            │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   2. BỘ PHÂN TÍCH Ý ĐỊNH (QUESTION ANALYZER)             │
│   - Phân loại Intent: schedule / speaker / ticket / venue / general      │
│   - Trích xuất Entity: event_code, speaker_name, ticket_type, keywords   │
│   - Xuất cấu trúc Intermediate Representation (IR JSON)                  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ IR JSON
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   3. BỘ TRUY XUẤT SỰ KIỆN (EVENT RETRIEVER)              │
│   - Parameterized Queries an toàn qua SQLAlchemy Models                  │
│   - Truy vấn 5 bảng: Events, Schedules, Speakers, Venues, Tickets        │
│   - Chỉ trích xuất dữ liệu của sự kiện liên quan (Data Isolation)        │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Raw DB Records
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   4. BỘ XÂY DỰNG NGỮ CẢNH (CONTEXT BUILDER)              │
│   - Chuẩn hóa Markdown, format bảng vé, timeline lịch trình              │
│   - Loại bỏ dữ liệu PII và ID kỹ thuật nội bộ                            │
│   - Kiểm soát dung lượng Token Budgeting (< 1.500 tokens)                │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Grounded Context
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   5. BỘ ĐÓNG GÓI CHỈ DẪN (RAG PROMPT BUILDER)            │
│   - System Instructions: "Bạn là Event AI Assistant..."                  │
│   - Strict Grounding Rule: "CHỈ trả lời dựa trên CONTEXT, KHÔNG bịa..."  │
│   - Few-shot Examples & Output Format Markdown                           │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Final Prompt
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│               6. ĐIỀU PHỐI MÔ HÌNH (DUAL-MODE INFERENCE ENGINE)          │
├──────────────────────────────────────┬───────────────────────────────────┤
│ [CHẾ ĐỘ ONLINE - PRIMARY]            │ [CHẾ ĐỘ OFFLINE - FALLBACK]       │
│ - Gọi Google Gemini 2.0 Flash API    │ - Tự động kích hoạt khi mất mạng  │
│ - Phản hồi tự nhiên, linh hoạt       │   hoặc lỗi Gemini API Key         │
│ - Độ trễ trung bình: 1.5s - 2.5s     │ - Ghép mẫu câu từ Ground Truth DB │
│                                      │ - Độ trễ cực thấp (< 50ms)        │
└──────────────────────────────────────┴───────────────────────────────────┘
                                     │
                                     ▼
                              CÂU TRẢ LỜI CHUẨN XÁC
```

---

## 2. Chi Tiết Các Thành Phần Cốt Lõi

### 2.1. Question Analyzer (`app/services/rag_service.py`)
Nhiệm vụ chuyển đổi ngôn ngữ tự nhiên không cấu trúc thành cấu trúc máy hiểu được:
- Nhận diện các mẫu câu hỏi về lịch trình (timeline, thời gian, mấy giờ, diễn ra khi nào).
- Nhận diện các câu hỏi về diễn giả (ai nói, chuyên gia nào, thông tin speaker).
- Nhận diện các câu hỏi về giá vé và quyền lợi (vé bao nhiêu tiền, vé VIP gồm gì, còn vé không).
- Nhận diện các câu hỏi về địa điểm (ở đâu, phòng nào, hướng dẫn đường đi).

### 2.2. Event Retriever & Data Barrier
- Thực hiện truy vấn có lọc tham số (`WHERE event_id = ? AND status = 'published'`).
- Không bao giờ truyền chuỗi User Input trực tiếp vào câu lệnh SQL raw.
- Không truy vấn các bảng chứa dữ liệu nhạy cảm như `users` (chứa password hash) hay `registrations` (chứa thông tin cá nhân của người khác).

### 2.3. Context Builder & Token Budgeting
- Xây dựng một khối văn bản ngữ cảnh rõ ràng:
  ```
  [SỰ KIỆN]: Vietnam AI Summit 2026 (EVT-2026-AI)
  - Thời gian: 15/10/2026 08:00 - 15/10/2026 17:00
  - Địa điểm: Trung tâm Hội nghị Quốc gia, Hà Nội
  [LỊCH TRÌNH & DIỄN GIẢ]:
  + 08:30 - 09:30: Khai mạc & Keynote AI | Diễn giả: TS. Lê Quang Dũng | Phòng: Hội trường Grand A
  + 09:45 - 11:30: Workshop LLM & RAG | Diễn giả: ThS. Ngô Xuân Thuỷ | Phòng: Phòng Hội thảo B2
  [BẢNG GIÁ VÉ & QUOTA]:
  + Vé Miễn Phí (free): 0 VNĐ | Còn lại: 45/50
  + Vé Tiêu Chuẩn (standard): 200,000 VNĐ | Còn lại: 80/100
  + Vé VIP (vip): 500,000 VNĐ | Còn lại: 15/20
  ```

### 2.4. Anti-Hallucination Prompt Architecture (5 Thành Phần)
Prompt được định nghĩa nghiêm ngặt:
1. **Role**: Chuyên gia tư vấn sự kiện tận tâm và chuyên nghiệp.
2. **Context**: Đoạn trích xuất từ Context Builder.
3. **Constraints**:
   - Nếu câu hỏi nằm ngoài Context: Trả lời "Dạ, hiện tại Ban tổ chức chưa công bố thông tin này..."
   - Tuyệt đối không tự ý bịa tên diễn giả, không tự ý giảm giá vé.
4. **Few-shots**: Mẫu câu hỏi và câu trả lời ngắn gọn.
5. **Output**: Tiếng Việt chuẩn mực, định dạng Markdown rõ ràng.

### 2.5. Offline Fallback Mock Engine
- Xử lý các tình huống ngoại lệ mạng hoặc hết hạn ngạch API.
- Tự động trích xuất các trường tương ứng trong Context để tạo câu trả lời mẫu mà không cần kết nối Internet.
- Ghi nhận trạng thái `mode: "mock"` trong JSON phản hồi để hỗ trợ việc kiểm thử và theo dõi chất lượng.
