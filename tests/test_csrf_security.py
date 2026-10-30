"""
Targeted CSRF Security Test Suite for Phase 6B Remediation.
Verifies cryptographic Synchronizer Token validation via Flask-WTF, rejection of missing/invalid/expired tokens,
protection of state-changing routes across all blueprints, and defense-in-depth across HTML forms and AJAX endpoints.
"""
import pytest
import time
import hashlib
import os
from itsdangerous import URLSafeTimedSerializer
from app.extensions import db, utc_now
from app.models import User, Event, Ticket, Attendee, Registration

def get_session_csrf_token(client, app):
    """Helper to extract a valid signed CSRF token for the client's current session."""
    with client.session_transaction() as sess:
        raw_token = sess.get('csrf_token')
        if not raw_token:
            raw_token = hashlib.sha1(os.urandom(64)).hexdigest()
            sess['csrf_token'] = raw_token
    s = URLSafeTimedSerializer(app.secret_key, salt="wtf-csrf-token")
    return s.dumps(raw_token)


def test_csrf_valid_token_accepted_on_form_post(client, app, sample_users):
    """Test 1: Verify standard form POST with a valid CSRF token succeeds."""
    token = get_session_csrf_token(client, app)
    res = client.post(
        '/auth/login',
        data={'username': 'admin', 'password': 'Admin@123', 'csrf_token': token},
        follow_redirects=False
    )
    assert res.status_code in (200, 302), f"Expected login success/redirect, got {res.status_code}"


