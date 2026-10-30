# EventAI Pro — Phase 8: Real Browser Staging QA Protocol & Matrix

**Status**: MANUAL PROTOCOL DEFINED / AUTOMATED HEADLESS CLI: `NOT VERIFIED (HEADLESS CLI)`  
**Auditor**: Senior Browser QA Engineer & Release Testing Specialist  
**Execution Context**: Windows 11 Automated Sandbox (No Interactive Display Server / No Pre-installed Automated Browser Drivers)  
**Standard**: ISO/IEC/IEEE 29119 Software Testing Standards & OWASP ASVS v4.0.3  

---

## 1. Environment Verification & Honest Disclosure

In strict adherence to project guidelines (*"Do not claim tests or verification passed unless they were actually run. Never fabricate browser results"*):

> **HEADLESS CLI ENVIRONMENT DISCLOSURE**:  
> During Phase 8, a system-level audit of Windows 11 application paths, the Windows Registry (`HKLM/HKCU App Paths`), and `where.exe` was conducted. The results confirmed that **no GUI browser automation binaries (Chromium/Playwright/Selenium) are attached or accessible** within this headless execution container.  
>  
> Consequently, automated browser test execution is formally marked:  
> **STATUS: NOT VERIFIED (HEADLESS CLI ENVIRONMENT)**  
>  
> To guarantee complete release readiness, this document establishes the **exhaustive Manual Staging QA Protocol (Workflows QA-01 through QA-06)** with exact user flows, input vectors, expected DOM states, and network payloads for human QA operators in the staging environment.

---

## 2. Definitive Browser Testing Matrix across 6 Domains

### Domain 1: Authentication & Session Lifecycle (QA-01)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-01.1** | **User Login** | 1. Visit `/auth/login`<br>2. Submit valid credentials | - `POST /auth/login` with `csrf_token`<br>- Session cookie `session` set (`HttpOnly; SameSite=Lax`)<br>- Redirect to `/events` | **MANUAL READY** |
| **QA-01.2** | **Synthetic Registration** | 1. Visit `/auth/register`<br>2. Fill unique user fields<br>3. Submit form | - `POST /auth/register` with `csrf_token`<br>- Redirect to `/auth/login`<br>- Flash message displayed | **MANUAL READY** |
| **QA-01.3** | **POST Logout** | 1. Log in as user<br>2. Click dropdown -> "Đăng xuất" | - Hidden `#globalLogoutForm` submitted via POST<br>- `csrf_token` present<br>- User redirected to `/`<br>- Session destroyed | **MANUAL READY** |
| **QA-01.4** | **GET Logout Non-Mutation** | 1. Log in as user<br>2. Type `/auth/logout` into address bar | - `GET /auth/logout` returns HTTP 200<br>- Confirmation card displayed<br>- **User remains 100% authenticated** | **MANUAL READY** |
| **QA-01.5** | **Missing CSRF Token** | 1. Submit POST login via curl without token | - HTTP 400 Bad Request<br>- Rendered `errors/400.html` | **AUTOMATED PASS** (T02) |
| **QA-01.6** | **Invalid CSRF Token** | 1. Modify DOM `csrf_token` to `"tampered"`<br>2. Submit form | - HTTP 400 Bad Request<br>- Friendly session error message | **AUTOMATED PASS** (T03) |
| **QA-01.7** | **Browser Refresh** | 1. Refresh page on `/auth/profile` | - Preserves authenticated state<br>- Re-renders current profile cleanly | **MANUAL READY** |
| **QA-01.8** | **Back/Forward Cache** | 1. Log out via POST<br>2. Click browser "Back" button | - `no-store` forces browser revalidation<br>- Redirects to login; no stale data | **MANUAL READY** |

---

