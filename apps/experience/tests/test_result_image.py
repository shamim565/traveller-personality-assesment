import pytest
from django.urls import reverse

from apps.experience.models import AssessmentSession, AssessmentStatus
from apps.experience.services import result_image

PROFILE = {"name": "Sazid", "age": 25, "gender": "male"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.fixture
def hx():
    return {"HTTP_HX_REQUEST": "true"}


def complete_flow(client, version, hx):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for q_order in range(1, 7):
        option = version.questions.get(order=q_order).options.get(order=1)
        client.post("/experience/answer/", {"answer_id": option.id}, **hx)
    response = client.post("/experience/complete/", **hx)
    assert response.status_code == 200
    return AssessmentSession.objects.get(status=AssessmentStatus.COMPLETED)


def result_url(assessment):
    return reverse("experience:result_image", args=[assessment.session_uuid])


def test_result_image_download(seeded, client, hx):
    assessment = complete_flow(client, seeded, hx)
    response = client.get(result_url(assessment))
    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert "attachment" in response["Content-Disposition"]
    assert "beach_lover-result.png" in response["Content-Disposition"]
    assert response.content.startswith(PNG_SIGNATURE)
    assert len(response.content) > 10_000


def test_result_image_ignores_incomplete_assessments(seeded, client, hx):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    assessment = AssessmentSession.objects.get()
    assert assessment.status == AssessmentStatus.STARTED
    assert client.get(result_url(assessment)).status_code == 404


def test_result_image_unknown_uuid_is_404(seeded, client):
    url = reverse(
        "experience:result_image",
        args=["00000000-0000-0000-0000-000000000000"],
    )
    assert client.get(url).status_code == 404


def test_result_image_renders_visitor_name(seeded, client, hx):
    assessment = complete_flow(client, seeded, hx)
    assert assessment.visitor_name == "Sazid"
    named = result_image.render_result_png(assessment)
    assessment.visitor_name = ""
    blank = result_image.render_result_png(assessment)
    assert named.startswith(PNG_SIGNATURE)
    assert blank.startswith(PNG_SIGNATURE)
    assert named != blank
