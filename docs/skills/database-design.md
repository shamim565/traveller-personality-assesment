# Skill — Database Design

## Responsibility

PostgreSQL models, constraints, indexes, and migration discipline for the
kiosk domain.

## Rules

1. Enforce integrity in the DB, not just the app: unique constraints
   (`AssessmentSession.session_uuid`, `(assessment, question)`,
   `(question, order)`, `(answer_option, persona)`), check constraints
   (`weight 0–5`, `min_age <= max_age`).
2. Index what analytics group by: `status`, `started_at`, `completed_at`,
   `primary_persona`, `age_group`, `gender`, `kiosk_identifier`.
3. Keep PII out of the schema by design: no name column, age stored as group FK.
4. Questionnaire versioning: assessments FK the version; never mutate a version
   with historical assessments without a documented recalibration decision.
5. Writes are minimal: one insert at start, one transactional update-bundle at
   completion, one status update on abandon. No per-answer writes.
6. Migrations are reviewed like code; no data-mutating migrations that can't be
   re-run safely; destructive changes go through explicit management commands.
7. Nullable fields mean something documented (e.g., `secondary_persona` null =
   score 0), not "we didn't know".

## Checklist (review)

- [ ] New FK has `on_delete` policy chosen deliberately
- [ ] Composite unique constraints exist where duplicates would corrupt analytics
- [ ] Grouped query fields are indexed
- [ ] No sensitive data added without a privacy.md update
