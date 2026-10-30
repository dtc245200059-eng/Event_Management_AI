"""
SEO Helper utilities for EventAI Pro.
Provides text sanitization, dynamic canonical URL generation, Open Graph formatting,
and Schema.org JSON-LD Structured Data builders (Event and BreadcrumbList).
"""
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse, urlencode
from xml.sax.saxutils import escape as xml_escape
from flask import request, current_app
import sqlite3
from sqlalchemy.exc import OperationalError as SAOperationalError, InterfaceError as SAInterfaceError

DEFAULT_META_DESCRIPTION = (
    "Nền tảng Quản trị & Trải nghiệm Sự kiện Thông minh tích hợp Trí tuệ Nhân tạo EventAI Pro. "
    "Khám phá hội thảo công nghệ, diễn đàn khoa học, đăng ký vé QR Code tức thì và trợ lý AI thông minh."
)

DEFAULT_OG_IMAGE_URL = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop"

def clean_meta_description(text, fallback="", max_len=160):
    """
    Sanitize text for use in meta descriptions.
    Strips HTML tags, collapses whitespaces, falls back if empty,
    and truncates cleanly at word boundaries if exceeding max_len.
    """
    raw = text if (text and str(text).strip()) else fallback
    raw_str = str(raw).strip() if raw else ""
    
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', raw_str)
    # Collapse multiple whitespaces and newlines
    clean = ' '.join(clean.split())
    
    if not clean:
        clean = DEFAULT_META_DESCRIPTION
        
    if len(clean) > max_len:
        truncated = clean[:max_len - 3]
        if ' ' in truncated:
            truncated = truncated.rsplit(' ', 1)[0]
        clean = truncated.strip() + '...'
        
    return clean

def build_canonical_url(path=None, keep_params=None):
    """
    Construct a clean, absolute canonical URL.
    - Honors CANONICAL_DOMAIN if set, otherwise falls back to request.url_root.
    - Strips query parameters by default (e.g., utm_source, fbclid, ref).
    - Preserves whitelisted query parameters (e.g., page) if keep_params is specified.
    - Normalizes trailing slashes (keeps root '/', strips trailing slash on sub-paths).
    """
    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip().rstrip('/')
    except Exception:
        canonical_domain = ''
        
    base_origin = canonical_domain if canonical_domain else (request.url_root.rstrip('/') if request else 'https://eventai.pro')

    target_path = path if path else (request.path if request else '/')
    if not target_path.startswith('/'):
        target_path = '/' + target_path

    # Normalize trailing slashes: root '/' remains '/', others stripped
    if len(target_path) > 1 and target_path.endswith('/'):
        target_path = target_path.rstrip('/')

    query_string = ''
    if keep_params and request and request.args:
        filtered_query = []
        for param in keep_params:
            if param in request.args:
                for val in request.args.getlist(param):
                    filtered_query.append((param, val))
        if filtered_query:
            query_string = '?' + urlencode(filtered_query)

    return f"{base_origin}{target_path}{query_string}"

def format_og_image(image_url=None):
    """
    Format Open Graph / Twitter image URL to an absolute URL.
    - If already absolute (http:// or https://), returns as is.
    - If relative path, prepends canonical domain or request.url_root.
    - If empty/None, falls back to default high-res hero banner image.
    """
    img = str(image_url).strip() if image_url else ''
    if not img:
        return DEFAULT_OG_IMAGE_URL
    if img.startswith('http://') or img.startswith('https://'):
        return img
        
    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip().rstrip('/')
    except Exception:
        canonical_domain = ''
        
    base_origin = canonical_domain if canonical_domain else (request.url_root.rstrip('/') if request else 'https://eventai.pro')
    if not img.startswith('/'):
        img = '/' + img
    return f"{base_origin}{img}"

def format_iso8601_date(dt, offset="+07:00"):
    """
    Format a datetime object into a clean ISO 8601 string.
    - If dt is timezone-aware, uses its own timezone offset.
    - If dt is naive, applies the specified explicit offset (default +07:00 for Vietnam/Indochina).
    - If dt is None or invalid, returns None.
    """
    if not dt or not isinstance(dt, datetime):
        return None
    
    if dt.tzinfo is not None:
        return dt.isoformat()
    
    # Naive datetime: format as YYYY-MM-DDTHH:MM:SS+HH:MM
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
    clean_offset = offset.strip() if offset else ''
    if clean_offset and not (clean_offset.startswith('+') or clean_offset.startswith('-')):
        clean_offset = '+' + clean_offset
    return f"{dt_str}{clean_offset}"

