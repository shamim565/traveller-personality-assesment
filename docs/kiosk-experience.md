# Kiosk Experience Design

One-shot, full-screen, touch-first journey: **~60–90 seconds** total. No menus, no
scrolling, no accounts, no typing beyond the name field.

## 1. Journey Map

```
Idle/Attract ──▶ Profile ──▶ Q1 ──▶ Q2 ──▶ Q3 ──▶ Q4 ──▶ Q5 ──▶ Q6
     │                                                    │
     │              (inactivity 45s, "Still there?" +10s) │
     │                                                    ▼
     │◀─────── Reset ◀── Result ◀── Reveal ◀── Analyzing (1–2s)
     └──────────────  (30–45s auto or manual)
```

## 2. Screen-by-Screen Specification

| # | Screen | Purpose | Expected duration | Primary action | Timeout | Transition |
|---|---|---|---|---|---|---|
| 1 | Idle / Attract | Draw people from a distance; headline + CTA | variable (loops) | Tap "Discover My Travel Personality" | none (attract loops forever) | HTMX POST `/experience/start/` swaps #experience to Profile |
| 2 | Profile | Collect name, age, gender | 10–15 s | Tap "Start the Quiz" | 45 s idle → "Still there?" → +10 s → reset | HTMX POST `/experience/profile/` → Question 1 partial |
| 3 | Quiz ×6 | One question per screen, large answer cards | 5–8 s each (30–48 s total) | Tap an answer card | 45 s idle → "Still there?" → +10 s → reset | HTMX POST `/experience/answer/` → next question (or Analyzing after Q6) |
| 4 | Analyzing | Moment of anticipation | 1–2 s | none | — | automatic: HTMX `load` trigger after ~1.6 s calls `/experience/complete/` |
| 5 | Reveal | Punchy persona announcement ("SAZID, YOU ARE A HERITAGE HUNTER!") | included in result | none | — | part of Result screen |
| 6 | Result | Avatar, description, keywords, style hints, branding; photo-ready | 10–20 s display, then auto-reset | Tap "Start Again" | 45 s auto-reset countdown (Alpine) | HTMX POST `/experience/reset/` → Idle |
| 7 | Error/Recovery | Friendly restart, never a Django traceback | as needed | Tap "Start Again" | none | `/experience/reset/` → Idle |

**Totals:** Profile 10–15 s + Quiz 30–48 s + Analyzing 1–2 s + Result 10–20 s ≈ **60–90 s**.

## 3. Interaction Standards

- Minimum tap target **44×44 CSS px**; answer cards and CTAs far larger (full-card taps).
- No hover-dependent UI, no dropdowns, no narrow radio buttons, no scroll
  (everything fits 1920×1080 landscape; responsive for tablets/laptops).
- Large type: headline ≥ 48 px, question ≥ 40 px, answers ≥ 32 px at kiosk size.
- High contrast; visible focus rings; semantic `<button>`/`<form>` elements;
  `aria-live` for question swaps.
- Progress indicator: always-visible bar + "Question 3 of 6" label.
- Tap feedback: instant Alpine press state on cards before HTMX swaps content.
- All transitions are server-rendered partial swaps — no page reloads.

## 4. Timing Parameters (configurable via settings/env)

| Parameter | Default | Meaning |
|---|---|---|
| `EXPERIENCE_RESET_DELAY_SECONDS` | 45 | Auto-reset countdown on result screen |
| `EXPERIENCE_STILL_THERE_SECONDS` | 45 | Idle before "Still there?" during profile/quiz |
| `EXPERIENCE_STILL_THERE_GRACE_SECONDS` | 10 | Extra grace before hard reset |
| `EXPERIENCE_ANALYZING_MS` | 1600 | Analysis transition duration |
| `EXPERIENCE_MIN_AGE` / `MAX_AGE` | 10 / 100 | Age input bounds |

## 5. Inactivity & Reset Behavior

1. **During profile/quiz:** Alpine timer resets on any `touchstart`/`click`.
   After 45 s → full-screen "Still there?" overlay with a large "Continue" button.
   After 10 more seconds → automatic POST to `/experience/reset/`.
2. **On result:** visible countdown; at 0 → `/experience/reset/`.
3. **Manual "Start Again"** available on result and error screens.
4. **Reset guarantees:** clears name, age, gender, answers, result state from the
   session; marks any unfinished assessment record `abandoned`; returns Idle.
   The next visitor can never see the previous visitor's data.

## 6. Attract-Loop & Branding

Idle screen: campaign headline, CTA, World Tourism Day 2026 key visual, organizer
and sponsor logos, persona illustration strip, slow CSS/light-Alpine animations
(branding-aware but logic-free). Asset paths configurable in
`static/branding/{world-tourism-day,logos,kv}/` with neutral fallbacks so the app
runs before final assets arrive.

## 7. Result Screen Layout (social-card-like)

- Top: campaign KV strip / event logo
- Center: avatar (large), "SAZID," → "YOU ARE A" → "HERITAGE HUNTER!"
- Persona short description (1–2 lines)
- "Your Travel Style": 4 keywords (e.g., History • Heritage • Architecture • Discovery)
- Optional "You Might Love": 4 destination-style hints
- Footer: organizer logos + campaign hashtag
- Bottom: "Start Again" + subtle countdown

Kept deliberately uncluttered so photos of the screen look clean and branded.

## 8. Error & Recovery UX

Any failed request renders a friendly full-screen partial: "Something went wrong.
Tap below to restart the experience." with a "Start Again" CTA. Server-side errors
are logged with context (no visitor PII) for operators. Browsers never see Django
debug pages in production.
