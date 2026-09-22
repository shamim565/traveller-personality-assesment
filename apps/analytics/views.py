from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET

from apps.analytics import selectors, services
from apps.experience.selectors import questionnaire as questionnaire_selectors

EXPORTS = {
    "assessment_summary": services.assessment_summary,
    "persona_distribution": services.persona_distribution,
    "answer_responses": services.answer_responses,
    "hourly_traffic": lambda request: services.hourly_traffic(_selected_date(request)),
}


def _selected_date(request):
    raw = request.GET.get("date", "")
    if raw:
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            pass
    return timezone.localdate()


def _chart_series(rows, key, label_key):
    labels = [row[label_key] for row in rows]
    values = [row[key] for row in rows]
    return {"labels": labels, "values": values}


def _hourly_series(rows):
    counts = {row["hour"].hour: row["count"] for row in rows}
    labels = [f"{hour:02d}:00" for hour in range(24)]
    values = [counts.get(hour, 0) for hour in range(24)]
    return {"labels": labels, "values": values}


@require_GET
@staff_member_required
def dashboard(request):
    selected_date = _selected_date(request)
    version = questionnaire_selectors.get_active_version()
    avg_duration = selectors.get_average_completion_time()
    context = {
        "selected_date": selected_date.isoformat(),
        "total_started": selectors.get_total_started(),
        "total_completed": selectors.get_total_completed(),
        "completion_rate": selectors.get_completion_rate(),
        "avg_duration": int(avg_duration) if avg_duration else None,
        "persona_chart": _chart_series(
            selectors.get_persona_distribution(), "count", "primary_persona__name"
        ),
        "hourly_chart": _hourly_series(selectors.get_hourly_traffic(selected_date)),
        "age_chart": _chart_series(selectors.get_age_distribution(), "count", "age_group__name"),
        "gender_chart": _chart_series(selectors.get_gender_distribution(), "count", "gender"),
        "companion_rows": selectors.get_companion_distribution(),
        "kiosk_rows": selectors.get_traffic_by_kiosk(),
        "abandonment_rows": selectors.get_abandonment_counts(),
        "answer_rows": selectors.get_answer_distribution(version) if version else [],
    }
    return render(request, "dashboard/index.html", context)


@require_GET
@staff_member_required
def export(request, report):
    if report not in EXPORTS:
        return HttpResponse("Unknown report", status=404)
    payload = EXPORTS[report](request) if report == "hourly_traffic" else EXPORTS[report]()
    response = HttpResponse(payload, content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{report}.csv"'
    return response