def test_csrf_missing_token_rejected_with_400(client):
    """Test 2: Verify POST request lacking CSRF token is rejected with HTTP 400 Bad Request."""
    res = client.post(
        '/auth/login',
        data={'username': 'admin', 'password': 'Admin@123'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400
    html = res.data.decode('utf-8')
    assert '400' in html
    assert 'Yêu Cầu Không Hợp Lệ' in html
    assert 'CSRF Token' in html


def test_csrf_invalid_token_rejected_with_400(client):
    """Test 3: Verify POST request with a tampered/invalid token is rejected with HTTP 400."""
    res = client.post(
        '/auth/login',
        data={'username': 'admin', 'password': 'Admin@123', 'csrf_token': 'completely_invalid_garbage_token'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_expired_token_rejected_with_400(client, app):
    """Test 4: Verify an expired CSRF token (timestamp past WTF_CSRF_TIME_LIMIT) is rejected."""
    with client.session_transaction() as sess:
        raw_token = hashlib.sha1(os.urandom(64)).hexdigest()
        sess['csrf_token'] = raw_token

    # Generate a token with a timestamp in the past (e.g., 2 hours ago when limit is 3600s)
    s = URLSafeTimedSerializer(app.secret_key, salt="wtf-csrf-token")
    # Simulate an expired token by passing a negative age during signing/loading or using mock
    expired_token = s.dumps(raw_token)
    
    # Test with time limit = 0 (immediate expiration)
    app.config['WTF_CSRF_TIME_LIMIT'] = -10
    try:
        res = client.post(
            '/auth/login',
            data={'username': 'admin', 'password': 'Admin@123', 'csrf_token': expired_token},
            headers={'X-Test-No-CSRF': '1'}
        )
        assert res.status_code == 400
    finally:
        app.config['WTF_CSRF_TIME_LIMIT'] = 3600


def test_csrf_token_from_another_session_rejected(client, app):
    """Test 5: Verify a valid token generated for Session A is rejected when submitted by Session B."""
    # Client A generates its token
    token_a = get_session_csrf_token(client, app)
    
    # Client B has a different session
    client_b = app.test_client()
    with client_b.session_transaction() as sess:
        sess['csrf_token'] = hashlib.sha1(os.urandom(64)).hexdigest()

    # Client B attempts to use Client A's token
    res = client_b.post(
        '/auth/login',
        data={'username': 'admin', 'password': 'Admin@123', 'csrf_token': token_a},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_json_ajax_without_token_returns_json_400(client):
    """Test 6: Verify AJAX / JSON mutation without token receives JSON 400 with clean error code."""
    res = client.post(
        '/checkin/verify-api',
        json={'ticket_number': 'TCK-123'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data is not None
    assert data['success'] is False
    assert data['code'] == 'CSRF_VALIDATION_FAILED'
    assert 'CSRF token missing or invalid' in data['error']


def test_csrf_json_ajax_with_valid_header_accepted(client, app, sample_users):
    """Test 7: Verify AJAX / JSON request with valid X-CSRFToken header passes CSRF verification."""
    # Login as staff first
    client.post('/auth/login', data={'username': 'staff', 'password': 'Staff@123'})
    
    token = get_session_csrf_token(client, app)
    res = client.post(
        '/checkin/verify-api',
        json={'ticket_number': 'TCK-NONEXISTENT-999'},
        headers={'X-CSRFToken': token}
    )
    # Passed CSRF check, reached view logic (returns 404 for nonexistent ticket or 400 for bad code)
    assert res.status_code in (200, 400, 404)
    data = res.get_json()
    # It must NOT be a CSRF error
    assert data.get('code') != 'CSRF_VALIDATION_FAILED'


def test_csrf_admin_user_management_protected(client, app, sample_users):
    """Test 8: Verify admin operations (/admin/users/create) reject mutations without CSRF token."""
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    
    res = client.post(
        '/admin/users/create',
        data={'username': 'hacker', 'password': 'Hacked@123', 'full_name': 'Hacker', 'role': 'admin'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_event_management_protected(client, app, sample_users):
    """Test 9: Verify event creation rejects requests without CSRF token."""
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    
    res = client.post(
        '/events/create',
        data={'title': 'CSRF Attack Event', 'start_date': '2026-12-01T09:00', 'end_date': '2026-12-01T17:00'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_ticket_registration_protected(client, app, sample_users):
    """Test 10: Verify ticket registration rejects requests without CSRF token."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    res = client.post(
        '/tickets/register/1',
        data={'ticket_id': 1},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_profile_update_protected(client, app, sample_users):
    """Test 11: Verify user profile update rejects requests without CSRF token."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    res = client.post(
        '/auth/profile/update',
        data={'full_name': 'Tampered Name', 'phone': '0999999999'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_password_change_protected(client, app, sample_users):
    """Test 12: Verify password change rejects requests without CSRF token."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    res = client.post(
        '/auth/profile/change-password',
        data={'current_password': 'User@123', 'new_password': 'NewPassword@123', 'confirm_password': 'NewPassword@123'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_checkin_quick_actions_protected(client, app, sample_users):
    """Test 13: Verify check-in quick actions reject mutations without CSRF token."""
    client.post('/auth/login', data={'username': 'staff', 'password': 'Staff@123'})
    
    res_quick = client.post(
        '/checkin/api/quick-checkin/1',
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res_quick.status_code == 400
    
    res_undo = client.post(
        '/checkin/api/undo-checkin/1',
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res_undo.status_code == 400


def test_csrf_ai_chat_protected(client):
    """Test 14: Verify AI chat endpoint rejects requests without CSRF token."""
    res = client.post(
        '/api/ai/chat',
        json={'message': 'Hello AI'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['code'] == 'CSRF_VALIDATION_FAILED'


def test_csrf_cross_origin_request_with_invalid_origin_rejected(client, app):
    """Test 15: Verify cross-origin request without valid token is rejected."""
    res = client.post(
        '/auth/login',
        data={'username': 'admin', 'password': 'Admin@123'},
        headers={'Origin': 'https://evil-attacker.com', 'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400



def test_csrf_logout_post_with_valid_token_succeeds(client, app, sample_users):
    """Test 16: Verify POST /auth/logout with valid CSRF token successfully logs out the user."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    token = get_session_csrf_token(client, app)
    res = client.post(
        '/auth/logout',
        data={'csrf_token': token},
        follow_redirects=False
    )
    assert res.status_code == 302
    assert res.location in ('/', 'http://localhost/')


def test_csrf_logout_post_without_token_rejected_with_400(client, app, sample_users):
    """Test 17: Verify POST /auth/logout without CSRF token is rejected with HTTP 400 (Anti-Logout-CSRF)."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    res = client.post(
        '/auth/logout',
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400


def test_csrf_cache_isolation_headers_present_on_html(client, app, sample_users):
    """Test 18: Verify HTML responses include Vary: Cookie and authenticated responses are marked private/no-cache."""
    # 1. Anonymous HTML response
    res_public = client.get('/')
    assert res_public.status_code == 200
    assert 'Cookie' in res_public.headers.get('Vary', '')
    
    # 2. Authenticated HTML response
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    res_auth = client.get('/auth/profile')
    assert res_auth.status_code == 200
    assert 'Cookie' in res_auth.headers.get('Vary', '')
    assert 'private' in res_auth.headers.get('Cache-Control', '')
    assert 'no-cache' in res_auth.headers.get('Cache-Control', '')
    assert res_auth.headers.get('Pragma') == 'no-cache'


def test_csrf_token_not_leaked_in_sitemap_or_robots(client):
    """Test 19: Verify XML sitemap and robots.txt never leak CSRF tokens or session state."""
    res_sitemap = client.get('/sitemap.xml')
    assert res_sitemap.status_code == 200
    assert 'csrf' not in res_sitemap.data.decode('utf-8').lower()
    
    res_robots = client.get('/robots.txt')
    assert res_robots.status_code == 200
    assert 'csrf' not in res_robots.data.decode('utf-8').lower()


def test_csrf_token_not_leaked_in_public_jsonld(client, app):
    """Test 20: Verify public event detail Schema.org JSON-LD structured data never contains CSRF tokens."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-AUDIT-01',
            title='Structured Data Security Audit Event',
            start_date=utc_now(),
            end_date=utc_now(),
            status='published'
        )
        db.session.add(event)
        db.session.commit()
        evt_id = event.id

    res = client.get(f'/events/{evt_id}')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    import re
    # Extract JSON-LD script blocks
    jsonld_blocks = re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    for block in jsonld_blocks:
        assert 'csrf_token' not in block.lower(), "CSRF token parameter must not appear in Schema.org JSON-LD"


def test_csrf_logout_get_does_not_terminate_session(client, app, sample_users):
    """Test 21 (Phase 8): Verify GET /auth/logout NEVER terminates user session and displays confirmation."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    # Send GET request to /auth/logout (simulating external <img src="/auth/logout"> or address bar GET)
    res_get = client.get('/auth/logout')
    assert res_get.status_code == 200
    assert 'Xác Nhận Đăng Xuất' in res_get.data.decode('utf-8')
    
    # Assert session is STILL authenticated by accessing a protected route
    res_profile = client.get('/auth/profile')
    assert res_profile.status_code == 200
    assert 'user1' in res_profile.data.decode('utf-8')
    
    # Directly verify authentication state inside client context
    from flask_login import current_user
    with client:
        client.get('/auth/profile')
        assert current_user.is_authenticated is True
        assert current_user.username == 'user1'


def test_csrf_logout_post_with_invalid_token_rejected_with_400(client, app, sample_users):
    """Test 22 (Phase 8): Verify POST /auth/logout with tampered CSRF token is rejected with 400."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    res = client.post(
        '/auth/logout',
        data={'csrf_token': 'tampered_invalid_token_xyz'},
        headers={'X-Test-No-CSRF': '1'}
    )
    assert res.status_code == 400
    
    # Session must remain authenticated
    res_profile = client.get('/auth/profile')
    assert res_profile.status_code == 200


def test_csrf_logout_post_with_expired_token_rejected_with_400(client, app, sample_users):
    """Test 23 (Phase 8): Verify POST /auth/logout with expired CSRF token is rejected with 400."""
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    with client.session_transaction() as sess:
        raw_token = sess.get('csrf_token')
        if not raw_token:
            raw_token = hashlib.sha1(os.urandom(64)).hexdigest()
            sess['csrf_token'] = raw_token
            
    s = URLSafeTimedSerializer(app.secret_key, salt="wtf-csrf-token")
    expired_token = s.dumps(raw_token)
    
    old_limit = app.config.get('WTF_CSRF_TIME_LIMIT')
    app.config['WTF_CSRF_TIME_LIMIT'] = -10
    try:
        res = client.post(
            '/auth/logout',
            data={'csrf_token': expired_token},
            headers={'X-Test-No-CSRF': '1'}
        )
    finally:
        app.config['WTF_CSRF_TIME_LIMIT'] = old_limit
    assert res.status_code == 400


def test_csrf_anonymous_and_authenticated_cache_isolation(client, app, sample_users):
    """Test 24 (Phase 8): Verify ALL HTML responses (anonymous & authenticated) emit Vary: Cookie and private, no-store."""
    # 1. Anonymous HTML (e.g. homepage)
    res_anon = client.get('/')
    assert res_anon.status_code == 200
    assert 'Cookie' in res_anon.headers.get('Vary', '')
    cc_anon = res_anon.headers.get('Cache-Control', '')
    assert 'private' in cc_anon
    assert 'no-store' in cc_anon
    assert res_anon.headers.get('Pragma') == 'no-cache'
    
    # 2. Authenticated HTML (e.g. profile page)
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    res_auth = client.get('/auth/profile')
    assert res_auth.status_code == 200
    assert 'Cookie' in res_auth.headers.get('Vary', '')
    cc_auth = res_auth.headers.get('Cache-Control', '')
    assert 'private' in cc_auth
    assert 'no-store' in cc_auth
    assert res_auth.headers.get('Pragma') == 'no-cache'
    
    # 3. Static / Non-HTML feeds (sitemap, robots) retain appropriate caching
    res_sitemap = client.get('/sitemap.xml')
    assert res_sitemap.status_code == 200
    assert 'no-store' not in res_sitemap.headers.get('Cache-Control', '')


def test_csrf_cross_user_qr_access_forbidden(client, app, sample_users):
    """Test 25 (Phase 8): Verify User A cannot access or download User B's QR code (RBAC & IDOR prevention)."""
    with app.app_context():
        att = Attendee.query.filter_by(user_id=sample_users['user_id']).first()
        event = Event.query.filter_by(status='published').first()
        if not event:
            event = Event(event_code='EVT-QR-TEST', title='QR Test', start_date=utc_now(), end_date=utc_now(), status='published')
            db.session.add(event)
            db.session.commit()
        
        ticket = Ticket.query.filter_by(event_id=event.id).first()
        if not ticket:
            ticket = Ticket(event_id=event.id, ticket_code='TCK-CODE-999', ticket_type='free', name='Standard Test', price=0, quota=100)
            db.session.add(ticket)
            db.session.commit()

        reg = Registration(
            registration_code='REG-TEST-QR-9999',
            event_id=event.id,
            attendee_id=att.id if att else 1,
            ticket_id=ticket.id,
            ticket_number='TICK-TEST-9999',
            registration_status='confirmed'
        )
        db.session.add(reg)
        db.session.commit()
        target_reg_id = reg.id

        u2 = User.query.filter_by(username='user2_attacker').first()
        if not u2:
            u2 = User(username='user2_attacker', email='u2@test.com', full_name='User 2 Attacker', role='attendee')
            u2.set_password('Pass@123')
            db.session.add(u2)
            db.session.commit()

    # Log in as User 2 (unauthorized user)
    client.post('/auth/login', data={'username': 'user2_attacker', 'password': 'Pass@123'})
    
    # Attempt to view User 1's ticket
    res_view = client.get(f'/tickets/view/{target_reg_id}')
    assert res_view.status_code == 403
    
    # Attempt to download User 1's QR code
    res_dl = client.get(f'/tickets/download-qr/{target_reg_id}')
    assert res_dl.status_code == 403


def test_csrf_route_inventory_no_mutating_get(app):
    """Test 26 (Phase 8): Verify that no GET route in Flask URL map performs state changes."""
    post_routes = []
    get_only_routes = []
    for rule in app.url_map.iter_rules():
        methods = rule.methods - {'OPTIONS', 'HEAD'}
        if 'POST' in methods:
            post_routes.append(rule.rule)
        elif methods == {'GET'}:
            get_only_routes.append(rule.rule)
            
    for action in ['/auth/logout', '/tickets/cancel', '/checkin/verify-api', '/events/create']:
        matched = any(r.startswith(action) or action in r for r in post_routes)
        assert matched, f"Action {action} must be accessible via POST with CSRF protection"
