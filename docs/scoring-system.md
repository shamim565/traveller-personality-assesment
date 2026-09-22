# Scoring System — Deterministic Persona Detection

The core classifier is a **deterministic weighted matrix** stored in the database
(`AnswerPersonaWeight`). No LLM, no remote API, no randomness. The system is branded
"AI Travel Personality Detector", but classification itself is explicit, offline,
reproducible business logic. Optional AI features (descriptions, itineraries) are
future, out-of-MVP add-ons.

## 1. Scoring Domain

Scoring questions: **Q1, Q2, Q3, Q4, Q6** (5 of 6 questions).
Question 5 is excluded from persona scoring entirely (see §6).

Weights are integers `0..5`. `0` = no association. `4` = strong primary association.
`1–3` = secondary association. Weights live in the DB so admins can recalibrate
without code changes. The seeded matrix below is the v1 calibration.

## 2. Complete Scoring Matrix (v1)

### Q1 — ধরুন, এখনই ছুটিতে যাচ্ছেন—কেমন ট্রিপ চাইবেন?

| # | Answer | Heritage | Beach | Adventure | Nature | Urban | Culture | Rationale |
|---|---|---|---|---|---|---|---|---|
| 1 | সমুদ্রের ধারে একদম রিল্যাক্স | 0 | **4** | 0 | 0 | 0 | 0 | Pure beach |
| 2 | পুরোনো জায়গা, ইতিহাস আর ঐতিহ্য ঘুরে দেখা | **4** | 0 | 0 | 0 | 0 | 1 | Heritage primary; culture secondary |
| 3 | পাহাড়, ট্রেকিং আর একটু অ্যাডভেঞ্চার | 0 | 0 | **3** | **3** | 0 | 0 | Dual mountain/trekking answer; "একটু অ্যাডভেঞ্চার" is mild → balanced A/N |
| 4 | স্থানীয় খাবার, মানুষ আর সংস্কৃতি এক্সপ্লোর করা | 1 | 0 | 0 | 0 | 0 | **4** | Culture primary |
| 5 | জমজমাট একটা শহর ঘুরে বেড়ানো | 0 | 0 | 0 | 0 | **4** | 0 | Pure urban |

### Q2 — কোন ধরনের জায়গা দেখলেই আপনার ব্যাগ গুছাতে ইচ্ছা করে?

| # | Answer | Heritage | Beach | Adventure | Nature | Urban | Culture | Rationale |
|---|---|---|---|---|---|---|---|---|
| 1 | সমুদ্র আর দ্বীপ | 0 | **4** | 0 | 0 | 0 | 0 | Pure beach |
| 2 | পাহাড় আর বন | 0 | 0 | 2 | **4** | 0 | 0 | Scenery-first: Nature primary, Adventure secondary |
| 3 | পুরোনো শহর বা ঐতিহাসিক জায়গা | **4** | 0 | 0 | 0 | 0 | 1 | Heritage primary |
| 4 | গ্রাম আর স্থানীয় জীবন | 0 | 0 | 0 | 1 | 0 | **4** | Culture primary; village = mild nature |
| 5 | আধুনিক শহর | 0 | 0 | 0 | 0 | **4** | 0 | Pure urban |

### Q3 — ট্রিপে গিয়ে কোন কাজটা সবচেয়ে বেশি করতে চান?

| # | Answer | Heritage | Beach | Adventure | Nature | Urban | Culture | Rationale |
|---|---|---|---|---|---|---|---|---|
| 1 | আরাম করব, ছবি তুলব, ভিউ উপভোগ করব | 0 | **3** | 0 | 2 | 0 | 0 | Relax+scenery: Beach primary, Nature secondary (photo/view) |
| 2 | পুরোনো স্থাপনা আর ঐতিহাসিক জায়গা ঘুরব | **4** | 0 | 0 | 0 | 0 | 1 | Heritage primary |
| 3 | ট্রেকিং, ক্যাম্পিং বা অ্যাডভেঞ্চার কিছু করব | 0 | 0 | **4** | 2 | 0 | 0 | Spec example: Adventure +4, Nature +2 |
| 4 | লোকাল খাবার খাব আর মানুষের সঙ্গে মিশব | 1 | 0 | 0 | 0 | 0 | **4** | Culture primary; heritage secondary |
| 5 | শপিং, ক্যাফে আর শহর ঘুরে দেখব | 0 | 0 | 0 | 0 | **4** | 1 | Urban primary; café/food = light culture |

