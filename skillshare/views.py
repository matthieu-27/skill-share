from typing import Any

from django.contrib import messages  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone
from django.views.generic import ListView  # type: ignore
from django.views.generic.edit import CreateView, FormView  # type: ignore

from .forms import ConfirmForm, ScheduleForm, SkillForm
from .models import Schedule, Skill


class HomeListView(ListView):
    model = Schedule
    template_name = "skillshare/index.html"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class SkillListView(ListView):
    model = Skill
    template_name = "skillshare/skill_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Regrouper les compétences par catégorie en utilisant object_list
        categories_dict: dict[Any, Any] = {}
        for skill in context["object_list"]:
            if skill.category not in categories_dict:
                categories_dict[skill.category] = []
            categories_dict[skill.category].append(skill)
        context["categories"] = categories_dict.items()
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


class ScheduleTakeFormView(LoginRequiredMixin, FormView):
    """
    View that sets the taker of a Schedule,
    Checks if the Schedule creator is the request maker, if so redirect.

    Otherwise saves the interested user for the selected Schedule
    """

    form_class = ConfirmForm
    template_name = "skillshare/schedule_take.html"
    login_url = "/skillshare"
    redirect_field_name = "redirect_to"

    def dispatch(self, request, *args, **kwargs):
        """
        Function used to check if the user is authenticated.

        Displays an error message if the user is not authenticated.
        """
        if not request.user.is_authenticated:
            messages.error(
                request, "Vous devez être connecté pour accéder à cette page."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Schedule object getter.
        """
        return Schedule.objects.get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        """
        Checks if the user is the owner of the schedule.

        Redirects to the home page if the user is the owner.
        """
        schedule = self.get_object()
        if schedule.user == request.user:
            messages.error(request, "Vous ne pouvez pas prendre votre propre créneau.")
            return HttpResponseRedirect("/skillshare")
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(form=form, schedule=schedule)
        )

    def post(self, request, *args, **kwargs):
        schedule = self.get_object()
        if schedule.taker is None:
            schedule.taker = request.user
            schedule.save()
        messages.success(self.request, "Le créneau a été pris avec succès.")
        return HttpResponseRedirect("/skillshare")


class ScheduleMatchingView(LoginRequiredMixin, ListView):
    """
    View that displays schedules matching the user's skills.
    """

    model = Schedule
    template_name = "skillshare/schedule_matching.html"
    login_url = "/skillshare"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        user_skills = self.request.user.skill_set.all()
        return Schedule.objects.filter(skill__in=user_skills).exclude(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["matchs"] = self.get_queryset()
        return context
