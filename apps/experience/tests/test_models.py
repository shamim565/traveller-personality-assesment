import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AnswerPersonaWeight,
    AssessmentAnswer,
    AssessmentSession,
    AssessmentStatus,
    Persona,
    PersonaAvatar,
    Question,
    QuestionnaireVersion,
)


def test_question_order_unique_per_version(qv):
    Question.objects.create(questionnaire_version=qv, text_bn="Q", order=1)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Question.objects.create(questionnaire_version=qv, text_bn="Q2", order=1)


def test_answer_option_order_unique_per_question(question):
    AnswerOption.objects.create(question=question, text_bn="A", order=1)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            AnswerOption.objects.create(question=question, text_bn="B", order=1)


def test_weight_unique_per_option_persona(answer, persona):
    AnswerPersonaWeight.objects.create(answer_option=answer, persona=persona, weight=4)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            AnswerPersonaWeight.objects.create(
                answer_option=answer, persona=persona, weight=3
            )


def test_weight_range_check(answer, persona):
    weight = AnswerPersonaWeight(answer_option=answer, persona=persona, weight=7)
    with pytest.raises(ValidationError):
        weight.full_clean()
    weight = AnswerPersonaWeight(answer_option=answer, persona=persona, weight=-1)
    with pytest.raises(ValidationError):
        weight.full_clean()


def test_age_group_min_lte_max_check(db):
    group = AgeGroup(name="Bad", min_age=30, max_age=20)
    with pytest.raises(ValidationError):
        group.full_clean()


def test_age_group_resolve_picks_inclusive_group(db):
    AgeGroup.objects.create(name="Teen", min_age=10, max_age=17, order=1)
    AgeGroup.objects.create(name="Young Adult", min_age=18, max_age=29, order=2)
    assert AgeGroup.resolve(12).name == "Teen"
    assert AgeGroup.resolve(17).name == "Teen"
    assert AgeGroup.resolve(18).name == "Young Adult"
    assert AgeGroup.resolve(35) is None


def test_assessment_answer_unique_per_question(qv, question, answer, persona):
    assessment = AssessmentSession.objects.create(
        questionnaire_version=qv, started_at=timezone.now()
    )
    AssessmentAnswer.objects.create(
        assessment=assessment, question=question, answer_option=answer
    )
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            AssessmentAnswer.objects.create(
                assessment=assessment, question=question, answer_option=answer
            )


def test_assessment_default_status_and_kiosk(settings, qv):
    settings.KIOSK_IDENTIFIER = "KIOSK-99"
    assessment = AssessmentSession.objects.create(
        questionnaire_version=qv, started_at=timezone.now()
    )
    assert assessment.status == AssessmentStatus.STARTED
    assert assessment.kiosk_identifier == "KIOSK-99"
    assert assessment.session_uuid is not None


def test_avatar_scoping_fields(persona):
    avatar = PersonaAvatar.objects.create(
        persona=persona, gender="male", image="avatars/x.webp", is_default=True
    )
    assert avatar.age_group is None
    assert avatar.is_default is True
