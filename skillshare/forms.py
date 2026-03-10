from bootstrap_datepicker_plus.widgets import DatePickerInput  # type: ignore
from django import forms  # type: ignore
from django.utils import timezone  # type: ignore

from .models import Schedule, Skill


class SkillForm(forms.ModelForm):
    """
    Skill ModelForm handler, fields : `name` and `category`.

    Adds custom French translated labels.
    """

    class Meta:
        model = Skill
        fields = ["name", "category"]
        labels = {"name": "Compétence", "category": "Catégorie"}

    def clean_name(self):
        """
        Validate the name field to ensure it is not empty and has a minimum length.

        Raises:
            forms.ValidationError: If the name is empty or too short.
        """
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Le nom de la compétence est obligatoire.")
        if len(name) < 3:
            raise forms.ValidationError(
                "Le nom de la compétence doit contenir au moins 3 caractères."
            )
        return name


class ScheduleForm(forms.ModelForm):
    """
    Schedule ModelForm handler, fields: `scheduled_at`, `skill`, `activity_description`, `is_request`.

    Adds custom French translated labels.
    """

    class Meta:
        model = Schedule
        fields = ["scheduled_at", "skill", "activity_description", "is_request"]
        widgets = {"scheduled_at": DatePickerInput(options={"format": "DD/MM/YYYY"})}
        labels = {
            "scheduled_at": "Jour désiré",
            "skill": "Compétences",
            "activity_description": "Description de la demande",
            "is_request": "Demande d'aide",
        }

    def clean_scheduled_at(self):
        """
        Validate the scheduled_at field to ensure it is not in the past.

        Raises:
            forms.ValidationError: If the scheduled_at is in the past.
        """
        scheduled_at = self.cleaned_data.get("scheduled_at")
        if scheduled_at and scheduled_at < timezone.now():
            raise forms.ValidationError("La date ne peut pas être dans le passé.")
        return scheduled_at


class ConfirmForm(forms.Form):
    """
    Confirmation `Form` used to "take" a schedule.

    Has a boolean field with French translated label.
    """

    confirm = forms.BooleanField(
        label="Êtes vous sur de confirmer ce créneaux ?", required=True
    )
