"""Kiosk assessment orchestration: start, profile, answer, complete, reset.

Views stay thin — all state transitions and persistence live here.
"""

import uuid

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from apps.experience.services import sessions
from apps.experience.forms import ProfileForm
from apps.experience.models import (
    AgeGroup,
    AnswerOption,
    AssessmentAnswer,
    AssessmentPersonaScore,
    AssessmentSession,
    AssessmentStatus,
    Persona,
    Question,
)
from apps.experience.selectors import questionnaire as questionnaire_selectors
from apps.experience.services import avatars, result_image, scoring


class ExperienceStateError(Exception):
    """Invalid or stale kiosk state — render the friendly error partial."""


def start_experience(request):
    version = questionnaire_selectors.get_active_version()
    if version is None:
        raise ExperienceStateError("no active questionnaire version configured")
    questions = list(questionnaire_selectors.get_active_questions(version))
    if not questions:
        raise ExperienceStateError("active questionnaire has no questions")

    previous_uuid = sessions.get_assessment_uuid(request)
    sessions.clear_session(request)
    if previous_uuid:
        _mark_abandoned_if_unfinished(previous_uuid)

    assessment = AssessmentSession.objects.create(
        questionnaire_version=version,
        started_at=timezone.now(),
    )
    sessions.write_start_state(request, version, questions, assessment)
    return assessment


def save_profile(request, data):
    if sessions.get_qv_id(request) is None:
        raise ExperienceStateError("experience not started")
    form = ProfileForm(data)
    if not form.is_valid():
        return form
    sessions.set_profile(request, form.cleaned_data)
    return None


def current_question(request):
    order = sessions.get_question_order(request)
    answers = sessions.get_answers(request)
    for question_id in order:
        if str(question_id) not in answers:
            return Question.objects.get(pk=question_id)
    return None


QUESTION_BACKGROUNDS = {
    1: ("backgrounds/q1.webp", "dark"),
    2: ("backgrounds/q2.webp", "medium"),
    3: ("backgrounds/q3.webp", "medium"),
    4: ("backgrounds/q4.webp", "dark"),
    5: ("backgrounds/q5.webp", "medium"),
    6: ("backgrounds/q6.webp", "dark"),
}


def question_context(question, request):
    options = list(question.options.filter(is_active=True).order_by("order"))
    answered = len(sessions.get_answers(request))
    total = len(sessions.get_question_order(request))
    background, background_overlay = QUESTION_BACKGROUNDS.get(
        question.order, ("branding/kv/kv-placeholder.webp", "medium")
    )
    return {
        "question": question,
        "options": options,
        "current": answered + 1,
        "total": total,
        "background": background,
        "background_overlay": background_overlay,
    }


def submit_answer(request, raw_answer_id):
    if sessions.get_qv_id(request) is None or sessions.get_name(request) is None:
        raise ExperienceStateError("profile not completed")
    try:
        answer_id = int(raw_answer_id)
    except (TypeError, ValueError):
        raise ExperienceStateError("invalid answer option")

    current = current_question(request)
    if current is None:
        raise ExperienceStateError("quiz already answered")

    try:
        option = AnswerOption.objects.select_related(
            "question__questionnaire_version"
        ).get(pk=answer_id)
    except AnswerOption.DoesNotExist:
        raise ExperienceStateError("unknown answer option")
    if not option.is_active or not option.question.is_active:
        raise ExperienceStateError("answer option unavailable")
    if option.question.questionnaire_version_id != sessions.get_qv_id(request):
        raise ExperienceStateError("answer from the wrong questionnaire")

    already_answered = str(option.question_id) in sessions.get_answers(request)
    if option.question_id != current.id and not already_answered:
        raise ExperienceStateError("answer for a non-current question")

    sessions.add_answer(request, option.question_id, option.id)

    next_question = current_question(request)
    if next_question is None:
        return "analyzing", {}
    return "question", question_context(next_question, request)


