from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone

from apps.analytics import selectors, services
from apps.experience.models import (
    AgeGroup,
    AssessmentAnswer,
    AssessmentPersonaScore,
    AssessmentSession,
    AssessmentStatus,
    Persona,
)

LOCAL_TZ = ZoneInfo(settings.TIME_ZONE)


def local_dt(year, month, day, hour):
    return datetime(year, month, day, hour, tzinfo=LOCAL_TZ)


@pytest.fixture
def data(seeded):
    personas = {p.slug: p for p in Persona.objects.all()}
    groups = {g.name: g for g in AgeGroup.objects.all()}

    def make(status, slug, age_group, gender, started, duration=60, kiosk="KIOSK-01"):
        session = AssessmentSession.objects.create(
            questionnaire_version=seeded,
            status=status,
            primary_persona=personas[slug] if slug else None,
            secondary_persona=None,
            age_group=groups[age_group] if age_group else None,
            gender=gender,
            started_at=started,
            completed_at=started + timedelta(seconds=duration) if status == AssessmentStatus.COMPLETED else None,
            duration_seconds=duration if status == AssessmentStatus.COMPLETED else None,
            kiosk_identifier=kiosk,
        )
        return session

    d = local_dt(2026, 9, 22, 10)  # 10:00 local
    make(AssessmentStatus.COMPLETED, "beach_lover", "Young Adult", "male", d, 70)
    make(AssessmentStatus.COMPLETED, "beach_lover", "Teen", "female", d + timedelta(hours=1), 55)
    make(AssessmentStatus.COMPLETED, "heritage_hunter", "Adult", "male", d + timedelta(hours=2), 80, kiosk="KIOSK-02")
    make(AssessmentStatus.COMPLETED, "heritage_hunter", "Senior", "female", d + timedelta(hours=2, minutes=30), 65)
    make(AssessmentStatus.ABANDONED, None, None, None, d + timedelta(hours=3))
    make(AssessmentStatus.TIMED_OUT, None, None, None, d + timedelta(hours=4))
    return d


def test_totals_and_completion_rate(data):
    assert selectors.get_total_started() == 6
    assert selectors.get_total_completed() == 4
    assert selectors.get_completion_rate() == round(4 / 6 * 100, 1)


def test_average_completion_time(data):
    assert selectors.get_average_completion_time() == round((70 + 55 + 80 + 65) / 4, 2)


def test_persona_distribution(data):
    rows = {row["primary_persona__slug"]: row["count"] for row in selectors.get_persona_distribution()}
    assert rows == {"beach_lover": 2, "heritage_hunter": 2}


def test_hourly_traffic_groups_in_local_time(data):
    rows = {row["hour"].hour: row["count"] for row in selectors.get_hourly_traffic(data.date())}
    assert rows == {10: 1, 11: 1, 12: 2, 13: 1, 14: 1}


def test_hourly_traffic_other_day_is_empty(data):
    assert list(selectors.get_hourly_traffic(data.date() + timedelta(days=1))) == []


def test_age_distribution(data):
    rows = {row["age_group__name"]: row["count"] for row in selectors.get_age_distribution()}
    assert rows == {"Teen": 1, "Young Adult": 1, "Adult": 1, "Senior": 1}


def test_gender_distribution(data):
    rows = {row["gender"]: row["count"] for row in selectors.get_gender_distribution()}
    assert rows == {"male": 2, "female": 2}


def test_traffic_by_kiosk(data):
    rows = {row["kiosk_identifier"]: row["count"] for row in selectors.get_traffic_by_kiosk()}
    assert rows == {"KIOSK-01": 5, "KIOSK-02": 1}


def test_abandonment_counts(data):
    rows = {row["status"]: row["count"] for row in selectors.get_abandonment_counts()}
    assert rows == {AssessmentStatus.COMPLETED: 4, AssessmentStatus.ABANDONED: 1, AssessmentStatus.TIMED_OUT: 1}


def test_answer_distribution_counts(data):
    version = AssessmentSession.objects.first().questionnaire_version
    rows = {row["order"]: row for row in selectors.get_answer_distribution(version)}
    assert rows[1]["total"] == 0  # no AssessmentAnswer rows created in this fixture
    assert all(count == 0 for count in rows[1]["counts"].values())


def test_answer_distribution_with_answers(seeded, data):
    question = seeded.questions.get(order=1)
    option_a = question.options.get(order=1)
    option_b = question.options.get(order=2)
    for assessment, option in [
        (AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED)[0], option_a),
        (AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED)[1], option_a),
        (AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED)[2], option_b),
    ]:
        AssessmentAnswer.objects.create(assessment=assessment, question=question, answer_option=option)
    rows = {row["order"]: row for row in selectors.get_answer_distribution(seeded)}
    assert rows[1]["total"] == 3
    assert rows[1]["counts"][option_a.text_bn] == 2
    assert rows[1]["counts"][option_b.text_bn] == 1
    first = next(iter(rows[1]["counts"]))
    assert first == option_a.text_bn


def test_companion_distribution_empty_when_none(data):
    assert list(selectors.get_companion_distribution()) == []


def test_csv_exports_produce_payload(data):
    payload = services.assessment_summary()
    assert "session_uuid" in payload
    assert "KIOSK-02" in payload
    payload = services.persona_distribution()
    assert "persona,completed" in payload
    payload = services.answer_responses()
    assert "question_order" in payload
    payload = services.hourly_traffic(data.date())
    assert "hour,started" in payload


@pytest.fixture
def staff_client(db):
    user = User.objects.create_superuser("staff", "staff@example.com", "pass12345")
    client = Client()
    client.force_login(user)
    return client


def test_dashboard_requires_staff(client):
    response = client.get("/dashboard/")
    assert response.status_code == 302
    assert "/admin/login/" in response["Location"]


def test_dashboard_renders_for_staff(staff_client, data):
    response = staff_client.get("/dashboard/")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Analytics Dashboard" in content
    assert "personaChart" in content
    assert "hourlyChart" in content


def test_export_requires_staff(client):
    response = client.get("/dashboard/export/assessment_summary/")
    assert response.status_code == 302


def test_export_returns_csv_for_staff(staff_client, data):
    response = staff_client.get("/dashboard/export/assessment_summary/")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert "attachment" in response["Content-Disposition"]


def test_unknown_export_404(staff_client, data):
    assert staff_client.get("/dashboard/export/nope/").status_code == 404


def test_empty_dashboard_is_safe(staff_client):
    response = staff_client.get("/dashboard/")
    assert response.status_code == 200
    assert selectors.get_completion_rate() == 0.0
