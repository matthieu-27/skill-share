from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from django.urls import path  # type: ignore

from .views import (
    HomeListView,
    ScheduleCreateView,
    ScheduleMatchingView,
    ScheduleTakeFormView,
    SkillListView,
)

app_name = "skillshare"
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
    path("schedules/add", ScheduleCreateView.as_view(), name="schedule_add"),
    path(
        "schedules/<int:pk>/take", ScheduleTakeFormView.as_view(), name="schedule_take"
    ),
    path(
        "schedules/matching", ScheduleMatchingView.as_view(), name="schedule_matching"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
