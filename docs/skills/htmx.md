# Skill — HTMX

## Responsibility

Server-driven partial updates, form submissions, quiz transitions, and
progressive enhancement for the kiosk experience.

## Rules

1. Server is the source of truth — avoid SPA-like client state.
2. One controlled container (`#experience`); endpoints return small, focused
   partials.
3. All state changes are POSTs with `hx-target="#experience"` and
   `hx-swap="innerHTML"` by default.
4. `hx-disabled-elt="this"` on every tap target (double-tap guard); server logic
   must also be idempotent — UI disabling alone is not enough.
5. Use `request.htmx` to choose partial vs full-page responses (graceful
   degradation when JS fails).
6. The only timer-driven request is the analyzing→complete handoff
   (`hx-trigger="load delay:1600ms"`). No polling elsewhere.
7. Handle failures visibly: validation errors render into the partial with
   friendly copy; unexpected errors render `partials/error.html`.
8. Inject CSRF once in `base.html` via HTMX headers — never per-form hacks.
9. No HTMX event spaghetti; avoid chained `hx-on` handlers.

## Checklist (review)

- [ ] Every swap partial is renderable standalone for tests
- [ ] No endpoint both mutates state and returns unrelated full-page chrome
- [ ] Failure path (error partial) reachable and tested
