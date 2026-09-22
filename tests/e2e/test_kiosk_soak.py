import pytest
from playwright.sync_api import expect

from apps.experience.models import AssessmentSession, AssessmentStatus

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]

PATTERNS = [
    ("BEACH LOVER", [1, 1, 1, 1, 1, 1]),
    ("HERITAGE HUNTER", [2, 3, 2, 2, 1, 2]),
    ("ADVENTURE SEEKER", [3, 2, 3, 3, 1, 3]),
    ("NATURE EXPLORER", [3, 2, 1, 1, 1, 1]),
    ("URBAN EXPLORER", [5, 5, 5, 5, 1, 5]),
    ("CULTURE CONNECTOR", [4, 4, 4, 4, 1, 4]),
]

TOTAL_RUNS = 100


def test_soak_100_consecutive_assessments(kiosk_page, seeded):
    page = kiosk_page
    option_texts = {
        question.order: {option.order: option.text_bn for option in question.options.all()}
        for question in seeded.questions.all()
    }

    for run in range(TOTAL_RUNS):
        persona_name, pattern = PATTERNS[run % len(PATTERNS)]

        page.get_by_role("button", name="Discover My Travel Personality").click()
        page.locator('input[name="name"]').fill(f"Visitor{run}")
        page.locator('input[name="age"]').fill(str(10 + (run % 90)))
        page.locator('label:has(input[value="male"])').click()
        page.get_by_role("button", name="কুইজ শুরু করুন").click()
        page.wait_for_timeout(150)

        for question_order, option_order in enumerate(pattern, start=1):
            text = option_texts[question_order][option_order]
            page.get_by_role("button", name=text, exact=True).click()
            page.wait_for_timeout(120)

        expect(page.get_by_text(persona_name, exact=False)).to_be_visible(timeout=10000)
        assert f"Visitor{run}" in page.content()
        page.get_by_role("button", name="Start Again — আবার শুরু করুন").click()
        expect(page.get_by_text("DETECT YOUR")).to_be_visible()
        assert page.locator('input[name="name"]') is not None
        assert f"Visitor{run}" not in page.content()

        if run % 20 == 19:
            completed = AssessmentSession.objects.filter(
                status=AssessmentStatus.COMPLETED
            ).count()
            assert completed == run + 1, f"completed drift at run {run}"

    assert AssessmentSession.objects.count() == TOTAL_RUNS
    assert AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED).count() == TOTAL_RUNS
    assert not AssessmentSession.objects.filter(status=AssessmentStatus.ABANDONED).exists()
    assert page.locator("#experience").count() == 1
