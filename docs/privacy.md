# Privacy & Data Strategy

Principle: **data minimization**. A tourism exhibition quiz does not need
identifying data to be valuable. Collect the minimum, keep it in the session
wherever possible, persist only what analytics justify.

## 1. Data Inventory

| Field | Where | Stored in DB? | Purpose | Retention |
|---|---|---|---|---|
| Visitor name | session, then completed assessment | Yes (completed only) | Result personalization (screen + downloaded picture) | Retention window |
| Age (exact) | session during flow | **No** (age group only) | Avatar group + demographics | Session-scoped |
| Age group | DB (FK) | Yes | Avatar + aggregate analytics | Retention window |
| Gender | session, then DB | Yes (enumerated) | Avatar + approved aggregate analytics | Retention window |
| Answers | session, then DB | Yes (anonymous) | Scoring + answer analytics | Retention window |
| Persona scores/outcome | DB | Yes | Core analytics | Retention window |
| Session UUID | DB | Yes | Anonymous correlation + idempotency | Retention window |
| Timestamps/duration | DB | Yes | Traffic/duration analytics | Retention window |
| Kiosk identifier | DB | Yes | Per-device analytics | Retention window |

## 2. Name Handling

- Name lives in the Django session during the flow.
- On completion it is copied to the assessment row (`AssessmentSession.visitor_name`)
  for one purpose: rendering the visitor's own result, including the picture the
  phone downloads from the result QR. Starting a new survey never touches
  previous rows, so each visitor's download carries exactly the name their own
  result screen showed.
- Abandoned or timed-out sessions are never given a name (the field is written
  only at completion).
- The name is **not** written to application logs, not included in analytics
  aggregates, and not part of CSV exports. Django admin exposes it read-only to
  staff on the session detail page.
- It is retained with the assessment for the documented retention window; deleting
  assessment data deletes it.
- Any additional use of the name (e.g., social-wall) still requires explicit
  consent, a documented business purpose, and a retention policy.

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
