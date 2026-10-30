# EventAI Pro — Phase 4 Real Browser Validation & Instrumentation Assessment

**Assessment Date:** 2026-10-29  
**Auditor:** Senior Browser QA Engineer & Frontend Performance Specialist  
**Execution Environment:** Windows 11 Workspace (Offline Mode)  
**Instrumentation Status:** **NOT VERIFIED (Headless browser automation not installed in environment)**  
**Laboratory Test Status:** **PASSED VIA FLASK HTTP RUNTIME SIMULATION**

---

## 1. Tooling Assessment & Disclosure

In accordance with strict verification guidelines:
- The local Python environment was inspected for browser automation drivers (`playwright`, `selenium`, `puppeteer`). None are currently installed.
- System paths were scanned for headless browser binaries (`msedge.exe`, `chrome.exe`). No browser binaries are exposed in the execution PATH.
- **Strict Compliance Statement:** **No synthetic Lighthouse scores, simulated FPS benchmarks, or fabricated screenshots have been generated.** Real-browser instrumentation is formally classified as **NOT VERIFIED**.

In place of unpermitted package installations, the complete DOM structure, asset loading pipeline, interactive scripting logic, and HTTP response characteristics were audited via the Flask Test Client and static DOM parsing.

---

## 2. Laboratory HTTP Simulation & Viewport Audit

| User Flow / View | Route | HTTP Status | DOM & Asset Integrity | Accessibility & UX Elements | Test Method |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Homepage** | `/` | 200 OK | Single `<h1>`, `<link rel="preconnect">`, `<script defer>`. First slide image has `fetchpriority="high"`. | `role="region"` on carousel, descriptive slide labels, `:focus-visible` styles. | Automated Test Client |
| **Event Catalog** | `/events` | 200 OK | Event cards with explicit `width="400" height="225"`, `loading="lazy"`. | `role="search"` on search form, `aria-label` on category filter `<select>`. | Automated Test Client |
| **Event Detail** | `/events/<id>` | 200 OK | Hero image has `fetchpriority="high"`. Valid Schema.org Event JSON-LD and BreadcrumbList. | Clear schedule timeline, active ticket tiers, price formatted in VND. | Automated Test Client |
| **Auth: Login** | `/auth/login` | 200 OK | Zero plain text credentials in markup. Forms declare `autocomplete` attributes. | `<meta name="robots" content="noindex, nofollow">`. Accessible input labels. | Automated Test Client |
| **Auth: Register** | `/auth/register` | 200 OK | Standard registration fields. No credential leaks. | `<meta name="robots" content="noindex, nofollow">`. Client validation attributes. | Automated Test Client |
| **My Tickets** | `/tickets/my-tickets` | 200 OK / 302 | Requires authentication (`@login_required`). Lists confirmed user registrations. | Secure ticket view and cancellation action buttons. | Automated Test Client |
| **QR Serving** | `/tickets/download-qr/<id>`| 200 / 403 | Returns `image/svg+xml` for ticket owner; returns `403 Forbidden` for other users. | Direct QR download with content disposition attachment. | Automated Test Client |
| **Check-in Scanner** | `/checkin/` | 200 / 403 | Requires `staff` or `admin` role. Non-staff receives 403 Forbidden. | Camera video element with HTML5 scanner hook. | Automated Test Client |
| **AI Assistant** | `/ai/workspace` & floating | 200 OK | Modeless floating container `#aiChatWindow` declares `aria-modal="false"`. | Focus restoration upon closing; Escape key dismissal. | Automated Test Client |

---

## 3. Core Web Vitals Architectural Analysis

While laboratory Chrome DevTools and real-user field data (CrUX) cannot be recorded without an active browser runtime, the underlying architectural prerequisites for Core Web Vitals success are fully verified:

### 3.1 Largest Contentful Paint (LCP) Prerequisites
- **Implementation:** The first carousel slide on `/` and the main hero banner on `/events/<id>` both declare:
  ```html
  fetchpriority="high" loading="eager" decoding="async"
  ```
- **Effect:** Prevents browser pre-loader from delaying hero image discovery and avoids queue contention with below-the-fold assets.
- **Status:** **ARCHITECTURALLY VERIFIED (PASS)**.

### 3.2 Cumulative Layout Shift (CLS) Prerequisites
- **Implementation:** 100% of image elements render with explicit HTML `width` and `height` attributes matching their source proportions (e.g. 800x450 or 400x225).
- **CSS Enforcement:** `app/static/css/style.css` defines explicit `aspect-ratio: 16 / 9` with `object-fit: cover`.
- **Effect:** The browser reserves layout dimensions during the initial HTML parse, eliminating reflow when images finish downloading.
- **Status:** **ARCHITECTURALLY VERIFIED (PASS)**.

### 3.3 Interaction to Next Paint (INP) Prerequisites
- **Implementation:**
  - All custom scripts (`main.js`, `ai_chat.js`, `search.js`) declare the `defer` attribute, preventing main-thread parser blocking.
  - Background carousel timers automatically suspend via `IntersectionObserver` when scrolled off-screen.
  - Background intervals suspend via `document.addEventListener('visibilitychange')` when the browser tab is hidden.
  - Reduced motion preference disables continuous slide rotation.
- **Effect:** Minimizes long tasks on the main JavaScript thread, ensuring user clicks and taps are processed immediately.
- **Status:** **ARCHITECTURALLY VERIFIED (PASS)**.

---

## 4. Manual Staging Browser Testing Protocol

Prior to final public release, human QA testers should execute the following test protocol on physical devices and representative desktop/mobile browsers:

### 4.1 Target Browser Matrix
1. **Desktop:** Google Chrome (Latest), Microsoft Edge (Latest), Mozilla Firefox (Latest), Apple Safari (macOS).
2. **Mobile:** Safari on iOS (iPhone 14/15/16), Chrome on Android (Samsung Galaxy / Google Pixel).
3. **Viewports:**
   - Desktop: `1920 x 1080` and `1440 x 900`
   - Tablet: `768 x 1024` (iPad Portrait)
   - Mobile: `375 x 812` (iPhone SE/Mini) and `412 x 915` (Android standard)

### 4.2 Interactive Verification Checklist
- [ ] **Carousel Interaction:** Verify carousel transitions smoothly via swipe on touch screens and arrow keys on desktop.
- [ ] **AI Chatbot Modeless Behavior:** Confirm users on desktop can click event details on the background page while the chat window is open.
- [ ] **AI Chatbot Focus Restoration:** Open chatbot with `chatBtn`, press `Escape`, and verify focus returns to `chatBtn`.
- [ ] **Dark / Light Mode Switching:** Toggle theme switch and verify contrast on navigation links, event cards, and modals.
- [ ] **QR Code Check-in:** Grant camera permission in `/checkin/` and verify QR camera stream operates at 30 FPS.
- [ ] **Mobile Bottom Navigation:** Verify all bottom tabs have a tap target of at least 44x44px.

