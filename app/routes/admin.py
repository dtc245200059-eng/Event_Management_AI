"""
Admin Dashboard Blueprint (Analytics, Charts, Registrations, Feedback Sentiment, Predictive Stats).
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models import Event, User, Registration, Ticket, Attendee, AIChatHistory

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Overall metrics
    total_events = Event.query.count()
    total_registrations = Registration.query.filter_by(registration_status='confirmed').count()
    total_revenue = db.session.query(func.sum(Registration.payment_amount)).filter_by(payment_status='paid').scalar() or 0.0
    total_checked_in = Registration.query.filter_by(checked_in=True).count()
    
    # Check-in rate
    checkin_rate = round((total_checked_in / total_registrations * 100), 1) if total_registrations > 0 else 0.0

    # Events summary list
    events = Event.query.order_by(Event.start_date.desc()).all()

    # Feedback and sentiment breakdown
    feedbacks = Registration.query.filter(Registration.feedback_rating.isnot(None)).order_by(Registration.feedback_submitted_at.desc()).limit(10).all()
    positive_count = Registration.query.filter_by(sentiment='positive').count()
    neutral_count = Registration.query.filter_by(sentiment='neutral').count()
    negative_count = Registration.query.filter_by(sentiment='negative').count()

    # Recent AI Interactions
    ai_logs = AIChatHistory.query.order_by(AIChatHistory.created_at.desc()).limit(8).all()

    # Pre-formatted chart data for clean JSON consumption
    top_events = events[:6]
    chart_data = {
        "event_titles": [f"{e.title[:20]}..." for e in top_events],
        "registered_data": [e.total_registered for e in top_events],
        "capacity_data": [e.max_attendees for e in top_events],
        "sentiment_data": [positive_count, neutral_count, negative_count]
    }

    return render_template(
        'admin/dashboard.html',
        total_events=total_events,
        total_registrations=total_registrations,
        total_revenue=total_revenue,
        total_checked_in=total_checked_in,
        checkin_rate=checkin_rate,
        events=events,
        feedbacks=feedbacks,
        positive_count=positive_count,
        neutral_count=neutral_count,
        negative_count=negative_count,
        ai_logs=ai_logs,
        chart_data=chart_data
    )

@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    total_users = len(users)
    total_admins = sum(1 for u in users if u.role == 'admin')
    total_staff = sum(1 for u in users if u.role == 'staff')
    total_attendees = sum(1 for u in users if u.role == 'attendee')

    return render_template(
        'admin/users.html',
        users=users,
        total_users=total_users,
        total_admins=total_admins,
        total_staff=total_staff,
        total_attendees=total_attendees
    )

@admin_bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', 'staff').strip().lower()
    phone = request.form.get('phone', '').strip()
    organization = request.form.get('organization', '').strip()

    if not username or not email or not full_name or not password:
        flash('Vui lòng điền đầy đủ tên đăng nhập, họ tên, email và mật khẩu khởi tạo!', 'danger')
        return redirect(url_for('admin.users_list'))

    if len(password) < 6:
        flash('Mật khẩu khởi tạo phải có tối thiểu 6 ký tự!', 'danger')
        return redirect(url_for('admin.users_list'))

    if role not in ['admin', 'staff', 'attendee']:
        flash('Vai trò (Role) không hợp lệ!', 'danger')
        return redirect(url_for('admin.users_list'))

    if User.query.filter_by(username=username).first():
        flash(f'Tên đăng nhập "@{username}" đã tồn tại trên hệ thống!', 'danger')
        return redirect(url_for('admin.users_list'))

    if User.query.filter_by(email=email).first():
        flash(f'Email "{email}" đã được đăng ký cho tài khoản khác!', 'danger')
        return redirect(url_for('admin.users_list'))

    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        phone=phone or None,
        is_active=True
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    code_prefix = 'STF' if role == 'staff' else ('ADM' if role == 'admin' else 'ATT')
    attendee_code = f"{code_prefix}-2026-{new_user.id:04d}"
    attendee = Attendee(
        attendee_code=attendee_code,
        user_id=new_user.id,
        full_name=full_name,
        email=email,
        phone=phone or None,
        organization=organization or ('Ban Tổ Chức / Staff' if role == 'staff' else ('Quản Trị Viên' if role == 'admin' else None))
    )
    db.session.add(attendee)
    db.session.commit()

    role_vn = 'Nhân viên (Staff)' if role == 'staff' else ('Quản trị viên (Admin)' if role == 'admin' else 'Khách mời (Attendee)')
    flash(f'Tạo thành công tài khoản {role_vn}: @{username} ({email})!', 'success')
    return redirect(url_for('admin.users_list'))

@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@login_required
@admin_required
def change_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Bạn không thể tự thay đổi vai trò của chính mình để tránh mất quyền quản trị!', 'warning')
        return redirect(url_for('admin.users_list'))

    new_role = request.form.get('role', '').strip().lower()
    if new_role not in ['admin', 'staff', 'attendee']:
        flash('Vai trò phân quyền không hợp lệ!', 'danger')
        return redirect(url_for('admin.users_list'))

    old_role = user.role
    user.role = new_role
    db.session.commit()

    role_names = {'admin': 'Quản Trị Viên (Admin)', 'staff': 'Nhân Viên (Staff)', 'attendee': 'Khách Mời (Attendee)'}
    flash(f'Đã phân quyền thành công tài khoản @{user.username}: chuyển từ {role_names.get(old_role, old_role)} sang {role_names.get(new_role, new_role)}.', 'success')
    return redirect(url_for('admin.users_list'))

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Bạn không thể tự khóa tài khoản của chính mình!', 'warning')
        return redirect(url_for('admin.users_list'))
    user.is_active = not user.is_active
    db.session.commit()
    status_text = 'kích hoạt' if user.is_active else 'khóa'
    flash(f'Đã {status_text} tài khoản {user.username}.', 'info')
    return redirect(url_for('admin.users_list'))
