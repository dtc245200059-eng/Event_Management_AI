# EventAI Pro — Phase 10B-R: Host Infrastructure & Toolchain Capability Audit

**Document ID**: `DOC-DEPLOY-PHASE10BR-HOST-004`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B-R — Infrastructure Reality Review  
**Auditor / Lead Architect**: Senior DevSecOps Deployment Architect & Systems Engineer  
**Host Machine**: Windows 11 Home (x64)  
**Date**: 2026-10-29  

---

## 1. Executive Summary

This document establishes the verified inventory of tools, runtimes, and system services physically present on the Windows 11 host machine.

It differentiates between software confirmed to be operational, software absent from PATH, and software that cannot be introduced without explicit user authorization.

---

## 2. Granular Host Toolchain Inventory

```
┌────────────────────────────────────────────────────────────────────────┐
│                   WINDOWS 11 HOST CAPABILITY MATRIX                    │
├──────────────────────┬───────────────────────┬─────────────────────────┤
│ Component / Tool     │ Observed System State │ Operational Status      │
├──────────────────────┼───────────────────────┼─────────────────────────┤
│ Operating System     │ Windows 11 Home (x64) │ Host OS                 │
│ Python Runtime       │ Python 3.14.2 (.venv) │ INSTALLED & VERIFIED    │
│ Pytest Framework     │ pytest 9.1.1 (.venv)  │ INSTALLED & VERIFIED    │
│ MS Edge Browser      │ msedge.exe v156 Core  │ INSTALLED & VERIFIED    │
│ Git Version Control  │ git.exe 2.4x          │ INSTALLED & VERIFIED    │
│ Windows Subsystem WSL│ Feature enabled       │ NO DISTRIBUTIONS (0)    │
│ Docker Engine / CLI  │ NOT IN PATH           │ CommandNotFound         │
│ Docker Compose       │ NOT IN PATH           │ CommandNotFound         │
│ Nginx Reverse Proxy  │ NOT IN PATH           │ CommandNotFound         │
│ OpenSSL Cryptography │ NOT IN PATH           │ CommandNotFound         │
│ Port 80 (HTTP)       │ Unbound / Inactive    │ FREE                    │
│ Port 443 (HTTPS)     │ Unbound / Inactive    │ FREE                    │
│ Port 5000 (Flask Dev)│ Unbound / Inactive    │ FREE                    │
│ Port 5001 (Staging)  │ Unbound / Inactive    │ FREE                    │
└──────────────────────┴───────────────────────┴─────────────────────────┘
```

---

## 3. Toolchain Status Categorization

### Category 1: Installed & Verified Operational
1. **Python Virtual Environment (`.venv`)**:
   - Python 3.14.2 (64-bit).
   - Contains all required project dependencies: Flask 3.1.3, Flask-WTF 1.3.0, SQLAlchemy 2.0.52, Gunicorn 26.2.0, Jinja2 3.1.6, Werkzeug 3.1.8.
   - 218/218 automated tests pass cleanly in 73 seconds.
2. **Microsoft Edge Core Chromium**:
   - Binary location: `C:\Program Files (x86)\Microsoft\EdgeCore\156.0.4314.50\msedge.exe`.
   - Verified headless execution, DOM compilation, and screenshot generation.

### Category 2: Software Not Found in PATH / Not Installed
1. **Docker & Docker Compose**:
   - Running `docker --version` or `docker compose version` yields PowerShell `CommandNotFoundException`.
   - Docker Desktop is not running and not registered in system PATH.
2. **Nginx Daemon**:
   - Neither Linux Nginx nor Windows native Nginx is installed in system PATH.
3. **OpenSSL**:
   - `openssl.exe` is not available from the Windows shell.
4. **WSL2 Linux Distributions**:
   - `wsl.exe -l -v` returns: *"Windows Subsystem for Linux has no installed distributions."*

### Category 3: Software Requiring Explicit User Approval
The following operations would alter the host operating system and are **strictly halted at Gate A**:
- Downloading/installing Docker Desktop for Windows.
- Running `wsl --install -d Ubuntu` to provision a Linux guest.
- Modifying Windows Defender Firewall rules for incoming ports 80/443.
- Installing third-party certificate authority utilities (e.g. mkcert).

---

## 4. Conclusion & Deployment Feasibility

Because Docker and Nginx are absent on this Windows host, **direct local containerized staging cannot be launched without user approval to install infrastructure software**.

This reality informs the three staging deployment options detailed in `docs/deployment/eventai-phase10br-staging-options.md`.

