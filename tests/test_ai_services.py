"""
Unit Tests for AI Services (RAG Chat, Fallback Mock, Recommendations, Predictive, Sentiment).
"""
from datetime import datetime, timedelta
from app.extensions import db
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
            start_date=datetime.utcnow() + timedelta(days=1),
            end_date=datetime.utcnow() + timedelta(days=1, hours=4),
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
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(hours=2),
            status='published'
        )
        evt2 = Event(
            event_code='EVT-BIZ-02',
            title='Kinh Doanh Bất Động Sản',
            category='Kinh doanh',
            description='Đầu tư tài chính',
            tags='Business, Finance',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(hours=2),
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
            start_date=datetime.utcnow() + timedelta(days=5),
            end_date=datetime.utcnow() + timedelta(days=5, hours=3)
        )
        db.session.add(evt)
        db.session.commit()

        stats = predict_event_attendance(evt.id)
        assert stats is not None
        assert 'expected_attendance' in stats
        assert 'predicted_showup_rate' in stats
        assert stats['venue_capacity'] == 100
