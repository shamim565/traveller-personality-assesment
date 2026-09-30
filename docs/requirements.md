# Requirements — AI Travel Personality Detector

World Tourism Day 2026 interactive exhibition experience.

## 1. Business Objective

Deliver a touchscreen kiosk activation for a World Tourism Day 2026 exhibition stall that:

- attracts visitors to the stall
- lets a visitor identify their **Travel Persona** in **60–90 seconds**
- produces a visually shareable, personalized result ("Sazid, You Are a Heritage Hunter!")
- collects privacy-conscious, aggregate analytics for post-event reporting
- runs reliably for hours without operator intervention

This is an **exhibition activation**, not a conventional web application. Reliability, speed, visual impact, touch usability, and simplicity outrank technical novelty.

## 2. Functional Requirements

### FR-1 — Attract (Idle) screen
- Full-screen attract loop with headline "DETECT YOUR TRAVEL PERSONA".
- Single CTA: "Discover My Travel Personality".
- World Tourism Day 2026 key visual, organizer/sponsor logos, persona graphics, subtle animation.
- All branding assets configurable via `static/branding/` with graceful fallbacks.

### FR-2 — Basic information
- Collect **Name** (Bangla/English, spaces, common punctuation; minimal validation), **Age** (touch-friendly, configurable range, default 10–100), **Gender** (large touch cards: Male / Female / Prefer not to say; configurable).
- Name personalizes the result only. Age/Gender never affect persona classification.

### FR-3 — Quiz
- Exactly **6 questions**, one at a time, large answer cards, no typing, no scrolling.
- Visible progress. Server-driven transitions (HTMX), smooth reveal.
- Target 5–8 seconds per question.

### FR-4 — Deterministic persona detection
- No LLM/remote AI call. Explicit weight matrix stored in the database.
- Same answers always produce the same result.
- Output: raw scores, normalized scores, ranked personas, primary + secondary persona, tie metadata.

### FR-5 — Result reveal
- Brief "Analyzing your travel personality…" transition (1–2 s), then reveal.
- Result screen: name, persona title, curated avatar (Persona + Gender + Age Group), short description, keywords, optional "Your Travel Style" / "You Might Love" lists, campaign branding.

### FR-6 — Avatar system
- Pre-created static assets; no live AI generation.
- Deterministic fallback chain: exact → persona+gender default → persona neutral → global default. Never a broken image.

### FR-7 — Session lifecycle
- Django-session-based visitor state; name never persisted to PostgreSQL by default.
- Manual "Start Again" plus configurable inactivity reset (45 s mid-quiz; 30–45 s on result).
- Next visitor must never see previous visitor data.

### FR-8 — Analytics persistence
- Persist one completed assessment per visitor: session UUID, age group, gender, questionnaire version, answers, persona scores, primary/secondary persona, timestamps, duration, kiosk identifier.
- Store age **group** (not exact age) by default. Never store the name.

### FR-9 — Analytics dashboard
- Staff-authenticated, `/dashboard/`, not reachable from the kiosk UI.
- Summary metrics, persona distribution, hourly traffic, age/gender distributions (where approved), average duration, answer distributions.
- Chart.js for a small number of meaningful charts.

### FR-10 — Content management
- Questions, answer options, scoring weights, personas, questionnaire versions, age groups, and avatars editable in Django Admin. No custom CMS.

### FR-11 — CSV export
- Authenticated export of assessment summary, persona distribution, answer responses, hourly traffic. No personal data.

### FR-12 — Multi-kiosk support
- Each assessment records `kiosk_identifier` (e.g. `KIOSK-01`) for per-device analytics and troubleshooting.

## 3. Non-Functional Requirements

| Area | Requirement |
|---|---|
| Determinism | Scoring is pure, repeatable, offline |
| Latency | Initial load < 3 s on exhibition hardware; question transition near-instant; HTMX request ideally < 300 ms on LAN; scoring < 100 ms |
| Reliability | Survives browser refresh, rapid double-taps, long sessions, app restart, DB hiccups; friendly recovery screen instead of error pages |
| Availability | Core quiz has zero internet dependency (no external AI/APIs) |
| Privacy | Data minimization; name in session only; no silent PII persistence |
| Security | CSRF, server-side validation, HTTPS, secure cookies, DEBUG=False, restrictive ALLOWED_HOSTS, authenticated dashboard, ORM-only queries |
| Accessibility | Semantic HTML, large text, high contrast, visible focus, 44 px+ touch targets, not color-only |
| Localization | Bangla-first UI; architecture supports `_bn`/`_en` fields and English later |
| Maintainability | Monolith with thin views, service layer, selectors; config over hardcoding |
| Operability | Docker Compose deployment, health endpoint, documented kiosk/browser setup, backup/restart runbooks |

## 4. MVP Scope

Idle screen → profile (name/age/gender) → 6-question Bangla quiz → analysis transition → persona reveal + avatar → result → restart/timeout reset. The result screen shows a QR code; scanning it opens a downloadable PNG of the result card on the visitor's phone (no visitor name included). Backing: Django Admin content management, seeded questionnaire, deterministic scoring engine, analytics persistence + dashboard, Docker production config, full documentation.

## 5. Future Scope (NOT in MVP)

Social sharing card, WhatsApp result, English UI, destination recommendations, tourism package suggestions, AI-generated descriptions/itineraries (only as clearly-optional, internet-dependent add-ons), CRM/email/WhatsApp integrations, multiple campaigns/locations, real-time remote analytics.

## 6. Explicit Exclusions

User registration, social login, mobile app, React/Next/SPA frontend, Django REST Framework, GraphQL, microservices, AI image generation, live LLM scoring, facial recognition, booking/payment, Kubernetes, Kafka, RabbitMQ, Redis (unless a measured need appears).

## 7. Assumptions

1. One active questionnaire version per exhibition period; version recorded per assessment.
2. Exact age is not required for business reporting; age group suffices (documented decision; reversible).
3. Gender collection is stakeholder-approved and aggregate-only.
4. Kiosks share one Django server on the exhibition LAN.
5. At least one operator can run documented restart/backup procedures.
6. Final campaign assets (KV, logos) may arrive late; fallback assets ship with the app.

## 8. Key Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Internet outage at venue | Quiz dies if any cloud dependency exists | Fully local deterministic stack; zero runtime internet dependency |
| Kiosk browser crash/refresh mid-quiz | Broken visitor state | Session-keyed flow; refresh re-enters at current step; friendly error + restart |
| Rapid double-taps | Duplicate answers/records | Idempotent answer storage (one per question), UI disabling during transition, unique constraints |
| Asset delays (KV, logos, avatars) | Broken images, off-brand look | Configurable static paths + deterministic fallback chain + neutral placeholder set |
| Wrong persona feel (miscalibration) | Bad visitor experience | Calibration test suite before launch; admin-editable weights without code changes |
| Previous visitor's data leaking to next visitor | Privacy incident | Mandatory session clear on every reset/timeout; manual "Start Again" on result |
| DB failure during event | Data loss | Single-node Postgres + documented pg_dump schedule; app degrades to friendly error |

## 9. Open Questions for Stakeholders (non-blocking)

- Confirm age range (default 10–100) and age-group boundaries.
- Confirm gender options (Male / Female / Prefer not to say).
- Approve zero persona-weight handling of Question 5 (companion trait for analytics only).
- Confirm kiosk count and identifiers (KIOSK-01…).
- Confirm whether exact age or only age group may be stored.
- Final campaign branding, hashtag, and logo assets.
