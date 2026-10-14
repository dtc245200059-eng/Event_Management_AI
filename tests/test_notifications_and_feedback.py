"""
Integration Tests for Notifications, Attendee Inbox, Organizer RBAC, and Feedback.
Covers Requirements 3.1.1, 3.1.6, 3.1.7, 3.1.8 from de_tai_09.md.
"""
from datetime import datetime, timedelta
from app.extensions import db, utc_now
from app.models import User, Event, Ticket, Registration, Attendee, Notification

def test_organizer_role_access(app, client, sample_users):
    with app.app_context():
        # Create organizer user
        org = User(
            username='org_tester',
            email='org_test@eventai.vn',
            full_name='Trưởng Ban Tổ Chức Test',
            role='organizer'
        )
        org.set_password('Org@123')
        db.session.add(org)
        db.session.commit()

    # 1. Login as Attendee -> Accessing /notifications/manage should be FORBIDDEN (403)
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    res_att = client.get('/notifications/manage')
    assert res_att.status_code == 403

    # Logout attendee
    client.get('/auth/logout')

    # 2. Login as Organizer -> Accessing /notifications/manage should be ALLOWED (200)
    client.post('/auth/login', data={'username': 'org_tester', 'password': 'Org@123'})
    res_org = client.get('/notifications/manage')
    assert res_org.status_code == 200

    # 3. Accessing /events/manage should be ALLOWED (200) for Organizer
    res_evt = client.get('/events/manage')
    assert res_evt.status_code == 200

def test_notification_creation_and_recipient_calc(app, client, sample_users):
    with app.app_context():
        admin = db.session.get(User, sample_users['admin_id'])
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-NOTIF-CALC',
            title='Diễn Đàn Chuyển Đổi Số 2026',
            start_date=utc_now() + timedelta(days=5),
            end_date=utc_now() + timedelta(days=5, hours=3)
        )
        db.session.add(evt)
        db.session.flush()

        tck = Ticket(event_id=evt.id, ticket_code='TCK-CALC-01', ticket_type='standard', name='Standard', price=0, quota=50)
        db.session.add(tck)
        db.session.flush()

        reg = Registration(
            registration_code='REG-CALC-01',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=tck.id,
            ticket_number='TCK-CALC-99',
            registration_status='confirmed',
            checked_in=True
        )
        db.session.add(reg)
        db.session.commit()
        evt_id = evt.id

    # Login as admin
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})

    # Create notification for checked_in audience
    res = client.post('/notifications/create', data={
        'event_id': evt_id,
        'notification_type': 'thank_you',
        'target_audience': 'checked_in',
        'title': '[Tri Ân] Cảm ơn bạn đã tham gia Diễn đàn Chuyển Đổi Số',
        'content': 'Ban tổ chức xin gửi lời cảm ơn trân trọng tới quý khách.'
    }, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        notif = Notification.query.filter_by(event_id=evt_id).first()
        assert notif is not None
        assert notif.title == '[Tri Ân] Cảm ơn bạn đã tham gia Diễn đàn Chuyển Đổi Số'
        assert notif.notification_type == 'thank_you'
        assert notif.recipient_count == 1  # Exactly 1 checked-in attendee

def test_attendee_notification_inbox(app, client, sample_users):
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-INBOX-TEST',
            title='Lễ Khai Mạc Năm Học',
            start_date=utc_now() + timedelta(days=7),
            end_date=utc_now() + timedelta(days=7, hours=2)
        )
        db.session.add(evt)
        db.session.flush()

        tck = Ticket(event_id=evt.id, ticket_code='TCK-INBOX-1', ticket_type='free', name='Free', quota=10)
        db.session.add(tck)
        db.session.flush()

        # Attendee registers
        reg = Registration(
            registration_code='REG-INBOX-1',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=tck.id,
            ticket_number='TCK-INBOX-NUM',
            registration_status='confirmed'
        )
        # Broadcast notification for this event
        notif = Notification(
            event_id=evt.id,
            title='[Nhắc Lịch] Chuẩn bị trang phục tham dự lễ khai mạc',
            notification_type='reminder',
            content='Trang phục lịch sự, có mặt đúng giờ.',
            recipient_count=1,
            status='sent'
        )
        db.session.add_all([reg, notif])
        db.session.commit()

    # Login as attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    res = client.get('/notifications/inbox')
    assert res.status_code == 200
    assert 'Chuẩn bị trang phục tham dự lễ khai mạc' in res.get_data(as_text=True)

def test_feedback_submission_and_sentiment_rating(app, client, sample_users):
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-FEEDBACK-TEST',
            title='Workshop Phân Tích Dữ Liệu',
            start_date=utc_now() - timedelta(days=1),
            end_date=utc_now() - timedelta(days=1, hours=3)
        )
        db.session.add(evt)
        db.session.flush()

        tck = Ticket(event_id=evt.id, ticket_code='TCK-FB-T1', ticket_type='free', name='Free', quota=20)
        db.session.add(tck)
        db.session.flush()

        reg = Registration(
            registration_code='REG-FB-T1',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=tck.id,
            ticket_number='TCK-FB-NUM-1',
            checked_in=True
        )
        db.session.add(reg)
        db.session.commit()
        reg_id = reg.id

    # Login as attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    # Submit 5-star positive feedback
    res = client.post(f'/tickets/feedback/{reg_id}', data={
        'feedback_rating': 5,
        'feedback_text': 'Hội thảo rất tuyệt vời, diễn giả nhiệt tình và tài liệu chất lượng cao!'
    }, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        updated_reg = db.session.get(Registration, reg_id)
        assert updated_reg.feedback_rating == 5
        assert updated_reg.sentiment == 'positive'
        assert updated_reg.sentiment_score > 0