### Domain 2: Event Management & Privacy (QA-02)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-02.1** | **Create Draft Event** | 1. Log in as organizer<br>2. Visit `/events/create`<br>3. Submit new event with status `draft` | - `POST /events/create` with CSRF<br>- Record created in SQLite<br>- Redirect to manage page | **MANUAL READY** |
| **QA-02.2** | **Edit Event Details** | 1. Click "Chỉnh sửa" on draft event<br>2. Modify title and description | - `POST /events/<id>/edit` with CSRF<br>- Changes saved to SQLite | **MANUAL READY** |
| **QA-02.3** | **Add Ticket Types** | 1. Visit `/events/<id>/tickets`<br>2. Add Free and Paid ticket types | - `POST /events/<id>/tickets/create`<br>- Quota allocated in SQLite | **MANUAL READY** |
| **QA-02.4** | **Publish Event** | 1. Click "Xuất bản sự kiện" | - `POST /events/<id>/edit` (status='published')<br>- Event appears on public `/events` | **MANUAL READY** |
| **QA-02.5** | **View Public Event & SEO** | 1. Open public event `/events/<id>`<br>2. Inspect source code | - Valid Schema.org Event JSON-LD present<br>- BreadcrumbList present<br>- Canonical URL valid | **AUTOMATED PASS** (Phase 3B) |
| **QA-02.6** | **Draft Event Privacy (404)** | 1. Copy URL of draft event<br>2. Open Private/Incognito window<br>3. Visit URL as anonymous | - HTTP 404 Not Found<br>- `X-Robots-Tag: noindex, nofollow`<br>- No draft data leaked | **AUTOMATED PASS** (T29) |

---

### Domain 3: Ticket Booking & Quota Integrity (QA-03)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-03.1** | **Free Ticket Registration** | 1. Log in as attendee<br>2. Select Free Ticket -> Submit | - `POST /tickets/register/<id>` with CSRF<br>- Registration confirmed; quota -1 | **MANUAL READY** |
| **QA-03.2** | **Complete Checkout** | 1. Review checkout page `/tickets/checkout/<id>`<br>2. Confirm registration | - `POST /tickets/checkout/<id>` with CSRF<br>- Ticket status set to `CONFIRMED` | **MANUAL READY** |
| **QA-03.3** | **View Personal QR Ticket** | 1. Go to `/tickets/view/<id>`<br>2. Inspect QR code | - QR code SVG rendered<br>- Print layout hides navbar/footer | **MANUAL READY** |
| **QA-03.4** | **Unauthorized QR Access** | 1. Log in as User 2<br>2. Attempt to open `/tickets/view/<User1_ID>` | - HTTP 403 Forbidden<br>- Access denied cleanly | **AUTOMATED PASS** (T25) |
| **QA-03.5** | **Ticket Cancellation** | 1. Click "Hủy vé" on `/tickets/my-tickets` | - `POST /tickets/cancel/<id>` with CSRF<br>- Status set to `CANCELLED`; quota +1 | **MANUAL READY** |
| **QA-03.6** | **Quota Consistency** | 1. Attempt registration when quota is 0 | - UI displays "Hết vé"<br>- Submission safely rejected | **AUTOMATED PASS** (Quota Suite) |

---

### Domain 4: Check-in Operations & Staff Tooling (QA-04)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-04.1** | **Staff Login & Scanner** | 1. Log in as staff account<br>2. Navigate to `/checkin/` | - Scanner UI loads<br>- Video viewfinder active | **MANUAL READY** |
| **QA-04.2** | **Camera Permission Prompt** | 1. Allow browser camera permission | - `navigator.mediaDevices.getUserMedia` succeeds<br>- Video stream binds to `<video>` | **MANUAL READY** |
| **QA-04.3** | **QR Scan Verification** | 1. Present attendee QR ticket to camera | - `POST /checkin/verify-api` via fetch<br>- `X-CSRFToken` attached<br>- Visual green checkmark; sound chime | **MANUAL READY** |
| **QA-04.4** | **Duplicate Rejection** | 1. Scan the identical QR code again | - Returns `already_checked_in`<br>- Red badge displays original scan time | **AUTOMATED PASS** (Upgrade Suite) |
| **QA-04.5** | **Quick Check-in from Roster** | 1. Go to `/checkin/`<br>2. Click Quick Check-in button for attendee | - `POST /checkin/api/quick-checkin/<id>`<br>- Instant DOM update without reload | **MANUAL READY** |
| **QA-04.6** | **Undo Check-in** | 1. Click Undo Check-in button | - `POST /checkin/api/undo-checkin/<id>`<br>- Status reverts to confirmed | **MANUAL READY** |