def get_schema_event_status(status):
    """
    Map internal Event.status values to standard Schema.org EventStatusType URLs.
    """
    mapping = {
        'published': 'https://schema.org/EventScheduled',
        'ongoing': 'https://schema.org/EventScheduled',
        'completed': 'https://schema.org/EventScheduled',
        'cancelled': 'https://schema.org/EventCancelled',
        'postponed': 'https://schema.org/EventPostponed',
        'rescheduled': 'https://schema.org/EventRescheduled',
    }
    return mapping.get(str(status).lower(), 'https://schema.org/EventScheduled')

def get_schema_attendance_mode(location_type):
    """
    Map internal Event.location_type to Schema.org EventAttendanceModeEnumeration URLs.
    """
    loc_type = str(location_type).lower() if location_type else 'offline'
    if loc_type == 'online':
        return 'https://schema.org/OnlineEventAttendanceMode'
    elif loc_type == 'hybrid':
        return 'https://schema.org/MixedEventAttendanceMode'
    return 'https://schema.org/OfflineEventAttendanceMode'

def build_event_location(event, public_event_url):
    """
    Build Schema.org location property for an Event:
    - Physical: Place with name and address.
    - Online: VirtualLocation with public join URL.
    - Hybrid: list containing both Place and VirtualLocation.
    """
    loc_type = str(getattr(event, 'location_type', 'offline')).lower()
    address_str = getattr(event, 'location_address', '') or ''
    meeting_url = getattr(event, 'online_meeting_url', '') or ''

    physical_place = {
        "@type": "Place",
        "name": address_str.strip() if address_str.strip() else "Địa điểm tổ chức sự kiện",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address_str.strip() if address_str.strip() else "Địa điểm sự kiện",
            "addressCountry": "VN"
        }
    }

    # For VirtualLocation, use clean online_meeting_url or public event detail page.
    # Strip query parameters (tokens, passwords) to protect security and privacy.
    clean_meeting_url = meeting_url.strip() if meeting_url.strip() else public_event_url
    if '?' in clean_meeting_url:
        sensitive_params = ('token=', 'pwd=', 'passcode=', 'password=', 'key=', 'secret=', 'sig=', 'auth=')
        if any(sp in clean_meeting_url.lower() for sp in sensitive_params):
            clean_meeting_url = clean_meeting_url.split('?')[0]

    virtual_loc = {
        "@type": "VirtualLocation",
        "url": clean_meeting_url
    }

    if loc_type == 'online':
        return virtual_loc
    elif loc_type == 'hybrid':
        return [physical_place, virtual_loc]
    else:
        return physical_place

def build_ticket_offers(event, public_event_url):
    """
    Build Schema.org Offer objects for public ticket types.
    - Reads real Ticket models associated with the event.
    - Sets price (numeric), priceCurrency (VND), availability (InStock / SoldOut).
    - URL points to the public event detail tickets section (no private credentials).
    """
    offers = []
    tickets = getattr(event, 'tickets', None)
    if not tickets:
        return offers

    ticket_list = tickets.all() if hasattr(tickets, 'all') else list(tickets)
    for ticket in ticket_list:
        ticket_status = getattr(ticket, 'status', 'active')
        if ticket_status not in ('active', 'sold_out', 'closed'):
            continue

        price_val = float(getattr(ticket, 'price', 0.0) or 0.0)
        is_avail = getattr(ticket, 'is_available', False)
        
        offer = {
            "@type": "Offer",
            "name": getattr(ticket, 'name', 'Vé tham dự'),
            "price": round(price_val, 2),
            "priceCurrency": "VND",
            "availability": "https://schema.org/InStock" if is_avail else "https://schema.org/SoldOut",
            "url": f"{public_event_url}#tickets"
        }

        created_at = getattr(ticket, 'created_at', None)
        if created_at and isinstance(created_at, datetime):
            offer["validFrom"] = format_iso8601_date(created_at)

        offers.append(offer)

    return offers

