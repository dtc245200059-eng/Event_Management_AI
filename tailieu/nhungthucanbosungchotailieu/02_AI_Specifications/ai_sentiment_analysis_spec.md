# Đặc tả AI Sentiment Analysis

> **File:** `ai_sentiment_analysis_spec.md`
> **Chuyên gia đề xuất:** Lead AI Architect
> **Mục tiêu bổ sung:** Chương III §AI04 — FR: Sentiment Analysis
> **Trạng thái:** Production-ready specification

---

## 1. Tổng quan

Sentiment Analysis Engine phân tích phản hồi của người tham dự sau sự kiện, xác định:
- **Sentiment polarity:** Positive / Neutral / Negative
- **Sentiment score:** Điểm số từ -1.0 đến +1.0
- **Topic extraction:** Các chủ đề/vấn đề được đề cập nhiều
- **Actionable insights:** Tóm tắt các điểm cần cải thiện

## 2. Phương pháp phân tích

### 2.1. Hybrid Approach

Kết hợp 2 phương pháp:

| Phương pháp | Vai trò | Ưu điểm |
|------------|---------|---------|
| **Gemini LLM** (primary) | Phân tích sâu, hiểu ngữ cảnh tiếng Việt | Xử lý câu phức, mỉa mai, ngữ cảnh |
| **Rule-based scoring** (backup) | Keyword matching + rating | Nhanh, không phụ thuộc API |

### 2.2. Luồng xử lý

```
Feedback Text + Rating
        │
        ▼
┌──────────────────┐
│ Pre-processing   │
│ • Normalize text │
│ • Remove noise   │
│ • Language detect │
└──────────────────┘
        │
        ├──────────────────────┐
        ▼                      ▼
┌──────────────────┐  ┌──────────────────┐
│ Gemini Analysis  │  │ Rule-based Score │
│ • Sentiment      │  │ • Rating weight  │
│ • Topics         │  │ • Keyword match  │
│ • Key phrases    │  │ • Simple score   │
└──────────────────┘  └──────────────────┘
        │                      │
        ▼                      ▼
┌──────────────────────────────────┐
│ Score Fusion                      │
│ final = 0.7 × gemini + 0.3 × rule│
└──────────────────────────────────┘
        │
        ▼
┌──────────────────┐
│ Store Results    │
│ • sentiment      │
│ • sentiment_score│
│ • topics         │
└──────────────────┘
```

## 3. Pre-processing

| Bước | Mô tả | Ví dụ |
|------|--------|-------|
| Normalize whitespace | Xóa khoảng trắng thừa | "Rất  tốt" → "Rất tốt" |
| Remove HTML | Strip tags | `<b>tốt</b>` → "tốt" |
| Lowercase | Chuyển thường (cho keyword matching) | "RẤT TỐT" → "rất tốt" |
| Remove URLs | Xóa links | "xem tại http://..." → "xem tại" |
| Emoji mapping | Chuyển emoji → text | "👍" → "[positive]", "👎" → "[negative]" |
| Min length check | Bỏ qua nếu < 5 ký tự | "ok" → skip |

## 4. Sentiment Classification

### 4.1. Gemini Prompt cho Sentiment

```
ROLE: Bạn là chuyên gia phân tích cảm xúc (Sentiment Analysis) cho hệ thống quản lý sự kiện.

TASK: Phân tích phản hồi sau sự kiện bên dưới.

RULES:
1. Phân loại sentiment: "positive", "neutral", hoặc "negative"
2. Cho điểm từ -1.0 (rất tiêu cực) đến +1.0 (rất tích cực)
3. Trích xuất 1-3 chủ đề chính được đề cập
4. Xác định các vấn đề cần cải thiện (nếu có)
5. CHỈ phân tích dựa trên nội dung được cung cấp

OUTPUT FORMAT (JSON):
{
    "sentiment": "positive|neutral|negative",
    "score": 0.0,
    "topics": ["topic1", "topic2"],
    "key_phrases": ["phrase1", "phrase2"],
    "improvement_suggestions": ["suggestion1"],
    "summary": "Tóm tắt ngắn 1-2 câu"
}

FEEDBACK DATA:
Event: {event_name}
Rating: {rating}/5
Feedback: {feedback_text}
```

