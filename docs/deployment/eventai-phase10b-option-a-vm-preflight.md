# EventAI Pro — Phase 10B Gate B-0: Option A Linux VM Preflight & Architecture Assessment

**Document ID**: `DOC-DEPLOY-PHASE10B-OPT-A-001`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B Gate B-0 — Infrastructure Investigation & Preflight Review  
**Auditor / Lead Architect**: Senior DevSecOps Engineer, Systems Virtualization Specialist & Deployment Architect  
**Deployment Decision**: **OPTION A — Dedicated Ubuntu Linux VM for EventAI Pro HTTPS Staging**  
**Gate B Status**: **CLOSED / BLOCKED (Investigation Only — Zero Network/Software Changes)**  
**Date**: 2026-10-29  

---

## 1. Existing VM Availability & Host Virtualization Audit

In accordance with Section 1 of the Phase 10B Gate B-0 instructions, a comprehensive, read-only audit of the Windows 11 host was conducted to verify the status of VMware Workstation/Player and any existing Ubuntu 24.04 LTS virtual machines:

```
┌────────────────────────────────────────────────────────────────────────┐
│               HOST VIRTUALIZATION & VM AVAILABILITY MATRIX             │
├──────────────────────┬───────────────────────┬─────────────────────────┤
│ System Component     │ Observed System State │ Audit Finding           │
├──────────────────────┼───────────────────────┼─────────────────────────┤
│ VMware Executables   │ None in Program Files │ VMware NOT INSTALLED    │
│ VMware Running Procs │ 0 Processes matching  │ None running            │
│ VMware Services      │ 0 Services in Win SCM │ No VMware service active│
│ Virtual Adapters     │ No VMnet1 / VMnet8    │ Only Physical Ethernet  │
│ Virtual Disks / VMX  │ 0 .vmx files on C: / D: No local VM files found │
│ Existing Ubuntu VM   │ Not accessible on host│ UNREACHABLE / DETACHED  │
│ WordPress / MySQL    │ Zero ports bound      │ No local conflict found │
└──────────────────────┴───────────────────────┴─────────────────────────┘
```

### Forensic Reality:
- Neither VMware Workstation, VMware Player, nor VMware network virtualization services (`vmnat`, `vmnetdhcp`) are currently installed or running on this Windows 11 machine.
- The previously referenced Ubuntu Server 24.04 LTS VM (which ran WordPress and other coursework) is **not physically accessible from this host**. It may reside on a separate physical computer, a detached external drive, an ICTU lab server, or a remote cloud environment.
- **Critical Safety Conclusion**: Because the existing VM cannot be detected locally, **zero interference with existing WordPress or coursework data has occurred or will occur**.

---

## 2. Verified Ubuntu & Docker Details

- **Host Ubuntu Version**: Not installed locally on host.
- **Docker Engine Version**: Not installed in Windows host PATH.
- **Target Ubuntu Specification Required**: **Ubuntu Server 24.04 LTS (Noble Numbat)** 64-bit.
- **Target Docker Engine Specification**: Docker Community Edition v27.x or later with `docker-compose-plugin` (Compose V2).
- **Target Host Compute Requirement**:
  - Minimum: 2 vCPUs, 4 GB RAM, 20 GB free disk space.
  - Recommended: 4 vCPUs, 8 GB RAM, 40 GB SSD.

---

## 3. Existing Services & Port Conflict Analysis

Because EventAI Pro requires ports 80 (HTTP redirect / ACME challenge) and 443 (HTTPS TLS 1.3):
- **On this Windows Host**: Ports 80, 443, 5000, 5001 are 100% free.
- **On the Existing/Previous Ubuntu VM**: Previous records indicated WordPress was deployed on the existing VM, typically binding port 80 or using an existing Nginx/Apache instance with MySQL.
- **Conflict Assessment**: Attempting to co-locate EventAI Pro onto an existing VM hosting WordPress introduces severe operational hazards:
  1. Port 80/443 binding conflicts between WordPress reverse proxy and EventAI Pro reverse proxy.
  2. Risk of breaking existing coursework or academic deliverables.
  3. Complicated certificate renewal collisions in `/etc/letsencrypt/`.

---

## 4. Resource Sufficiency & Dedicated VM Recommendation

### Architecture Decision: **`DEDICATED NEW VM RECOMMENDED`**

