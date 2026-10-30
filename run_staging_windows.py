"""
EventAI Pro — Windows Native Staging Server Runner.
Launches the Flask application factory under StagingConfig bound strictly to 127.0.0.1:5001.
Completely isolated from the production database (instance/event_management.db).
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Force Staging environment variables
os.environ['FLASK_ENV'] = 'staging'
staging_db_path = BASE_DIR / 'instance_staging' / 'staging.db'
os.environ['DATABASE_URI'] = f"sqlite:///{staging_db_path}"
os.environ['CANONICAL_DOMAIN'] = 'http://127.0.0.1:5001'
os.environ['PORT'] = '5001'

# Check if database needs seeding
if not staging_db_path.exists() or '--seed' in sys.argv:
    print("[STAGING LAUNCHER] Staging database not found or --seed provided. Seeding now...")
    from scripts.seed_staging import seed_staging_database
    seed_staging_database()

from app import create_app

app = create_app('staging')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    host = '127.0.0.1'
    
    print("=" * 70)
    print("  EVENTAI PRO — WINDOWS NATIVE STAGING ENVIRONMENT")
    print("=" * 70)
    print(f"  * Status:              ACTIVE (Native Windows 11)")
    print(f"  * Environment:         {app.config.get('ENV_NAME', 'staging')}")
    print(f"  * Target URL:          http://{host}:{port}")
    print(f"  * Database:            {staging_db_path}")
    print(f"  * Production DB:       PROTECTED & UNTOUCHED")
    print(f"  * CSRF Protection:     {app.config.get('WTF_CSRF_ENABLED')}")
    print(f"  * AI Fallback Mock:    {app.config.get('ENABLE_AI_FALLBACK_MOCK')}")
    print(f"  * Session Secure:      {app.config.get('SESSION_COOKIE_SECURE')} (HTTP Loopback)")
    print("-" * 70)
    print("  Synthetic Personas (Isolated Staging DB):")
    print("    - Admin:             admin_staging (admin@staging.eventai.local)")
    print("    - Staff (Check-in):  staff_staging (staff@staging.eventai.local)")
    print("    - Organizer:         organizer_staging (organizer@staging.eventai.local)")
    print("    - Attendee:          attendee_staging (attendee@staging.eventai.local)")
    print("  * Credentials:         Stored in instance_staging/.staging_secrets.json")
    print("  * Local Retrieval:     Run '.\\.venv\\Scripts\\python.exe scripts\\get_staging_credentials.py'")
    print("-" * 70)
    print("  Press Ctrl+C to terminate the staging server.")
    print("=" * 70)

    # In staging, debug=False to ensure realistic error handling
    app.run(host=host, port=port, debug=False)

