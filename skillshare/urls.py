from django.urls import path  # type: ignore

from .views import HomeListView, ScheduleCreateView, SkillCreateView, SkillListView

app_name = "skillshare"
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
    path("skills/add", SkillCreateView.as_view(), name="skill_add"),
    path("schedules/add", ScheduleCreateView.as_view(), name="schedule_add"),
]
