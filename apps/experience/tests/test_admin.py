import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import Client

from apps.experience import admin as experience_admin
from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AnswerPersonaWeight,
    AssessmentSession,
    Persona,
    PersonaAvatar,
    Question,
    QuestionnaireVersion,
)


@pytest.fixture
def staff_client(db):
    user = User.objects.create_superuser("admin", "admin@example.com", "pass12345")
    client = Client()
    client.force_login(user)
    return client


REGISTERED = [
    QuestionnaireVersion,
    Persona,
    Question,
    AnswerOption,
    AnswerPersonaWeight,
    AgeGroup,
    PersonaAvatar,
    AssessmentSession,
]


@pytest.mark.parametrize("model", REGISTERED)
def test_models_registered_in_admin(model):
    assert model in admin.site._registry


def test_activate_versions_action_deactivates_others(db):
    qv1 = QuestionnaireVersion.objects.create(name="One", version="v1", is_active=True)
    qv2 = QuestionnaireVersion.objects.create(name="Two", version="v2", is_active=False)
    experience_admin.activate_versions(None, None, QuestionnaireVersion.objects.filter(pk=qv2.pk))
    qv1.refresh_from_db()
    qv2.refresh_from_db()
    assert qv2.is_active is True
    assert qv1.is_active is False


def test_version_of_resolution(qv, question, answer_option_with_weight):
    mixin = experience_admin.VersionedContentWarningMixin()
    assert mixin._questionnaire_version_of(qv) == qv
    assert mixin._questionnaire_version_of(question) == qv
    assert mixin._questionnaire_version_of(answer_option_with_weight) == qv
    assert mixin._questionnaire_version_of(None) is None


def test_admin_index_and_question_change_view_accessible(staff_client, qv, question):
    response = staff_client.get("/admin/")
    assert response.status_code == 200
    response = staff_client.get(f"/admin/experience/question/{question.pk}/change/")
    assert response.status_code == 200


def test_change_view_accessible_with_used_version(staff_client, qv, question):
    from apps.experience.models import AssessmentSession
    from django.utils import timezone

    AssessmentSession.objects.create(questionnaire_version=qv, started_at=timezone.now())
    response = staff_client.get(f"/admin/experience/question/{question.pk}/change/")
    assert response.status_code == 200
