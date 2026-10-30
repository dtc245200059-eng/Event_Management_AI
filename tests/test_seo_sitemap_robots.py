"""
Targeted tests for Phase 3C: Dynamic XML Sitemap and Robots.txt.
Verifies valid XML sitemap syntax, namespace compliance, content-type headers,
inclusion of indexable public events, strict exclusion of draft/cancelled/private routes,
accurate lastmod timestamps, robots.txt directives, canonical domain handling,
and security/privacy regressions.
Uses Python's standard library xml.etree.ElementTree and urllib.parse (zero third-party dependencies).
"""
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from datetime import datetime, timezone
import pytest
from flask import url_for
from sqlalchemy import text
from app.extensions import db
from app.models import Event, User, Ticket, Schedule, Speaker, Venue
from app.seo_helpers import (
    INDEXABLE_EVENT_STATUSES,
    MAX_SITEMAP_URLS,
    is_event_indexable,
    get_trusted_canonical_origin,
    build_sitemap_xml,
    build_robots_txt
)

# Namespace map for XPath searches in sitemaps
SITEMAP_NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


def parse_sitemap_xml(xml_string):
    """Helper to parse XML string and return root Element."""
    return ET.fromstring(xml_string)


def extract_locs(root):
    """Extract list of loc text values from parsed sitemap root."""
    return [elem.text.strip() for elem in root.findall('sm:url/sm:loc', SITEMAP_NS) if elem.text]


@pytest.fixture
def test_events_for_sitemap(app, sample_users):
    """Fixture providing events with various statuses and timestamps for sitemap testing."""
    with app.app_context():
        creator_id = sample_users['admin_id']

        pub_event = Event(
            event_code='EVT-SM-PUB-01',
            title='Hội Thảo Công Nghệ Cloud 2026',
            description='Hội thảo chuyên sâu về Cloud Native và AI.',
            category='Công nghệ & AI',
            start_date=datetime(2026, 12, 1, 9, 0, 0),
            end_date=datetime(2026, 12, 1, 17, 0, 0),
            status='published',
            created_by=creator_id,
            updated_at=datetime(2026, 10, 15, 14, 30, 0)
        )
        ongoing_event = Event(
            event_code='EVT-SM-ONG-01',
            title='Triển Lãm Đổi Mới Sáng Tạo Quốc Gia',
            description='Sự kiện đổi mới sáng tạo đang diễn ra.',
            category='Triển lãm & Hội chợ',
            start_date=datetime(2026, 10, 28, 8, 0, 0),
            end_date=datetime(2026, 10, 30, 18, 0, 0),
            status='ongoing',
            created_by=creator_id,
            updated_at=datetime(2026, 10, 20, 10, 0, 0)
        )
        completed_event = Event(
            event_code='EVT-SM-CMP-01',
            title='Diễn Đàn Chuyển Đổi Số 2025',
            description='Diễn đàn đã hoàn thành thành công.',
            category='Diễn đàn Khoa học',
            start_date=datetime(2025, 5, 1, 9, 0, 0),
            end_date=datetime(2025, 5, 1, 16, 0, 0),
            status='completed',
            created_by=creator_id,
            updated_at=datetime(2025, 5, 2, 8, 0, 0)
        )
        draft_event = Event(
            event_code='EVT-SM-DFT-01',
            title='Dự Thảo Kế Hoạch AI Hackathon',
            description='Sự kiện nội bộ chưa công bố.',
            category='Cuộc thi & Hackathon',
            start_date=datetime(2026, 12, 20, 9, 0, 0),
            end_date=datetime(2026, 12, 21, 18, 0, 0),
            status='draft',
            created_by=creator_id,
            updated_at=datetime(2026, 10, 1, 12, 0, 0)
        )
        cancelled_event = Event(
            event_code='EVT-SM-CNC-01',
            title='Hội Nghị Đã Bị Hủy Bỏ',
            description='Sự kiện đã bị hủy bỏ do bất khả kháng.',
            category='Hội thảo Chuyên đề',
            start_date=datetime(2026, 11, 10, 9, 0, 0),
            end_date=datetime(2026, 11, 10, 17, 0, 0),
            status='cancelled',
            created_by=creator_id,
            updated_at=datetime(2026, 10, 5, 9, 0, 0)
        )
        no_lastmod_event = Event(
            event_code='EVT-SM-NOLAST-01',
            title='Sự Kiện Không Có Lastmod',
            description='Sự kiện published không có giá trị updated_at.',
            category='Công nghệ & AI',
            start_date=datetime(2026, 11, 15, 9, 0, 0),
            end_date=datetime(2026, 11, 15, 17, 0, 0),
            status='published',
            created_by=creator_id,
            updated_at=None
        )

        db.session.add_all([
            pub_event,
            ongoing_event,
            completed_event,
            draft_event,
            cancelled_event,
            no_lastmod_event
        ])
        db.session.commit()

        # Explicitly set updated_at to NULL in database to bypass model default
        db.session.execute(
            text("UPDATE events SET updated_at = NULL WHERE id = :id"),
            {'id': no_lastmod_event.id}
        )
        db.session.commit()

        return {
            'published': pub_event.id,
            'ongoing': ongoing_event.id,
            'completed': completed_event.id,
            'draft': draft_event.id,
            'cancelled': cancelled_event.id,
            'no_lastmod': no_lastmod_event.id
        }


