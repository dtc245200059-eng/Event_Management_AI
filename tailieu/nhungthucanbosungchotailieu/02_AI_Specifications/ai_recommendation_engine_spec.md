# Đặc tả AI Recommendation Engine

> **File:** `ai_recommendation_engine_spec.md`
> **Chuyên gia đề xuất:** Lead AI Architect
> **Mục tiêu bổ sung:** Chương III §AI01 — FR: AI Recommendation
> **Trạng thái:** Production-ready specification

---

## 1. Tổng quan

AI Recommendation Engine cá nhân hóa danh sách sự kiện đề xuất cho từng người tham dự (Attendee) dựa trên:
- Hồ sơ người dùng (interests, job_title, organization)
- Lịch sử tham gia sự kiện (events đã đăng ký, đã check-in)
- Hành vi tương tác (xem, click, bookmark — nếu có bảng `user_event_interactions`)
- Đặc trưng sự kiện (category, tags, speakers, thời gian)

## 2. Thuật toán được lựa chọn

### 2.1. Phase 1: Content-Based Filtering (MVP)

Sử dụng **TF-IDF + Cosine Similarity** để tính độ tương đồng giữa profile người dùng và đặc trưng sự kiện.

**Feature Vector cho Event:**
```
event_features = TF-IDF(
    event.category + " " +
    event.tags + " " +
    event.description + " " +
    [speaker.bio for speaker in event.speakers]
)
```

**Feature Vector cho User:**
```
user_features = TF-IDF(
    attendee.interests + " " +
    attendee.job_title + " " +
    attendee.organization + " " +
    [past_event.category for past_event in user_history]
)
```

**Scoring:**
```python
similarity_score = cosine_similarity(user_features, event_features)
recommended_events = top_n(similarity_score, n=10)
```

### 2.2. Phase 2: Hybrid Filtering (Mở rộng)

Kết hợp Content-Based với **Collaborative Filtering** (User-Item Matrix Factorization) khi có đủ dữ liệu tương tác.

```
final_score = α × content_score + (1 - α) × collaborative_score
```
- `α = 0.7` (ưu tiên content khi dữ liệu ít)
- Giảm dần `α` khi dữ liệu tương tác tăng

## 3. Data Pipeline

```
┌─────────────┐    ┌──────────────────┐    ┌────────────────┐
│  Data        │    │  Feature         │    │  Model         │
│  Collection  │───▶│  Engineering     │───▶│  Training      │
│              │    │                  │    │                │
│ • attendees  │    │ • TF-IDF vectors │    │ • Cosine Sim   │
│ • events     │    │ • Category encode│    │ • Top-N ranking│
│ • registra-  │    │ • History encode │    │ • Score cache  │
│   tions      │    │ • Normalization  │    │                │
└─────────────┘    └──────────────────┘    └────────────────┘
                                                    │
                                                    ▼
┌─────────────┐    ┌──────────────────┐    ┌────────────────┐
│  Response    │    │  Post-processing │    │  Inference     │
│  to Client   │◀──│  & Filtering     │◀──│  (Realtime)    │
│              │    │                  │    │                │
│ • Top-N list │    │ • Loại expired   │    │ • Lookup user  │
│ • Score      │    │ • Loại đã đăng ký│    │ • Compute sim  │
│ • Reason     │    │ • Diversity boost│    │ • Rank events  │
└─────────────┘    └──────────────────┘    └────────────────┘
```

## 4. Bộ lọc Pre-Processing (Business Rules)

Trước khi đưa vào Recommendation Engine, danh sách sự kiện phải qua bộ lọc:

| # | Quy tắc | Mô tả |
|---|---------|-------|
| 1 | Status Filter | Chỉ sự kiện `status = 'published'` hoặc `'ongoing'` |
| 2 | Date Filter | `start_date > NOW()` (chưa diễn ra) |
| 3 | Capacity Filter | `sold_count < quota` (còn vé) |
| 4 | Duplicate Filter | Loại sự kiện người dùng đã đăng ký |
| 5 | Diversity Boost | Tối đa 3 sự kiện cùng category trong Top-10 |

## 5. API Contract: Flask Backend ↔ Recommendation Service

### 5.1. Request (Internal Function Call)

**Endpoint nội bộ:** `RecommendationService.get_recommendations(user_id, top_n)`

**Hoặc nếu tách service qua HTTP:**

```
POST /api/ai/recommendation
Content-Type: application/json
Authorization: Bearer <internal_service_token>
```

**Request Body:**
```json
{
    "user_id": 42,
    "attendee_id": 15,
    "user_profile": {
        "interests": "machine learning, cloud computing, data science",
        "job_title": "Software Engineer",
        "organization": "ICTU",
        "past_events": [
            {
                "event_id": 3,
                "category": "technology",
                "tags": "AI, workshop",
                "attended": true,
                "feedback_rating": 5
            },
            {
                "event_id": 7,
                "category": "technology",
                "tags": "cloud, AWS",
                "attended": true,
                "feedback_rating": 4
            }
        ]
    },
    "filters": {
        "max_results": 10,
        "exclude_event_ids": [3, 7],
        "min_date": "2026-10-01T00:00:00",
        "status_whitelist": ["published", "ongoing"]
    },
    "config": {
        "algorithm": "content_based",
        "diversity_factor": 0.3,
        "include_reasons": true
    }
}
```

