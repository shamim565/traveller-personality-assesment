# HTMX Interaction Architecture

Server is the single source of truth. Every kiosk transition is an HTMX partial
swap inside one controlled container. No page reloads during the experience.

## 1. Container & Convention

```html
<main id="experience"> <!-- controlled by HTMX -->
```

Every experience endpoint returns either a full page (plain browser GET to `/`)
or a partial (HTMX request). Detection via `request.htmx`. All POSTs carry the
CSRF token through the standard HTMX header (injected once in `base.html`).
Double-tap protection: every posting button sets `hx-disabled-elt="this"` so the
button disables itself while the request is in flight; server logic is also
idempotent (one answer per question; complete-once).

## 2. Flow Details

### 2.1 Start
```
Idle "Start" button
hx-post="/experience/start/"  hx-target="#experience"  hx-swap="innerHTML"
↓ service: mark any previous unfinished assessment abandoned
↓ create session state + minimal AssessmentSession row (status=started)
↓ return partials/profile_form.html
```

### 2.2 Profile submit
```
Form  hx-post="/experience/profile/"  hx-target="#experience"
↓ view: bind + validate ProfileForm (name, age 10–100, gender) server-side
↓ invalid → re-render form partial with friendly errors (HTTP 200 + error UI)
↓ valid → service stores name/age/gender in session
↓ return partials/question.html (Q1) incl. progress partial
```
No redirects; the swap is the transition.

### 2.3 Answer submit (Q1–Q5)
```
Answer card button
hx-post="/experience/answer/"  hx-vals='{"answer_id": N}'  hx-target="#experience"
↓ service validates: session in quiz state; question id = current question;
  answer belongs to that question; question/answer active
↓ store answer in session (replace if re-answered)
↓ return partials/question.html (next) + updated progress (swap-oob)
```

### 2.4 Final answer (Q6) → Analyzing
```
Same endpoint; after Q6 answer, returns partials/analyzing.html:
  spinner + "Analyzing your travel personality…"
  <div hx-post="/experience/complete/" hx-trigger="load delay:1600ms"
       hx-target="#experience" hx-swap="innerHTML"></div>
```
The reveal feels immediate (server-driven; no artificial AI wait).

### 2.5 Complete
```
POST /experience/complete/
↓ guard: only when all active questions answered and assessment status != completed
↓ service: calculate_travel_persona(answers)  (deterministic, <100 ms)
↓ single transaction: update AssessmentSession (age_group, gender, personas,
  scores, completed_at, duration, status=completed)
  + insert AssessmentAnswer rows + AssessmentPersonaScore rows
↓ copy experience.name onto the completed assessment (privacy.md §2)
↓ return partials/result.html
↓ idempotency: if already completed → return persisted result, no re-write
```

### 2.6 Reset
```
"Start Again" button (result/error) or Alpine timeout
hx-post="/experience/reset/"  hx-target="#experience"
↓ mark unfinished assessment abandoned (if any)
↓ delete all experience.* session keys
↓ return idle partial
```

## 3. Partial Inventory (`templates/partials/`)

| Partial | Renders |
|---|---|
| `profile_form.html` | name/age/gender form (+errors) |
| `question.html` | question text + answer cards |
| `progress.html` | progress bar + "Question X of 6" (oob-updated) |
| `analyzing.html` | spinner + auto-complete trigger |
| `result.html` | persona reveal, avatar, description, restart, QR code |
| `error.html` | friendly recovery + Start Again |
| still-there overlay | rendered in `base.html` outside `#experience`; controlled by the body-level Alpine `kioskSession` guard (survives partial swaps) |

Not HTMX: GET `/experience/result/<uuid>/image/` is a plain image download
(QR target, scanned by the visitor's phone) — see architecture.md §5.

## 4. HTMX Attributes Used (conventions)

- `hx-post` for every state change (start/profile/answer/complete/reset)
- `hx-target="#experience"`, `hx-swap="innerHTML"` (default container)
- `hx-trigger="load delay:1600ms"` for the analyzing→complete handoff
- `hx-disabled-elt="this"` on all tap targets
- `hx-indicator` for the analyzing spinner
- `hx-vals` to send the chosen answer id

## 5. Error & Failure Handling

- Server validation failures return a partial with friendly errors (never a 500 page).
- Unexpected exceptions: 4xx/5xx → `partials/error.html` with "Start Again";
  details logged server-side without PII.
- If JS/HTMX fails to load, the attract screen still renders; POST endpoints
  fall back to full-page responses where practical (graceful degradation).
- Failed HTMX requests: Alpine listens for `htmx:responseError` to show the
  recovery screen if HTMX's default swap doesn't.

## 6. Anti-Patterns Avoided

- No client-side answer/score computation; no duplicated scoring in JS.
- No HTMX polling; the only timer-driven request is the analyzing→complete handoff.
- No out-of-band state spread: everything the client needs arrives in the swap.
- No JSON APIs pretending to be "REST" for the kiosk UI; endpoints are
  HTML-partial-oriented and kiosk-semantic (`/experience/answer/`, not
  `/api/v1/answers`).
