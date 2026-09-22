# Skill — Tailwind UI

## Responsibility

Touch-first, large-type kiosk styling with Tailwind CSS; Bangla typography;
responsive 1920×1080 → tablet layouts.

## Rules

1. Utility-first; kiosk design tokens (colors, type scale, card sizes) defined
   once in `tailwind.config` theme extension — no ad-hoc hex values in templates.
2. Type scale for a standing visitor: headline ≥ text-5xl, question ≥ text-4xl,
   answer cards ≥ text-2xl; generous line-height for Bangla conjuncts.
3. Self-host `Noto Sans Bengali` (OFL, license file bundled) with system font
   fallbacks; verify no tofu glyphs on event hardware.
4. Answer cards: large tap area, clear selected/pressed states (Alpine), strong
   contrast, focus-visible rings; never color-only state.
5. No absolute dimensions for screen sizing — use viewport-aware utilities and
   max-widths; test 1920×1080, 1366×768, tablet.
6. Production CSS is a compiled Tailwind build; no CDN at runtime (offline event).
7. Keep animations GPU-friendly (transform/opacity); respect
   `prefers-reduced-motion`.

## Checklist (review)

- [ ] No inline `style=""` hacks duplicating theme tokens
- [ ] Contrast AA on text, AAA for headline/CTA
- [ ] Mixed Bangla/English renders without clipping at large sizes
