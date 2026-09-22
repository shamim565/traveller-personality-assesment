import pytest

from apps.experience.models import AgeGroup, Persona, PersonaAvatar
from apps.experience.services.avatars import resolve_avatar


@pytest.fixture
def persona(db):
    return Persona.objects.create(name="Beach Lover", slug="beach_lover")


@pytest.fixture
def age_groups(db):
    return {
        "young_adult": AgeGroup.objects.create(name="Young Adult", min_age=18, max_age=29),
        "adult": AgeGroup.objects.create(name="Adult", min_age=30, max_age=49),
    }


def avatar(persona, gender="", age_group=None, image="x.webp", is_default=False):
    return PersonaAvatar.objects.create(
        persona=persona, gender=gender, age_group=age_group, image=image, is_default=is_default
    )


def test_exact_match_wins(persona, age_groups):
    avatar(persona, "male", age_groups["young_adult"], "exact.webp")
    avatar(persona, "male", None, "gender-default.webp", is_default=True)
    avatar(persona, "", None, "neutral.webp", is_default=True)
    assert (
        resolve_avatar(persona, gender="male", age_group=age_groups["young_adult"])
        == "exact.webp"
    )


def test_is_default_preferred_among_exact_matches(persona, age_groups):
    avatar(persona, "male", age_groups["young_adult"], "variant-2.webp")
    avatar(persona, "male", age_groups["young_adult"], "variant-default.webp", is_default=True)
    assert (
        resolve_avatar(persona, gender="male", age_group=age_groups["young_adult"])
        == "variant-default.webp"
    )


def test_gender_default_used_without_age_variant(persona, age_groups):
    avatar(persona, "male", None, "gender-default.webp", is_default=True)
    avatar(persona, "", None, "neutral.webp", is_default=True)
    assert (
        resolve_avatar(persona, gender="male", age_group=age_groups["adult"])
        == "gender-default.webp"
    )


def test_gender_default_ignores_non_default_rows(persona, age_groups):
    avatar(persona, "male", None, "not-default.webp", is_default=False)
    avatar(persona, "", None, "neutral.webp", is_default=True)
    assert (
        resolve_avatar(persona, gender="male", age_group=age_groups["adult"])
        == "neutral.webp"
    )


def test_neutral_default_used_without_gender_match(persona, age_groups):
    avatar(persona, "male", age_groups["young_adult"], "male-only.webp")
    avatar(persona, "", None, "neutral.webp", is_default=True)
    assert resolve_avatar(persona, gender="female", age_group=age_groups["young_adult"]) == "neutral.webp"
    assert resolve_avatar(persona) == "neutral.webp"


def test_neutral_any_row_when_no_flag(persona):
    avatar(persona, "", None, "neutral-unflagged.webp")
    assert resolve_avatar(persona, gender="female") == "neutral-unflagged.webp"


def test_global_default_when_persona_has_no_avatars(persona, settings):
    settings.AVATAR_GLOBAL_DEFAULT = "avatars/global-default.svg"
    assert resolve_avatar(persona, gender="male") == "avatars/global-default.svg"


def test_prefer_not_to_say_falls_to_neutral(persona, age_groups):
    avatar(persona, "male", None, "male.webp", is_default=True)
    avatar(persona, "", None, "neutral.webp", is_default=True)
    assert (
        resolve_avatar(persona, gender="prefer_not_to_say", age_group=age_groups["young_adult"])
        == "neutral.webp"
    )
