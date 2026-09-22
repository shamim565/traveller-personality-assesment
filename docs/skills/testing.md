# Skill — QA / Testing

## Responsibility

Scoring tests, model/form tests, HTMX integration tests, analytics tests, E2E
kiosk flows, and edge-case coverage.

## Rules

1. Scoring engine gets 100% calibration coverage before any UI work (phase
   gate 11).
2. Test through the documented contracts (scoring-system.md §7, analytics.md §2);
   tests assert behavior, not implementation details.
3. HTMX tests use the Django test client with `HTTP_HX-Request` and assert
   partial templates + context, not full pages.
4. Session lifecycle tests must cover: start, profile, answers, replace-answer,
   complete-idempotency, reset-clears-everything, name-never-persisted.
5. E2E (Playwright) covers the kiosk journeys incl. abandon, timeout, refresh,
   double-tap, missing avatar, invalid session, double completion.
6. Reliability suite (soak, DB interruption, restart) runs before event freeze.
7. Never skip/disable failing tests to green the build. Fix the code.
8. Fixtures: the real seed command, not hand-rolled parallel data, so tests
   drift-detection covers seed changes.

## Checklist (review)

- [ ] Every bug fixed gets a regression test
- [ ] Determinism tests run scoring multiple times and compare outputs
- [ ] Analytics tests use a known dataset, not random rows
