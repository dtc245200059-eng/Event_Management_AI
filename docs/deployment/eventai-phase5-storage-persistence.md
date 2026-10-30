# EventAI Pro — Phase 5 Storage Persistence & Container Volume Specification

**Specification Date:** 2026-10-29  
**DevSecOps Specialist:** Senior Storage Reliability & Container Architecture Engineer  
**Target Environments:** Isolated Staging (Docker & Bare Metal Linux)  
**Database Engine:** SQLite 3 (Rollback Journal & WAL Modes)  
**Status:** **VERIFIED PERSISTENCE SPECIFICATION**

---

## 1. Storage Architecture & Runtime Assets

The persistence model of EventAI Pro encompasses three distinct categories of stateful files that must survive application restarts, container redeployments, and host reboots:

| Storage Asset | Host Path (Production) | Host Path (Staging) | Container Mount Point | Description & Lifecycle |
| :--- | :--- | :--- | :--- | :--- |
| **Relational Database** | `instance/event_management.db` | `./instance_staging/staging.db` | `/app/instance` | Primary ACID database storing all 9 relational entities. |
| **WAL & Shared Memory**| `instance/*.db-wal`, `*.db-shm` | `./instance_staging/*.db-wal` | `/app/instance` | Write-Ahead Log journal and memory-mapped shared indices. |
| **Generated QR Codes** | `app/static/qr_codes/` | `./app/static/qr_codes_staging/` | `/app/app/static/qr_codes` | Scalable SVG ticket tokens and check-in dynamic codes. |
| **Static Uploads** | `app/static/uploads/` | `./app/static/uploads_staging/` | `/app/app/static/uploads` | High-resolution event banners, venue floorplans, avatars. |

---

## 2. Container Volume Defect Analysis & Remediation

### 2.1 The Container Ephemeral Storage Defect
In Phase 4, an audit of the baseline [`docker-compose.yml`](file:///d:/Event_Management_AI/docker-compose.yml) identified a critical architectural gap:
```yaml
# DEFECTIVE CONFIGURATION IN BASELINE COMPOSE:
volumes:
  - ./app/static/qr_codes:/app/app/static/qr_codes
  - ./app/static/uploads:/app/app/static/uploads
  # NOTE: The instance/ directory is omitted!
```
- **Consequence:** In Flask applications, relative SQLite connection strings (`sqlite:///event_management.db`) default to `app.instance_path` (`/app/instance/event_management.db`).
- Because `/app/instance` resided in the container's disposable writable layer, executing `docker compose down` and `docker compose up` permanently destroyed all attendee registrations, created events, and ticket counts.

### 2.2 Isolated Staging Resolution (`docker-compose.staging.yml`)
To guarantee complete persistence while isolating staging rehearsal from production data:
```yaml
services:
  eventai-staging:
    image: eventai-pro:staging
    volumes:
      # 1. Dedicated Staging Database Directory (Contains .db, .db-wal, .db-shm)
      - ./instance_staging:/app/instance
      # 2. Dedicated Staging QR Codes
      - ./app/static/qr_codes_staging:/app/app/static/qr_codes
      # 3. Dedicated Staging Uploads
      - ./app/static/uploads_staging:/app/app/static/uploads
```
- **Directory Separation:** Production data in `instance/` remains untouched.
- **Atomic WAL Coverage:** Mounts the entire `/app/instance` directory rather than individual file bind-mounts, ensuring that temporary WAL (`.db-wal`) and shared-memory (`.db-shm`) files are preserved together.

---

## 3. SQLite File Locking & Network Storage Constraints

> [!WARNING]
> **NEVER host SQLite database files on network filesystems (NFS, SMB/CIFS, GlusterFS, or AWS EFS).**

1. **POSIX Advisory Lock Limitations:** Network storage protocols often implement buggy, non-conformant, or asynchronously cached advisory byte-range locks. When multiple worker threads or processes attempt concurrent writes across an NFS mount, locks may succeed simultaneously on different nodes, resulting in catastrophic database corruption.
2. **Local Storage Mandate:** For staging and production deployments, SQLite databases must reside on a **local POSIX-compliant block device** (SSD, NVMe, or AWS EBS / Google Cloud Persistent Disk with ext4/XFS filesystems).

---

## 4. Bare Metal & Virtual Machine File System Permissions

On non-containerized Linux staging servers (`/var/www/eventai`):
```bash
# Set ownership to unprivileged web server process user
sudo chown -R www-data:www-data /var/www/eventai/instance
sudo chown -R www-data:www-data /var/www/eventai/app/static/qr_codes
sudo chown -R www-data:www-data /var/www/eventai/app/static/uploads

# Restrict directory access strictly to process owner (read/write/traverse)
sudo chmod 700 /var/www/eventai/instance

# Restrict SQLite files strictly to read/write by owner
sudo chmod 600 /var/www/eventai/instance/*.db
```

---

## 5. Graceful Container Shutdown & WAL Checkpoint Flushing

When Docker stops a container, it dispatches `SIGTERM`, waits a grace period (`stop_grace_period`, default 10 seconds), and sends `SIGKILL` if the process has not exited:
- **Risk:** If Gunicorn workers are terminated abruptly by `SIGKILL`, SQLite transactions in the `.db-wal` file may remain uncheckpointed. While SQLite recovers cleanly on the next startup, clean checkpoints keep file sizes small.
- **Mitigation:** In Compose and systemd specifications, configure a generous grace period:
  ```yaml
  stop_grace_period: 30s
  ```
  This provides Gunicorn workers sufficient time to commit open transactions, flush WAL pages back into the main database, and close connections gracefully.

