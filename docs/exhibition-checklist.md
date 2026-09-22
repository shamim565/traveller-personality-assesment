# Exhibition Checklist (Event-Day Runbook)

Print this for the booth team. Verify every item on setup day and spot-check
during the event.

## A. Setup Day

- [ ] Server hardware powered; Docker host reachable on booth LAN
- [ ] `docker compose up -d` → all three services healthy
- [ ] `curl http://<server-ip>/health/` returns `{"status": "ok", "db": true}`
- [ ] Migrations applied; `seed_travel_personas` run; version "World Tourism Day 2026 v1" is active
- [ ] Kiosk browser launches in full-screen kiosk mode on boot
- [ ] Touchscreen calibrated; all answer cards tap-able with a finger
- [ ] System time/date correct on server and kiosk (affects hourly analytics)
- [ ] Correct KV / organizer logos / sponsor logos loaded (branding folder)
- [ ] All 6×5 avatar combinations present or fallback verified (no broken images)
- [ ] Questionnaire text reviewed end-to-end in Bangla rendering (no tofu glyphs)
- [ ] Scoring spot-check: one known "pure" run per persona gives the expected result
- [ ] Reset tested: finish quiz → Start Again → previous visitor's data gone
- [ ] Timeout tested: leave mid-quiz → "Still there?" → idle
- [ ] Dashboard login tested; staff password set (not default)
- [ ] Backup schedule active; one restore dry-run done
- [ ] Power: kiosk + server on UPS or at least protected circuit
- [ ] Emergency restart steps laminated near kiosk
- [ ] Fallback branding assets exist in case final assets arrive late

## B. During Event (spot checks, every ~2 h)

- [ ] Idle screen playing; no error screen stuck on display
- [ ] Dashboard traffic numbers increasing (sanity check)
- [ ] No lag on question transitions (tap → next question near-instant)
- [ ] Postgres data growing normally; disk not full
- [ ] LAN stable; kiosk not showing "can't connect"

## C. Emergency Responses

| Symptom | Action |
|---|---|
| Frozen screen | Close browser, relaunch kiosk shortcut |
| "Something went wrong" stuck | Tap Start Again; if persistent, `docker compose restart web` |
| Dashboard unreachable | Check server power/LAN; restart compose stack |
| DB errors | Check disk space; restore latest pg_dump per runbook |
| Whole booth down | Full power-cycle: server first, then kiosk; autostart policies bring everything back |

## D. End of Day

- [ ] Backup taken (pg_dump) and stored off the event machine
- [ ] Dashboard screenshots for stakeholder debrief
- [ ] Notes on any anomalies (kiosk issues, peak hours, asset problems)