### 4.2. Rule-based Backup

**Positive keywords (tiếng Việt):**
```python
POSITIVE_KEYWORDS = [
    "tuyệt vời", "xuất sắc", "rất tốt", "hay", "bổ ích",
    "hữu ích", "chuyên nghiệp", "ấn tượng", "thú vị",
    "hài lòng", "tốt", "giỏi", "chất lượng", "tận tâm",
    "đáng tham gia", "đáng giá", "recommend", "5 sao"
]
```

**Negative keywords:**
```python
NEGATIVE_KEYWORDS = [
    "tệ", "kém", "chán", "nhàm chán", "thất vọng",
    "lãng phí", "chậm", "muộn", "lộn xộn", "không tốt",
    "tồi", "quá dở", "không hài lòng", "không đáng",
    "phí thời gian", "khó chịu", "ồn ào", "nóng"
]
```

**Rule-based score:**
```python
def rule_based_sentiment(text, rating):
    text_lower = text.lower()
    pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)

    # Rating weight: rating/5 → [-1, 1] scale
    rating_score = (rating - 3) / 2  # 1→-1, 3→0, 5→+1

    # Keyword score
    if pos_count + neg_count > 0:
        keyword_score = (pos_count - neg_count) / (pos_count + neg_count)
    else:
        keyword_score = 0

    # Weighted average
    final_score = 0.6 * rating_score + 0.4 * keyword_score

    if final_score > 0.2:
        return "positive", final_score
    elif final_score < -0.2:
        return "negative", final_score
    else:
        return "neutral", final_score
```

## 5. Topic Extraction

### 5.1. Predefined Topic Categories

| Category | Keywords | Mô tả |
|----------|----------|-------|
| `content_quality` | "nội dung", "bài giảng", "chất lượng", "kiến thức" | Chất lượng nội dung |
| `speaker_quality` | "diễn giả", "giảng viên", "người nói", "trình bày" | Chất lượng diễn giả |
| `organization` | "tổ chức", "sắp xếp", "lịch trình", "thời gian" | Công tác tổ chức |
| `venue_facility` | "địa điểm", "phòng", "nóng", "lạnh", "âm thanh", "ghế" | Cơ sở vật chất |
| `checkin_process` | "check-in", "đăng ký", "chờ đợi", "xếp hàng" | Quy trình check-in |
| `networking` | "giao lưu", "kết nối", "networking", "bạn bè" | Cơ hội kết nối |
| `food_beverage` | "ăn", "uống", "nước", "cơm", "snack", "tea break" | Ẩm thực |
| `technology` | "wifi", "máy chiếu", "micro", "màn hình", "app" | Công nghệ hỗ trợ |

## 6. API Contract: Flask Backend ↔ Sentiment Service

### 6.1. Phân tích đơn (Single Feedback)

**Request:**
```
POST /api/ai/sentiment/analyze
Content-Type: application/json
```

```json
{
    "registration_id": 123,
    "event_id": 12,
    "event_name": "Hội thảo AI và Machine Learning 2026",
    "feedback_rating": 4,
    "feedback_text": "Nội dung rất hay và bổ ích, diễn giả trình bày chuyên nghiệp. Tuy nhiên phần check-in hơi chậm và phòng hơi nóng.",
    "analyze_topics": true
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "registration_id": 123,
    "analysis": {
        "sentiment": "positive",
        "sentiment_score": 0.65,
        "confidence": 0.88,
        "topics": [
            {
                "category": "content_quality",
                "sentiment": "positive",
                "key_phrases": ["nội dung rất hay", "bổ ích"]
            },
            {
                "category": "speaker_quality",
                "sentiment": "positive",
                "key_phrases": ["diễn giả trình bày chuyên nghiệp"]
            },
            {
                "category": "checkin_process",
                "sentiment": "negative",
                "key_phrases": ["check-in hơi chậm"]
            },
            {
                "category": "venue_facility",
                "sentiment": "negative",
                "key_phrases": ["phòng hơi nóng"]
            }
        ],
        "improvement_suggestions": [
            "Cải thiện quy trình check-in để giảm thời gian chờ",
            "Kiểm tra hệ thống điều hòa trước sự kiện"
        ],
        "summary": "Người tham dự đánh giá cao nội dung và diễn giả nhưng góp ý cải thiện quy trình check-in và điều kiện phòng.",
        "method": "gemini_llm",
        "model_name": "gemini-2.0-flash"
    },
    "metadata": {
        "processing_time_ms": 1200,
        "timestamp": "2026-11-16T10:30:00Z"
    }
}
```