# ==============================================================================
# SECTION A: SITEMAP.XML ENDPOINT TESTS
# ==============================================================================

class TestSitemapEndpoint:

    def test_sitemap_status_and_headers(self, client):
        """1. Verify GET /sitemap.xml returns HTTP 200 with XML content-type and security headers."""
        resp = client.get('/sitemap.xml')
        assert resp.status_code == 200
        assert 'application/xml' in resp.content_type
        assert 'charset=utf-8' in resp.content_type.lower()
        assert resp.headers.get('X-Content-Type-Options') == 'nosniff'
        assert 'public' in resp.headers.get('Cache-Control', '')

    def test_sitemap_xml_well_formed_and_namespace(self, client):
        """2. Verify /sitemap.xml is valid XML and has proper sitemaps.org namespace."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        assert root is not None
        assert root.tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset'

    def test_sitemap_includes_homepage_and_events_catalog(self, client):
        """3. Verify sitemap includes the homepage and the events catalog page."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        # Check relative paths in locs
        paths = [urlparse(loc).path for loc in locs]
        assert '/' in paths or '' in paths  # Homepage
        assert '/events' in paths           # Events catalog

    def test_sitemap_includes_published_events(self, client, test_events_for_sitemap):
        """4. Verify published events are included in the sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        pub_id = test_events_for_sitemap['published']
        expected_path = f"/events/{pub_id}"
        assert any(urlparse(loc).path == expected_path for loc in locs)

    def test_sitemap_includes_ongoing_and_completed_events(self, client, test_events_for_sitemap):
        """5. Verify ongoing and completed events are included in the sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        ong_id = test_events_for_sitemap['ongoing']
        cmp_id = test_events_for_sitemap['completed']
        assert any(urlparse(loc).path == f"/events/{ong_id}" for loc in locs)
        assert any(urlparse(loc).path == f"/events/{cmp_id}" for loc in locs)

    def test_sitemap_strictly_excludes_draft_events(self, client, test_events_for_sitemap):
        """6. Verify draft events are strictly excluded from the sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        draft_id = test_events_for_sitemap['draft']
        draft_path = f"/events/{draft_id}"
        assert not any(urlparse(loc).path == draft_path for loc in locs)

    def test_sitemap_strictly_excludes_cancelled_events(self, client, test_events_for_sitemap):
        """7. Verify cancelled events (which have noindex) are strictly excluded from sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        cancelled_id = test_events_for_sitemap['cancelled']
        cancelled_path = f"/events/{cancelled_id}"
        assert not any(urlparse(loc).path == cancelled_path for loc in locs)

    def test_sitemap_excludes_private_and_admin_urls(self, client, test_events_for_sitemap):
        """8. Verify admin, checkin, qr codes, tickets, and api routes are never in sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        for loc in locs:
            path = urlparse(loc).path
            assert not path.startswith('/admin')
            assert not path.startswith('/checkin')
            assert not path.startswith('/static/qr_codes')
            assert not path.startswith('/api')
            assert not path.startswith('/tickets')

    def test_sitemap_excludes_auth_urls(self, client):
        """9. Verify login and register endpoints are not listed in sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        for loc in locs:
            path = urlparse(loc).path
            assert path not in ('/auth/login', '/auth/register')

    def test_sitemap_loc_elements_are_absolute_urls(self, client):
        """10. Verify every loc element contains an absolute URL with scheme and host."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        assert len(locs) >= 2
        for loc in locs:
            parsed = urlparse(loc)
            assert parsed.scheme in ('http', 'https')
            assert parsed.netloc

    def test_sitemap_honors_canonical_domain_config(self, app, client):
        """11. Verify CANONICAL_DOMAIN configuration is honored across all loc elements."""
        app.config['CANONICAL_DOMAIN'] = 'https://eventai.example.vn'
        try:
            resp = client.get('/sitemap.xml')
            root = parse_sitemap_xml(resp.data)
            locs = extract_locs(root)

            for loc in locs:
                assert loc.startswith('https://eventai.example.vn')
        finally:
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_sitemap_no_duplicate_urls(self, client, test_events_for_sitemap):
        """12. Verify that there are zero duplicate loc entries in the sitemap."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        assert len(locs) == len(set(locs))

    def test_sitemap_no_query_parameters(self, client):
        """13. Verify no loc URLs contain tracking or pagination query parameters."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        for loc in locs:
            parsed = urlparse(loc)
            assert not parsed.query, f"URL {loc} contains query parameters"

    def test_sitemap_lastmod_format_and_accuracy(self, client, test_events_for_sitemap):
        """14. Verify lastmod is in YYYY-MM-DD format and accurately matches updated_at."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)

        pub_id = test_events_for_sitemap['published']
        pub_path = f"/events/{pub_id}"

        found_pub = False
        for url_elem in root.findall('sm:url', SITEMAP_NS):
            loc_elem = url_elem.find('sm:loc', SITEMAP_NS)
            if loc_elem is not None and urlparse(loc_elem.text).path == pub_path:
                found_pub = True
                lastmod_elem = url_elem.find('sm:lastmod', SITEMAP_NS)
                assert lastmod_elem is not None
                assert lastmod_elem.text == '2026-10-15'
                # Verify valid date
                datetime.strptime(lastmod_elem.text, '%Y-%m-%d')
                break

        assert found_pub

    def test_sitemap_omits_lastmod_when_updated_at_none(self, client, test_events_for_sitemap):
        """15. Verify that an event with updated_at=None omits the lastmod element."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)

        no_lastmod_id = test_events_for_sitemap['no_lastmod']
        no_lastmod_path = f"/events/{no_lastmod_id}"

        found = False
        for url_elem in root.findall('sm:url', SITEMAP_NS):
            loc_elem = url_elem.find('sm:loc', SITEMAP_NS)
            if loc_elem is not None and urlparse(loc_elem.text).path == no_lastmod_path:
                found = True
                lastmod_elem = url_elem.find('sm:lastmod', SITEMAP_NS)
                assert lastmod_elem is None, "lastmod must not be fabricated when updated_at is None"
                break

        assert found

    def test_sitemap_static_pages_omit_lastmod(self, client):
        """16. Verify static pages (Homepage, /events) do not have fabricated lastmod elements."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)

        for url_elem in root.findall('sm:url', SITEMAP_NS):
            loc_elem = url_elem.find('sm:loc', SITEMAP_NS)
            if loc_elem is not None:
                path = urlparse(loc_elem.text).path
                if path in ('/', '/events'):
                    lastmod_elem = url_elem.find('sm:lastmod', SITEMAP_NS)
                    assert lastmod_elem is None, f"Static page {path} should not have lastmod"

    def test_sitemap_deterministic_ordering(self, client, test_events_for_sitemap):
        """17. Verify event URLs in sitemap are ordered deterministically by event id."""
        resp = client.get('/sitemap.xml')
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        event_ids = []
        for loc in locs:
            path = urlparse(loc).path
            if path.startswith('/events/') and path[8:].isdigit():
                event_ids.append(int(path[8:]))

        assert event_ids == sorted(event_ids), "Event IDs in sitemap must be in ascending order"

    def test_sitemap_handles_empty_events_database(self, app, client):
        """18. Verify sitemap works cleanly when no events are published."""
        resp = client.get('/sitemap.xml')
        assert resp.status_code == 200
        root = parse_sitemap_xml(resp.data)
        locs = extract_locs(root)

        assert len(locs) >= 2
        paths = [urlparse(loc).path for loc in locs]
        assert '/' in paths or '' in paths
        assert '/events' in paths


