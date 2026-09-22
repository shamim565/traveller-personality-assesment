# Skill — Kiosk Experience Design

## Responsibility

Flow timing, touch usability, inactivity/reset behavior, visual hierarchy,
persona reveal, and visitor throughput for the exhibition kiosk.

## Rules

1. Every screen passes the 5-second comprehension test: headline, one obvious
   primary action, no instructions required.
2. All primary controls ≥ 44×44 CSS px; answer cards are full-card tap targets.
3. No scrolling, no hover-only UI, no dropdowns, no menus anywhere in the
   public flow.
4. Total journey target: 60–90 s (profile 10–15 s, 6 questions × 5–8 s,
   analyzing 1–2 s, result 10–20 s).
5. Progress is always visible ("Question 3 of 6" + bar).
6. Inactivity: 45 s → "Still there?" overlay → +10 s → auto-reset. Result
   screen auto-resets at 45 s with visible countdown.
7. Reset clears every piece of visitor state; next visitor never sees prior data.
8. Every failure state offers a single "Start Again" action; never an error page.
9. Reveal is fast and punchy; analysis delay is cosmetic (≤ 2 s), not "waiting
   for AI".
10. Animations are subtle (attract loop, card press, reveal) and never block input.

## Checklist (per screen)

- [ ] Can visitors understand it immediately?
- [ ] Can every button be tapped comfortably?
- [ ] Does it fit without scrolling at 1920×1080 and on a tablet?
- [ ] Can someone abandon mid-flow without breaking the next session?
- [ ] Does it reset safely?
