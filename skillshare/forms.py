from bootstrap_datepicker_plus.widgets import DatePickerInput  # type: ignore
from django import forms  # type: ignore
from django.utils import timezone  # type: ignore

from .models import Schedule


class ScheduleForm(forms.ModelForm):
    """
    Schedule ModelForm handler, fields: `scheduled_at`, `skill`, `activity_description`.

    Adds custom French translated labels.
    """

    class Meta:
        model = Schedule
        fields = ["scheduled_at", "skill", "activity_description"]
        widgets = {"scheduled_at": DatePickerInput(options={"format": "DD/MM/YYYY"})}
        labels = {
            "scheduled_at": "Jour désiré",
            "skill": "Compétences",
            "activity_description": "Description de la demande",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ScheduleForm, self).__init__(*args, **kwargs)

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

    def save(self, commit=True):
        """
        Save the form and set is_request based on whether the user owns the skill.
        """
        instance = super().save(commit=False)
        if self.user and self.cleaned_data.get("skill"):
            instance.is_request = not self.user.skill_set.filter(
                id=self.cleaned_data["skill"].id
            ).exists()
        if commit:
            instance.save()
        return instance


class ConfirmForm(forms.Form):
    """
    Confirmation `Form` used to "take" a schedule.

    Has a boolean field with French translated label.
    """

    confirm = forms.BooleanField(
        label="Êtes vous sur de confirmer ce créneaux ?", required=True
    )
