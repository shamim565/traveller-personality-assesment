from django.conf import settings
from django.test import Client


def test_health_endpoint_ok(db):
    response = Client().get("/health/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["db"] is True


def test_landing_renders():
    response = Client().get("/")
    assert response.status_code == 200


def test_kiosk_settings_defaults():
    assert settings.KIOSK_IDENTIFIER == "KIOSK-01"
    assert settings.EXPERIENCE_MIN_AGE == 10
    assert settings.EXPERIENCE_MAX_AGE == 100
    assert settings.EXPERIENCE_RESET_DELAY_SECONDS == 45
    assert settings.EXPERIENCE_STILL_THERE_SECONDS == 45
    assert settings.EXPERIENCE_STILL_THERE_GRACE_SECONDS == 10
    assert settings.EXPERIENCE_ANALYZING_MS == 1600


def test_domain_apps_installed():
    installed = settings.INSTALLED_APPS
    assert "apps.core" in installed
    assert "apps.experience" in installed
    assert "apps.analytics" in installed
