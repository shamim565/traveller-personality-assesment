# Skill — Django Full-Stack

## Responsibility

Django models, forms, views, templates, sessions, admin, ORM, middleware,
security, and production configuration for this project.

## Rules

1. **Thin views**: validate request → call service → prepare context → return
   response. No scoring math, no multi-step persistence logic in `views.py`.
2. **Services** own business logic; **selectors** own complex read queries.
3. Models carry data + constraints only; no unrelated logic bolted onto models.
4. Use Django Forms for profile input; backend validation is authoritative
   (never trust browser validation).
5. Session access is centralized in `services/sessions.py` — no scattered
   `request.session[...]` writes across views.
6. Prefer `update_or_create`/transactions for idempotent writes; wrap
   multi-row persistence in `transaction.atomic()`.
7. Admin: use list display, filters, ordering, inlines, and `clean()` validation
   instead of building a custom CMS.
8. Respect Django's security defaults (CSRF, escaping, ORM); never `raw()` SQL
   unless measured and documented.
9. Never log request bodies or personal data.

## Checklist (code review)

- [ ] View < ~40 lines; delegates to service
- [ ] Any `.values()`/`annotate()` aggregation lives in a selector
- [ ] Form + model validation agree on business rules
- [ ] `select_related`/`prefetch_related` used on hot paths
