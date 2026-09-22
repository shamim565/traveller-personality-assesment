# Analytics Architecture

Analytics are a **by-product of persisted assessments** — no extra writes during
the visitor flow beyond the single assessment transaction. The `analytics` app is
read-only over the `experience` models and performs database-side aggregation.

## 1. Data Sources

- `AssessmentSession` — traffic, completion, duration, demographics, persona outcome
- `AssessmentAnswer` — per-question answer distributions
- `AssessmentPersonaScore` — score spreads (future calibration insight)

## 2. Metrics & Query Definitions (selectors.py)

| Metric | Definition |
|---|---|
| `get_total_started()` | `AssessmentSession.objects.count()` |
| `get_total_completed()` | count(status="completed") |
| `get_completion_rate()` | completed / started |
| `get_average_completion_time()` | `Avg(duration_seconds)` over completed |
| `get_persona_distribution()` | values("primary_persona__slug").annotate(count) over completed |
| `get_hourly_traffic(date=None)` | `TruncHour("started_at")` counts (optionally per-day) |
| `get_age_distribution()` | values("age_group__name").annotate(count) over completed |
| `get_gender_distribution()` | values("gender").annotate(count) over completed |
| `get_answer_distribution(question)` | per option counts over that question's answers |
| `get_companion_distribution()` | Q5 trait counts (solo/couple/family/friends/destination_first) |
| `get_traffic_by_kiosk()` | values("kiosk_identifier").annotate(count) |
| `get_abandonment_counts()` | counts by status (started/abandoned/timed_out) |

All aggregations use Django ORM `values().annotate()` + `Count/Avg/TruncHour`.
Nothing pulls full rows into Python.

## 3. Dashboard (`/dashboard/`)

Staff-login protected (`login_required` + `staff_member_required`). Layout:

1. **Summary cards:** Started, Completed, Completion Rate, Avg Duration
2. **Persona distribution** — donut (Chart.js)
3. **Hourly traffic** — bar chart, default today, date selector
4. **Age-group distribution** — bar chart
5. **Gender distribution** — donut (only if gender collection enabled)
6. **Answer insights** — most popular option per question, Q5 companion split
7. **Kiosk table** — traffic per kiosk identifier

Charts are few and meaningful; no decorative BI. Templates use the same design
language but are explicitly *not* part of the kiosk experience.

## 4. CSV Export (staff-only)

| Report | Contents |
|---|---|
| `assessment_summary` | uuid, kiosk, version, status, started_at, completed_at, duration, age_group, gender, primary/secondary persona, companion trait |
| `persona_distribution` | persona, count, percentage |
| `answer_responses` | question order, answer order, answer text (bn), count, percentage |
| `hourly_traffic` | date, hour, started, completed |

Generated server-side (`csv` module), streamed with `Content-Disposition`.
Excludes names/exact ages; protected by the same staff auth as the dashboard.

## 5. Kiosk Identifiers

- Configured per deployment via `KIOSK_IDENTIFIER` env (default `KIOSK-01`).
- Stored on every assessment row; enables per-device comparison and
  troubleshooting (one kiosk misbehaving shows up as a traffic anomaly).

## 6. Query Performance

- Indexes on the grouped fields: `status`, `started_at`, `completed_at`,
  `primary_persona`, `age_group`, `gender`, `kiosk_identifier`
  (see database-design.md).
- Dashboard queries run in O(#groups); at exhibition scale (thousands of rows
  per day) this is far below any measurable latency target.
- No caching layer in MVP; add only if measurements justify it.

## 7. Event Tracking (deferred)

`KioskEvent` (schema in database-design.md) is a documented future extension for
step-level funnels (experience_started, profile_completed, question_reached,
assessment_completed, result_viewed, restart_clicked, timeout). MVP metrics in
§2 do not require it, so it stays out to avoid write noise.
