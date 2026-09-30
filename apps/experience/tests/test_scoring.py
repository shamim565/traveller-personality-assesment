import pytest

from apps.experience.models import (
    AnswerOption,
    AnswerPersonaWeight,
    Persona,
    Question,
    QuestionnaireVersion,
)
from apps.experience.services.scoring import (
    ScoringValidationError,
    calculate_travel_persona,
)

PERSONAS = [
    ("heritage_hunter", "Heritage Hunter", 1),
    ("beach_lover", "Beach Lover", 5),
    ("adventure_seeker", "Adventure Seeker", 4),
    ("nature_explorer", "Nature Explorer", 2),
    ("urban_explorer", "Urban Explorer", 6),
    ("culture_connector", "Culture Connector", 3),
]


@pytest.fixture
def personas(db):
    return {
        slug: Persona.objects.create(name=name, slug=slug, tie_break_order=tie_break)
        for slug, name, tie_break in PERSONAS
    }


def answer_for(version, q_order, o_order):
    question = Question.objects.get(questionnaire_version=version, order=q_order)
    return (
        AnswerOption.objects.select_related("question__questionnaire_version")
        .get(question=question, order=o_order)
    )


def make_answers(version, pairs):
    return [answer_for(version, q, o) for q, o in pairs]


def build_fixture_questionnaire(personas, spec):
    version = QuestionnaireVersion.objects.create(name="Fixture", version="v1", is_active=True)
    for q_order, options in spec.items():
        question = Question.objects.create(
            questionnaire_version=version, text_bn=f"Q{q_order}", order=q_order
        )
        for o_order, weights in options.items():
            option = AnswerOption.objects.create(
                question=question, text_bn=f"O{o_order}", order=o_order
            )
            for slug, weight in weights.items():
                AnswerPersonaWeight.objects.create(
                    answer_option=option, persona=personas[slug], weight=weight
                )
    return version


# ---------------------------------------------------------------------------
# Calibration cases — expected results per docs/scoring-system.md §6
# ---------------------------------------------------------------------------

CALIBRATION_CASES = [
    (
        "pure_beach",
        [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
        "beach_lover",
        {"beach_lover": 18, "nature_explorer": 7},
    ),
    (
        "pure_heritage",
        [(1, 2), (2, 3), (3, 2), (4, 2), (5, 1), (6, 2)],
        "heritage_hunter",
        {"heritage_hunter": 20, "culture_connector": 5},
    ),
    (
        "pure_adventure",
        [(1, 3), (2, 2), (3, 3), (4, 3), (5, 1), (6, 3)],
        "adventure_seeker",
        {"adventure_seeker": 17, "nature_explorer": 12},
    ),
    (
        "pure_nature",
        [(1, 3), (2, 2), (3, 1), (4, 1), (5, 1), (6, 1)],
        "nature_explorer",
        {"nature_explorer": 14, "beach_lover": 10, "adventure_seeker": 5},
    ),
    (
        "pure_urban",
        [(1, 5), (2, 5), (3, 5), (4, 5), (5, 1), (6, 5)],
        "urban_explorer",
        {"urban_explorer": 20, "culture_connector": 2},
    ),
    (
        "pure_culture",
        [(1, 4), (2, 4), (3, 4), (4, 4), (5, 1), (6, 4)],
        "culture_connector",
        {"culture_connector": 20, "heritage_hunter": 4, "nature_explorer": 2},
    ),
    (
        "heritage_culture",
        [(1, 2), (2, 4), (3, 2), (4, 4), (5, 1), (6, 4)],
        "culture_connector",
        {"culture_connector": 14, "heritage_hunter": 10},
    ),
    (
        "nature_adventure",
        [(1, 3), (2, 2), (3, 3), (4, 3), (5, 1), (6, 3)],
        "adventure_seeker",
        {"adventure_seeker": 17, "nature_explorer": 12},
    ),
    (
        "beach_nature",
        [(1, 1), (2, 2), (3, 1), (4, 1), (5, 1), (6, 1)],
        "beach_lover",
        {"beach_lover": 14, "nature_explorer": 11},
    ),
    (
        "urban_culture",
        [(1, 5), (2, 4), (3, 5), (4, 4), (5, 1), (6, 5)],
        "urban_explorer",
        {"urban_explorer": 12, "culture_connector": 10},
    ),
]


@pytest.mark.parametrize("name,pairs,expected_primary,expected_raw", CALIBRATION_CASES)
def test_calibration_cases(seeded, name, pairs, expected_primary, expected_raw):
    result = calculate_travel_persona(make_answers(seeded, pairs))
    assert result.primary == expected_primary, name
    assert result.tie_metadata["step"] == "raw"
    for slug, raw in expected_raw.items():
        assert result.raw_scores[slug] == raw, f"{name}: {slug}"
    assert result.ranked_personas[0] == expected_primary


def test_scoring_question_count_excludes_q5(seeded):
    result = calculate_travel_persona(
        make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)])
    )
    assert result.scoring_question_count == 5


