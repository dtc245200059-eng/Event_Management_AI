"""
Pytest configuration and test fixtures.
"""
import os
import hashlib
import pytest
from itsdangerous import URLSafeTimedSerializer
from flask.testing import FlaskClient
from app import create_app
from app.extensions import db
from app.models import User, Event, Ticket, Attendee, Registration

class CsrfAwareClient(FlaskClient):
    """
    Standard test client that simulates real browser behavior with CSRF protection enabled.
    In modern browsers, main.js automatically attaches the active session X-CSRFToken header
    to same-origin state-changing requests (POST, PUT, DELETE, PATCH).
    Tests can explicitly bypass auto-injection by passing headers={'X-Test-No-CSRF': '1'}
    to verify that missing CSRF tokens are rejected with HTTP 400.
    """
    def open(self, *args, **kwargs):
        method = (kwargs.get('method') or 'GET').upper()
        if method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            headers = kwargs.get('headers')
            if headers is None:
                headers = {}
            elif isinstance(headers, list):
                headers = dict(headers)
            elif not isinstance(headers, dict):
                headers = dict(headers)
                
            if headers.get('X-Test-No-CSRF') == '1':
                del headers['X-Test-No-CSRF']
            elif 'X-CSRFToken' not in headers and not (isinstance(kwargs.get('data'), dict) and 'csrf_token' in kwargs['data']):
                with self.session_transaction() as sess:
                    raw_token = sess.get('csrf_token')
                    if not raw_token:
                        raw_token = hashlib.sha1(os.urandom(64)).hexdigest()
                        sess['csrf_token'] = raw_token
                s = URLSafeTimedSerializer(self.application.secret_key, salt="wtf-csrf-token")
                headers['X-CSRFToken'] = s.dumps(raw_token)
            kwargs['headers'] = headers
        return super().open(*args, **kwargs)

@pytest.fixture
def app():
    app = create_app('testing')
    app.test_client_class = CsrfAwareClient
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_users(app):
    with app.app_context():
        admin = User(username='admin', email='admin@test.com', full_name='Admin Test', role='admin')
        admin.set_password('Admin@123')

        staff = User(username='staff', email='staff@test.com', full_name='Staff Test', role='staff')
        staff.set_password('Staff@123')

        attendee_user = User(username='user1', email='user1@test.com', full_name='User One', role='attendee')
        attendee_user.set_password('User@123')

        db.session.add_all([admin, staff, attendee_user])
        db.session.commit()

        att_profile = Attendee(
            attendee_code='ATT-TEST-001',
            user_id=attendee_user.id,
            full_name=attendee_user.full_name,
            email=attendee_user.email,
            interests='Trí tuệ nhân tạo, Python'
        )
        db.session.add(att_profile)
        db.session.commit()

        return {
            'admin_id': admin.id,
            'staff_id': staff.id,
            'user_id': attendee_user.id,
            'attendee_profile_id': att_profile.id
        }
