# EventAI Pro — Phase 10B-R: Staging Network & Deployment Options Review

**Document ID**: `DOC-DEPLOY-PHASE10BR-OPTS-005`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B-R — Infrastructure Strategy & Deployment Review  
**Auditor / Lead Architect**: Senior DevSecOps Deployment Architect & Cloud Systems Engineer  
**Date**: 2026-10-29  

---

## 1. Executive Summary

Based on the verified reality of the host machine (Windows 11 with Python and Edge, but lacking Docker and Nginx), three distinct, actionable staging deployment paths are presented for user consideration.

The release engineer will not select a target host, provision infrastructure, or request TLS certificates until the user explicitly approves one of these options.

---

## 2. Comparative Evaluation of the 3 Staging Deployment Options

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STAGING DEPLOYMENT OPTIONS MATRIX                               │
├──────────────────────┬────────────────────────┬───────────────────────┬────────────────┤
│ Evaluation Attribute │ OPTION A (Linux Staging│ OPTION B (Windows Host│ OPTION C (Local│
│                      │ Dedicated Server / VM) │ Docker Desktop / WSL2)│ host-Only WSGI)│
├──────────────────────┼────────────────────────┼───────────────────────┼────────────────┤
│ Production Parity    │ IDENTICAL (Full Stack) │ VERY HIGH             │ LOW            │
│ Host OS Modification │ ZERO (Remote instance) │ HIGH (Install Docker) │ ZERO (Current) │
│ Mobile Device Camera │ UNBLOCKED (Trusted TLS)│ FEASIBLE (Via WiFi/LAN│ BLOCKED        │
│ TLS Certificate Feas.│ Let's Encrypt (Autom.) │ ACME DNS-01 or PortFwd│ Localhost only │
│ Network Exposure     │ Restricted Public/VPN  │ Local LAN / PortFwd   │ 127.0.0.1 Only │
│ Docker Requirement   │ Native Linux Engine    │ Docker Desktop + WSL2 │ NONE           │
│ Staging Data Isolat. │ Isolated host mounts   │ Isolated host mounts  │ Isolated DB file
│ User Approvals Req.  │ SSH/Host access        │ Host software install │ Current session│
│ Operational Risk     │ LOW (Isolated target)  │ MODERATE (Host load)  │ ZERO           │
├──────────────────────┼────────────────────────┼───────────────────────┼────────────────┤
│ RECOMMENDATION       │ **STRONGLY RECOMMENDED**│ VIABLE ALTERNATIVE    │ DEV-ONLY FALLB.│
└──────────────────────┴────────────────────────┴───────────────────────┴────────────────┘
```

---

## 3. Detailed Option Breakdown

### OPTION A: Dedicated Linux VM or Server with Isolated Docker Staging (STRONGLY RECOMMENDED)

- **Description**: Deploy `docker-compose.staging.https.yml` to an independent Linux virtual machine or cloud instance (Ubuntu 24.04 LTS / Debian 12) managed by the organization.
- **Required Software**: Docker Engine, Docker Compose plugin, Nginx, Certbot.
- **Installation Requirements**: Standard package installation on the remote Linux host (`apt install docker.io docker-compose-v2`).
- **Network Exposure**: Can be bound to private VPN / corporate intranet, or exposed to the public Internet behind HTTP Basic Auth.
- **TLS Feasibility**: Seamless Let's Encrypt automated ACME HTTP-01 or DNS-01 certificate issuance.
- **Mobile-Device Reachability**: **EXCELLENT**. Physical iPhones and Android phones connect directly over WiFi/Internet to the trusted staging FQDN with valid OS-trusted TLS, **unblocking camera QR check-in**.
- **Data Isolation**: Persistent volumes mounted strictly in `/var/lib/eventai_staging/`. Zero touch of development laptop files.
- **User Approvals Needed**: Target server IP/FQDN, SSH access or CI/CD deployment authorization.
- **Operational Risks**: Minimal; complete decoupling from local developer workstation.

---

### OPTION B: Existing Windows Host with Approved Additional Infrastructure

- **Description**: Install Docker Desktop on the local Windows 11 machine and run the staging compose stack via WSL2.
- **Required Software**: Docker Desktop for Windows, WSL2 Linux kernel, Ubuntu distro (`wsl --install -d Ubuntu`).
- **Installation Requirements**: Requires downloading Docker Desktop (~600MB), enabling Hyper-V/VirtualMachinePlatform features, and rebooting.
- **Network Exposure**: Requires modifying Windows Firewall to accept incoming TCP traffic on ports 80 and 443 from the local LAN.
- **TLS Feasibility**: Let's Encrypt HTTP-01 is difficult if the developer machine sits behind a home NAT router without port forwarding. ACME DNS-01 or an organization wildcard certificate is required.
- **Mobile-Device Reachability**: Feasible if smartphones connect to the same WiFi network and DNS resolves to the Windows host's LAN IP.
- **Data Isolation**: Host mounts mapped to `./instance_staging` and `./app/static/*_staging`.
- **User Approvals Needed**: Explicit approval to install Docker Desktop and modify Windows firewall.
- **Operational Risks**: Moderate; host memory consumption (WSL2 Vmmem), NAT bridging nuances between Windows and mobile devices.

---

### OPTION C: Localhost-Only Windows Staging for Continued Desktop Testing (FALLBACK)

- **Description**: Run EventAI Pro locally using Python in `StagingConfig` bound strictly to `127.0.0.1:5001`.
- **Required Software**: Existing Python `.venv` (no external tools required).
- **Installation Requirements**: None.
- **Network Exposure**: Strictly internal loopback (`127.0.0.1`). Zero external exposure.
- **TLS Feasibility**: Chromium/Edge treats `http://localhost` or `http://127.0.0.1` as a **Secure Context** for desktop testing, but lacks genuine TLS.
- **Mobile-Device Reachability**: **PERMANENTLY BLOCKED**. Physical smartphones cannot reach `127.0.0.1` of the developer laptop.
- **Data Isolation**: Database points to `instance/staging_local.db`.
- **User Approvals Needed**: None (Runs autonomously within local environment).
- **Operational Risks**: Zero risk, but **fails to satisfy mobile camera acceptance requirements**.

---

## 4. Architectural Recommendation

To genuinely unblock the real mobile camera check-in release blocker, **Option A is the optimal and industry-standard path**. If remote server infrastructure is not immediately available, Option B can be authorized, or Option C can be used as an interim step for extended desktop QA.

