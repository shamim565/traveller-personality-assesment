# System Architecture

Django full-stack monolith. Server-rendered HTML + HTMX + Tailwind + minimal
Alpine.js. No SPA, no DRF, no microservices, no external AI dependency for core
functionality.

## 1. High-Level Diagram

```
┌───────────────────────────────────────┐
│  Exhibition Touchscreen / Kiosk       │
│  (Chrome kiosk mode, 1920×1080)       │
└──────────────────┬────────────────────┘
                   │ HTTP (LAN)
                   ▼
┌───────────────────────────────────────┐
│ Nginx (static files, proxy, TLS)      │
└──────────────────┬────────────────────┘
                   ▼
┌───────────────────────────────────────┐
│ Gunicorn → Django WSGI                │
│  Templates + Tailwind + HTMX + Alpine │
└──────┬──────────────┬────────────┬────┘
       │              │            │
       ▼              ▼            ▼
  experience       analytics     core
  (quiz flow,     (selectors,   (shared UI,
   scoring,        services,     health, utils)
   sessions,       dashboard)
   models, admin)
       │              │
       └──────┬───────┘
              ▼
         PostgreSQL
              │
   ┌──────────┴──────────┐
   ▼                     ▼
Django Admin        Analytics Dashboard
(staff content)     (staff, /dashboard/)
```

## 2. Application Modules

```
travel_persona/
├── config/                  # settings package (base/development/production), urls, wsgi
├── apps/
│   ├── core/                # shared utilities, health endpoint, shared template tags
│   ├── experience/          # public kiosk domain
│   │   ├── models.py        #   questionnaire + persona + assessment models
│   │   ├── forms.py         #   profile form (thin validation)
│   │   ├── views.py         #   thin HTTP views
│   │   ├── urls.py          #   public routes
│   │   ├── admin.py         #   content management
│   │   ├── services/        #   business logic (no HTTP)
│   │   │   ├── scoring.py   #   deterministic scoring engine
│   │   │   ├── assessment.py#   start/answer/complete/reset orchestration
│   │   │   ├── sessions.py  #   Django-session state read/write + clearing
│   │   │   └── avatars.py   #   avatar resolution + fallback chain
│   │   ├── selectors/
│   │   │   └── questionnaire.py  # active version/question retrieval
│   │   ├── management/commands/seed_travel_personas.py
│   │   └── tests/
│   └── analytics/
│       ├── selectors.py     # ORM aggregations only
│       ├── services.py      # export/CSV + metric assembly
│       ├── views.py         # staff-only dashboard + export views
│       ├── urls.py
│       └── tests/
├── templates/               # base, kiosk/*, partials/*, dashboard/*
├── static/                  # src/css (Tailwind), js (htmx, alpine, kiosk.js),
│                            # branding/, personas/, avatars/, backgrounds/, fonts/
├── docs/
├── manage.py, pyproject.toml, package.json
├── Dockerfile, docker-compose.yml, .env.example
```

Dependency direction: `views → services/selectors → models → PostgreSQL`.
Services never import HTTP objects (`request`, `HttpResponse`, templates).

## 3. Layering Rules

- **Views:** validate request → delegate to service → prepare context → return
  full page (normal) or partial (HTMX). No scoring math, no persistence logic.
- **Services:** transactional business logic (session orchestration, assessment
  persistence, scoring invocation).
- **Selectors:** read-model queries only (active questionnaire, dashboard metrics).
- **Models:** data + constraints; no HTTP, no scoring math.

## 4. Session Strategy (visitor state)

Django cookie session holds only ephemeral visitor state under the `experience.`
key prefix:

```
experience.started_at       # ISO timestamp
experience.name             # session during the flow; copied to the assessment at completion (privacy.md §2)
experience.age              # int
experience.gender           # slug
experience.qv_id            # active questionnaire version id
experience.question_order   # list of active question ids in order
experience.answers          # {question_id: answer_id}
experience.assessment_uuid  # UUID of the open AssessmentSession row
```

Persistence split: nothing personal is written to PostgreSQL until completion;
on completion only analytics-safe fields are written (see database-design.md).
On `start`, a minimal `AssessmentSession` row (uuid, version, started_at, kiosk,
status=`started`) is inserted so completion rate and traffic exist even if the
visitor abandons. That is the only DB write before completion.

