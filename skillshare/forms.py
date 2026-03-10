from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms  # type: ignore

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


class ConfirmForm(forms.Form):
    """
    Confirmation `Form` used to "take" a schedule.

    Has a boolean field with French translated label.
    """

    confirm = forms.BooleanField(
        label="Êtes vous sur de confirmer ce créneaux ?", required=True
    )
