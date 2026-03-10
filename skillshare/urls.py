from django.urls import path  # type: ignore

from .views import (
    HomeListView,
    ScheduleCreateView,
    SkillCreateView,
    SkillListView,
    schedule_matching_view,
    schedule_take_form,
)

app_name = "skillshare"
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
    path("skills/add", SkillCreateView.as_view(), name="skill_add"),
    path("schedules/add", ScheduleCreateView.as_view(), name="schedule_add"),
    path("schedules/<int:pk>/take", schedule_take_form, name="schedule_take"),
    path("schedules/matching", schedule_matching_view, name="schedule_matching"),
]
