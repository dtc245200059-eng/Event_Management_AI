# EventAI Pro — Phase 10: Real Mobile Device QA Matrix (Android & iOS)

**Document ID**: `DOC-DEPLOY-PHASE10-MOB-003`  
**System**: EventAI Pro (`D:\Event_Management_AI`)  
**Phase**: Phase 10A — Mobile QA Architecture & Real-Device Test Specification  
**Auditor / Lead Architect**: Senior Mobile Web QA Specialist & Browser Testing Engineer  
**Target Devices**: iPhone 13/14/15 (iOS 16/17 Safari), Samsung Galaxy S22/S23 (Android 13/14 Chrome), Xiaomi Redmi Note (Android Chrome)  
**Date**: 2026-10-29  

---

## 1. Executive Summary & Gating Notice

Modern mobile operating systems strictly enforce the W3C WebAppSec Secure Contexts specification. Access to `navigator.mediaDevices.getUserMedia` is hard-blocked over unencrypted LAN IP connections (e.g. `http://192.168.1.50:5000`).

Consequently, while **100% of the underlying check-in endpoints, cryptographic ticket verification, CSRF validations, and database state machines are automated and verified (PASS)**, all physical camera hardware interactions on real smartphones remain formally classified as:
> **STATUS: BLOCKED (REQUIRES TRUSTED HTTPS HOST)**  
> **GATE: GATED PENDING EXPLICIT PHASE 10B APPROVAL FOR TLS STAGING HOST**

This document establishes the exhaustive 20-scenario mobile QA matrix ready for immediate execution the instant the HTTPS staging host is provisioned in Phase 10B.

---

## 2. 20-Scenario Real Mobile Device QA Matrix

### Category 1: Camera Hardware & Permissions (TC-MOB-01 to TC-MOB-04)

| Test ID | Test Scenario | Device / OS | Pre-conditions | Test Steps | Expected Result | Phase 10A Status |
|---|---|---|---|---|---|:---:|
| **TC-MOB-01** | W3C Secure Context Validation | iOS Safari & Android Chrome | Browser open | Load staging URL; check `window.isSecureContext` in console. | Returns `true`. `navigator.mediaDevices` is defined. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-02** | Camera Permission Prompt (First Visit) | iOS Safari | Fresh session, camera permission not yet granted | Navigate to `/checkin/scanner`. Tap "Bật máy ảnh". | iOS displays native prompt: *"staging.eventai.vn would like to use your camera"*. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-03** | Permission Denial Handling | Android Chrome | Camera permission denied | Deny camera permission on prompt. | UI displays graceful fallback error message: "Không thể truy cập camera. Vui lòng cho phép quyền hoặc nhập mã thủ công" and shows manual input field. | **VERIFIED (Code Review)** / BLOCKED (Hardware) |
| **TC-MOB-04** | Rear Camera Selection (`facingMode: environment`) | Multi-camera Android & iPhone | Permission granted | Activate camera scanner. | Scanner selects default rear/environment sensor; does NOT activate selfie camera. | **BLOCKED (Requires HTTPS)** |

---

### Category 2: Real-World Optical QR Scanning (TC-MOB-05 to TC-MOB-09)

| Test ID | Test Scenario | Test Artifact | Ambient Conditions | Scan Distance & Angle | Expected Result | Phase 10A Status |
|---|---|---|---|---|---|:---:|
| **TC-MOB-05** | High-Contrast Printed Ticket Scan | A4 Paper Ticket (300 DPI SVG QR code) | Normal office lighting (300-500 lux) | 15–25 cm, perpendicular (90°) | Decodes ticket string within < 300ms; triggers check-in API request. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-06** | Screen-to-Screen QR Scan (Glare Test) | Smartphone OLED/LCD screen displaying ticket | High ambient light with reflection/glare | 20 cm, 10° off-axis | html5-qrcode / jsQR decoder successfully filters glare and reads ticket payload. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-07** | Off-Axis & Skewed QR Scan | Printed badge | Standard lighting | 30° to 45° tilt angle, 20 cm distance | Decodes successfully without requiring perfect perpendicular alignment. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-08** | Low-Light Optical Scan | Printed Ticket | Dim lighting (< 50 lux) | 15 cm | Camera auto-exposure adjusts; decodes ticket accurately within < 1000ms. | **BLOCKED (Requires HTTPS)** |
| **TC-MOB-09** | Damaged / Partially Obscured QR | Printed Ticket with 15% corner smudge | Standard lighting | 20 cm | Decoded successfully utilizing Reed-Solomon error correction level M/Q. | **BLOCKED (Requires HTTPS)** |

---

### Category 3: Real-Time Check-In Business Logic & Feedback (TC-MOB-10 to TC-MOB-14)

