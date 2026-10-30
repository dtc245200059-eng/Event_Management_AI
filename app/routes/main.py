"""
Main Blueprint (Home, Event listing, Search, Filter, Event Details).
"""
from flask import Blueprint, render_template, request, jsonify, abort, Response
from flask_login import current_user
from app.extensions import db
from app.models import Event, Speaker, Venue, Ticket, Schedule

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # All upcoming published events
    all_events = Event.query.filter_by(status='published').order_by(Event.start_date.asc()).all()
    
    # Dynamic distinct categories
    db_cats = [c[0] for c in Event.query.with_entities(Event.category).distinct().all() if c[0]]
    categories = ['Tất cả'] + sorted(list(set(db_cats)))
    
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

    # Dynamic distinct categories
    db_cats = [c[0] for c in Event.query.with_entities(Event.category).distinct().all() if c[0]]
    categories = ['Tất cả'] + sorted(list(set(db_cats)))

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
    event = db.get_or_404(Event, event_id)
    
    # Enforce publication policy & preview permissions
    is_draft_preview = False
    if event.status == 'draft':
        # Only event creator or system administrator can preview draft events
        if current_user.is_authenticated and (current_user.is_admin or event.created_by == current_user.id):
            is_draft_preview = True
        else:
            abort(404)

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
        user_registration=user_registration,
        is_draft_preview=is_draft_preview
    )

@main_bp.route('/sitemap.xml')
def sitemap():
    """
    Dynamic XML Sitemap endpoint.
    Returns valid XML containing publicly indexable URLs:
    - Homepage
    - Events listing
    - Public published, ongoing, and completed events (excluding draft and cancelled)
    """
    from app.seo_helpers import (
        get_trusted_canonical_origin,
        build_sitemap_xml,
        INDEXABLE_EVENT_STATUSES,
        MAX_SITEMAP_URLS
    )
    try:
        origin = get_trusted_canonical_origin()
    except Exception:
        abort(500)

    # Query only needed fields for indexable events, ordered deterministically.
    # Cap event query at (MAX_SITEMAP_URLS - 2) so that total URLs (including homepage and /events)
    # never exceeds the strict 50,000 protocol boundary.
    max_event_entries = max(0, MAX_SITEMAP_URLS - 2)
    event_records = db.session.query(Event.id, Event.updated_at).filter(
        Event.status.in_(INDEXABLE_EVENT_STATUSES)
    ).order_by(Event.id.asc()).limit(max_event_entries).all()

    xml_content = build_sitemap_xml(base_origin=origin, event_records=event_records)

    response = Response(xml_content, mimetype='application/xml')
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@main_bp.route('/robots.txt')
def robots():
    """
    Robots.txt endpoint.
    Returns plain text crawling directives and Sitemap reference.
    """
    from app.seo_helpers import (
        get_trusted_canonical_origin,
        build_robots_txt
    )
    try:
        origin = get_trusted_canonical_origin()
    except Exception:
        origin = 'http://localhost:5000'

    robots_content = build_robots_txt(base_origin=origin)

    response = Response(robots_content, mimetype='text/plain')
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

@main_bp.route('/health')
def health_check():
    """Endpoint kiểm tra sức khỏe hệ thống (Health Check Probe) cho Docker/K8s/PaaS."""
    from datetime import datetime, timezone
    from sqlalchemy import text
    try:
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
        http_code = 200
        overall_status = 'healthy'
    except Exception as e:
        db_status = f'error: {str(e)}'
        http_code = 503
        overall_status = 'unhealthy'

    return jsonify({
        'status': overall_status,
        'app': 'EventAI Pro',
        'version': '1.0.0',
        'database': db_status,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), http_code
