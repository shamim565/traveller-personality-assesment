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
- **Production:** Docker Compose — gunicorn + PostgreSQL behind an existing nginx (`docs/deployment-vps.md`)

## The Experience

Idle/Attract → Name · Age · Gender → 6-question Bangla quiz (one at a time,
large touch cards) → 1.6 s "Analyzing…" → persona reveal → avatar + personalized
result → QR code to download the result picture (with the visitor's name) →
"Start Again". Deterministic scoring: no external AI calls, same answers always
produce the same persona.

## Six Personas

Heritage Hunter · Beach Lover · Adventure Seeker · Nature Explorer ·
Urban Explorer · Culture Connector

## Documentation

- [docs/deployment-vps.md](docs/deployment-vps.md) — Docker stack, env vars, TLS, backups

## Quickstart

```bash
cp .env.example .env            # fill in secrets (see docs/deployment-vps.md)
docker compose up -d --build    # web runs migrate + collectstatic on start
docker compose exec web python manage.py seed_travel_personas
docker compose exec web python manage.py createsuperuser
# kiosk: http://localhost/        dashboard: http://localhost/dashboard/
```

## Local development

```bash
uv sync                         # creates .venv from pyproject.toml + uv.lock
npm install && npm run build:css
uv run python manage.py migrate && uv run python manage.py seed_travel_personas
uv run python manage.py runserver
```
