# Travel Persona Model

Six personas. Each is a **travel preference archetype**, not a demographic segment. Age and gender never determine the persona; they only select the result avatar and feed aggregate analytics.

## 1. The Six Personas

### Heritage Hunter
Loves history, heritage, historical architecture, monuments, old cities, museums, stories of the past.

### Beach Lover
Loves beaches, islands, riversides, relaxation, sunsets, resorts, calm vacations.

### Adventure Seeker
Loves trekking, hiking, camping, kayaking, cycling, physical challenge, excitement, risk-in-fun.

### Nature Explorer
Loves mountains, forests, landscapes, wildlife, scenic places, peaceful natural environments. **Not** necessarily thrill-seeking.

### Urban Explorer
Loves cities, cafés, restaurants, shopping, entertainment, nightlife, modern attractions.

### Culture Connector
Loves local people, traditions, festivals, local markets, local food, villages, community experiences. **Not** the same as historical monuments.

## 2. Persona Boundaries (overlap management)

### Adventure Seeker vs Nature Explorer
| | Adventure Seeker | Nature Explorer |
|---|---|---|
| Motivation | Physical activity, challenge, thrill | Scenery, calm, natural beauty |
| Verbs | Trekking, kayaking, camping, cycling | Watching, walking, photographing, relaxing |
| Emotion | Excitement | Peace |

Rule: an answer mentioning *activity/adventure* scores Adventure first, Nature secondary. An answer about *mountains/forests/scenery* scores Nature first. Someone who wants nature without thrill must reach Nature Explorer (see scoring-system.md §calibration).

### Heritage Hunter vs Culture Connector
| | Heritage Hunter | Culture Connector |
|---|---|---|
| Focus | The past: monuments, architecture, museums, ruins | The living present: people, food, festivals, markets |
| Emotion | Awe, curiosity about history | Connection, warmth, participation |

Rule: "পুরোনো স্থাপনা / ঐতিহাসিক জায়গা" → Heritage primary, Culture small secondary. "লোকাল খাবার / মানুষ / উৎসব / গ্রাম" → Culture primary, Heritage small secondary.

### Beach Lover vs Nature Explorer
Both are "calm + scenic". Rule: water answers (sea, island, riverbank, sunset by water) → Beach. Land answers (mountain, forest, wildlife) → Nature. Answers about relaxing with views give Beach primary and Nature a small secondary.

### Culture Connector vs Urban Explorer
Both are "people + consumption". Rule: local/authentic (markets, festivals, villages, local food) → Culture. Modern/city (cafés, shopping, nightlife, entertainment) → Urban.

## 3. Age Impact

- Age does **not** influence persona classification.
- Age selects the avatar **age group** and feeds aggregate age-group analytics.
- Configurable age groups (seed defaults):

| Key | Name | Range |
|---|---|---|
| `teen` | Teen | 10–17 |
| `young_adult` | Young Adult | 18–29 |
| `adult` | Adult | 30–49 |
| `mature_adult` | Mature Adult | 50–64 |
| `senior` | Senior | 65–100 |

Age input is validated against a configurable global range (default 10–100). Groups are matched inclusively; boundaries are reviewable by stakeholders in Admin.

## 4. Gender Impact

- Gender does **not** influence persona classification.
- Gender selects the avatar variant and feeds optional aggregate gender analytics.
- Options (configurable): `male`, `female`, `prefer_not_to_say`.

## 5. Secondary Persona

Internally the top two personas are stored (`primary_persona`, `secondary_persona`). The public result screen shows only the primary. Secondary exists for future recommendations and analytics; a secondary with score 0 is stored as null.

## 6. Companion Trait (from Question 5)

Question 5 ("who do you travel with") does **not** classify personas. It produces a supplementary trait: `solo`, `couple`, `family`, `friends`, `destination_first`, stored per assessment for insight/analytics. See scoring-system.md §6.

## 7. Persona Reachability Contract

Every persona must be achievable as primary by a plausible answer pattern. This is enforced by the calibration test suite (testing.md §2.1). Personas must never be reachable only via contrived or contradictory answers.
