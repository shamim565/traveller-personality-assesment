# Skill — Persona Scoring

## Responsibility

The deterministic scoring matrix, normalization, persona differentiation, tie
handling, calibration, and its test coverage.

## Rules

1. Deterministic always: same answers → same result. No randomness, no LLM.
2. Weights live in the DB (`AnswerPersonaWeight`, 0–5); the code contains no
   hardcoded scoring values — only the tie-break priority constant.
3. Distinctions to protect:
   - Adventure (activity/thrill) vs Nature (scenery/peace) — different
     primaries on shared answers.
   - Heritage (past/monuments) vs Culture (living people/food/festivals).
4. Question 5 contributes **zero** persona weight in v1; its answer is recorded
   as a companion trait only. Any change requires a new questionnaire version.
5. Ranking uses raw scores; normalized scores (raw/max_possible×100) are display
   and analytics only — never labeled as probabilities.
6. Tie chain, in order: raw score → strong-answer count (weight ≥ 4) →
   core-question (Q1–Q4) confidence → fixed priority
   `Heritage > Nature > Culture > Adventure > Beach > Urban`.
7. Primary + secondary computed; secondary null when its raw score is 0.

## Checklist (persona QA)

- [ ] Every persona reachable as primary via a plausible answer pattern
- [ ] No persona has an unfair scoring advantage (maxima reviewed in matrix doc)
- [ ] Nature/Adventure and Heritage/Culture stay distinct in mixed cases
- [ ] Q5 neutrality proven by test (changing Q5 never flips the persona)
- [ ] All calibration cases in docs/scoring-system.md §6 covered by tests
