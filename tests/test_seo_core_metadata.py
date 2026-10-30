"""
Targeted Core SEO and Metadata regression tests for Phase 3A implementation.
Verifies dynamic titles, meta descriptions, canonical URLs, Open Graph / Twitter Card tags,
semantic heading hierarchy (H1 -> H2 -> H3), parameter stripping, and security baseline preservation.
Uses standard library HTMLParser to avoid introducing third-party dependencies.
"""
import re
from html.parser import HTMLParser
import pytest
from app.extensions import db, utc_now
from app.models import Event, User, Ticket


class TagNode:
    """Represents an HTML tag node parsed by SimpleHTMLDoc."""
    def __init__(self, tag, attrs):
        self.tag = tag.lower()
        self.attrs = {k.lower(): v for k, v in attrs}
        self.text_parts = []

    @property
    def text(self):
        return ''.join(self.text_parts).strip()

    def get(self, attr_name, default=None):
        return self.attrs.get(attr_name.lower(), default)

    def __getitem__(self, item):
        return self.attrs[item.lower()]


class SimpleHTMLDoc(HTMLParser):
    """Lightweight zero-dependency HTML document parser based on Python's standard library."""
    def __init__(self, html_content):
        super().__init__()
        self.all_nodes = []
        self.stack = []
        self.feed(html_content)

    def handle_starttag(self, tag, attrs):
        node = TagNode(tag, attrs)
        self.all_nodes.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag_lower:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        for node in self.stack:
            node.text_parts.append(data)

    def find(self, tag, attrs=None):
        tag_lower = tag.lower()
        for node in self.all_nodes:
            if node.tag == tag_lower:
                if attrs:
                    if all(node.attrs.get(k.lower()) == v for k, v in attrs.items()):
                        return node
                else:
                    return node
        return None

    def find_all(self, tag, attrs=None):
        tag_lower = tag.lower()
        results = []
        for node in self.all_nodes:
            if node.tag == tag_lower:
                if attrs:
                    if all(node.attrs.get(k.lower()) == v for k, v in attrs.items()):
                        results.append(node)
                else:
                    results.append(node)
        return results


