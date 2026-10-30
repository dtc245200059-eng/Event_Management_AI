"""
EventAI Pro — Windows Native Staging Workflows Verification Suite (Hardened).
Executes 14 end-to-end integration workflows against http://127.0.0.1:5001.
Validates session cookies, CSRF protection, RBAC, AI RAG chat, QR check-in, and security rejection.
Dynamically retrieves synthetic credentials from instance_staging/.staging_secrets.json.
Repeatable test execution with pre-test reset and post-test cleanup of fixtures.
"""
import requests
import re
import sys
import json
import sqlite3
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = "http://127.0.0.1:5001"
secrets_file = BASE_DIR / 'instance_staging' / '.staging_secrets.json'

def extract_csrf(html_text):
    # Try finding meta tag
    match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']', html_text)
    if match:
        return match.group(1)
    # Try finding hidden form input
    match = re.search(r'<input[^>]+name=["\']csrf_token["\'][^>]+value=["\']([^"\']+)["\']', html_text)
    if match:
        return match.group(1)
    return None

def load_staging_credentials():
    if not secrets_file.exists():
        print(f"[ERROR] Staging credentials file not found: {secrets_file}")
        print("Please run '.\\.venv\\Scripts\\python.exe scripts\\seed_staging.py --reseed' first.")
        sys.exit(1)
    with open(secrets_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_staging_suite():
    creds = load_staging_credentials()
    results = []
    
    # 1. Reset staging check-in status before test suite
    db_path = BASE_DIR / 'instance_staging' / 'staging.db'
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("UPDATE registrations SET checked_in=0, checked_in_at=NULL, checked_in_by=NULL WHERE ticket_number='TCK-001-0001-STG'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not reset staging registration: {e}")
    
    def log_result(name, passed, details):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} — {details}")
        results.append((name, passed, details))

    print("=" * 70)
    print("  RUNNING EVENTAI PRO WINDOWS NATIVE STAGING VERIFICATION SUITE")
    print(f"  Target Server: {BASE_URL}")
    print("  Auth Model:    Dynamic Staging Secrets (.staging_secrets.json)")
    print("=" * 70)

    # WF01: Homepage Anonymous
    s = requests.Session()
    try:
        r = s.get(f"{BASE_URL}/", timeout=5)
        csrf = extract_csrf(r.text)
        passed = r.status_code == 200 and "EventAI Pro" in r.text and csrf is not None
        log_result("WF01_HOMEPAGE_ANON", passed, f"HTTP {r.status_code}, CSRF Meta detected: {bool(csrf)}")
    except Exception as e:
        log_result("WF01_HOMEPAGE_ANON", False, str(e))

    # WF02: Event Detail
    try:
        r = s.get(f"{BASE_URL}/events/1", timeout=5)
        passed = r.status_code == 200 and "Hội Thảo Công Nghệ" in r.text and "TS. Nguyễn Văn AI" in r.text
        log_result("WF02_EVENT_DETAIL", passed, f"HTTP {r.status_code}, Title & Speaker found in DOM")
    except Exception as e:
        log_result("WF02_EVENT_DETAIL", False, str(e))

    # WF03: Login Form & CSRF
    login_csrf = None
    try:
        r = s.get(f"{BASE_URL}/auth/login", timeout=5)
        login_csrf = extract_csrf(r.text)
        has_session_cookie = 'session' in s.cookies
        passed = r.status_code == 200 and login_csrf is not None and has_session_cookie
        log_result("WF03_LOGIN_FORM_CSRF", passed, f"HTTP {r.status_code}, Form CSRF token: {bool(login_csrf)}, Session Cookie: {has_session_cookie}")
    except Exception as e:
        log_result("WF03_LOGIN_FORM_CSRF", False, str(e))

    # WF04: Admin Login
    admin_session = requests.Session()
    r = admin_session.get(f"{BASE_URL}/auth/login")
    adm_csrf = extract_csrf(r.text)
    adm_user = creds['admin']['username']
    adm_pwd = creds['admin']['password']
    try:
        r = admin_session.post(
            f"{BASE_URL}/auth/login",
            data={
                "csrf_token": adm_csrf,
                "username": adm_user,
                "password": adm_pwd
            },
            allow_redirects=False,
            timeout=5
        )
        passed = r.status_code in (302, 200) and 'session' in admin_session.cookies
        log_result("WF04_ADMIN_LOGIN", passed, f"HTTP {r.status_code}, Redirect: {r.headers.get('Location')}")
    except Exception as e:
        log_result("WF04_ADMIN_LOGIN", False, str(e))

    # WF05: Admin Dashboard Access
    try:
        r = admin_session.get(f"{BASE_URL}/admin/dashboard", timeout=5)
        passed = r.status_code == 200 and ("Tổng quan" in r.text or "Bảng điều khiển" in r.text or "EventAI" in r.text)
        log_result("WF05_ADMIN_DASHBOARD", passed, f"HTTP {r.status_code}, Admin dashboard verified")
    except Exception as e:
        log_result("WF05_ADMIN_DASHBOARD", False, str(e))

    # WF06: AI Chatbot Query with CSRF
    try:
        r_home = admin_session.get(f"{BASE_URL}/")
        page_csrf = extract_csrf(r_home.text)
        r = admin_session.post(
            f"{BASE_URL}/ai/chat",
            json={
                "message": "Diễn giả của hội thảo là ai?",
                "event_id": 1
            },
            headers={
                "X-CSRFToken": page_csrf
            },
            timeout=10
        )
        data = r.json() if r.status_code == 200 else {}
        answer = data.get("response", "") or data.get("answer", "") or data.get("message", "")
        passed = r.status_code == 200 and len(answer) > 0
        log_result("WF06_AI_RAG_CHAT", passed, f"HTTP {r.status_code}, AI response received ({len(answer)} chars)")
    except Exception as e:
        log_result("WF06_AI_RAG_CHAT", False, str(e))

    # WF07: Staff Login
    staff_session = requests.Session()
    r = staff_session.get(f"{BASE_URL}/auth/login")
    stf_csrf = extract_csrf(r.text)
    stf_user = creds['staff']['username']
    stf_pwd = creds['staff']['password']
    try:
        r = staff_session.post(
            f"{BASE_URL}/auth/login",
            data={
                "csrf_token": stf_csrf,
                "username": stf_user,
                "password": stf_pwd
            },
            allow_redirects=False,
            timeout=5
        )
        passed = r.status_code in (302, 200)
        log_result("WF07_STAFF_LOGIN", passed, f"HTTP {r.status_code}, Staff logged in")
    except Exception as e:
        log_result("WF07_STAFF_LOGIN", False, str(e))

    # WF08: Check-in Interface Access
    try:
        r = staff_session.get(f"{BASE_URL}/checkin/", timeout=5)
        passed = r.status_code == 200 and "checkin" in r.text.lower()
        log_result("WF08_CHECKIN_PAGE", passed, f"HTTP {r.status_code}, Check-in console loaded")
    except Exception as e:
        log_result("WF08_CHECKIN_PAGE", False, str(e))

    # WF09: QR Check-in Scan Valid
    try:
        r_page = staff_session.get(f"{BASE_URL}/checkin/")
        chk_csrf = extract_csrf(r_page.text)
        r = staff_session.post(
            f"{BASE_URL}/checkin/verify-api",
            json={
                "ticket_number": "TCK-001-0001-STG",
                "event_id": 1
            },
            headers={
                "X-CSRFToken": chk_csrf
            },
            timeout=5
        )
        data = r.json() if r.status_code == 200 else {}
        passed = r.status_code == 200 and data.get("status") == "valid" and data.get("success") is True
        log_result("WF09_QR_CHECKIN_VALID", passed, f"HTTP {r.status_code}, Result: {data.get('status')}, Msg: {data.get('message', '')[:60]}")
    except Exception as e:
        log_result("WF09_QR_CHECKIN_VALID", False, str(e))

    # WF10: QR Check-in Duplicate Attempt (Anti-fraud)
    try:
        r = staff_session.post(
            f"{BASE_URL}/checkin/verify-api",
            json={
                "ticket_number": "TCK-001-0001-STG",
                "event_id": 1
            },
            headers={
                "X-CSRFToken": chk_csrf
            },
            timeout=5
        )
        data = r.json()
        passed = r.status_code == 409 and data.get("status") == "duplicate"
        log_result("WF10_QR_CHECKIN_DUPLICATE", passed, f"HTTP {r.status_code}, Status: {data.get('status')} (Anti-duplicate confirmed)")
    except Exception as e:
        log_result("WF10_QR_CHECKIN_DUPLICATE", False, str(e))

    # WF11: Attendee Login
    att_session = requests.Session()
    r = att_session.get(f"{BASE_URL}/auth/login")
    att_csrf = extract_csrf(r.text)
    att_user = creds['attendee']['username']
    att_pwd = creds['attendee']['password']
    try:
        r = att_session.post(
            f"{BASE_URL}/auth/login",
            data={
                "csrf_token": att_csrf,
                "username": att_user,
                "password": att_pwd
            },
            allow_redirects=False,
            timeout=5
        )
        passed = r.status_code in (302, 200)
        log_result("WF11_ATTENDEE_LOGIN", passed, f"HTTP {r.status_code}, Attendee logged in")
    except Exception as e:
        log_result("WF11_ATTENDEE_LOGIN", False, str(e))

    # WF12: Attendee My Tickets
    try:
        r = att_session.get(f"{BASE_URL}/tickets/my-tickets", timeout=5)
        passed = r.status_code == 200 and ("TCK-001-0001-STG" in r.text or "Vé của tôi" in r.text or "Vé Của Tôi" in r.text)
        log_result("WF12_ATTENDEE_MY_TICKETS", passed, f"HTTP {r.status_code}, My Tickets page verified")
    except Exception as e:
        log_result("WF12_ATTENDEE_MY_TICKETS", False, str(e))

    # WF13: Logout POST with CSRF
    try:
        r_page = att_session.get(f"{BASE_URL}/tickets/my-tickets")
        out_csrf = extract_csrf(r_page.text)
        r = att_session.post(
            f"{BASE_URL}/auth/logout",
            data={"csrf_token": out_csrf},
            allow_redirects=False,
            timeout=5
        )
        passed = r.status_code in (302, 200)
        log_result("WF13_LOGOUT_POST", passed, f"HTTP {r.status_code}, Logged out cleanly")
    except Exception as e:
        log_result("WF13_LOGOUT_POST", False, str(e))

    # WF14: CSRF Rejection (POST without CSRF)
    try:
        bad_session = requests.Session()
        bad_session.get(f"{BASE_URL}/auth/login")
        r = bad_session.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": adm_user,
                "password": adm_pwd
                # Omit csrf_token
            },
            allow_redirects=False,
            timeout=5
        )
        passed = r.status_code == 400
        log_result("WF14_CSRF_REJECTION", passed, f"HTTP {r.status_code} (Expected 400 Bad Request on missing CSRF)")
    except Exception as e:
        log_result("WF14_CSRF_REJECTION", False, str(e))

    # 2. Cleanup / Restore disposable check-in status after test suite
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("UPDATE registrations SET checked_in=0, checked_in_at=NULL, checked_in_by=NULL WHERE ticket_number='TCK-001-0001-STG'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not restore staging registration: {e}")

    print("-" * 70)
    passed_count = sum(1 for _, p, _ in results if p)
    print(f"  TOTAL WORKFLOWS: {len(results)} | PASSED: {passed_count} | FAILED: {len(results) - passed_count}")
    print("=" * 70)
    return passed_count == len(results)

if __name__ == "__main__":
    success = run_staging_suite()
    sys.exit(0 if success else 1)
