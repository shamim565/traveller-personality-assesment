from django import forms
from django.conf import settings

from apps.experience.models import Gender

ERROR_MESSAGES = {
    "bn": {
        "name_required": "নাম লিখতে হবে।",
        "name_invalid": "নামে অবৈধ অক্ষর রয়েছে।",
        "name_max_length": "নাম ৮০ অক্ষরের বেশি হতে পারবে না।",
        "age_required": "বয়স লিখতে হবে।",
        "age_invalid": "সঠিক বয়স লিখুন।",
        "age_min_value": "বয়স কমপক্ষে %(limit_value)s বছর হতে হবে।",
        "age_max_value": "বয়স %(limit_value)s বছরের বেশি হতে পারবে না।",
        "gender_required": "লিঙ্গ নির্বাচন করতে হবে।",
        "gender_invalid": "সঠিক লিঙ্গ নির্বাচন করুন।",
    },
    "en": {
        "name_required": "Name is required.",
        "name_invalid": "Name contains invalid characters.",
        "name_max_length": "Name must be 80 characters or fewer.",
        "age_required": "Age is required.",
        "age_invalid": "Enter a valid age.",
        "age_min_value": "Age must be at least %(limit_value)s.",
        "age_max_value": "Age must be %(limit_value)s or less.",
        "gender_required": "Please select a gender.",
        "gender_invalid": "Select a valid gender.",
    },
}

GENDER_LABELS = {
    Gender.MALE: {"bn": "পুরুষ", "en": "Male"},
    Gender.FEMALE: {"bn": "নারী", "en": "Female"},
}


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=80, label="Name")
    age = forms.IntegerField(
        label="Age",
        min_value=settings.EXPERIENCE_MIN_AGE,
        max_value=settings.EXPERIENCE_MAX_AGE,
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=[
            (Gender.MALE, GENDER_LABELS[Gender.MALE]["bn"]),
            (Gender.FEMALE, GENDER_LABELS[Gender.FEMALE]["bn"]),
        ],
    )

    def __init__(self, data=None, lang="bn"):
        super().__init__(data=data)
        self.lang = lang if lang in ERROR_MESSAGES else "bn"
        messages = ERROR_MESSAGES[self.lang]
        self.fields["gender"].choices = [
            (value, GENDER_LABELS[value][self.lang])
            for value in (Gender.MALE, Gender.FEMALE)
        ]
        self.fields["name"].error_messages = {
            "required": messages["name_required"],
            "max_length": messages["name_max_length"],
        }
        self.fields["age"].error_messages = {
            "required": messages["age_required"],
            "invalid": messages["age_invalid"],
            "min_value": messages["age_min_value"],
            "max_value": messages["age_max_value"],
        }
        self.fields["gender"].error_messages = {
            "required": messages["gender_required"],
            "invalid_choice": messages["gender_invalid"],
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError(ERROR_MESSAGES[self.lang]["name_required"])
        if any(ord(char) < 32 for char in name):
            raise forms.ValidationError(ERROR_MESSAGES[self.lang]["name_invalid"])
        return name

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        if gender is None:
            raise forms.ValidationError(ERROR_MESSAGES[self.lang]["gender_required"])
        if gender not in GENDER_LABELS:
            raise forms.ValidationError(ERROR_MESSAGES[self.lang]["gender_invalid"])
        return gender
