from typing import Any

from django.contrib import messages  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone
from django.views.generic import ListView  # type: ignore
from django.views.generic.edit import CreateView, FormView  # type: ignore

from .forms import ConfirmForm, ScheduleForm
from .models import Schedule, Skill


class HomeListView(ListView):
    """
    View that displays a list of schedules.
    """

    model = Schedule
    template_name = "skillshare/index.html"
    paginate_by = 5  # Nombre de créneaux par page
    # order par date de création du plus récent au ancien
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        """
        Function used to add the current time to the context.

        Returns:
            dict: The context with the current time added.
        """
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class SkillListView(ListView):
    """
    View that displays a list of skills grouped by category.
    """

    model = Skill
    template_name = "skillshare/skill_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Function used to group skills by category and add them to the context.
        """
        context = super().get_context_data(**kwargs)
        # Regrouper les compétences par catégorie en utilisant object_list
        categories_dict: dict[Any, Any] = {}
        for skill in context["object_list"]:
            if skill.category not in categories_dict:
                categories_dict[skill.category] = []
            categories_dict[skill.category].append(skill)
        context["categories"] = categories_dict.items()
        return context


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    """
    Schedule creation view, allows users to create a new schedule for a skill.

    Uses LoginRequiredMixin to ensure the user is authenticated.

    Uses CreateView to handle the form submission.
    """

    model = Schedule
    form_class = ScheduleForm
    template_name = "skillshare/schedule_form.html"
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

    def get_form_kwargs(self):
        """
        Function used to pass the user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Function used to save the form and display a success message.
        """
        form.instance.user = self.request.user
        messages.success(self.request, "Votre demande a bien été enregistrée.")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Function used to redirect the user to the home page after the form is submitted.
        """
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
        """
        Handles the form submission. If the schedule is available, the user is assigned as the taker.

        Redirects to the home page after the operation.
        """
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
        """
        Function used to get the schedules matching the user's skills.
        """
        # Accéder aux compétences de l'utilisateur via la relation ManyToMany
        user_skills = self.request.user.skills.all()
        return Schedule.objects.filter(skill__in=user_skills).exclude(
            giver=self.request.user
        )

    def get_context_data(self, **kwargs):
        """
        Function used to add the matching schedules to the context.
        """
        context = super().get_context_data(**kwargs)
        context["matchs"] = self.get_queryset()
        return context
