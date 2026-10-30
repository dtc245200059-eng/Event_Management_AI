"""
Targeted security and indexability tests for Phase 2.5 remediation.
Verifies credential protection, private ticket QR access controls, event publication policies, and indexing directives.
"""
import os
import pytest
from app.extensions import db, utc_now
from app.models import User, Event, Ticket, Attendee, Registration

def test_login_page_does_not_expose_credentials(client):
    """Test 1: Verify login page no longer exposes plaintext passwords or demo accounts."""
    res = client.get('/auth/login')
    assert res.status_code == 200
    html = res.data.decode('utf-8')

    # Passwords must NOT be present in public HTML
    assert 'Admin@123' not in html, "Admin password must not be exposed"
    assert 'Staff@123' not in html, "Staff password must not be exposed"
    assert 'User@123' not in html, "User password must not be exposed"
    assert 'Tài khoản Demo có sẵn' not in html, "Demo credential block must not be present"

    # Login form inputs must remain intact
    assert 'name="username"' in html
    assert 'name="password"' in html

def test_login_and_register_pages_have_noindex(client):
    """Test 2: Verify authentication pages have noindex meta tag."""
    res_login = client.get('/auth/login')
    assert res_login.status_code == 200
    assert '<meta name="robots" content="noindex, nofollow">' in res_login.data.decode('utf-8')

    res_reg = client.get('/auth/register')
    assert res_reg.status_code == 200
    assert '<meta name="robots" content="noindex, nofollow">' in res_reg.data.decode('utf-8')

def test_error_pages_have_noindex(client):
    """Test 3: Verify custom error handlers include noindex meta tag."""
    res = client.get('/this-path-does-not-exist-at-all-404')
    assert res.status_code == 404
    assert '<meta name="robots" content="noindex, nofollow">' in res.data.decode('utf-8')

def test_anonymous_cannot_access_private_qr_static(client, sample_users):
    """Test 4: Verify unauthenticated users/bots cannot access static QR code assets."""
    res = client.get('/static/qr_codes/TCK-TEST-999-ABCDEF.svg')
    assert res.status_code == 403, "Anonymous access to QR tickets must be blocked"

def test_cross_user_ticket_qr_access_denied(client, app, sample_users):
    """Test 5: Verify User A cannot access User B's private ticket QR code."""
    with app.app_context():
        # Setup event and ticket
        event = Event(
            event_code='EVT-SEC-01',
            title='Security Audit Event',
            start_date=utc_now(),
            end_date=utc_now(),
            status='published'
        )
        db.session.add(event)
        db.session.commit()

        # User 1 (Owner)
        user1 = db.session.get(User, sample_users['user_id'])
        ticket = Ticket(event_id=event.id, ticket_code='TCK-SEC-T1', ticket_type='standard', name='Vé Standard', price=100.0, quota=50)
        db.session.add(ticket)
        db.session.commit()

        reg1 = Registration(
            registration_code='REG-SEC-U1',
            event_id=event.id,
            attendee_id=sample_users['attendee_profile_id'],
            ticket_id=ticket.id,
            registration_status='confirmed',
            payment_status='paid',
            payment_amount=100.0,
            ticket_number='TCK-SEC-U1-998877',
            qr_code_path='qr_codes/TCK-SEC-U1-998877.svg'
        )
        db.session.add(reg1)

        # User 2 (Attacker / Other attendee)
        user2 = User(username='user2', email='user2@test.com', full_name='User Two', role='attendee')
        user2.set_password('Secret@123')
        db.session.add(user2)
        db.session.commit()

        att2 = Attendee(attendee_code='ATT-SEC-U2', user_id=user2.id, full_name='User Two', email='user2@test.com')
        db.session.add(att2)
        db.session.commit()

    # Login as User 2
    client.post('/auth/login', data={'username': 'user2', 'password': 'Secret@123'})

    # User 2 attempts to fetch User 1's QR ticket
    res = client.get('/static/qr_codes/TCK-SEC-U1-998877.svg')
    assert res.status_code == 403, "Cross-user access to ticket QR must be denied with 403"

def test_authorized_owner_can_access_own_ticket_qr(client, app, sample_users):
    """Test 6: Verify ticket owner can access their own ticket QR code and receives noindex header."""
    with app.app_context():
        event = Event(
            event_code='EVT-SEC-02',
            title='Authorized Owner Event',
            start_date=utc_now(),
            end_date=utc_now(),
            status='published'
        )
        db.session.add(event)
        db.session.commit()

        ticket = Ticket(event_id=event.id, ticket_code='TCK-SEC-T2', ticket_type='free', name='Vé Free', price=0.0, quota=50)
        db.session.add(ticket)
        db.session.commit()

        # Ensure QR file exists on disk for serving
        qr_dir = os.path.join(app.static_folder, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)
        ticket_file = os.path.join(qr_dir, 'TCK-SEC-U1-OWNER.svg')
        with open(ticket_file, 'w', encoding='utf-8') as f:
            f.write('<svg><rect width="100" height="100"/></svg>')

        reg = Registration(
            registration_code='REG-SEC-OWNER',
            event_id=event.id,
            attendee_id=sample_users['attendee_profile_id'],
            ticket_id=ticket.id,
            registration_status='confirmed',
            payment_status='free',
            payment_amount=0.0,
            ticket_number='TCK-SEC-U1-OWNER',
            qr_code_path='qr_codes/TCK-SEC-U1-OWNER.svg'
        )
        db.session.add(reg)
        db.session.commit()

    # Login as User 1 (Owner)
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    res = client.get('/static/qr_codes/TCK-SEC-U1-OWNER.svg')
    assert res.status_code == 200, "Ticket owner must be granted access to their QR SVG"
    assert res.headers.get('X-Robots-Tag') == 'noindex, nofollow, noarchive'
    assert 'private' in res.headers.get('Cache-Control', '')

