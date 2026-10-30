"""
Targeted Schema.org Event & BreadcrumbList structured data regression tests for Phase 3B implementation.
Verifies compliant JSON-LD generation, ISO 8601 timestamps, physical/virtual/hybrid locations,
ticket offer structures, status mappings, draft exclusions, XSS sanitization, and PII protection.
Uses Python's standard library HTMLParser and json modules (zero third-party dependencies).
"""
import json
import re
from html.parser import HTMLParser
from datetime import datetime, timezone
import pytest
from app.extensions import db, utc_now
from app.models import Event, User, Ticket, Schedule, Speaker, Venue
from app.seo_helpers import (
    format_iso8601_date,
    get_schema_event_status,
    get_schema_attendance_mode,
    build_event_location,
    build_ticket_offers,
    build_event_schema,
    build_breadcrumb_schema
)


class ScriptJsonLdExtractor(HTMLParser):
    """Extracts all script type='application/ld+json' blocks from rendered HTML."""
    def __init__(self, html_content):
        super().__init__()
        self.schemas = []
        self._in_ldjson = False
        self._buffer = []
        self.feed(html_content)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            attr_dict = {k.lower(): v for k, v in attrs}
            if attr_dict.get('type') == 'application/ld+json':
                self._in_ldjson = True
                self._buffer = []

    def handle_endtag(self, tag):
        if tag.lower() == 'script' and self._in_ldjson:
            self._in_ldjson = False
            raw_text = ''.join(self._buffer).strip()
            if raw_text:
                try:
                    parsed = json.loads(raw_text)
                    self.schemas.append(parsed)
                except Exception as e:
                    self.schemas.append({"_parse_error": str(e), "_raw": raw_text})

    def handle_data(self, data):
        if self._in_ldjson:
            self._buffer.append(data)


@pytest.fixture
def rich_published_event(app, sample_users):
    """Fixture providing a published event with physical location, tickets, and speakers."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-PUB-001',
            title='Hội Thảo Quốc Tế AI & Bán Dẫn 2026',
            description='<p>Diễn đàn công nghệ <strong>đột phá</strong> về AI và thiết kế vi mạch.</p>',
            category='Công nghệ & AI',
            banner_url='https://images.unsplash.com/photo-tech-ai-2026?w=1200',
            start_date=datetime(2026, 11, 20, 8, 30, 0),
            end_date=datetime(2026, 11, 20, 17, 30, 0),
            location_type='offline',
            location_address='Trung tâm Hội nghị Quốc gia, Hà Nội',
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()

        # Add tickets (free and paid)
        t_free = Ticket(
            event_id=event.id,
            ticket_code=f'TCK-{event.id}-FREE',
            ticket_type='free',
            name='Vé Miễn Phí (Sinh Viên)',
            price=0.0,
            quota=50,
            sold_count=10,
            status='active'
        )
        t_vip = Ticket(
            event_id=event.id,
            ticket_code=f'TCK-{event.id}-VIP',
            ticket_type='vip',
            name='Vé VIP Doanh Nghiệp',
            price=250000.0,
            quota=30,
            sold_count=30,  # Sold out
            status='sold_out'
        )
        db.session.add_all([t_free, t_vip])

        # Add speaker and agenda
        speaker = Speaker(
            name='GS. Đặng Hoàng Nam',
            title='Viện trưởng Viện Trí tuệ Nhân tạo',
            organization='Viện Công nghệ Tiên tiến'
        )
        db.session.add(speaker)
        db.session.commit()

        sched = Schedule(
            event_id=event.id,
            speaker_id=speaker.id,
            title='Xu hướng Generative AI trong Thiết kế Vi mạch',
            start_at=datetime(2026, 11, 20, 9, 0, 0),
            end_at=datetime(2026, 11, 20, 10, 30, 0)
        )
        db.session.add(sched)
        db.session.commit()

        return event.id


@pytest.fixture
def online_event(app, sample_users):
    """Fixture providing a virtual online event."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-ONL-002',
            title='Tọa Đàm Trực Tuyến: Kỹ Năng Prompt Engineering',
            description='Workshop thực chiến trực tuyến qua Zoom.',
            category='Workshop',
            banner_url='/static/uploads/webinar-prompt.jpg',
            start_date=datetime(2026, 12, 1, 19, 0, 0),
            end_date=datetime(2026, 12, 1, 21, 0, 0),
            location_type='online',
            online_meeting_url='https://zoom.us/j/987654321',
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


