# EventAI Pro — Phase 7: Real Browser End-to-End Testing Matrix & Protocol

**Status**: MANUAL PROTOCOL DEFINED / AUTOMATED HEADLESS CLI: `NOT VERIFIED (HEADLESS CLI)`  
**Auditor**: Senior Browser QA Engineer & Release Testing Specialist  
**Execution Context**: Windows 11 Headless Developer Sandbox (No GUI Display / No Automated Browser Binary Attached)  
**Standard**: ISO/IEC/IEEE 29119 Software Testing Standards & OWASP ASVS v4.0.3  

---

## 1. Environment Disclosure & Testing Mandate

In strict adherence to the project's engineering principles (*"Do not claim tests or verification passed unless they were actually run"*):

> **HEADLESS CLI LIMITATION NOTICE**:  
> Automated end-to-end browser execution (e.g., via automated Chromium/Playwright/Selenium harnesses) was **NOT executed** in this phase because the runtime environment is an automated, headless Windows terminal without an interactive display server or pre-installed browser drivers.  
>  
> Consequently, automated browser test execution is formally marked:  
> **STATUS: NOT VERIFIED (AUTOMATED BROWSER)**  
>  
> To guarantee complete release readiness, this document establishes the **exhaustive Manual End-to-End Verification Protocol (Matrix E2E-01 through E2E-06)** with exact user flows, input vectors, expected DOM states, and network payloads for human QA operators in the controlled staging environment.

---

## 2. Comprehensive Workflow Verification Matrix

### Domain 1: Authentication & Session Lifecycle (E2E-01)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-01.1** | **User Registration** | 1. Navigate to `/auth/register`<br>2. Fill unique email, full name, password<br>3. Submit form | - `POST /auth/register` with `csrf_token`<br>- HTTP 302 Redirect to `/auth/login`<br>- Flash message displayed | New user record in SQLite with Argon2id hashed password. |
| **E2E-01.2** | **User Login** | 1. Navigate to `/auth/login`<br>2. Input credentials<br>3. Submit form | - `POST /auth/login` with `csrf_token`<br>- Session cookie `session` set (`HttpOnly; SameSite=Lax`)<br>- Redirect to `/events` or return URL | Authenticated navbar displays user name and avatar dropdown. |
| **E2E-01.3** | **CSRF-Protected Logout** | 1. Log in as any user<br>2. Click User Dropdown -> "Đăng xuất" | - Hidden `#globalLogoutForm` submitted via `POST /auth/logout`<br>- Payload contains `csrf_token`<br>- HTTP 302 Redirect to `/`<br>- Session cookie invalidated | User is logged out; clicking browser "Back" does not show protected data. |
| **E2E-01.4** | **Tampered CSRF Submission** | 1. Inspect DOM on `/auth/profile`<br>2. Modify `input[name="csrf_token"]` value to `"invalid_tampered_token"`<br>3. Submit profile update | - `POST /auth/profile`<br>- HTTP 400 Bad Request<br>- Rendered `errors/400.html` explaining session error | No database write occurs; user notified cleanly without 500 crash. |

---

### Domain 2: Public Exploration & SEO Verification (E2E-02)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-02.1** | **Homepage & Discovery** | 1. Navigate to `/`<br>2. Inspect title and meta tags<br>3. Toggle search and filter | - HTTP 200 OK<br>- Canonical link matches origin<br>- OpenGraph & Twitter cards populated | Smooth CSS glassmorphism cards; no console JavaScript errors. |
| **E2E-02.2** | **Published Event Detail** | 1. Navigate to `/events/<id>` (Published event)<br>2. View page source | - `<script type="application/ld+json">` present<br>- Valid Schema.org `@type: Event`<br>- BreadcrumbList present | Structured data validates on Google Rich Results Test; 0 syntax errors. |
| **E2E-02.3** | **Draft Event Isolation** | 1. Copy URL of draft event (e.g. `/events/15`)<br>2. Open Private/Incognito window (anonymous)<br>3. Paste and enter URL | - HTTP 404 Not Found<br>- `X-Robots-Tag: noindex, nofollow`<br>- No JSON-LD emitted | Anonymous visitors cannot discover or preview unpublished events. |
| **E2E-02.4** | **Sitemap & Robots.txt** | 1. Navigate to `/robots.txt`<br>2. Navigate to `/sitemap.xml` | - `robots.txt`: Disallows `/admin/`, `/checkin/`, `/api/`<br>- `sitemap.xml`: Lists only published events<br>- Content-Type: `application/xml` | Sitemaps and robots conform to search engine crawler standards. |

---

