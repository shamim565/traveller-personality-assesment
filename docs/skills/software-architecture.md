# Skill — Software Architecture

> Project-internal engineering guide. Can be promoted to an agent skill file if
> the environment supports it.

## Responsibility

Own architecture boundaries, dependency direction, data flow, package
structure, and complexity management for this Django monolith.

## Rules

1. Keep the monolith modular — separate apps by domain (`experience`,
   `analytics`, `core`), not by technical layer.
2. Do not introduce services/microservices, message queues, or event buses
   without a concrete requirement.
3. Prefer explicit, boring code over clever abstractions.
4. Avoid premature abstraction: introduce a service/selector only when a second
   caller exists or clarity demands it.
5. Dependency direction: `views → services/selectors → models`. Services never
   import HTTP objects; models never import services.
6. Any cross-app dependency must be one-directional and documented
   (`analytics` reads `experience` models; `experience` never imports `analytics`).
7. Config over hardcoding: timings, kiosk id, fallback assets via settings/env.

## Checklist (architecture review)

- [ ] Business logic lives in services, not views or templates
- [ ] No circular imports between apps
- [ ] Every abstraction has ≥1 concrete benefit named in code review
- [ ] New dependencies justified against MVP scope
