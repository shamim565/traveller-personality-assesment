import re
import time

import pytest
from playwright.sync_api import expect

from apps.experience.models import (
    AgeGroup,
    AssessmentSession,
    AssessmentStatus,
    Persona,
    PersonaAvatar,
)

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


def start_quiz(page):
    page.get_by_role("button", name="Discover My Travel Personality").click()
    page.locator('input[name="name"]').fill("Sazid")
    page.locator('input[name="age"]').fill("25")
    page.locator('label:has(input[value="male"])').click()
    page.get_by_role("button", name="কুইজ শুরু করুন").click()
    page.get_by_text("প্রশ্ন 1 / 6").wait_for(timeout=5000)


def answer_first(page):
    page.locator("button[hx-post='/experience/answer/']").first.click()


def complete_flow(page):
    start_quiz(page)
    for _ in range(6):
        answer_first(page)
        page.wait_for_timeout(250)
    page.get_by_text("BEACH LOVER", exact=False).wait_for(timeout=10000)


def test_happy_path_and_restart_clears_data(kiosk_page, seeded):
    page = kiosk_page
    expect(page.get_by_text("DETECT YOUR")).to_be_visible()
    expect(page.locator('header img[alt="Organizer"]')).to_be_visible()
    complete_flow(page)
    expect(page.get_by_text("Sazid,", exact=False)).to_be_visible()
    expect(page.locator('img[alt$="avatar"]')).to_be_visible()
    expect(page.locator('header img[alt="Organizer"]')).to_be_visible()

    page.get_by_role("button", name=re.compile("Start Again")).click()
    expect(page.get_by_text("DETECT YOUR")).to_be_visible()
    expect(page.locator('header img[alt="Organizer"]')).to_be_visible()

    page.get_by_role("button", name="Discover My Travel Personality").click()
    expect(page.locator('input[name="name"]')).to_be_visible()
    expect(page.locator('header img[alt="Organizer"]')).to_be_visible()
    assert page.locator('input[name="name"]').input_value() == ""
    assert "Sazid" not in page.content()


def test_abandon_via_reset_then_new_session(kiosk_page, seeded):
    page = kiosk_page
    start_quiz(page)
    answer_first(page)
    answer_first(page)
    assert AssessmentSession.objects.filter(status=AssessmentStatus.STARTED).count() == 1

    page.evaluate(
        "() => htmx.ajax('POST', '/experience/reset/', { target: '#experience', swap: 'innerHTML' })"
    )
    expect(page.get_by_text("DETECT YOUR")).to_be_visible()
    assert AssessmentSession.objects.filter(status=AssessmentStatus.ABANDONED).count() == 1

    start_quiz(page)
    for _ in range(6):
        page.locator("button[hx-post='/experience/answer/']").first.click()
        page.wait_for_timeout(250)
    page.get_by_text("BEACH LOVER", exact=False).wait_for(timeout=10000)
    assert AssessmentSession.objects.count() == 2
    assert AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED).count() == 1


def test_inactivity_timeout_shows_prompt_then_resets(settings, live_server, page, seeded):
    settings.EXPERIENCE_STILL_THERE_SECONDS = 3
    settings.EXPERIENCE_STILL_THERE_GRACE_SECONDS = 2
    page.goto(live_server.url)
    start_quiz(page)
    page.get_by_text("Still there?", exact=False).wait_for(timeout=8000)
    page.get_by_text("DETECT YOUR").wait_for(timeout=8000)
    assert AssessmentSession.objects.filter(status=AssessmentStatus.ABANDONED).count() == 1
    page.get_by_role("button", name="Discover My Travel Personality").click()
    assert page.locator('input[name="name"]').input_value() == ""


def test_refresh_resumes_at_same_question(kiosk_page, seeded):
    page = kiosk_page
    start_quiz(page)
    answer_first(page)
    answer_first(page)
    expected = seeded.questions.get(order=3).text_bn
    expect(page.get_by_text(expected)).to_be_visible()

    page.reload()
    expect(page.get_by_text(expected)).to_be_visible()
    expect(page.get_by_text("প্রশ্ন 3 / 6")).to_be_visible()


def test_double_tap_records_single_answer(kiosk_page, seeded):
    page = kiosk_page
    start_quiz(page)
    card = page.locator("button[hx-post='/experience/answer/']").first
    card.wait_for(state="visible")
    box = card.bounding_box()
    page.mouse.dblclick(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.get_by_text("প্রশ্ন 2 / 6").wait_for(timeout=6000)
    assert "Something went wrong" not in page.content()


def test_broken_avatar_falls_back_to_global(kiosk_page, seeded):
    persona = Persona.objects.get(slug="beach_lover")
    group = AgeGroup.objects.get(name="Young Adult")
    PersonaAvatar.objects.get_or_create(
        persona=persona,
        gender="male",
        age_group=group,
        defaults={"image": "avatars/beach_lover/missing-e2e.webp"},
    )
    page = kiosk_page
    complete_flow(page)
    avatar = page.locator('img[alt$="avatar"]')
    expect(avatar).to_have_attribute("src", re.compile(r"global-default\.svg"), timeout=8000)


def test_slow_server_answers_still_complete(kiosk_page, seeded):
    page = kiosk_page

    def slow_route(route):
        time.sleep(1.2)
        route.continue_()

    page.route("**/experience/answer/", slow_route)
    complete_flow(page)
    page.unroute("**/experience/answer/", slow_route)
    assert AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED).count() == 1


def test_double_completion_creates_single_record(kiosk_page, seeded):
    page = kiosk_page
    complete_flow(page)
    page.evaluate(
        """() => {
            htmx.ajax('POST', '/experience/complete/', { target: '#experience', swap: 'innerHTML' });
            htmx.ajax('POST', '/experience/complete/', { target: '#experience', swap: 'innerHTML' });
        }"""
    )
    page.wait_for_timeout(1500)
    assert AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED).count() == 1
    expect(page.get_by_text("BEACH LOVER", exact=False)).to_be_visible()


def test_stale_session_shows_friendly_recovery(kiosk_page, seeded):
    page = kiosk_page
    start_quiz(page)
    answer_first(page)
    page.get_by_text("প্রশ্ন 2 / 6").wait_for(timeout=6000)
    page.context.clear_cookies(name="sessionid")
    page.locator("button[hx-post='/experience/answer/']").first.click()
    page.get_by_text("Something went wrong.", exact=False).wait_for(timeout=6000)
    page.get_by_role("button", name=re.compile("Start Again")).click()
    expect(page.get_by_text("DETECT YOUR")).to_be_visible()
