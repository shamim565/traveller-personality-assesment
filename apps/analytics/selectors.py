"""Aggregate read queries for the analytics dashboard.

Everything is database-side aggregation; nothing pulls full rows into Python.
"""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Avg, Count
from django.db.models.functions import TruncHour

from apps.experience.models import (
    AnswerOption,
    AssessmentSession,
    AssessmentStatus,
    Question,
)

LOCAL_TZ = ZoneInfo(settings.TIME_ZONE)


def _completed():
    return AssessmentSession.objects.filter(status=AssessmentStatus.COMPLETED)


def get_total_started():
    return AssessmentSession.objects.count()


def get_total_completed():
    return _completed().count()


def get_completion_rate():
    started = get_total_started()
    if not started:
        return 0.0
    return round(get_total_completed() / started * 100, 1)


def get_average_completion_time():
    return _completed().aggregate(avg=Avg("duration_seconds"))["avg"]


def get_persona_distribution():
    return (
        _completed()
        .values("primary_persona__slug", "primary_persona__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )


def get_hourly_traffic(date=None):
    queryset = AssessmentSession.objects.all()
    if date is not None:
        start_local = datetime.combine(date, time.min, tzinfo=LOCAL_TZ)
        end_local = start_local + timedelta(days=1)
        queryset = queryset.filter(started_at__gte=start_local, started_at__lt=end_local)
    return (
        queryset.annotate(hour=TruncHour("started_at", tzinfo=LOCAL_TZ))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by("hour")
    )


def get_age_distribution():
    return (
        _completed()
        .values("age_group__name")
        .annotate(count=Count("id"))
        .order_by("age_group__name")
    )


def get_gender_distribution():
    return (
        _completed()
        .exclude(gender__isnull=True)
        .values("gender")
        .annotate(count=Count("id"))
        .order_by("gender")
    )


def get_answer_distribution(version):
    questions = Question.objects.filter(
        questionnaire_version=version, is_active=True
    ).order_by("order")
    rows = []
    for question in questions:
        counts = dict(
            AnswerOption.objects.filter(question=question, is_active=True)
            .annotate(count=Count("answers"))
            .order_by("-count")
            .values_list("text_bn", "count")
        )
        rows.append(
            {
                "order": question.order,
                "text_bn": question.text_bn,
                "counts": counts,
                "total": sum(counts.values()),
            }
        )
    return rows


def get_companion_distribution():
    return (
        _completed()
        .exclude(companion_trait__isnull=True)
        .values("companion_trait")
        .annotate(count=Count("id"))
        .order_by("-count")
    )


def get_traffic_by_kiosk():
    return (
        AssessmentSession.objects.values("kiosk_identifier")
        .annotate(count=Count("id"))
        .order_by("-count")
    )


def get_abandonment_counts():
    return (
        AssessmentSession.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
