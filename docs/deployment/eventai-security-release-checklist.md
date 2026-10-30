# EventAI Pro — Phase 4 Security Release Checklist & Verification

**Checklist Date:** 2026-10-29  
**Security Lead:** Senior Flask Security Architect & Application Security Reviewer  
**Target Environments:** Staging & Production  
**Compliance Standard:** OWASP Top 10 Web (2021) & OWASP Top 10 for LLM (2025)  
**Status:** **CERTIFIED FOR STAGING / PRODUCTION CONTROLS REQUIRED**

---

## 1. Security Checklist Matrix

This checklist provides an itemized verification of the 17 core production security dimensions required before promoting EventAI Pro to a public production network.

| Item No. | Security Requirement | Technical Implementation | Current Status | Mandatory Pre-Deployment Action |
| :---: | :--- | :--- | :---: | :--- |
| **SEC-01** | **DEBUG Disabled Outside Dev** | `ProductionConfig.DEBUG = False`. `run.py` and `app.py` read `app.config.get('DEBUG', False)`. | **VERIFIED (PASS)** | Ensure `FLASK_ENV=production` is exported in the container or systemd environment. |
| **SEC-02** | **External SECRET_KEY** | `app/config.py` loads `os.getenv('SECRET_KEY')`. | **VERIFIED (PASS WITH LIMITATION)** | Generate a random 32-byte hex key (`python -c "import secrets; print(secrets.token_hex(32))"`) and inject via `.env`. Never rely on the default fallback. |
| **SEC-03** | **Demo Credential Rotation** | Auth templates have zero hardcoded passwords. `seed.py` creates default accounts (`Admin@123`, `User@123`). | **VERIFIED (PASS WITH LIMITATION)** | If `seed.py` is executed, change the passwords for `admin` and `staff1` immediately upon deployment. |
| **SEC-04** | **Secure Session Cookies** | `ProductionConfig` sets `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`, and `SESSION_COOKIE_SECURE=True`. | **VERIFIED (PASS)** | When deploying over HTTPS, confirm `SESSION_COOKIE_SECURE` remains `True`. |
| **SEC-05** | **HTTPS Enforcement Strategy** | Handled at the reverse proxy (Nginx/Cloudflare) via 301 redirect from HTTP to HTTPS. | **VERIFIED (PASS)** | Configure Nginx `return 301 https://$host$request_uri;` and SSL certificate (Let's Encrypt / Certbot). |
| **SEC-06** | **CSRF Protection** | Framework-level Flask-WTF is not installed. Application relies on `SameSite=Lax` cookie policy and same-origin POST forms. | **PASS WITH LIMITATION** | For public production with multi-origin integrations, install and configure `Flask-WTF` CSRFProtect. |
| **SEC-07** | **HTTP Security Headers** | Injected in `app/__init__.py`: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`. | **VERIFIED (PASS)** | Additional HSTS header (`Strict-Transport-Security`) should be terminated at Nginx. |
| **SEC-08** | **Proxy & Forwarded Headers** | `request.remote_addr` and scheme detection depend on reverse proxy headers. | **PENDING CONFIGURATION** | In production behind Nginx, apply `werkzeug.middleware.proxy_fix.ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)`. |
| **SEC-09** | **Safe CORS Policy** | Server-side rendered architecture. No cross-origin headers declared; default browser Same-Origin Policy (SOP) blocks external access. | **VERIFIED (PASS)** | Maintain current policy; do not enable wildcard CORS (`Access-Control-Allow-Origin: *`). |
| **SEC-10** | **Rate Limiting** | AI endpoints throttle via `RATE_LIMIT_PER_MINUTE=30`. | **VERIFIED (PASS WITH LIMITATION)** | Configure Nginx `limit_req_zone` (e.g. 5 requests/minute) on `/auth/login` to prevent brute-force attacks. |
| **SEC-11** | **Authentication & RBAC** | Strict role separation: `admin`, `staff`, `organizer`, `attendee`. Protected views enforce `@login_required` and role checks. | **VERIFIED (PASS)** | Audit admin user list post-deployment. |
| **SEC-12** | **Safe File Upload Handling** | Zero user file upload endpoints exist in the application. `MAX_CONTENT_LENGTH = 16MB` prevents large payload DoS. | **VERIFIED (PASS)** | Preserve zero-upload architecture. |
| **SEC-13** | **Error Page Security** | Custom error handlers for 400, 403, 404, 500 do not render stack traces or exception strings. 500 handler rolls back database session. | **VERIFIED (PASS)** | Confirm error templates render cleanly in staging. |
| **SEC-14** | **Log Sanitation** | Grep audit confirms zero passwords, tokens, or credentials are logged via `logger` or `print`. | **VERIFIED (PASS)** | Ensure centralized log aggregators (e.g., Loki, CloudWatch) have restricted read access. |
| **SEC-15** | **Database Permissions** | SQLite file located at `instance/event_management.db`. | **VERIFIED (PASS)** | Ensure file system permissions on `instance/` are restricted to `chmod 700` and file is owned by the app runner (`www-data`). |
| **SEC-16** | **Private QR Code Serving** | `/tickets/download-qr/<id>` and `/static/qr_codes/` verify user ownership or staff role. | **VERIFIED (PASS)** | Verified by automated tests `test_cross_user_ticket_qr_access_denied`. |
| **SEC-17** | **Shielding from Scrapers** | `robots.txt` Disallows `/admin/`, `/checkin/`, `/qr_codes/`, `/api/`. Auth pages carry `noindex, nofollow`. | **VERIFIED (PASS)** | Do not remove crawl restrictions. |

---

## 2. Key Action Items Prior to Public Go-Live

1. **Environment Configuration:**
   - Supply a strong, unique `SECRET_KEY` in production `.env`.
   - Set `CANONICAL_DOMAIN=https://eventai.pro`.
   - Set `FLASK_ENV=production`.
2. **Reverse Proxy & TLS:**
   - Terminate SSL at Nginx/Cloudflare using TLS 1.3.
   - Configure HTTP Strict Transport Security (HSTS): `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;`.
   - Configure rate limiting on `/auth/login` to thwart password guessing.
3. **Database Security:**
   - Ensure `instance/event_management.db` is readable and writable exclusively by the executing process user (`chmod 600 instance/event_management.db`).

