import uuid

from django.conf import settings
from django.db import models


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"


class AssessmentStatus(models.TextChoices):
    STARTED = "started", "Started"
    COMPLETED = "completed", "Completed"
    ABANDONED = "abandoned", "Abandoned"
    TIMED_OUT = "timed_out", "Timed out"


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "single_choice", "Single choice"


class CompanionTrait(models.TextChoices):
    SOLO = "solo", "Solo"
    COUPLE = "couple", "Couple"
    FAMILY = "family", "Family"
    FRIENDS = "friends", "Friends"
    DESTINATION_FIRST = "destination_first", "Destination first"


def default_kiosk_identifier():
    return settings.KIOSK_IDENTIFIER


class QuestionnaireVersion(models.Model):
    name = models.CharField(max_length=120)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.version})"


class Persona(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    short_description_bn = models.CharField(max_length=160, blank=True)
    short_description_en = models.CharField(max_length=160, blank=True)
    description_bn = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    tagline_bn = models.CharField(max_length=120, blank=True)
    tagline_en = models.CharField(max_length=120, blank=True)
    keywords_bn = models.CharField(max_length=255, blank=True)
    keywords_en = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Question(models.Model):
    questionnaire_version = models.ForeignKey(
        QuestionnaireVersion, on_delete=models.CASCADE, related_name="questions"
    )
    text_bn = models.TextField()
    text_en = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField()
    question_type = models.CharField(
        max_length=20, choices=QuestionType.choices, default=QuestionType.SINGLE_CHOICE
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["questionnaire_version", "order"],
                name="uniq_question_version_order",
            ),
        ]
        indexes = [
            models.Index(
                fields=["questionnaire_version", "is_active", "order"],
                name="idx_q_version_active",
            ),
        ]

    def __str__(self):
        return f"Q{self.order}: {self.text_bn[:40]}"


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text_bn = models.CharField(max_length=255)
    text_en = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    companion_trait = models.CharField(
        max_length=20, choices=CompanionTrait.choices, null=True, blank=True
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "order"], name="uniq_option_question_order"
            ),
        ]

    def __str__(self):
        return f"{self.question_id}#{self.order}: {self.text_bn[:40]}"


class AnswerPersonaWeight(models.Model):
    answer_option = models.ForeignKey(
        AnswerOption, on_delete=models.CASCADE, related_name="weights"
    )
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="answer_weights"
    )
    weight = models.SmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["answer_option", "persona"], name="uniq_weight_option_persona"
            ),
            models.CheckConstraint(
                condition=models.Q(weight__gte=0) & models.Q(weight__lte=5),
                name="chk_weight_0_to_5",
            ),
        ]

    def __str__(self):
        return f"{self.answer_option_id} -> {self.persona_id}: {self.weight}"


class AgeGroup(models.Model):
    name = models.CharField(max_length=40, unique=True)
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(min_age__lte=models.F("max_age")),
                name="chk_agegroup_min_lte_max",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.min_age}–{self.max_age})"

    @classmethod
    def resolve(cls, age):
        return (
            cls.objects.filter(min_age__lte=age, max_age__gte=age)
            .order_by("order")
            .first()
        )


class PersonaAvatar(models.Model):
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="avatars"
    )
    gender = models.CharField(
        max_length=20, choices=Gender.choices, blank=True, default=""
    )
    age_group = models.ForeignKey(
        AgeGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    image = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["persona__sort_order", "id"]

    def __str__(self):
        scope = "-".join(
            part for part in (self.persona.slug, self.gender, str(self.age_group_id or "")) if part
        ) or "unscoped"
        return f"{scope}: {self.image}"


class AssessmentSession(models.Model):
    session_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    questionnaire_version = models.ForeignKey(
        QuestionnaireVersion, on_delete=models.PROTECT, related_name="assessments"
    )
    age_group = models.ForeignKey(
        AgeGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    gender = models.CharField(max_length=20, choices=Gender.choices, null=True, blank=True)
    primary_persona = models.ForeignKey(
        Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    secondary_persona = models.ForeignKey(
        Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    companion_trait = models.CharField(
        max_length=20, choices=CompanionTrait.choices, null=True, blank=True
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=AssessmentStatus.choices, default=AssessmentStatus.STARTED
    )
    kiosk_identifier = models.CharField(max_length=20, default=default_kiosk_identifier)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["status"], name="idx_asm_status"),
            models.Index(fields=["started_at"], name="idx_asm_started"),
            models.Index(fields=["completed_at"], name="idx_asm_completed"),
            models.Index(fields=["primary_persona"], name="idx_asm_primary"),
            models.Index(fields=["kiosk_identifier"], name="idx_asm_kiosk"),
            models.Index(fields=["age_group"], name="idx_asm_agegroup"),
            models.Index(fields=["gender"], name="idx_asm_gender"),
        ]

    def __str__(self):
        return str(self.session_uuid)


class AssessmentAnswer(models.Model):
    assessment = models.ForeignKey(
        AssessmentSession, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="+")
    answer_option = models.ForeignKey(
        AnswerOption, on_delete=models.PROTECT, related_name="+"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "question"], name="uniq_answer_assessment_question"
            ),
        ]

    def __str__(self):
        return f"{self.assessment_id} Q{self.question.order}"


class AssessmentPersonaScore(models.Model):
    assessment = models.ForeignKey(
        AssessmentSession, on_delete=models.CASCADE, related_name="persona_scores"
    )
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="+")
    raw_score = models.PositiveSmallIntegerField()
    normalized_score = models.PositiveSmallIntegerField()
    rank = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["rank"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "persona"], name="uniq_score_assessment_persona"
            ),
        ]

    def __str__(self):
        return f"{self.assessment_id} {self.persona.slug} #{self.rank}"
