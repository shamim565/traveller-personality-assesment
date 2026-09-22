from django import template

from apps.experience.services import avatars

register = template.Library()


@register.simple_tag
def avatar_image(persona, gender=None, age_group=None):
    return avatars.resolve_avatar(persona, gender=gender, age_group=age_group)
