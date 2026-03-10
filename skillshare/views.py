from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from django.views.generic import ListView  # type: ignore
from django.views.generic.edit import CreateView  # type: ignore

from .forms import SkillForm
from .models import Schedule, Skill


class HomeListView(ListView):
    model = Schedule
    template_name = "skillshare/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class SkillListView(ListView):
    model = Skill
    template_name = "skillshare/skill_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "skillshare/skill_form.html"
    login_url = "/skillshare"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        form.instance.giver = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("skillshare:skill_form")
