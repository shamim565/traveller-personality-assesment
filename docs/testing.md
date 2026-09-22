# Testing Strategy

Toolchain: **pytest + pytest-django + Django test client** for backend;
**Playwright** for kiosk E2E. Tests run against PostgreSQL in CI (matching
production behavior for aggregates); SQLite acceptable for pure-unit runs.

## 1. Test Layers

| Layer | Tool | What it covers |
|---|---|---|
| Unit — scoring | pytest | the scoring engine in isolation |
| Unit — services | pytest + Django | session orchestration, avatar fallback, idempotency |
| Unit — models/forms | pytest | constraints, validation, choices |
| Integration — HTTP/HTMX | Django test client with `HTTP_HX-Request` headers | endpoint behaviors, partial responses |
| Integration — analytics | pytest | selectors/aggregations |
| E2E — kiosk | Playwright | full visitor journeys + reliability cases |

Shared fixture: the seeded questionnaire (via `seed_travel_personas` command)
loaded per test session.

## 2. Scoring Tests (apps/experience/tests/test_scoring.py)

2.1 **Pure persona cases** — all six personas reachable with expected raw scores
(see scoring-system.md §6).
2.2 **Mixed cases** — Heritage+Culture, Nature+Adventure, Beach+Nature,
Urban+Culture produce the documented primary.
2.3 **Q5 neutrality** — changing Q5 answer must never change the persona result.
2.4 **Ties** — contrived equal-score answer sets resolve deterministically at
each tie-break step (raw → strong count → core confidence → fixed priority);
same input always yields same output (repeat runs).
2.5 **Malformed input** — missing answers, duplicate question ids, answers from
inactive questions, unknown answer ids → `ScoringValidationError`.
2.6 **Secondary persona** — runner-up recorded; null when score 0.
2.7 **Normalization** — normalized = raw/max_possible×100, bounded 0–100.

## 3. Session & Flow Tests (test_client)

- `start` creates session state + a `started` AssessmentSession row.
- Profile stored in session; invalid profile (age out of range, missing gender)
  returns form errors, no state persisted.
- Answers stored; re-answering a question replaces (no duplicates).
- `complete` persists exactly one assessment with answers + 6 score rows;
  double-complete writes once (idempotent).
- `reset` clears all `experience.*` keys and marks unfinished `abandoned`.
- Name present in session during flow, absent after complete/reset.
- Refresh mid-quiz re-enters the correct question.
- Stale/invalid session state returns friendly error partial.

## 4. HTMX Integration Tests

- Profile POST with `HX-Request` header returns the Q1 partial (assert template
  + context), not a full page.
- Answer POST returns next question partial; after Q6 returns analyzing partial.
- Non-HTMX POST falls back to full page (graceful degradation).
- Invalid submission returns error-marked partial with HTTP 200 (kiosk-friendly).
- CSRF: POSTs without token rejected.

## 5. Analytics Tests (apps/analytics/tests/)

Seed a known set of assessments → assert:
`get_total_started`, `get_total_completed`, `get_completion_rate`,
`get_persona_distribution`, `get_hourly_traffic` (including empty hours),
`get_age_distribution`, `get_gender_distribution`,
`get_average_completion_time`, `get_answer_distribution`, abandonment counts.
Dashboard view requires staff auth (anonymous → redirect).

## 6. E2E (Playwright, kiosk.ts-style scenarios)

6.1 **Happy path:** idle → start → profile → 6 answers → analyzing → expected
persona → Start Again → idle (verify previous data gone).
6.2 **Abandon at Q3** → start a new session → old assessment marked abandoned,
new session unaffected.
6.3 **Inactivity timeout** (shortened timer via settings override) → "Still
there?" appears → grace expires → idle.
6.4 **Browser refresh** mid-quiz → same question re-renders.
6.5 **Rapid double-tap** on answer card → single answer recorded, next question
shown.
6.6 **Missing avatar** → global fallback asset rendered (no broken image).
6.7 **Slow server** (Playwright route delay) → indicator shown, flow completes.
6.8 **Completed session submitted twice** → one assessment row.
6.9 **Invalid session** (cleared cookies mid-flow) → friendly recovery screen.

## 7. Exhibition Reliability Tests (Phase 18)

- Scripted soak: 100+ consecutive Playwright assessments with no leaked state.
- Repeated reset/timeout cycling; DB interruption simulation (stop/start db
  container mid-flow); app restart mid-flow; browser refresh storm.
- Assert: no duplicate records, no memory leaks beyond tolerance, no broken UI
  states, recovery screens appear and recover.

## 8. CI Expectations

`pytest` must be green before merge; E2E runs on a schedule or pre-release.
Never disable/skip failing tests to make the build green. Coverage goal:
scoring 100%, services/selectors ≥ 90%, views/forms ≥ 80% (indicative, not a gate).