---

### Domain 5: AI Assistant & Services (QA-05)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-05.1** | **Open Floating Chatbot** | 1. Click floating sparkle icon in bottom right | - Smooth popover expansion<br>- Input auto-focuses; backdrop blur | **MANUAL READY** |
| **QA-05.2** | **Send Message (Offline Mock)** | 1. Type: *"Sự kiện nào diễn ra tuần này?"*<br>2. Press Enter | - `POST /api/ai/chat` with `X-CSRFToken`<br>- Grounded response formatted in Markdown | **AUTOMATED PASS** (AI Suite) |
| **QA-05.3** | **No External Token Leakage** | 1. Inspect network tab during AI call | - Request sent exclusively to same-origin<br>- Zero tokens sent to external APIs | **AUTOMATED PASS** (T15) |
| **QA-05.4** | **Fallback on Quota/Offline** | 1. Disconnect network or trigger 429 quota | - Local Grounded Fallback Mock Engine activates<br>- Clean, structured database answer returned | **AUTOMATED PASS** (AI Suite) |
| **QA-05.5** | **Escape Key Dismissal** | 1. Press `Escape` while chatbot is open | - Modal dismisses smoothly | **MANUAL READY** |
| **QA-05.6** | **Focus Restoration** | 1. Verify where keyboard focus lands | - Focus returns cleanly to floating sparkle button | **MANUAL READY** |

---

### Domain 6: Liquid Glass Design & Accessibility (QA-06)

| Case ID | Workflow / Action | Execution Steps | Expected Network & DOM Result | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **QA-06.1** | **Desktop Navigation** | 1. Navigate across all public pages | - Fixed glassmorphism navbar; smooth hover | **MANUAL READY** |
| **QA-06.2** | **Mobile Drawer Navigation** | 1. Emulate viewport <= 768px<br>2. Tap hamburger icon | - Slide-in mobile drawer displays smoothly<br>- Focus trapped inside drawer | **MANUAL READY** |
| **QA-06.3** | **Dark / Light Theme** | 1. Click theme toggle button | - `data-bs-theme` attribute switches<br>- Contrast ratio >= 4.5:1 (WCAG AA) | **AUTOMATED PASS** (Phase 3D) |
| **QA-06.4** | **Event Search & Filtering** | 1. Type keyword into search input | - Dynamic filtering without layout shifts | **MANUAL READY** |
| **QA-06.5** | **Liquid Glass Animations** | 1. Hover on event cards and buttons | - Subtle 1.02x scale; GPU-accelerated | **AUTOMATED PASS** (Phase 3D) |
| **QA-06.6** | **Keyboard Accessibility** | 1. Tab through entire page | - High-contrast focus rings on all controls | **MANUAL READY** |
| **QA-06.7** | **Reduced Motion** | 1. Enable `prefers-reduced-motion` | - All transitions collapse to instantaneous | **AUTOMATED PASS** (Phase 3D) |
| **QA-06.8** | **Ticket Print Preview** | 1. Press `Ctrl + P` on `/tickets/view/<id>` | - Exactly 1 ticket per page; clean print | **MANUAL READY** |

---

## 3. Staging Sign-Off Checklist for Human QA Team

Prior to production launch, the human QA team must execute the above manual test cases on the staging deployment URL and check off all domains:

- [ ] **Domain 1: Authentication & Session Lifecycle** (8/8 Cases Verified)
- [ ] **Domain 2: Event Management & Privacy** (6/6 Cases Verified)
- [ ] **Domain 3: Ticket Booking & Quota Integrity** (6/6 Cases Verified)
- [ ] **Domain 4: Check-in Operations & Staff Tooling** (6/6 Cases Verified)
- [ ] **Domain 5: AI Assistant & Services** (6/6 Cases Verified)
- [ ] **Domain 6: Liquid Glass Design & Accessibility** (8/8 Cases Verified)

**Overall Browser QA Status**: **PROTOCOL SPECIFIED — READY FOR HUMAN STAGING EXECUTION**

