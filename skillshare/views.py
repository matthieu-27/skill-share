from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from django.views.generic import ListView  # type: ignore
from django.views.generic.edit import CreateView  # type: ignore

from .forms import ScheduleForm, SkillForm
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
        return reverse("skillshare:skill_add")


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "skillshare/schedule_form.html"
    login_url = "/skillshare"
    redirect_field_name = "redirect_to"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["skill"].queryset = Skill.objects.filter(giver=self.request.user)
        return form

    def get_success_url(self) -> str:
        return reverse("skillshare:schedule_add")


class ScheduleTakeView(LoginRequiredMixin, CreateView):
    def post(
        self, request: HttpRequest, pk: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        schedule = get_object_or_404(Schedule, pk=pk)
        if not schedule.is_active and schedule.taker is None:
            schedule.taker = request.user
            schedule.is_active = True
            schedule.save()
        return redirect("skillshare:index")
