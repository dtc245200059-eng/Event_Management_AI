# Đặc tả AI Predictive Analytics Pipeline

> **File:** `ai_predictive_analytics_spec.md`
> **Chuyên gia đề xuất:** Lead AI Architect
> **Mục tiêu bổ sung:** Chương III §AI03 — FR: Predictive Analytics
> **Trạng thái:** Production-ready specification

---

## 1. Tổng quan

Predictive Analytics Engine dự báo số lượng người tham dự thực tế cho mỗi sự kiện, hỗ trợ ban tổ chức lập kế hoạch nguồn lực (ghế, tài liệu, suất ăn, nhân viên vận hành).

**Bài toán ML:** Regression — Dự đoán `actual_attendees` từ các đặc trưng sự kiện và dữ liệu đăng ký.

## 2. Lựa chọn Model

### 2.1. Model chính: Gradient Boosting Regressor (scikit-learn)

| Tiêu chí | Lý do lựa chọn |
|----------|-----------------|
| Accuracy | Xử lý tốt dữ liệu tabular, phi tuyến |
| Interpretability | Feature importance có sẵn |
| Data size | Phù hợp cho dataset nhỏ-vừa (< 10K records) |
| Training time | Nhanh trên CPU, không cần GPU |
| Dependencies | scikit-learn (đã có trong requirements.txt) |

### 2.2. Model backup: Linear Regression + Random Forest

Dùng làm baseline comparison.

## 3. Feature Engineering

### 3.1. Event Features (Static)

| Feature | Type | Source | Mô tả |
|---------|------|--------|--------|
| `category_encoded` | Categorical → One-hot | `events.category` | Loại sự kiện |
| `is_weekend` | Binary (0/1) | `events.start_date` | Có diễn ra cuối tuần không |
| `day_of_week` | Integer (0-6) | `events.start_date` | Thứ trong tuần |
| `hour_of_day` | Integer (0-23) | `events.start_date` | Giờ bắt đầu |
| `event_duration_hours` | Float | `end_date - start_date` | Thời lượng sự kiện |
| `num_speakers` | Integer | `COUNT(schedules.speaker_id)` | Số diễn giả |
| `num_sessions` | Integer | `COUNT(schedules.id)` | Số phiên |
| `venue_capacity` | Integer | `venues.capacity` | Sức chứa địa điểm |
| `is_online` | Binary | `events.location_type` | Online hay offline |
| `has_paid_tickets` | Binary | `tickets.ticket_type` | Có vé trả phí không |
| `min_ticket_price` | Float | `MIN(tickets.price)` | Giá vé thấp nhất |
| `max_ticket_price` | Float | `MAX(tickets.price)` | Giá vé cao nhất |
| `total_ticket_quota` | Integer | `SUM(tickets.quota)` | Tổng quota vé |
| `description_length` | Integer | `LEN(events.description)` | Độ dài mô tả |
| `tags_count` | Integer | `COUNT(events.tags.split(','))` | Số tags |

### 3.2. Registration Features (Dynamic — tính tại thời điểm dự báo)

| Feature | Type | Source | Mô tả |
|---------|------|--------|--------|
| `total_registrations` | Integer | `COUNT(registrations)` | Tổng đăng ký |
| `paid_registrations` | Integer | `COUNT(payment_status='paid')` | Đã thanh toán |
| `unpaid_registrations` | Integer | `COUNT(payment_status='unpaid')` | Chưa thanh toán |
| `registration_velocity` | Float | `registrations/day` trong 7 ngày gần nhất | Tốc độ đăng ký |
| `days_until_event` | Integer | `start_date - NOW()` | Số ngày còn lại |
| `free_ticket_ratio` | Float | `free_registrations / total` | Tỷ lệ vé miễn phí |

### 3.3. Historical Features (Aggregated)

| Feature | Type | Source | Mô tả |
|---------|------|--------|--------|
| `hist_avg_attendance_rate` | Float | Trung bình `checked_in / registered` của cùng category | Tỷ lệ tham dự TB theo category |
| `hist_avg_no_show_rate` | Float | `1 - attendance_rate` | Tỷ lệ vắng mặt TB |
| `hist_same_venue_rate` | Float | Tỷ lệ tham dự TB tại cùng venue | Venue factor |
| `organizer_track_record` | Float | Tỷ lệ tham dự TB của events do cùng `created_by` tạo | Uy tín ban tổ chức |

