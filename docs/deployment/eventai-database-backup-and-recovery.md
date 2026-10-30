# EventAI Pro — Phase 4 Database Backup, Concurrency & Disaster Recovery Guide

**Guide Date:** 2026-10-29  
**Database Architect:** Senior Database Administrator & Reliability Engineer  
**Engine:** SQLite 3.x (with SQLAlchemy ORM abstraction)  
**Database File:** `instance/event_management.db`  
**Status:** **OPERATIONAL DISASTER RECOVERY PROTOCOL**

---

## 1. Database Architecture & Concurrency Profile

EventAI Pro utilizes an embedded SQLite 3 database file located at `instance/event_management.db`. SQLite provides a zero-administration, serverless relational database that enforces ACID transactions for the application's 9 core tables (Users, Events, Schedules, Speakers, Venues, Tickets, Registrations, Notifications, FAQs).

### 1.1 Concurrency Characteristics & PRAGMA Tuning
An audit of `instance/event_management.db` revealed the following default settings:
- **Journal Mode:** `DELETE`
- **Busy Timeout:** `5000ms` (5 seconds)
- **Foreign Keys:** `OFF` (SQLite default)

#### Recommended Production Optimizations:
1. **Write-Ahead Logging (WAL Mode):**
   - By default (`DELETE` journal mode), every write operation requires an exclusive lock on the entire database file, temporarily blocking all concurrent readers.
   - Enabling WAL mode (`PRAGMA journal_mode = WAL;`) allows multiple readers to read simultaneously while a writer is writing to the `.db-wal` file.
   - WAL mode reduces write contention, eliminates reader-writer deadlocks, and boosts ticket check-in throughput.
   - Activation command:
     ```bash
     sqlite3 instance/event_management.db "PRAGMA journal_mode = WAL;"
     ```
2. **Extended Busy Timeout:**
   - Increase `busy_timeout` to `10000ms` (10 seconds) to ensure that if a write is in progress, incoming requests wait smoothly rather than failing immediately with `OperationalError: database is locked`.
3. **Foreign Key Enforcement:**
   - Configure SQLAlchemy event listener to execute `PRAGMA foreign_keys = ON;` on every connection checkout.

---

## 2. Online Hot Backup Procedures (Zero Downtime)

> [!CAUTION]
> **NEVER use standard file copy (`cp`, `xcopy`, or `Copy-Item`) while the web application is running.**  
> Copying an active SQLite database file while a transaction is writing can capture a torn page, resulting in permanent database corruption.

### 2.1 Method A: Python SQLite Online Backup API (Recommended)
Python's standard library `sqlite3` module provides a thread-safe, lockless `backup()` method that copies pages incrementally while web traffic continues uninterrupted:

```python
#!/usr/bin/env python3
"""
scripts/backup_database.py - Online Hot Backup for EventAI Pro
"""
import os
import sqlite3
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'instance' / 'event_management.db'
BACKUP_DIR = BASE_DIR / 'backups'

def run_hot_backup():
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = BACKUP_DIR / f"eventai_backup_{timestamp}.db"

    print(f"[*] Starting online hot backup from {DB_PATH} to {backup_file}...")
    source_conn = sqlite3.connect(str(DB_PATH))
    dest_conn = sqlite3.connect(str(backup_file))

    try:
        # Executes incremental hot backup without blocking readers
        source_conn.backup(dest_conn, pages=100)
        print("[+] Online backup completed successfully.")

        # Verify integrity of the backup copy
        cur = dest_conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        result = cur.fetchone()[0]
        if result == 'ok':
            print("[+] Backup integrity verified: OK")
        else:
            raise RuntimeError(f"Backup integrity check failed: {result}")
    finally:
        dest_conn.close()
        source_conn.close()

if __name__ == '__main__':
    run_hot_backup()
```

### 2.2 Method B: SQLite CLI Command
Alternatively, invoke the SQLite CLI `.backup` command directly:
```bash
sqlite3 instance/event_management.db ".backup 'backups/eventai_$(date +%Y%m%d_%H%M%S).db'"
sqlite3 "backups/eventai_$(date +%Y%m%d_%H%M%S).db" "PRAGMA integrity_check;"
```

---

## 3. Automated Backup Schedule & Retention Policy

Deploy an automated cron job on Linux (`/etc/cron.d/eventai-backup`):
```cron
# Full Online Backup every day at 02:00 AM
0 2 * * * www-data /var/www/eventai/.venv/bin/python /var/www/eventai/scripts/backup_database.py >> /var/log/eventai/backup.log 2>&1

# Hourly snapshot during major event registration periods (08:00 to 22:00)
0 8-22 * * * www-data /var/www/eventai/.venv/bin/python /var/www/eventai/scripts/backup_database.py >> /var/log/eventai/backup.log 2>&1

# Purge backups older than 30 days
30 2 * * * www-data find /var/www/eventai/backups -name "eventai_backup_*.db" -type f -mtime +30 -delete
```

---

## 4. Disaster Recovery & Restoration Runbook

In the event of database corruption, disk failure, or unintended data deletion, execute the following step-by-step restoration playbook:

### Step 1: Gracefully Halt the Web Service
Stop incoming writes immediately to prevent cascading errors:
```bash
sudo systemctl stop eventai
# Or in Docker:
docker stop eventai_pro_app
```

### Step 2: Quarantine the Faulty Database
Preserve the existing database file and WAL logs for forensic investigation:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mv instance/event_management.db instance/event_management_corrupted_${TIMESTAMP}.db
[ -f instance/event_management.db-wal ] && mv instance/event_management.db-wal instance/event_management_corrupted_${TIMESTAMP}.db-wal
[ -f instance/event_management.db-shm ] && mv instance/event_management.db-shm instance/event_management_corrupted_${TIMESTAMP}.db-shm
```

### Step 3: Restore the Target Verified Backup
Select the most recent verified backup from the `backups/` directory:
```bash
LATEST_BACKUP=$(ls -t backups/eventai_backup_*.db | head -n 1)
cp "$LATEST_BACKUP" instance/event_management.db
chmod 600 instance/event_management.db
chown www-data:www-data instance/event_management.db
```

### Step 4: Verify Database Integrity
Run a hardware and structural integrity check on the restored database:
```bash
sqlite3 instance/event_management.db "PRAGMA integrity_check;"
# Expected output: ok
```

### Step 5: Restart the Web Service & Verify Health
```bash
sudo systemctl start eventai
curl -s http://127.0.0.1:5000/health
# Expected output: {"database":"connected","status":"healthy"}
```

---

## 5. Recovery Objectives

| Metric | Target SLA | Strategy |
| :--- | :--- | :--- |
| **Recovery Time Objective (RTO)** | **< 5 minutes** | Automated backup swap and single-command service restart. |
| **Recovery Point Objective (RPO)** | **< 1 hour** | Hourly snapshot schedule during active registration windows. |
| **Data Integrity Assurance** | **100% (Zero Corruption)** | Automated `PRAGMA integrity_check` executed on every snapshot. |

