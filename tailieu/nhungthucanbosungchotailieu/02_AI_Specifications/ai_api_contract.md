# Đặc tả API Contract — Giao tiếp Backend ↔ AI Service

> **File:** `ai_api_contract.md`
> **Chuyên gia đề xuất:** Lead AI Architect + CTO
> **Mục tiêu bổ sung:** Chương III §3.1.7 — Tích hợp AI
> **Trạng thái:** Production-ready specification

---

## 1. Tổng quan Kiến trúc Giao tiếp

Hệ thống sử dụng **Internal Service Call** (function call trong cùng Flask process) cho phiên bản hiện tại. Khi scale thành Microservices, có thể chuyển sang HTTP REST.

```
┌────────────────────┐         ┌─────────────────────┐
│  Flask Blueprint   │         │   AI Service Layer   │
│  (Route Controller)│         │  (Python Modules)    │
│                    │         │                      │
│  ai_bp             │──call──▶│  AIOrchestrator      │
│  POST /ai/chat     │         │    ├── GeminiService  │
│  POST /ai/recommend│         │    ├── RAGService     │
│  POST /ai/predict  │         │    ├── RecService     │
│  POST /ai/sentiment│         │    ├── PredService    │
│                    │◀─return─│    └── SentService    │
└────────────────────┘         └─────────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  External APIs   │
                              │  • Gemini 2.0    │
                              │    Flash API     │
                              └─────────────────┘
```

## 2. Bảng tổng hợp Endpoints

| # | Endpoint | Method | Chức năng | Auth Required | Rate Limit |
|---|----------|--------|-----------|---------------|------------|
| 1 | `/api/ai/chat` | POST | Chatbot RAG | Yes (any role) | 5/min/user |
| 2 | `/api/ai/recommendation` | POST | Gợi ý sự kiện | Yes (attendee+) | 5/min/user |
| 3 | `/api/ai/predict-attendance` | POST | Dự báo số người | Yes (manager+) | 3/min/user |
| 4 | `/api/ai/sentiment/analyze` | POST | Phân tích đơn | Yes (manager+) | 10/min/user |
| 5 | `/api/ai/sentiment/batch` | POST | Phân tích hàng loạt | Yes (manager+) | 2/min/user |
| 6 | `/api/ai/generate-description` | POST | Sinh mô tả sự kiện | Yes (manager+) | 5/min/user |
| 7 | `/api/ai/improve-content` | POST | Cải thiện nội dung | Yes (manager+) | 5/min/user |

## 3. Common Headers

### Request Headers
```http
Content-Type: application/json
Accept: application/json
X-Session-Token: <flask_session_cookie>
X-Request-ID: <uuid>  (optional, for tracing)
```

### Response Headers
```http
Content-Type: application/json
X-AI-Model: gemini-2.0-flash | fallback_mock
X-Processing-Time-Ms: 1200
X-Rate-Limit-Remaining: 3
X-Rate-Limit-Reset: 1696000000
```

## 4. Common Error Responses

### 4.1. Rate Limit Exceeded (429)
```json
{
    "status": "error",
    "error_code": "RATE_LIMITED",
    "message": "Bạn đã vượt quá giới hạn {limit} request/phút. Vui lòng đợi {retry_after} giây.",
    "retry_after_seconds": 30
}
```

### 4.2. Unauthorized (401)
```json
{
    "status": "error",
    "error_code": "UNAUTHORIZED",
    "message": "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."
}
```

### 4.3. Forbidden (403)
```json
{
    "status": "error",
    "error_code": "FORBIDDEN",
    "message": "Bạn không có quyền truy cập chức năng này. Yêu cầu role: {required_role}."
}
```

### 4.4. AI Service Unavailable (503)
```json
{
    "status": "error",
    "error_code": "AI_SERVICE_UNAVAILABLE",
    "message": "Dịch vụ AI tạm thời không khả dụng. Hệ thống đã sử dụng phương pháp thay thế.",
    "fallback_used": true,
    "fallback_method": "mock_engine"
}
```

### 4.5. Validation Error (400)
```json
{
    "status": "error",
    "error_code": "VALIDATION_ERROR",
    "message": "Dữ liệu đầu vào không hợp lệ.",
    "details": [
        {"field": "message", "error": "Vượt quá 500 ký tự."},
        {"field": "event_id", "error": "Sự kiện không tồn tại."}
    ]
}
```

## 5. Chi tiết từng Endpoint

### 5.1. Chatbot RAG — `/api/ai/chat`

*(Chi tiết đầy đủ trong `ai_chatbot_rag_pipeline_spec.md`)*

**Request:**
```json
{
    "message": "string (max 500 chars, required)",
    "event_id": "integer | null (optional, scope to specific event)",
    "conversation_history": [
        {"role": "user|assistant", "content": "string"}
    ],
    "max_context_events": "integer (default: 5, max: 10)"
}
```

