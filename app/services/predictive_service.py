"""
Predictive Analytics Service: Attendance Probability and Resource Forecast.
"""
from datetime import datetime
from app.extensions import db
from app.models import Event, Registration

def predict_event_attendance(event_id):
    """
    Dự báo số lượng người tham dự thực tế (% Show-up Rate) dựa trên:
    - Loại vé (Vé VIP/Paid có tỷ lệ tham gia cao hơn ~85-95% so với vé Free ~60-75%)
    - Thời điểm đăng ký (Đăng ký sát ngày có xu hướng show-up cao hơn)
    - Trạng thái thanh toán
    """
    event = db.session.get(Event, event_id)
    if not event:
        return None

    registrations = event.registrations.filter_by(registration_status='confirmed').all()
    total_reg = len(registrations)

    if total_reg == 0:
        return {
            'total_registered': 0,
            'expected_attendance': 0,
            'predicted_showup_rate': 0.0,
            'venue_capacity': event.max_attendees or 500,
            'risk_level': 'Low',
            'recommended_seats': 0,
            'teabreak_portions': 0
        }

    expected_attendees = 0.0

    for reg in registrations:
        # Base probability by ticket type
        if reg.ticket.ticket_type == 'vip':
            prob = 0.92
        elif reg.ticket.ticket_type == 'paid' or reg.ticket.price > 0:
            prob = 0.85
        else:
            prob = 0.68  # Free ticket showup rate

        # Adjusted by payment
        if reg.payment_status == 'paid':
            prob = min(0.98, prob + 0.05)

        # Adjusted by registration recency
        days_before_event = (event.start_date - reg.created_at).days
        if days_before_event <= 3:
            prob = min(0.98, prob + 0.04)
        elif days_before_event > 20:
            prob = max(0.50, prob - 0.05)

        expected_attendees += prob

    predicted_count = int(round(expected_attendees))
    showup_rate = round((predicted_count / total_reg) * 100, 1)

    # Risk level for venue capacity
    capacity = event.max_attendees or 500
    if predicted_count > capacity:
        risk_level = 'High (Nguy cơ quá tải phòng họp)'
    elif predicted_count > capacity * 0.85:
        risk_level = 'Medium (Gần đạt giới hạn sức chứa)'
    else:
        risk_level = 'Normal (An toàn)'

    return {
        'total_registered': total_reg,
        'expected_attendance': predicted_count,
        'predicted_showup_rate': showup_rate,
        'venue_capacity': capacity,
        'risk_level': risk_level,
        'recommended_seats': int(predicted_count * 1.05),  # 5% buffer
        'teabreak_portions': int(predicted_count * 1.08)   # 8% buffer
    }
