# Handover — AI Travel Personality Detector

World Tourism Day 2026 exhibition kiosk. This document is the operator-facing
summary of the delivered system: what it is, how to run it, what to do on
event day, and the key engineering decisions.

## 1. What Was Delivered

A production-ready, deterministic travel-persona kiosk experience:

- **Idle/attract screen → profile (name/age/gender) → 6-question Bangla quiz →
  1.6 s analysis → persona reveal → social-card result → auto/manual reset**
- Six personas: Heritage Hunter, Beach Lover, Adventure Seeker, Nature
  Explorer, Urban Explorer, Culture Connector — deterministic weighted scoring
  (no AI calls, works fully offline)
- Touch-first UI (44 px+ targets, no scrolling, 1920×1080 primary),
  self-hosted Hind Siliguri, vendored htmx/Alpine/Chart.js
- Staff analytics dashboard (`/dashboard/`) with traffic, completion, persona,
  hourly, age/gender, companion, kiosk and answer insights + CSV exports
- Django Admin content management: questions, answers, scoring weights,
  personas, avatars, age groups, questionnaire versions
- Docker Compose production stack: nginx + gunicorn + PostgreSQL

**Final validation:** 126 unit/integration tests + 12 browser E2E tests
(including a 100-consecutive-assessment soak) — all green. Full visitor flow
verified against the Docker production stack.

## 2. Running the System

```bash
cp .env.example .env                  # set DJANGO_SECRET_KEY, POSTGRES_PASSWORD
docker compose up -d --build          # web auto-runs migrate + collectstatic
docker compose exec web python manage.py seed_travel_personas
docker compose exec web python manage.py createsuperuser
```

- Kiosk: `http://<server-ip>/` (Chrome kiosk mode — see deployment.md §9)
- Dashboard: `http://<server-ip>/dashboard/` (staff login)
- Health: `http://<server-ip>/health/`

## 3. Event-Day Essentials

Print and follow `docs/exhibition-checklist.md`. Highlights:

- Verify `health/` endpoint, kiosk full-screen, touch calibration, system time
- Spot-check one "pure" run per persona against expected results
- Test reset + timeout; confirm previous visitor data never lingers
- Emergency: restart stack with `docker compose restart`; full procedure in
  deployment.md §10; laminated recovery card next to the kiosk
- Content changes after freeze: Admin only (questions/weights), never code
  deploys on event day

## 4. Replacing Placeholder Assets

Current KV/logos/avatars are neutral placeholders:

- **Per-page background images:** each kiosk page includes
  `templates/partials/page_background.html` from its wrapper
  (`templates/kiosk/<page>.html`) with an `image="branding/…"` path — change
  that one path per page to use a different photo (drop files in
  `static/backgrounds/` or `static/branding/kv/`, rebuild the image, then
  `docker compose exec web python manage.py collectstatic --noinput`).
  Overlay strength is per page too (`overlay="light|medium|dark"`).
- `static/branding/kv/`, `static/branding/logos/`,
  `static/branding/world-tourism-day/` — drop in final files, then
  `docker compose exec web python manage.py collectstatic --noinput`
- Avatars: add rows via **Admin → PersonaAvatar** (persona + gender +
  age group + static path + is_default) with files in
  `static/avatars/<persona_slug>/`; the fallback chain (exact → gender
  default → neutral → global) guarantees no broken images

## 5. Key Engineering Decisions

- **No AI in the classification path** — deterministic weights (DB-managed),
  instant, offline, reproducible. "AI" is branding only
- **Question 5 (companion) carries zero persona weight** — analytics-only
  trait (solo/couple/family/friends/destination_first)
- **Privacy:** visitor name lives only in the Django session (cleared on
  reset/timeout, never in PostgreSQL); exact age not stored (age group only)
- **Reliability:** idempotent answers, single-transaction completion,
  refresh-safe resume, inactivity guard, DB-enforced integrity
- **Deployment:** local LAN server (Option B); internet optional

## 6. Documentation Index

`docs/` — requirements, architecture, kiosk-experience, persona-model,
scoring-system (full weight matrix), database-design, htmx-flow, analytics,
privacy, testing, deployment, exhibition-checklist, development-plan, skills/.

## 7. Project State

Phases 1–22 complete. Git history follows the documented commit sequence.
Remaining work is on-site only: operator training, final asset drop-in,
kiosk browser setup.
