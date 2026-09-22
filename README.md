# AI Travel Personality Detector

Interactive exhibition activation for **World Tourism Day 2026**: a touchscreen
kiosk that identifies a visitor's Travel Persona in 60–90 seconds — no accounts,
no typing (beyond a name), fully offline-deterministic, privacy-conscious, and
analytics-enabled.

## Stack

- **Backend:** Python, Django (full-stack monolith — no SPA, no DRF)
- **Frontend:** Django Templates + HTMX + Tailwind CSS + minimal Alpine.js
- **Database:** PostgreSQL
- **Admin/Content:** Django Admin (questions, answers, weights, personas, avatars)
- **Testing:** pytest, pytest-django, Django test client, Playwright (kiosk E2E)
- **Production:** Docker Compose — nginx + gunicorn + PostgreSQL (local exhibition server)

## The Experience

Idle/Attract → Name · Age · Gender → 6-question Bangla quiz (one at a time,
large touch cards) → 1.6 s "Analyzing…" → persona reveal → avatar + personalized
result → auto/manual reset. Deterministic scoring: no external AI calls, same
answers always produce the same persona.

## Six Personas

Heritage Hunter · Beach Lover · Adventure Seeker · Nature Explorer ·
Urban Explorer · Culture Connector

## Documentation

| Doc | Contents |
|---|---|
| [docs/requirements.md](docs/requirements.md) | Scope, MVP, exclusions, risks |
| [docs/architecture.md](docs/architecture.md) | Monolith design, modules, session strategy, security |
| [docs/kiosk-experience.md](docs/kiosk-experience.md) | Screen-by-screen flow, timings, reset/timeout |
| [docs/persona-model.md](docs/persona-model.md) | Persona boundaries, overlaps, avatar logic |
| [docs/scoring-system.md](docs/scoring-system.md) | Full weight matrix, ties, normalization, calibration |
| [docs/database-design.md](docs/database-design.md) | Models, constraints, indexes, ER overview |
| [docs/htmx-flow.md](docs/htmx-flow.md) | Every HTMX interaction and partial |
| [docs/analytics.md](docs/analytics.md) | Metrics, queries, dashboard, exports |
| [docs/privacy.md](docs/privacy.md) | Data inventory, retention, name strategy |
| [docs/testing.md](docs/testing.md) | Test strategy incl. E2E + reliability |
| [docs/deployment.md](docs/deployment.md) | Docker, env vars, kiosk mode, backups |
| [docs/exhibition-checklist.md](docs/exhibition-checklist.md) | Event-day runbook |
| [docs/development-plan.md](docs/development-plan.md) | Phase sequence and gates |
| [docs/skills/](docs/skills/) | Engineering skill guides used by the team |

## Status

**Phases 1–22 complete.** The MVP is production-ready and Docker-validated
(nginx → gunicorn → PostgreSQL). Remaining: Phase 22 on-site handover
(staff training, final asset drop-in, kiosk setup per docs/exhibition-checklist.md).

## Quickstart

```bash
cp .env.example .env            # fill in secrets (see docs/deployment.md)
docker compose up -d --build    # web runs migrate + collectstatic on start
docker compose exec web python manage.py seed_travel_personas
docker compose exec web python manage.py createsuperuser
# kiosk: http://localhost/        dashboard: http://localhost/dashboard/
```

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
npm install && npm run build:css
python manage.py migrate && python manage.py seed_travel_personas
python manage.py runserver
pytest                # unit + integration (fast)
pytest -m e2e         # browser E2E incl. 100-assessment soak (slow)
```
