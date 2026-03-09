from django.urls import path  # type: ignore

from .views import HomeListView, SkillListView

app_name = "skillshare"
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
]
