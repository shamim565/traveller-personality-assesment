"""Avatar resolution with the deterministic fallback chain:

exact persona+gender+age_group
    -> persona+gender default (is_default, no age group)
    -> persona neutral default (blank gender, no age group)
    -> global default asset (settings.AVATAR_GLOBAL_DEFAULT)

Works on the related manager's prefetch cache: `persona.avatars.all()` is
materialized once and filtered in Python, so callers can prefetch_related.
"""

from django.conf import settings


def resolve_avatar(persona, gender=None, age_group=None):
    avatars = list(persona.avatars.all())

    if gender and age_group is not None:
        group_id = age_group.id if hasattr(age_group, "id") else age_group
        matches = [
            avatar
            for avatar in avatars
            if avatar.gender == gender and avatar.age_group_id == group_id
        ]
        if matches:
            return sorted(matches, key=lambda avatar: avatar.is_default, reverse=True)[0].image

    if gender:
        matches = [
            avatar
            for avatar in avatars
            if avatar.gender == gender and avatar.age_group_id is None and avatar.is_default
        ]
        if matches:
            return matches[0].image

    matches = [
        avatar
        for avatar in avatars
        if avatar.gender == "" and avatar.age_group_id is None and avatar.is_default
    ]
    if matches:
        return matches[0].image

    matches = [
        avatar
        for avatar in avatars
        if avatar.gender == "" and avatar.age_group_id is None
    ]
    if matches:
        return matches[0].image

    return settings.AVATAR_GLOBAL_DEFAULT
