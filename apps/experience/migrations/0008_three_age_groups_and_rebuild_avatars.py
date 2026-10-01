from django.db import migrations

AGE_GROUPS = [
    ("Teen", 10, 20, 1),
    ("Young", 21, 40, 2),
    ("Adult", 41, 100, 3),
]
AGE_KEYS = {"Teen": "teen", "Young": "young", "Adult": "adult"}


def forwards(apps, schema_editor):
    AgeGroup = apps.get_model("experience", "AgeGroup")
    AssessmentSession = apps.get_model("experience", "AssessmentSession")
    Persona = apps.get_model("experience", "Persona")
    PersonaAvatar = apps.get_model("experience", "PersonaAvatar")

    AssessmentSession.objects.all().delete()

    PersonaAvatar.objects.filter(age_group__isnull=False).delete()
    AgeGroup.objects.all().delete()

    groups = {}
    for name, min_age, max_age, order in AGE_GROUPS:
        groups[name] = AgeGroup.objects.create(
            name=name, min_age=min_age, max_age=max_age, order=order
        )

    for persona in Persona.objects.all():
        for gender in ("male", "female"):
            for name, key in AGE_KEYS.items():
                PersonaAvatar.objects.create(
                    persona=persona,
                    gender=gender,
                    age_group=groups[name],
                    image=f"avatars/{persona.slug}/{gender}-{key}.webp",
                    is_default=False,
                )


class Migration(migrations.Migration):
    dependencies = [
        ("experience", "0007_merge_senior_into_mature_adult"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