### Q4 — কোন ধরনের ট্রিপ আপনার কাছে সবচেয়ে মজার?

| # | Answer | Heritage | Beach | Adventure | Nature | Urban | Culture | Rationale |
|---|---|---|---|---|---|---|---|---|
| 1 | একদম শান্ত আর আরামদায়ক | 0 | **3** | 0 | 1 | 0 | 0 | Calm: Beach primary, light Nature |
| 2 | ইতিহাস আর গল্পে ভরা | **4** | 0 | 0 | 0 | 0 | 1 | Heritage primary |
| 3 | একটু ঝুঁকি, একটু রোমাঞ্চ | 0 | 0 | **4** | 1 | 0 | 0 | Thrill = Adventure primary |
| 4 | লোকাল কালচার আর নতুন অভিজ্ঞতায় ভরা | 1 | 0 | 0 | 0 | 0 | **4** | Culture primary |
| 5 | ফান, এন্টারটেইনমেন্ট আর সিটি লাইফ | 0 | 0 | 0 | 0 | **4** | 0 | Pure urban |

### Q6 — ট্রিপে একটা পুরো দিন নিজের মতো কাটাতে পারলে কী করবেন?

| # | Answer | Heritage | Beach | Adventure | Nature | Urban | Culture | Rationale |
|---|---|---|---|---|---|---|---|---|
| 1 | সমুদ্র বা নদীর ধারে বসে সূর্যাস্ত দেখব | 0 | **4** | 0 | 1 | 0 | 0 | Water+sunset: Beach primary, light Nature |
| 2 | কোনো পুরোনো প্রাসাদ, মন্দির বা ঐতিহাসিক জায়গা ঘুরব | **4** | 0 | 0 | 0 | 0 | 1 | Heritage primary |
| 3 | ট্রেকিং, কায়াকিং বা সাইক্লিং করব | 0 | 0 | **4** | 2 | 0 | 0 | Active: Adventure primary, Nature secondary |
| 4 | লোকাল বাজার, উৎসব বা গ্রাম ঘুরে দেখব | 1 | 0 | 0 | 1 | 0 | **4** | Spec example: Culture +4, Heritage +1, Nature +1 |
| 5 | শহর, রেস্টুরেন্ট আর মজার জায়গাগুলো এক্সপ্লোর করব | 0 | 0 | 0 | 0 | **4** | 1 | Urban primary; restaurant culture secondary |

### Max possible raw score per persona (v1)

| Persona | Max | Where |
|---|---|---|
| Heritage Hunter | 20 | Q1b4 + Q2c4 + Q3b4 + Q4b4 + Q6b4 |
| Beach Lover | 18 | Q1a4 + Q2a4 + Q3a3 + Q4a3 + Q6a4 |
| Adventure Seeker | 17 | Q1c3 + Q2b2 + Q3c4 + Q4c4 + Q6c4 |
| Nature Explorer | 12 | Q1c3 + Q2b4 + Q3a2 + Q4a1 + Q6c2 |
| Urban Explorer | 20 | Q1e4 + Q2e4 + Q3e4 + Q4e4 + Q6e4 |
| Culture Connector | 20 | Q1d4 + Q2d4 + Q3d4 + Q4d4 + Q6d4 |

Maxima differ by design: Nature Explorer is a narrower archetype with fewer
first-class answers; normalization (§3) makes percentages comparable for display,
while **ranking uses raw scores** (documented in §4).

## 3. Raw Score & Normalization

