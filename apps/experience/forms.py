from django import forms
from django.conf import settings

from apps.experience.models import Gender


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=80, label="Name")
    age = forms.IntegerField(
        label="Age",
        min_value=settings.EXPERIENCE_MIN_AGE,
        max_value=settings.EXPERIENCE_MAX_AGE,
    )
    gender = forms.ChoiceField(label="Gender", choices=Gender.choices)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        if any(ord(char) < 32 for char in name):
            raise forms.ValidationError("Name contains invalid characters.")
        return name
