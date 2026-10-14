"""
Unit Tests for Ticketing Quotas, Atomic Booking, and QR Check-in.
"""
from datetime import datetime, timedelta
from app.extensions import db, utc_now
from app.models import Event, Ticket, Registration

def test_ticket_quota_limit(app, sample_users):
    with app.app_context():
        evt = Event(
            event_code='EVT-TEST-01',
            title='Test Event Quota',
            category='Tech',
            start_date=utc_now() + timedelta(days=2),
            end_date=utc_now() + timedelta(days=2, hours=4),
            status='published'
        )
        db.session.add(evt)
        db.session.commit()

        # Ticket with quota = 1
        ticket = Ticket(
            event_id=evt.id,
            ticket_code='TCK-TEST-LTD',
            ticket_type='standard',
            name='Vé Giới Hạn 1 Chỗ',
            price=100000.0,
            quota=1,
            sold_count=0
        )
        db.session.add(ticket)
        db.session.commit()

        assert ticket.is_available is True
        assert ticket.remaining_quota == 1

        # Simulate 1 purchase
        ticket.sold_count += 1
        if ticket.sold_count >= ticket.quota:
            ticket.status = 'sold_out'
        db.session.commit()

        assert ticket.is_available is False
        assert ticket.remaining_quota == 0

def test_checkin_anti_duplicate(app, client, sample_users):
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-TEST-02',
            title='Checkin Event',
            start_date=utc_now(),
            end_date=utc_now() + timedelta(hours=3)
        )
        db.session.add(evt)
        db.session.commit()

        ticket = Ticket(event_id=evt.id, ticket_code='TCK-02', ticket_type='free', name='Free Ticket', quota=10)
        db.session.add(ticket)
        db.session.commit()

        reg = Registration(
            registration_code='REG-TEST-123',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=ticket.id,
            ticket_number='TCK-NUM-TEST-999',
            payment_status='free',
            checked_in=False
        )
        db.session.add(reg)
        db.session.commit()

    # Login as staff
    client.post('/auth/login', data={'username': 'staff', 'password': 'Staff@123'})

    # First Check-in: Should SUCCESS (200)
    res1 = client.post('/checkin/verify-api', json={'ticket_number': 'TCK-NUM-TEST-999'})
    data1 = res1.get_json()
    assert res1.status_code == 200
    assert data1['success'] is True
    assert data1['status'] == 'valid'

    # Second Check-in: Should FAIL with DUPLICATE WARNING (409)
    res2 = client.post('/checkin/verify-api', json={'ticket_number': 'TCK-NUM-TEST-999'})
    data2 = res2.get_json()
    assert res2.status_code == 409
    assert data2['success'] is False
    assert data2['status'] == 'duplicate'

def test_cancel_ticket_and_reclaim_quota(app, client, sample_users):
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-TEST-CANCEL',
            title='Cancel Test Event',
            start_date=utc_now() + timedelta(days=5),
            end_date=utc_now() + timedelta(days=5, hours=3)
        )
        db.session.add(evt)
        db.session.commit()

        ticket = Ticket(
            event_id=evt.id,
            ticket_code='TCK-CANCEL-01',
            ticket_type='free',
            name='Test Quota Ticket',
            quota=5,
            sold_count=5,
            status='sold_out'
        )
        db.session.add(ticket)
        db.session.commit()

        reg = Registration(
            registration_code='REG-CANCEL-999',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=ticket.id,
            ticket_number='TCK-NUM-CANCEL-111',
            registration_status='confirmed',
            payment_status='free',
            checked_in=False
        )
        db.session.add(reg)
        db.session.commit()
        reg_id = reg.id

    # Login as attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    # Perform Cancel Ticket POST
    res = client.post(f'/tickets/cancel/{reg_id}', follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        updated_reg = db.session.get(Registration, reg_id)
        assert updated_reg is not None
        assert updated_reg.registration_status == 'cancelled'

        updated_ticket = db.session.get(Ticket, updated_reg.ticket_id)
        assert updated_ticket is not None
        assert updated_ticket.sold_count == 4
        assert updated_ticket.status == 'active'
        assert updated_ticket.is_available is True

def test_re_register_after_cancel_or_pending(app, client, sample_users):
    """Test ensuring no UNIQUE constraint violation when re-registering an event."""
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-RE-REG',
            title='Re-Register Test Event',
            start_date=utc_now() + timedelta(days=10),
            end_date=utc_now() + timedelta(days=10, hours=4)
        )
        db.session.add(evt)
        db.session.commit()

        ticket = Ticket(
            event_id=evt.id,
            ticket_code='TCK-RE-01',
            ticket_type='standard',
            name='Paid Ticket',
            price=200000.0,
            quota=10,
            sold_count=0,
            status='active'
        )
        db.session.add(ticket)
        db.session.commit()
        evt_id = evt.id
        ticket_id = ticket.id

    # Login as attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    # Step 1: Register ticket (creates pending registration)
    res1 = client.post(f'/tickets/register/{evt_id}', data={'ticket_id': ticket_id}, follow_redirects=False)
    assert res1.status_code == 302
    assert '/tickets/checkout/' in res1.headers['Location']

    # Step 2: Try to re-register the same event without completing checkout (should update pending record without error)
    res2 = client.post(f'/tickets/register/{evt_id}', data={'ticket_id': ticket_id}, follow_redirects=False)
    assert res2.status_code == 302
    assert '/tickets/checkout/' in res2.headers['Location']

    with app.app_context():
        regs = Registration.query.filter_by(event_id=evt_id, attendee_id=att_id).all()
        assert len(regs) == 1
        assert regs[0].registration_status == 'pending'

