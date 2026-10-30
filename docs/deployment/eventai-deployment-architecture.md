# EventAI Pro — Phase 4 Production Deployment Architecture Specification

**Specification Date:** 2026-10-29  
**DevOps Architect:** Senior Systems & Production Readiness Engineer  
**Target Environments:** Staging & Linux Production (Ubuntu 22.04 / 24.04 LTS / Debian 12)  
**Primary Engine:** Python 3.12 / 3.14 | Gunicorn 21.2 | Nginx 1.24+ | SQLite 3 (WAL Mode)  
**Status:** **APPROVED ARCHITECTURAL BLUEPRINT**

---

## 1. System Architecture Overview

EventAI Pro is designed as a modular 3-tier web application combining a Flask Application Server, an Nginx Reverse Proxy, and an embedded SQLite database engine with dual-engine AI orchestration (Google Gemini API with local grounded fallback).

```
[ Internet Clients: Desktop & Mobile ]
                 │ (HTTPS - Port 443)
                 ▼
     ┌────────────────────────┐
     │  Nginx Reverse Proxy   │ ── TLS Termination & HTTP/2
     │  - Rate Limiting       │ ── Static Asset Offloading (CSS/JS/Img)
     │  - Security Headers    │ ── Request Routing & SSL Offloading
     └───────────┬────────────┘
                 │ (Unix Domain Socket / Localhost HTTP - Port 5000)
                 ▼
     ┌────────────────────────┐
     │  Gunicorn WSGI Server  │ ── 2 Workers x 4 Threads (gthread)
     │  - ProxyFix Middleware │ ── Request Validation & Routing
     │  - Flask Application   │ ── Jinja2 Apple Liquid Glass Rendering
     └───────────┬────────────┘
                 │ (Direct In-Process I/O - Shared Memory)
                 ▼
     ┌────────────────────────┐
     │ SQLite 3 (instance/)   │ ── WAL Mode (Write-Ahead Logging)
     │ - 9 Tables (3NF Schema)│ ── 10s Busy Timeout / ACID Transactions
     └────────────────────────┘
```

---

## 2. Web Server Gateway Interface (WSGI) Configuration

### 2.1 Gunicorn Production Configuration
The application is configured to run under Gunicorn via `Procfile` and standard systemd unit files:
- **Binding:** `127.0.0.1:5000` or a Unix Domain Socket (`/run/eventai/gunicorn.sock`).
- **Worker Architecture:** Multi-threaded worker model (`--workers 2 --threads 4 --worker-class gthread`).
  - Total concurrent connections: 8 concurrent requests.
  - Optimal balance for SQLite's single-writer model while allowing concurrent I/O-bound Gemini API queries.
- **Worker Timeout:** Set to `--timeout 120` to prevent worker restarts during complex multi-agent analysis or long-running RAG queries.
- **Graceful Lifecycle:** Handles `SIGTERM` and `SIGHUP` for zero-downtime rolling worker reloads.

### 2.2 Forwarded Header Integration (ProxyFix)
When deployed behind Nginx, Flask must trust forwarded reverse proxy headers to accurately determine client IP addresses and HTTPS schemes:
```python
# In production initialization:
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
```

---

## 3. Reverse Proxy (Nginx) Reference Configuration

An Nginx configuration optimized for EventAI Pro must provide TLS termination, static asset caching, rate limiting, and private route shielding:

```nginx
# Rate Limiting Zones
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=ai_limit:10m rate=30r/m;

server {
    listen 80;
    listen [::]:80;
    server_name eventai.pro www.eventai.pro;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name eventai.pro;

    # TLS / SSL Certificates (Let's Encrypt / Certbot)
    ssl_certificate /etc/letsencrypt/live/eventai.pro/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/eventai.pro/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    # Max Payload & Timeouts
    client_max_body_size 16M;
    keepalive_timeout 65;

    # HSTS & Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;

    # 1. Public Static Assets (Direct Nginx Serving)
    location /static/ {
        alias /var/www/eventai/app/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # 2. Guarded Private QR Codes (Pass to Flask for Ownership Check)
    location /static/qr_codes/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 3. Rate-Limited Authentication Portal
    location /auth/login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 4. Standard Application Proxy
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 60s;
    }
}
```

---

## 4. Containerization Architecture (Docker & Docker Compose)

### 4.1 Volume Mount Defect & Resolution
- **Defect in Existing `docker-compose.yml`:** The existing compose file mounted only `./app/static/qr_codes` and `./app/static/uploads`. The SQLite database located at `instance/event_management.db` was unmounted, causing all registrations, events, and database states to be lost whenever the container was recreated.
- **Approved Docker Compose Specification:**
  ```yaml
  version: '3.8'

  services:
    eventai-pro:
      build: .
      container_name: eventai_pro_app
      restart: unless-stopped
      ports:
        - "127.0.0.1:5000:5000"
      environment:
        - FLASK_ENV=production
        - SECRET_KEY=${SECRET_KEY}
        - DATABASE_URI=sqlite:///event_management.db
        - CANONICAL_DOMAIN=https://eventai.pro
        - GEMINI_API_KEY=${GEMINI_API_KEY}
        - GEMINI_MODEL=gemini-2.5-flash
        - ENABLE_AI_FALLBACK_MOCK=True
      volumes:
        - ./instance:/app/instance
        - ./app/static/qr_codes:/app/app/static/qr_codes
        - ./app/static/uploads:/app/app/static/uploads
      healthcheck:
        test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"]
        interval: 30s
        timeout: 5s
        retries: 3
        start_period: 10s
  ```

---

## 5. Systemd Service Specification (Bare Metal / VM Deployment)

For non-containerized Linux deployments, manage the Gunicorn process using systemd (`/etc/systemd/system/eventai.service`):

```ini
[Unit]
Description=EventAI Pro Flask Application Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/eventai
Environment="PATH=/var/www/eventai/.venv/bin"
EnvironmentFile=/var/www/eventai/.env
ExecStart=/var/www/eventai/.venv/bin/gunicorn run:app \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/eventai/access.log \
    --error-logfile /var/log/eventai/error.log
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=30
PrivateTmp=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 6. Health Check & Monitoring Strategy

The application provides a dedicated health check endpoint at `/health`:
- **Route:** `GET /health` (`main.health_check`)
- **Behavior:** Queries the database (`db.session.execute(text('SELECT 1'))`) to verify DB engine responsiveness.
- **Response:** Returns HTTP 200 with JSON payload `{"status": "healthy", "database": "connected"}`.
- **Monitoring Integration:** Suitable for uptime monitoring (UptimeRobot, Datadog, Prometheus Blackbox Exporter, AWS Route53 Health Checks).

