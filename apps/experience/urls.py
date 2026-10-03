from django.urls import path

from apps.experience import views

app_name = "experience"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("experience/language/", views.set_language, name="set_language"),
    path("experience/start/", views.start, name="start"),
    path("experience/profile/", views.profile, name="profile"),
    path("experience/answer/", views.answer, name="answer"),
    path("experience/complete/", views.complete, name="complete"),
    path(
        "experience/result/<uuid:session_uuid>/image/",
        views.result_image,
        name="result_image",
    ),
    path("experience/reset/", views.reset, name="reset"),
]
