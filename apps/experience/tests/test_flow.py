import pytest
from django.test import Client

from apps.experience.models import (
    AssessmentAnswer,
    AssessmentPersonaScore,
    AssessmentSession,
    AssessmentStatus,
    Question,
)

PROFILE = {"name": "Sazid", "age": 25, "gender": "male"}

ALL_BEACH = [(q, 1) for q in range(1, 7)]
ALL_HERITAGE = [(1, 2), (2, 3), (3, 2), (4, 2), (5, 1), (6, 2)]


@pytest.fixture
def hx():
    return {"HTTP_HX_REQUEST": "true"}


def start(client, **headers):
    return client.post("/experience/start/", **headers)


def answer(client, answer_option_id, **headers):
    return client.post("/experience/answer/", {"answer_id": answer_option_id}, **headers)


def answer_option_id(version, q_order, o_order):
    question = Question.objects.get(questionnaire_version=version, order=q_order)
    return question.options.get(order=o_order).id


def run_full_flow(client, version, pairs, hx):
    assert start(client, **hx).status_code == 200
    assert client.post("/experience/profile/", PROFILE, **hx).status_code == 200
    for q_order, o_order in pairs:
        response = answer(client, answer_option_id(version, q_order, o_order), **hx)
        assert response.status_code == 200
    response = client.post("/experience/complete/", **hx)
    assert response.status_code == 200
    return response


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------

def test_start_creates_session_and_started_record(seeded, client, hx):
    response = start(client, **hx)
    assert response.status_code == 200
    session = client.session
    assert session["experience.qv_id"] == seeded.id
    assert session["experience.answers"] == {}
    assert len(session["experience.question_order"]) == 6
    assert "experience.name" not in session
    assessment = AssessmentSession.objects.get()
    assert assessment.status == AssessmentStatus.STARTED
    assert assessment.questionnaire_version == seeded


def test_profile_valid_stores_session_and_returns_q1(seeded, client, hx):
    start(client, **hx)
    response = client.post("/experience/profile/", PROFILE, **hx)
    assert response.status_code == 200
    assert "প্রশ্ন" in response.content.decode()
    session = client.session
    assert session["experience.name"] == "Sazid"
    assert session["experience.age"] == 25
    assert session["experience.gender"] == "male"


def test_profile_invalid_returns_errors_without_state(seeded, client, hx):
    start(client, **hx)
    response = client.post(
        "/experience/profile/", {"name": "Sazid", "age": 250, "gender": "male"}, **hx
    )
    assert response.status_code == 200
    session = client.session
    assert "experience.name" not in session
    content = response.content.decode()
    assert "আপনার বয়স" in content
    assert "100" in content


def test_profile_without_start_returns_error(client, hx):
    response = client.post("/experience/profile/", PROFILE, **hx)
    assert response.status_code == 200
    assert "Something went wrong" in response.content.decode()