### Domain 3: Ticket Booking & Attendee Experience (E2E-03)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-03.1** | **Free Ticket Checkout** | 1. Log in as attendee<br>2. Navigate to free event<br>3. Select Free Ticket -> Submit | - `POST /tickets/register/<type_id>` with CSRF<br>- HTTP 302 to `/tickets/my-tickets`<br>- Success flash message | Ticket record created with status `CONFIRMED`; quota decremented by 1. |
| **E2E-03.2** | **Quota Limit Enforcement** | 1. Attempt to register when `available_quantity == 0` | - UI indicates "Hết vé" (Sold Out)<br>- Direct POST returns flash warning<br>- Database prevents negative quota | Atomic transaction rollback prevents over-booking under concurrency. |
| **E2E-03.3** | **Ticket View & QR Display** | 1. Go to `/tickets/view/<id>`<br>2. Verify QR code display<br>3. Click "In vé" (Print Ticket) | - SVG/PNG QR code renders cleanly<br>- Print CSS enforces 1 ticket per page<br>- Navigation and buttons hidden in print mode | High-contrast QR code easily readable by physical 2D barcode scanner. |
| **E2E-03.4** | **Ticket Cancellation** | 1. Click "Hủy vé" on `/tickets/my-tickets`<br>2. Confirm modal dialog | - `POST /tickets/cancel/<id>` with CSRF<br>- Status changes to `CANCELLED`<br>- Available quota incremented by 1 | Reclaimed quota immediately becomes available to other attendees. |

---

### Domain 4: Check-in Operations & Staff Tooling (E2E-04)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-04.1** | **Camera QR Scan Check-in** | 1. Log in as Staff/Admin<br>2. Navigate to `/checkin/scanner`<br>3. Present attendee QR to camera | - `POST /checkin/process` via `fetch`<br>- `X-CSRFToken` attached automatically<br>- HTTP 200 JSON `{status: "success", attendee: ...}` | Audio chime / visual green badge; attendee status updated in real-time. |
| **E2E-04.2** | **Duplicate Check-in Rejection** | 1. Re-scan the same QR code immediately | - `POST /checkin/process`<br>- HTTP 400 JSON `{status: "already_checked_in", timestamp: ...}`<br>- Visual red warning badge | Prevents pass-back ticket fraud; displays original check-in timestamp. |
| **E2E-04.3** | **Quick Check-in from Roster** | 1. Go to attendee roster `/events/<id>/manage`<br>2. Click Quick Check-in button | - `POST /checkin/quick/<id>` with CSRF<br>- Button toggles to "Đã check-in"<br>- Undo option becomes visible | Immediate DOM state change without full page reload. |

---

### Domain 5: AI Assistant & Real-Time Services (E2E-05)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-05.1** | **AI Floating Widget Open/Close** | 1. Click floating sparkle icon in bottom-right<br>2. Verify modal animation | - Smooth glassmorphism popover expansion<br>- Input field auto-focuses<br>- Backdrop blur renders smoothly | Compliant with Apple Liquid Glass design tokens; smooth 60fps animation. |
| **E2E-05.2** | **AI Event Query (Grounded RAG)** | 1. Ask: *"Có những sự kiện công nghệ nào sắp tới?"*<br>2. Click Send | - `POST /api/chat` with `X-CSRFToken`<br>- Typing indicator displays<br>- HTTP 200 JSON with grounded Markdown response | Answer cites actual database events; links directly to event detail pages. |
| **E2E-05.3** | **RAG Fallback on Quota/Offline** | 1. Simulate Gemini API timeout or quota limit | - Local Fallback Mock Engine activates<br>- Clean, structured database answer returned | Zero user-facing crashes; response includes grounded schedule/venue info. |

---

### Domain 6: Liquid Glass Design & Accessibility (E2E-06)

| Case ID | Scenario / Action | Steps to Execute | Expected Network & DOM Result | Manual Verification Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-06.1** | **Dark / Light Theme Toggle** | 1. Click theme toggle button in navbar<br>2. Verify color palette shift | - `data-bs-theme` attribute toggles on `<html>`<br>- Preference stored in `localStorage`<br>- Liquid Glass border and blur adapt | Contrast ratio meets WCAG AA (>= 4.5:1) in both light and dark modes. |
| **E2E-06.2** | **Mobile Responsive Navigation** | 1. Resize viewport to <= 768px (Mobile)<br>2. Tap hamburger menu icon<br>3. Verify mobile drawer | - Off-canvas mobile drawer slides in smoothly<br>- Focus trapped inside drawer<br>- Touch swipe-to-close works | Backdrop overlay dismisses drawer; navbar stays fixed at top. |
| **E2E-06.3** | **Keyboard Accessibility** | 1. Use `Tab` / `Shift+Tab` across forms<br>2. Use `Enter` / `Space` on buttons | - Visible focus ring around all interactive controls<br>- Logical tab order matches visual layout<br>- Modals dismiss with `Escape` key | 100% accessible without a mouse or pointing device. |

---

## 3. Staging Sign-Off Protocol for Human QA

Before production release, the Staging QA Lead must execute the above 18 test cases on the staging deployment URL and check off each domain:

- [ ] Domain 1: Authentication & Session Lifecycle (E2E-01) — 4/4 Verified
- [ ] Domain 2: Public Exploration & SEO Verification (E2E-02) — 4/4 Verified
- [ ] Domain 3: Ticket Booking & Attendee Experience (E2E-03) — 4/4 Verified
- [ ] Domain 4: Check-in Operations & Staff Tooling (E2E-04) — 3/3 Verified
- [ ] Domain 5: AI Assistant & Real-Time Services (E2E-05) — 3/3 Verified
- [ ] Domain 6: Liquid Glass Design & Accessibility (E2E-06) — 3/3 Verified

**Overall Browser E2E Status**: **PROTOCOL SPECIFIED — READY FOR HUMAN STAGING EXECUTION**

