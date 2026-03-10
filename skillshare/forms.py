from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms  # type: ignore

from .models import Schedule, Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category"]


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["scheduled_at", "skill"]
        widgets = {"scheduled_at": DatePickerInput(options={"format": "DD/MM/YYYY"})}