def test_answers_accumulate_and_replace_on_reanswer(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    option_1 = answer_option_id(seeded, 1, 1)
    option_2 = answer_option_id(seeded, 1, 2)
    answer(client, option_1, **hx)
    assert client.session["experience.answers"] == {"1": option_1}
    response = answer(client, option_2, **hx)
    assert response.status_code == 200
    assert client.session["experience.answers"] == {"1": option_2}
    assert "প্রশ্ন" in response.content.decode()


def test_answer_for_non_current_question_rejected(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    response = answer(client, answer_option_id(seeded, 3, 1), **hx)
    assert "Something went wrong" in response.content.decode()
    assert client.session["experience.answers"] == {}


def test_unknown_answer_id_rejected(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    response = answer(client, 999999, **hx)
    assert "Something went wrong" in response.content.decode()


def test_final_answer_returns_analyzing(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for q_order in range(1, 6):
        answer(client, answer_option_id(seeded, q_order, 1), **hx)
    response = answer(client, answer_option_id(seeded, 6, 1), **hx)
    assert "Analyzing" in response.content.decode()


# ---------------------------------------------------------------------------
# Completion & persistence
# ---------------------------------------------------------------------------

def test_complete_persists_assessment(seeded, client, hx):
    response = run_full_flow(client, seeded, ALL_BEACH, hx)
    assert "BEACH LOVER" in response.content.decode()
    assessment = AssessmentSession.objects.get()
    assert assessment.status == AssessmentStatus.COMPLETED
    assert assessment.primary_persona.slug == "beach_lover"
    assert assessment.secondary_persona.slug == "nature_explorer"
    assert assessment.gender == "male"
    assert assessment.age_group.name == "Young Adult"
    assert assessment.companion_trait == "solo"
    assert assessment.duration_seconds is not None
    assert AssessmentAnswer.objects.count() == 6
    assert AssessmentPersonaScore.objects.count() == 6
    assert assessment.persona_scores.get(rank=1).persona.slug == "beach_lover"


def test_heritage_flow_primary(seeded, client, hx):
    response = run_full_flow(client, seeded, ALL_HERITAGE, hx)
    assert "HERITAGE HUNTER" in response.content.decode()
    assert AssessmentSession.objects.get().primary_persona.slug == "heritage_hunter"


def test_complete_is_idempotent(seeded, client, hx):
    run_full_flow(client, seeded, ALL_BEACH, hx)
    client.post("/experience/complete/", **hx)
    client.post("/experience/complete/", **hx)
    assert AssessmentSession.objects.count() == 1
    assert AssessmentAnswer.objects.count() == 6
    assert AssessmentPersonaScore.objects.count() == 6


def test_complete_with_missing_answers_fails_gracefully(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    answer(client, answer_option_id(seeded, 1, 1), **hx)
    response = client.post("/experience/complete/", **hx)
    assert "Something went wrong" in response.content.decode()
    assessment = AssessmentSession.objects.get()
    assert assessment.status == AssessmentStatus.STARTED


def test_name_never_persisted_to_db(seeded, client, hx):
    run_full_flow(client, seeded, ALL_BEACH, hx)
    field_names = [field.name for field in AssessmentSession._meta.fields]
    assert "name" not in field_names
    assert "Sazid" not in str(
        list(AssessmentSession.objects.values())
    )


# ---------------------------------------------------------------------------
# Reset & privacy
# ---------------------------------------------------------------------------

def test_reset_clears_session_and_abandons(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    response = client.post("/experience/reset/", **hx)
    assert response.status_code == 200
    assert "DETECT YOUR TRAVEL PERSONA" in response.content.decode()
    session = client.session
    for key in ["experience.name", "experience.age", "experience.gender", "experience.answers", "experience.assessment_uuid"]:
        assert key not in session
    assert AssessmentSession.objects.get().status == AssessmentStatus.ABANDONED


def test_start_abandons_previous_unfinished(seeded, client, hx):
    start(client, **hx)
    start(client, **hx)
    sessions = list(AssessmentSession.objects.order_by("started_at"))
    assert len(sessions) == 2
    assert sessions[0].status == AssessmentStatus.ABANDONED
    assert sessions[1].status == AssessmentStatus.STARTED


def test_completed_assessment_survives_reset(seeded, client, hx):
    run_full_flow(client, seeded, ALL_BEACH, hx)
    client.post("/experience/reset/", **hx)
    assert AssessmentSession.objects.get().status == AssessmentStatus.COMPLETED


# ---------------------------------------------------------------------------
# Landing / refresh resume
# ---------------------------------------------------------------------------

def test_landing_idle_when_fresh(client):
    response = Client().get("/")
    assert "DETECT YOUR TRAVEL PERSONA" in response.content.decode()


def test_landing_resumes_quiz_after_refresh(seeded, client, hx):
    start(client, **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for q_order in range(1, 4):
        answer(client, answer_option_id(seeded, q_order, 1), **hx)
    response = client.get("/")
    assert "প্রশ্ন" in response.content.decode()
    assert "প্রশ্ন 4 / 6" in response.content.decode()


def test_landing_shows_result_after_complete(seeded, client, hx):
    run_full_flow(client, seeded, ALL_BEACH, hx)
    response = client.get("/")
    assert "BEACH LOVER" in response.content.decode()


def test_landing_shows_profile_when_missing(seeded, client, hx):
    start(client, **hx)
    response = client.get("/")
    assert "আপনার নাম" in response.content.decode()


# ---------------------------------------------------------------------------
# HTMX response contracts
# ---------------------------------------------------------------------------

def test_htmx_request_returns_partial(seeded, client, hx):
    start(client, **hx)
    response = client.post("/experience/profile/", PROFILE, **hx)
    assert "<html" not in response.content.decode()


def test_non_htmx_request_returns_full_page(seeded, client):
    start(client)
    response = client.post("/experience/profile/", PROFILE)
    assert "<html" in response.content.decode()


def test_csrf_enforced(client):
    strict = Client(enforce_csrf_checks=True)
    response = strict.post("/experience/start/")
    assert response.status_code == 403
