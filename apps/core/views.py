from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def health(request):
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_ok = False
    return JsonResponse({"status": "ok" if db_ok else "degraded", "db": db_ok})


def landing(request):
    return render(request, "core/bootstrap.html")
