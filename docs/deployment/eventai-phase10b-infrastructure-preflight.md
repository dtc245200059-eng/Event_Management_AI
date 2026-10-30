# EventAI Pro — Phase 10B: Infrastructure Preflight & Host Environment Audit

**Document ID**: `DOC-DEPLOY-PHASE10B-PREFLIGHT-002`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10B — Infrastructure Preflight Audit  
**Auditor / Lead Architect**: Senior DevSecOps Engineer & Deployment Architect  
**Host Environment**: Microsoft Windows 11 Home (x64) / Python 3.14.2  
**Date**: 2026-10-29  

---

## 1. Executive Summary

This preflight document records the concrete physical telemetry of the host execution environment, evaluates the feasibility of candidate deployment platforms, and validates path consistency between project configuration files and container orchestration specifications.

---

## 2. Host Toolchain & Capability Telemetry

Empirical probing of system binaries on the host machine yielded the following results:

```
┌────────────────────────────────────────────────────────────────────────┐
│                    HOST SYSTEM CAPABILITY MATRIX                       │
├──────────────────────┬───────────────────────┬─────────────────────────┤
│ Tool / Component     │ Observed System State │ Preflight Assessment    │
├──────────────────────┼───────────────────────┼─────────────────────────┤
│ Operating System     │ Windows 11 Home (x64) │ Host OS                 │
│ Python Virtual Env   │ Python 3.14.2 (.venv) │ OPERATIONAL (218 Tests) │
│ Microsoft Edge       │ msedge.exe v156 Core  │ OPERATIONAL (Headless)  │
│ Docker CLI           │ NOT INSTALLED IN PATH │ CommandNotFound         │
│ Docker Compose       │ NOT INSTALLED IN PATH │ CommandNotFound         │
│ Nginx Daemon         │ NOT INSTALLED IN PATH │ CommandNotFound         │
│ OpenSSL CLI          │ NOT INSTALLED IN PATH │ CommandNotFound         │
│ Port 5000 (Flask Dev)│ FREE (Not listening)  │ Available for binding   │
│ Port 5001 (Staging)  │ FREE (Not listening)  │ Available for binding   │
│ Port 80 (HTTP)       │ FREE (Not listening)  │ Available for binding   │
│ Port 443 (HTTPS)     │ FREE (Not listening)  │ Available for binding   │
└──────────────────────┴───────────────────────┴─────────────────────────┘
```

### Architectural Implications:
1. **Host In-Place Containerization**: The local Windows 11 development machine currently does not have Docker Desktop or Nginx installed in system PATH.
2. **Deployment Platform Decision (Approval Item F)**:
   - **Path A (Recommended / Enterprise)**: Provision an isolated Linux staging VM / cloud instance (Ubuntu 24.04 LTS / Debian 12) with Docker, Docker Compose, and Nginx natively supported.
   - **Path B (Local Container)**: User explicitly authorizes installing Docker Desktop for Windows with WSL2 backend.
   - **Path C (Local Windows Native)**: Run Flask under a production WSGI server for Windows (e.g., Waitress) paired with a standalone Windows port of Nginx.

---

## 3. Path Consistency Audit (Dockerfile vs Docker Compose Bind Mounts)

A forensic comparison between the container image definition (`Dockerfile`) and the staging compose file (`docker-compose.staging.yml`) was conducted to eliminate container filesystem mismatch bugs:

```
[ Dockerfile Inspection ]
Line 5:   WORKDIR /app
Line 25:  COPY . .
          └── Result: Repository root is mapped to /app
              ├── /app/app/                 (Application package)
              ├── /app/app/static/          (Static assets)
              │   ├── /app/app/static/qr_codes/
              │   └── /app/app/static/uploads/
              └── /app/instance/            (SQLite instance directory)
```

```
[ Docker Compose Bind Mount Verification ]
Line 30:  - ./instance_staging:/app/instance
          └── Correct: Mounts host instance_staging to container /app/instance.
Line 32:  - ./app/static/qr_codes_staging:/app/app/static/qr_codes
          └── Correct: Maps staging QR directory directly over package static path.
Line 33:  - ./app/static/uploads_staging:/app/app/static/uploads
          └── Correct: Maps staging upload directory directly over package static path.
```

- **Validation Result**: **100% PATH CONSISTENCY CONFIRMED**.
- The bind mounts correctly target `/app/instance` and `/app/app/static/*` without colliding with the local development database or production assets.

---

## 4. Secret Isolation & Synthetic Environment Plan

In compliance with security directives:
1. Staging will utilize a dedicated, isolated environment file `.env.staging` (derived from `env.staging.example`).
2. Staging `SECRET_KEY` will be generated locally via `python -c "import secrets; print(secrets.token_hex(32))"`. No secrets will be pasted into chat or committed to version control.
3. Database connection string points strictly to `sqlite:///instance/staging.db`, preventing cross-environment contamination.

---

## 5. Preflight Conclusion

The application architecture and path configurations are fully verified. Execution of external containerization and reverse-proxy deployment requires resolution of Approval Items A, E, and F.