def build_event_schema(event):
    """
    Construct complete, compliant Schema.org Event JSON-LD structure.
    - Omit completely for draft events or draft previews to respect Phase 2.5 privacy.
    - Includes name, description, dates, location, offers, organizer, performer.
    """
    if not event or getattr(event, 'status', '') == 'draft':
        return None

    event_id = getattr(event, 'id', None)
    event_path = f"/events/{event_id}" if event_id is not None else "/events"
    public_event_url = build_canonical_url(event_path)

    # Start date & End date
    start_dt = getattr(event, 'start_date', None)
    start_iso = format_iso8601_date(start_dt)
    if not start_iso:
        return None

    end_dt = getattr(event, 'end_date', None)
    end_iso = format_iso8601_date(end_dt)
    
    # Handle invalid date intervals: end_date before start_date
    if start_dt and end_dt and end_dt < start_dt:
        end_iso = start_iso

    # Clean description
    raw_desc = getattr(event, 'description', '')
    event_title = getattr(event, 'title', '')
    desc_clean = clean_meta_description(raw_desc, fallback=event_title, max_len=5000)

    # Banner image
    banner_url = getattr(event, 'banner_url', None)
    image_url = format_og_image(banner_url)

    # Event Status & Attendance Mode
    event_status = get_schema_event_status(getattr(event, 'status', 'published'))
    attendance_mode = get_schema_attendance_mode(getattr(event, 'location_type', 'offline'))

    # Location
    location = build_event_location(event, public_event_url)

    # Organizer
    organizer_name = "EventAI Pro"
    try:
        creator = getattr(event, 'creator', None)
        if creator and getattr(creator, 'full_name', None):
            organizer_name = creator.full_name.strip()
    except (SAOperationalError, SAInterfaceError, sqlite3.OperationalError, sqlite3.InterfaceError, AttributeError, KeyError, IndexError):
        # Specifically catch detached SQLAlchemy session errors, multithread resultproxy races,
        # or missing creator attributes without silently masking unexpected bugs.
        organizer_name = "EventAI Pro"

    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip().rstrip('/')
    except Exception:
        canonical_domain = ''
    base_origin = canonical_domain if canonical_domain else (request.url_root.rstrip('/') if request else 'https://eventai.pro')

    organizer = {
        "@type": "Organization",
        "name": organizer_name,
        "url": base_origin
    }

    # Offers
    offers = build_ticket_offers(event, public_event_url)

    # Performers from Schedules
    performers = []
    schedules = getattr(event, 'schedules', None)
    if schedules:
        sched_list = schedules.all() if hasattr(schedules, 'all') else list(schedules)
        seen_speakers = set()
        for sched in sched_list:
            speaker = getattr(sched, 'speaker', None)
            if speaker and speaker.id not in seen_speakers:
                seen_speakers.add(speaker.id)
                speaker_item = {
                    "@type": "Person",
                    "name": speaker.name
                }
                if getattr(speaker, 'title', None):
                    speaker_item["jobTitle"] = speaker.title
                performers.append(speaker_item)

    schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event_title,
        "description": desc_clean,
        "url": public_event_url,
        "startDate": start_iso,
        "eventStatus": event_status,
        "eventAttendanceMode": attendance_mode,
        "location": location,
        "image": [image_url],
        "organizer": organizer
    }

    if end_iso:
        schema["endDate"] = end_iso

    if offers:
        schema["offers"] = offers

    if performers:
        schema["performer"] = performers

    return schema

def build_breadcrumb_schema(items):
    """
    Construct Schema.org BreadcrumbList JSON-LD structure.
    items: list of (name, url) tuples or dicts representing navigation hierarchy.
    Example: [('Trang chủ', 'https://eventai.pro/'), ('Sự kiện', 'https://eventai.pro/events'), ('Chi tiết', 'https://eventai.pro/events/1')]
    """
    if not items:
        return None

    elements = []
    for idx, item in enumerate(items, 1):
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            name, url = item[0], item[1]
        elif isinstance(item, dict):
            name, url = item.get('name'), item.get('url')
        else:
            continue
        
        elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": str(name),
            "item": str(url)
        })

    if not elements:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }


# SEO & Sitemaps Protocol Constants
INDEXABLE_EVENT_STATUSES = ('published', 'ongoing', 'completed')
MAX_SITEMAP_URLS = 50000

def is_event_indexable(event):
    """
    Centralized single source of truth for event search engine indexability.
    Eligible for indexing:
    - Must exist and have an ID.
    - Status must be in INDEXABLE_EVENT_STATUSES ('published', 'ongoing', 'completed').
    - Status 'draft' is excluded (unpublished, returns 404 for anonymous).
    - Status 'cancelled' is excluded from sitemap (has noindex directive in HTML).
    """
    if not event:
        return False
    status = str(getattr(event, 'status', '')).lower()
    return status in INDEXABLE_EVENT_STATUSES

