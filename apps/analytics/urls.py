from django.urls import path

from apps.analytics import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/export/<str:report>/", views.export, name="export"),
]
