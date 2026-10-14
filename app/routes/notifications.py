"""
Notifications Blueprint (Broadcast Announcements, AI Email Drafts, Attendee Inbox, and Delivery Analytics).
Implements Requirement 3.1.6 & 3.2.1 from de_tai_09.md.
"""
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.extensions import db, utc_now
from app.models import Notification, Event, Registration, Ticket

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

def organizer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_organizer:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def calculate_recipient_count(event_id, target_audience):
    """Tính toán số lượng người nhận thực tế dựa trên phân khúc đối tượng tham dự."""
    base_query = Registration.query.filter(
        Registration.event_id == event_id,
        Registration.registration_status != 'cancelled'
    )
    if target_audience == 'checked_in':
        return base_query.filter_by(checked_in=True).count()
    elif target_audience == 'not_checked_in':
        return base_query.filter_by(checked_in=False).count()
    elif target_audience == 'vip':
        return base_query.join(Ticket).filter(Ticket.ticket_type == 'vip').count()
    # Mặc định: all_registered
    return base_query.count()

@notifications_bp.route('/manage')
@login_required
@organizer_required
def manage():
    """Bảng điều khiển quản lý và thống kê thông báo đã gửi."""
    if current_user.is_admin:
        events = Event.query.order_by(Event.start_date.desc()).all()
        notifications = Notification.query.order_by(Notification.sent_at.desc()).all()
    else:
        events = Event.query.filter_by(created_by=current_user.id).order_by(Event.start_date.desc()).all()
        event_ids = [e.id for e in events]
        notifications = Notification.query.filter(Notification.event_id.in_(event_ids)).order_by(Notification.sent_at.desc()).all() if event_ids else []

    total_sent = len(notifications)
    total_recipients = sum(n.recipient_count for n in notifications)
    total_reminders = sum(1 for n in notifications if n.notification_type == 'reminder')
    total_invitations = sum(1 for n in notifications if n.notification_type == 'invitation')
    total_thank_yous = sum(1 for n in notifications if n.notification_type == 'thank_you')
    total_updates = sum(1 for n in notifications if n.notification_type == 'update')

    return render_template(
        'notifications/manage.html',
        events=events,
        notifications=notifications,
        total_sent=total_sent,
        total_recipients=total_recipients,
        total_reminders=total_reminders,
        total_invitations=total_invitations,
        total_thank_yous=total_thank_yous,
        total_updates=total_updates
    )

@notifications_bp.route('/create', methods=['GET', 'POST'])
@login_required
@organizer_required
def create():
    """Giao diện soạn thảo và gửi thông báo, tích hợp AI Assistant sinh bản thảo."""
    if current_user.is_admin:
        events = Event.query.filter(Event.status.in_(['published', 'ongoing', 'draft'])).order_by(Event.start_date.asc()).all()
    else:
        events = Event.query.filter(
            Event.created_by == current_user.id,
            Event.status.in_(['published', 'ongoing', 'draft'])
        ).order_by(Event.start_date.asc()).all()

    selected_event_id = request.args.get('event_id', type=int)

    if request.method == 'POST':
        event_id = request.form.get('event_id', type=int)
        notification_type = request.form.get('notification_type', 'reminder').strip()
        target_audience = request.form.get('target_audience', 'all_registered').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not event_id or not title or not content:
            flash('Vui lòng chọn sự kiện, nhập tiêu đề và nội dung thông báo.', 'danger')
            return render_template('notifications/create.html', events=events, selected_event_id=selected_event_id)

        event = db.get_or_404(Event, event_id)
        if not current_user.is_admin and event.created_by != current_user.id:
            abort(403)

        recipients = calculate_recipient_count(event_id, target_audience)

        notif = Notification(
            event_id=event_id,
            title=title,
            notification_type=notification_type,
            target_audience=target_audience,
            content=content,
            recipient_count=recipients,
            status='sent',
            sent_at=utc_now(),
            created_by=current_user.id
        )
        db.session.add(notif)
        db.session.commit()

        flash(f'Đã phát hành thông báo "{title}" thành công tới {recipients} người tham dự sự kiện {event.title}!', 'success')
        return redirect(url_for('notifications.manage'))

    return render_template(
        'notifications/create.html',
        events=events,
        selected_event_id=selected_event_id
    )

@notifications_bp.route('/inbox')
@login_required
def inbox():
    """Hộp thư thông báo và tin tức sự kiện dành cho người tham dự."""
    if not current_user.attendee_profile:
        notifications = []
    else:
        # Lấy danh sách event_id mà người dùng đã đăng ký tham gia
        regs = current_user.attendee_profile.registrations.filter(Registration.registration_status != 'cancelled').all()
        event_ids = [r.event_id for r in regs]
        if event_ids:
            notifications = Notification.query.filter(
                Notification.event_id.in_(event_ids),
                Notification.status == 'sent'
            ).order_by(Notification.sent_at.desc()).all()
        else:
            notifications = []

    return render_template('notifications/inbox.html', notifications=notifications)

@notifications_bp.route('/view/<int:notif_id>')
@login_required
def view_detail(notif_id):
    """Xem chi tiết nội dung thông báo / email đã gửi."""
    notif = db.get_or_404(Notification, notif_id)
    return render_template('notifications/view.html', notification=notif)

@notifications_bp.route('/api/recent', methods=['GET'])
@login_required
def api_recent():
    """API trả về danh sách thông báo mới nhất cho dropdown thông báo."""
    user_notifications = []
    if current_user.attendee_profile:
        regs = current_user.attendee_profile.registrations.filter(Registration.registration_status != 'cancelled').all()
        event_ids = [r.event_id for r in regs]
        if event_ids:
            user_notifications = Notification.query.filter(
                Notification.event_id.in_(event_ids),
                Notification.status == 'sent'
            ).order_by(Notification.sent_at.desc()).limit(5).all()
    elif current_user.is_admin or current_user.is_organizer:
        user_notifications = Notification.query.filter_by(status='sent').order_by(Notification.sent_at.desc()).limit(5).all()

    items = []
    for n in user_notifications:
        items.append({
            'id': n.id,
            'title': n.title,
            'event_title': n.event.title if n.event else '',
            'type': n.notification_type,
            'sent_at': n.sent_at.strftime('%H:%M • %d/%m/%Y'),
            'url': url_for('notifications.view_detail', notif_id=n.id)
        })
    return jsonify({'success': True, 'unread_count': len(items), 'notifications': items})

