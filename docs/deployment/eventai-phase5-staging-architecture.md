# EventAI Pro — Phase 5 Isolated Staging Architecture Specification

**Specification Date:** 2026-10-29  
**Lead DevSecOps Architect:** Senior Deployment Security & Infrastructure Engineer  
**Execution Host:** Windows 11 Workspace (with Linux VM / Docker Staging Profiles)  
**Configuration Profile:** `StagingConfig` in `app/config.py`  
**Status:** **APPROVED FOR CONTROLLED STAGING REHEARSAL**

---

## 1. Staging Principles & Non-Interference Mandate

The Phase 5 staging architecture enforces strict separation between development, rehearsal, and production assets. Under no circumstances may a staging rehearsal read from or write to the primary application database (`instance/event_management.db`) or consume external third-party API quotas.

### Key Isolation Guarantees:
1. **Database Isolation:** Staging operates against a dedicated database file (`instance/staging.db` or `./instance_staging/staging.db`).
2. **Network Isolation:** Staging servers bind strictly to loopback addresses (`127.0.0.1`) or private virtual network interfaces. Public internet exposure is prohibited.
3. **AI Engine Isolation:** `ENABLE_AI_FALLBACK_MOCK=True` is enforced to route all LLM operations through the local Grounded Mock Engine, preventing Gemini API quota depletion.
4. **Credential Isolation:** Throwaway staging secret keys and synthetic accounts are utilized; zero real production secrets or customer PII are deployed.

---

## 2. Multi-Platform Staging Strategies

Because the developer workstation operates on Windows 11, where Linux WSGI servers (Gunicorn) and daemon managers (systemd) cannot run natively, three distinct staging deployment profiles are defined:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             STAGING STRATEGY SELECTION                           │
├─────────────────────────┬────────────────────────────┬───────────────────────────┤
│ Profile A: Local Win11  │ Profile B: Containerized   │ Profile C: Dedicated VM   │
│ (Rapid Local Rehearsal) │ (Environment Parity)       │ (Production Mirror)       │
├─────────────────────────┼────────────────────────────┼───────────────────────────┤
│ • Windows 11 Native     │ • Docker Desktop / Engine  │ • Ubuntu 22.04/24.04 VM   │
│ • Waitress / Flask WSGI │ • Gunicorn in Linux Base   │ • Native Gunicorn 21.2    │
│ • Localhost 127.0.0.1   │ • Isolated Staging Volumes │ • Nginx TLS Termination   │
│ • instance/staging.db   │ • 127.0.0.1:5001:5000      │ • staging.eventai.internal│
└─────────────────────────┴────────────────────────────┴───────────────────────────┘
```

### 2.1 Profile A: Local Windows Staging Rehearsal (Immediate Execution)
- **Use Case:** Pre-release verification, smoke testing, and regression analysis on the local developer machine.
- **Server:** Flask WSGI runner or `waitress-serve`:
  ```powershell
  $env:FLASK_ENV="staging"
  $env:DATABASE_URI="sqlite:///instance/staging.db"
  $env:CANONICAL_DOMAIN="http://127.0.0.1:5000"
  python run.py
  ```
- **Configuration:** `StagingConfig` sets `DEBUG=False`, `SESSION_COOKIE_SECURE=False` (permits local HTTP testing without TLS warnings), `ENABLE_AI_FALLBACK_MOCK=True`.

### 2.2 Profile B: Containerized Staging Deployment (`docker-compose.staging.yml`)
- **Use Case:** Full environment parity on machines with Docker Desktop installed.
- **Specification:** Managed via [`docker-compose.staging.yml`](file:///d:/Event_Management_AI/docker-compose.staging.yml):
  ```yaml
  services:
    eventai-staging:
      build: .
      container_name: eventai_staging_app
      ports:
        - "127.0.0.1:5001:5000"
      environment:
        - FLASK_ENV=staging
        - DATABASE_URI=sqlite:///instance/staging.db
      volumes:
        - ./instance_staging:/app/instance
        - ./app/static/qr_codes_staging:/app/app/static/qr_codes
        - ./app/static/uploads_staging:/app/app/static/uploads
  ```
- **Durability Assurance:** Mounts separate `./instance_staging` and `./app/static/*_staging` directories, completely shielding production assets.

### 2.3 Profile C: Dedicated Linux Staging Server / Virtual Machine
- **Use Case:** Pre-production staging server or staging Kubernetes/VM cluster.
- **Components:**
  - Nginx 1.24+ reverse proxy terminating staging SSL (internal wildcard certificate).
  - Gunicorn 21.2 multi-threaded WSGI (`--workers 2 --threads 4 --worker-class gthread`).
  - Systemd service unit `eventai-staging.service`.
  - SQLite 3 operating in WAL mode with hourly hot backups.

---

## 3. Configuration Architecture (`StagingConfig`)

In [`app/config.py`](file:///d:/Event_Management_AI/app/config.py), the dedicated `StagingConfig` profile defines:

```python
class StagingConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 't')
    ENABLE_AI_FALLBACK_MOCK = True
```

- **`DEBUG = False`:** Deactivates Werkzeug interactive debug console and PIN.
- **`TESTING = False`:** Runs live blueprint routes and authentication middleware without test mocks.
- **`SESSION_COOKIE_HTTPONLY = True`:** Shields session cookies from JavaScript document.cookie access.
- **`SESSION_COOKIE_SAMESITE = 'Lax'`:** Provides baseline defense against third-party cross-site request forgery.
- **`ENABLE_AI_FALLBACK_MOCK = True`:** Guarantees deterministic, zero-cost AI recommendations, attendance forecasts, and chat interactions.

---

## 4. Staging Network & Host Header Validation

1. **Host Header Filtering:** Requests with unauthorized Host headers (e.g. host injection attempts) are rejected by Nginx or the WSGI proxy boundary.
2. **Canonical Origin Enforcement:** All canonical URLs, sitemaps, and Open Graph meta tags resolve to the staging domain specified in `CANONICAL_DOMAIN` (e.g. `http://127.0.0.1:5000` or `https://staging.eventai.internal`).
3. **Loopback Binding:** Network listeners are bound exclusively to `127.0.0.1` to prevent unauthorized LAN or WAN probing.