## 4. Data Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    PREDICTIVE ANALYTICS PIPELINE                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────────┐   │
│  │ 1. DATA     │   │ 2. FEATURE   │   │ 3. MODEL           │   │
│  │ COLLECTION  │──▶│ ENGINEERING  │──▶│ TRAINING/INFERENCE │   │
│  │             │   │              │   │                    │   │
│  │ • events    │   │ • One-hot    │   │ • GBR (primary)    │   │
│  │ • regist.   │   │ • Normalize  │   │ • RF (baseline)    │   │
│  │ • tickets   │   │ • Aggregate  │   │ • LR (baseline)    │   │
│  │ • schedules │   │ • Time feat. │   │ • Cross-validate   │   │
│  │ • venues    │   │ • History    │   │ • Hyperparameter   │   │
│  │ • checkins  │   │              │   │   tuning           │   │
│  └─────────────┘   └──────────────┘   └────────────────────┘   │
│                                                │                 │
│                                                ▼                 │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────────┐   │
│  │ 6. LOG &    │   │ 5. POST-     │   │ 4. PREDICTION      │   │
│  │ MONITOR     │◀──│ PROCESSING   │◀──│ OUTPUT             │   │
│  │             │   │              │   │                    │   │
│  │ • accuracy  │   │ • Confidence │   │ • predicted_count  │   │
│  │ • drift     │   │ • Range calc │   │ • lower_bound      │   │
│  │ • retrain   │   │ • Resource   │   │ • upper_bound      │   │
│  │   trigger   │   │   planning   │   │ • confidence       │   │
│  └─────────────┘   └──────────────┘   └────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 5. Train/Test Split Strategy

| Chiến lược | Mô tả |
|-----------|-------|
| **Split ratio** | 80% train / 20% test (time-based split, không random) |
| **Cross-validation** | 5-Fold TimeSeriesSplit |
| **Minimum training data** | Ít nhất 20 sự kiện đã hoàn thành có dữ liệu check-in |
| **Retrain trigger** | Sau mỗi 10 sự kiện mới hoàn thành hoặc mỗi 30 ngày |

## 6. Evaluation Metrics

| Metric | Công thức | Mục tiêu | Mô tả |
|--------|-----------|----------|-------|
| **MAE** | Mean Absolute Error | ≤ 15 người | Sai số tuyệt đối trung bình |
| **RMSE** | Root Mean Squared Error | ≤ 25 người | Sai số bình phương trung bình |
| **MAPE** | Mean Absolute Percentage Error | ≤ 20% | Sai số phần trăm |
| **R²** | Coefficient of Determination | ≥ 0.70 | Khả năng giải thích |

## 7. API Contract: Flask Backend ↔ Predictive Service

### 7.1. Request

```
POST /api/ai/predict-attendance
Content-Type: application/json
Authorization: Bearer <session_token>
```

**Request Body:**
```json
{
    "event_id": 12,
    "prediction_type": "attendance",
    "include_resource_planning": true,
    "confidence_level": 0.95,
    "context": {
        "event_code": "EVT-2026-012",
        "title": "Hội thảo AI và Machine Learning 2026",
        "category": "technology",
        "start_date": "2026-11-15T09:00:00",
        "end_date": "2026-11-15T17:00:00",
        "venue_capacity": 300,
        "location_type": "offline",
        "total_registrations": 250,
        "paid_registrations": 180,
        "unpaid_registrations": 70,
        "free_ticket_count": 120,
        "paid_ticket_count": 130,
        "days_until_event": 45,
        "num_speakers": 5,
        "num_sessions": 8,
        "has_paid_tickets": true,
        "min_price": 0,
        "max_price": 200000
    }
}
```

### 7.2. Response (Success — 200 OK)