def test_secondary_persona_is_runner_up(seeded):
    result = calculate_travel_persona(
        make_answers(seeded, [(1, 2), (2, 3), (3, 2), (4, 2), (5, 1), (6, 2)])
    )
    assert result.primary == "heritage_hunter"
    assert result.secondary == "culture_connector"


def test_normalization_uses_persona_max(seeded):
    result = calculate_travel_persona(
        make_answers(seeded, [(1, 1), (2, 2), (3, 1), (4, 1), (5, 1), (6, 1)])
    )
    assert result.normalized_scores["beach_lover"] == round(14 * 100 / 18)
    assert result.normalized_scores["nature_explorer"] == round(11 * 100 / 14)
    assert result.normalized_scores["adventure_seeker"] == round(2 * 100 / 17)


def test_q5_never_changes_persona(seeded):
    base = calculate_travel_persona(
        make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)])
    )
    for option in range(1, 6):
        varied = calculate_travel_persona(
            make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, option), (6, 1)])
        )
        assert varied.raw_scores == base.raw_scores
        assert varied.primary == base.primary
    assert base.companion_trait == "solo"


def test_companion_trait_extracted(seeded):
    result = calculate_travel_persona(
        make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 3), (6, 1)])
    )
    assert result.companion_trait == "family"


def test_deterministic_repeat_runs(seeded):
    answers = make_answers(seeded, [(1, 3), (2, 2), (3, 1), (4, 1), (5, 4), (6, 1)])
    assert calculate_travel_persona(answers) == calculate_travel_persona(answers)


# ---------------------------------------------------------------------------
# Tie handling — contrived fixtures per docs/scoring-system.md §4
# ---------------------------------------------------------------------------

def test_tie_broken_by_strong_count(personas):
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4, "beach_lover": 1}},
            2: {1: {"heritage_hunter": 4, "beach_lover": 1}},
            3: {1: {"beach_lover": 4}},
            4: {1: {"beach_lover": 1}},
            5: {1: {"beach_lover": 1}},
        },
    )
    result = calculate_travel_persona(
        make_answers(version, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)])
    )
    assert result.raw_scores["heritage_hunter"] == 8
    assert result.raw_scores["beach_lover"] == 8
    assert result.primary == "heritage_hunter"
    assert result.tie_metadata["step"] == "strong"


def test_tie_broken_by_core_confidence(personas):
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4}},
            2: {1: {"heritage_hunter": 4}},
            3: {1: {"beach_lover": 4}},
            4: {1: {}},
            5: {1: {"beach_lover": 4}},
        },
    )
    result = calculate_travel_persona(
        make_answers(version, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)])
    )
    assert result.raw_scores["heritage_hunter"] == 8
    assert result.raw_scores["beach_lover"] == 8
    assert result.primary == "heritage_hunter"
    assert result.tie_metadata["step"] == "core"


def test_tie_broken_by_tie_break_order(personas):
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4}},
            2: {1: {"heritage_hunter": 4}},
            3: {1: {"beach_lover": 4}},
            4: {1: {"beach_lover": 4}},
        },
    )
    result = calculate_travel_persona(
        make_answers(version, [(1, 1), (2, 1), (3, 1), (4, 1)])
    )
    assert result.raw_scores["heritage_hunter"] == 8
    assert result.raw_scores["beach_lover"] == 8
    assert result.primary == "heritage_hunter"
    assert result.tie_metadata["step"] == "priority"


