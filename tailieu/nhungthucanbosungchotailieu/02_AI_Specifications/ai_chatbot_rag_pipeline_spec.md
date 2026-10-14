# Đặc tả AI Chatbot RAG Pipeline

> **File:** `ai_chatbot_rag_pipeline_spec.md`
> **Chuyên gia đề xuất:** Lead AI Architect
> **Mục tiêu bổ sung:** Chương III §AI02 — FR: AI Chatbot LLM/RAG
> **Trạng thái:** Production-ready specification

---

## 1. Tổng quan

AI Chatbot sử dụng kiến trúc **Retrieval-Augmented Generation (RAG)** để trả lời câu hỏi về sự kiện. Chatbot **KHÔNG** tự do sinh văn bản mà luôn dựa trên dữ liệu thực tế từ CSDL (events, schedules, speakers, venues, tickets).

**Nguyên tắc cốt lõi:** Database-first, không Hallucination.

## 2. Kiến trúc RAG Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                      RAG CHATBOT PIPELINE                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐    │
│  │ 1. USER     │    │ 2. INPUT     │    │ 3. INTENT        │    │
│  │    INPUT     │───▶│ VALIDATION   │───▶│ CLASSIFICATION   │    │
│  │             │    │              │    │                  │    │
│  │ "Sự kiện AI │    │ • Length ≤500│    │ • event_info     │    │
│  │  diễn ra khi│    │ • Sanitize   │    │ • schedule_query │    │
│  │  nào?"      │    │ • Rate limit │    │ • speaker_query  │    │
│  └─────────────┘    └──────────────┘    │ • ticket_query   │    │
│                                         │ • venue_query    │    │
│                                         │ • general_qa     │    │
│                                         │ • greeting       │    │
│                                         │ • out_of_scope   │    │
│                                         └──────────────────┘    │
│                                                │                 │
│                                                ▼                 │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐    │
│  │ 6. RESPONSE │    │ 5. LLM       │    │ 4. CONTEXT       │    │
│  │ VALIDATION  │◀───│ GENERATION   │◀───│ RETRIEVAL        │    │
│  │ & RENDER    │    │              │    │                  │    │
│  │             │    │ • System     │    │ • SQL Query      │    │
│  │ • Markdown  │    │   Prompt     │    │ • Filter by      │    │
│  │ • Sanitize  │    │ • Context    │    │   intent entity  │    │
│  │ • Log       │    │ • User Q     │    │ • Format context │    │
│  └─────────────┘    │ • Gemini API │    │ • PII Filter     │    │
│                     └──────────────┘    └──────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 3. Chi tiết từng giai đoạn

### 3.1. Input Validation

| Rule | Giá trị | Hành động khi vi phạm |
|------|---------|----------------------|
| Max length | 500 ký tự | Truncate + warning |
| Min length | 2 ký tự | Reject: "Vui lòng nhập câu hỏi rõ ràng hơn" |
| Banned patterns | SQL injection, script tags | Strip + log attempt |
| Rate limit | 5 request/phút/user | HTTP 429 |
| Empty input | Chuỗi rỗng | Reject |

### 3.2. Intent Classification

Sử dụng **keyword matching + Gemini classification** (hybrid approach):

| Intent | Keywords / Patterns | DB Tables cần truy xuất |
|--------|-------------------|------------------------|
| `event_info` | "sự kiện", "chương trình", "hoạt động", tên sự kiện cụ thể | events |
| `schedule_query` | "lịch trình", "thời gian", "mấy giờ", "phiên", "session" | schedules, events |
| `speaker_query` | "diễn giả", "người nói", "giảng viên", tên speaker | speakers, schedules |
| `ticket_query` | "vé", "giá", "đăng ký", "mua vé", "còn vé" | tickets, events |
| `venue_query` | "địa điểm", "phòng", "ở đâu", "chỗ", "sức chứa" | venues, schedules |
| `checkin_query` | "check-in", "check in", "QR", "vào cửa" | registrations |
| `general_qa` | Không match các pattern trên | events (overview) |
| `greeting` | "xin chào", "hello", "hi" | Không cần DB |
| `out_of_scope` | "thời tiết", "tin tức", unrelated | Không cần DB |

