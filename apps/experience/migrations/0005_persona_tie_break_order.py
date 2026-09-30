from django.db import migrations, models

TIE_BREAK_ORDER = {
    "heritage_hunter": 1,
    "nature_explorer": 2,
    "culture_connector": 3,
    "adventure_seeker": 4,
    "beach_lover": 5,
    "urban_explorer": 6,
}

# v1.1 nature recalibration: calm/scenic answers gain +1 Nature so the
# archetype is not outscored by Beach on scenery answers.
NATURE_WEIGHT_UPDATES = [
    # (question order, option order, old weight, new weight)
    (3, 1, 2, 3),
    (4, 1, 1, 2),
    (6, 1, 1, 2),
]


def apply_calibration(apps, schema_editor):
    Persona = apps.get_model("experience", "Persona")
    AnswerPersonaWeight = apps.get_model("experience", "AnswerPersonaWeight")
    for slug, order in TIE_BREAK_ORDER.items():
        Persona.objects.filter(slug=slug).update(tie_break_order=order)
    for question_order, option_order, old_weight, new_weight in NATURE_WEIGHT_UPDATES:
        AnswerPersonaWeight.objects.filter(
            persona__slug="nature_explorer",
            answer_option__question__order=question_order,
            answer_option__order=option_order,
            weight=old_weight,
        ).update(weight=new_weight)


def revert_calibration(apps, schema_editor):
    Persona = apps.get_model("experience", "Persona")
    AnswerPersonaWeight = apps.get_model("experience", "AnswerPersonaWeight")
    Persona.objects.update(tie_break_order=0)
    for question_order, option_order, old_weight, new_weight in NATURE_WEIGHT_UPDATES:
        AnswerPersonaWeight.objects.filter(
            persona__slug="nature_explorer",
            answer_option__question__order=question_order,
            answer_option__order=option_order,
            weight=new_weight,
        ).update(weight=old_weight)


class Migration(migrations.Migration):
    dependencies = [
        ("experience", "0004_assessmentanswer_idx_asmanswer_option"),
    ]

    operations = [
        migrations.AddField(
            model_name="persona",
            name="tie_break_order",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.RunPython(apply_calibration, revert_calibration),
    ]