```json
{
    "status": "success",
    "event_id": 12,
    "prediction": {
        "predicted_attendees": 195,
        "lower_bound": 172,
        "upper_bound": 218,
        "confidence_interval": "95%",
        "predicted_attendance_rate": 0.78,
        "predicted_no_show_rate": 0.22,
        "confidence_level": "high",
        "key_factors": [
            {
                "factor": "paid_registration_ratio",
                "value": 0.72,
                "impact": "positive",
                "description": "Tỷ lệ đã thanh toán cao (72%) → giảm no-show"
            },
            {
                "factor": "days_until_event",
                "value": 45,
                "impact": "neutral",
                "description": "Còn 45 ngày, đăng ký có thể tiếp tục tăng"
            },
            {
                "factor": "hist_category_rate",
                "value": 0.75,
                "impact": "positive",
                "description": "Sự kiện 'technology' thường có tỷ lệ tham dự 75%"
            },
            {
                "factor": "free_ticket_ratio",
                "value": 0.48,
                "impact": "negative",
                "description": "Vé miễn phí chiếm 48%, thường có no-show cao hơn"
            }
        ]
    },
    "resource_planning": {
        "recommended_seats": 220,
        "recommended_documents": 210,
        "recommended_meals": 200,
        "recommended_staff": 8,
        "reasoning": "Dự phòng 10-15% so với dự báo để đảm bảo trải nghiệm"
    },
    "model_info": {
        "model_name": "GradientBoostingRegressor",
        "model_version": "v1.3",
        "training_data_size": 85,
        "last_trained": "2026-10-01T02:00:00Z",
        "training_r2": 0.82,
        "test_mae": 12.5
    },
    "warnings": [
        "Dự báo dựa trên 85 sự kiện lịch sử. Độ chính xác sẽ tăng khi có thêm dữ liệu."
    ],
    "metadata": {
        "processing_time_ms": 380,
        "timestamp": "2026-10-15T10:30:00Z"
    }
}
```

### 7.3. Response (Insufficient Data)

```json
{
    "status": "warning",
    "event_id": 12,
    "message": "Không đủ dữ liệu lịch sử (cần tối thiểu 20 sự kiện đã hoàn thành, hiện có 8).",
    "fallback": {
        "method": "rule_based",
        "predicted_attendees": 188,
        "calculation": "total_registrations × historical_avg_rate = 250 × 0.75",
        "confidence_level": "low",
        "note": "Ước lượng dựa trên tỷ lệ tham dự trung bình chung, không phải ML model"
    }
}
```

## 8. Cơ chế xử lý khi dự đoán sai (RSK-09)

| Tình huống | Xử lý |
|-----------|-------|
| Dự báo **cao hơn** thực tế > 30% | Ghi nhận sai số, trigger flag để review features |
| Dự báo **thấp hơn** thực tế > 30% | Ghi nhận, cảnh báo có thể thiếu tài nguyên |
| Model R² < 0.5 | Tự động switch sang rule-based fallback |
| Không có dữ liệu lịch sử | Dùng tỷ lệ trung bình ngành (70-80% registration → attendance) |

**Nguyên tắc quan trọng:** Kết quả dự báo LUÔN được trình bày dưới dạng:
```
Số đăng ký hiện tại: 250
Dự báo tham dự: 195 (khoảng 172 — 218)
Mức tin cậy: 95%
Phương pháp: GradientBoostingRegressor v1.3
```
**KHÔNG BAO GIỜ** trình bày một con số duy nhất như sự thật tuyệt đối.

## 9. Hyperparameter Configuration

```python
model_config = {
    "GradientBoostingRegressor": {
        "n_estimators": 200,
        "max_depth": 5,
        "learning_rate": 0.1,
        "min_samples_split": 5,
        "min_samples_leaf": 3,
        "subsample": 0.8,
        "random_state": 42
    },
    "RandomForestRegressor": {
        "n_estimators": 100,
        "max_depth": 8,
        "min_samples_split": 5,
        "random_state": 42
    }
}
```

## 10. Monitoring & Retraining

| Metric | Ngưỡng cảnh báo | Hành động |
|--------|-----------------|-----------|
| MAE tăng > 50% so với baseline | Warning | Review feature drift |
| R² giảm < 0.5 | Critical | Switch to rule-based + retrain |
| Dữ liệu mới > 10 events | Info | Trigger retraining pipeline |
| Thời gian kể từ lần train cuối > 30 ngày | Warning | Schedule retrain |
