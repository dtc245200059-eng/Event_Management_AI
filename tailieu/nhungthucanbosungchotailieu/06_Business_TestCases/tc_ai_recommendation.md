# Bộ Test Cases — AI Recommendation Engine

> **File:** `tc_ai_recommendation.md`
> **Chuyên gia đề xuất:** Lead AI Architect
> **Mục tiêu bổ sung:** Sprint 3 — Kiểm thử AI Recommendation
> **Phạm vi:** Content-Based Filtering, Cold Start, Diversity, API

---

## 1. Kịch bản kiểm thử: Recommendation cơ bản

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback — Xử lý khi AI dự đoán sai |
|-------|---------------|-------------------|-------------------|-------------------|----------------------------------------|
| TC-RC-001 | Recommendation cho user có lịch sử | 1. User đã tham gia 3 sự kiện "technology"<br>2. Gọi API recommendation<br>3. Kiểm tra kết quả | user_id=42, history=[3 tech events] | - Top-10 events được trả về<br>- Sự kiện "technology" được ưu tiên<br>- similarity_score > 0.15<br>- Sự kiện đã đăng ký bị loại | Nếu AI đề xuất sai category: Post-filter kiểm tra, nếu > 70% events ngoài interests → Fallback Popular Events |
| TC-RC-002 | Recommendation với interests text | 1. Attendee có interests="machine learning, AI"<br>2. Chưa có lịch sử tham gia<br>3. Gọi API | interests="machine learning, AI", history=[] | - TF-IDF matching với interests<br>- Sự kiện AI/ML được ưu tiên<br>- confidence='medium' (ít dữ liệu) | Nếu TF-IDF cho kết quả kém (max_score < 0.15): Fallback sang Popular Events + category filter |
| TC-RC-003 | Loại bỏ sự kiện đã đăng ký | 1. User đã đăng ký Event #12, #18<br>2. Gọi recommendation | exclude_event_ids=[12, 18] | - Event #12, #18 KHÔNG xuất hiện trong kết quả<br>- Chỉ sự kiện chưa đăng ký | N/A — Business logic filter |
| TC-RC-004 | Chỉ sự kiện published/ongoing | 1. DB có events: draft, published, completed<br>2. Gọi recommendation | status_whitelist=["published","ongoing"] | - Chỉ events status='published'/'ongoing'<br>- KHÔNG có draft, completed, cancelled | N/A — Pre-filter |
| TC-RC-005 | Chỉ sự kiện còn vé | 1. Event A: sold_count < quota<br>2. Event B: sold_count == quota<br>3. Gọi recommendation | Mix of available and sold-out events | - Event A xuất hiện<br>- Event B KHÔNG xuất hiện (hết vé) | N/A — Pre-filter |

## 2. Kịch bản kiểm thử: Cold Start

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback — Xử lý khi AI dự đoán sai |
|-------|---------------|-------------------|-------------------|-------------------|----------------------------------------|
| TC-RC-006 | User mới — không có lịch sử, không có interests | 1. User mới đăng ký<br>2. interests = null<br>3. history = [] | user_id=99, interests=null, history=[] | - Cold Start detected<br>- Fallback: Popular Events (Top-10 theo registration_count)<br>- confidence='low' | **Đây chính là Fallback:** Hiển thị sự kiện phổ biến nhất thay vì cá nhân hóa |
| TC-RC-007 | User mới — có interests nhưng không có history | 1. User mới, interests="data science"<br>2. history = [] | interests="data science", history=[] | - TF-IDF matching với interests<br>- Kết quả cá nhân hóa cơ bản<br>- confidence='medium' | Nếu không có event match interests: Fallback Popular Events |
| TC-RC-008 | User có 1 sự kiện (dưới cold start threshold) | 1. User đã tham gia 1 sự kiện<br>2. cold_start_threshold = 2 | history=[1 event], threshold=2 | - Cold Start vẫn kích hoạt (1 < 2)<br>- Hybrid: 70% interests + 30% history<br>- confidence='medium' | Nếu 1 event history cho bias quá lớn: Tăng interests weight lên 0.9 |

## 3. Kịch bản kiểm thử: Diversity & Quality

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback — Xử lý khi AI dự đoán sai |
|-------|---------------|-------------------|-------------------|-------------------|----------------------------------------|
| TC-RC-009 | Diversity — không quá 3 cùng category | 1. User quan tâm "technology"<br>2. DB có 8 events "technology"<br>3. diversity_factor=0.3 | Top candidates all technology | - Tối đa 3 events "technology" trong Top-10<br>- Còn lại từ categories khác<br>- Diversity ≥ 0.4 | Nếu Top-10 toàn cùng category: Re-ranking bắt buộc diversity constraint |
| TC-RC-010 | Sự kiện quá khứ bị loại | 1. DB có events start_date < NOW()<br>2. Gọi recommendation | min_date=NOW() | - Chỉ sự kiện tương lai<br>- KHÔNG có sự kiện đã diễn ra | N/A — Date filter |
| TC-RC-011 | Recommendation reasons | 1. include_reasons=true<br>2. Gọi API | config.include_reasons=true | - Mỗi event có `recommendation_reasons`<br>- Reasons giải thích tại sao match<br>- Ít nhất 1 reason per event | N/A — Feature requirement |

## 4. Kịch bản kiểm thử: Performance & Cache

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback — Xử lý khi AI dự đoán sai |
|-------|---------------|-------------------|-------------------|-------------------|----------------------------------------|
| TC-RC-012 | Response time < 500ms | 1. DB có 100 events<br>2. Gọi recommendation<br>3. Đo thời gian | 100 events in DB | - processing_time_ms < 500<br>- Kết quả trả về đúng | Nếu timeout > 2000ms: Return cached results hoặc Popular Events |
| TC-RC-013 | Cache hit (gọi lại trong TTL) | 1. Gọi recommendation lần 1<br>2. Gọi lại trong 1 giờ (TTL=3600s) | Same user, within TTL | - Lần 2 trả cache<br>- processing_time_ms < 50<br>- Kết quả giống lần 1 | N/A — Cache mechanism |
| TC-RC-014 | Cache invalidation khi user tương tác mới | 1. Gọi recommendation (cached)<br>2. User đăng ký event mới<br>3. Gọi lại recommendation | User registers new event between calls | - Cache invalidated<br>- Kết quả mới (event mới đăng ký bị loại)<br>- Recompute scores | N/A — Cache invalidation |

## 5. Kịch bản kiểm thử: Error Handling

| Mã TC | Tên Test Case | Các bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi | AI Fallback — Xử lý khi AI dự đoán sai |
|-------|---------------|-------------------|-------------------|-------------------|----------------------------------------|
| TC-RC-015 | User không tồn tại | 1. Gọi recommendation với user_id không tồn tại | user_id=99999 | - HTTP 404<br>- "User not found" | N/A |
| TC-RC-016 | Không có sự kiện nào eligible | 1. Tất cả events đều draft/completed<br>2. Gọi recommendation | 0 eligible events | - recommendations=[]<br>- Message: "Hiện chưa có sự kiện phù hợp" | Hiển thị "Không có sự kiện mới. Vui lòng quay lại sau." |
| TC-RC-017 | Rate limit cho recommendation | 1. Gọi > 5 lần/phút | 6th request in 60s | - HTTP 429<br>- retry_after_seconds | N/A — Rate Limiter |
