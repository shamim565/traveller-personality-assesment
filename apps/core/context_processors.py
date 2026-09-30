from django.conf import settings


def kiosk_settings(request):
    return {
        "K_MIN_AGE": settings.EXPERIENCE_MIN_AGE,
        "K_MAX_AGE": settings.EXPERIENCE_MAX_AGE,
        "K_STILL_THERE_SECONDS": settings.EXPERIENCE_STILL_THERE_SECONDS,
        "K_STILL_THERE_GRACE_SECONDS": settings.EXPERIENCE_STILL_THERE_GRACE_SECONDS,
        "K_ANALYZING_MS": settings.EXPERIENCE_ANALYZING_MS,
    }