## 5. Request Flows

**Start:** POST `/experience/start/` → service creates session state + row →
returns Profile partial.

**Profile:** POST `/experience/profile/` → form validated server-side → session
updated → first Question partial.

**Answer:** POST `/experience/answer/` → service validates (question active and
current, answer belongs to question, no earlier answer overwritten without
intent — re-answers on same question are replaced, unique per question) → next
Question partial, or Analyzing partial after the last question.

**Complete:** POST `/experience/complete/` (auto-fired from Analyzing) → service
validates all answers present → runs scoring → persists assessment +
answers + scores in one transaction (visitor name written to the assessment) →
Result partial.
Idempotent: if the assessment UUID is already `completed`, the persisted result
is returned without a second write.

**Reset:** POST `/experience/reset/` → marks unfinished assessment `abandoned`
(if any) → clears all `experience.*` session keys → Idle partial.

**Result image:** GET `/experience/result/<uuid>/image/` (no session needed) →
looks up the completed assessment by UUID → renders the result card as a PNG
(Pillow, `apps/experience/services/result_image.py`) → serves it with
`Content-Disposition: attachment`. The kiosk result partial embeds a QR code of
this URL (`qr_image`); the visitor's phone scans it and downloads the picture,
including the name the visitor entered (stored on the completed assessment at
completion; docs/privacy.md §2).

See htmx-flow.md for per-request detail.

## 6. HTMX / Alpine / Tailwind Split

| Concern | Owner | Notes |
|---|---|---|
| Server-rendered screens & transitions | Django templates + HTMX | Single controlled container `#experience`; small focused partials |
| Form submission & progress | HTMX | `hx-post`, `hx-target="#experience"`, `hx-disabled-elt` for double-tap guard |
| Inactivity timers, "Still there?" | Alpine.js | Browser-only state; listens to touch events; fires HTMX reset |
| Selected/pressed card states, reveal animation | Alpine.js | Presentation only; source of truth stays server-side |
| All styling, large touch-first design | Tailwind CSS | Utility classes, theme tokens in `tailwind.config` |

Rules: no scoring logic in JS; no SPA-like client state; Alpine never owns the
quiz flow — Django/HTMX do.

## 7. Analytics Architecture

The `analytics` app is read-only over the data written by `experience`:
`AssessmentSession`, `AssessmentAnswer`, `AssessmentPersonaScore`.
`selectors.py` provides ORM aggregation functions (no per-row Python); the
dashboard views call selectors; Chart.js renders a small set of charts; CSV
export is generated server-side, staff-only.

## 8. Admin & Content Management

Django Admin manages questionnaire versions, questions, answers, weights,
personas, age groups, avatars. Inline editing for answers-with-weights, list
filters, ordering, and admin-side validation. No custom CMS in MVP.

## 9. Deployment Topology

Recommended (see deployment.md): **Option B — local exhibition server**:

```
Kiosk(s) ── LAN ──▶ Docker host (nginx + gunicorn/Django + PostgreSQL)
                        │
                        └─ optional, out-of-band: pg_dump backup / rsync
```

Internet optional; core experience never needs it. Option A (cloud) only when
remote management is mandatory; Option C (all-on-kiosk) when exactly one kiosk
exists.

## 10. Failure & Recovery

- **Browser refresh:** state in session → server re-renders current step.
- **Rapid double-tap:** per-question answer replacement + `hx-disabled-elt`.
- **DB interruption:** connection retry via Django defaults; friendly error partial.
- **App restart:** sessions persist (DB-backed sessions optional; cookie default
  acceptable — see privacy.md §6).
- **Network loss:** no external dependency; LAN-only mode works.
- **Error screen:** never a traceback; always offers "Start Again".

## 11. Security Requirements (summary)

CSRF on all POSTs (HTMX header injection), server-side validation authoritative,
HTTPS in production, `SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE`/`HttpOnly`,
`DEBUG=False`, restrictive `ALLOWED_HOSTS`, dashboard requires staff auth,
ORM-only queries, auto-escaping templates, no secrets in repo, no visitor PII in
logs.
