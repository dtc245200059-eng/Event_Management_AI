"""
Pytest configuration and test fixtures.
"""
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Event, Ticket, Attendee, Registration

@pytest.fixture
def app():
    app = create_app('testing')
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
