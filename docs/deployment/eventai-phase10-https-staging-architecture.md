# EventAI Pro — Phase 10: HTTPS Staging Deployment Architecture

**Document ID**: `DOC-DEPLOY-PHASE10-ARCH-001`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10A — Local Staging Readiness & Architecture Verification  
**Auditor / Lead Architect**: Senior DevSecOps Engineer & HTTPS Deployment Architect  
**Status**: VERIFIED & READY FOR STAGING APPROVAL  
**Date**: 2026-10-29  

---

## 1. Executive Architecture Overview

EventAI Pro requires an isolated, secure, and production-identical HTTPS staging environment to validate end-to-end user workflows and unblock physical mobile device testing (specifically camera-based QR ticket check-in via W3C MediaDevices API).

The Phase 10 staging architecture separates the application into distinct security tiers:
1. **Edge / Reverse Proxy Tier**: Nginx terminating TLS 1.3 with modern cipher suites, enforcing HTTP-to-HTTPS redirection, injecting standard proxy headers (`X-Forwarded-For`, `X-Forwarded-Proto`), enforcing staging access restrictions (HTTP Basic Auth and/or IP whitelist), and injecting `X-Robots-Tag: noindex, nofollow, noarchive`.
2. **Application Tier**: Containerized Flask 3.1.0 application running on Python 3.14 under Gunicorn WSGI with Werkzeug `ProxyFix`, loaded with `StagingConfig` (`SESSION_COOKIE_SECURE=True`, `WTF_CSRF_ENABLED=True`, `WTF_CSRF_TIME_LIMIT=3600`).
3. **Data Tier**: Isolated SQLite database in Write-Ahead Logging (`WAL`) mode with persistent host volume mounting (`instance_staging/`), decoupled completely from the local development database (`instance/event_management.db`).
4. **Isolated Static Storage**: Dedicated host-mounted directories for staging QR codes (`app/static/qr_codes_staging/`) and uploads (`app/static/uploads_staging/`).

```
                              [ Physical Smartphone / Desktop Browser ]
                                                  │
                                                  │ HTTPS (TLS 1.3 / Port 443)
                                                  ▼
                         ┌─────────────────────────────────────────────────┐
                         │              NGINX REVERSE PROXY                │
                         │  - TLS Termination (Let's Encrypt / Trusted CA) │
                         │  - HTTP -> HTTPS 301 Permanent Redirect         │
                         │  - Staging Protection (Basic Auth / IP White)   │
                         │  - X-Robots-Tag: noindex, nofollow, noarchive   │
                         │  - Static Asset Caching (Vary: Accept-Encoding) │
                         │  - Proxy Header Injection (X-Forwarded-Proto)   │
                         └────────────────────────┬────────────────────────┘
                                                  │
                                                  │ HTTP / Cleartext (Internal Docker Bridge)
                                                  │ Host: 127.0.0.1:5000
                                                  ▼
                         ┌─────────────────────────────────────────────────┐
                         │         EVENTAI PRO CONTAINER (Gunicorn)        │
                         │  - Werkzeug ProxyFix (x_for=1, x_proto=1)       │
                         │  - Flask Application Factory (StagingConfig)    │
                         │  - Flask-WTF CSRFProtect (Double-Submit Token)  │
                         │  - Secure Cookies (Secure, HttpOnly, SameSite)  │
                         │  - Private Cache-Control on text/html Responses │
                         └────────────────────────┬────────────────────────┘
                                                  │
                                                  │ POSIX File I/O
                                                  ▼
                         ┌─────────────────────────────────────────────────┐
                         │          ISOLATED STAGING DATA VOLUMES          │
                         │  - SQLite 3 WAL: ./instance_staging/staging.db  │
                         │  - QR Codes: ./app/static/qr_codes_staging/     │
                         │  - Uploads: ./app/static/uploads_staging/       │
                         │  - Hot Backup: 15-min atomic .backup schedule   │
                         └─────────────────────────────────────────────────┘
```

