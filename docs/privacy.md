# Privacy & Data Strategy

Principle: **data minimization**. A tourism exhibition quiz does not need
identifying data to be valuable. Collect the minimum, keep it in the session
wherever possible, persist only what analytics justify.

## 1. Data Inventory

| Field | Where | Stored in DB? | Purpose | Retention |
|---|---|---|---|---|
| Visitor name | Django session only | **No** | Result personalization | Deleted on reset/timeout/complete |
| Age (exact) | session during flow | **No** (age group only) | Avatar group + demographics | Session-scoped |
| Age group | DB (FK) | Yes | Avatar + aggregate analytics | Retention window |
| Gender | session, then DB | Yes (enumerated) | Avatar + approved aggregate analytics | Retention window |
| Answers | session, then DB | Yes (anonymous) | Scoring + answer analytics | Retention window |
| Persona scores/outcome | DB | Yes | Core analytics | Retention window |
| Session UUID | DB | Yes | Anonymous correlation + idempotency | Retention window |
| Timestamps/duration | DB | Yes | Traffic/duration analytics | Retention window |
| Kiosk identifier | DB | Yes | Per-device analytics | Retention window |

## 2. Name Handling

- Name lives **only** in the Django session, from profile submission until the
  experience resets (manual restart, inactivity timeout, or a new visitor
  starting). Nothing persists it to PostgreSQL.
- Result screen may show the name because it is rendered in the same session
  context; nothing persists it.
- If stakeholders later require name retention (e.g., social-wall), it requires:
  explicit consent, a documented business purpose, and a retention policy.
  The model intentionally has no name column.

## 3. Age Handling

- Exact age is validated (default 10–100) and used to resolve an **age group**.
- Only the age group FK is persisted — better privacy at zero analytics cost
  (all §50 age metrics are group-based). If exact-age analytics are ever
  approved, this is a single additive migration with documented justification.

## 4. Gender Handling

- Enumerated values only (`male`, `female`, `prefer_not_to_say`).
- Used for avatar selection and aggregate distribution; never exposed per-record
  outside staff dashboards.

## 5. Sessions

- Django cookie session (default engine acceptable for MVP; swap to DB/cache
  sessions if the venue requires stateless restarts — see §6).
- `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True` in production.
- Session expiry: short (default 30 min) plus explicit reset clearing.
- All session keys namespaced under `experience.` and cleared atomically on
  reset/timeout.

## 6. DB Session Trade-off (documented decision)

Cookie sessions: zero server writes, survives nothing across restarts but the
visitor simply restarts the quiz — acceptable at a kiosk. If operators demand
that an in-progress quiz survive a server restart, enable DB-backed sessions via
a one-line setting change. MVP default: cookie sessions.

## 7. Retention & Deletion

- Recommended event window: keep data **90 days** post-event for reporting,
  then purge.
- Provide a management command `purge_assessments --before YYYY-MM-DD` that
  deletes `AssessmentSession` (+ cascaded answers/scores).
- Document the chosen window in the exhibition runbook; default is conservative.

## 8. Dashboard & Export Access

- `/dashboard/` and all CSV exports require authenticated **staff** accounts.
- Staff accounts: individual logins, no shared "admin/admin" password; created
  via `createsuperuser`/Admin before the event.
- Exports never include names or exact ages.

## 9. Logging

- Application logs must not contain visitor names or raw personal data.
- Error logs include session UUID (anonymous) for correlation.

## 10. Security (kiosk = untrusted client)

- CSRF protection on all state-changing endpoints.
- Server-side validation is authoritative for every input.
- HTTPS in production; secure cookies; `DEBUG=False`; restrictive
  `ALLOWED_HOSTS`; secrets via environment, never committed.
- Scoring inputs verified: question belongs to the active questionnaire version,
  answer belongs to that question, assessment state valid — no trust in hidden
  fields.
- ORM-only queries; auto-escaped templates.
