from django.views.generic import ListView  # type: ignore

from .models import Schedule


class HomePageView(ListView):
    model = Schedule
    template_name = "skillshare/index.html"
