import time

import pytest
from playwright.sync_api import expect

from apps.experience.models import Question
from apps.experience.services.scoring import calculate_travel_persona

pytestmark = pytest.mark.django_db


def all_option_objects(seeded, pattern):
    options = []
    for question_order, option_order in pattern:
        question = Question.objects.get(questionnaire_version=seeded, order=question_order)
        options.append(question.options.get(order=option_order))
    return options


def test_scoring_speed_under_150ms(seeded):
    answers = all_option_objects(seeded, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)])
    calculate_travel_persona(answers)  # warm caches
    runs = 500
    start = time.perf_counter()
    for _ in range(runs):
        calculate_travel_persona(answers)
    elapsed = time.perf_counter() - start
    average_ms = elapsed / runs * 1000
    assert average_ms < 150, f"scoring too slow: {average_ms:.1f}ms average"


def test_scoring_absolute_worst_case(seeded):
    answers = all_option_objects(seeded, [(1, 3), (2, 2), (3, 3), (4, 3), (5, 1), (6, 3)])
    start = time.perf_counter()
    result = calculate_travel_persona(answers)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert result.primary == "adventure_seeker"
    assert elapsed_ms < 200


@pytest.mark.e2e
def test_kiosk_page_weight_and_no_chartjs(live_server, page):
    sizes = []
    chart_requests = []

    def on_response(response):
        if "chart" in response.url:
            chart_requests.append(response.url)
        length = response.headers.get("content-length")
        if length:
            sizes.append(int(length))

    page.on("response", on_response)
    page.goto(live_server.url, wait_until="load")
    total_bytes = sum(sizes)
    # Per-page campaign photography (idle.webp ~235KB + logos) replaced the
    # placeholder SVGs; ~465KB keeps the LAN kiosk load well under 1s.
    assert total_bytes < 600_000, f"kiosk page too heavy: {total_bytes} bytes"
    assert chart_requests == []


@pytest.mark.e2e
def test_question_transition_is_fast(live_server, page, seeded):
    page.goto(live_server.url, wait_until="load")
    page.get_by_role("button", name="Discover My Travel Personality").click()
    start = time.perf_counter()
    expect(page.locator('input[name="name"]')).to_be_visible(timeout=3000)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 1000, f"start transition too slow: {elapsed_ms:.0f}ms"
