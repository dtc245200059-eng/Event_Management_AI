# EventAI Pro — Phase 10B: Staging Deployment Execution & Runbook

**Document ID**: `DOC-DEPLOY-PHASE10B-EXEC-004`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B — Deployment Execution & Runbook  
**Auditor / Lead Architect**: Senior DevSecOps Engineer & Production Release Manager  
**Execution State**: **PREFLIGHT COMPLETE — PENDING GATE B INFRASTRUCTURE AUTHORIZATION**  
**Date**: 2026-10-29  

---

## 1. Executive Summary & Deployment Status

This document details the exact execution state of the staging infrastructure and provides the audited, step-by-step runbook for launching the HTTPS staging environment upon receipt of Gate B approval.

### Reality-Checked Deployment Status:
- **Active Staging Containers**: **0 running** (No unauthorized processes launched).
- **Public Ports Bound**: **0 open** (Ports 80 and 443 remain untouched).
- **DNS / Network Records**: **0 modified**.
- **Database Status**: Local development database remains isolated; staging database directory initialized.

---

## 2. Pre-Deployment Configuration Artifacts

The deployment templates have been authored, validated, and staged in the project workspace:

1. **Staging Environment Template** (`.env.staging`):
   ```ini
   FLASK_ENV=staging
   SECRET_KEY=<SECURELY_GENERATED_64_CHAR_HEX>
   DATABASE_URI=sqlite:///instance/staging.db
   CANONICAL_DOMAIN=https://<APPROVED_STAGING_FQDN>
   SESSION_COOKIE_SECURE=True
   REMEMBER_COOKIE_SECURE=True
   WTF_CSRF_ENABLED=True
   WTF_CSRF_TIME_LIMIT=3600
   ENABLE_AI_FALLBACK_MOCK=True
   USE_PROXY_FIX=True
   ```
2. **Reverse Proxy Specification**: `nginx/staging.conf` incorporating conservative HSTS, ProxyFix headers, rate limiting, and HTTP Basic Auth.
3. **Multi-Container Compose File**: `docker-compose.staging.https.yml` targeting isolated persistent directories.

---

## 3. Step-by-Step Staging Launch Runbook (For Gate B Execution)

The moment the user provides authorization for Items A through H, the deployment engineer executes the following protocol:

```bash
# ==============================================================================
# STEP 1: INITIALIZE STAGING STORAGE & PERMISSIONS
# ==============================================================================
mkdir -p instance_staging app/static/qr_codes_staging app/static/uploads_staging
mkdir -p nginx certbot/conf certbot/www

# ==============================================================================
# STEP 2: GENERATE SECURE STAGING CREDENTIALS & HTACCESS
# ==============================================================================
# Generate local cryptographically strong secret key (Never printed to logs)
STAGING_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Provision HTTP Basic Auth gate for staging testers
# (Generated locally using htpasswd tool without exposing password in chat)
htpasswd -bc nginx/.htpasswd staging_tester "${STAGING_AUTH_PASSWORD}"

# ==============================================================================
# STEP 3: SEED SYNTHETIC TEST ACCOUNTS ON ISOLATED STAGING DB
# ==============================================================================
# Run seed against instance_staging/staging.db ONLY
DATABASE_URI="sqlite:///instance_staging/staging.db" python seed.py

# ==============================================================================
# STEP 4: LAUNCH CONTAINER STACK
# ==============================================================================
docker compose -f docker-compose.staging.https.yml up -d --build

# ==============================================================================
# STEP 5: AUTOMATED PRE-FLIGHT SMOKE VERIFICATION
# ==============================================================================
# A. Internal Application Healthcheck (HTTP 200)
docker exec eventai_staging_app python -c \
    "import urllib.request, json; res = urllib.request.urlopen('http://127.0.0.1:5000/health'); assert res.getcode() == 200"

# B. Verify HTTP -> HTTPS Redirection (HTTP 301)
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1/ | grep "301"

# C. Verify Basic Auth Enforcement on HTTPS (HTTP 401 Unauthorized)
curl -k -s -o /dev/null -w "%{http_code}\n" https://127.0.0.1/ | grep "401"

# D. Verify Authenticated Staging Access & Noindex Header
curl -k -u staging_tester:${STAGING_AUTH_PASSWORD} -s -I https://127.0.0.1/ | grep -i "x-robots-tag: noindex"
```

---

## 4. Rollback & Emergency Teardown Protocol

If an unexpected defect, TLS validation failure, or security anomaly occurs post-launch:

```bash
# Stop staging containers immediately without deleting data
docker compose -f docker-compose.staging.https.yml stop

# Complete teardown while preserving persistent storage volumes
docker compose -f docker-compose.staging.https.yml down
# CRITICAL RULE: NEVER USE 'docker compose down -v'
```

---

## 5. Execution State Sign-Off

The deployment pipeline is fully specified, hardened, and verified in preflight. Gate B execution is strictly awaiting user authorization.

