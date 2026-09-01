"""
Event Management Blueprint for Admin/Staff (Create, Edit, Delete, Schedules, Speakers, Venues).
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Event, Speaker, Venue, Schedule, Ticket

events_bp = Blueprint('events', __name__)

def staff_required(f):
    """Decorator to restrict routes to staff and admin only."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@events_bp.route('/manage')
@login_required
@staff_required
def manage():
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('events/manage.html', events=events)

@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
@staff_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Trí tuệ nhân tạo').strip()
        description = request.form.get('description', '').strip()
        banner_url = request.form.get('banner_url', '').strip()
        start_date_str = request.form.get('start_date', '')
        end_date_str = request.form.get('end_date', '')
        location_type = request.form.get('location_type', 'offline')
        location_address = request.form.get('location_address', '').strip()
        online_meeting_url = request.form.get('online_meeting_url', '').strip()
        max_attendees = int(request.form.get('max_attendees', 500))
        status = request.form.get('status', 'published')
        tags = request.form.get('tags', '').strip()

        if not title or not start_date_str or not end_date_str:
            flash('Vui lòng nhập tên sự kiện và thời gian bắt đầu / kết thúc.', 'danger')
            return render_template('events/form.html', event=None)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Định dạng thời gian không hợp lệ.', 'danger')
            return render_template('events/form.html', event=None)

        # Generate event code
        import uuid
        event_code = f"EVT-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

        event = Event(
            event_code=event_code,
            title=title,
            category=category,
            description=description,
            banner_url=banner_url or 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800',
            start_date=start_date,
            end_date=end_date,
            location_type=location_type,
            location_address=location_address,
            online_meeting_url=online_meeting_url,
            max_attendees=max_attendees,
            status=status,
            tags=tags,
            created_by=current_user.id
        )
        db.session.add(event)
        db.session.commit()

        # Create default free ticket
        ticket_code = f"TCK-{event.id:04d}-FREE"
        free_ticket = Ticket(
            event_id=event.id,
            ticket_code=ticket_code,
            ticket_type='free',
            name='Vé Tiêu Chuẩn Miễn Phí',
            price=0.0,
            quota=max_attendees,
            sold_count=0
        )
        db.session.add(free_ticket)
        db.session.commit()

        flash(f'Tạo sự kiện "{event.title}" thành công!', 'success')
        return redirect(url_for('events.manage'))

    return render_template('events/form.html', event=None)

@events_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def edit(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.title = request.form.get('title', '').strip()
        event.category = request.form.get('category', '').strip()
        event.description = request.form.get('description', '').strip()
        event.banner_url = request.form.get('banner_url', '').strip()
        start_date_str = request.form.get('start_date', '')
        end_date_str = request.form.get('end_date', '')
        event.location_type = request.form.get('location_type', 'offline')
        event.location_address = request.form.get('location_address', '').strip()
        event.online_meeting_url = request.form.get('online_meeting_url', '').strip()
        event.max_attendees = int(request.form.get('max_attendees', 500))
        event.status = request.form.get('status', 'published')
        event.tags = request.form.get('tags', '').strip()

        try:
            event.start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            event.end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Định dạng thời gian không hợp lệ.', 'danger')
            return render_template('events/form.html', event=event)

        db.session.commit()
        flash('Cập nhật sự kiện thành công!', 'success')
        return redirect(url_for('events.manage'))

    return render_template('events/form.html', event=event)

@events_bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@staff_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f'Đã xóa sự kiện "{title}".', 'info')
    return redirect(url_for('events.manage'))
