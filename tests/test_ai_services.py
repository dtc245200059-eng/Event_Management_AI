"""
Unit Tests for AI Services (RAG Chat, Fallback Mock, Recommendations, Predictive, Sentiment).
"""
from datetime import datetime, timedelta
from app.extensions import db, utc_now
from app.models import Event, Speaker, Venue, Schedule, Ticket
from app.services.rag_service import answer_event_query
from app.services.recommendation_service import get_personalized_recommendations
from app.services.predictive_service import predict_event_attendance

def test_rag_fallback_mock_engine(app):
    with app.app_context():
        # Setup event
        evt = Event(
            event_code='EVT-RAG-TEST',
            title='Hội Thảo Deep Learning 2026',
            category='Trí tuệ nhân tạo',
            description='Nghiên cứu về Deep Learning và RAG',
            start_date=utc_now() + timedelta(days=1),
            end_date=utc_now() + timedelta(days=1, hours=4),
            status='published'
        )
        db.session.add(evt)
        db.session.commit()

        # Test RAG query
        response, mode, latency = answer_event_query("Lịch trình sự kiện thế nào?", event_id=evt.id)
        assert response is not None
        assert len(response) > 20
        assert mode in ('live', 'mock')
        assert latency >= 0

def test_recommendation_engine(app):
    with app.app_context():
        evt1 = Event(
            event_code='EVT-AI-01',
            title='AI Summit 2026',
            category='Trí tuệ nhân tạo',
            description='GenAI, Transformer, Machine Learning',
            tags='AI, Python',
            start_date=utc_now(),
            end_date=utc_now() + timedelta(hours=2),
            status='published'
        )
        evt2 = Event(
            event_code='EVT-BIZ-02',
            title='Kinh Doanh Bất Động Sản',
            category='Kinh doanh',
            description='Đầu tư tài chính',
            tags='Business, Finance',
            start_date=utc_now(),
            end_date=utc_now() + timedelta(hours=2),
            status='published'
        )
        db.session.add_all([evt1, evt2])
        db.session.commit()

        recs = get_personalized_recommendations(user_interests='Học hỏi về Trí tuệ nhân tạo và Machine Learning', top_n=2)
        assert len(recs) > 0
        # First recommendation should be the AI event
        assert recs[0]['event'].id == evt1.id

def test_predictive_attendance_calculation(app):
    with app.app_context():
        evt = Event(
            event_code='EVT-PRED',
            title='Predictive Event',
            max_attendees=100,
            start_date=utc_now() + timedelta(days=5),
            end_date=utc_now() + timedelta(days=5, hours=3)
        )
        db.session.add(evt)
        db.session.commit()

        stats = predict_event_attendance(evt.id)
        assert stats is not None
        assert 'expected_attendance' in stats
        assert 'predicted_showup_rate' in stats
        assert stats['venue_capacity'] == 100

def test_question_analysis():
    from app.services.rag_service import analyze_question
    # Free query
    res_free = analyze_question("Có sự kiện nào tham gia miễn phí không?")
    assert res_free["is_free_query"] is True

    # Schedule query
    res_sched = analyze_question("Lịch trình và timeline các phiên họp diễn ra mấy giờ?")
    assert res_sched["is_schedule_query"] is True

    # Speaker query
    res_spk = analyze_question("Có những diễn giả hoặc chuyên gia nào tham gia thuyết trình?")
    assert res_spk["is_speaker_query"] is True

    # Location entity
    res_loc = analyze_question("Sự kiện tổ chức ở Thái Nguyên hay Hà Nội?")
    assert res_loc["location_filter"] in ("Thái Nguyên", "Hà Nội")

def test_rag_context_and_free_event_retrieval(app):
    with app.app_context():
        # Setup free and paid event
        free_evt = Event(
            event_code='EVT-FREE-TEST',
            title='Lễ Khai Giảng ICTU',
            category='Khoa học dữ liệu',
            description='Sự kiện miễn phí sinh viên',
            start_date=utc_now() + timedelta(days=2),
            end_date=utc_now() + timedelta(days=2, hours=3),
            status='published'
        )
        paid_evt = Event(
            event_code='EVT-PAID-TEST',
            title='VIP Business Conference',
            category='Kinh doanh',
            description='Sự kiện cao cấp',
            start_date=utc_now() + timedelta(days=3),
            end_date=utc_now() + timedelta(days=3, hours=3),
            status='published'
        )
        db.session.add_all([free_evt, paid_evt])
        db.session.flush()

        free_ticket = Ticket(
            ticket_code='TCK-FREE-01',
            event_id=free_evt.id,
            ticket_type='standard',
            name='Vé Miễn Phí',
            price=0,
            quota=50
        )
        paid_ticket = Ticket(
            ticket_code='TCK-PAID-01',
            event_id=paid_evt.id,
            ticket_type='vip',
            name='Vé VIP',
            price=500000,
            quota=20
        )
        db.session.add_all([free_ticket, paid_ticket])
        db.session.commit()

        from app.services.rag_service import build_retrieved_context
        ctx = build_retrieved_context("Tìm sự kiện miễn phí 0 đồng")
        assert "Lễ Khai Giảng ICTU" in ctx
        assert "0 VNĐ (MIỄN PHÍ)" in ctx