def test_auto_qr_generation_and_download(app, client, sample_users):
    """Kiểm tra tự động sinh mã QR và tải file mã QR đính kèm."""
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-QR-TEST',
            title='QR Auto Gen Test Event',
            start_date=utc_now() + timedelta(days=3),
            end_date=utc_now() + timedelta(days=3, hours=3)
        )
        db.session.add(evt)
        db.session.commit()

        ticket = Ticket(
            event_id=evt.id,
            ticket_code='TCK-QR-FREE',
            ticket_type='free',
            name='Free QR Ticket',
            price=0.0,
            quota=10,
            sold_count=0
        )
        db.session.add(ticket)
        db.session.commit()
        evt_id = evt.id
        ticket_id = ticket.id

    # Login as attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    # Register free ticket
    res = client.post(f'/tickets/register/{evt_id}', data={'ticket_id': ticket_id}, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        reg = Registration.query.filter_by(event_id=evt_id, attendee_id=att_id).first()
        assert reg is not None
        assert reg.ticket_number.startswith('TCK-')
        assert reg.qr_code_path is not None
        assert reg.qr_code_path.endswith('.svg')
        reg_id = reg.id

    # Download QR SVG
    dl_res = client.get(f'/tickets/download-qr/{reg_id}')
    assert dl_res.status_code == 200
    assert 'image/svg+xml' in dl_res.content_type

def test_event_attendees_roster_and_quick_checkin(app, client, sample_users):
    """Kiểm tra API lấy danh sách người tham dự theo sự kiện và API check-in nhanh / hoàn tác."""
    with app.app_context():
        att_id = sample_users['attendee_profile_id']

        evt = Event(
            event_code='EVT-ROSTER-01',
            title='Roster API Event',
            start_date=utc_now() + timedelta(days=1),
            end_date=utc_now() + timedelta(days=1, hours=2)
        )
        db.session.add(evt)
        db.session.commit()

        ticket = Ticket(
            event_id=evt.id,
            ticket_code='TCK-ROSTER-01',
            ticket_type='standard',
            name='Standard Ticket',
            price=150000.0,
            quota=20,
            sold_count=1
        )
        db.session.add(ticket)
        db.session.commit()

        reg = Registration(
            registration_code='REG-ROSTER-001',
            event_id=evt.id,
            attendee_id=att_id,
            ticket_id=ticket.id,
            registration_status='confirmed',
            payment_status='paid',
            ticket_number='TCK-ROSTER-USER1-999',
            checked_in=False
        )
        db.session.add(reg)
        db.session.commit()
        evt_id = evt.id
        reg_id = reg.id

    # Login as staff
    client.post('/auth/login', data={'username': 'staff', 'password': 'Staff@123'})

    # 1. Test Event Attendees API
    res = client.get(f'/checkin/api/event-attendees/{evt_id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['total_registered'] == 1
    assert data['total_checked_in'] == 0
    assert len(data['attendees']) == 1
    assert data['attendees'][0]['ticket_number'] == 'TCK-ROSTER-USER1-999'

    # 2. Test Quick Checkin API
    qc_res = client.post(f'/checkin/api/quick-checkin/{reg_id}')
    assert qc_res.status_code == 200
    qc_data = qc_res.get_json()
    assert qc_data['success'] is True

    with app.app_context():
        updated = db.session.get(Registration, reg_id)
        assert updated is not None
        assert updated.checked_in is True
        assert updated.checked_in_by == 'staff'

    # 3. Test Undo Checkin API
    undo_res = client.post(f'/checkin/api/undo-checkin/{reg_id}')
    assert undo_res.status_code == 200
    undo_data = undo_res.get_json()
    assert undo_data['success'] is True

    with app.app_context():
        re_updated = db.session.get(Registration, reg_id)
        assert re_updated is not None
        assert re_updated.checked_in is False

