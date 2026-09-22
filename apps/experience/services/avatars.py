"""Avatar resolution with the deterministic fallback chain
(docs/persona-model.md §7, docs/database-design.md §PersonaAvatar):

exact persona+gender+age_group
    -> persona+gender default (is_default, no age group)
    -> persona neutral default (blank gender, no age group)
    -> global default asset (settings.AVATAR_GLOBAL_DEFAULT)
"""

from django.conf import settings


def resolve_avatar(persona, gender=None, age_group=None):
    avatars = persona.avatars.all()

    if gender and age_group:
        match = avatars.filter(gender=gender, age_group=age_group).order_by("-is_default").first()
        if match:
            return match.image

    if gender:
        match = avatars.filter(gender=gender, age_group__isnull=True, is_default=True).first()
        if match:
            return match.image

    match = avatars.filter(gender="", age_group__isnull=True, is_default=True).first()
    if match:
        return match.image

    match = avatars.filter(gender="", age_group__isnull=True).first()
    if match:
        return match.image

    return settings.AVATAR_GLOBAL_DEFAULT
