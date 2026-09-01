"""
Unit Tests for Authentication and RBAC.
"""
from app.extensions import db
from app.models.user import User

def test_user_password_hashing(app):
    user = User(username='testhash', email='hash@test.com', full_name='Hash User')
    user.set_password('Secret@123')
    assert user.check_password('Secret@123') is True
    assert user.check_password('WrongPassword') is False
    assert user.password_hash != 'Secret@123'

def test_user_roles(app, sample_users):
    with app.app_context():
        admin = User.query.get(sample_users['admin_id'])
        staff = User.query.get(sample_users['staff_id'])
        attendee = User.query.get(sample_users['user_id'])

        assert admin.is_admin is True
        assert admin.is_staff is True
        assert staff.is_admin is False
        assert staff.is_staff is True
        assert attendee.is_attendee is True

def test_login_success(client, sample_users):
    res = client.post('/auth/login', data={
        'username': 'user1',
        'password': 'User@123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Ch\xc3\xa0o m\xe1\xbb\xabng tr\xe1\xbb\x9f l\xe1\xba\xa1i' in res.data or b'User One' in res.data

def test_login_failure_wrong_password(client, sample_users):
    res = client.post('/auth/login', data={
        'username': 'user1',
        'password': 'IncorrectPassword'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'kh\xc3\xb4ng ch\xc3\xadnh x\xc3\xa1c' in res.data or b'danger' in res.data

def test_admin_create_staff_user(client, app, sample_users):
    # Login as admin
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    
    # Create a new staff account
    res = client.post('/admin/users/create', data={
        'username': 'staff_new_01',
        'email': 'staff01@test.com',
        'full_name': 'Nguyen Staff Member',
        'password': 'StaffPassword@123',
        'role': 'staff',
        'phone': '0987654321',
        'organization': 'ICTU Check-in Team'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'staff_new_01' in res.data
    
    with app.app_context():
        created_user = User.query.filter_by(username='staff_new_01').first()
        assert created_user is not None
        assert created_user.role == 'staff'
        assert created_user.is_staff is True
        assert created_user.check_password('StaffPassword@123') is True

def test_admin_change_user_role(client, app, sample_users):
    # Login as admin
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    
    # Promote user1 (attendee) to staff
    res = client.post(f'/admin/users/{sample_users["user_id"]}/change-role', data={
        'role': 'staff'
    }, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        updated_user = db.session.get(User, sample_users['user_id'])
        assert updated_user.role == 'staff'
        assert updated_user.is_staff is True

def test_non_admin_cannot_manage_users(client, sample_users):
    # Login as normal attendee
    client.post('/auth/login', data={'username': 'user1', 'password': 'User@123'})
    
    # Try accessing admin users page
    res = client.get('/admin/users')
    assert res.status_code == 403

    # Try creating staff
    res_post = client.post('/admin/users/create', data={
        'username': 'hacked_staff',
        'email': 'hack@test.com',
        'full_name': 'Hacker',
        'password': 'Password123',
        'role': 'admin'
    })
    assert res_post.status_code == 403