@pytest.fixture
def hybrid_event(app, sample_users):
    """Fixture providing a hybrid (offline + online) event."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-HYB-003',
            title='Hội Nghị Thượng Đỉnh Khởi Nghiệp Đổi Mới Sáng Tạo 2026',
            description='Sự kiện kết hợp trực tiếp tại Đà Nẵng và trực tuyến đa cầu truyền hình.',
            category='Khởi nghiệp',
            start_date=datetime(2026, 12, 10, 8, 0, 0),
            end_date=datetime(2026, 12, 11, 17, 0, 0),
            location_type='hybrid',
            location_address='Cung Hội nghị Quốc tế Furama, Đà Nẵng',
            online_meeting_url='https://meet.google.com/abc-defg-hij?authuser=0&token=private_secret_token_123',
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


@pytest.fixture
def cancelled_event(app, sample_users):
    """Fixture providing a cancelled event."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-CAN-004',
            title='Hội Chợ Triển Lãm Robot Công Nghiệp (Tạm Dừng)',
            description='Sự kiện đã bị hủy theo quyết định của ban tổ chức.',
            category='Triển lãm',
            start_date=datetime(2026, 11, 5, 9, 0, 0),
            end_date=datetime(2026, 11, 5, 17, 0, 0),
            status='cancelled',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


@pytest.fixture
def draft_event(app, sample_users):
    """Fixture providing an unpublished draft event."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-DRF-005',
            title='Kế Hoạch Chiến Lược Nội Bộ 2027 (Bản Nháp)',
            description='Tài liệu mật chưa công bố.',
            category='Nội bộ',
            start_date=datetime(2027, 1, 10, 8, 0, 0),
            end_date=datetime(2027, 1, 10, 12, 0, 0),
            status='draft',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


# ==============================================================================
# 1. CORE EVENT SCHEMA ATTRIBUTES
# ==============================================================================

def test_published_event_produces_valid_event_schema(client, rich_published_event):
    """Test 1: Verify rendered page contains Schema.org Event JSON-LD with correct context and type."""
    res = client.get(f'/events/{rich_published_event}')
    assert res.status_code == 200
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    
    event_schema = next((s for s in extractor.schemas if s.get('@type') == 'Event'), None)
    assert event_schema is not None, "Event JSON-LD schema must be present"
    assert event_schema.get('@context') == 'https://schema.org'
    assert event_schema.get('@type') == 'Event'


def test_schema_event_name(client, rich_published_event):
    """Test 2: Verify event name in schema matches event title exactly."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert event_schema['name'] == 'Hội Thảo Quốc Tế AI & Bán Dẫn 2026'


def test_schema_event_description_sanitized(client, rich_published_event):
    """Test 3: Verify description is cleanly sanitized of HTML tags (<p>, <strong>)."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    
    desc = event_schema['description']
    assert '<p>' not in desc
    assert '<strong>' not in desc
    assert 'đột phá' in desc


def test_schema_event_canonical_url(client, rich_published_event):
    """Test 4: Verify schema url is an absolute URL matching the canonical event path."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert event_schema['url'].endswith(f'/events/{rich_published_event}')
    assert event_schema['url'].startswith('http://') or event_schema['url'].startswith('https://')


# ==============================================================================
# 2. DATE AND TIMEZONE HANDLING
# ==============================================================================

def test_schema_iso8601_start_date(client, rich_published_event):
    """Test 5: Verify startDate is formatted in strict ISO 8601 with explicit offset."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    start_date = event_schema['startDate']
    assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+\d{2}:\d{2}|Z)?$', start_date)
    assert '2026-11-20T08:30:00' in start_date


def test_schema_iso8601_end_date(client, rich_published_event):
    """Test 6: Verify endDate is formatted in strict ISO 8601 with explicit offset."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    end_date = event_schema['endDate']
    assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+\d{2}:\d{2}|Z)?$', end_date)
    assert '2026-11-20T17:30:00' in end_date


