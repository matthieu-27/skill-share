from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from django.urls import path  # type: ignore

from . import views

app_name = "skillshare"
urlpatterns = [
    path("", views.HomeListView.as_view(), name="index"),
    path("skills/", views.SkillListView.as_view(), name="skill_list"),
    path("schedules/add", views.ScheduleCreateView.as_view(), name="schedule_add"),
    path(
        "schedules/<int:pk>/take",
        views.ScheduleTakeFormView.as_view(),
        name="schedule_take",
    ),
    path(
        "schedules/matching",
        views.ScheduleMatchingView.as_view(),
        name="schedule_matching",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
