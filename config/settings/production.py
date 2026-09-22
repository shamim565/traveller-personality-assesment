"""Production settings: PostgreSQL, hardened security, static collection.

All values come from environment variables. Intended to run behind nginx
(which terminates TLS) inside Docker (see docs/deployment.md).
"""

from .base import *  # noqa: F401,F403

DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1800  # 30 minutes; kiosk flow resets explicitly

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 0  # enable once TLS termination policy is confirmed

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host != "*"
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