def test_chat_api_endpoint(client, app):
    with app.app_context():
        # Test post to /api/ai/chat with history
        res = client.post('/api/ai/chat', json={
            'message': 'Xin chào, bạn là ai?',
            'history': [
                {'role': 'user', 'content': 'Chào trợ lý'},
                {'role': 'model', 'content': 'Xin chào, tôi là EventAI Concierge!'}
            ]
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert len(data['response']) > 10
        assert data['mode'] in ('live', 'mock')

def test_ai_notification_generator(client, app):
    with app.app_context():
        evt = Event(
            event_code='EVT-NOTIF-TEST',
            title='Hội Thảo Cloud & DevOps 2026',
            category='Cloud & DevOps',
            description='Chia sẻ kiến thức Kubernetes và Docker',
            start_date=utc_now() + timedelta(days=2),
            end_date=utc_now() + timedelta(days=2, hours=4),
            status='published'
        )
        db.session.add(evt)
        db.session.commit()

        # Test POST /api/ai/generate-notification
        res = client.post('/api/ai/generate-notification', json={
            'event_id': evt.id,
            'notification_type': 'reminder',
            'target_audience': 'sinh viên và kỹ sư phần mềm đã đăng ký'
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert 'subject' in data
        assert len(data['subject']) > 5
        assert 'content' in data
        assert len(data['content']) > 20

def test_ai_feedback_summary_groups(client, app):
    with app.app_context():
        from app.models import Attendee, Ticket, Registration
        from app.services.sentiment_service import summarize_event_feedback_groups

        evt = Event(
            event_code='EVT-FB-TEST',
            title='AI Developer Day',
            start_date=utc_now() - timedelta(days=1),
            end_date=utc_now() - timedelta(days=1, hours=3)
        )
        db.session.add(evt)
        db.session.flush()

        att1 = Attendee(attendee_code='ATT-FB-01', full_name='Lê Thảo', email='thao.le@test.vn')
        att2 = Attendee(attendee_code='ATT-FB-02', full_name='Trần Hưng', email='hung.tran@test.vn')
        tck = Ticket(ticket_code='TCK-FB-01', event_id=evt.id, ticket_type='free', name='Free', quota=50)
        db.session.add_all([att1, att2, tck])
        db.session.flush()

        # Seed sample feedback comments covering opinions
        r1 = Registration(
            registration_code='REG-FB-1', event_id=evt.id, attendee_id=att1.id, ticket_id=tck.id,
            ticket_number='TCK-FB-1', feedback_rating=5,
            feedback_text='Nội dung hội thảo và diễn giả trình bày rất hay, bổ ích và chuyên sâu.'
        )
        r2 = Registration(
            registration_code='REG-FB-2', event_id=evt.id, attendee_id=att2.id, ticket_id=tck.id,
            ticket_number='TCK-FB-2', feedback_rating=4,
            feedback_text='Khâu check-in quét mã QR nhanh gọn, hội trường âm thanh rõ nét, wifi hơi chậm.'
        )
        db.session.add_all([r1, r2])
        db.session.commit()

        # Direct service test
        summary = summarize_event_feedback_groups(evt.id)
        assert summary['success'] is True
        assert 'content_and_speakers' in summary
        assert 'checkin_and_operations' in summary
        assert 'venue_and_logistics' in summary
        assert 'schedule_and_timing' in summary
        assert len(summary['actionable_takeaways']) > 0

        # API endpoint test
        res = client.get(f'/api/ai/feedback-summary/{evt.id}')
        assert res.status_code == 200
        api_data = res.get_json()
        assert api_data['success'] is True
        assert 'content_and_speakers' in api_data

def test_rag_faq_retrieval(app):
    with app.app_context():
        from app.models import EventFAQ
        from app.services.rag_service import build_retrieved_context

        evt = Event(
            event_code='EVT-FAQ-TEST',
            title='ICTU Tech Expo 2026',
            category='Trí tuệ nhân tạo',
            description='Triển lãm công nghệ',
            start_date=utc_now() + timedelta(days=3),
            end_date=utc_now() + timedelta(days=3, hours=4),
            status='published'
        )
        db.session.add(evt)
        db.session.flush()

        faq = EventFAQ(
            event_id=evt.id,
            question='Có bãi đỗ xe ô tô tại hội trường không?',
            answer='Có bãi đỗ xe ô tô và xe máy miễn phí trước cổng chính.',
            category='logistics'
        )
        db.session.add(faq)
        db.session.commit()

        ctx = build_retrieved_context("bãi đỗ xe tại ICTU Tech Expo", target_event_id=evt.id)
        assert "CÁC CÂU HỎI THƯỜNG GẶP (FAQ)" in ctx
        assert "bãi đỗ xe ô tô" in ctx


