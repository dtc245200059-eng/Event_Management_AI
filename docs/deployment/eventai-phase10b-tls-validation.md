# EventAI Pro — Phase 10B: TLS Certificate Validation & HSTS Policy Review

**Document ID**: `DOC-DEPLOY-PHASE10B-TLS-003`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B — TLS Architecture & Policy Audit  
**Auditor / Lead Architect**: Senior TLS Security Engineer & Infrastructure Architect  
**Current Status**: **BLOCKED PENDING USER DOMAIN & CERTIFICATE STRATEGY (ITEM B & C)**  
**Date**: 2026-10-29  

---

## 1. Executive Summary & Domain Governance

In accordance with Section 4 of the deployment specification:
1. **Zero Domain Assumptions**: Example hostnames (such as `staging.eventai.vn` or `staging.local`) are strictly architectural placeholders and must never be presumed to belong to the user without explicit confirmation.
2. **Prohibition of Self-Signed Certificates**: Untrusted self-signed certificates require testers to bypass browser TLS warnings. Mobile browsers (iOS Safari, Android Chrome) treat bypassed self-signed origins as **untrusted**, which permanently disables W3C Secure Context APIs and blocks camera check-in (`getUserMedia`).
3. **Private IP Limitation**: Public Certificate Authorities (such as Let's Encrypt) do not issue publicly trusted TLS certificates to RFC 1918 private IPv4 addresses (e.g. `192.168.x.x` or `10.x.x.x`). A valid FQDN is mandatory for trusted public TLS.

---

## 2. Evaluation of Candidate TLS Issuance Strategies

| Issuance Strategy | Network Requirements | Firewall / Port Exposure | Suitability for Staging | Approval Needed |
|---|---|---|---|:---:|
| **Strategy 1: ACME HTTP-01** (Let's Encrypt) | Publicly reachable FQDN pointing to staging IP. | Port 80 open to public Internet for challenge validation. | Excellent for public staging endpoints. | User owns domain; approves opening port 80. |
| **Strategy 2: ACME DNS-01** (Let's Encrypt) | Domain DNS managed via supported provider API (Cloudflare, Route53, etc.). | **Zero public ports required**. Staging can remain purely internal on private LAN/VPN. | **Recommended for Private Staging** (most secure). | User provides delegated DNS API credentials. |
| **Strategy 3: Existing Wildcard Certificate** | Organization pre-issued certificate (`*.domain.com`). | Zero ACME challenges required. | Ideal if organization has existing PKI. | User provides cert/key via secure local provisioning. |
| **Strategy 4: Untrusted Self-Signed / Local CA** | Local generation via OpenSSL / mkcert. | None. | **DISALLOWED**: Mobile devices reject camera access on untrusted certificates. | N/A |

---

## 3. Conservative Staging HSTS Policy Review

### 3.1 The Danger of Overly Aggressive HSTS on Staging
In Phase 10A, the proposed HSTS header was:
`Strict-Transport-Security: max-age=31536000; includeSubDomains`

**Security Risk Analysis**:
- Setting `max-age=31536000` (1 full year) with `includeSubDomains` instructs client browsers to cache the HTTPS-only policy across **every single subdomain** under the root domain.
- If staging experiences a certificate lapse, or if unrelated subdomains under the parent organization do not yet support HTTPS, users' browsers will hard-block all connections without an override option.
- `preload` must never be added to staging environments, as removing a domain from the Chrome/Firefox HSTS preload list can take months.

### 3.2 The Reconciled Conservative Staging Policy
For the EventAI Pro HTTPS staging deployment, the HSTS policy is revised to a host-specific, gradual ramp-up policy:

```nginx
# Phase 1: Initial Staging Verification (24-hour host-specific trial)
# Excludes 'includeSubDomains' and excludes 'preload'
add_header Strict-Transport-Security "max-age=86400" always;

# Phase 2: Post-Verification Stable Staging (Only after 7 days of 100% uptime)
# add_header Strict-Transport-Security "max-age=2592000" always; # 30 days
```

---

## 4. Reverse Proxy Trust & ProxyFix Parameter Hardening

Werkzeug's `ProxyFix` middleware must only trust headers from explicit, verified upstream proxies. Blindly enabling all trust parameters exposes the application to client-spoofed `X-Forwarded-For` and `X-Forwarded-Proto` attacks.

```python
# Verified Production/Staging Configuration:
from werkzeug.middleware.proxy_fix import ProxyFix

# Behind a SINGLE trusted Nginx reverse proxy:
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,      # Trust ONLY the 1 immediate Nginx proxy for client IP
    x_proto=1,    # Trust ONLY the 1 immediate Nginx proxy for scheme (https)
    x_host=1,     # Trust ONLY the 1 immediate Nginx proxy for Host header
    x_port=1,     # Trust ONLY the 1 immediate Nginx proxy for port
    x_prefix=0    # Do NOT trust forwarded prefix unless explicitly mounted under sub-path
)
```

### Upstream Nginx Header Sanitization:
In `nginx/staging.conf`, incoming client-supplied `X-Forwarded-*` headers are stripped and overwritten with the trusted values:
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $remote_addr; # Resets client-supplied spoofed IPs
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
```

---

## 5. TLS Validation Sign-Off Status

Because the staging hostname and certificate issuance method require user selection under Approval Items B and C, physical TLS validation and real-device camera testing are formally recorded as **BLOCKED (PENDING USER SELECTION)**.

