import re

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


def test_idle_has_branding_and_no_avatars(seeded):
    content = idle_page()
    assert "branding/kv/kv-placeholder.webp" in content
    assert "branding/logos/govt.png" in content
    assert "branding/logos/BG-tourism-board.png" in content
    assert "world-tourism-day/world-tourism-day-logo.png" in content
    assert "#WorldTourismDay2026" in content
    assert "neutral.svg" not in content
    assert "global-default.svg" not in content


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


def header_paths(content):
    return all(
        path in content
        for path in [
            "branding/logos/govt.png",
            "world-tourism-day/world-tourism-day-logo.png",
            "branding/logos/BG-tourism-board.png",
        ]
    )


def test_header_visible_on_all_kiosk_pages(seeded, client, hx):
    assert header_paths(client.get("/").content.decode())

    client.post("/experience/start/", **hx)
    assert header_paths(client.get("/").content.decode())

    client.post("/experience/profile/", PROFILE, **hx)
    assert header_paths(client.get("/").content.decode())

    for question in seeded.questions.order_by("order"):
        option = question.options.filter(is_active=True).first()
        client.post("/experience/answer/", {"answer_id": option.id}, **hx)
    client.post("/experience/complete/", **hx)
    assert header_paths(client.get("/").content.decode())


def test_background_present_on_all_kiosk_pages(seeded, client, hx):
    assert "branding/kv/kv-placeholder.webp" in client.get("/").content.decode()

    client.post("/experience/start/", **hx)
    assert "backgrounds/profile.webp" in client.get("/").content.decode()

    client.post("/experience/profile/", PROFILE, **hx)
    assert "backgrounds/q1.webp" in client.get("/").content.decode()

    for question in seeded.questions.order_by("order"):
        option = question.options.filter(is_active=True).first()
        client.post("/experience/answer/", {"answer_id": option.id}, **hx)
    client.post("/experience/complete/", **hx)
    assert "backgrounds/result.webp" in client.get("/").content.decode()


def test_each_question_has_its_own_background(seeded, client, hx):
    client.post("/experience/start/", **hx)
    response = client.post("/experience/profile/", PROFILE, **hx)
    assert "backgrounds/q1.webp" in response.content.decode()

    for question in seeded.questions.order_by("order"):
        option = question.options.filter(is_active=True).first()
        response = client.post("/experience/answer/", {"answer_id": option.id}, **hx)
        next_order = question.order + 1
        if next_order <= 6:
            expected = f"backgrounds/q{next_order}.webp"
            assert expected in response.content.decode(), f"expected {expected} after Q{question.order}"
            assert "hx-swap-oob" in response.content.decode()
        else:
            assert "backgrounds/analyzing.webp" in response.content.decode()

    response = client.post("/experience/complete/", **hx)
    assert "backgrounds/result.webp" in response.content.decode()


def test_reset_restores_kv_background(seeded, client, hx):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for question in seeded.questions.order_by("order"):
        option = question.options.filter(is_active=True).first()
        client.post("/experience/answer/", {"answer_id": option.id}, **hx)
    client.post("/experience/complete/", **hx)
    response = client.post("/experience/reset/", **hx)
    assert "branding/kv/kv-placeholder.webp" in response.content.decode()


def test_refresh_shows_current_question_background(seeded, client, hx):
    client.post("/experience/start/", **hx)
    client.post("/experience/profile/", PROFILE, **hx)
    for order in (1, 2):
        question = seeded.questions.get(order=order)
        option = question.options.filter(is_active=True).first()
        client.post("/experience/answer/", {"answer_id": option.id}, **hx)
    content = client.get("/").content.decode()
    assert "backgrounds/q3.webp" in content


def test_compact_header_has_no_background_band(seeded, client, hx):
    client.post("/experience/start/", **hx)
    content = client.get("/").content.decode()
    header_tags = re.findall(r"<header[^>]*>", content)
    assert header_tags, "header not found"
    for tag in header_tags:
        assert "bg-brand-night" not in tag
        assert "backdrop-blur" not in tag


def test_result_page_has_avatar_and_manual_restart(seeded, client, hx):
    start_and_profile(client, hx)
    for q_order in range(1, 7):
        question = seeded.questions.get(order=q_order)
        option = question.options.get(order=1)
        client.post(
            "/experience/answer/", {"answer_id": option.id}, **hx
        )
    response = client.post("/experience/complete/", **hx)
    content = response.content.decode()
    assert "kioskCountdown" not in content
    assert "avatars/beach_lover/male-young_adult.webp" in content
    assert "BEACH LOVER" in content
    assert "/experience/reset/" in content
    assert "data:image/png;base64" in content
    assert "Scan to download your result image" in content
