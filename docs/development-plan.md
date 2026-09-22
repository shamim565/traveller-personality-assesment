# Development Plan

Sequenced phases. Architecture-first: no feature code before the foundation is
locked. This document is the single source of sequencing truth; statuses update
as work proceeds.

## Phases

| # | Phase | Deliverables | Status |
|---|---|---|---|
| 1 | Requirements | docs/requirements.md | ✅ Done |
| 2 | MVP definition | scope/future/exclusions (requirements.md §4–6) | ✅ Done |
| 3 | Experience architecture | docs/kiosk-experience.md | ✅ Done |
| 4 | Persona architecture | docs/persona-model.md, docs/scoring-system.md | ✅ Done |
| 5 | Technical architecture | docs/architecture.md, database-design.md, htmx-flow.md, analytics.md, privacy.md, testing.md, deployment.md | ✅ Done |
| 6 | Agent skills | docs/skills/*.md | ✅ Done |
| 7 | Project bootstrap | Django project, settings package, Tailwind/HTMX/Alpine wiring, pytest, Docker skeleton; app starts | ⬜ Next |
| 8 | Models | all §2 database-design.md models + migrations + constraints/indexes | ⬜ |
| 9 | Admin | content management for versions/questions/answers/weights/personas/age groups/avatars | ⬜ |
| 10 | Seed data | `seed_travel_personas` (idempotent) — six personas, v1 questionnaire, weights, age groups | ⬜ |
| 11 | Scoring engine | services/scoring.py + full calibration test suite green | ⬜ |
| 12 | Kiosk backend flow | start/profile/question/answer/complete/reset + session services | ⬜ |
| 13 | HTMX UI | idle, profile, question partials, progress, analyzing, result, restart, error | ⬜ |
| 14 | Persona avatars | resolution service + fallback chain + placeholder assets | ⬜ |
| 15 | Analytics | persistence verification, selectors/services, dashboard + charts + CSV exports | ⬜ |
| 16 | Testing | full pytest suite + Playwright E2E green | ⬜ |
| 17 | Code review | senior-review checklist (oversized views, logic in templates, HTMX anti-patterns, privacy leaks) | ⬜ |
| 18 | Kiosk reliability | 100+ assessment soak, reset/timeout/refresh/double-tap/DB-interruption drills | ⬜ |
| 19 | Performance | asset sizing, query/index verification, load timing | ⬜ |
| 20 | Deployment | Dockerfile, compose, nginx, health endpoint, release procedure | ⬜ |
| 21 | Exhibition review | checklist dry-run with operators | ⬜ |
| 22 | Handover | docs final pass, runbook training | ⬜ |

## Phase Gates

- **Gate after 11:** all scoring calibration cases green before any UI work.
- **Gate after 16:** no skipped/disabled tests; E2E happy path green.
- **Gate after 18:** soak test clean before event-day freeze.
- **Freeze after 21:** content changes only via Admin (no deploys on event day).

## Definition of Done (MVP)

Idle screen works · start works · Bangla/English name works · age validation
works · gender selection works · 6 questions work · HTMX transitions work ·
deterministic scoring · all six personas reachable · result shows name, persona,
avatar · avatar fallback works · restart works · timeout works · previous
visitor data removed · analytics persist · traffic/persona/hourly/age/gender
metrics work where enabled · admin can edit questions and weights · dashboard
auth works · Docker deployment works · tests pass · E2E passes · docs complete ·
exhibition checklist present.
