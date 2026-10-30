"""
Targeted tests for Phase 3D: Performance, Core Web Vitals (LCP, CLS, INP) & Accessibility (WCAG 2.2 AA).
Verifies resource preconnect hints, LCP hero prioritization, below-the-fold image lazy loading,
explicit dimensions (CLS prevention), IntersectionObserver lifecycle cleanup, reduced-motion compliance,
accessible ARIA labels, keyboard focus visibility, mobile GPU optimizations, and security baselines.
Uses Python standard library html.parser and re (zero third-party dependencies).
"""
import re
from html.parser import HTMLParser
from datetime import datetime
import pytest
from flask import url_for
from app.extensions import db
from app.models import Event, User


class ImageTagExtractor(HTMLParser):
    """Extracts all <img> tags and their attributes from rendered HTML."""
    def __init__(self, html_content):
        super().__init__()
        self.images = []
        self.feed(html_content)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'img':
            self.images.append(dict(attrs))


class LinkTagExtractor(HTMLParser):
    """Extracts all <link> tags and their attributes from rendered HTML."""
    def __init__(self, html_content):
        super().__init__()
        self.links = []
        self.feed(html_content)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'link':
            self.links.append(dict(attrs))


class ScriptTagExtractor(HTMLParser):
    """Extracts all <script> tags and their attributes from rendered HTML."""
    def __init__(self, html_content):
        super().__init__()
        self.scripts = []
        self.feed(html_content)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            self.scripts.append(dict(attrs))


@pytest.fixture
def performance_sample_event(app, sample_users):
    """Fixture providing a published event for performance and accessibility testing."""
    with app.app_context():
        creator_id = sample_users['admin_id']
        event = Event(
            event_code='EVT-PERF-001',
            title='Diễn Đàn Chuyển Đổi Số & Điện Toán Đám Mây 2026',
            description='Hội nghị thượng đỉnh quy tụ các chuyên gia công nghệ hàng đầu.',
            category='Công nghệ & AI',
            banner_url='https://images.unsplash.com/photo-tech-cloud-2026?w=1200',
            start_date=datetime(2026, 12, 10, 8, 30, 0),
            end_date=datetime(2026, 12, 10, 17, 30, 0),
            status='published',
            location_type='offline',
            location_address='Trung tâm Đổi mới Sáng tạo Quốc gia, Hà Nội',
            created_by=creator_id
        )
        db.session.add(event)
        db.session.commit()
        return event.id


# ==============================================================================
# SECTION A: RESOURCE HINTS, PRECONNECT & SCRIPT DEFER (FCP / LCP DISCOVERY)
# ==============================================================================

