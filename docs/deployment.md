# Deployment Guide

## 1. Deployment Options Evaluated

| Option | Description | Pros | Cons | Verdict |
|---|---|---|---|---|
| A — Cloud hosted | Kiosk → internet → cloud Django/Postgres | Central analytics, remote admin | Internet dependency at the booth; latency; failure mode | Fallback only |
| B — Local exhibition server | Kiosks → LAN → one Docker host (nginx + gunicorn + Postgres) | Zero internet dependency, <300 ms, full control | Onsite setup, local hardware | **Recommended** |
| C — Single machine (all on kiosk) | Django + Postgres on the kiosk box | Simplest for 1 kiosk | Kiosk becomes SPOF for data; weaker isolation | Acceptable for exactly 1 kiosk |

**Recommendation: Option B** — a small server (any x86 box/laptop) on the venue
LAN running Docker Compose; kiosks browse `http://<server-ip>/` in Chrome kiosk
mode. Internet is optional and used only out-of-band (backups, remote support).

## 2. Docker Compose Topology

Services: `web` (gunicorn), `db` (postgres), `nginx` (static + reverse proxy).
No Redis in MVP.

```
kiosk browsers ──▶ nginx:80 (also :443 if TLS enabled) ──▶ web:8000 ──▶ db:5432
                       └─ serves /static/ directly
```

```yaml
# docker-compose.yml (skeleton)
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
    env_file: .env
    depends_on: [db]
  db:
    image: postgres:16
    environment: [POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD]
    volumes: [pgdata:/var/lib/postgresql/data]
  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes: [./nginx.conf:/etc/nginx/conf.d/default.conf, static:/static]
    depends_on: [web]
volumes: {pgdata: {}, static: {}}
```

Nginx: serves `/static/`, proxies `/` to web, `proxy_read_timeout` generous for
the LAN, gzip for text assets.

## 3. Environment Variables (.env.example)

```
DJANGO_SECRET_KEY=<generate with get_random_secret_key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<server-ip>,localhost
# Exhibition LANs often serve plain HTTP on a closed network. Default True
# (TLS-ready). Set False ONLY when TLS termination is unavailable:
# DJANGO_SECURE_COOKIES=True
POSTGRES_DB=travel_persona
POSTGRES_USER=travel_persona
POSTGRES_PASSWORD=<strong password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
KIOSK_IDENTIFIER=KIOSK-01
# optional:
EXPERIENCE_RESET_DELAY_SECONDS=45
```

Never commit `.env`. `.env.example` is the documented template.

## 4. Production Settings (config/settings/production.py)

`DEBUG=False`, `ALLOWED_HOSTS` from env, secure cookies, HTTPS behind nginx
(`SECURE_PROXY_SSL_HEADER`), static via `collectstatic`, `SESSION_COOKIE_SECURE`,
no admin URL obfuscation needed but keep staff auth strict, file logging to
stdout (docker logs) without PII.

## 5. Release Procedure

```bash
docker compose build && docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py seed_travel_personas
docker compose exec web python manage.py createsuperuser   # dashboard/admin staff
# verify
curl http://<server-ip>/health/   # {"status": "ok", "db": true}
```

## 6. Health Checks

- `/health/` returns 200 JSON with DB connectivity flag; nginx/kiosk watchdog can
  poll it.
- Docker healthchecks on `db` (`pg_isready`) and `web` (curl /health/).

## 7. Static Assets & Fonts

- Tailwind built at image build time; output collected into the static volume.
- Self-host `Noto Sans Bengali` (OFL) in `static/fonts/` with system fallbacks;
  license file kept alongside.
- Avatar/branding assets deployed as static files with the fallback chain
  (database-design.md §PersonaAvatar).

## 8. Backups

- Nightly (or post-event) `pg_dump` from the `db` container to a mounted volume,
  optionally `rsync`ed offsite when internet exists.
- Document restore: `pg_restore` into a fresh db container.

## 9. Kiosk Browser Setup (Chrome/Chromium)

Documented for operators (no unsafe OS changes performed by code):

1. Launch: `chrome --kiosk http://<server-ip>/ --disable-pinch --overscroll-history-navigation=0`
   (autostart via desktop entry/startup task on the kiosk OS).
2. Prevent accidental navigation: kiosk mode hides chrome UI; disable
   `--enable-swipe` gestures; optionally `--disable-context-menu`.
3. Screen sleep: disable screen sleep/lock in OS power settings (and consider a
   Caffeine-style keep-awake utility).
4. Recovery: document "close browser → relaunch shortcut" and "restart machine"
   steps on a laminated card next to the kiosk.

## 10. Restart / Failure Procedures

- Web/db restart: `docker compose restart web db` (sessions are cookie-based;
  in-flight quizzes restart cleanly to the error/recovery screen).
- Full restart: `docker compose up -d` after host reboot; autostart policy
  `restart: unless-stopped` on all services.
- DB failure: watch `/health/`; runbook restores latest `pg_dump`.

## 11. Internet Independence Checklist (event-day)

Core quiz: no external calls at all. Verify: no third-party fonts/CDNs, no
analytics beacons, no AI APIs, Chart.js and htmx/alpine bundled locally.