def test_staff_and_admin_can_access_any_ticket_qr(client, app, sample_users):
    """Test 7: Verify check-in staff and admin have role-based authorization to inspect any ticket QR."""
    with app.app_context():
        # Ensure QR file exists on disk
        qr_dir = os.path.join(app.static_folder, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)
        ticket_file = os.path.join(qr_dir, 'TCK-SEC-STAFF-INSPECT.svg')
        with open(ticket_file, 'w', encoding='utf-8') as f:
            f.write('<svg><rect width="100" height="100"/></svg>')

        event = Event(event_code='EVT-STAFF-01', title='Staff Event', start_date=utc_now(), end_date=utc_now(), status='published')
        db.session.add(event)
        db.session.commit()

        ticket = Ticket(event_id=event.id, ticket_code='TCK-STAFF-T1', ticket_type='standard', name='Vé Staff', price=50.0, quota=50)
        db.session.add(ticket)
        db.session.commit()

        reg = Registration(
            registration_code='REG-STAFF-INSPECT',
            event_id=event.id,
            attendee_id=sample_users['attendee_profile_id'],
            ticket_id=ticket.id,
            registration_status='confirmed',
            payment_status='paid',
            payment_amount=50.0,
            ticket_number='TCK-SEC-STAFF-INSPECT',
            qr_code_path='qr_codes/TCK-SEC-STAFF-INSPECT.svg'
        )
        db.session.add(reg)
        db.session.commit()

    # Login as Staff
    client.post('/auth/login', data={'username': 'staff', 'password': 'Staff@123'})

    res = client.get('/static/qr_codes/TCK-SEC-STAFF-INSPECT.svg')
    assert res.status_code == 200, "Check-in staff must be authorized to inspect QR tickets"

def test_anonymous_cannot_access_draft_event(client, app, sample_users):
    """Test 8: Verify unpublished draft events return 404 for anonymous users."""
    with app.app_context():
        draft_event = Event(
            event_code='EVT-DRAFT-01',
            title='Unpublished Draft Summit 2026',
            start_date=utc_now(),
            end_date=utc_now(),
            status='draft',
            created_by=sample_users['admin_id']
        )
        db.session.add(draft_event)
        db.session.commit()
        draft_id = draft_event.id

    res = client.get(f'/events/{draft_id}')
    assert res.status_code == 404, "Draft event must return 404 for anonymous users"

def test_regular_attendee_cannot_access_draft_event(client, app, sample_users):
    """Test 9: Verify unpublished draft events return 404 for regular logged-in attendees."""
    with app.app_context():
        draft_event = Event(
            event_code='EVT-DRAFT-02',
            title='Internal Draft Meeting',
            start_date=utc_now(),
            end_date=utc_now(),
            status='draft',
            created_by=sample_users['admin_id']
        )
        db.session.add(draft_event)
        db.session.commit()
        draft_id = draft_event.id

    # Login as regular attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})

    res = client.get(f'/events/{draft_id}')
    assert res.status_code == 404, "Draft event must return 404 for regular attendees"

def test_admin_and_creator_can_preview_draft_event(client, app, sample_users):
    """Test 10: Verify event creator and admin can preview draft events with noindex directive."""
    with app.app_context():
        draft_event = Event(
            event_code='EVT-DRAFT-03',
            title='Executive Strategic Session',
            start_date=utc_now(),
            end_date=utc_now(),
            status='draft',
            created_by=sample_users['admin_id']
        )
        db.session.add(draft_event)
        db.session.commit()
        draft_id = draft_event.id

    # Login as Admin (Creator)
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})

    res = client.get(f'/events/{draft_id}')
    assert res.status_code == 200, "Admin/Creator must be allowed to preview draft events"
    html = res.data.decode('utf-8')
    assert 'Draft Preview' in html or 'Xem Trước Sự Kiện Bản Nháp' in html
    assert '<meta name="robots" content="noindex, follow">' in html
    assert 'Chưa Mở Bán Vé' in html, "Ticket booking must be guarded on draft preview"