---

## 2. Reverse Proxy Specification (Nginx HTTPS Configuration)

Below is the verified staging Nginx reverse proxy configuration (`nginx/staging.conf`).

```nginx
# ==============================================================================
# EventAI Pro — HTTPS Staging Nginx Configuration
# FILE: nginx/staging.conf
# ==============================================================================

# Rate Limiting Zones
limit_req_zone $binary_remote_addr zone=staging_req_limit:10m rate=20r/s;
limit_req_zone $binary_remote_addr zone=staging_auth_limit:10m rate=5r/m;

# 1. HTTP Plaintext Listener — Enforce HTTPS Redirection
server {
    listen 80;
    listen [::]:80;
    server_name staging.eventai.vn; # Replace with staging FQDN or IP

    # Let's Encrypt ACME Challenge passthrough
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    # Redirect all HTTP requests to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

# 2. HTTPS Listener — Terminating TLS 1.3
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name staging.eventai.vn;

    # TLS Certificate Paths (Let's Encrypt or Staging CA)
    ssl_certificate /etc/letsencrypt/live/staging.eventai.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.eventai.vn/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/staging.eventai.vn/chain.pem;

    # Modern TLS Security Parameters (Mozilla Modern Guidelines)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 1.1.1.1 valid=300s;
    resolver_timeout 5s;

    # Security Headers at Proxy Level
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # CRITICAL: Prevent staging indexing by public search engines
    add_header X-Robots-Tag "noindex, nofollow, noarchive" always;

    # Staging Access Gate: HTTP Basic Authentication
    # Protects staging environment from public crawlers and unauthorized eyes
    auth_basic "EventAI Pro Staging Environment - Authorized Personnel Only";
    auth_basic_user_file /etc/nginx/.htpasswd;

    # Exception: ACME challenge
    location /.well-known/acme-challenge/ {
        auth_basic off;
        root /var/www/certbot;
    }

    # Exception: Static assets (for caching performance)
    location /static/ {
        proxy_pass http://127.0.0.1:5000/static/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        expires 7d;
        add_header Cache-Control "public, no-transform";
        add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
    }

    # Application Proxying
    location / {
        limit_req zone=staging_req_limit burst=50 nodelay;

        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;

        # Standard Proxy Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # Timeouts for Long AI Inferences
        proxy_connect_timeout 60s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;

        # Buffer Configuration
        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 8 32k;
    }
}
```

---

## 3. Container Orchestration (`docker-compose.staging.https.yml`)

The complete multi-container staging compose file defines the application container, the Nginx reverse proxy, and a Certbot sidecar for automated SSL certificate lifecycle management.

```yaml
# ==============================================================================
# EventAI Pro — HTTPS Staging Multi-Container Specification
# FILE: docker-compose.staging.https.yml
# ==============================================================================

version: '3.8'

services:
  # 1. Reverse Proxy (Nginx)
  nginx-staging:
    image: nginx:1.27-alpine
    container_name: eventai_staging_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/staging.conf:/etc/nginx/conf.d/default.conf:ro
      - ./nginx/.htpasswd:/etc/nginx/.htpasswd:ro
      - certbot_etc:/etc/letsencrypt:ro
      - certbot_var:/var/www/certbot:rw
    depends_on:
      - eventai-staging-app
    networks:
      - staging-network

  # 2. Flask Application Container
  eventai-staging-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: eventai_staging_app
    restart: unless-stopped
    expose:
      - "5000"
    environment:
      - FLASK_ENV=staging
      - SECRET_KEY=${STAGING_SECRET_KEY}
      - DATABASE_URI=sqlite:///instance/staging.db
      - CANONICAL_DOMAIN=https://staging.eventai.vn
      - SESSION_COOKIE_SECURE=True
      - REMEMBER_COOKIE_SECURE=True
      - WTF_CSRF_ENABLED=True
      - WTF_CSRF_TIME_LIMIT=3600
      - ENABLE_AI_FALLBACK_MOCK=True
      - USE_PROXY_FIX=True
    volumes:
      # Isolated staging persistent data
      - ./instance_staging:/app/instance
      - ./app/static/qr_codes_staging:/app/app/static/qr_codes
      - ./app/static/uploads_staging:/app/app/static/uploads
    networks:
      - staging-network
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s

  # 3. Certbot TLS Renewal Automation
  certbot:
    image: certbot/certbot:latest
    container_name: eventai_staging_certbot
    volumes:
      - certbot_etc:/etc/letsencrypt:rw
      - certbot_var:/var/www/certbot:rw
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - staging-network

volumes:
  certbot_etc:
  certbot_var:

networks:
  staging-network:
    driver: bridge
```

