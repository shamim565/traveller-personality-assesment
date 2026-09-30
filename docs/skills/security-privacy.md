# Skill — Security & Privacy

## Responsibility

Public-kiosk attack surface, sessions, authentication, input validation, data
minimization, retention, and dashboard protection.

## Rules

1. Treat kiosk browsers as untrusted clients: CSRF on all POSTs, server-side
   validation authoritative, no trust in hidden fields.
2. Scoring inputs verified against the DB: question belongs to the active
   questionnaire version, answer belongs to the question, session state valid.
3. Production: `DEBUG=False`, restrictive `ALLOWED_HOSTS`, HTTPS, secure +
   HttpOnly session/CSRF cookies, secrets via environment only.
4. Dashboard/exports: `staff_member_required`; individual staff accounts, no
   shared credentials.
5. Data minimization is the default: the name is kept in session during the flow
   and written to the completed assessment only (for its result/download); exact
   age not stored; enumerated gender; anonymous UUIDs.
6. Logs contain no visitor names or personal data; errors include anonymous
   session UUID for correlation.
7. Retention documented (default 90 days) with a purge management command.
8. ORM-only queries; templates auto-escape; uploaded files (if any later) served
   safely — never from `MEDIA_ROOT` directly on the public path.
9. Idempotency is a security property too: duplicate-tap and double-completion
   must be impossible by DB constraint + service guard.

## Checklist (review)

- [ ] No raw user input in SQL or templates without escaping
- [ ] Session clearing verified on every reset/timeout path (tested)
- [ ] No secrets in repo, docker images, or logs
- [ ] Every new collected field updates privacy.md