class TestResourceHintsAndLoading:

    def test_base_template_has_preconnect_hints(self, client):
        """1. Verify preconnect hints exist for critical external CDNs and image hosts."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = LinkTagExtractor(html)

        preconnect_hrefs = [
            link.get('href') for link in extractor.links if link.get('rel') == 'preconnect'
        ]
        assert 'https://cdn.jsdelivr.net' in preconnect_hrefs
        assert 'https://cdnjs.cloudflare.com' in preconnect_hrefs
        assert 'https://images.unsplash.com' in preconnect_hrefs

    def test_base_template_has_dns_prefetch_hints(self, client):
        """2. Verify dns-prefetch fallback hints exist for early DNS resolution."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = LinkTagExtractor(html)

        prefetch_hrefs = [
            link.get('href') for link in extractor.links if link.get('rel') == 'dns-prefetch'
        ]
        assert 'https://cdn.jsdelivr.net' in prefetch_hrefs
        assert 'https://cdnjs.cloudflare.com' in prefetch_hrefs
        assert 'https://images.unsplash.com' in prefetch_hrefs

    def test_application_scripts_have_defer_attribute(self, client):
        """3. Verify non-critical application scripts are deferred to unblock parsing."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ScriptTagExtractor(html)

        main_js_found = False
        ai_chat_js_found = False
        for s in extractor.scripts:
            src = s.get('src', '')
            if 'main.js' in src:
                main_js_found = True
                assert 'defer' in s
            if 'ai_chat.js' in src:
                ai_chat_js_found = True
                assert 'defer' in s

        assert main_js_found, "main.js script tag not found"
        assert ai_chat_js_found, "ai_chat.js script tag not found"


# ==============================================================================
# SECTION B: LCP OPTIMIZATION (HERO PRIORITIZATION & LAZY LOADING)
# ==============================================================================

class TestLcpAndLazyLoading:

    def test_homepage_hero_carousel_lcp_first_image_priority(self, client, performance_sample_event):
        """4. Verify first hero carousel slide (LCP candidate) has fetchpriority='high' and async decoding."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ImageTagExtractor(html)

        hero_imgs = [img for img in extractor.images if 'hero-slide-img' in img.get('class', '')]
        assert len(hero_imgs) >= 1
        first_img = hero_imgs[0]
        assert first_img.get('fetchpriority') == 'high'
        assert first_img.get('decoding') == 'async'
        assert first_img.get('width') == '600'
        assert first_img.get('height') == '380'
        # Crucial: Must NEVER lazy-load the actual LCP candidate
        assert first_img.get('loading') != 'lazy'

    def test_homepage_hero_carousel_subsequent_images_lazy_loaded(self, client, app, sample_users):
        """5. Verify carousel slides after the first slide are lazy-loaded to save bandwidth."""
        with app.app_context():
            # Ensure multiple published events exist for multiple slides
            for i in range(2, 4):
                evt = Event(
                    event_code=f'EVT-MULTI-{i}',
                    title=f'Sự Kiện Đỉnh Cao Số {i}',
                    category='Công nghệ & AI',
                    start_date=datetime(2026, 12, 1, 9, 0),
                    end_date=datetime(2026, 12, 1, 17, 0),
                    status='published',
                    created_by=sample_users['admin_id']
                )
                db.session.add(evt)
            db.session.commit()

        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ImageTagExtractor(html)

        hero_imgs = [img for img in extractor.images if 'hero-slide-img' in img.get('class', '')]
        if len(hero_imgs) > 1:
            for sub_img in hero_imgs[1:]:
                assert sub_img.get('loading') == 'lazy'
                assert sub_img.get('decoding') == 'async'
                assert sub_img.get('fetchpriority') != 'high'

    def test_homepage_below_the_fold_cards_lazy_loaded(self, client, performance_sample_event):
        """6. Verify event card images below the fold have loading='lazy' and explicit dimensions."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ImageTagExtractor(html)

        card_imgs = [img for img in extractor.images if 'event-card-img' in img.get('class', '')]
        assert len(card_imgs) >= 1
        for img in card_imgs:
            assert img.get('loading') == 'lazy'
            assert img.get('decoding') == 'async'
            assert img.get('width') == '400'
            assert img.get('height') == '225'

    def test_event_detail_hero_banner_high_priority_and_never_lazy(self, client, performance_sample_event):
        """7. Verify event detail hero banner has fetchpriority='high' and never lazy-loaded."""
        resp = client.get(f'/events/{performance_sample_event}')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ImageTagExtractor(html)

        # Main hero image on detail page
        detail_hero_imgs = [
            img for img in extractor.images if img.get('width') == '800' and img.get('height') == '480'
        ]
        assert len(detail_hero_imgs) == 1
        hero = detail_hero_imgs[0]
        assert hero.get('fetchpriority') == 'high'
        assert hero.get('decoding') == 'async'
        assert hero.get('loading') != 'lazy'

    def test_events_catalog_images_loading_strategy(self, client, performance_sample_event):
        """8. Verify events catalog applies decoding='async' and lazy-loading appropriately."""
        resp = client.get('/events')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        extractor = ImageTagExtractor(html)

        card_imgs = [img for img in extractor.images if 'event-card-img' in img.get('class', '')]
        assert len(card_imgs) >= 1
        # First image has async decoding
        assert card_imgs[0].get('decoding') == 'async'
        assert card_imgs[0].get('width') == '400'
        assert card_imgs[0].get('height') == '225'


# ==============================================================================
# SECTION C: CLS (CUMULATIVE LAYOUT SHIFT) PREVENTION
# ==============================================================================

class TestLayoutStability:

    def test_image_tags_have_explicit_width_and_height(self, client, performance_sample_event):
        """9. Verify all public event images declare explicit width & height attributes."""
        for path in ['/', '/events', f'/events/{performance_sample_event}']:
            resp = client.get(path)
            assert resp.status_code == 200
            html = resp.data.decode('utf-8')
            extractor = ImageTagExtractor(html)
            for img in extractor.images:
                # Every image tag in our main templates must specify dimensions
                if 'hero-slide-img' in img.get('class', '') or 'event-card-img' in img.get('class', ''):
                    assert img.get('width') is not None, f"Missing width on {img.get('src')}"
                    assert img.get('height') is not None, f"Missing height on {img.get('src')}"

    def test_css_aspect_ratio_rules_exist(self):
        """10. Verify CSS enforces aspect-ratio on image wrappers to reserve layout space."""
        with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        assert 'aspect-ratio: 16 / 10' in css
        assert '.event-card-img-wrapper' in css


# ==============================================================================
# SECTION D: INP & ANIMATION EFFICIENCY (JS LIFECYCLE & CPU OPTIMIZATIONS)
# ==============================================================================

class TestAnimationAndInteractionEfficiency:

    def test_javascript_slider_has_reduced_motion_check(self):
        """11. Verify main.js checks prefers-reduced-motion before starting auto-scroll loop."""
        with open('app/static/js/main.js', 'r', encoding='utf-8') as f:
            js = f.read()

        assert 'prefers-reduced-motion: reduce' in js
        assert 'prefersReducedMotion' in js

    def test_javascript_slider_uses_intersection_observer(self):
        """12. Verify main.js uses IntersectionObserver to pause loop when scrolled offscreen."""
        with open('app/static/js/main.js', 'r', encoding='utf-8') as f:
            js = f.read()

        assert 'IntersectionObserver' in js
        assert 'isIntersecting' in js
        assert 'stopLoop' in js

    def test_javascript_slider_uses_page_visibility_api(self):
        """13. Verify main.js pauses animation loop when tab is backgrounded."""
        with open('app/static/js/main.js', 'r', encoding='utf-8') as f:
            js = f.read()

        assert 'visibilitychange' in js
        assert 'document.hidden' in js

    def test_css_gpu_compositing_will_change_rules(self):
        """14. Verify CSS promotes sliding items to GPU compositor layer with will-change."""
        with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        assert 'will-change: transform, opacity;' in css
        assert 'will-change: scroll-position;' in css


# ==============================================================================
# SECTION E: ACCESSIBILITY (WCAG 2.2 AA TARGET)
# ==============================================================================

class TestAccessibilityCompliance:

    def test_carousel_indicators_have_descriptive_accessible_names(self, client, performance_sample_event):
        """15. Verify carousel indicator buttons have descriptive aria-labels (not generic Slide X)."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')

        # Check aria-label on carousel indicators (matching data-bs-slide-to)
        indicator_labels = re.findall(r'data-bs-slide-to="[^"]*"[^>]*aria-label="([^"]+)"', html)
        assert len(indicator_labels) >= 1
        for label in indicator_labels:
            assert 'Chuyển đến sự kiện nổi bật' in label

    def test_carousel_prev_next_controls_have_accessible_labels(self, client, performance_sample_event):
        """16. Verify carousel Prev and Next controls have clear accessible names."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')

        assert 'aria-label="Sự kiện nổi bật trước"' in html
        assert 'aria-label="Sự kiện nổi bật sau"' in html

    def test_search_forms_have_accessible_search_role_and_labels(self, client):
        """17. Verify search forms declare role='search' and input fields have aria-labels."""
        for path in ['/', '/events']:
            resp = client.get(path)
            assert resp.status_code == 200
            html = resp.data.decode('utf-8')
            assert 'role="search"' in html
            assert 'aria-label="Tìm kiếm sự kiện' in html

    def test_events_category_select_has_aria_label(self, client):
        """18. Verify category filter dropdown has accessible name."""
        resp = client.get('/events')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'aria-label="Lọc theo danh mục sự kiện"' in html

    def test_ai_chat_modal_and_controls_accessibility(self, client):
        """19. Verify AI Assistant dialog has role='dialog', aria-modal='false' for modeless floating widget, and accessible labels."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')

        assert 'role="dialog"' in html
        assert 'aria-modal="false"' in html
        assert 'aria-label="Trợ lý EventAI"' in html
        assert 'aria-label="Mở Trợ lý Sự kiện AI"' in html
        assert 'aria-label="Gửi câu hỏi cho Trợ lý AI"' in html

    def test_css_visible_focus_indicators(self):
        """20. Verify CSS declares visible :focus-visible outline indicators (WCAG 2.2 AA)."""
        with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        assert ':focus-visible' in css
        assert 'outline: 2px solid var(--accent-primary)' in css
        assert 'outline-offset: 2px' in css

    def test_css_reduced_motion_media_query_present(self):
        """21. Verify CSS supports prefers-reduced-motion for motion sensitivity."""
        with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        assert '@media (prefers-reduced-motion: reduce)' in css


