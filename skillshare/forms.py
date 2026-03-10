from django import forms  # type: ignore

from .models import Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category"]