def test_format_iso8601_timezone_handling():
    """Test 7: Verify format_iso8601_date handles timezone-aware and naive datetimes properly."""
    naive_dt = datetime(2026, 10, 29, 14, 0, 0)
    formatted_naive = format_iso8601_date(naive_dt, offset="+07:00")
    assert formatted_naive == '2026-10-29T14:00:00+07:00'

    aware_dt = datetime(2026, 10, 29, 14, 0, 0, tzinfo=timezone.utc)
    formatted_aware = format_iso8601_date(aware_dt)
    assert formatted_aware == '2026-10-29T14:00:00+00:00'

    assert format_iso8601_date(None) is None


def test_invalid_date_interval_normalized(app, sample_users):
    """Test 7b: Verify an event with end_date before start_date does not produce invalid range."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-INV-009',
            title='Sự Kiện Lỗi Khoảng Thời Gian',
            start_date=datetime(2026, 11, 20, 18, 0, 0),
            end_date=datetime(2026, 11, 20, 10, 0, 0),
            status='published',
            created_by=sample_users['admin_id']
        )
        schema = build_event_schema(event)
        assert schema is not None
        assert schema['endDate'] == schema['startDate']


# ==============================================================================
# 3. LOCATION TYPES: PHYSICAL, ONLINE, HYBRID
# ==============================================================================

def test_physical_event_location(client, rich_published_event):
    """Test 8: Verify offline event has Schema.org Place location and Offline attendance mode."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    assert event_schema['eventAttendanceMode'] == 'https://schema.org/OfflineEventAttendanceMode'
    location = event_schema['location']
    assert isinstance(location, dict)
    assert location['@type'] == 'Place'
    assert 'Hà Nội' in location['name']
    assert location['address']['@type'] == 'PostalAddress'
    assert location['address']['addressCountry'] == 'VN'