### 6.2. Phân tích hàng loạt (Batch Analysis)

**Request:**
```
POST /api/ai/sentiment/batch
Content-Type: application/json
```

```json
{
    "event_id": 12,
    "feedbacks": [
        {
            "registration_id": 123,
            "rating": 5,
            "text": "Tuyệt vời! Rất bổ ích."
        },
        {
            "registration_id": 124,
            "rating": 2,
            "text": "Nội dung không như mong đợi, quá chậm."
        },
        {
            "registration_id": 125,
            "rating": 4,
            "text": "Hay, nhưng phòng hơi chật."
        }
    ]
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "event_id": 12,
    "summary": {
        "total_feedbacks": 3,
        "sentiment_distribution": {
            "positive": 2,
            "neutral": 0,
            "negative": 1
        },
        "average_score": 0.43,
        "average_rating": 3.67,
        "top_positive_topics": [
            {"category": "content_quality", "count": 2, "sample": "Tuyệt vời! Rất bổ ích"}
        ],
        "top_negative_topics": [
            {"category": "venue_facility", "count": 1, "sample": "phòng hơi chật"},
            {"category": "organization", "count": 1, "sample": "quá chậm"}
        ],
        "overall_assessment": "Phần lớn người tham dự hài lòng (67%). Cần cải thiện: cơ sở vật chất và tốc độ trình bày.",
        "word_cloud_data": [
            {"word": "bổ ích", "count": 2, "sentiment": "positive"},
            {"word": "chậm", "count": 1, "sentiment": "negative"},
            {"word": "chật", "count": 1, "sentiment": "negative"}
        ]
    },
    "individual_results": [
        {"registration_id": 123, "sentiment": "positive", "score": 0.92},
        {"registration_id": 124, "sentiment": "negative", "score": -0.65},
        {"registration_id": 125, "sentiment": "positive", "score": 0.55}
    ]
}
```

## 7. Xử lý Edge Cases

| Tình huống | Xử lý |
|-----------|-------|
| Feedback chỉ có rating, không có text | Dùng rule-based: rating → sentiment |
| Text tiếng Anh lẫn tiếng Việt | Gemini xử lý multilingual |
| Text quá ngắn (< 5 ký tự) | Skip sentiment, chỉ dùng rating |
| Text mỉa mai/ironic | Gemini prompt hướng dẫn detect sarcasm |
| Gemini timeout | Fallback sang rule-based |
| Feedback chứa PII | Pre-filter trước khi phân tích |
| Rating = 3, text positive | Ưu tiên text analysis (weight 0.6) |

## 8. Cấu hình & Ngưỡng

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `POSITIVE_THRESHOLD` | > 0.2 | Score trên mức này = positive |
| `NEGATIVE_THRESHOLD` | < -0.2 | Score dưới mức này = negative |
| `GEMINI_WEIGHT` | 0.7 | Trọng số Gemini trong score fusion |
| `RULE_WEIGHT` | 0.3 | Trọng số rule-based |
| `BATCH_SIZE` | 20 | Số feedback gửi Gemini mỗi batch |
| `MIN_TEXT_LENGTH` | 5 | Độ dài tối thiểu để phân tích text |
| `BATCH_TIMEOUT` | 30s | Timeout cho batch processing |
