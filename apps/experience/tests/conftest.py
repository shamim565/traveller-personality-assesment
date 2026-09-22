import pytest

from apps.experience.models import (
    AnswerOption,
    AnswerPersonaWeight,
    Persona,
    Question,
    QuestionnaireVersion,
)


@pytest.fixture
def qv(db):
    return QuestionnaireVersion.objects.create(name="Test", version="v1")


@pytest.fixture
def persona(db):
    return Persona.objects.create(name="Heritage Hunter", slug="heritage_hunter")


@pytest.fixture
def question(qv):
    return Question.objects.create(questionnaire_version=qv, text_bn="প্রশ্ন?", order=1)


@pytest.fixture
def answer(question):
    return AnswerOption.objects.create(question=question, text_bn="উত্তর", order=1)


@pytest.fixture
def answer_option_with_weight(question, persona):
    option = AnswerOption.objects.create(question=question, text_bn="ওজন", order=2)
    AnswerPersonaWeight.objects.create(answer_option=option, persona=persona, weight=4)
    return option