def get_trusted_canonical_origin():
    """
    Retrieve and strictly validate the trusted canonical origin.
    - Honors CANONICAL_DOMAIN from current_app.config or os.environ.
    - Strict validation: scheme must be http or https, hostname must be valid,
      no credentials, no newlines/CRLF injection, no path/query parameters.
    - When CANONICAL_DOMAIN is empty (local dev / testing):
      safely falls back to request.url_root if valid, or 'http://localhost:5000'.
    - Rejects suspicious or injected Host / X-Forwarded-Host headers.
    """
    canonical_domain = ""
    try:
        canonical_domain = current_app.config.get('CANONICAL_DOMAIN', '').strip()
    except Exception:
        canonical_domain = os.getenv('CANONICAL_DOMAIN', '').strip()

    if canonical_domain:
        canonical_domain = canonical_domain.rstrip('/')
        if '\r' in canonical_domain or '\n' in canonical_domain:
            raise ValueError("CANONICAL_DOMAIN contains invalid newline characters.")
            
        parsed = urlparse(canonical_domain)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError(f"CANONICAL_DOMAIN must use http or https scheme: {canonical_domain}")
            
        if not parsed.netloc:
            raise ValueError(f"CANONICAL_DOMAIN has invalid netloc: {canonical_domain}")
            
        if '@' in parsed.netloc:
            raise ValueError("CANONICAL_DOMAIN must not contain user credentials.")
            
        return f"{parsed.scheme}://{parsed.netloc}"

    # Safe development/testing fallback
    if request:
        try:
            raw_host = request.host
            if '\r' in raw_host or '\n' in raw_host or ' ' in raw_host or '@' in raw_host:
                return 'http://localhost:5000'
            if not re.match(r'^[a-zA-Z0-9\.\-]+(:\d+)?$', raw_host):
                return 'http://localhost:5000'
            scheme = request.scheme if request.scheme in ('http', 'https') else 'http'
            return f"{scheme}://{raw_host}"
        except Exception:
            return 'http://localhost:5000'

    return 'http://localhost:5000'

def build_sitemap_xml(base_origin=None, event_records=None):
    """
    Generate standard compliant XML sitemap string.
    - Base origin validated through get_trusted_canonical_origin().
    - Includes core public static pages: '/' and '/events'.
    - Includes public indexable events from event_records: list of (event_id, updated_at).
    - Preserves accurate lastmod from real updated_at timestamps (omits if not present).
    - Guaranteed unique URLs, stable ordering, and XML character escaping.
    """
    origin = base_origin if base_origin else get_trusted_canonical_origin()
    origin = origin.rstrip('/')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    seen_urls = set()

    # 1. Homepage
    home_url = f"{origin}/"
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{xml_escape(home_url)}</loc>')
    xml_lines.append('  </url>')
    seen_urls.add(home_url)

    # 2. Events List Page
    events_url = f"{origin}/events"
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{xml_escape(events_url)}</loc>')
    xml_lines.append('  </url>')
    seen_urls.add(events_url)

    # 3. Public Indexable Events
    if event_records:
        for item in event_records:
            if len(seen_urls) >= MAX_SITEMAP_URLS:
                break

            if isinstance(item, (tuple, list)):
                event_id = item[0]
                updated_at = item[1] if len(item) > 1 else None
            else:
                event_id = getattr(item, 'id', None)
                updated_at = getattr(item, 'updated_at', None)

            if not event_id:
                continue

            event_url = f"{origin}/events/{event_id}"
            if event_url in seen_urls:
                continue
            seen_urls.add(event_url)

            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{xml_escape(event_url)}</loc>')
            if updated_at and isinstance(updated_at, datetime):
                xml_lines.append(f'    <lastmod>{updated_at.strftime("%Y-%m-%d")}</lastmod>')
            xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    return '\n'.join(xml_lines)

def build_robots_txt(base_origin=None):
    """
    Generate standard compliant plain text robots.txt string.
    - Disallows crawler access to administrative, checkin, QR codes and internal API routes.
    - Allows crawler access to public CSS and JavaScript assets.
    - Does NOT block auth routes so search engines can read their noindex directives.
    - References valid Sitemap URL using the trusted canonical origin.
    """
    origin = base_origin if base_origin else get_trusted_canonical_origin()
    origin = origin.rstrip('/')

    lines = [
        "User-agent: *",
        "Allow: /",
        "Allow: /static/css/",
        "Allow: /static/js/",
        "",
        "# Administrative & check-in interfaces",
        "Disallow: /admin/",
        "Disallow: /checkin/",
        "",
        "# Defense-in-depth: Private QR ticket assets",
        "Disallow: /static/qr_codes/",
        "",
        "# Internal API endpoints",
        "Disallow: /api/",
        "",
        f"Sitemap: {origin}/sitemap.xml"
    ]
    return '\n'.join(lines) + '\n'
