from django.db import migrations


def merge_senior_into_mature_adult(apps, schema_editor):
    AgeGroup = apps.get_model("experience", "AgeGroup")
    AssessmentSession = apps.get_model("experience", "AssessmentSession")
    PersonaAvatar = apps.get_model("experience", "PersonaAvatar")

    mature = AgeGroup.objects.filter(name="Mature Adult").first()
    senior = AgeGroup.objects.filter(name="Senior").first()

    if mature is None:
        if senior is None:
            return
        senior.name = "Mature Adult"
        senior.max_age = 100
        senior.order = 4
        senior.save(update_fields=["name", "max_age", "order"])
        return

    if mature.max_age < 100 or mature.order != 4:
        mature.max_age = 100
        mature.order = 4
        mature.save(update_fields=["max_age", "order"])

    if senior is not None:
        AssessmentSession.objects.filter(age_group=senior).update(age_group=mature)
        PersonaAvatar.objects.filter(age_group=senior).delete()
        senior.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("experience", "0006_assessmentsession_visitor_name"),
    ]

    operations = [
        migrations.RunPython(merge_senior_into_mature_adult, migrations.RunPython.noop),
    ]