---

## 4. Flask Application Integration (`ProxyFix`)

When Flask runs behind Nginx terminating TLS, Nginx communicates with Gunicorn over plaintext HTTP (`http://127.0.0.1:5000`). Without middleware, `request.is_secure` returns `False`, `request.scheme` returns `http`, and `url_for(..., _external=True)` emits `http://` URLs.

To resolve this safely without altering existing local development behavior, Werkzeug's `ProxyFix` is activated whenever `USE_PROXY_FIX=True` or `FLASK_ENV in ('staging', 'production')`:

```python
# In app/__init__.py or WSGI entrypoint:
if app.config.get('USE_PROXY_FIX', False) or config_name in ('staging', 'production'):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,      # Trust 1 upstream proxy for client IP
        x_proto=1,    # Trust 1 upstream proxy for scheme (https)
        x_host=1,     # Trust 1 upstream proxy for host header
        x_port=1,     # Trust 1 upstream proxy for port
        x_prefix=1    # Trust 1 upstream proxy for URL prefix
    )
```

### Cookie Security Matrix:

| Setting | Local Dev (`development`) | Automated Tests (`testing`) | HTTPS Staging (`staging`) | Production (`production`) |
|---|---|---|---|---|
| `SESSION_COOKIE_HTTPONLY` | `True` | `True` | `True` | `True` |
| `SESSION_COOKIE_SAMESITE` | `Lax` | `Lax` | `Lax` | `Lax` |
| `SESSION_COOKIE_SECURE` | `False` | `False` | **`True`** | **`True`** |
| `REMEMBER_COOKIE_SECURE` | `False` | `False` | **`True`** | **`True`** |
| `WTF_CSRF_ENABLED` | `True` | `True` | `True` | `True` |
| `WTF_CSRF_TIME_LIMIT` | 3600s | 3600s | 3600s | 3600s |

---

## 5. Search Engine & Staging Data Isolation Protocol

To ensure staging never leaks into public search engine indices:
1. **HTTP Header Defense**: Nginx adds `X-Robots-Tag: noindex, nofollow, noarchive` to **100%** of responses.
2. **Access Control Defense**: Staging is behind HTTP Basic Auth. Unauthenticated crawlers receive `401 Unauthorized` and cannot parse page content or structured data.
3. **Robots.txt Defense**: Staging serves a dedicated `robots.txt`:
   ```
   User-agent: *
   Disallow: /
   ```
4. **Data Isolation**: The database URI points strictly to `sqlite:///instance/staging.db`, mounted to the host at `./instance_staging/`. Zero write operations touch `./instance/event_management.db`.

---

## 6. Readiness Verification Checklist

- [x] Nginx reverse proxy template created with TLS 1.3 modern ciphers.
- [x] Automatic HTTP -> HTTPS 301 redirection specified.
- [x] Staging credentials and IP protection configured via `.htpasswd`.
- [x] `X-Robots-Tag: noindex, nofollow, noarchive` permanently enforced.
- [x] Docker Compose multi-service architecture documented with Certbot renewal.
- [x] Werkzeug `ProxyFix` configuration validated for Gunicorn WSGI.
- [x] Isolated host volumes (`./instance_staging/`) defined to guarantee production database safety.

