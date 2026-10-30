# EventAI Pro — Phase 8: Session Integrity & CSRF Token Cache Isolation Audit

**Status**: HARDENED & VERIFIED  
**Auditor**: HTTP Infrastructure & Web Security Architect  
**Scope**: HTTP Caching Headers (`Cache-Control`, `Vary`, `Pragma`, `Expires`), Reverse Proxy / CDN Behavior, and CSRF Token Isolation  
**Reference Standards**: RFC 9111 (HTTP Caching), OWASP ASVS v4.0.3  

---

## 1. Verified Facts & Prior Phase Audit

In Phase 7, response caching was enhanced to protect authenticated sessions. However, a deeper architectural inspection revealed a subtle caching hazard:
- **Prior Implementation**: In `app/__init__.py`, `Cache-Control: private, no-cache, no-store, must-revalidate` was gated behind `if current_user.is_authenticated:`.
- **Identified Risk**: In `app/templates/base.html`, the line `<meta name="csrf-token" content="{{ csrf_token() }}">` is rendered for **every** HTML page, including public pages visited by anonymous users (e.g., `/`, `/events`, `/auth/login`, `/auth/register`). When an anonymous user visits, Flask-WTF generates a session-specific CSRF token bound to their anonymous session cookie.
- **Cache Poisoning Hazard**: If an intermediate caching proxy (Cloudflare, Varnish, Nginx, or an ISP cache) were to store an anonymous HTML page, a subsequent anonymous user could receive User A's cached HTML containing User A's session CSRF token. Any state-changing form or chat submission by User B would fail with HTTP 400 (`The CSRF tokens do not match.`).

---

## 2. Fixed Defect & Comprehensive Cache Isolation Architecture

### 2.1 Universal HTML Non-Cacheability (`app/__init__.py`)
Because all HTML documents in EventAI Pro render `base.html` and embed an active session CSRF token, all HTML responses must be strictly marked as non-cacheable by intermediate proxies:

```python
elif response.mimetype == 'text/html':
    # 1. Enforce downstream proxy differentiation by Cookie
    existing_vary = response.headers.get('Vary', '')
    if 'Cookie' not in existing_vary:
        response.headers['Vary'] = f"{existing_vary}, Cookie".strip(', ')
        
    # 2. Prevent shared proxy / CDN caching for ALL HTML documents containing CSRF tokens
    response.headers['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
```

### 2.2 Preservation of Static Asset Performance
A critical requirement of Phase 8 was ensuring that performance optimizations from Phase 3D are preserved. The `response.mimetype == 'text/html'` condition guarantees that non-HTML assets are completely untouched:
- **CSS Stylesheets** (`mimetype='text/css'`): Retain high-performance browser and CDN caching.
- **JavaScript Bundles** (`mimetype='application/javascript'`): Cached aggressively for sub-second loads.
- **Images & Icons** (`mimetype='image/png'`, `'image/svg+xml'`, `'image/webp'`): Full caching preserved.
- **Search Engine Sitemaps** (`mimetype='application/xml'`): Cacheable; zero tokens injected.
- **Robots Directives** (`mimetype='text/plain'`): Cacheable; zero tokens injected.

---

## 3. Comprehensive Caching Policy Matrix

| Response Category | Typical Path | Mime-Type | `Vary` Header | `Cache-Control` Policy | Security & Performance Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Anonymous HTML** | `/`<br>`/events`<br>`/auth/login` | `text/html` | `Cookie` | `private, no-cache, no-store, must-revalidate` | **Secured**: Session-specific CSRF meta tag cannot be cached or leaked to another visitor. |
| **Authenticated HTML** | `/auth/profile`<br>`/tickets/my-tickets` | `text/html` | `Cookie` | `private, no-cache, no-store, must-revalidate` | **Secured**: Private user PII and tokens isolated from disk and proxy caches. |
| **Search Engine Sitemaps** | `/sitemap.xml` | `application/xml` | Default | Default / Cacheable | **Optimized**: Fast crawler ingestion; verified 100% free of session tokens. |
| **Robots Directives** | `/robots.txt` | `text/plain` | Default | Default / Cacheable | **Optimized**: Fast crawler retrieval; no session dependencies. |
| **Static Stylesheets & JS** | `/static/css/style.css`<br>`/static/js/main.js` | `text/css`<br>`application/javascript` | Default | `public, max-age=...` | **High Performance**: CDN edge caching enabled; zero token leakage risk. |
| **Ticket QR Codes** | `/static/qr_codes/...` | `image/svg+xml` | Default | `private, no-cache, no-store, must-revalidate` | **Secured**: Enforces IDOR check and strict `noindex, noarchive`. |

---

## 4. Test Results & Verification Evidence

Automated tests in `tests/test_csrf_security.py` confirm the behavior across all session scenarios:

1. **`test_csrf_anonymous_and_authenticated_cache_isolation` (Test 24)**:
   - Evaluates `GET /` (Anonymous):
     - `Vary` header contains `Cookie`.
     - `Cache-Control` contains `private` and `no-store`.
     - `Pragma` is `no-cache`.
   - Evaluates `GET /auth/profile` (Authenticated):
     - `Vary` header contains `Cookie`.
     - `Cache-Control` contains `private` and `no-store`.
     - `Pragma` is `no-cache`.
   - Evaluates `GET /sitemap.xml`:
     - Confirms `no-store` is NOT present, preserving crawler performance.
   - **Result**: `PASSED`.

2. **`test_csrf_token_not_leaked_in_sitemap_or_robots` (Test 19)**:
   - Confirms that `/sitemap.xml` and `/robots.txt` contain zero occurrences of CSRF tokens or user session identifiers.
   - **Result**: `PASSED`.

3. **`test_csrf_token_not_leaked_in_public_jsonld` (Test 20)**:
   - Confirms that public Schema.org Event structured data contains zero CSRF token attributes.
   - **Result**: `PASSED`.

---

## 5. Remaining Risks & Manual Actions

- **Remaining Risk**: None within Flask response dispatching.
- **Manual Action for Staging Deployment**: Ensure that the external reverse proxy (e.g., Nginx) does NOT override the backend `Cache-Control` header for HTML pages (avoid `proxy_ignore_headers Cache-Control`).

---

## 6. Security Sign-off

**Defect Classification**: MEDIUM (Resolved)  
**Remediation Verdict**: **CLOSED & VERIFIED**