@pytest.fixture
def test_event(app, sample_users):
    """Fixture providing a published sample event."""
    with app.app_context():
        event = Event(
            event_code='EVT-SEO-2026-001',
            title='Diễn Đàn Trí Tuệ Nhân Tạo & "Machine Learning" 2026',
            description='<p>Khám phá <strong>xu hướng công nghệ AI</strong> tiên tiến nhất với các chuyên gia đầu ngành & giải pháp thực tiễn.</p>',
            category='Công nghệ & AI',
            banner_url='https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200',
            start_date=utc_now(),
            end_date=utc_now(),
            location_type='offline',
            location_address='Trung tâm Hội nghị Quốc gia, Hà Nội',
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


@pytest.fixture
def long_desc_event(app, sample_users):
    """Fixture providing an event with very long description for truncation testing."""
    with app.app_context():
        long_text = (
            "Hội nghị cấp cao toàn cầu về chuyển đổi số và ứng dụng trí tuệ nhân tạo trong các ngành kinh tế trọng điểm. "
            "Sự kiện quy tụ hơn 50 diễn giả quốc tế, 100 gian hàng công nghệ và hàng ngàn đại biểu tham dự từ khắp nơi trên thế giới. "
            "Chương trình bao gồm các phiên tọa đàm chuyên sâu, thảo luận bàn tròn và kết nối đầu tư khởi nghiệp công nghệ cao."
        )
        event = Event(
            event_code='EVT-SEO-LONG-002',
            title='Hội Nghị Chuyển Đổi Số Toàn Cầu 2026',
            description=long_text,
            category='Chuyển đổi số',
            banner_url='/static/uploads/global-summit.jpg',
            start_date=utc_now(),
            end_date=utc_now(),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


@pytest.fixture
def empty_desc_event(app, sample_users):
    """Fixture providing an event with empty description for fallback testing."""
    with app.app_context():
        event = Event(
            event_code='EVT-SEO-EMPTY-003',
            title='Hội Thảo Lập Trình Python Căn Bản',
            description='',
            category='Workshop',
            banner_url=None,
            start_date=utc_now(),
            end_date=utc_now(),
            status='published',
            created_by=sample_users['admin_id']
        )
        db.session.add(event)
        db.session.commit()
        return event.id


# ==============================================================================
# 1. HOMEPAGE SEO TESTS
# ==============================================================================

def test_homepage_title_and_description(client):
    """Verify homepage title and meta description are rendered and non-empty."""
    res = client.get('/')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    title = doc.find('title')
    assert title is not None
    assert 'EventAI Pro' in title.text
    assert 'Nền Tảng Quản Lý' in title.text

    desc = doc.find('meta', {'name': 'description'})
    assert desc is not None
    assert desc.get('content')
    assert 'EventAI Pro' in desc['content']
    assert len(desc['content']) > 20


def test_homepage_canonical_url(client):
    """Verify homepage has an absolute canonical URL pointing to /."""
    res = client.get('/')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    canonical = doc.find('link', {'rel': 'canonical'})
    assert canonical is not None
    href = canonical.get('href')
    assert href.startswith('http://') or href.startswith('https://')
    assert href.endswith('/')


def test_homepage_og_and_twitter_cards(client):
    """Verify Open Graph and Twitter Card tags on homepage."""
    res = client.get('/')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    # Open Graph
    assert doc.find('meta', {'property': 'og:type'})['content'] == 'website'
    assert doc.find('meta', {'property': 'og:site_name'})['content'] == 'EventAI Pro'
    assert 'EventAI Pro' in doc.find('meta', {'property': 'og:title'})['content']
    assert doc.find('meta', {'property': 'og:description'})['content'] != ''
    assert doc.find('meta', {'property': 'og:locale'})['content'] == 'vi_VN'
    og_img = doc.find('meta', {'property': 'og:image'})['content']
    assert og_img.startswith('http://') or og_img.startswith('https://')

    # Twitter Card
    assert doc.find('meta', {'name': 'twitter:card'})['content'] == 'summary_large_image'
    assert 'EventAI Pro' in doc.find('meta', {'name': 'twitter:title'})['content']
    assert doc.find('meta', {'name': 'twitter:image'})['content'] == og_img


# ==============================================================================
# 2. EVENTS LISTING PAGE SEO TESTS
# ==============================================================================

def test_events_page_title_and_description(client):
    """Verify events catalog page has dynamic title and meta description."""
    res = client.get('/events')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    title = doc.find('title')
    assert title is not None
    assert 'Danh Sách Sự Kiện' in title.text
    assert 'EventAI Pro' in title.text

    desc = doc.find('meta', {'name': 'description'})
    assert desc is not None
    assert 'hội thảo công nghệ' in desc['content'].lower() or 'sự kiện' in desc['content'].lower()


def test_events_page_canonical_url(client):
    """Verify events catalog page canonical tag points to /events."""
    res = client.get('/events')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    canonical = doc.find('link', {'rel': 'canonical'})
    assert canonical is not None
    assert canonical['href'].endswith('/events')


def test_events_page_strips_tracking_parameters(client):
    """Verify tracking parameters (utm_*, fbclid, ref) are stripped from canonical URL."""
    res = client.get('/events?utm_source=facebook&utm_medium=cpc&utm_campaign=spring2026&fbclid=IwAR0123&ref=banner')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    canonical = doc.find('link', {'rel': 'canonical'})
    assert canonical is not None
    href = canonical['href']
    assert 'utm_source' not in href
    assert 'utm_medium' not in href
    assert 'utm_campaign' not in href
    assert 'fbclid' not in href
    assert 'ref=' not in href
    assert href.endswith('/events')


# ==============================================================================
# 3. EVENT DETAIL PAGE SEO TESTS
# ==============================================================================

def test_event_detail_dynamic_metadata(client, test_event):
    """Verify dynamic title, meta description, and canonical URL on event detail."""
    res = client.get(f'/events/{test_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    title = doc.find('title')
    assert title is not None
    assert 'Diễn Đàn Trí Tuệ Nhân Tạo' in title.text
    assert 'EventAI Pro' in title.text

    desc = doc.find('meta', {'name': 'description'})
    assert desc is not None
    assert 'xu hướng công nghệ AI' in desc['content']


def test_event_detail_meta_description_html_stripping(client, test_event):
    """Verify HTML tags (<p>, <strong>) are completely stripped from meta description."""
    res = client.get(f'/events/{test_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    desc = doc.find('meta', {'name': 'description'})['content']
    assert '<p>' not in desc
    assert '</p>' not in desc
    assert '<strong>' not in desc
    assert '</strong>' not in desc
    assert 'xu hướng công nghệ AI' in desc

    og_desc = doc.find('meta', {'property': 'og:description'})['content']
    assert '<p>' not in og_desc
    assert '<strong>' not in og_desc


def test_event_detail_meta_description_truncation(client, long_desc_event):
    """Verify long descriptions are truncated cleanly with word boundary and ellipsis."""
    res = client.get(f'/events/{long_desc_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    desc = doc.find('meta', {'name': 'description'})['content']
    assert len(desc) <= 160
    assert desc.endswith('...')


def test_event_detail_meta_description_fallback(client, empty_desc_event):
    """Verify event with empty description falls back to event title or platform description."""
    res = client.get(f'/events/{empty_desc_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    desc = doc.find('meta', {'name': 'description'})['content']
    assert desc != ''
    assert len(desc) > 10


def test_event_detail_canonical_url(client, test_event):
    """Verify canonical URL points to /events/<id>."""
    res = client.get(f'/events/{test_event}?utm_source=email&ref=newsletter')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    canonical = doc.find('link', {'rel': 'canonical'})
    assert canonical is not None
    assert canonical['href'].endswith(f'/events/{test_event}')
    assert 'utm_source' not in canonical['href']


def test_event_detail_og_type_and_image(client, test_event):
    """Verify Open Graph type is article and image is formatted as absolute URL."""
    res = client.get(f'/events/{test_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    og_type = doc.find('meta', {'property': 'og:type'})
    assert og_type['content'] == 'article'

    og_img = doc.find('meta', {'property': 'og:image'})['content']
    assert og_img.startswith('https://images.unsplash.com')

    tw_img = doc.find('meta', {'name': 'twitter:image'})['content']
    assert tw_img == og_img


def test_event_detail_relative_image_is_made_absolute(client, long_desc_event):
    """Verify relative banner URLs are converted to absolute URLs in og:image."""
    res = client.get(f'/events/{long_desc_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    og_img = doc.find('meta', {'property': 'og:image'})['content']
    assert og_img.startswith('http://') or og_img.startswith('https://')
    assert '/static/uploads/global-summit.jpg' in og_img


def test_event_detail_fallback_og_image(client, empty_desc_event):
    """Verify event without banner falls back to default high-res banner image."""
    res = client.get(f'/events/{empty_desc_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    og_img = doc.find('meta', {'property': 'og:image'})['content']
    assert og_img.startswith('http://') or og_img.startswith('https://')


# ==============================================================================
# 4. CANONICAL DOMAIN OVERRIDE
# ==============================================================================

def test_canonical_domain_configuration_override(app, client, test_event):
    """Verify CANONICAL_DOMAIN setting is honored in canonical and og:url tags."""
    app.config['CANONICAL_DOMAIN'] = 'https://eventai.pro'
    res = client.get(f'/events/{test_event}?ref=ad')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    canonical = doc.find('link', {'rel': 'canonical'})
    assert canonical['href'] == f'https://eventai.pro/events/{test_event}'

    og_url = doc.find('meta', {'property': 'og:url'})
    assert og_url['content'] == f'https://eventai.pro/events/{test_event}'


# ==============================================================================
# 5. SPECIAL CHARACTER & ATTRIBUTE ESCAPING
# ==============================================================================

def test_special_characters_in_metadata_are_escaped(client, test_event):
    """Verify quotes and ampersands in titles do not break HTML attribute syntax."""
    res = client.get(f'/events/{test_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    og_title = doc.find('meta', {'property': 'og:title'})
    assert og_title is not None
    assert 'Machine Learning' in og_title['content']


# ==============================================================================
# 6. NO DUPLICATE TAGS CHECK
# ==============================================================================

def test_no_duplicate_metadata_tags(client, test_event):
    """Verify exactly one title, description, and canonical tag exist on all main views."""
    for url in ['/', '/events', f'/events/{test_event}']:
        res = client.get(url)
        assert res.status_code == 200
        doc = SimpleHTMLDoc(res.data.decode('utf-8'))

        titles = doc.find_all('title')
        assert len(titles) == 1, f"Duplicate <title> found on {url}"

        descriptions = doc.find_all('meta', {'name': 'description'})
        assert len(descriptions) == 1, f"Duplicate meta description found on {url}"

        canonicals = doc.find_all('link', {'rel': 'canonical'})
        assert len(canonicals) == 1, f"Duplicate canonical found on {url}"

        og_titles = doc.find_all('meta', {'property': 'og:title'})
        assert len(og_titles) == 1, f"Duplicate og:title found on {url}"

        tw_titles = doc.find_all('meta', {'name': 'twitter:title'})
        assert len(tw_titles) == 1, f"Duplicate twitter:title found on {url}"


# ==============================================================================
# 7. SEMANTIC HEADING HIERARCHY TESTS (H1 -> H2 -> H3)
# ==============================================================================

def test_homepage_semantic_heading_hierarchy(client):
    """Verify homepage has exactly ONE <h1> and sub-headings are <h2>."""
    res = client.get('/')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    h1_tags = doc.find_all('h1')
    assert len(h1_tags) == 1, f"Homepage must have exactly one <h1>, found {len(h1_tags)}"
    assert 'Trải Nghiệm Sự Kiện' in h1_tags[0].text

    h2_tags = doc.find_all('h2')
    assert len(h2_tags) >= 2, "Homepage must have at least 2 <h2> sub-headings"


def test_events_page_semantic_heading_hierarchy(client):
    """Verify events catalog page has exactly ONE <h1>."""
    res = client.get('/events')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    h1_tags = doc.find_all('h1')
    assert len(h1_tags) == 1, f"Events page must have exactly one <h1>, found {len(h1_tags)}"
    assert 'Tất Cả Sự Kiện' in h1_tags[0].text


def test_event_detail_semantic_heading_hierarchy(client, test_event):
    """Verify event detail page has exactly ONE <h1> matching the event title."""
    res = client.get(f'/events/{test_event}')
    assert res.status_code == 200
    doc = SimpleHTMLDoc(res.data.decode('utf-8'))

    h1_tags = doc.find_all('h1')
    assert len(h1_tags) == 1, f"Event detail must have exactly one <h1>, found {len(h1_tags)}"
    assert 'Diễn Đàn Trí Tuệ Nhân Tạo' in h1_tags[0].text

    # Section headings must be h2
    h2_tags = doc.find_all('h2')
    h2_texts = [h.text for h in h2_tags]
    assert any('Giới Thiệu Sự Kiện' in t for t in h2_texts)
    assert any('Lịch Trình Chi Tiết' in t for t in h2_texts)
    assert any('Chọn Hạng Vé' in t for t in h2_texts)


# ==============================================================================
# 8. SECURITY BASELINE PRESERVATION TESTS
# ==============================================================================

def test_security_baseline_auth_and_errors_retain_noindex(client):
    """Verify auth and 404 views retain noindex directives from Phase 2.5."""
    res_login = client.get('/auth/login')
    assert res_login.status_code == 200
    assert '<meta name="robots" content="noindex, nofollow">' in res_login.data.decode('utf-8')

    res_reg = client.get('/auth/register')
    assert res_reg.status_code == 200
    assert '<meta name="robots" content="noindex, nofollow">' in res_reg.data.decode('utf-8')

    res_404 = client.get('/non-existent-page-xyz-404')
    assert res_404.status_code == 404
    assert '<meta name="robots" content="noindex, nofollow">' in res_404.data.decode('utf-8')


def test_security_baseline_draft_event_is_protected(client, app, sample_users):
    """Verify unpublished draft events remain inaccessible to anonymous users and have noindex for previewers."""
    with app.app_context():
        draft_event = Event(
            event_code='EVT-SEO-DRAFT-099',
            title='Confidential Strategy Summit',
            start_date=utc_now(),
            end_date=utc_now(),
            status='draft',
            created_by=sample_users['admin_id']
        )
        db.session.add(draft_event)
        db.session.commit()
        draft_id = draft_event.id

    # Anonymous user -> 404
    res_anon = client.get(f'/events/{draft_id}')
    assert res_anon.status_code == 404

    # Admin user -> 200 preview with noindex
    client.post('/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    res_admin = client.get(f'/events/{draft_id}')
    assert res_admin.status_code == 200
    assert '<meta name="robots" content="noindex, follow">' in res_admin.data.decode('utf-8')


def test_security_baseline_private_qr_remains_blocked(client):
    """Verify unauthenticated users cannot access private QR code files."""
    res = client.get('/static/qr_codes/TCK-TEST-999-ABCDEF.svg')
    assert res.status_code == 403
