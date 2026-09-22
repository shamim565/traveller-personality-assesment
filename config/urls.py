"""Root URL configuration.

Public kiosk routes live under apps.experience.urls ("/"),
the staff dashboard under apps.analytics.urls ("/dashboard/").
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.experience.urls")),
    path("", include("apps.analytics.urls")),
]
