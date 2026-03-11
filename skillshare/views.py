from typing import Any

from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.shortcuts import render  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from django.views.generic import ListView  # type: ignore
from django.views.generic.edit import CreateView  # type: ignore

from .forms import ConfirmForm, ScheduleForm, SkillForm
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "Vous devez être connecté pour accéder à cette page."
            )
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, "Vous devez être connecté pour accéder à cette page."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Votre demande a bien été enregistrée.")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("skillshare:index")


def schedule_take_form(request, pk):
    """
    Form that sets the taker of a Schedule,
    Checks if the Schedule creator is the request maker, if so redirect.

    Otherwise saves the interested user for the selected Schedule
    """
    schedule = Schedule.objects.get(pk=pk)
    if schedule.user == request.user:
        return HttpResponseRedirect("/skillshare")
    if request.method == "GET":
        form = ConfirmForm()
        return render(
            request,
            "skillshare/schedule_take.html",
            {"form": form, "schedule": schedule},
        )
    if request.method == "POST":
        if schedule.taker is None:
            schedule.taker = request.user
            schedule.save()
        return HttpResponseRedirect("/skillshare")
    return render(
        request, "skillshare/schedule_take.html", {"form": form, "schedule": schedule}
    )


@login_required(login_url="/")
def schedule_matching_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour accéder à cette page.")
    user_skills = request.user.skill_set.all()
    matching_schedules = Schedule.objects.filter(skill__in=user_skills).exclude(
        user=request.user
    )
    return render(
        request, "skillshare/schedule_matching.html", {"matchs": matching_schedules}
    )
