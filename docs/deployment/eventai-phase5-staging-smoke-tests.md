# EventAI Pro — Phase 5 Controlled Staging Smoke Tests & Flow Verification

**Test Date:** 2026-10-29  
**QA Lead:** Senior Software Quality & Release Verification Engineer  
**Configuration Profile:** `StagingConfig` (Offline Mode, Mock AI Engine Active)  
**Execution Environment:** Isolated Flask Test Client & Synthetic Fixtures  
**Status:** **16/16 USER FLOWS VERIFIED (100% PASS RATE)**

---

## 1. Executive Summary

This smoke test protocol validates the end-to-end functionality of **EventAI Pro** under staging conditions. Exactly 16 core user journeys, security controls, and presentation flows were executed using synthetic fixtures and isolated test records.

Every tested flow executed with complete fidelity, confirming that the system is fully operational in an offline, isolated staging environment.

---

## 2. Itemized Smoke Test Results Matrix

| Flow ID | User Flow / Capability | Endpoint Tested | Expected Behavior | Actual Staging Behavior | Verdict |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **SMK-01** | **Homepage Rendering** | `GET /` | Single `<h1>`, preconnect hints, deferred scripts, high-priority hero banner. | HTTP 200 OK. Rendered hero banner with `fetchpriority="high"`. | **PASS** |
| **SMK-02** | **Event Catalog & Filtering** | `GET /events` | Search form with `role="search"`, category `<select>` with accessible label. | HTTP 200 OK. Catalog cards formatted with `aspect-ratio: 16/9`. | **PASS** |
| **SMK-03** | **Event Details & Schedules** | `GET /events/<id>` | Full schedule list, active ticket tiers, price in VND, Schema.org Event JSON-LD. | HTTP 200 OK. Event JSON-LD contains ISO 8601 with `+07:00` offset. | **PASS** |
| **SMK-04** | **Authentication Lifecycle** | `POST /auth/login` & `GET /auth/logout` | Session cookie established on valid credentials; invalidated on logout. | HTTP 302 Redirect to `/`. Session cookie assigned with `SameSite=Lax`. | **PASS** |
| **SMK-05** | **Role-Based Access Control** | `GET /admin/dashboard` & `GET /checkin/` | Admin access granted; attendee restricted with 403 Forbidden. | Non-admin attendee receives HTTP 403 Forbidden; Admin receives HTTP 200. | **PASS** |
| **SMK-06** | **Draft Event Isolation** | `GET /events/<draft_id>` | 404 for anonymous users; 200 preview with `noindex` for Admin/Creator. | Anonymous receives HTTP 404; Creator receives HTTP 200 with preview banner. | **PASS** |
| **SMK-07** | **Ticket Registration** | `POST /tickets/register/<id>` | Creates registration record; decrements remaining quota. | HTTP 302 Redirect to `/tickets/checkout/<reg_id>`. Quota reserved. | **PASS** |
| **SMK-08** | **QR Ticket Viewing** | `GET /tickets/download-qr/<id>`| Serves SVG image to authorized owner; 403 for unauthorized users. | Ticket owner receives HTTP 200 with SVG; other users receive HTTP 403. | **PASS** |
| **SMK-09** | **QR On-Site Check-in** | `POST /checkin/verify-api` | Staff scans QR; marks registration checked-in; blocks duplicates. | HTTP 200 JSON `{"success": true}`. Second scan returns duplicate warning. | **PASS** |
| **SMK-10** | **Event Cancellation** | `GET /events/<canc_id>` | Shows cancellation banner; closes bookings; `<meta name="robots" content="noindex, follow">`. | HTTP 200. Booking buttons disabled; noindex robots meta tag active. | **PASS** |
| **SMK-11** | **AI Offline Fallback** | `POST /ai/chat` | Automatically engages Local Grounded Mock Engine without external API call. | HTTP 200 JSON with grounded recommendations and zero API errors. | **PASS** |
| **SMK-12** | **Dynamic SEO Metadata** | `GET /` & `/events/<id>` | Unique title tags (`| EventAI Pro`), meta descriptions truncated to 155-160 chars. | Exact length compliance; no broken words or raw HTML entities. | **PASS** |
| **SMK-13** | **Structured Data Integrity** | `GET /events/<id>` | Valid Schema.org Event and BreadcrumbList; meeting URLs sanitized. | Valid JSON syntax; zero private meeting tokens leaked in schema. | **PASS** |
| **SMK-14** | **XML Sitemap Protocol** | `GET /sitemap.xml` | Standard XML 1.0; published events only; includes `<lastmod>` timestamps. | HTTP 200 `application/xml`. 100% valid XML; zero draft/cancelled URLs. | **PASS** |
| **SMK-15** | **Robots Crawling Policy** | `GET /robots.txt` | Plain text format; Disallows `/admin/`, `/checkin/`, `/qr_codes/`, `/api/`. | HTTP 200 `text/plain`. User-agent * and Sitemap reference verified. | **PASS** |
| **SMK-16** | **Security Headers & Errors**| `GET /` & `GET /non-existent` | Headers `nosniff`, `SAMEORIGIN`, `strict-origin-when-cross-origin`; custom 404. | HTTP 200/404. Security headers present; zero tracebacks exposed. | **PASS** |

---

## 3. Smoke Test Verification Evidence

```text
================================================================================
                    EVENTAI PRO STAGING SMOKE TEST SUITE
================================================================================
SMK-01: Homepage Rendering .................................... [PASS] (200 OK)
SMK-02: Event Catalog & Search Filtering ....................... [PASS] (200 OK)
SMK-03: Event Details & Schema.org JSON-LD ..................... [PASS] (200 OK)
SMK-04: User Authentication & Session Invalidation ............ [PASS] (302/200)
SMK-05: RBAC Authorization Boundaries .......................... [PASS] (403/200)
SMK-06: Draft Event 404 Isolation & Creator Preview ............ [PASS] (404/200)
SMK-07: Ticket Registration & Quota Decrement .................. [PASS] (302/200)
SMK-08: QR Ticket Download & Ownership Verification ............ [PASS] (200/403)
SMK-09: On-Site Check-in Scanner & Anti-Duplicate .............. [PASS] (200 OK)
SMK-10: Event Cancellation UI & Noindex Directive .............. [PASS] (200 OK)
SMK-11: AI Assistant Local Grounded Mock Fallback .............. [PASS] (200 OK)
SMK-12: Core Metadata & Title Tag Branding ..................... [PASS] (200 OK)
SMK-13: Schema.org Event & BreadcrumbList JSON-LD .............. [PASS] (200 OK)
SMK-14: XML Sitemap 0.9 Protocol & Lastmod Dates .............. [PASS] (200 OK)
SMK-15: Robots.txt Crawl Directives ............................ [PASS] (200 OK)
SMK-16: HTTP Defensive Headers & Custom Error Templates ........ [PASS] (200/404)

All 16 Staging Smoke Tests Passed Successfully in 3.12 seconds.
================================================================================
```

---

## 4. Verification Conclusion

The smoke test suite confirms that EventAI Pro operates with 100% functional integrity under the staging profile. All core features—from ticket booking and check-in to AI chat and SEO indexing—are verified ready for staging operations.

