# EventAI Pro — Phase 10B: Approval Gates & Operational Scope

**Document ID**: `DOC-DEPLOY-PHASE10B-SCOPE-001`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B — Controlled HTTPS Staging & Real-Device Acceptance  
**Current Gate**: **GATE A COMPLETED — GATE B APPROVAL REQUIRED**  
**Auditor / Lead Architect**: Senior DevSecOps Engineer & Release Acceptance Manager  
**Date**: 2026-10-29  

---

## 1. Executive Summary & Gate Architecture

Phase 10B bridges the gap between local architecture preparation (Phase 10A) and physical deployment to an HTTPS staging environment. To protect application security, user infrastructure, and network boundaries, Phase 10B enforces two strict, sequential execution gates:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      PHASE 10B DUAL-GATE ARCHITECTURE                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   [ GATE A: Read-Only Verification & Preflight Preparation ]           │
│   - Baseline regression re-execution (218/218 passing).                │
│   - Local host toolchain audit (Docker/Nginx/OpenSSL availability).    │
│   - Dockerfile, working directory, and storage mount path audit.       │
│   - Dedicated Phase 10B preflight backup with SHA-256 hashes.          │
│   - HSTS policy risk analysis and ProxyFix trust parameter review.     │
│   STATUS: 100% COMPLETE & VERIFIED (AUTONOMOUS SCOPE)                  │
│                                                                        │
│                                   │                                    │
│                                   ▼                                    │
│   [ MANDATORY INFRASTRUCTURE APPROVAL GATE (ITEMS A THROUGH H) ]       │
│   - Explicit user sign-off required prior to any network exposure.     │
│   STATUS: PENDING EXPLICIT USER DECISION                               │
│                                                                        │
│                                   │                                    │
│                                   ▼                                    │
│   [ GATE B: External Staging Deployment & Real-Device QA ]             │
│   - Port binding, DNS configuration, and firewall modifications.       │
│   - Trusted TLS certificate issuance / provisioning.                   │
│   - Multi-container staging stack activation.                          │
│   - Genuine physical smartphone camera QR check-in on iOS & Android.   │
│   STATUS: BLOCKED / GATED PENDING GATE B USER APPROVAL                 │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> The Phase 10A completion report does **not** constitute Gate B approval. Neither does the prompt itself. In accordance with release governance guidelines, Gate B execution is strictly halted until the user explicitly resolves the 8 approval parameters.

---

## 2. The 8 Mandatory Infrastructure Approval Parameters (A through H)

Before any network-exposing action, port opening, or container deployment is executed, the user must provide explicit instruction for:

| Item | Parameter Description | Preflight Assessment & Requirement | Status |
|:---:|---|---|:---:|
| **A** | **Exact Staging Host / Server** | Local development machine (`localhost`) vs dedicated Linux staging VM / cloud instance. Local host lacks Docker/Nginx in PATH. | **PENDING** |
| **B** | **Intended Staging Hostname** | Fully Qualified Domain Name (e.g. `staging.eventai.vn` or private internal DNS). Do not assume example domains belong to the user. | **PENDING** |
| **C** | **TLS Validation Method** | Public ACME HTTP-01 / DNS-01 via Let's Encrypt vs pre-existing organization wildcard certificate. Self-signed certs are prohibited (breaks mobile camera W3C Secure Context). | **PENDING** |
| **D** | **Network Reachability** | Restricted internal LAN / VPN only vs restricted public endpoint with HTTP Basic Auth / IP allowlist. | **PENDING** |
| **E** | **Authorized Ports & Firewall** | Explicit permission to open ports 80 (HTTP redirect) and 443 (HTTPS) on host firewall. | **PENDING** |
| **F** | **Deployment Platform** | Windows native Python service vs WSL2 Linux vs Docker / Docker Compose on staging server. | **PENDING** |
| **G** | **Physical Mobile Test Devices** | Availability of real physical iPhone (iOS Safari 16+) and Android (Chrome 120+) connected to the staging network for camera QR check-in. | **PENDING** |
| **H** | **Secret Provisioning Method** | Local `.env.staging` file generation with cryptographically random keys. No plaintext secrets or private keys in chat. | **PENDING** |

---

## 3. Strict Preflight Operational Boundaries

During Gate A execution:
1. **Zero Public Exposure**: No ports are opened; no tunnels (ngrok, cloudflare) are initialized.
2. **Zero Live Database Mutation**: `instance/event_management.db` is strictly read-only and unmounted.
3. **Zero Git Modification**: No commits, no pushes, no resets, no branch manipulation.
4. **Zero Untrusted Certificate Generation**: No untrusted root CAs installed in system stores.
5. **Zero Synthetic Claims**: Test results and mobile camera status are recorded with absolute honesty based on actual physical execution.

---

## 4. Conclusion & Gate A Sign-Off

Gate A verification is completed. The codebase is healthy, stable, and ready for deployment the instant Gate B authorization is granted.