**Raw score** for persona P = sum of weights of the visitor's chosen answers where
the answer has a weight for P.

**Normalized score** = `raw / max_possible(P) × 100`, rounded to integer.
`max_possible(P)` = sum of P's maximum weight across each scoring question
(Q1–Q4, Q6). Normalized scores are **relative preference scores for display and
analytics only** — they are not probabilities and must not be labeled as such.
They are also not used for ranking (raw scores are).

## 4. Primary Persona & Deterministic Tie Handling

1. **Raw score** — highest wins.
2. **Strong-answer count** — among tied personas, the one with more "strong"
   associations wins. A strong association = an answer with weight ≥ 4 for that
   persona.
3. **Core-question confidence** — among still-tied personas, higher sum of weights
   from core questions Q1–Q4 wins.
4. **Fixed priority fallback** — predefined, hardcoded persona priority constant:
   `Heritage > Nature > Culture > Adventure > Beach > Urban`. Never random.

All steps are deterministic. The full chain is exercised by tests (testing.md §2.4).

**Secondary persona** = rank 2 after tie resolution; stored as null if its raw
score is 0.

## 5. Question 5 Handling (Companion)

Question 5 answers map to a companion trait and carry **zero persona weights** in v1:

| # | Answer | Trait |
|---|---|---|
| 1 | একাই | `solo` |
| 2 | পার্টনারের সঙ্গে | `couple` |
| 3 | পরিবারের সঙ্গে | `family` |
| 4 | বন্ধুদের সঙ্গে | `friends` |
| 5 | আসলে জায়গাটা ভালো হলেই হলো! | `destination_first` |

Effect on classification: **none**. Uses: analytics insight, future
recommendations, future light modifiers (the model supports nonzero weights if
stakeholders later request them; any change requires a new questionnaire version).

## 6. Calibration Test Cases (expected results)

| Case | Answers (Q1–Q6) | Expected primary |
|---|---|---|
| Pure Beach | 1a, 2a, 3a, 4a, 5(any), 6a | Beach Lover (B18, N4) |
| Pure Heritage | 1b, 2c, 3b, 4b, 5(any), 6b | Heritage Hunter (H20, C5) |
| Pure Adventure | 1c, 2b, 3c, 4c, 5(any), 6c | Adventure Seeker (A17, N12) |
| Pure Nature (scenic, no thrill) | 1c, 2b, 3a, 4a, 5(any), 6a | Nature Explorer (N11, B10, A5) |
| Pure Urban | 1e, 2e, 3e, 4e, 5(any), 6e | Urban Explorer (U20, C2) |
| Pure Culture | 1d, 2d, 3d, 4d, 5(any), 6d | Culture Connector (C20, H4, N2) |
| Heritage + Culture | 1b, 2d, 3b, 4d, 5(any), 6d | Culture Connector (C14, H10) |
| Nature + Adventure (thrill) | 1c, 2b, 3c, 4c, 5(any), 6c | Adventure Seeker (A17, N12) |
| Beach + Nature | 1a, 2b, 3a, 4a, 5(any), 6a | Beach Lover (B14, N8) |
| Urban + Culture | 1e, 2d, 3e, 4d, 5(any), 6e | Urban Explorer (U12, C10) |
| Tie exercise (contrived) | see testing.md | deterministic per §4 chain |

## 7. Scoring Service Contract

```python
# apps/experience/services/scoring.py
result = calculate_travel_persona(answers: list[AnswerOption]) -> ScoringResult

ScoringResult:
    raw_scores: dict[persona_slug, int]
    normalized_scores: dict[persona_slug, int]   # display only
    ranked_personas: list[persona_slug]          # deterministic order
    primary: persona_slug
    secondary: persona_slug | None
    tie_metadata: dict                            # which tie-break step decided
    companion_trait: str | None                   # from Q5
    scoring_question_count: int
```

Pure function: no HTTP, no templates, no session access. Raises
`ScoringValidationError` on malformed input (missing answers, answers from
inactive questions, duplicate question answers, inactive persona weights).