def complete_experience(request):
    raw_uuid = sessions.get_assessment_uuid(request)
    if not raw_uuid:
        raise ExperienceStateError("no active experience")
    try:
        assessment_uuid = uuid.UUID(raw_uuid)
    except ValueError:
        raise ExperienceStateError("invalid assessment state")

    with transaction.atomic():
        assessment = AssessmentSession.objects.select_for_update().get(
            session_uuid=assessment_uuid
        )
        if assessment.status == AssessmentStatus.COMPLETED:
            return result_context(assessment, request)

        questions = list(
            questionnaire_selectors.get_active_questions(assessment.questionnaire_version)
        )
        answers_map = sessions.get_answers(request)
        if len(answers_map) != len(questions):
            raise ExperienceStateError("assessment incomplete")

        options = list(
            AnswerOption.objects.select_related("question__questionnaire_version").filter(
                pk__in=answers_map.values()
            )
        )
        scoring_result = scoring.calculate_travel_persona(options)

        persona_by_slug = {p.slug: p for p in Persona.objects.filter(is_active=True)}
        assessment.visitor_name = sessions.get_name(request) or ""
        assessment.age_group = AgeGroup.resolve(sessions.get_age(request))
        assessment.gender = sessions.get_gender(request)
        assessment.primary_persona = persona_by_slug[scoring_result.primary]
        assessment.secondary_persona = (
            persona_by_slug.get(scoring_result.secondary)
            if scoring_result.secondary
            else None
        )
        assessment.companion_trait = scoring_result.companion_trait
        assessment.completed_at = timezone.now()
        assessment.duration_seconds = max(
            0, int((assessment.completed_at - assessment.started_at).total_seconds())
        )
        assessment.status = AssessmentStatus.COMPLETED
        assessment.save(
            update_fields=[
                "visitor_name",
                "age_group",
                "gender",
                "primary_persona",
                "secondary_persona",
                "companion_trait",
                "completed_at",
                "duration_seconds",
                "status",
            ]
        )

        AssessmentAnswer.objects.bulk_create(
            [
                AssessmentAnswer(
                    assessment=assessment,
                    question_id=int(question_id),
                    answer_option_id=answer_option_id,
                )
                for question_id, answer_option_id in answers_map.items()
            ]
        )
        AssessmentPersonaScore.objects.bulk_create(
            [
                AssessmentPersonaScore(
                    assessment=assessment,
                    persona=persona_by_slug[slug],
                    raw_score=scoring_result.raw_scores[slug],
                    normalized_score=scoring_result.normalized_scores[slug],
                    rank=index,
                )
                for index, slug in enumerate(scoring_result.ranked_personas, start=1)
            ]
        )
    return result_context(assessment, request)


def result_context(assessment, request):
    persona = assessment.primary_persona
    download_url = request.build_absolute_uri(
        reverse("experience:result_image", args=[assessment.session_uuid])
    )
    return {
        "name": sessions.get_name(request),
        "persona": persona,
        "background": result_image.result_background(persona),
        "keywords": [
            keyword.strip()
            for keyword in persona.keywords_bn.split("•")
            if keyword.strip()
        ],
        "avatar": avatars.resolve_avatar(
            persona, gender=assessment.gender, age_group=assessment.age_group
        ),
        "qr_image": result_image.qr_png_data_uri(download_url),
    }


def reset_experience(request):
    assessment_uuid = sessions.get_assessment_uuid(request)
    sessions.clear_session(request)
    if assessment_uuid:
        _mark_abandoned_if_unfinished(assessment_uuid)


def resume_context(request):
    if sessions.get_qv_id(request) is None:
        return {"step": "idle"}

    raw_uuid = sessions.get_assessment_uuid(request)
    if raw_uuid:
        try:
            assessment = AssessmentSession.objects.get(session_uuid=uuid.UUID(raw_uuid))
        except (ValueError, AssessmentSession.DoesNotExist):
            sessions.clear_session(request)
            return {"step": "idle"}
        if assessment.status == AssessmentStatus.COMPLETED:
            return {"step": "result", "context": result_context(assessment, request)}

    if sessions.get_name(request) is None:
        return {"step": "profile", "context": {"form": ProfileForm()}}

    question = current_question(request)
    if question is None:
        return {
            "step": "analyzing",
            "context": {"analyzing_ms": settings.EXPERIENCE_ANALYZING_MS},
        }
    return {"step": "quiz", "context": question_context(question, request)}


def _mark_abandoned_if_unfinished(assessment_uuid):
    try:
        parsed = uuid.UUID(assessment_uuid)
    except (ValueError, TypeError):
        return
    AssessmentSession.objects.filter(
        session_uuid=parsed, status=AssessmentStatus.STARTED
    ).update(status=AssessmentStatus.ABANDONED)
