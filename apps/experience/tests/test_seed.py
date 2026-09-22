import pytest
from django.core.management import call_command

from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AnswerPersonaWeight,
    CompanionTrait,
    Persona,
    PersonaAvatar,
    Question,
    QuestionnaireVersion,
)

PERSONA_SLUGS = [
    "heritage_hunter",
    "beach_lover",
    "adventure_seeker",
    "nature_explorer",
    "urban_explorer",
    "culture_connector",
]


@pytest.fixture
def seeded(db):
    call_command("seed_travel_personas", verbosity=0)


def test_seed_is_idempotent(db):
    call_command("seed_travel_personas", verbosity=0)
    call_command("seed_travel_personas", verbosity=0)
    assert QuestionnaireVersion.objects.count() == 1
    assert Persona.objects.count() == 6
    assert Question.objects.count() == 6
    assert AnswerOption.objects.count() == 30
    assert AnswerPersonaWeight.objects.count() == 46
    assert AgeGroup.objects.count() == 5
    assert PersonaAvatar.objects.count() == 6


def test_active_version_exists(seeded):
    version = QuestionnaireVersion.objects.get()
    assert version.name == "World Tourism Day 2026"
    assert version.version == "v1"
    assert version.is_active is True
    assert QuestionnaireVersion.objects.filter(is_active=True).count() == 1


def test_all_six_personas_seeded(seeded):
    assert set(Persona.objects.values_list("slug", flat=True)) == set(PERSONA_SLUGS)
    for persona in Persona.objects.all():
        assert persona.short_description_bn
        assert persona.keywords_bn


def test_matrix_spot_checks(seeded):
    version = QuestionnaireVersion.objects.get()

    def weights(q_order, o_order):
        question = Question.objects.get(questionnaire_version=version, order=q_order)
        option = AnswerOption.objects.get(question=question, order=o_order)
        return {w.persona.slug: w.weight for w in option.weights.all()}

    assert weights(3, 3) == {"adventure_seeker": 4, "nature_explorer": 2}
    assert weights(6, 4) == {"culture_connector": 4, "heritage_hunter": 1, "nature_explorer": 1}
    assert weights(1, 3) == {"adventure_seeker": 3, "nature_explorer": 3}
    assert weights(2, 2) == {"nature_explorer": 4, "adventure_seeker": 2}


def test_question_5_is_trait_only_without_weights(seeded):
    version = QuestionnaireVersion.objects.get()
    q5 = Question.objects.get(questionnaire_version=version, order=5)
    assert q5.options.count() == 5
    assert not AnswerPersonaWeight.objects.filter(answer_option__question=q5).exists()
    traits = {o.companion_trait for o in q5.options.all()}
    assert traits == {
        CompanionTrait.SOLO,
        CompanionTrait.COUPLE,
        CompanionTrait.FAMILY,
        CompanionTrait.FRIENDS,
        CompanionTrait.DESTINATION_FIRST,
    }


def test_seed_preserves_admin_edits(seeded):
    question = Question.objects.get(order=1)
    question.text_bn = "Admin-edited text"
    question.save(update_fields=["text_bn"])
    call_command("seed_travel_personas", verbosity=0)
    question.refresh_from_db()
    assert question.text_bn == "Admin-edited text"
    assert Question.objects.count() == 6


def test_age_groups_seeded_with_ranges(seeded):
    assert AgeGroup.objects.get(name="Teen").min_age == 10
    assert AgeGroup.objects.get(name="Senior").max_age == 100
    assert AgeGroup.resolve(25).name == "Young Adult"


def test_default_avatars_seeded(seeded):
    for slug in PERSONA_SLUGS:
        avatar = PersonaAvatar.objects.get(persona__slug=slug)
        assert avatar.is_default is True
        assert avatar.gender == ""
        assert avatar.image == f"avatars/{slug}/neutral.svg"
