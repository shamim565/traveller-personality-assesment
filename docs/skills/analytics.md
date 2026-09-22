# Skill — Analytics

## Responsibility

Data model for insights, aggregation queries, dashboard metrics, CSV exports,
and kiosk identifiers.

## Rules

1. Store only data with a named business use; MVP persists assessments alone —
   no event table (documented as deferred).
2. Prefer database aggregation (`values().annotate()`, `Count`, `Avg`,
   `TruncHour`) — never pull rows into Python for simple counts.
3. All metrics live as named selector functions with tests
   (`get_total_started`, `get_persona_distribution`, `get_hourly_traffic`, …).
4. Dashboard is staff-only, visually simple, charts only where they aid
   understanding: persona donut, hourly bar, age-group bar, gender donut
   (if approved), summary cards.
5. CSV exports: server-generated, authenticated, no names/exact ages.
6. Every assessment carries `kiosk_identifier` from settings/env for per-device
   comparison.
7. Percentages are shares of completed assessments (or of answers for
   answer-level stats) — label them, don't imply scientific precision.

## Checklist (review)

- [ ] Each dashboard metric maps to a tested selector
- [ ] No N+1 or full-table pulls into Python
- [ ] Hourly buckets include empty hours where the chart needs continuity
- [ ] Exports and views share the same auth requirement
