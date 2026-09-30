"""QR code for the kiosk result screen plus the PNG download served to a
visitor's phone after scanning it (docs/kiosk-experience.md §Result).

The visitor name lives only in the kiosk session and is never persisted
(docs/privacy.md), so the downloadable image is built from the completed
assessment alone and intentionally contains no visitor name.
"""

from __future__ import annotations

import base64
import io
import logging
from functools import lru_cache
from pathlib import Path

import qrcode
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont, features

from apps.experience.services import avatars as avatar_service

logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1080, 1350
PADDING = 90
AVATAR_SIZE = 380
NAME_Y = 172
YOU_ARE_A_Y = 258
PERSONA_Y = 350
AVATAR_TOP = 420

NIGHT = (15, 23, 42)
SAND = (245, 158, 11)
OCEAN = (14, 116, 144)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)
PILL = (30, 41, 59)
SILHOUETTE = (14, 93, 119)

FONT_REGULAR = settings.BASE_DIR / "static" / "fonts" / "hind-siliguri-400.ttf"
FONT_BOLD = settings.BASE_DIR / "static" / "fonts" / "hind-siliguri-700.ttf"

RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def qr_png_data_uri(url):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=3
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color=NIGHT, back_color="white").convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def render_result_png(assessment):
    persona = assessment.primary_persona
    avatar = avatar_service.resolve_avatar(
        persona, gender=assessment.gender, age_group=assessment.age_group
    )
    keywords = [k.strip() for k in persona.keywords_bn.split("•") if k.strip()]
    name = assessment.visitor_name

    image = _canvas()
    draw = ImageDraw.Draw(image)

    _draw_tracked(draw, WIDTH // 2, 116, "TRAVELLER PERSONALITY", _font(30, bold=True), SAND, 10)
    if name:
        name_font = _font(56, bold=True)
        draw.text(
            (WIDTH // 2, NAME_Y),
            _ellipsize(draw, f"{name},", name_font, WIDTH - 2 * PADDING),
            font=name_font,
            fill=WHITE,
            anchor="mm",
        )
    _draw_tracked(draw, WIDTH // 2, YOU_ARE_A_Y, "YOU ARE A", _font(44), WHITE, 14)
    draw.text(
        (WIDTH // 2, PERSONA_Y),
        persona.name.upper(),
        font=_font(104, bold=True),
        fill=SAND,
        anchor="mm",
    )

    y = _draw_avatar(image, avatar, persona.slug, top=AVATAR_TOP)
    y = _draw_wrapped(draw, y, persona.short_description_bn, _font(46), WHITE, max_lines=4)
    _draw_keywords(draw, y + 56, keywords)
    _draw_footer(draw, assessment)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _ellipsize(draw, text, font, max_width):
    if draw.textlength(text, font=font) <= max_width:
        return text
    while text and draw.textlength(f"{text}…", font=font) > max_width:
        text = text[:-1]
    return f"{text}…"


@lru_cache(maxsize=1)
def _layout_engine():
    if features.check("raqm"):
        return ImageFont.Layout.RAQM
    logger.warning("Pillow has no Raqm support; Bengali text may render unshaped")
    return ImageFont.Layout.BASIC


@lru_cache(maxsize=None)
def _font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(path), size, layout_engine=_layout_engine())


def _canvas():
    image = Image.new("RGB", (WIDTH, HEIGHT), NIGHT)
    path = finders.find("backgrounds/result.webp")
    if not path:
        return image
    try:
        background = Image.open(path).convert("RGB")
    except Exception:
        logger.exception("result background load failed")
        return image
    image.paste(_cover(background, (WIDTH, HEIGHT)))
    return Image.blend(image, Image.new("RGB", (WIDTH, HEIGHT), NIGHT), 0.62)


def _cover(image, size):
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.LANCZOS
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def _draw_tracked(draw, center_x, y, text, font, fill, tracking):
    widths = [draw.textlength(char, font=font) for char in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = center_x - total / 2
    for char, width in zip(text, widths):
        draw.text((x, y), char, font=font, fill=fill, anchor="lm")
        x += width + tracking


def _draw_wrapped(draw, y, text, font, fill, max_lines):
    line_height = font.size + 22
    for line in _wrap(draw, text, font, WIDTH - 2 * PADDING, max_lines):
        draw.text((WIDTH // 2, y), line, font=font, fill=fill, anchor="mm")
        y += line_height
    return y + 24


def _wrap(draw, text, font, max_width, max_lines):
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if not current or draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def _draw_keywords(draw, y, keywords):
    if not keywords:
        return
    font = _font(38)
    gap, pad_x, pad_y = 20, 36, 18
    max_width = WIDTH - 2 * PADDING
    rows, row, row_width = [], [], 0
    for keyword in keywords:
        width = draw.textlength(keyword, font=font) + 2 * pad_x
        needed = width if not row else row_width + gap + width
        if row and needed > max_width:
            rows.append((row, row_width))
            row, row_width = [keyword], width
        else:
            row.append(keyword)
            row_width = needed
    if row:
        rows.append((row, row_width))

    for items, total in rows:
        x = (WIDTH - total) / 2
        height = font.size + 2 * pad_y
        for keyword in items:
            width = draw.textlength(keyword, font=font) + 2 * pad_x
            draw.rounded_rectangle(
                (x, y, x + width, y + height), radius=height / 2, fill=PILL
            )
            draw.text(
                (x + width / 2, y + height / 2), keyword, font=font, fill=SAND, anchor="mm"
            )
            x += width + gap
        y += height + 24


def _draw_avatar(image, avatar_path, slug, top):
    left = (WIDTH - AVATAR_SIZE) // 2
    box = (left, top, left + AVATAR_SIZE, top + AVATAR_SIZE)
    raster = _load_raster_avatar(avatar_path)
    if raster is None:
        _draw_avatar_placeholder(ImageDraw.Draw(image), box, slug)
        return top + AVATAR_SIZE + 60
    mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, AVATAR_SIZE, AVATAR_SIZE), radius=44, fill=255
    )
    image.paste(_cover(raster, (AVATAR_SIZE, AVATAR_SIZE)), box[:2], mask)
    return top + AVATAR_SIZE + 60


def _load_raster_avatar(avatar_path):
    if not avatar_path or Path(avatar_path).suffix.lower() not in RASTER_SUFFIXES:
        return None
    found = finders.find(avatar_path)
    if not found:
        return None
    try:
        return Image.open(found).convert("RGBA")
    except Exception:
        logger.exception("avatar load failed for result image")
        return None


def _draw_avatar_placeholder(draw, box, slug):
    x0, y0, x1, y1 = box
    size = x1 - x0
    center = (x0 + x1) / 2
    draw.rounded_rectangle(box, radius=44, fill=OCEAN)
    head = size * 0.19
    draw.ellipse(
        (center - head, y0 + size * 0.22, center + head, y0 + size * 0.22 + 2 * head),
        fill=SILHOUETTE,
    )
    shoulders = size * 0.34
    draw.pieslice(
        (center - shoulders, y0 + size * 0.62, center + shoulders, y0 + size * 0.62 + 2 * shoulders),
        180,
        360,
        fill=SILHOUETTE,
    )
    draw.text((center, y1 - 32), slug, font=_font(28), fill=WHITE, anchor="mm")


def _draw_footer(draw, assessment):
    completed = assessment.completed_at or timezone.now()
    label = f"{assessment.kiosk_identifier}  •  {completed:%d %b %Y}"
    draw.text((WIDTH // 2, HEIGHT - 76), label, font=_font(30), fill=MUTED, anchor="mm")