### 5.2. Response (Success — 200 OK)

```json
{
    "status": "success",
    "user_id": 42,
    "algorithm_used": "content_based_tfidf",
    "total_candidates": 45,
    "recommendations": [
        {
            "rank": 1,
            "event_id": 12,
            "event_code": "EVT-2026-012",
            "title": "Hội thảo AI và Machine Learning 2026",
            "category": "technology",
            "tags": ["AI", "ML", "deep learning"],
            "start_date": "2026-11-15T09:00:00",
            "location": "Hội trường A, ICTU",
            "similarity_score": 0.92,
            "confidence": "high",
            "recommendation_reasons": [
                "Cùng lĩnh vực Machine Learning với sự kiện bạn đã tham gia",
                "Phù hợp với sở thích 'AI, data science'",
                "Diễn giả có chuyên môn liên quan đến lịch sử tham gia"
            ],
            "tickets_available": true,
            "min_price": 0,
            "max_price": 200000
        },
        {
            "rank": 2,
            "event_id": 18,
            "event_code": "EVT-2026-018",
            "title": "Workshop Cloud Native với Kubernetes",
            "category": "technology",
            "tags": ["cloud", "kubernetes", "devops"],
            "start_date": "2026-11-22T14:00:00",
            "location": "Phòng Lab B2, ICTU",
            "similarity_score": 0.85,
            "confidence": "high",
            "recommendation_reasons": [
                "Liên quan đến 'cloud computing' trong sở thích",
                "Tương tự sự kiện Cloud/AWS bạn đã đánh giá 4/5 sao"
            ],
            "tickets_available": true,
            "min_price": 50000,
            "max_price": 50000
        }
    ],
    "metadata": {
        "processing_time_ms": 245,
        "model_version": "v1.2",
        "data_freshness": "2026-10-01T08:00:00Z"
    }
}
```

### 5.3. Response (Error)

```json
{
    "status": "error",
    "error_code": "INSUFFICIENT_DATA",
    "message": "Không đủ dữ liệu lịch sử để tạo đề xuất cá nhân hóa. Hiển thị danh sách sự kiện phổ biến thay thế.",
    "fallback": "popular_events",
    "popular_events": [
        {
            "event_id": 5,
            "title": "Ngày hội CNTT 2026",
            "registration_count": 350,
            "category": "technology"
        }
    ]
}
```

## 6. Ngưỡng và Cấu hình

| Tham số | Giá trị mặc định | Mô tả |
|---------|------------------|-------|
| `TOP_N` | 10 | Số sự kiện đề xuất tối đa |
| `MIN_SIMILARITY` | 0.15 | Ngưỡng tối thiểu để đưa vào danh sách |
| `DIVERSITY_FACTOR` | 0.3 | Trọng số phạt khi cùng category |
| `COLD_START_THRESHOLD` | 2 | Số event tối thiểu đã tham gia để dùng content-based |
| `CACHE_TTL` | 3600 | Thời gian cache kết quả (giây) |
| `CONFIDENCE_HIGH` | ≥ 0.75 | Ngưỡng confidence "high" |
| `CONFIDENCE_MEDIUM` | 0.40 – 0.74 | Ngưỡng confidence "medium" |
| `CONFIDENCE_LOW` | < 0.40 | Ngưỡng confidence "low" |

## 7. Cold Start Strategy

Khi người dùng mới (chưa có lịch sử):

1. **Dựa trên `interests` text:** Nếu attendee có trường `interests`, dùng TF-IDF matching
2. **Dựa trên `organization`:** Đề xuất sự kiện phổ biến trong cùng đơn vị
3. **Popular Events Fallback:** Hiển thị Top-10 sự kiện có `registration_count` cao nhất
4. **Category Exploration:** Chia đều 2 sự kiện/category để khám phá sở thích

## 8. Metrics đánh giá

| Metric | Công thức | Mục tiêu |
|--------|-----------|----------|
| Precision@K | `|relevant ∩ recommended| / K` | ≥ 0.3 |
| Recall@K | `|relevant ∩ recommended| / |relevant|` | ≥ 0.5 |
| NDCG@K | Normalized Discounted Cumulative Gain | ≥ 0.6 |
| Coverage | `|unique events recommended| / |total events|` | ≥ 0.7 |
| Diversity | `1 - avg(similarity between pairs in Top-K)` | ≥ 0.4 |

## 9. Diagram: Recommendation Flow

```
User Request (GET /events/recommendations)
    │
    ▼
Flask Route (events_bp)
    │
    ▼
AIOrchestrator.get_recommendations()
    │
    ├── Rate Limiter Check ──▶ HTTP 429 nếu vượt quota
    │
    ├── Load User Profile (attendees + registrations)
    │
    ├── Load Candidate Events (pre-filtered)
    │
    ├── Check Cold Start?
    │    ├── YES → Popular Events Fallback
    │    └── NO  → Continue
    │
    ▼
RecommendationService.compute()
    │
    ├── Feature Engineering (TF-IDF)
    ├── Cosine Similarity Calculation
    ├── Diversity Re-ranking
    ├── Top-N Selection
    │
    ▼
Post-Processing
    │
    ├── Generate recommendation_reasons
    ├── Add ticket availability info
    ├── Add confidence level
    │
    ▼
Response → Client (JSON)
    │
    ▼
Log to ai_chat_history (chat_type = 'recommendation')
```
