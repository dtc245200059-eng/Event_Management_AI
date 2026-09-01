"""
Authentication Blueprint (Login, Register, Logout, Profile).
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.attendee import Attendee

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Tài khoản của bạn đã bị khóa. Vui lòng liên hệ Admin.', 'danger')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            flash(f'Chào mừng trở lại, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không chính xác.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        organization = request.form.get('organization', '').strip()
        interests = request.form.get('interests', '').strip()

        # Basic validations
        if not username or not email or not password or not full_name:
            flash('Vui lòng điền đầy đủ các thông tin bắt buộc.', 'warning')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email này đã được đăng ký tài khoản.', 'danger')
            return render_template('auth/register.html')

        # Create User & Attendee profile
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role='attendee'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()  # get new_user.id

        attendee_code = f"ATT-2026-{new_user.id:04d}"
        new_attendee = Attendee(
            attendee_code=attendee_code,
            user_id=new_user.id,
            full_name=full_name,
            email=email,
            phone=phone,
            organization=organization,
            interests=interests
        )
        db.session.add(new_attendee)
        db.session.commit()

        flash('Đăng ký tài khoản thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất an toàn.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    registrations = []
    if current_user.attendee_profile:
        registrations = current_user.attendee_profile.registrations.order_by(
            db.desc('created_at')
        ).all()
    return render_template('auth/profile.html', user=current_user, registrations=registrations)

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Cập nhật thông tin hồ sơ cá nhân và sở thích AI."""
    full_name = request.form.get('full_name', '').strip()
    phone = request.form.get('phone', '').strip()
    organization = request.form.get('organization', '').strip()
    job_title = request.form.get('job_title', '').strip()
    interests = request.form.get('interests', '').strip()
    avatar_url = request.form.get('avatar_url', '').strip()

    if not full_name:
        flash('Họ và tên không được để trống.', 'warning')
        return redirect(url_for('auth.profile', tab='edit'))

    # Update User model
    current_user.full_name = full_name
    current_user.phone = phone
    if avatar_url:
        current_user.avatar_url = avatar_url

    # Update or Create Attendee profile
    if current_user.attendee_profile:
        current_user.attendee_profile.full_name = full_name
        current_user.attendee_profile.phone = phone
        current_user.attendee_profile.organization = organization
        current_user.attendee_profile.job_title = job_title
        current_user.attendee_profile.interests = interests
    else:
        attendee_code = f"ATT-2026-{current_user.id:04d}"
        new_attendee = Attendee(
            attendee_code=attendee_code,
            user_id=current_user.id,
            full_name=full_name,
            email=current_user.email,
            phone=phone,
            organization=organization,
            job_title=job_title,
            interests=interests
        )
        db.session.add(new_attendee)

    db.session.commit()
    flash('Cập nhật hồ sơ cá nhân thành công!', 'success')
    return redirect(url_for('auth.profile', tab='edit'))

@auth_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Đổi mật khẩu tài khoản bảo mật."""
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_user.check_password(current_password):
        flash('Mật khẩu hiện tại không chính xác.', 'danger')
        return redirect(url_for('auth.profile', tab='security'))

    if len(new_password) < 6:
        flash('Mật khẩu mới phải có độ dài tối thiểu 6 ký tự.', 'warning')
        return redirect(url_for('auth.profile', tab='security'))

    if new_password != confirm_password:
        flash('Mật khẩu xác nhận không khớp.', 'danger')
        return redirect(url_for('auth.profile', tab='security'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Đổi mật khẩu tài khoản thành công!', 'success')
    return redirect(url_for('auth.profile', tab='security'))
