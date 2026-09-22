import logging

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from apps.core.http import is_htmx
from apps.experience.forms import ProfileForm
from apps.experience.services import assessment as assessment_service

logger = logging.getLogger(__name__)

PARTIAL_PAGES = {
    "partials/idle.html": "kiosk/idle.html",
    "partials/profile_form.html": "kiosk/profile.html",
    "partials/question.html": "kiosk/quiz.html",
    "partials/analyzing.html": "kiosk/analyzing.html",
    "partials/result.html": "kiosk/result.html",
    "partials/error.html": "kiosk/error.html",
}

LANDING_TEMPLATES = {
    "idle": "kiosk/idle.html",
    "profile": "kiosk/profile.html",
    "quiz": "kiosk/quiz.html",
    "analyzing": "kiosk/analyzing.html",
    "result": "kiosk/result.html",
}


def _response(request, template, context=None):
    context = context or {}
    if not is_htmx(request):
        return render(request, PARTIAL_PAGES[template], context)
    return render(request, template, context)


def _error_response(request, action):
    logger.exception("kiosk action failed: %s", action)
    return _response(request, "partials/error.html")


@require_GET
def landing(request):
    state = assessment_service.resume_context(request)
    return render(
        request,
        LANDING_TEMPLATES[state["step"]],
        state.get("context", {}),
    )


@require_POST
def start(request):
    try:
        assessment_service.start_experience(request)
    except Exception:
        return _error_response(request, "start")
    return _response(request, "partials/profile_form.html", {"form": ProfileForm()})


@require_POST
def profile(request):
    try:
        form = assessment_service.save_profile(request, request.POST)
    except Exception:
        return _error_response(request, "profile")
    if form is not None:
        return _response(request, "partials/profile_form.html", {"form": form})

    question = assessment_service.current_question(request)
    if question is None:
        return _response(
            request,
            "partials/analyzing.html",
            {"analyzing_ms": settings.EXPERIENCE_ANALYZING_MS},
        )
    return _response(
        request,
        "partials/question.html",
        assessment_service.question_context(question, request),
    )


@require_POST
def answer(request):
    try:
        kind, context = assessment_service.submit_answer(
            request, request.POST.get("answer_id")
        )
    except Exception:
        return _error_response(request, "answer")
    if kind == "analyzing":
        return _response(
            request,
            "partials/analyzing.html",
            {"analyzing_ms": settings.EXPERIENCE_ANALYZING_MS},
        )
    return _response(request, "partials/question.html", context)


@require_POST
def complete(request):
    try:
        context = assessment_service.complete_experience(request)
    except Exception:
        return _error_response(request, "complete")
    return _response(request, "partials/result.html", context)


@require_POST
def reset(request):
    try:
        assessment_service.reset_experience(request)
    except Exception:
        logger.exception("kiosk reset failed")
    return _response(request, "partials/idle.html")
