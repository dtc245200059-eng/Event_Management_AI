"""
Main Blueprint (Home, Event listing, Search, Filter, Event Details).
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.models import Event, Speaker, Venue, Ticket, Schedule

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # All upcoming published events
    all_events = Event.query.filter_by(status='published').order_by(Event.start_date.asc()).all()
    categories = ['Tất cả', 'Trí tuệ nhân tạo', 'Cloud & DevOps', 'Khoa học dữ liệu', 'Startup & Đầu tư', 'Workshop', 'Kỹ thuật phần mềm', 'Âm nhạc & Nghệ thuật']
    
    # Stats
    total_events = len(all_events)
    total_speakers = Speaker.query.count()
    total_venues = Venue.query.count()

    return render_template(
        'main/index.html',
        featured_events=all_events,
        categories=categories,
        total_events=total_events,
        total_speakers=total_speakers,
        total_venues=total_venues
    )

@main_bp.route('/events')
def event_list():
    query = Event.query.filter(Event.status.in_(['published', 'ongoing']))
    
    # Search keyword
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(
            (Event.title.ilike(f'%{q}%')) |
            (Event.description.ilike(f'%{q}%')) |
            (Event.tags.ilike(f'%{q}%'))
        )

    # Category filter
    category = request.args.get('category', '').strip()
    if category and category != 'Tất cả':
        query = query.filter_by(category=category)

    # Location type filter (online, offline, hybrid)
    location_type = request.args.get('location_type', '').strip()
    if location_type:
        query = query.filter_by(location_type=location_type)

    all_matched = query.order_by(Event.start_date.asc()).all()
    total_matched = len(all_matched)

    # Pagination: 6 events per page
    page = request.args.get('page', 1, type=int)
    per_page = 6
    total_pages = max(1, (total_matched + per_page - 1) // per_page)
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_events = all_matched[start_idx:end_idx]

    categories = ['Tất cả', 'Trí tuệ nhân tạo', 'Cloud & DevOps', 'Khoa học dữ liệu', 'Startup & Đầu tư', 'Workshop', 'Kỹ thuật phần mềm', 'Âm nhạc & Nghệ thuật']

    return render_template(
        'main/events.html',
        events=paginated_events,
        categories=categories,
        selected_category=category,
        selected_location=location_type,
        q=q,
        current_page=page,
        total_pages=total_pages,
        total_events=total_matched
    )

@main_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    schedules = event.schedules.order_by(Schedule.start_at.asc()).all()
    tickets = event.tickets.filter_by(status='active').all()
    
    # Check if current user is registered
    is_registered = False
    user_registration = None
    if current_user.is_authenticated and current_user.attendee_profile:
        user_registration = event.registrations.filter_by(
            attendee_id=current_user.attendee_profile.id,
            registration_status='confirmed'
        ).first()
        if user_registration:
            is_registered = True

    return render_template(
        'main/event_detail.html',
        event=event,
        schedules=schedules,
        tickets=tickets,
        is_registered=is_registered,
        user_registration=user_registration
    )
