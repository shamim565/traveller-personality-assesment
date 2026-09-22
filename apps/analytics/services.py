"""CSV export builders for authorized staff (docs/analytics.md §4)."""

import csv
import io

from apps.analytics import selectors
from apps.experience.models import AssessmentSession
from apps.experience.selectors import questionnaire as questionnaire_selectors


def _csv_response(filename, header, rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue()


def assessment_summary():
    rows = []
    for session in AssessmentSession.objects.select_related(
        "questionnaire_version",
        "age_group",
        "primary_persona",
        "secondary_persona",
    ).order_by("started_at"):
        rows.append(
            [
                session.session_uuid,
                session.kiosk_identifier,
                session.questionnaire_version.version if session.questionnaire_version else "",
                session.status,
                session.started_at.isoformat(),
                session.completed_at.isoformat() if session.completed_at else "",
                session.duration_seconds or "",
                session.age_group.name if session.age_group else "",
                session.gender or "",
                session.primary_persona.slug if session.primary_persona else "",
                session.secondary_persona.slug if session.secondary_persona else "",
                session.companion_trait or "",
            ]
        )
    return _csv_response(
        "assessment_summary.csv",
        [
            "session_uuid",
            "kiosk",
            "version",
            "status",
            "started_at",
            "completed_at",
            "duration_seconds",
            "age_group",
            "gender",
            "primary_persona",
            "secondary_persona",
            "companion_trait",
        ],
        rows,
    )


def persona_distribution():
    rows = [
        [row["primary_persona__name"], row["count"]]
        for row in selectors.get_persona_distribution()
    ]
    return _csv_response("persona_distribution.csv", ["persona", "completed"], rows)


def answer_responses():
    version = questionnaire_selectors.get_active_version()
    rows = []
    if version is not None:
        for question in selectors.get_answer_distribution(version):
            for text_bn, count in question["counts"].items():
                total = question["total"] or 1
                rows.append(
                    [
                        question["order"],
                        question["text_bn"],
                        text_bn,
                        count,
                        round(count / total * 100, 1),
                    ]
                )
    return _csv_response(
        "answer_responses.csv",
        ["question_order", "question_bn", "answer_bn", "count", "percentage"],
        rows,
    )


def hourly_traffic(date):
    rows = [
        [row["hour"].isoformat(), row["count"]]
        for row in selectors.get_hourly_traffic(date=date)
    ]
    return _csv_response("hourly_traffic.csv", ["hour", "started"], rows)
