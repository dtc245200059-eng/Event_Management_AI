"""
EventAI Pro — Secure Local Staging Credentials Retrieval.
Reads instance_staging/.staging_secrets.json for local authorized operators only.
DO NOT SHARE, COMMIT, OR PASTE INTO PUBLIC CHANNELS.
"""
import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
secrets_file = BASE_DIR / 'instance_staging' / '.staging_secrets.json'

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def display_credentials():
    if not secrets_file.exists():
        print(f"[ERROR] Staging secrets file not found at: {secrets_file}")
        print("Please run '.\\.venv\\Scripts\\python.exe scripts\\seed_staging.py --reseed' to initialize.")
        sys.exit(1)

    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not read secrets file: {e}")
        sys.exit(1)

    print("=" * 70)
    print("  EVENTAI PRO — LOCAL STAGING AUTHORIZED CREDENTIALS")
    print("  CONFIDENTIAL: Local Windows Staging environment only.")
    print("  Excluded from Git. Never commit or transmit.")
    print("=" * 70)
    print(f"{'Role':<12} | {'Username':<18} | {'Email':<30} | {'Password'}")
    print("-" * 70)
    for role, data in creds.items():
        print(f"{role.capitalize():<12} | {data.get('username', ''):<18} | {data.get('email', ''):<30} | {data.get('password', '')}")
    print("=" * 70)
    print("Use these credentials on http://127.0.0.1:5001/auth/login")

if __name__ == '__main__':
    display_credentials()

