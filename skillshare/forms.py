from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms  # type: ignore

from .models import Schedule, Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category"]
        labels = {"name": "Compétence", "category": "Catégorie"}


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["scheduled_at", "skill", "is_request"]
        widgets = {"scheduled_at": DatePickerInput(options={"format": "DD/MM/YYYY"})}
        labels = {
            "scheduled_at": "Jour désiré",
            "skill": "Compétences",
            "is_request": "Demande d'aide",
        }