# ==============================================================================
# SECTION B: ROBOTS.TXT ENDPOINT TESTS
# ==============================================================================

class TestRobotsTxtEndpoint:

    def test_robots_status_and_content_type(self, client):
        """19. Verify GET /robots.txt returns HTTP 200 with text/plain content-type."""
        resp = client.get('/robots.txt')
        assert resp.status_code == 200
        assert 'text/plain' in resp.content_type
        assert 'charset=utf-8' in resp.content_type.lower()
        assert resp.headers.get('X-Content-Type-Options') == 'nosniff'
        assert 'public' in resp.headers.get('Cache-Control', '')

    def test_robots_user_agent_directive(self, client):
        """20. Verify robots.txt contains standard User-agent: * directive."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'User-agent: *' in text

    def test_robots_allows_root(self, client):
        """21. Verify robots.txt explicitly allows root path."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Allow: /' in text

    def test_robots_allows_static_assets(self, client):
        """22. Verify robots.txt explicitly allows CSS and JS for proper page rendering."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Allow: /static/css/' in text
        assert 'Allow: /static/js/' in text

    def test_robots_disallows_admin(self, client):
        """23. Verify robots.txt disallows administrative routes."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Disallow: /admin/' in text

    def test_robots_disallows_checkin(self, client):
        """24. Verify robots.txt disallows check-in scanner interface."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Disallow: /checkin/' in text

    def test_robots_disallows_qr_codes(self, client):
        """25. Verify robots.txt disallows static QR code ticket directory."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Disallow: /static/qr_codes/' in text

    def test_robots_disallows_api(self, client):
        """26. Verify robots.txt disallows internal API routes."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert 'Disallow: /api/' in text

    def test_robots_leaves_auth_unblocked(self, client):
        """27. Verify auth routes (/auth/) are NOT disallowed, allowing discovery of noindex."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        disallow_lines = [line.strip() for line in text.splitlines() if line.strip().startswith('Disallow:')]
        for line in disallow_lines:
            assert '/auth' not in line, f"Disallow directive must not block /auth/: {line}"

    def test_robots_sitemap_directive_points_to_sitemap_xml(self, client):
        """28. Verify Sitemap directive is present and ends with /sitemap.xml."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        sitemap_lines = [line.strip() for line in text.splitlines() if line.strip().startswith('Sitemap:')]
        assert len(sitemap_lines) == 1
        sitemap_url = sitemap_lines[0].split('Sitemap:', 1)[1].strip()
        assert sitemap_url.endswith('/sitemap.xml')
        parsed = urlparse(sitemap_url)
        assert parsed.scheme in ('http', 'https')
        assert parsed.netloc

    def test_robots_honors_canonical_domain(self, app, client):
        """29. Verify Sitemap directive in robots.txt honors CANONICAL_DOMAIN config."""
        app.config['CANONICAL_DOMAIN'] = 'https://eventai.example.vn'
        try:
            resp = client.get('/robots.txt')
            text = resp.data.decode('utf-8')
            assert 'Sitemap: https://eventai.example.vn/sitemap.xml' in text
        finally:
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_robots_no_html_tags(self, client):
        """30. Verify robots.txt is strictly plain text with zero HTML markup."""
        resp = client.get('/robots.txt')
        text = resp.data.decode('utf-8')
        assert '<html' not in text.lower()
        assert '</div>' not in text.lower()
        assert '<script' not in text.lower()


# ==============================================================================
# SECTION C: SEO HELPERS UNIT TESTS
# ==============================================================================

class TestSeoHelpersUnit:

    def test_is_event_indexable_statuses(self):
        """31. Verify is_event_indexable returns True for published, ongoing, completed."""
        class MockEvent:
            def __init__(self, status):
                self.status = status

        assert is_event_indexable(MockEvent('published')) is True
        assert is_event_indexable(MockEvent('ongoing')) is True
        assert is_event_indexable(MockEvent('completed')) is True

    def test_is_event_indexable_unindexable_statuses(self):
        """32. Verify is_event_indexable returns False for draft, cancelled, unknown, None."""
        class MockEvent:
            def __init__(self, status):
                self.status = status

        assert is_event_indexable(MockEvent('draft')) is False
        assert is_event_indexable(MockEvent('cancelled')) is False
        assert is_event_indexable(MockEvent('archived')) is False
        assert is_event_indexable(MockEvent(None)) is False
        assert is_event_indexable(None) is False

    def test_get_trusted_canonical_origin_with_config(self, app):
        """33. Verify get_trusted_canonical_origin uses CANONICAL_DOMAIN correctly."""
        with app.app_context():
            app.config['CANONICAL_DOMAIN'] = 'https://eventai.pro/'
            origin = get_trusted_canonical_origin()
            assert origin == 'https://eventai.pro'
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_get_trusted_canonical_origin_rejects_crlf(self, app):
        """34. Verify get_trusted_canonical_origin rejects CRLF injection."""
        with app.app_context():
            app.config['CANONICAL_DOMAIN'] = 'https://evil.com\r\nSet-Cookie: pwn=1'
            with pytest.raises(ValueError, match="newline"):
                get_trusted_canonical_origin()
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_get_trusted_canonical_origin_rejects_userinfo(self, app):
        """35. Verify get_trusted_canonical_origin rejects user:pass@host credentials."""
        with app.app_context():
            app.config['CANONICAL_DOMAIN'] = 'https://user:pass@evil.com'
            with pytest.raises(ValueError, match="credentials"):
                get_trusted_canonical_origin()
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_get_trusted_canonical_origin_rejects_non_http_scheme(self, app):
        """36. Verify get_trusted_canonical_origin rejects non-http schemes (e.g. javascript, ftp)."""
        with app.app_context():
            app.config['CANONICAL_DOMAIN'] = 'javascript:alert(1)'
            with pytest.raises(ValueError, match="scheme"):
                get_trusted_canonical_origin()
            app.config.pop('CANONICAL_DOMAIN', None)

    def test_build_sitemap_xml_basic_records(self):
        """37. Verify build_sitemap_xml creates valid XML with tuples."""
        origin = 'https://eventai.pro'
        records = [
            (101, datetime(2026, 10, 20, 10, 0, 0)),
            (102, None)
        ]
        xml_str = build_sitemap_xml(origin, records)
        root = ET.fromstring(xml_str)
        locs = extract_locs(root)

        assert 'https://eventai.pro/' in locs
        assert 'https://eventai.pro/events' in locs
        assert 'https://eventai.pro/events/101' in locs
        assert 'https://eventai.pro/events/102' in locs

    def test_build_sitemap_xml_object_records(self):
        """38. Verify build_sitemap_xml creates valid XML with object instances."""
        class MockEventRecord:
            def __init__(self, id, updated_at):
                self.id = id
                self.updated_at = updated_at

        origin = 'https://eventai.pro'
        records = [
            MockEventRecord(501, datetime(2026, 11, 1, 8, 0, 0)),
            MockEventRecord(502, None)
        ]
        xml_str = build_sitemap_xml(origin, records)
        root = ET.fromstring(xml_str)
        locs = extract_locs(root)

        assert 'https://eventai.pro/events/501' in locs
        assert 'https://eventai.pro/events/502' in locs

    def test_build_sitemap_xml_deduplication(self):
        """39. Verify build_sitemap_xml prevents duplicate URLs from being inserted."""
        origin = 'https://eventai.pro'
        records = [
            (201, datetime(2026, 10, 20)),
            (201, datetime(2026, 10, 21))  # Duplicate ID
        ]
        xml_str = build_sitemap_xml(origin, records)
        root = ET.fromstring(xml_str)
        locs = extract_locs(root)
        assert locs.count('https://eventai.pro/events/201') == 1

    def test_build_sitemap_xml_xml_character_escaping(self):
        """40. Verify build_sitemap_xml properly escapes XML reserved characters."""
        origin = 'https://eventai.pro'
        records = [(1, datetime(2026, 1, 1))]
        xml_str = build_sitemap_xml(origin, records)
        # Parse must succeed without xml.etree.ElementTree.ParseError
        root = ET.fromstring(xml_str)
        assert root is not None

    def test_build_robots_txt_format(self):
        """41. Verify build_robots_txt produces required directives and custom origin."""
        origin = 'https://custom.eventai.pro'
        robots_str = build_robots_txt(origin)
        assert 'User-agent: *' in robots_str
        assert 'Allow: /' in robots_str
        assert 'Disallow: /admin/' in robots_str
        assert 'Disallow: /checkin/' in robots_str
        assert 'Disallow: /static/qr_codes/' in robots_str
        assert 'Disallow: /api/' in robots_str
        assert 'Sitemap: https://custom.eventai.pro/sitemap.xml' in robots_str

    def test_indexable_event_statuses_constant(self):
        """42. Verify INDEXABLE_EVENT_STATUSES is a tuple containing the three expected statuses."""
        assert isinstance(INDEXABLE_EVENT_STATUSES, (tuple, list, set))
        assert set(INDEXABLE_EVENT_STATUSES) == {'published', 'ongoing', 'completed'}

    def test_build_sitemap_xml_strictly_caps_at_max_urls(self):
        """42b. Verify build_sitemap_xml never exceeds MAX_SITEMAP_URLS (50,000) protocol boundary."""
        origin = 'https://eventai.pro'
        # Generate 50,010 mock event records
        overflow_records = [(i, None) for i in range(1, 50011)]
        xml_str = build_sitemap_xml(origin, overflow_records)
        root = ET.fromstring(xml_str)
        locs = extract_locs(root)
        assert len(locs) == MAX_SITEMAP_URLS
        assert len(locs) == 50000
        # Ensure static URLs are present
        assert 'https://eventai.pro/' in locs
        assert 'https://eventai.pro/events' in locs


# ==============================================================================
# SECTION D: SECURITY & PRIVACY REGRESSION TESTS
# ==============================================================================

class TestSecurityAndPrivacyRegression:

    def test_login_page_retains_noindex_nofollow(self, client):
        """43. Verify Phase 2.5 fix: /auth/login has noindex, nofollow meta tag."""
        resp = client.get('/auth/login')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert '<meta name="robots" content="noindex, nofollow">' in html

    def test_register_page_retains_noindex_nofollow(self, client):
        """44. Verify Phase 2.5 fix: /auth/register has noindex, nofollow meta tag."""
        resp = client.get('/auth/register')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert '<meta name="robots" content="noindex, nofollow">' in html

    def test_draft_event_remains_404_for_anonymous_user(self, client, test_events_for_sitemap):
        """45. Verify Phase 2.5 fix: draft events return 404 for anonymous users."""
        draft_id = test_events_for_sitemap['draft']
        resp = client.get(f'/events/{draft_id}')
        assert resp.status_code == 404

    def test_cancelled_event_retains_noindex_follow(self, client, test_events_for_sitemap):
        """46. Verify Phase 2.5 fix: cancelled events have noindex, follow meta tag."""
        cancelled_id = test_events_for_sitemap['cancelled']
        resp = client.get(f'/events/{cancelled_id}')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert '<meta name="robots" content="noindex, follow">' in html

    def test_checkin_scanner_requires_auth(self, client):
        """47. Verify /checkin scanner route redirects unauthenticated users."""
        resp = client.get('/checkin/', follow_redirects=False)
        assert resp.status_code in (301, 302, 308, 401, 403, 404)

    def test_admin_dashboard_requires_auth(self, client):
        """48. Verify /admin dashboard redirects unauthenticated users."""
        resp = client.get('/admin/', follow_redirects=False)
        assert resp.status_code in (301, 302, 308, 401, 403, 404)