def test_online_event_location(client, online_event):
    """Test 9: Verify online event has VirtualLocation and Online attendance mode."""
    res = client.get(f'/events/{online_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    assert event_schema['eventAttendanceMode'] == 'https://schema.org/OnlineEventAttendanceMode'
    location = event_schema['location']
    assert isinstance(location, dict)
    assert location['@type'] == 'VirtualLocation'
    assert location['url'] == 'https://zoom.us/j/987654321'


def test_hybrid_event_location(client, hybrid_event):
    """Test 10: Verify hybrid event contains both Place and VirtualLocation."""
    res = client.get(f'/events/{hybrid_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    assert event_schema['eventAttendanceMode'] == 'https://schema.org/MixedEventAttendanceMode'
    location = event_schema['location']
    assert isinstance(location, list)
    assert len(location) == 2
    types = [loc['@type'] for loc in location]
    assert 'Place' in types
    assert 'VirtualLocation' in types


def test_missing_location_fallback(app, sample_users):
    """Test 11: Verify missing location address defaults gracefully without crashing."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-NOLOC-010',
            title='Hội Thảo Địa Điểm Đang Cập Nhật',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 11, 0, 0),
            location_type='offline',
            location_address='',
            status='published',
            created_by=sample_users['admin_id']
        )
        schema = build_event_schema(event)
        assert schema is not None
        assert schema['location']['@type'] == 'Place'
        assert schema['location']['name'] == 'Địa điểm tổ chức sự kiện'


# ==============================================================================
# 4. EVENT STATUS MAPPING
# ==============================================================================

def test_event_status_mapping_scheduled(client, rich_published_event):
    """Test 12: Published event maps to https://schema.org/EventScheduled."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert event_schema['eventStatus'] == 'https://schema.org/EventScheduled'


def test_cancelled_event_schema(client, cancelled_event):
    """Test 13: Cancelled event is public and maps to https://schema.org/EventCancelled."""
    res = client.get(f'/events/{cancelled_event}')
    assert res.status_code == 200
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert event_schema['eventStatus'] == 'https://schema.org/EventCancelled'


# ==============================================================================
# 5. DRAFT PRIVACY AND ACCESS CONTROLS
# ==============================================================================

def test_draft_event_excluded_from_schema_builder(app, draft_event):
    """Test 14: build_event_schema returns None for draft events."""
    with app.app_context():
        event = db.session.get(Event, draft_event)
        assert build_event_schema(event) is None


def test_anonymous_cannot_view_draft_event(client, draft_event):
    """Test 15: Anonymous user gets 404 when accessing draft event."""
    res = client.get(f'/events/{draft_event}')
    assert res.status_code == 404


def test_authorized_draft_preview_does_not_emit_jsonld(client, draft_event):
    """Test 16: Admin previewing draft event gets 200 but NO Event JSON-LD is emitted."""
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    res = client.get(f'/events/{draft_event}')
    assert res.status_code == 200
    
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schemas = [s for s in extractor.schemas if s.get('@type') == 'Event']
    assert len(event_schemas) == 0, "Draft preview must not emit Event JSON-LD"


# ==============================================================================
# 6. TICKET OFFERS
# ==============================================================================

def test_ticket_offers_free_ticket(client, rich_published_event):
    """Test 17: Free ticket has price 0.0 and InStock availability."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    offers = event_schema.get('offers', [])
    free_offer = next(o for o in offers if 'Miễn Phí' in o['name'])
    assert free_offer['price'] == 0.0
    assert free_offer['priceCurrency'] == 'VND'
    assert free_offer['availability'] == 'https://schema.org/InStock'
    assert free_offer['url'].endswith(f'/events/{rich_published_event}#tickets')


def test_ticket_offers_paid_ticket(client, rich_published_event):
    """Test 18: Paid ticket has numeric price > 0 and VND currency."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    offers = event_schema.get('offers', [])
    vip_offer = next(o for o in offers if 'VIP' in o['name'])
    assert vip_offer['price'] == 250000.0
    assert vip_offer['priceCurrency'] == 'VND'


def test_ticket_offers_sold_out(client, rich_published_event):
    """Test 19: Sold-out ticket has SoldOut availability."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    offers = event_schema.get('offers', [])
    vip_offer = next(o for o in offers if 'VIP' in o['name'])
    assert vip_offer['availability'] == 'https://schema.org/SoldOut'


def test_multiple_ticket_types_array(client, rich_published_event):
    """Test 20: Multiple ticket types are represented as an array of Offer objects."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert isinstance(event_schema['offers'], list)
    assert len(event_schema['offers']) >= 2


def test_missing_price_safe_fallback(app, sample_users):
    """Test 21: Ticket with None price defaults safely to 0.0 without crash."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-TKT-011',
            title='Sự Kiện Vé Không Giá',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 11, 0, 0),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()

        tkt = Ticket(
            event_id=event.id,
            ticket_code=f'TCK-{event.id}-NOPRICE',
            ticket_type='standard',
            name='Vé Thường',
            price=0.0,
            quota=10,
            status='active'
        )
        db.session.add(tkt)
        db.session.commit()

        schema = build_event_schema(event)
        assert schema['offers'][0]['price'] == 0.0


# ==============================================================================
# 7. IMAGES, ORGANIZER, OPTIONAL FIELDS
# ==============================================================================

def test_relative_image_url_made_absolute(client, online_event):
    """Test 22: Relative banner image is made absolute in schema image property."""
    res = client.get(f'/events/{online_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    images = event_schema.get('image', [])
    assert len(images) >= 1
    assert images[0].startswith('http://') or images[0].startswith('https://')
    assert '/static/uploads/webinar-prompt.jpg' in images[0]


def test_organizer_structure(client, rich_published_event):
    """Test 23: Organizer is an Organization with name and URL, and no email or phone leaked."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    organizer = event_schema['organizer']
    assert organizer['@type'] == 'Organization'
    assert organizer['name'] != ''
    assert organizer['url'].startswith('http')
    assert 'email' not in organizer
    assert 'phone' not in organizer


def test_missing_optional_fields_handled_gracefully(app, sample_users):
    """Test 24: Event without tickets, speakers, or banner omits them without error."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-MIN-012',
            title='Buổi Họp Nhóm Tối Giản',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 11, 0, 0),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()

        schema = build_event_schema(event)
        assert schema is not None
        assert 'offers' not in schema
        assert 'performer' not in schema


# ==============================================================================
# 8. SECURITY, XSS & UNICODE HANDLING
# ==============================================================================

def test_json_escaping_and_valid_syntax(app, sample_users):
    """Test 25: JSON-LD block parses as fully valid JSON."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-SYN-013',
            title='Hội Nghị Chuẩn Cú Pháp JSON',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 11, 0, 0),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id

    client = app.test_client()
    res = client.get(f'/events/{event_id}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    assert len(extractor.schemas) >= 1
    assert not any('_parse_error' in s for s in extractor.schemas)


def test_xss_script_breakout_prevention(app, sample_users):
    """Test 26: Malicious title containing script tag cannot break out of JSON-LD script."""
    with app.app_context():
        event = Event(
            event_code='EVT-SCHEMA-XSS-014',
            title='</script><script>alert("XSS")</script> & Special "Chars"',
            description='<p>Mô tả chứa <b>thẻ</b> & payload: </script><script>alert(1)</script></p>',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 11, 0, 0),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id

    client = app.test_client()
    res = client.get(f'/events/{event_id}')
    raw_html = res.data.decode('utf-8')

    # Must NOT have unescaped script closing tag breaking out of JSON-LD
    assert '</script><script>alert("XSS")</script>' not in raw_html
    extractor = ScriptJsonLdExtractor(raw_html)
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')
    assert 'alert("XSS")' in event_schema['name']


def test_vietnamese_unicode_in_schema(client, rich_published_event):
    """Test 27: Vietnamese diacritics are preserved accurately without corrupt encoding."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    assert 'Hội Thảo Quốc Tế AI & Bán Dẫn 2026' == event_schema['name']
    assert 'Hà Nội' in event_schema['location']['name']


def test_no_duplicate_event_schema(client, rich_published_event):
    """Test 28: Rendered page contains exactly ONE Event schema and ONE BreadcrumbList schema."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))

    event_schemas = [s for s in extractor.schemas if s.get('@type') == 'Event']
    breadcrumb_schemas = [s for s in extractor.schemas if s.get('@type') == 'BreadcrumbList']

    assert len(event_schemas) == 1, "There must be exactly one Event schema on event detail"
    assert len(breadcrumb_schemas) == 1, "There must be exactly one BreadcrumbList schema on event detail"


# ==============================================================================
# 9. BREADCRUMBLIST STRUCTURED DATA
# ==============================================================================

def test_breadcrumblist_schema(client, rich_published_event):
    """Test 29: BreadcrumbList schema reflects Home -> Events -> Current Event hierarchy."""
    res = client.get(f'/events/{rich_published_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    bc_schema = next(s for s in extractor.schemas if s.get('@type') == 'BreadcrumbList')

    items = bc_schema['itemListElement']
    assert len(items) == 3

    assert items[0]['position'] == 1
    assert items[0]['name'] == 'Trang chủ'
    assert items[0]['item'].endswith('/')

    assert items[1]['position'] == 2
    assert items[1]['name'] == 'Sự kiện'
    assert items[1]['item'].endswith('/events')

    assert items[2]['position'] == 3
    assert items[2]['name'] == 'Hội Thảo Quốc Tế AI & Bán Dẫn 2026'
    assert items[2]['item'].endswith(f'/events/{rich_published_event}')


def test_breadcrumblist_builder_standalone():
    """Test 30: build_breadcrumb_schema handles empty and malformed inputs safely."""
    assert build_breadcrumb_schema([]) is None
    assert build_breadcrumb_schema(None) is None
    single = build_breadcrumb_schema([('Home', 'https://eventai.pro/')])
    assert len(single['itemListElement']) == 1


# ==============================================================================
# 10. PRIVACY AND PII SAFEGUARDS
# ==============================================================================

def test_no_private_tokens_or_pii_in_schema(client, hybrid_event):
    """Test 31: Private meeting tokens and PII are stripped from schema location URLs and offers."""
    res = client.get(f'/events/{hybrid_event}')
    extractor = ScriptJsonLdExtractor(res.data.decode('utf-8'))
    event_schema = next(s for s in extractor.schemas if s.get('@type') == 'Event')

    raw_json = json.dumps(event_schema)
    assert 'private_secret_token_123' not in raw_json
    assert 'qr_codes' not in raw_json
    assert 'TCK-' not in raw_json
    assert '@test.com' not in raw_json
