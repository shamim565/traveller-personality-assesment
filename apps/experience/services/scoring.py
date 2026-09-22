"""Deterministic persona scoring engine.

The complete weight matrix, normalization rules, tie handling and
calibration cases are documented in docs/scoring-system.md — this module
is their executable implementation.

Pure business logic: no HTTP, no templates, no session access.
The engine performs small, indexed reads (personas, weights, active
questions) so the caller can pass plain AnswerOption instances.
"""

from dataclasses import dataclass

from apps.experience.models import (
    AnswerOption,
    AnswerPersonaWeight,
    Persona,
    Question,
)

TIE_BREAK_PRIORITY = [
    "heritage_hunter",
    "nature_explorer",
    "culture_connector",
    "adventure_seeker",
    "beach_lover",
    "urban_explorer",
]

CORE_QUESTION_ORDERS = frozenset({1, 2, 3, 4})
STRONG_WEIGHT_THRESHOLD = 4


class ScoringValidationError(Exception):
    """Malformed assessment input: missing, duplicate or inactive data."""


@dataclass(frozen=True)
class ScoringResult:
    raw_scores: dict
    normalized_scores: dict
    ranked_personas: list
    primary: str
    secondary: str | None
    tie_metadata: dict
    companion_trait: str | None
    scoring_question_count: int


def calculate_travel_persona(answers):
    """Score a completed assessment. Raises ScoringValidationError on bad input.

    answers: list[AnswerOption] — every active question of one questionnaire
             version answered exactly once (Question 5 included; it carries
             no weights and therefore cannot influence classification).
    """
    if not answers:
        raise ScoringValidationError("assessment has no answers")
    if not all(isinstance(answer, AnswerOption) for answer in answers):
        raise ScoringValidationError("answers must be AnswerOption instances")

    question_ids = [answer.question_id for answer in answers]
    if len(set(question_ids)) != len(question_ids):
        raise ScoringValidationError("duplicate answers for the same question")

    version_ids = {answer.question.questionnaire_version_id for answer in answers}
    if len(version_ids) != 1:
        raise ScoringValidationError("answers span multiple questionnaire versions")
    version = answers[0].question.questionnaire_version

    for answer in answers:
        if not answer.question.is_active:
            raise ScoringValidationError(
                f"answer for inactive question #{answer.question.order}"
            )
        if not answer.is_active:
            raise ScoringValidationError(
                f"inactive answer option selected on question #{answer.question.order}"
            )

    active_questions = list(
        Question.objects.filter(questionnaire_version=version, is_active=True).order_by("order")
    )
    answered_ids = set(question_ids)
    missing = [q.order for q in active_questions if q.id not in answered_ids]
    if missing:
        raise ScoringValidationError(f"missing answers for question orders {missing}")

    active_personas = list(Persona.objects.filter(is_active=True))
    if not active_personas:
        raise ScoringValidationError("no active personas configured")
    active_slugs = {persona.slug for persona in active_personas}

    weight_rows = list(
        AnswerPersonaWeight.objects.select_related(
            "persona", "answer_option__question__questionnaire_version"
        ).filter(answer_option__question__questionnaire_version=version)
    )
    inactive_refs = {
        row.persona.slug for row in weight_rows if row.persona.slug not in active_slugs
    }
    if inactive_refs:
        raise ScoringValidationError(
            f"weights reference inactive personas: {sorted(inactive_refs)}"
        )

    option_weights = {}
    question_max = {}
    for row in weight_rows:
        option = row.answer_option
        if not option.is_active or row.weight <= 0:
            continue
        if not option.question.is_active:
            continue
        option_weights.setdefault(option.id, []).append((row.persona.slug, row.weight))
        per_slug = question_max.setdefault(option.question_id, {})
        per_slug[row.persona.slug] = max(per_slug.get(row.persona.slug, 0), row.weight)

    max_possible = {}
    for per_slug in question_max.values():
        for slug, weight in per_slug.items():
            max_possible[slug] = max_possible.get(slug, 0) + weight

    raw = {slug: 0 for slug in active_slugs}
    strong = {slug: 0 for slug in active_slugs}
    core = {slug: 0 for slug in active_slugs}

    for answer in answers:
        question = answer.question
        for slug, weight in option_weights.get(answer.id, []):
            raw[slug] += weight
            if weight >= STRONG_WEIGHT_THRESHOLD:
                strong[slug] += 1
            if question.order in CORE_QUESTION_ORDERS:
                core[slug] += weight

    priority_index = {slug: index for index, slug in enumerate(TIE_BREAK_PRIORITY)}
    fallback_index = len(TIE_BREAK_PRIORITY)

    def sort_key(slug):
        return (
            -raw[slug],
            -strong[slug],
            -core[slug],
            priority_index.get(slug, fallback_index),
        )

    ranked = sorted(active_slugs, key=sort_key)

    primary = ranked[0]
    secondary = ranked[1] if len(ranked) > 1 and raw[ranked[1]] > 0 else None

    normalized = {
        slug: int(round(raw[slug] * 100 / max_possible[slug]))
        if max_possible.get(slug)
        else 0
        for slug in active_slugs
    }

    companion_trait = next(
        (answer.companion_trait for answer in answers if answer.companion_trait), None
    )

    return ScoringResult(
        raw_scores=dict(sorted(raw.items())),
        normalized_scores=dict(sorted(normalized.items())),
        ranked_personas=ranked,
        primary=primary,
        secondary=secondary,
        tie_metadata={"step": _resolve_tie_step(ranked, raw, strong, core)},
        companion_trait=companion_trait,
        scoring_question_count=len(question_max),
    )


def _resolve_tie_step(ranked, raw, strong, core):
    top_raw = raw[ranked[0]]
    raw_tied = [slug for slug in ranked if raw[slug] == top_raw]
    if len(raw_tied) == 1:
        return "raw"
    top_strong = max(strong[slug] for slug in raw_tied)
    strong_tied = [slug for slug in raw_tied if strong[slug] == top_strong]
    if len(strong_tied) == 1:
        return "strong"
    top_core = max(core[slug] for slug in strong_tied)
    core_tied = [slug for slug in strong_tied if core[slug] == top_core]
    if len(core_tied) == 1:
        return "core"
    return "priority"