**Response fields:**
```json
{
    "status": "success",
    "response": {
        "message": "string (markdown formatted)",
        "intent_detected": "event_info|schedule_query|speaker_query|ticket_query|venue_query|general_qa|greeting|out_of_scope",
        "sources_used": ["events", "schedules", "speakers", "venues", "tickets"],
        "response_mode": "live|mock",
        "confidence": "high|medium|low"
    },
    "metadata": {
        "model_name": "string",
        "latency_ms": "integer",
        "context_tokens": "integer",
        "response_tokens": "integer",
        "chat_history_id": "integer"
    }
}
```

### 5.2. Recommendation — `/api/ai/recommendation`

*(Chi tiết đầy đủ trong `ai_recommendation_engine_spec.md`)*

**Request:**
```json
{
    "user_id": "integer (required)",
    "attendee_id": "integer (required)",
    "filters": {
        "max_results": "integer (default: 10)",
        "exclude_event_ids": ["integer"],
        "min_date": "datetime ISO 8601",
        "status_whitelist": ["published", "ongoing"]
    },
    "config": {
        "algorithm": "content_based|hybrid",
        "diversity_factor": "float (0-1, default: 0.3)",
        "include_reasons": "boolean (default: true)"
    }
}
```

### 5.3. Predictive Analytics — `/api/ai/predict-attendance`

*(Chi tiết đầy đủ trong `ai_predictive_analytics_spec.md`)*

**Request:**
```json
{
    "event_id": "integer (required)",
    "prediction_type": "attendance|resource|budget",
    "include_resource_planning": "boolean (default: true)",
    "confidence_level": "float (0.90|0.95|0.99, default: 0.95)"
}
```

### 5.4. Generate Description — `/api/ai/generate-description`

**Request:**
```json
{
    "event_name": "Hội thảo AI và Machine Learning 2026",
    "category": "technology",
    "target_audience": "sinh viên CNTT, kỹ sư phần mềm",
    "location": "Hội trường A, Trường ĐH CNTT&TT",
    "date": "2026-11-15",
    "additional_info": "Có 5 diễn giả từ Google, Microsoft",
    "tone": "professional|casual|academic",
    "max_length": 500
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "generated_content": {
        "description": "Hội thảo AI và Machine Learning 2026 là sự kiện thường niên quy tụ các chuyên gia hàng đầu từ Google, Microsoft...",
        "word_count": 245,
        "tone_used": "professional"
    },
    "metadata": {
        "model_name": "gemini-2.0-flash",
        "latency_ms": 2100,
        "response_mode": "live"
    }
}
```

### 5.5. Improve Content — `/api/ai/improve-content`

**Request:**
```json
{
    "original_content": "Sự kiện về AI sẽ diễn ra ngày 15/11. Có nhiều diễn giả hay.",
    "improvement_goals": ["clarity", "professionalism", "detail"],
    "preserve_facts": true,
    "max_length": 500
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "improved_content": {
        "text": "Sự kiện chuyên đề về Trí tuệ Nhân tạo sẽ được tổ chức vào ngày 15 tháng 11, quy tụ nhiều diễn giả uy tín trong lĩnh vực công nghệ...",
        "changes_summary": [
            "Thay 'AI' bằng 'Trí tuệ Nhân tạo' cho rõ ràng hơn",
            "Bổ sung chi tiết về diễn giả",
            "Cải thiện cấu trúc câu"
        ],
        "word_count": 180
    },
    "metadata": {
        "model_name": "gemini-2.0-flash",
        "latency_ms": 1800,
        "response_mode": "live"
    }
}
```

## 6. Data Flow Summary

```
Client Request
     │
     ▼
Flask Route (ai_bp)
     │
     ├── Authentication Check (session)
     ├── Authorization Check (role)
     ├── Rate Limiter Check
     ├── Input Validation
     │
     ▼
AIOrchestrator
     │
     ├── Build Context (DB queries)
     ├── PII Filtering
     ├── Select AI Service
     │
     ├──▶ GeminiService ──▶ Gemini API ──▶ Response
     │    (timeout 3s)         │
     │         │               ▼
     │         └── Fallback → MockEngine → Response
     │
     ├── Response Validation
     ├── Log to ai_chat_history
     │
     ▼
JSON Response → Client
```

## 7. Logging Schema (ai_chat_history)

Mỗi request AI đều được log vào bảng `ai_chat_history`:

```json
{
    "user_id": 42,
    "event_id": 12,
    "chat_type": "chat|recommendation|predictive|sentiment|generate|improve",
    "user_message": "<original request>",
    "ai_response": "<full response JSON>",
    "model_name": "gemini-2.0-flash",
    "response_mode": "live|mock",
    "latency_ms": 1200,
    "created_at": "2026-10-15T10:30:00Z"
}
```