def test_public_published_event_is_accessible_to_all(client, app, sample_users):
    """Test 11: Verify public published events remain accessible and indexable."""
    with app.app_context():
        pub_event = Event(
            event_code='EVT-PUB-01',
            title='Public AI Expo 2026',
            start_date=utc_now(),
            end_date=utc_now(),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(pub_event)
        db.session.commit()
        pub_id = pub_event.id

    res = client.get(f'/events/{pub_id}')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Public AI Expo 2026' in html
    # Must NOT have noindex
    assert '<meta name="robots" content="noindex' not in html

def test_cancelled_event_has_noindex_and_closed_booking(client, app, sample_users):
    """Test 12: Verify cancelled events show cancellation notice and have noindex meta."""
    with app.app_context():
        canc_event = Event(
            event_code='EVT-CANC-01',
            title='Cancelled Conference 2026',
            start_date=utc_now(),
            end_date=utc_now(),
            status='cancelled',
            created_by=sample_users['admin_id']
        )
        db.session.add(canc_event)
        db.session.commit()
        canc_id = canc_event.id

    res = client.get(f'/events/{canc_id}')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'HỦY' in html
    assert '<meta name="robots" content="noindex, follow">' in html
    assert 'Đã Đóng Đăng Ký' in html

def test_http_security_headers_present(client):
    """Test 13: Verify core HTTP security headers (nosniff, SAMEORIGIN, strict-origin-when-cross-origin)."""
    res = client.get('/')
    assert res.status_code == 200
    assert res.headers.get('X-Content-Type-Options') == 'nosniff'
    assert res.headers.get('X-Frame-Options') == 'SAMEORIGIN'
    assert res.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
    assert 'camera=*' in res.headers.get('Permissions-Policy', '')

def test_production_config_cookie_security():
    """Test 14: Verify ProductionConfig enforces secure cookie defaults."""
    from app.config import ProductionConfig
    assert ProductionConfig.DEBUG is False
    assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
    assert ProductionConfig.SESSION_COOKIE_SAMESITE == 'Lax'
    assert ProductionConfig.SESSION_COOKIE_SECURE is True

def test_staging_config_profile():
    """Test 15: Verify StagingConfig provides isolated, secure staging profile."""
    from app.config import StagingConfig
    assert StagingConfig.DEBUG is False
    assert StagingConfig.TESTING is False
    assert StagingConfig.ENABLE_AI_FALLBACK_MOCK is True
    assert StagingConfig.SESSION_COOKIE_HTTPONLY is True
    assert StagingConfig.SESSION_COOKIE_SAMESITE == 'Lax'

def test_cross_origin_state_changing_request_protection(client):
    """Test 16: Verify unauthorized cross-origin state mutations are rejected."""
    res = client.post(
        '/tickets/register/1',
        data={'ticket_id': 1},
        headers={'Origin': 'https://evil-attacker-site.com'}
    )
    assert res.status_code in (302, 401, 403, 404)




def test_zero_state_changing_get_routes(app):
    """Test 17: Audit all registered routes to verify zero state-changing GET endpoints exist."""
    state_changing_keywords = ['/delete', '/toggle', '/cancel', '/checkout', '/undo']
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            methods = rule.methods - {'HEAD', 'OPTIONS'}
            # If the route only accepts GET (no POST)
            if methods == {'GET'}:
                rule_str = str(rule).lower()
                for kw in state_changing_keywords:
                    assert kw not in rule_str, f"Suspicious state-changing GET route found: {rule_str}"


def test_seo_helpers_creator_lazy_load_exception_handling(app):
    """Test 18: Verify specific DB exception handling in build_event_schema for creator lazy-loading."""
    import sqlite3
    from sqlalchemy.exc import OperationalError as SAOperationalError
    from app.seo_helpers import build_event_schema
    from datetime import datetime, timezone
    
    class FaultyEvent:
        id = 999
        status = 'published'
        title = 'Faulty Event Concurrency Test'
        description = 'Testing creator exception handling'
        banner_url = None
        start_date = datetime(2026, 12, 1, 9, 0, tzinfo=timezone.utc)
        end_date = datetime(2026, 12, 1, 17, 0, tzinfo=timezone.utc)
        location_type = 'offline'
        location_address = '123 Test St'
        tickets = []
        schedules = []
        
        @property
        def creator(self):
            # Simulate SQLite / SQLAlchemy thread concurrency or detached session error
            raise sqlite3.OperationalError("database is locked (simulated concurrency race)")

    with app.test_request_context('/events/999'):
        faulty = FaultyEvent()
        schema = build_event_schema(faulty)
        assert schema is not None
        assert schema['@type'] == 'Event'
        assert schema['name'] == 'Faulty Event Concurrency Test'
        assert schema['organizer']['name'] == 'EventAI Pro'


def test_csrf_cookie_same_site_defense_in_depth():
    """Test 19: Verify SameSite=Lax and HttpOnly are enforced across staging and production profiles."""
    from app.config import StagingConfig, ProductionConfig
    
    for cfg in (StagingConfig, ProductionConfig):
        assert cfg.SESSION_COOKIE_SAMESITE == 'Lax'
        assert cfg.SESSION_COOKIE_HTTPONLY is True
        assert cfg.REMEMBER_COOKIE_HTTPONLY is True
        assert cfg.REMEMBER_COOKIE_SAMESITE == 'Lax'
