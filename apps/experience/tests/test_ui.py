import pytest
from django.test import Client

PROFILE = {"name": "Sazid", "age": 25, "gender": "male"}


def idle_page():
    return Client().get("/").content.decode()


def start_and_profile(client, hx):
    assert client.post("/experience/start/", **hx).status_code == 200
    assert client.post("/experience/profile/", PROFILE, **hx).status_code == 200


@pytest.fixture
def hx():
    return {"HTTP_HX_REQUEST": "true"}


def test_idle_has_branding_and_persona_strip(seeded):
    content = idle_page()
    assert "branding/kv/kv-placeholder.svg" in content
    assert "organizer-placeholder.svg" in content
    assert "sponsor-placeholder.svg" in content
    assert "wtd-mark-placeholder.svg" in content
    assert "#WorldTourismDay2026" in content
    for persona in seeded_avatar_slugs():
        assert f"avatars/{persona}/neutral.svg" in content


def test_quiz_page_has_inactivity_guard(seeded, client, hx):
    start_and_profile(client, hx)
    response = client.get("/")
    assert response.status_code == 200
    content = response.content.decode()
    assert 'data-guard="1"' in content
    assert "progressbar" in content


def test_profile_page_has_stepper_and_gender_cards(seeded, client, hx):
    client.post("/experience/start/", **hx)
    content = client.get("/").content.decode()
    assert "আপনার নাম" in content
    assert "আপনার বয়স" in content
    assert "পুরুষ" in content
    assert "নারী" in content
    assert "বলতে চাই না" in content
    assert "kioskPress" in content


def test_base_includes_still_there_overlay_and_local_vendors(db, client):
    content = client.get("/").content.decode()
    assert "Still there?" in content
    assert "js/vendor/htmx.min.js" in content
    assert "js/vendor/alpine.min.js" in content
    assert "js/kiosk.js" in content


def test_base_binds_kiosk_session_guard(db, client):
    content = client.get("/").content.decode()
    assert "kioskSession" in content
    assert "/experience/reset/" in content


def test_result_page_has_countdown_and_avatar(seeded, client, hx):
    start_and_profile(client, hx)
    for q_order in range(1, 7):
        question = seeded.questions.get(order=q_order)
        option = question.options.get(order=1)
        client.post(
            "/experience/answer/", {"answer_id": option.id}, **hx
        )
    response = client.post("/experience/complete/", **hx)
    content = response.content.decode()
    assert "kioskCountdown" in content
    assert "avatars/beach_lover/neutral.svg" in content
    assert "BEACH LOVER" in content
    assert "সেকেন্ড পরে স্বয়ংক্রিয়ভাবে রিসেট হবে" in content


def seeded_avatar_slugs():
    return [
        "heritage_hunter",
        "beach_lover",
        "adventure_seeker",
        "nature_explorer",
        "urban_explorer",
        "culture_connector",
    ]
