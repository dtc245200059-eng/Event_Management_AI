"""
Event Management Blueprint for Admin/Organizer (CRUD Events, Schedules, Speakers, Venues, Tickets).
Implements Requirements 3.1.1, 3.1.2, 3.1.3 & 3.1.4 from de_tai_09.md.
"""
from functools import wraps
from datetime import datetime
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db, utc_now
from app.models import Event, Speaker, Venue, Schedule, Ticket

events_bp = Blueprint('events', __name__)

def organizer_required(f):
    """Decorator to restrict routes to organizer and admin only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_organizer:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@events_bp.route('/manage')
@login_required
@organizer_required
def manage():
    if current_user.is_admin:
        events = Event.query.order_by(Event.created_at.desc()).all()
    else:
        events = Event.query.filter_by(created_by=current_user.id).order_by(Event.created_at.desc()).all()
    return render_template('events/manage.html', events=events)

@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
@organizer_required
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
        event_code = f"EVT-{utc_now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

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
@organizer_required
def edit(event_id):
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

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
@organizer_required
def delete(event_id):
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)
    title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f'Đã xóa sự kiện "{title}".', 'info')
    return redirect(url_for('events.manage'))

# ==========================================
# QUẢN LÝ LỊCH TRÌNH (SCHEDULES / SESSIONS)
# ==========================================
@events_bp.route('/<int:event_id>/schedules', methods=['GET'])
@login_required
@organizer_required
def schedules(event_id):
    """Giao diện xem và quản lý các phiên thảo luận của sự kiện."""
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    event_schedules = event.schedules.order_by(Schedule.start_at.asc()).all()
    speakers = Speaker.query.order_by(Speaker.name.asc()).all()
    venues = Venue.query.order_by(Venue.name.asc()).all()

    return render_template(
        'events/schedules.html',
        event=event,
        schedules=event_schedules,
        speakers=speakers,
        venues=venues
    )

@events_bp.route('/<int:event_id>/schedules/create', methods=['POST'])
@login_required
@organizer_required
def create_schedule(event_id):
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    title = request.form.get('title', '').strip()
    speaker_id = request.form.get('speaker_id', type=int)
    venue_id = request.form.get('venue_id', type=int)
    start_at_str = request.form.get('start_at', '')
    end_at_str = request.form.get('end_at', '')
    description = request.form.get('description', '').strip()

    if not title or not start_at_str or not end_at_str:
        flash('Vui lòng nhập tên phiên và thời gian bắt đầu / kết thúc.', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    try:
        start_at = datetime.strptime(start_at_str, '%Y-%m-%dT%H:%M')
        end_at = datetime.strptime(end_at_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Định dạng thời gian phiên không hợp lệ.', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    if start_at >= end_at:
        flash('Thời gian bắt đầu phiên phải trước thời gian kết thúc!', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    schedule_item = Schedule(
        event_id=event.id,
        speaker_id=speaker_id if speaker_id else None,
        venue_id=venue_id if venue_id else None,
        title=title,
        description=description,
        start_at=start_at,
        end_at=end_at
    )
    db.session.add(schedule_item)
    db.session.commit()

    flash(f'Đã thêm phiên thảo luận "{title}" vào lịch trình!', 'success')
    return redirect(url_for('events.schedules', event_id=event.id))

@events_bp.route('/schedules/<int:schedule_id>/edit', methods=['POST'])
@login_required
@organizer_required
def edit_schedule(schedule_id):
    item = db.get_or_404(Schedule, schedule_id)
    event = item.event
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    title = request.form.get('title', '').strip()
    speaker_id = request.form.get('speaker_id', type=int)
    venue_id = request.form.get('venue_id', type=int)
    start_at_str = request.form.get('start_at', '')
    end_at_str = request.form.get('end_at', '')
    description = request.form.get('description', '').strip()

    if not title or not start_at_str or not end_at_str:
        flash('Vui lòng nhập tên phiên và thời gian bắt đầu / kết thúc.', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    try:
        start_at = datetime.strptime(start_at_str, '%Y-%m-%dT%H:%M')
        end_at = datetime.strptime(end_at_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Định dạng thời gian phiên không hợp lệ.', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    if start_at >= end_at:
        flash('Thời gian bắt đầu phiên phải trước thời gian kết thúc!', 'danger')
        return redirect(url_for('events.schedules', event_id=event.id))

    item.title = title
    item.speaker_id = speaker_id if speaker_id else None
    item.venue_id = venue_id if venue_id else None
    item.start_at = start_at
    item.end_at = end_at
    item.description = description
    db.session.commit()

    flash(f'Đã cập nhật phiên thảo luận "{title}" thành công!', 'success')
    return redirect(url_for('events.schedules', event_id=event.id))

@events_bp.route('/schedules/<int:schedule_id>/delete', methods=['POST'])
@login_required
@organizer_required
def delete_schedule(schedule_id):
    item = db.get_or_404(Schedule, schedule_id)
    event_id = item.event_id
    event = item.event
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    db.session.delete(item)
    db.session.commit()
    flash('Đã xóa phiên thảo luận khỏi lịch trình.', 'info')
    return redirect(url_for('events.schedules', event_id=event_id))


# ==========================================
# QUẢN LÝ DIỄN GIẢ (SPEAKERS)
# ==========================================
@events_bp.route('/speakers', methods=['GET'])
@login_required
@organizer_required
def speakers_list():
    speakers = Speaker.query.order_by(Speaker.name.asc()).all()
    return render_template('events/speakers.html', speakers=speakers)

@events_bp.route('/speakers/create', methods=['POST'])
@login_required
@organizer_required
def create_speaker():
    name = request.form.get('name', '').strip()
    title = request.form.get('title', '').strip()
    organization = request.form.get('organization', '').strip()
    bio = request.form.get('bio', '').strip()
    avatar_url = request.form.get('avatar_url', '').strip()
    email = request.form.get('email', '').strip().lower()
    phone = request.form.get('phone', '').strip()
    linkedin_url = request.form.get('linkedin_url', '').strip()

    if not name:
        flash('Vui lòng nhập họ và tên diễn giả.', 'danger')
        return redirect(url_for('events.speakers_list'))

    speaker = Speaker(
        name=name,
        title=title or 'Chuyên gia khách mời',
        organization=organization or 'Tổ chức đối tác',
        bio=bio or 'Chuyên gia giàu kinh nghiệm trong lĩnh vực công nghệ và sự kiện.',
        avatar_url=avatar_url or 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150',
        email=email or None,
        phone=phone or None,
        linkedin_url=linkedin_url or None
    )
    db.session.add(speaker)
    db.session.commit()

    flash(f'Đã thêm diễn giả "{name}" thành công!', 'success')
    return redirect(url_for('events.speakers_list'))

@events_bp.route('/speakers/<int:speaker_id>/delete', methods=['POST'])
@login_required
@organizer_required
def delete_speaker(speaker_id):
    if not current_user.is_admin:
        abort(403)
    speaker = db.get_or_404(Speaker, speaker_id)
    name = speaker.name
    db.session.delete(speaker)
    db.session.commit()
    flash(f'Đã xóa diễn giả "{name}".', 'info')
    return redirect(url_for('events.speakers_list'))

# ==========================================
# QUẢN LÝ CÁC HẠNG VÉ (TICKET TIERS)
# ==========================================
@events_bp.route('/<int:event_id>/tickets', methods=['GET'])
@login_required
@organizer_required
def manage_tickets(event_id):
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)
    tickets = event.tickets.all()
    return render_template('events/tickets.html', event=event, tickets=tickets)

@events_bp.route('/<int:event_id>/tickets/create', methods=['POST'])
@login_required
@organizer_required
def create_ticket(event_id):
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    name = request.form.get('name', '').strip()
    ticket_type = request.form.get('ticket_type', 'standard').strip()
    price = float(request.form.get('price', 0.0))
    quota = int(request.form.get('quota', 100))

    if not name or quota <= 0:
        flash('Vui lòng nhập tên vé và số lượng quota hợp lệ.', 'danger')
        return redirect(url_for('events.manage_tickets', event_id=event.id))

    ticket_code = f"TCK-{event.id:04d}-{ticket_type.upper()}-{uuid.uuid4().hex[:4].upper()}"

    ticket = Ticket(
        event_id=event.id,
        ticket_code=ticket_code,
        ticket_type=ticket_type,
        name=name,
        price=price,
        quota=quota,
        sold_count=0,
        status='active'
    )
    db.session.add(ticket)
    db.session.commit()

    flash(f'Đã thêm hạng vé "{name}" với {quota} suất phát hành!', 'success')
    return redirect(url_for('events.manage_tickets', event_id=event.id))

# ==========================================
# QUẢN LÝ VÀ TỔNG HỢP Ý KIẾN PHẢN HỒI (FEEDBACK REVIEW & AGGREGATION)
# ==========================================
@events_bp.route('/<int:event_id>/feedback', methods=['GET'])
@login_required
@organizer_required
def event_feedback(event_id):
    """
    Authorized Feedback Review & Aggregation for Event Organizers and Admins.
    Displays rating distribution, sentiment breakdown, individual comments and AI opinion summary.
    """
    event = db.get_or_404(Event, event_id)
    if not current_user.is_admin and event.created_by != current_user.id:
        abort(403)

    from app.models import Registration
    from app.services.sentiment_service import summarize_event_feedback_groups

    feedbacks = Registration.query.filter(
        Registration.event_id == event.id,
        Registration.feedback_rating.isnot(None)
    ).order_by(Registration.feedback_submitted_at.desc()).all()

    total_feedbacks = len(feedbacks)
    avg_rating = round(sum(f.feedback_rating for f in feedbacks) / total_feedbacks, 1) if total_feedbacks > 0 else 0.0

    star_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for f in feedbacks:
        if f.feedback_rating in star_counts:
            star_counts[f.feedback_rating] += 1
        sent = f.sentiment or 'neutral'
        if sent in sentiment_counts:
            sentiment_counts[sent] += 1

    ai_summary = summarize_event_feedback_groups(event.id) if total_feedbacks > 0 else None

    return render_template(
        'events/feedback_list.html',
        event=event,
        feedbacks=feedbacks,
        total_feedbacks=total_feedbacks,
        avg_rating=avg_rating,
        star_counts=star_counts,
        sentiment_counts=sentiment_counts,
        ai_summary=ai_summary
    )