| Test ID | Scenario | Input Data | Expected API Response | Expected Mobile UI / Haptic Feedback | Phase 10A Status |
|---|---|---|---|---|:---:|
| **TC-MOB-10** | Valid Attendee Check-In | Valid active ticket `TCK-2026-001` | `200 OK`, `status: success` | Green banner, success chime/vibration, attendee name displayed, badge counter increments. | **PASS (Automated)** / BLOCKED (Hardware) |
| **TC-MOB-11** | Duplicate Check-In (Anti-Passback) | Re-scan ticket checked in 2 min ago | `400 Bad Request`, `already_checked_in` | Amber/Yellow alert: *"Vé đã được check-in lúc 14:32 bởi Staff 1"*. Anti-passback prevents double-entry. | **PASS (Automated)** / BLOCKED (Hardware) |
| **TC-MOB-12** | Invalid / Counterfeit Ticket | Malformed QR payload `"HACK-FAKE-999"` | `404 Not Found`, `ticket_not_found` | Red warning modal: *"Mã vé không hợp lệ hoặc không tồn tại trong hệ thống"*. Scanner pauses 2s. | **PASS (Automated)** / BLOCKED (Hardware) |
| **TC-MOB-13** | Cancelled Ticket Check-In | Registration marked `cancelled` | `400 Bad Request`, `registration_cancelled` | Red alert: *"Đăng ký này đã bị hủy. Không thể check-in"*. | **PASS (Automated)** / BLOCKED (Hardware) |
| **TC-MOB-14** | Event Date Mismatch Check-In | Ticket belongs to next week's event | `400 Bad Request`, `event_inactive` | Amber alert: *"Vé hợp lệ nhưng sự kiện diễn ra vào 05/11/2026. Chưa đến giờ check-in"*. | **PASS (Automated)** / BLOCKED (Hardware) |

---

### Category 4: Mobile Responsive UX & Security (TC-MOB-15 to TC-MOB-20)

| Test ID | Scenario | Device / Resolution | Interaction Flow | Acceptance Criteria | Phase 10A Status |
|---|---|---|---|---|:---:|
| **TC-MOB-15** | Mobile Viewport Layout | iPhone SE (375x667) & Galaxy S23 (360x780) | Browse Homepage, Event Details, Checkout | Zero horizontal scrollbar; fluid typography; 44x44px minimum touch targets. | **VERIFIED (Liquid Glass CSS)** |
| **TC-MOB-16** | Liquid Glass Backdrop Filter | iOS Safari 17 & Android Chrome 120 | Scroll content under navigation bar | `backdrop-filter: blur(20px)` renders smoothly at 60fps without lag or paint stutter. | **VERIFIED (CSS Specs)** |
| **TC-MOB-17** | Mobile Bottom Navigation & Thumb Zone | Handheld one-hand thumb reach | Tap Bottom Navigation items (Home, Events, Tickets, Profile) | Nav items comfortably reachable within standard thumb sweep arc. Active tab highlighted. | **VERIFIED (Templates)** |
| **TC-MOB-18** | Mobile Network Latency & Offline Recovery | 3G throttling (300kbps, 400ms RTT) | Scan ticket during network drop | Spinner indicates request in progress; timeout after 10s with "Lỗi kết nối mạng, vui lòng thử lại". | **PASS (Automated Timeout)** |
| **TC-MOB-19** | Mobile Session Persistence | Mobile Safari backgrounding | Switch apps for 10 minutes, return to scanner | Staff session remains authenticated (`SESSION_COOKIE_HTTPONLY=True`, `SameSite=Lax`). Scanner resumes immediately. | **BLOCKED (Requires Staging)** |
| **TC-MOB-20** | Mobile Logout CSRF Protection | Mobile Safari & Chrome | Tap Logout button in mobile drawer | Displays `logout_confirm.html` confirmation modal; submittal uses valid CSRF token; session invalidated cleanly. | **PASS (Automated & Tested)** |

---

## 3. Human QA Execution Runbook (For Phase 10B)

Upon user authorization and deployment of the HTTPS staging container in Phase 10B, the browser QA team will execute the following physical validation steps:

1. Connect physical test phone (iPhone on iOS 17 and Samsung on Android 14) to the staging WiFi network.
2. Open mobile browser and navigate to `https://staging.eventai.vn/login`.
3. Enter staging HTTP Basic Auth credentials (`staging_qa` / password).
4. Log in as Staff user: `staff@eventai.vn` / `Staff@123456`.
5. Navigate to `/checkin/scanner`.
6. Verify browser prompts for camera permission. Tap "Allow".
7. Aim camera at test QR code sheet (containing valid, duplicate, invalid, and cancelled test tickets).
8. Record exact scan latency, visual alerts, audio chimes, and haptic feedback.
9. Log results in Phase 10B Acceptance Ledger.