def test_tie_break_order_field_controls_priority(personas):
    personas["beach_lover"].tie_break_order = 1
    personas["beach_lover"].save(update_fields=["tie_break_order"])
    personas["heritage_hunter"].tie_break_order = 6
    personas["heritage_hunter"].save(update_fields=["tie_break_order"])
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4}},
            2: {1: {"heritage_hunter": 4}},
            3: {1: {"beach_lover": 4}},
            4: {1: {"beach_lover": 4}},
        },
    )
    result = calculate_travel_persona(
        make_answers(version, [(1, 1), (2, 1), (3, 1), (4, 1)])
    )
    assert result.raw_scores["heritage_hunter"] == 8
    assert result.raw_scores["beach_lover"] == 8
    assert result.primary == "beach_lover"
    assert result.tie_metadata["step"] == "priority"


def test_unset_tie_break_order_falls_back_to_slug(personas):
    Persona.objects.update(tie_break_order=0)
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4}},
            2: {1: {"heritage_hunter": 4}},
            3: {1: {"beach_lover": 4}},
            4: {1: {"beach_lover": 4}},
        },
    )
    result = calculate_travel_persona(
        make_answers(version, [(1, 1), (2, 1), (3, 1), (4, 1)])
    )
    assert result.primary == "beach_lover"


def test_seeded_matrix_tie_resolves_by_priority(seeded):
    result = calculate_travel_persona(
        make_answers(seeded, [(1, 2), (2, 5), (3, 2), (4, 5), (5, 1), (6, 1)])
    )
    assert result.raw_scores["heritage_hunter"] == 8
    assert result.raw_scores["urban_explorer"] == 8
    assert result.primary == "heritage_hunter"
    assert result.tie_metadata["step"] == "priority"


def test_secondary_none_when_runner_up_scores_zero(personas):
    version = build_fixture_questionnaire(
        personas,
        {
            1: {1: {"heritage_hunter": 4}},
            2: {1: {}},
        },
    )
    result = calculate_travel_persona(make_answers(version, [(1, 1), (2, 1)]))
    assert result.primary == "heritage_hunter"
    assert result.secondary is None


# ---------------------------------------------------------------------------
# Malformed input
# ---------------------------------------------------------------------------

def test_empty_answers_raises():
    with pytest.raises(ScoringValidationError):
        calculate_travel_persona([])


def test_duplicate_question_raises(seeded):
    option = answer_for(seeded, 1, 1)
    with pytest.raises(ScoringValidationError, match="duplicate"):
        calculate_travel_persona([option, option])


def test_missing_answer_raises(seeded):
    answers = make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)])
    with pytest.raises(ScoringValidationError, match="missing"):
        calculate_travel_persona(answers)


def test_inactive_question_raises(seeded):
    question = Question.objects.get(questionnaire_version=seeded, order=6)
    question.is_active = False
    question.save(update_fields=["is_active"])
    answers = make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)])
    with pytest.raises(ScoringValidationError, match="inactive question"):
        calculate_travel_persona(answers)


def test_inactive_option_raises(seeded):
    option = answer_for(seeded, 6, 1)
    option.is_active = False
    option.save(update_fields=["is_active"])
    answers = make_answers(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)])
    with pytest.raises(ScoringValidationError, match="inactive answer option"):
        calculate_travel_persona(answers)


def test_mixed_versions_raise(seeded):
    other = QuestionnaireVersion.objects.create(name="Other", version="v2", is_active=False)
    Question.objects.create(questionnaire_version=other, text_bn="X", order=1)
    AnswerOption.objects.create(question=Question.objects.get(questionnaire_version=other, order=1), text_bn="Y", order=1)
    answers = [
        answer_for(seeded, 1, 1),
        answer_for(other, 1, 1),
    ]
    with pytest.raises(ScoringValidationError, match="multiple questionnaire versions"):
        calculate_travel_persona(answers)


def test_weight_on_inactive_persona_raises(personas):
    version = build_fixture_questionnaire(personas, {1: {1: {"heritage_hunter": 4}}})
    personas["heritage_hunter"].is_active = False
    personas["heritage_hunter"].save(update_fields=["is_active"])
    with pytest.raises(ScoringValidationError, match="inactive personas"):
        calculate_travel_persona(make_answers(version, [(1, 1)]))