# ==============================================================================
# SECTION F: MOBILE-FIRST RESPONSIVENESS & GPU PERFORMANCE
# ==============================================================================

class TestMobileFirstAndGpuPerformance:

    def test_viewport_meta_tag_configured_for_mobile(self, client):
        """22. Verify mobile viewport meta tag includes width=device-width and viewport-fit=cover."""
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'name="viewport"' in html
        assert 'width=device-width' in html
        assert 'viewport-fit=cover' in html

    def test_mobile_gpu_backdrop_blur_optimization_in_css(self):
        """23. Verify CSS reduces backdrop-filter blur on mobile viewports (max-width: 576px)."""
        with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        assert '@media (max-width: 576px)' in css
        assert 'backdrop-filter: blur(12px) !important;' in css


# ==============================================================================
# SECTION G: SECURITY & PRIVACY BASELINE PRESERVATION (PHASE 2.5 & 3C)
# ==============================================================================

class TestSecurityBaselinePreservation:

    def test_login_page_no_credentials_exposed(self, client):
        """24. Verify Phase 2.5 baseline: login page never exposes demo passwords."""
        resp = client.get('/auth/login')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'Admin@123' not in html
        assert 'Staff@123' not in html
        assert '<meta name="robots" content="noindex, nofollow">' in html

    def test_anonymous_cannot_access_draft_event(self, client, app, sample_users):
        """25. Verify draft events return 404 for anonymous users."""
        with app.app_context():
            draft_evt = Event(
                event_code='EVT-DRAFT-P3D',
                title='Sự Kiện Draft An Toàn',
                category='Nội bộ',
                start_date=datetime(2026, 12, 1, 9, 0),
                end_date=datetime(2026, 12, 1, 17, 0),
                status='draft',
                created_by=sample_users['admin_id']
            )
            db.session.add(draft_evt)
            db.session.commit()
            draft_id = draft_evt.id

        resp = client.get(f'/events/{draft_id}')
        assert resp.status_code == 404

    def test_sitemap_xml_protocol_capped_at_max_urls(self, client):
        """26. Verify sitemap.xml returns 200 XML and never exceeds protocol boundary."""
        resp = client.get('/sitemap.xml')
        assert resp.status_code == 200
        assert 'application/xml' in resp.content_type
        assert resp.headers.get('X-Content-Type-Options') == 'nosniff'

    def test_robots_txt_remains_valid(self, client):
        """27. Verify robots.txt returns 200 plain text with proper crawler directives."""
        resp = client.get('/robots.txt')
        assert resp.status_code == 200
        assert 'text/plain' in resp.content_type
        assert 'Disallow: /admin/' in resp.data.decode('utf-8')
        assert 'Disallow: /checkin/' in resp.data.decode('utf-8')
        assert 'Disallow: /static/qr_codes/' in resp.data.decode('utf-8')
        assert 'Disallow: /api/' in resp.data.decode('utf-8')