### 3.3. Context Retrieval (Database Queries)

**Nguyên tắc:** Truy xuất dữ liệu **tại thời điểm hỏi** (realtime), không cache lâu.

#### Event Context Builder:
```python
def build_event_context(event_id=None, keyword=None):
    query = Event.query.filter(Event.status.in_(['published', 'ongoing']))

    if event_id:
        query = query.filter(Event.id == event_id)
    elif keyword:
        query = query.filter(
            or_(
                Event.title.ilike(f'%{keyword}%'),
                Event.category.ilike(f'%{keyword}%'),
                Event.tags.ilike(f'%{keyword}%')
            )
        )

    events = query.order_by(Event.start_date.asc()).limit(10).all()
    return format_events_context(events)
```

#### Context Format Template:
```
=== DỮ LIỆU SỰ KIỆN ===
{{event_context}}

=== LỊCH TRÌNH ===
{{schedule_context}}

=== DIỄN GIẢ ===
{{speaker_context}}

=== THÔNG TIN VÉ ===
{{ticket_context}}

=== ĐỊA ĐIỂM ===
{{venue_context}}
```

### 3.4. PII Filtering

Trước khi đưa vào Context cho Gemini, **bắt buộc loại bỏ**:

| Trường | Hành động |
|--------|----------|
| `attendees.email` | Không bao giờ đưa vào context |
| `attendees.phone` | Không bao giờ đưa vào context |
| `users.password_hash` | Không bao giờ đưa vào context |
| `registrations.payment_ref` | Không bao giờ đưa vào context |
| `speakers.email` | Chỉ hiển thị nếu speaker public profile |
| `speakers.phone` | Không đưa vào context |

### 3.5. Prompt Engineering

#### System Prompt (Version 3):
```
ROLE:
Bạn là Event Management Assistant — trợ lý AI của Hệ thống Quản lý Sự kiện.

CONTEXT:
Thông tin sự kiện được cung cấp bên dưới là dữ liệu CHÍNH THỨC từ hệ thống.

RULES (BẮT BUỘC TUÂN THỦ):
1. CHỈ sử dụng thông tin có trong phần DỮ LIỆU bên dưới.
2. KHÔNG BAO GIỜ tự tạo tên sự kiện, lịch trình, diễn giả, giá vé, địa điểm.
3. KHÔNG BAO GIỜ tự tạo thời gian, ngày tháng nếu không có trong dữ liệu.
4. Nếu dữ liệu KHÔNG ĐỦ để trả lời → nói rõ: "Tôi không tìm thấy thông tin này trong hệ thống."
5. KHÔNG tiết lộ email, số điện thoại, thông tin thanh toán của bất kỳ ai.
6. KHÔNG trả lời câu hỏi ngoài phạm vi sự kiện (thời tiết, tin tức, v.v.).
7. Nếu có nhiều sự kiện phù hợp, liệt kê tối đa 5 sự kiện.

OUTPUT FORMAT:
- Trả lời bằng tiếng Việt, rõ ràng, có cấu trúc.
- Sử dụng bullet points hoặc bảng khi liệt kê.
- Trích dẫn tên sự kiện chính xác từ dữ liệu.
```

#### User Prompt Template:
```
=== DỮ LIỆU HỆ THỐNG ===
{context}

=== CÂU HỎI CỦA NGƯỜI DÙNG ===
{user_question}

Hãy trả lời dựa trên dữ liệu hệ thống được cung cấp ở trên.
```

### 3.6. Response Validation

Sau khi nhận response từ Gemini, thực hiện kiểm tra:

| Check | Mô tả | Hành động nếu fail |
|-------|--------|-------------------|
| Empty response | Response rỗng | Fallback message |
| Contains PII patterns | Regex check email/phone | Strip + regenerate |
| Response too long | > 2000 ký tự | Truncate + "Xem thêm" |
| Timeout | > 3 giây | Use Fallback Mock |
| API Error | 4xx/5xx từ Gemini | Use Fallback Mock + log |

### 3.7. Fallback Mock Engine

Khi Gemini API không phản hồi:

