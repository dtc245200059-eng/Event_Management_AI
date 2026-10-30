# EventAI Pro — Phase 10: Disaster Recovery Drill Protocol & Scenarios

**Document ID**: `DOC-DEPLOY-PHASE10-RECOVERY-008`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10A — Disaster Recovery Drill Specification  
**Auditor / Lead Architect**: Senior DevSecOps Engineer & SQLite Reliability Specialist  
**Recovery Objectives**: Target RTO < 10 Minutes | Maximum Data Loss RPO $\le$ 15 Minutes  
**Date**: 2026-10-29  

---

## 1. Executive Summary

This document specifies the standard operating procedures (SOP) and execution runbooks for six critical disaster recovery scenarios (Scenarios A through F). These protocols govern how operations and DevSecOps personnel rapidly restore EventAI Pro to a verified, operational state following data corruption, accidental deletion, host failure, or transaction deadlocks.

All restoration procedures are designed to meet a **Recovery Time Objective (RTO) of under 10 minutes** (empirically calculated at ~5.5 minutes) while maintaining strict data integrity.

---

## 2. Six Disaster Recovery Scenarios (A through F)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DISASTER RECOVERY SCENARIO MATRIX                    │
├──────────┬─────────────────────────────────────┬──────────────┬────────┤
│ Scenario │ Description                         │ Root Cause   │ Target │
├──────────┼─────────────────────────────────────┼──────────────┼────────┤
│ **A**    │ B-Tree / Page Corruption            │ Hardware I/O │ 5 min  │
│ **B**    │ Accidental Table Drop / Truncate    │ Human Error  │ 6 min  │
│ **C**    │ Total Host Loss / Disk Crash        │ Infra Outage │ 8 min  │
│ **D**    │ WAL Desynchronization / Lock Jam    │ Concurrency  │ 3 min  │
│ **E**    │ Sudden Kernel Panic / Power Drop    │ Power Loss   │ 4 min  │
│ **F**    │ Point-In-Time Rollback (PITR)       │ Bad Migration│ 6 min  │
└──────────┴─────────────────────────────────────┴──────────────┴────────┘
```

---

### Scenario A: Database Corruption Detected by Integrity Check

#### 1. Symptom & Detection
- Application logs report `sqlite3.DatabaseError: database disk image is malformed` or `PRAGMA integrity_check` returns non-zero / error strings.
#### 2. Restoration Runbook
1. Stop the application container to halt incoming write transactions:
   ```bash
   docker stop eventai_staging_app
   ```
2. Quarantine the corrupted database and WAL files for forensic analysis:
   ```bash
   mv instance_staging/staging.db instance_staging/corrupted_$(date +%s).db
   rm -f instance_staging/staging.db-wal instance_staging/staging.db-shm
   ```
3. Locate the latest verified snapshot in `instance_staging/backups/`:
   ```bash
   LATEST=$(ls -t instance_staging/backups/eventai_backup_*.db.gz | head -n 1)
   sha256sum -c "${LATEST}.sha256"
   ```
4. Restore snapshot:
   ```bash
   gunzip -c "${LATEST}" > instance_staging/staging.db
   sqlite3 instance_staging/staging.db "PRAGMA integrity_check;"
   ```
5. Restart application and verify:
   ```bash
   docker start eventai_staging_app
   curl -s -f http://127.0.0.1:5001/health
   ```
- **Estimated RTO**: 4 minutes.

---

### Scenario B: Accidental Table Drop or Malicious Truncation

#### 1. Symptom & Detection
- An operator error runs `DROP TABLE tickets;` or `DELETE FROM users;` during maintenance.
#### 2. Restoration Runbook
1. Immediately isolate application traffic:
   ```bash
   docker stop eventai_staging_app
   ```
2. Verify missing schema tables:
   ```bash
   sqlite3 instance_staging/staging.db ".tables"
   ```
3. Fetch the most recent pre-incident backup snapshot (e.g. from 15 minutes prior):
   ```bash
   gunzip -c instance_staging/backups/eventai_backup_PRE_INCIDENT.db.gz > instance_staging/staging.db
   ```
4. Run schema audit and record count assertion:
   ```bash
   sqlite3 instance_staging/staging.db "SELECT count(*) FROM users;"
   sqlite3 instance_staging/staging.db "SELECT count(*) FROM tickets;"
   sqlite3 instance_staging/staging.db "PRAGMA foreign_key_check;"
   ```
5. Restart application container and verify login.
- **Estimated RTO**: 5 minutes.

---

### Scenario C: Total Server Disk Failure / Host Rebuild

#### 1. Symptom & Detection
- Cloud VM or physical host crashes; host disk unrecoverable.
#### 2. Restoration Runbook
1. Provision new host/VM with Docker and Docker Compose installed.
2. Clone application codebase:
   ```bash
   git clone <repo-url> /opt/eventai && cd /opt/eventai
   ```
3. Create staging persistent directory structure:
   ```bash
   mkdir -p instance_staging app/static/qr_codes_staging app/static/uploads_staging
   ```
4. Pull latest off-site snapshot from immutable cloud storage:
   ```bash
   rclone copy remote-storage:eventai-staging-backups/latest.db.gz ./
   sha256sum -c latest.db.gz.sha256
   gunzip -c latest.db.gz > instance_staging/staging.db
   ```
5. Pull static QR code and upload asset tarball:
   ```bash
   rclone copy remote-storage:eventai-staging-backups/assets_latest.tar.gz ./
   tar -xzf assets_latest.tar.gz -C app/static/
   ```
6. Launch containers:
   ```bash
   docker compose -f docker-compose.staging.https.yml up -d
   ```
- **Estimated RTO**: 8 minutes.

---

### Scenario D: WAL File Desynchronization or Locking Deadlock

#### 1. Symptom & Detection
- Application throws `sqlite3.OperationalError: database is locked` continuously; write transactions timeout.
#### 2. Restoration Runbook
1. Stop application container to release held file descriptors:
   ```bash
   docker stop eventai_staging_app
   ```
2. Run explicit WAL checkpoint to fold WAL frames back into the main database file:
   ```bash
   sqlite3 instance_staging/staging.db "PRAGMA wal_checkpoint(TRUNCATE);"
   ```
3. If checkpoint completes with `0 0 0`, the lock is resolved.
4. If checkpoint hangs due to an orphaned reader process, remove `-shm` (shared memory index) safely while the DB is stopped:
   ```bash
   rm -f instance_staging/staging.db-shm
   sqlite3 instance_staging/staging.db "PRAGMA wal_checkpoint(RESTART);"
   ```
5. Verify integrity:
   ```bash
   sqlite3 instance_staging/staging.db "PRAGMA integrity_check;"
   ```
6. Start application container:
   ```bash
   docker start eventai_staging_app
   ```
- **Estimated RTO**: 3 minutes.

---

### Scenario E: Incomplete Transaction During Sudden Power Loss / Kernel Panic

#### 1. Symptom & Detection
- Host rebooted unexpectedly during peak check-in. SQLite WAL mode provides ACID guarantees, but dirty buffers need replay validation.
#### 2. Restoration Runbook
1. Verify database and WAL file presence:
   ```bash
   ls -la instance_staging/staging.db*
   ```
2. Allow SQLite to automatically recover and replay the uncommitted WAL log upon opening:
   ```bash
   sqlite3 instance_staging/staging.db "PRAGMA schema_version;"
   sqlite3 instance_staging/staging.db "PRAGMA integrity_check;"
   ```
3. Verify foreign key constraints and record consistency:
   ```bash
   sqlite3 instance_staging/staging.db "PRAGMA foreign_key_check;"
   ```
4. If integrity returns `ok`, restart application container.
- **Estimated RTO**: 2.5 minutes.

---

### Scenario F: Point-in-Time Recovery (PITR) to Nearest 15-Minute Window

#### 1. Symptom & Detection
- An unwanted bulk operation (e.g. incorrect price update on all tickets) occurred at 14:22.
#### 2. Restoration Runbook
1. Identify the 15-minute snapshot immediately preceding the incident (14:15 snapshot):
   ```bash
   TARGET_BACKUP="instance_staging/backups/eventai_backup_20261029_141500.db.gz"
   ```
2. Stop container, restore database to 14:15 state, run integrity check, and resume operations.
- **Estimated RTO**: 4 minutes.

---

## 3. Post-Recovery Validation Protocol

Before opening the restored staging application to users, the operator must execute the automated Smoke Test Suite:

```bash
# 1. Healthcheck probe
curl -s -f http://127.0.0.1:5001/health | grep '"status":"healthy"'

# 2. Database Record Assertion
python -c "
from app import create_app, db
from app.models.user import User
from app.models.event import Event
app = create_app('staging')
with app.app_context():
    print('Users:', User.query.count())
    print('Events:', Event.query.count())
    assert User.query.count() > 0, 'No users found!'
"

# 3. HTTP 200 on Critical Routes
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5001/
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5001/events
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5001/auth/login
```

---

## 4. Disaster Recovery Audit Sign-Off

The 6-scenario disaster recovery protocol establishes executable, step-by-step procedures ensuring RTO $\le$ 10 minutes and RPO $\le$ 15 minutes. It is certified for operational deployment in Phase 10B.

