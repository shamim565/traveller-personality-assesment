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
| 7 | Project bootstrap | Django project, settings package, Tailwind/HTMX/Alpine wiring, pytest, Docker skeleton | ✅ Done |
| 8 | Models | all database-design.md models + migrations + constraints/indexes | ✅ Done |
| 9 | Admin | content management for versions/questions/answers/weights/personas/age groups/avatars | ✅ Done |
| 10 | Seed data | `seed_travel_personas` (idempotent) | ✅ Done |
| 11 | Scoring engine | services/scoring.py + calibration suite green | ✅ Done |
| 12 | Kiosk backend flow | start/profile/question/answer/complete/reset + session services | ✅ Done |
| 13 | HTMX UI | idle, profile, question partials, progress, analyzing, result, restart, error | ✅ Done |
| 14 | Persona avatars | resolution service + fallback chain + broken-image recovery | ✅ Done |
| 15 | Analytics | persistence, selectors/services, dashboard + charts + CSV exports | ✅ Done |
| 16 | Testing | 126 unit/integration + 9 E2E + soak + performance suites green | ✅ Done |
| 17 | Code review | senior-review fixes (N+1 prefetch, constraints, query budgets) | ✅ Done |
| 18 | Kiosk reliability | 100-assessment soak; countdown-leak bug fixed | ✅ Done |
| 19 | Performance | targets verified; indexes, gzip, manifest storage | ✅ Done |
| 20 | Deployment | Docker production stack validated end-to-end (Postgres path) | ✅ Done |
| 21 | Exhibition review | checklist dry-run + docs final pass | ✅ Done |
| 22 | Handover | docs/handover.md + full final validation green | ✅ Done |

## Phase Gates (all green)

- **Gate after 11:** scoring calibration green before UI — ✅
- **Gate after 16:** no skipped tests; E2E happy path green — ✅
- **Gate after 18:** soak clean before freeze — ✅
- **Freeze after 21:** content changes only via Admin (no deploys on event day)

## Definition of Done (MVP) — all met

Idle screen · start · Bangla/English name · age validation · gender selection ·
6 questions · HTMX transitions · deterministic scoring · all six personas
reachable · result with name/persona/avatar · avatar fallback · restart ·
timeout · previous visitor data removed · analytics persist · traffic/persona/
hourly/age/gender metrics · admin question/weight editing · dashboard auth ·
Docker deployment · tests · E2E · docs · exhibition checklist.
