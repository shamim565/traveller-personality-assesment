"""Read-model queries for the kiosk flow (docs/architecture.md §3)."""

from apps.experience.models import Question, QuestionnaireVersion


def get_active_version():
    return QuestionnaireVersion.objects.filter(is_active=True).order_by("-created_at").first()


def get_active_questions(version):
    return Question.objects.filter(
        questionnaire_version=version, is_active=True
    ).order_by("order")