```python
def fallback_response(intent, context):
    if intent == 'event_info':
        events = context.get('events', [])
        if events:
            return format_event_list(events)
        return "Hiện tại chưa có sự kiện nào được công bố."

    elif intent == 'schedule_query':
        return format_schedule_table(context.get('schedules', []))

    elif intent == 'greeting':
        return "Xin chào! Tôi là Event Assistant. Hiện tại AI đang bảo trì, nhưng tôi vẫn có thể hiển thị thông tin sự kiện từ hệ thống."

    else:
        return "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau hoặc liên hệ ban tổ chức."
```

## 4. API Contract: Flask Route ↔ RAG Service

### 4.1. Request

```
POST /api/ai/chat
Content-Type: application/json
X-Session-Token: <user_session>
```

**Request Body:**
```json
{
    "message": "Hội thảo AI diễn ra khi nào?",
    "event_id": null,
    "conversation_history": [
        {
            "role": "user",
            "content": "Có sự kiện nào về AI không?"
        },
        {
            "role": "assistant",
            "content": "Có, hiện tại có 3 sự kiện liên quan đến AI..."
        }
    ],
    "max_context_events": 5
}
```

### 4.2. Response (Success — 200 OK)

```json
{
    "status": "success",
    "response": {
        "message": "Hội thảo **AI và Machine Learning 2026** sẽ diễn ra vào:\n\n- **Ngày:** 15/11/2026\n- **Thời gian:** 09:00 — 17:00\n- **Địa điểm:** Hội trường A, ICTU\n\n**Lịch trình chính:**\n1. 09:00 - 10:30: Keynote — AI trong thực tiễn (TS. Nguyễn Văn A)\n2. 10:45 - 12:00: Workshop — Xây dựng chatbot với LLM\n3. 14:00 - 15:30: Panel Discussion — Tương lai AI\n\nBạn có muốn biết thêm về vé hoặc diễn giả không?",
        "intent_detected": "schedule_query",
        "sources_used": ["events", "schedules", "speakers", "venues"],
        "response_mode": "live",
        "confidence": "high"
    },
    "metadata": {
        "model_name": "gemini-2.0-flash",
        "latency_ms": 1850,
        "context_tokens": 1200,
        "response_tokens": 280,
        "chat_history_id": 456
    }
}
```

### 4.3. Response (Fallback — 200 OK)

```json
{
    "status": "success",
    "response": {
        "message": "Hiện tại AI đang bảo trì. Dựa trên dữ liệu hệ thống:\n\nCó **3 sự kiện** liên quan đến 'AI':\n1. Hội thảo AI và Machine Learning 2026 — 15/11/2026\n2. Workshop Deep Learning — 22/11/2026\n3. AI Summit Thái Nguyên — 01/12/2026",
        "intent_detected": "event_info",
        "sources_used": ["events"],
        "response_mode": "mock",
        "confidence": "medium"
    },
    "metadata": {
        "model_name": "fallback_mock",
        "latency_ms": 45,
        "fallback_reason": "gemini_timeout"
    }
}
```

### 4.4. Response (Rate Limited — 429)

```json
{
    "status": "error",
    "error_code": "RATE_LIMITED",
    "message": "Bạn đã gửi quá 5 câu hỏi trong 1 phút. Vui lòng đợi 30 giây và thử lại.",
    "retry_after_seconds": 30
}
```

## 5. Conversation Context Management

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| Max conversation history | 10 turns | Giữ 10 lượt hội thoại gần nhất |
| Context window | ~4000 tokens | Giới hạn context gửi Gemini |
| Session timeout | 30 phút | Reset conversation sau 30' không hoạt động |
| History storage | `ai_chat_history` table | Lưu trữ vĩnh viễn cho analytics |

## 6. Anti-Hallucination Checklist

- [x] Context chỉ từ CSDL, không hardcode
- [x] System Prompt cấm tự tạo dữ liệu
- [x] PII filter trước khi gửi Gemini
- [x] Response validation sau khi nhận
- [x] Fallback khi không đủ dữ liệu
- [x] Timestamp check (context luôn realtime)
- [x] Max 500 ký tự input
- [x] Tách System Instruction khỏi User Prompt (chống Prompt Injection)
