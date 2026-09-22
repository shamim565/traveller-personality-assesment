from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from apps.experience import models


class VersionedContentWarningMixin:
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if request.method == "POST" and object_id is not None:
            obj = self.get_object(request, object_id)
            version = self._questionnaire_version_of(obj)
            if version is not None and version.assessments.exists():
                messages.warning(
                    request,
                    _(
                        "This questionnaire version already has recorded assessments. "
                        "Edits affect future scoring only; for significant changes, "
                        "create a new questionnaire version."
                    ),
                )
        return super().changeform_view(request, object_id, form_url, extra_context)

    @staticmethod
    def _questionnaire_version_of(obj):
        if obj is None:
            return None
        if isinstance(obj, models.QuestionnaireVersion):
            return obj
        if isinstance(obj, models.Question):
            return obj.questionnaire_version
        if isinstance(obj, models.AnswerOption):
            return obj.question.questionnaire_version
        if isinstance(obj, models.AnswerPersonaWeight):
            return obj.answer_option.question.questionnaire_version
        return None


@admin.action(description="Activate selected version(s)")
def activate_versions(modeladmin, request, queryset):
    queryset.update(is_active=True)
    models.QuestionnaireVersion.objects.exclude(pk__in=queryset).update(is_active=False)
    if modeladmin is not None:
        modeladmin.message_user(request, _("Selected version activated; others deactivated."))


class AnswerPersonaWeightInline(admin.TabularInline):
    model = models.AnswerPersonaWeight
    extra = 0


class AnswerOptionInline(admin.TabularInline):
    model = models.AnswerOption
    extra = 4
    fields = ("text_bn", "text_en", "order", "is_active", "companion_trait", "weights_summary")
    readonly_fields = ("weights_summary",)
    show_change_link = True

    @admin.display(description=_("Persona weights"))
    def weights_summary(self, obj):
        if obj.pk is None:
            return ""
        return ", ".join(
            f"{w.persona.slug}={w.weight}" for w in obj.weights.select_related("persona").order_by("persona__sort_order")
        )


@admin.register(models.QuestionnaireVersion)
class QuestionnaireVersionAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "is_active", "created_at", "assessments_count")
    list_filter = ("is_active",)
    actions = [activate_versions]

    @admin.display(description=_("Assessments"))
    def assessments_count(self, obj):
        return obj.assessments.count()


@admin.register(models.Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
    search_fields = ("name", "slug")


@admin.register(models.Question)
class QuestionAdmin(VersionedContentWarningMixin, admin.ModelAdmin):
    list_display = ("text_bn", "questionnaire_version", "order", "question_type", "is_active")
    list_filter = ("questionnaire_version", "is_active", "question_type")
    list_editable = ("order", "is_active")
    ordering = ("questionnaire_version", "order")
    inlines = [AnswerOptionInline]


@admin.register(models.AnswerOption)
class AnswerOptionAdmin(VersionedContentWarningMixin, admin.ModelAdmin):
    list_display = ("text_bn", "question", "order", "is_active", "companion_trait")
    list_filter = ("question__questionnaire_version", "is_active", "companion_trait")
    list_editable = ("order", "is_active")
    ordering = ("question__questionnaire_version", "question__order", "order")
    inlines = [AnswerPersonaWeightInline]


@admin.register(models.AnswerPersonaWeight)
class AnswerPersonaWeightAdmin(VersionedContentWarningMixin, admin.ModelAdmin):
    list_display = ("answer_option", "persona", "weight")
    list_filter = ("persona",)
    list_editable = ("weight",)
    search_fields = ("answer_option__text_bn",)


@admin.register(models.AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "min_age", "max_age", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(models.PersonaAvatar)
class PersonaAvatarAdmin(admin.ModelAdmin):
    list_display = ("persona", "gender", "age_group", "is_default", "image")
    list_filter = ("persona", "gender", "is_default")
    search_fields = ("image",)


@admin.register(models.AssessmentSession)
class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_uuid",
        "status",
        "started_at",
        "primary_persona",
        "kiosk_identifier",
        "duration_seconds",
    )
    list_filter = ("status", "kiosk_identifier", "primary_persona", "age_group", "gender")
    date_hierarchy = "started_at"
    readonly_fields = [f.name for f in models.AssessmentSession._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
