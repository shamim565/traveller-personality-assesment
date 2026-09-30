# Database Design

PostgreSQL. All models in `apps/experience/models.py` (they are the kiosk domain),
read by the `analytics` app. Design rules: enforce integrity in the database
(unique constraints, check constraints), index the analytics paths, minimize PII.

## 1. ER Overview (textual)

```
QuestionnaireVersion 1───N Question 1───N AnswerOption 1───N AnswerPersonaWeight N───1 Persona
                                │ 1
                                │ N
                            AssessmentAnswer N───1 AssessmentSession 1───N AssessmentPersonaScore N───1 Persona
                                │                                 │
                                N                                 N
                             Question                        QuestionnaireVersion (via assessment)

Persona 1───N PersonaAvatar N───1 AgeGroup (optional)
AssessmentSession N───1 AgeGroup (optional)
```

## 2. Models

### QuestionnaireVersion
| Field | Type | Notes |
|---|---|---|
| name | CharField(120) | e.g. "World Tourism Day 2026" |
| version | CharField(20) | e.g. "v1" |
| is_active | BooleanField | only one enforced active by service (admin warning) |
| created_at | DateTimeField(auto_now_add) | |

### Persona
| Field | Type | Notes |
|---|---|---|
| name | CharField(60) unique | "Heritage Hunter" |
| slug | SlugField unique | "heritage_hunter" (stable analytics key) |
| short_description_bn / _en | CharField(160) | result screen one-liner |
| description_bn / _en | TextField | longer copy |
| tagline_bn / _en | CharField(120) | optional |
| keywords_bn / _en | CharField(255) | "ইতিহাস • ঐতিহ্য • স্থাপত্য" |
| sort_order | PositiveSmallIntegerField(default 0) | display/admin ordering only |
| tie_break_order | PositiveSmallIntegerField(default 0) | scoring tie-break priority (scoring-system.md §4); seeded 1–6, 0 = unset (falls back to slug) |
| is_active | BooleanField(default True) | |

### Question
| Field | Type | Notes |
|---|---|---|
| questionnaire_version | FK | related_name="questions" |
| text_bn / text_en | TextField | |
| order | PositiveSmallIntegerField | |
| question_type | CharField choices | v1: only `single_choice` |
| is_active | BooleanField(default True) | |

Constraints: `UniqueConstraint(fields=["questionnaire_version","order"])`.
Index: `(questionnaire_version, is_active, order)`.

### AnswerOption
| Field | Type | Notes |
|---|---|---|
| question | FK | related_name="options" |
| text_bn / text_en | CharField(255) | |
| order | PositiveSmallIntegerField | |
| is_active | BooleanField(default True) | |
| companion_trait | CharField(20) null/blank | only Q5: solo/couple/family/friends/destination_first |

Constraints: `UniqueConstraint(fields=["question","order"])`.

### AnswerPersonaWeight
| Field | Type | Notes |
|---|---|---|
| answer_option | FK | related_name="weights" |
| persona | FK | |
| weight | SmallIntegerField | 0..5, check constraint |

Constraints: `UniqueConstraint(answer_option, persona)`,
`CheckConstraint(weight >= 0 AND weight <= 5)`. Index: `(answer_option)`.

### AgeGroup
| Field | Type | Notes |
|---|---|---|
| name | CharField(40) unique | "Young Adult" |
| min_age / max_age | SmallIntegerField | inclusive |
| order | PositiveSmallIntegerField | |

Check: `min_age <= max_age`. Seed defaults: Teen 10–17, Young Adult 18–29,
Adult 30–49, Mature Adult 50–64, Senior 65–100.

### PersonaAvatar
| Field | Type | Notes |
|---|---|---|
| persona | FK | |
| gender | CharField(20) choices | male/female/prefer_not_to_say; blank = neutral |
| age_group | FK null/blank | blank = persona-level default |
| image | CharField(255) | static path, e.g. `avatars/heritage/male-young_adult.webp` |
| is_default | BooleanField | marks the fallback asset within its scope |

Fallback resolution (service `avatars.py`), in order: exact persona+gender+age →
persona+gender `is_default` → persona-neutral `is_default` (blank gender) →
global default asset constant `AVATAR_GLOBAL_DEFAULT`.

### AssessmentSession
| Field | Type | Notes |
|---|---|---|
| session_uuid | UUIDField unique, default=uuid4 | stable anonymous id |
| questionnaire_version | FK PROTECT | preserves analytics integrity |
| age_group | FK SET_NULL null | exact age **not** stored (privacy decision, privacy.md §4) |
| gender | CharField(20) choices null | |
| primary_persona | FK SET_NULL null | |
| secondary_persona | FK SET_NULL null | |
| companion_trait | CharField(20) null | from Q5 |
| started_at | DateTimeField | written at start |
| completed_at | DateTimeField null | |
| duration_seconds | PositiveIntegerField null | |
| status | CharField(20) choices | started / completed / abandoned / timed_out |
| kiosk_identifier | CharField(20), default from settings | "KIOSK-01" |
| created_at | DateTimeField(auto_now_add) | |

Indexes: `status`, `started_at`, `completed_at`, `primary_persona`,
`kiosk_identifier`, `age_group`, `gender`.

### AssessmentAnswer
| Field | Type |
|---|---|
| assessment | FK related_name="answers" |
| question | FK PROTECT |
| answer_option | FK PROTECT |

Constraint: `UniqueConstraint(assessment, question)` — one answer per question,
guarantees duplicate-tap protection at the DB level.

### AssessmentPersonaScore
| Field | Type |
|---|---|
| assessment | FK related_name="persona_scores" |
| persona | FK |
| raw_score | PositiveSmallIntegerField |
| normalized_score | PositiveSmallIntegerField |
| rank | PositiveSmallIntegerField | 1 = primary after tie resolution |

Constraint: `UniqueConstraint(assessment, persona)`.

### KioskEvent (deferred — NOT in MVP)
Documented for future detailed funnel/abandonment analytics: `id, session_uuid,
event_type, timestamp, kiosk_identifier, metadata(JSONB)`. Only added if
stakeholders need per-step event data; MVP satisfies all §50 metrics without it.

## 3. Questionnaire Versioning Integrity

- Assessments FK the version they used → old analytics remain correct when
  questions/weights change.
- Weight/option edits inside an **already-used** version must either create a new
  version or be a conscious, documented recalibration (admin warning when a
  version has assessments).
- Seed command creates version "World Tourism Day 2026" v1 and marks it active.

## 4. Write Pattern

- Start: 1 insert (minimal row, `status=started`).
- Complete: 1 update + N answer inserts + 6 score inserts, **single transaction**.
- Reset/timeout: 1 status update to `abandoned`/`timed_out`.
- No per-question writes, no event table in MVP.

## 5. Privacy Implications

- Visitor name: never a column (session only).
- Exact age: not stored; age group FK only.
- Gender: stored as enumerated slug (needed for avatar + approved analytics).
- Every row is anonymous and joinable only via random UUID.
- Deletion strategy: retention window + purge management command (privacy.md).
