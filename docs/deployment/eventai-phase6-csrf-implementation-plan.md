# EventAI Pro — Phase 6 CSRF Implementation Plan (`Flask-WTF`)

**Document Reference:** `docs/deployment/eventai-phase6-csrf-implementation-plan.md`  
**Execution Date:** 2026-10-29  
**Security Lead:** Senior Flask Application Security Architect & DevSecOps Engineer  
**Target Dependency:** `Flask-WTF == 1.3.0` (Pending Human Authorization)  
**Compatibility:** Python 3.14.2, Flask 3.1.0, Jinja2 3.1.5  
**Gate Condition:** **APPROVED FOR STAGING ARCHITECTURE / PENDING USER APPROVAL FOR CODE MODIFICATION**

---

## 1. Objective & Scope

This implementation plan outlines the exact, production-ready technical architecture for integrating automated, cryptographically secure Cross-Site Request Forgery (CSRF) protection into **EventAI Pro** using `Flask-WTF`.

The plan encompasses:
1. Extension initialization in `app/extensions.py` and factory wiring in `app/__init__.py`.
2. Dynamic token generation via Jinja2 template helpers.
3. Automated client-side AJAX / Fetch header injection via `app/static/js/main.js` and `ai_chat.js`.
4. Dedicated custom error handling for HTTP 400 CSRF validation failures.
5. Testing strategy and compatibility switches (`WTF_CSRF_ENABLED = False` in `TestingConfig`).

---

## 2. Technical Architecture & Component Flow

```
User Browser / Form / Fetch Request
        │
        ├── (1) Standard HTML Form POST
        │         └─ Payload includes: <input type="hidden" name="csrf_token" value="...">
        │
        └── (2) Asynchronous Fetch / AJAX POST
                  └─ Header includes: 'X-CSRFToken': '<meta name="csrf-token" content="...">
        │
        ▼
WSGI Server (Gunicorn / Waitress)
        │
        ▼
Flask Application Factory (`app/__init__.py`)
        │
        ▼
`CSRFProtect.before_request()` Hook (`Flask-WTF`)
        │
        ├── Validate Token against Server-Side Secret Key & User Session
        ├── [Token Valid]   ──► Pass control to Blueprint Route Handler (200 / 302)
        └── [Token Invalid] ──► Raise CSRFError ──► Return Custom 400 JSON / HTML Error Page
```

---

## 3. Step-by-Step Implementation Specification

### Step 3.1: Extension Registration in `app/extensions.py`
In `app/extensions.py`, instantiate `CSRFProtect` alongside existing extensions:
```python
# app/extensions.py
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
```

### Step 3.2: Application Factory Wiring in `app/__init__.py`
In `create_app()`:
```python
# app/__init__.py
from app.extensions import csrf

def create_app(config_name=None):
    # ...
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  # Initialize CSRF protection globally
    # ...
```

### Step 3.3: Configuration Presets in `app/config.py`
Ensure the testing environment disables CSRF validation so existing unit/integration tests continue passing without requiring mock token injection:
```python
# app/config.py
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'event_mgmt_ai_secret_super_key_2026')
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour expiration for CSRF tokens

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False  # Keep disabled for pure unit and functional test speed
```

### Step 3.4: Base Template Metadata Injection (`app/templates/base.html`)
Inject the active CSRF token into a `<meta>` tag in the document `<head>` to support JavaScript fetch and AJAX callers:
```html
<!-- app/templates/base.html -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSRF Token for JavaScript Fetch / AJAX calls -->
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{% block title %}EventAI Pro{% endblock %}</title>
    <!-- ... -->
</head>
```

### Step 3.5: Client-Side AJAX / Fetch Interceptor (`app/static/js/main.js`)
Ensure all outbound state-changing AJAX requests (`POST`, `PUT`, `DELETE`) automatically attach the `X-CSRFToken` header:
```javascript
// app/static/js/main.js
(function() {
    'use strict';
    
    // Retrieve CSRF token from document meta tag
    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    }

    // Wrap window.fetch to automatically append CSRF token to state-changing requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        options = options || {};
        const method = (options.method || 'GET').toUpperCase();
        
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
            options.headers = options.headers || {};
            if (options.headers instanceof Headers) {
                if (!options.headers.has('X-CSRFToken')) {
                    options.headers.append('X-CSRFToken', getCsrfToken());
                }
            } else if (Array.isArray(options.headers)) {
                options.headers.push(['X-CSRFToken', getCsrfToken()]);
            } else {
                if (!options.headers['X-CSRFToken']) {
                    options.headers['X-CSRFToken'] = getCsrfToken();
                }
            }
        }
        return originalFetch.call(this, url, options);
    };
})();
```

### Step 3.6: Form Token Injection Across HTML Templates
For standard server-rendered forms, inject the token helper within the `<form>` element:
```html
<form method="POST" action="{{ url_for('auth.login') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <!-- Form fields -->
</form>
```

Affected Templates Inventory (19 Form Templates):
1. `app/templates/auth/login.html`
2. `app/templates/auth/register.html`
3. `app/templates/auth/profile.html` (Update Profile & Change Password forms)
4. `app/templates/admin/users.html` (Create User modal)
5. `app/templates/events/create.html`
6. `app/templates/events/edit.html`
7. `app/templates/events/event_detail.html` (Delete Event modal, Create Schedule, Create Ticket modals)
8. `app/templates/tickets/register.html`
9. `app/templates/tickets/checkout.html`
10. `app/templates/tickets/ticket_detail.html` (Cancel Ticket modal, Submit Feedback modal)
11. `app/templates/notifications/create.html`

### Step 3.7: Custom Error Handling for CSRF Failures (`app/routes/errors.py`)
Provide an informative, user-friendly, and secure error response when a CSRF token is expired or missing, avoiding default unstyled werkzeug 400 pages:
```python
# app/routes/errors.py or app/__init__.py
from flask_wtf.csrf import CSRFError
from flask import render_template, jsonify, request

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.is_json or request.path.startswith('/api/') or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': False,
            'error': 'CSRF token missing or invalid. Please refresh the page and try again.',
            'code': 'CSRF_VALIDATION_FAILED'
        }), 400
    return render_template('errors/400.html', reason='Phiên làm việc hoặc mã bảo mật (CSRF Token) đã hết hạn. Vui lòng tải lại trang và thử lại.'), 400
```

---

## 4. Rollout Phasing & Staging Strategy

| Phase | Milestone | Actions | Expected Outcome |
|---|---|---|---|
| **Phase 6A** | Approval & Lock | Human authorization of `Flask-WTF 1.3.0` | Dependency added to `requirements.txt` |
| **Phase 6B** | Core Wiring | Register `CSRFProtect` in `extensions.py` & `__init__.py` | Global protection active in dev/staging |
| **Phase 6C** | UI & JS Integration | Update `base.html`, `main.js`, and form templates | Zero user disruption; seamless token injection |
| **Phase 6D** | Test Automation | Create `tests/test_csrf_protection.py` (verify valid vs invalid tokens) | 100% automated regression coverage |
| **Phase 6E** | Production Sign-off | Enable in staging environment; conduct live rehearsal | Public production release gate unblocked |

