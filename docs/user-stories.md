# User Stories Specification

> **Dự Án:** Hệ Thống Quản Lý Sự Kiện Tích Hợp AI (Event Management AI System)  
> **Trạng thái triển khai:** `[IMPLEMENTED]` (Đầy đủ 20/20 User Stories cho 4 vai trò tác nhân)  
> **Tài Liệu Tham Chiếu:** [requirements.md](file:///d:/Event_Management_AI/docs/requirements.md), [customer-requirement.md](file:///d:/Event_Management_AI/docs/customer-requirement.md), [acceptance-criteria.md](file:///d:/Event_Management_AI/docs/acceptance-criteria.md), [traceability-matrix.md](file:///d:/Event_Management_AI/docs/traceability-matrix.md)  
> **Kỹ năng liên quan:** [requirements-analysis](file:///d:/Event_Management_AI/.agents/skills/requirements-analysis/SKILL.md)  
> **Quy Chuẩn Định Dạng:** `As a <role>, I want <capability>, so that <benefit>`

---

## 1. Danh Sách User Stories Theo Tác Nhân (Actors)

### 1.1. Nhóm Người Tham Dự (Attendee)

| Story ID | Trạng Thái | User Story (Nội Dung) | Liên Kết FR | Mức Độ Ưu Tiên |
| :--- | :---: | :--- | :--- | :---: |
| **US-ATT-01** | `[IMPLEMENTED]` | **As an Attendee**, I want to create an account and log in securely, **so that** I can manage my event registrations and ticket history. | `FR-01` | High |
| **US-ATT-02** | `[IMPLEMENTED]` | **As an Attendee**, I want to browse, search, and filter published events by category and date, **so that** I can find events matching my professional interests. | `FR-02` | High |
| **US-ATT-03** | `[IMPLEMENTED]` | **As an Attendee**, I want to view detailed event timeline schedules and speaker bios, **so that** I know who is speaking and what topics will be presented. | `FR-03` | High |
| **US-ATT-04** | `[IMPLEMENTED]` | **As an Attendee**, I want to register and select ticket types (Free, Standard, VIP), **so that** I can secure my seat with transparent pricing and real-time quota status. | `FR-04`, `FR-05` | Critical |
| **US-ATT-05** | `[IMPLEMENTED]` | **As an Attendee**, I want to access my digital tickets with unique QR codes on my mobile device, **so that** I can present it for fast check-in at the venue entrance. | `FR-06` | Critical |
| **US-ATT-06** | `[IMPLEMENTED]` | **As an Attendee**, I want to cancel my ticket registration if I cannot attend, **so that** my ticket quota is returned to other interested participants. | `FR-04`, `FR-05` | Medium |
| **US-ATT-07** | `[IMPLEMENTED]` | **As an Attendee**, I want to submit feedback and star ratings after attending an event, **so that** the organizers can improve future events. | `FR-08` | Medium |
| **US-ATT-08** | `[IMPLEMENTED]` | **As an Attendee**, I want to chat with the AI Assistant using natural language, **so that** I can quickly get answers about schedules, speakers, tickets, and venues 24/7. | `FR-AI-01` | High |
| **US-ATT-09** | `[IMPLEMENTED]` | **As an Attendee**, I want to receive personalized event recommendations based on my viewing history and interests, **so that** I discover relevant tech seminars. | `FR-AI-05` | Medium |
| **US-ATT-10** | `[IMPLEMENTED]` | **As an Attendee**, I want to receive notifications and announcements in my private inbox, **so that** I am updated about schedule changes or venue alerts. | `FR-07` | High |
| **US-ATT-11** | `[IMPLEMENTED]` | **As an Attendee**, I want to consult a Multi-Agent Decision Advisory system with transparent reasoning, **so that** I can compare complex event trade-offs and find optimal events matching my budget and location. | `FR-AI-07` | High |

---

### 1.2. Nhóm Nhân Viên Soát Vé (Staff)

| Story ID | Trạng Thái | User Story (Nội Dung) | Liên Kết FR | Mức Độ Ưu Tiên |
| :--- | :---: | :--- | :--- | :---: |
| **US-STF-01** | `[IMPLEMENTED]` | **As a Staff member**, I want to log in with my designated staff credentials, **so that** I can access the operational check-in scanner module. | `FR-01` | High |
| **US-STF-02** | `[IMPLEMENTED]` | **As a Staff member**, I want to scan attendee QR codes using my web browser camera or enter ticket codes manually, **so that** I can verify ticket validity within 500ms. | `FR-06` | Critical |
| **US-STF-03** | `[IMPLEMENTED]` | **As a Staff member**, I want the system to immediately warn and reject already-checked-in tickets, **so that** duplicate check-ins and ticket fraud are completely prevented. | `FR-06` | Critical |
| **US-STF-04** | `[IMPLEMENTED]` | **As a Staff member**, I want to view the live attendee check-in count for the ongoing event, **so that** I know how many participants have arrived. | `FR-06`, `FR-09` | Medium |

---

### 1.3. Nhóm Ban Tổ Chức (Organizer)

| Story ID | Trạng Thái | User Story (Nội Dung) | Liên Kết FR | Mức Độ Ưu Tiên |
| :--- | :---: | :--- | :--- | :---: |
| **US-ORG-01** | `[IMPLEMENTED]` | **As an Organizer**, I want to broadcast targeted announcements (all, checked-in, not checked-in, VIP), **so that** I can communicate efficiently with attendees. | `FR-07` | High |
| **US-ORG-02** | `[IMPLEMENTED]` | **As an Organizer**, I want to generate professional email and notification drafts with AI without leaking attendee PII, **so that** I save communication overhead. | `FR-AI-02` | High |
| **US-ORG-03** | `[IMPLEMENTED]` | **As an Organizer**, I want AI to automatically summarize attendee feedback into 4 structured themes and extract actionable improvements, **so that** I can enhance upcoming events. | `FR-AI-03` | High |

---

### 1.4. Nhóm Quản Trị Viên (Admin)

| Story ID | Trạng Thái | User Story (Nội Dung) | Liên Kết FR | Mức Độ Ưu Tiên |
| :--- | :---: | :--- | :--- | :---: |
| **US-ADM-01** | `[IMPLEMENTED]` | **As an Admin**, I want to create, edit, publish, and delete events with banner images, categories, and venues, **so that** I can manage the event catalog efficiently. | `FR-02` | High |
| **US-ADM-02** | `[IMPLEMENTED]` | **As an Admin**, I want to assign speakers, session timelines, and conference rooms to events, **so that** attendees have an organized schedule. | `FR-03` | High |
| **US-ADM-03** | `[IMPLEMENTED]` | **As an Admin**, I want to configure ticket tiers with strict quota limits and pricing, **so that** the system prevents overselling. | `FR-04` | Critical |
| **US-ADM-04** | `[IMPLEMENTED]` | **As an Admin**, I want to monitor real-time analytics dashboards showing total revenue, ticket sales, check-in percentages, and attendance charts, **so that** I make data-driven decisions. | `FR-09` | High |
| **US-ADM-05** | `[IMPLEMENTED]` | **As an Admin**, I want to use AI to automatically generate engaging event descriptions and agenda drafts, **so that** I save marketing copywriting time. | `FR-AI-04` | Medium |
| **US-ADM-06** | `[IMPLEMENTED]` | **As an Admin**, I want to view AI predictive attendance forecasts (% show-up rate) and sentiment analysis summaries of attendee feedback, **so that** I can optimize catering and evaluate event success. | `FR-AI-06` | High |
| **US-ADM-07** | `[IMPLEMENTED]` | **As an Admin**, I want to manage system user accounts, toggle active statuses, and assign roles (Admin, Staff, Attendee), **so that** system security and RBAC governance are upheld. | `FR-01` | High |

---

## 2. Ma Trận Truy Vết User Story ── Yêu Cầu Chức Năng (Traceability)

```
[FR-01 Auth & RBAC] ────────────► US-ATT-01, US-STF-01, US-ADM-07
[FR-02 Event CRUD] ─────────────► US-ATT-02, US-ADM-01
[FR-03 Speaker & Schedule] ─────► US-ATT-03, US-ADM-02
[FR-04 Ticketing & Quotas] ─────► US-ATT-04, US-ATT-06, US-ADM-03
[FR-05 Booking & Payment] ──────► US-ATT-04, US-ATT-06
[FR-06 QR Check-in] ────────────► US-ATT-05, US-STF-02, US-STF-03, US-STF-04
[FR-07 Communications] ────────► US-ATT-10, US-ORG-01
[FR-08 Feedback & Survey] ──────► US-ATT-07
[FR-09 Dashboard Analytics] ────► US-ADM-04, US-STF-04
[FR-AI-01 RAG Chatbot] ─────────► US-ATT-08
[FR-AI-02 Draft Generator] ─────► US-ORG-02
[FR-AI-03 Feedback Summary] ────► US-ORG-03
[FR-AI-04 Event Generator] ─────► US-ADM-05
[FR-AI-05 Recommendations] ─────► US-ATT-09
[FR-AI-06 Predictive/Sentiment] ─► US-ADM-06
[FR-AI-07 Multi-Agent Advisory] ─► US-ATT-11
```
