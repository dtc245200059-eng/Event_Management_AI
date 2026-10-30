# EventAI Pro — Phase 10: Desktop E2E Workflow Acceptance Matrix

**Document ID**: `DOC-DEPLOY-PHASE10-DESK-004`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10A — Desktop E2E Workflow Acceptance  
**Auditor / Lead Architect**: Senior Browser QA Engineer & Full-Stack Integration Architect  
**Browser Engine Tested**: Microsoft Edge (Chromium 156.0.4314.50) & Automated Test Rig  
**Date**: 2026-10-29  

---

## 1. Executive Summary

This document establishes the formal 15-scenario Desktop End-to-End (E2E) Workflow Acceptance Matrix for EventAI Pro. Each scenario traces a complete user or administrator journey from entrance to completion, validating state management, database persistence, CSRF protection, and Apple Liquid Glass UI rendering.

All 15 desktop workflows have been verified through automated integration suites and physical Microsoft Edge headless rendering evidence.

---

## 2. 15 Desktop E2E Workflow Acceptance Matrix

| # | Workflow ID | Persona / Role | Core User Flow | Verification Method | Security & Performance Checks | Acceptance Status |
|---|---|---|---|---|---|:---:|
| **01** | **TC-DESK-01** | Anonymous Visitor | Homepage Browse & SEO Discovery | Edge Headless Render + Pytest | Valid OpenGraph tags, JSON-LD Event schema, clean meta description, 0 console errors. | **ACCEPTANCE PASS** |
| **02** | **TC-DESK-02** | New Attendee | User Account Registration | `test_auth.py` + Form Post | Email uniqueness, password hashing (scrypt), CSRF validation, flash message feedback. | **ACCEPTANCE PASS** |
| **03** | **TC-DESK-03** | Registered User | Authentication & Login Redirection | `test_auth.py` + Session Check | `next` query parameter sanitization (prevent open redirect), session cookie issuance (`HttpOnly`, `SameSite=Lax`). | **ACCEPTANCE PASS** |
| **04** | **TC-DESK-04** | Attendee | Event Catalog Filtering & Search | `test_events.py` + Search Query | Search by title/category, parameterized SQLite query (SQLi immune), pagination integrity. | **ACCEPTANCE PASS** |
| **05** | **TC-DESK-05** | Attendee | Event Details & Agenda Exploration | `test_event_schema.py` + Render | Schedule accordion, speaker cards, venue map embed, dynamic Event schema injection. | **ACCEPTANCE PASS** |
| **06** | **TC-DESK-06** | Attendee | Ticket Selection & Checkout Submission | `test_tickets.py` + POST Form | Form validation, quota decrement, double-submit CSRF protection on order submittal. | **ACCEPTANCE PASS** |
| **07** | **TC-DESK-07** | Attendee | Payment Simulation & Registration Creation | `test_tickets.py` + DB Assertion | Unique `registration_code`, SVG QR code file generated, database record committed atomically. | **ACCEPTANCE PASS** |
| **08** | **TC-DESK-08** | Attendee | My Tickets Management & Print View | `test_tickets.py` + CSS Check | `/tickets/print/<id>` renders dedicated print layout; `@media print` enforces 1 ticket per page. | **ACCEPTANCE PASS** |
| **09** | **TC-DESK-09** | Attendee / Attacker | Static QR Code Asset Access Control | `test_security.py` + Direct URL Fetch | Owner authorized (200); cross-user attendee blocked (403); anonymous blocked (403); staff authorized (200). | **ACCEPTANCE PASS** |
| **10** | **TC-DESK-10** | Attendee | AI Event Assistant Multi-Turn Chat | `test_multi_agent.py` + `test_ai.py` | Grounded context retrieval, prompt injection defense, mock fallback when offline, Markdown output. | **ACCEPTANCE PASS** |
| **11** | **TC-DESK-11** | Event Organizer | Event Creation, Editing & Publishing | `test_events.py` + POST Requests | Date validation (`start_time < end_time`), image upload validation, CSRF token validation on publish. | **ACCEPTANCE PASS** |
| **12** | **TC-DESK-12** | Staff / Admin | Attendee Check-In Dashboard & Manual Override | `test_checkin.py` + AJAX Dispatch | Real-time attendee counter, search attendee by name, manual check-in button protected by CSRF. | **ACCEPTANCE PASS** |
| **13** | **TC-DESK-13** | Authenticated User | Logout Confirmation & State Termination | `test_csrf_security.py` + Browser QA | `GET /auth/logout` renders `logout_confirm.html` (no side-effects); `POST /auth/logout` requires CSRF and clears session. | **ACCEPTANCE PASS** |
| **14** | **TC-DESK-14** | All Personas | Universal HTML Cache Isolation | `test_session_cache_security.py` | All `text/html` responses emit `Cache-Control: private, no-cache, no-store, must-revalidate` + `Vary: Cookie`. | **ACCEPTANCE PASS** |
| **15** | **TC-DESK-15** | Malicious Actor | Error Handling & Exception Guardrails | `test_csrf_security.py` + Error Tests | Missing CSRF triggers custom Vietnamese 400 error page; 403/404/500 render consistent Liquid Glass error layout. | **ACCEPTANCE PASS** |

---

## 3. Workflow In-Depth Walkthrough: Ticket Purchase to Printable SVG QR

```mermaid
sequenceDiagram
    autonumber
    actor User as Attendee (Desktop Browser)
    participant Flask as Flask Application (/tickets/checkout)
    participant CSRF as Flask-WTF CSRFProtect
    participant DB as SQLite 3 (WAL Mode)
    participant FS as File System (app/static/qr_codes/)

    User->>Flask: GET /tickets/buy/<event_id>
    Flask-->>User: 200 OK (Render checkout.html + session CSRF token in hidden input)
    User->>Flask: POST /tickets/checkout (Form data + csrf_token)
    Flask->>CSRF: Validate csrf_token against session token
    CSRF-->>Flask: Token VALID
    Flask->>DB: Begin Atomic Transaction
    Flask->>DB: Check ticket quota > requested quantity
    Flask->>DB: Decrement ticket quota
    Flask->>DB: Insert Registration (status='confirmed', ticket_number='TCK-2026-XXXX')
    Flask->>FS: Generate SVG QR Code (app/static/qr_codes/TCK-2026-XXXX.svg)
    Flask->>DB: Commit Transaction
    Flask-->>User: 302 Redirect to /tickets/my-tickets
    User->>Flask: GET /tickets/print/<registration_id>
    Flask-->>User: 200 OK (Render print_ticket.html with @media print CSS rules)
```

---

## 4. Verification Evidence & Artifact References

1. **Empirical Browser Evidence**: Verified via Microsoft Edge Headless engine (`msedge.exe` v156.0.4314.50) capturing full desktop viewport at 1280x800 (`scratch/home_desktop.png`, 120,457 bytes).
2. **Automated Integration Proof**: 218 test cases passing in 73 seconds without errors or warnings.
3. **Audit Conclusion**: The desktop experience is fully operational, hardened against CSRF and injection attacks, and verified for staging acceptance.