Attempting to force EventAI Pro into an existing multi-tenant VM with legacy WordPress services is strongly discouraged:
1. **Zero Contamination**: A clean, dedicated Ubuntu Server 24.04 LTS VM guarantees that EventAI Pro runs in a pristine sandbox with dedicated ports 80/443.
2. **Predictable Performance**: AI RAG multi-agent processing (which takes ~20–30 seconds during intensive multi-turn benchmarking) will not contend with WordPress/MySQL database locks or Apache worker threads.
3. **Coursework Safety**: Guarantees zero risk of accidental corruption, port stealing, or downtime for previous academic coursework.

---

## 5. Proposed Isolated Deployment Topology

```
                          [ Physical Smartphones / Browsers ]
                                          │
                                          │ HTTPS (Port 443 / TLS 1.3)
                                          ▼
                ┌─────────────────────────────────────────────────────────┐
                │          DEDICATED UBUNTU SERVER 24.04 LTS VM           │
                │                                                         │
                │   ┌─────────────────────────────────────────────────┐   │
                │   │           NGINX REVERSE PROXY CONTAINER         │   │
                │   │  - Binds 0.0.0.0:80 (HTTP -> HTTPS 301)         │   │
                │   │  - Binds 0.0.0.0:443 (TLS 1.3 Termination)      │   │
                │   │  - HTTP Basic Auth (.htpasswd for staging)      │   │
                │   │  - X-Robots-Tag: noindex, nofollow, noarchive   │   │
                │   │  - Permissions-Policy: camera=(self)            │   │
                │   └────────────────────────┬────────────────────────┘   │
                │                            │ Internal Bridge Network    │
                │                            ▼                            │
                │   ┌─────────────────────────────────────────────────┐   │
                │   │           EVENTAI PRO FLASK CONTAINER           │   │
                │   │  - Gunicorn 26.2.0 (4 workers)                  │   │
                │   │  - Python 3.12/3.14 + Werkzeug ProxyFix         │   │
                │   │  - Flask StagingConfig (Cookie Secure=True)     │   │
                │   │  - WTF_CSRF_ENABLED = True                      │   │
                │   └────────────────────────┬────────────────────────┘   │
                │                            │ Volume Mount               │
                │                            ▼                            │
                │   ┌─────────────────────────────────────────────────┐   │
                │   │             ISOLATED HOST STORAGE               │   │
                │   │  - SQLite WAL: /var/lib/eventai/staging.db      │   │
                │   │  - QR Codes:   /var/lib/eventai/qr_codes/       │   │
                │   │  - Uploads:    /var/lib/eventai/uploads/        │   │
                │   │  - Hot Backup: 15-min atomic backup script      │   │
                │   └─────────────────────────────────────────────────┘   │
                └─────────────────────────────────────────────────────────┘
```

---

## 6. Network Accessibility & Reachability Analysis

```
┌────────────────────────────────────────────────────────────────────────┐
│                   NETWORK ADAPTER & REACHABILITY MATRIX                │
├──────────────────┬─────────────────────────────┬───────────────────────┤
│ Network Mode     │ Reachable from Host PC?     │ Reachable from Phone? │
├──────────────────┼─────────────────────────────┼───────────────────────┤
│ Bridged Mode     │ YES (Direct LAN IP)         │ **YES (Same Wi-Fi)**  │
│ NAT Mode         │ YES (Via Host NAT Gateway)  │ **NO (Requires P-Fwd)**│
│ Host-Only Mode   │ YES (Host-only subnet)      │ **NO (Completely Iso)│
│ Cloud VM (Public)│ YES (Public IP / FQDN)      │ **YES (4G/5G/Wi-Fi)** │
└──────────────────┴─────────────────────────────┴───────────────────────┘
```

### Critical Smartphone Camera Constraint:
- If a local hypervisor VM is created on the developer LAN:
  - **Bridged Networking MUST be selected** so the VM receives an IP from the home/office router (e.g. `192.168.10.X`).
  - Physical iPhones and Android phones connected to the same Wi-Fi SSID can then communicate directly with the VM.
- If a cloud VM (AWS / DigitalOcean / Hetzner) is provisioned:
  - Accessible from anywhere over standard HTTPS.

---

## 7. Trusted HTTPS & Certificate Strategy

In compliance with W3C Secure Contexts (`window.isSecureContext === true`), the certificate must chain to an operating system root authority:

1. **Option 1: Public ACME HTTP-01 (Let's Encrypt)**:
   - Requires public FQDN (e.g. `staging.eventai.vn` or `eventai-staging.yourdomain.com`).
   - Requires VM port 80 to be publicly accessible to Let's Encrypt validation servers.
2. **Option 2: Public ACME DNS-01 (Let's Encrypt) — STRONGLY RECOMMENDED FOR PRIVATE STAGING**:
   - The VM can stay 100% private inside the local LAN / VPN with zero incoming public firewall ports.
   - Certbot provisions the certificate via DNS TXT record automation (Cloudflare / Route53 / Namecheap API).
   - Generates a **100% publicly trusted certificate** recognized by iOS Safari and Android Chrome without warnings.
3. **Disallowed Methods**:
   - Self-signed certificates without root installation (breaks mobile camera W3C secure context).
   - Plain HTTP LAN access (permanently blocks `navigator.mediaDevices.getUserMedia`).

---

## 8. Data Isolation & Packaging Protocol

EventAI Pro will be packaged and transferred to the Ubuntu VM cleanly without contaminating the local development environment:
1. **Source Code**: Packaged via `tar` or `git archive` excluding:
   - `instance/` (Local SQLite development database is never transferred).
   - `.env` (Development secrets are never transferred).
   - `.venv/` (Windows binaries are never transferred).
   - Academic files (`tailieu/`, `.docx`, `.pptx`).
2. **Staging Environment File** (`.env.staging`):
   - Generated fresh on the Linux VM.
   - Cryptographically random `SECRET_KEY` generated via `python3 -c "import secrets; print(secrets.token_hex(32))"`.
3. **Synthetic Database Seeding**:
   - Initialized on the VM using `python3 seed.py` into `/var/lib/eventai/staging.db`.
   - Uses synthetic accounts only: `staff@eventai.vn`, `attendee@eventai.vn`.

---

## 9. Security Risks & Mitigation Controls

| Identified Security Hazard | Likelihood | Impact | Built-in Mitigation Mechanism |
|---|:---:|:---:|---|
| Public search crawler indexing | High | Medium | Nginx enforces `X-Robots-Tag: noindex, nofollow, noarchive` across 100% of routes. |
| Unauthorized public tampering | Medium | High | Nginx enforces HTTP Basic Auth (`.htpasswd`) before reaching Flask application. |
| CSRF attacks on staging routes | Low | High | `Flask-WTF` `CSRFProtect` active on all 34 state-changing POST routes. |
| Cross-user ticket scraping (IDOR) | Low | High | `@app.before_request` restricts `/static/qr_codes/` to ticket owners and staff. |
| Session hijacking over Wi-Fi | Low | High | `SESSION_COOKIE_SECURE=True` and `SESSION_COOKIE_HTTPONLY=True`. |

---

## 10. Missing Information & Required User Approvals (For Gate B)

Before any infrastructure provisioning or network configuration can proceed, the user must provide decisions on the following 6 items:

1. **Target VM Location**:
   - [ ] Provision a clean dedicated Ubuntu VM on a local hypervisor (VMware / Hyper-V / VirtualBox).
   - [ ] Provision a dedicated Ubuntu 24.04 cloud VM (e.g., DigitalOcean, AWS, GCP, Azure).
   - [ ] Provide connection details for an existing external Linux server.
2. **Staging Domain / FQDN**:
   - The domain name to be assigned to the staging host (e.g. `staging.yourdomain.com`).
3. **TLS Validation Method**:
   - [ ] ACME DNS-01 (Recommended for private LAN staging; zero public ports needed).
   - [ ] ACME HTTP-01 (Requires public IP and port 80 open).
   - [ ] Organization Wildcard Certificate (User supplies cert/key securely).
4. **Network Exposure Level**:
   - [ ] Private LAN / Wi-Fi only (with HTTP Basic Auth).
   - [ ] Restricted Public Endpoint (with HTTP Basic Auth).
5. **Port Authorization**:
   - Explicit confirmation to bind ports 80 and 443 on the staging VM.
6. **Physical Test Devices**:
   - Confirmation that an iPhone (iOS 16+) and an Android (Chrome 120+) are ready to connect to the staging network for camera QR check-in.

---

## 11. Final Decision

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PHASE 10B GATE B-0 FINAL DECISION                    │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                 >>> DEDICATED NEW VM RECOMMENDED <<<                   │
│                                                                        │
│   1. The existing Ubuntu VM cannot be located or accessed on this host. │
│   2. Co-locating EventAI Pro with existing WordPress coursework risks  │
│      port conflicts and unintended academic disruption.                │
│   3. A clean, dedicated Ubuntu Server 24.04 LTS VM provides 100%       │
│      isolation, guaranteed port 80/443 availability, and clean TLS.    │
│   4. Gate B remains strictly CLOSED awaiting user approval for VM      │
│      provisioning and the 6 infrastructure parameters.                 │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

