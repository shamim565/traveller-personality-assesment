import pytest

from apps.experience.models import Question, QuestionnaireVersion
from apps.experience.services.scoring import (
    ScoringValidationError,
    calculate_travel_persona,
)

PROFILE = {"name": "Sazid", "age": 25, "gender": "male"}


@pytest.fixture
def hx():
    return {"HTTP_HX_REQUEST": "true"}


def option_id(question_order, option_order=1):
    question = Question.objects.get(order=question_order)
    return question.options.get(order=option_order).id


def test_start_query_budget(seeded, client, hx, django_assert_num_queries):
    with django_assert_num_queries(7):
        client.post("/experience/start/", **hx)


def test_profile_query_budget(seeded, client, hx, django_assert_num_queries):
    client.post("/experience/start/", **hx)
    with django_assert_num_queries(6):
        client.post("/experience/profile/", PROFILE, **hx)


def test_answer_query_budget(seeded, client, hx, django_assert_num_queries):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    with django_assert_num_queries(10):
        client.post("/experience/answer/", {"answer_id": option_id(1)}, **hx)


def test_complete_query_budget(seeded, client, hx, django_assert_num_queries):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for order in range(1, 7):
        client.post("/experience/answer/", {"answer_id": option_id(order)}, **hx)
    with django_assert_num_queries(17):
        client.post("/experience/complete/", **hx)


def test_idle_landing_has_no_avatar_n_plus_one(seeded, client, django_assert_num_queries):
    with django_assert_num_queries(2):
        client.get("/")


def test_version_name_unique_constraint(seeded):
    with pytest.raises(Exception):
        QuestionnaireVersion.objects.create(name="World Tourism Day 2026", version="v1")


def test_scoring_raises_when_no_active_personas(seeded):
    from apps.experience.models import Persona

    Persona.objects.update(is_active=False)
    answers = list(
        seeded.questions.get(order=1).options.all()[:1]
    ) + [
        q.options.first()
        for q in seeded.questions.exclude(order=1).order_by("order")
    ]
    with pytest.raises(ScoringValidationError, match="no active personas"):
        calculate_travel_persona(answers)
