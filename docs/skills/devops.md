# Skill — DevOps / Deployment

## Responsibility

Docker production configuration, nginx/gunicorn, environment management,
health checks, backups, kiosk browser setup, and event-day operations.

## Rules

1. Deployment model: local exhibition server (Option B) — nginx + gunicorn +
   PostgreSQL in Docker Compose; no Redis, no Kubernetes.
2. The core experience must run with zero internet: all assets (fonts, JS libs,
   avatars, branding) self-hosted; no CDN, no external APIs.
3. Secrets via `.env` (gitignored); `.env.example` is the template; production
   defaults are secure (`DEBUG=False`, restrictive hosts).
4. `/health/` endpoint reports app + DB status; compose services get
   healthchecks and `restart: unless-stopped`.
5. Backups: scheduled `pg_dump` to a mounted volume with a tested restore path.
6. Static assets: compiled Tailwind + collectstatic served by nginx.
7. Kiosk browser: documented Chrome kiosk-mode launch, autostart, screen-sleep
   prevention, and laminated recovery steps — no unsafe OS modifications by code.
8. Releases: build → migrate → seed (idempotent) → collectstatic → health check;
   no deploys on event day after freeze.
9. Verify `pip`/`npm` dependency locks committed for reproducible builds.

## Checklist (release)

- [ ] Fresh host: compose up from scratch works from README steps
- [ ] Health endpoint green; dashboard login reachable
- [ ] Backup/restore dry-run done
- [ ] Event-day runbook (exhibition-checklist.md) printed
