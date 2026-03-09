from django.urls import path  # type: ignore

from .views import HomePageView

app_name = "skillshare"
urlpatterns = [path("", HomePageView.as_view(), name="index")]
