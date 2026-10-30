# EventAI Pro — Phase 6 Production Configuration & Proxy Architecture Review

**Document Reference:** `docs/deployment/eventai-phase6-production-configuration-review.md`  
**Execution Date:** 2026-10-29  
**Lead Engineer:** Senior Flask Production Architect & DevOps Security Specialist  
**Target File:** `app/config.py`, `app/__init__.py`, `docker-compose.staging.yml`, `env.staging.example`  
**Status:** **AUDITED, HARDENED & COMPLIANT**

---

## 1. Overview & Configuration Hierarchy

EventAI Pro organizes application settings through class-based inheritance in `app/config.py`. In Phase 5 and Phase 6, distinct configuration profiles were established to ensure complete isolation between Development, Testing, Staging, and Production environments:

```
                  ┌───────────────────────┐
                  │      class Config     │
                  │ (Base Settings & Keys)│
                  └───────────┬───────────┘
                              │
       ┌───────────────┬──────┴────────┬───────────────┐
       ▼               ▼               ▼               ▼
DevelopmentConfig TestingConfig StagingConfig ProductionConfig
 (DEBUG=True)   (In-Memory DB)  (Mock AI/Safe)  (Strict Security)
```

---

## 2. Configuration Profiles Detailed Audit

| Setting Key | Base `Config` | `TestingConfig` | `StagingConfig` | `ProductionConfig` | Production Security Rationale |
|---|---|---|---|---|---|
| `DEBUG` | False | False | **False** | **False** | Prevents interactive Werkzeug traceback debugger exposure. |
| `TESTING` | False | **True** | **False** | **False** | Disables test mode flags; ensures production exception flows execute. |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///event_management.db` | `sqlite:///:memory:` | File-based SQLite / External DB | Managed Persistent DB | Memory database prevents test state pollution; staging/production persist data. |
| `SESSION_COOKIE_HTTPONLY` | Default (False) | False | **True** | **True** | Blocks client-side JavaScript access to session cookie via `document.cookie` (mitigates XSS token exfiltration). |
| `SESSION_COOKIE_SAMESITE` | Default (None) | None | **'Lax'** | **'Lax'** | Enforces browser withholding of session cookies on cross-site requests (CSRF mitigation). |
| `SESSION_COOKIE_SECURE` | False | False | Configurable (`False`/`True`) | **True** (Default) | Restricts cookies to HTTPS-only transmissions; prevents plaintext sniffing over HTTP. |
| `REMEMBER_COOKIE_HTTPONLY` | Default (False) | False | **True** | **True** | Hardens long-lived "Remember Me" authentication tokens against XSS. |
| `REMEMBER_COOKIE_SAMESITE` | Default (None) | None | **'Lax'** | **'Lax'** | Prevents cross-origin CSRF attacks against long-lived sessions. |
| `ENABLE_AI_FALLBACK_MOCK` | False | True | **True** | False (Requires API Key) | Allows staging rehearsals to operate 100% offline without burning Gemini API quota. |
| `RATE_LIMIT_PER_MINUTE` | 30 | 30 | 30 | 30 | Prevents resource exhaustion and brute-force abuse on AI and check-in endpoints. |
| `MAX_CONTENT_LENGTH` | 16 MB | 16 MB | 16 MB | 16 MB | Prevents Denial of Service (DoS) via oversized HTTP multipart file uploads. |

---

## 3. Reverse Proxy & ProxyFix Architecture

### 3.1 The Need for `ProxyFix`
When EventAI Pro is deployed behind an edge reverse proxy (such as Nginx, Traefik, AWS CloudFront, or Cloudflare), the upstream proxy terminates TLS and forwards requests to Flask over an internal network.
Without middleware adjustment:
- `request.remote_addr` sees the internal IP of the reverse proxy, corrupting rate limiters and audit logs.
- `request.scheme` reports `http` instead of `https`, causing redirect loops and breaking canonical URL generation.
- `request.host` may report internal container hostnames (`web:5000`) instead of the public domain.

### 3.2 Secure ProxyFix Specification
Werkzeug provides `werkzeug.middleware.proxy_fix.ProxyFix`. In `app/__init__.py`:
```python
# app/__init__.py (Production / Staging Setup)
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(config_name=None):
    # ...
    if config_name in ('staging', 'production'):
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,      # Trust 1 upstream proxy for client IP
            x_proto=1,    # Trust 1 upstream proxy for scheme (https)
            x_host=1,     # Trust 1 upstream proxy for Host header
            x_port=1,     # Trust 1 upstream proxy for port
            x_prefix=1    # Trust 1 upstream proxy for SCRIPT_NAME prefix
        )
    # ...
```
> [!IMPORTANT]
> The parameter count (`x_for=1`) must match the exact number of trusted reverse proxies. Setting an excessive number (e.g., `x_for=5`) allows untrusted clients to spoof their client IP by injecting fake `X-Forwarded-For` headers.

---

## 4. Host Header Injection & Canonical Domain Verification

To defend against Host Header poisoning and cache poisoning attacks, `app/seo_helpers.py` implements strict origin validation in `get_trusted_canonical_origin()`:
1. **Explicit Whitelist:** If `CANONICAL_DOMAIN` is set (e.g., `https://eventai.pro`), all canonical links, sitemaps, and robots directives strictly use this origin.
2. **Format Sanitation:** Rejects any `CANONICAL_DOMAIN` or `Host` header containing carriage returns (`\r`), newlines (`\n`), spaces, `@` userinfo credentials, or non-HTTP schemes.
3. **Safe Local Fallback:** When `CANONICAL_DOMAIN` is unset (local development), requests with malformed host headers cleanly fall back to `http://localhost:5000`.

---

## 5. Secret Management & Staging Hygiene

1. **Zero Secret Hardcoding:** All production secrets (`SECRET_KEY`, `GEMINI_API_KEY`, `DATABASE_URI`) are loaded dynamically from environment variables via `os.getenv()`.
2. **Template vs. Runtime Isolation:**
   - `env.staging.example` contains sanitized placeholders (`stg_secret_key_change_me_in_rehearsal_2026`).
   - The real `.env` file is excluded from version control via `.gitignore`.
3. **Cookie Secure Flag in Staging:**
   - In staging without TLS termination, `SESSION_COOKIE_SECURE = False` enables developer validation over HTTP.
   - In production, `SESSION_COOKIE_SECURE = True` is strictly enforced to ensure cookies are never transmitted over unencrypted links.

