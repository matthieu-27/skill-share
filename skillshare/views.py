from typing import Any

from django.utils import timezone  # type: ignore
from django.views.generic import ListView  # type: ignore

from .models import Schedule


class HomePageView(ListView):
    model = Schedule
    template_name = "skillshare/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
