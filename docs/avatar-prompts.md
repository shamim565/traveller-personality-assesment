# Avatar Generation Prompts

AI image-generation prompts for the 60 persona avatars
(6 personas × 2 genders × 5 age groups). Avatars are **pre-generated static
assets** (docs/requirements.md FR-6) — nothing in this repo calls an image
model at runtime. Generate the images off-line (Gemini/Imagen or Flux), save
them with the exact filenames below, then register the rows in
**Admin → PersonaAvatar** (or run the snippet in §8).

**How to use this file:** copy **one prompt at a time**, in the order listed in
§7, and save each result under the file path shown above the prompt. The style
clause is intentionally repeated word-for-word in all 60 prompts — do not
paraphrase it; that is what keeps the set visually consistent.

`prefer_not_to_say` is not generated here: it falls back to each persona's
existing `neutral.svg` via the resolver chain in
`apps/experience/services/avatars.py`. §9 has optional prompts to upgrade those
placeholders later.

## Quick facts

| | |
|---|---|
| Count | 60 (Heritage Hunter ×10, Beach Lover ×10, Adventure Seeker ×10, Nature Explorer ×10, Urban Explorer ×10, Culture Connector ×10) |
| Style | Modern flat vector illustration, stylized character art |
| Composition | Head-and-shoulders, centered, generous margin, 1:1 square |
| Generate at | 1024×1024 |
| Export | 512×512 WebP, quality ~80, ≤150KB |
| Tools | Gemini / Imagen or Flux (off-line, one prompt at a time) |

## 1. Asset contract

| Item | Rule |
|---|---|
| Aspect / size | 1:1 square; generate at 1024×1024, export at 512×512 |
| Crop safety | Face and hair fully inside the center 70% — the app crops to a rounded square (28px radius at the 192px kiosk size, 44px at 380px in the result PNG) |
| Background | Flat, simple, soft gradient; a faint single-motif silhouette behind the subject is allowed and expected |
| Forbidden | Text, letters, numbers, logos, watermarks, borders, frames, busy scenes, texture noise |
| Palette | Brand ocean `#0e7490`, sand `#f59e0b`, night `#0f172a` plus the per-persona accents in §4 |
| Subject | South Asian (Bangladeshi), warm medium-brown skin tone, warm friendly expression, eyes open |
| File names | `static/avatars/<persona_slug>/<gender>-<age_group_key>.webp` |
| DB `image` value | `avatars/<persona_slug>/<gender>-<age_group_key>.webp` |
| Slugs | `heritage_hunter`, `beach_lover`, `adventure_seeker`, `nature_explorer`, `urban_explorer`, `culture_connector` |
| Age keys | `teen`, `young_adult`, `adult`, `mature_adult`, `senior` |
| Gender keys | `male`, `female` (`prefer_not_to_say` → persona `neutral` asset) |

## 2. Master style block

Every prompt below embeds this clause verbatim; it defines the shared look:

> Modern flat vector illustration in stylized character art: [subject],
> [wardrobe and props], head-and-shoulders portrait centered with generous
> margin, [background] with a faint [motif] silhouette behind [pronoun], clean
> geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat
> design, 1:1 square, no text, no logos, no watermark, no border.

## 3. Age & gender guidance

Appearance cues per age group (used in the subject phrase):

| Key | Group | Age | Cues |
|---|---|---|---|
| `teen` | Teen | 10–17 | 15-year-old, smooth youthful features, slim; clearly a fictional stylized character, never photorealistic |
| `young_adult` | Young Adult | 18–29 | 24-year-old, smooth skin, full hair, bright eyes |
| `adult` | Adult | 30–49 | 38-year-old, confident, subtle smile lines |
| `mature_adult` | Mature Adult | 50–64 | 56-year-old, gentle laugh lines, salt-and-pepper hair/beard (male), soft grey streaks (female) |
| `senior` | Senior | 65–100 | 72-year-old, grey or white hair, warm smile with visible smile lines |

Gender presentation (wardrobe cut and hair only — no stereotyping, keep every
expression warm and neutral-friendly):

| Key | Cues |
|---|---|
| `male` | Male garment cut, short hair; light beard from Adult upward, salt-and-pepper/white beard for Mature Adult/Senior |
| `female` | Female garment cut, longer hair worn as ponytail, bun, braid or loose, per the persona brief |

## 4. Persona briefs

Wardrobe, props, background motif and accent per persona:

| Persona | Wardrobe | Props | Background + motif | Accent |
|---|---|---|---|---|
| Heritage Hunter | Panjabi/kurta and sarees in mustard, rust, olive, cream | Vintage camera, satchel, guidebook | Warm sandstone gradient; terracotta Mughal arch | Mustard / rust |
| Beach Lover | Linen shirts, sundresses, kurtis in sunny yellow, aqua, white, sky blue | Sunglasses, straw hat, shell pendant | Soft aqua-to-teal gradient; setting sun over gentle waves | Aqua / white |
| Adventure Seeker | Windbreakers, trekking jackets, softshells in orange, teal, forest green, navy | Daypack, steel water bottle, coiled rope, walking pole | Deep teal-to-navy gradient; jagged mountain range | Orange / teal |
| Nature Explorer | Field shirts, fleeces and jackets in soft green, sage, olive, forest green | Binoculars, bucket/wide-brim hat, walking stick | Soft sage-to-forest-green gradient; pine forest and rolling hills | Green / sage |
| Urban Explorer | Denim, bomber and blazer jackets in denim blue, charcoal, navy with mustard accents | Headphones, takeaway coffee, tote bag | Deep navy-to-charcoal gradient; skyline with warm-lit windows | Charcoal / mustard |
| Culture Connector | Colorful kurtas, kurtis and sarees in coral, marigold, deep red, cream | Cane market basket, clay tea cup, marigold garland | Warm marigold-to-red gradient; festival bunting and market canopies | Marigold / red |

## 5. The 60 prompts

> Style tail repeated in every prompt: *clean geometric shapes, minimal cel
> shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text,
> no logos, no watermark, no border.*

### Heritage Hunter (01–10)

`01 — Heritage Hunter · Male · Teen` · `static/avatars/heritage_hunter/male-teen.webp` → DB `avatars/heritage_hunter/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing a mustard-yellow panjabi with a slim brown satchel and a small vintage camera on a strap, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`02 — Heritage Hunter · Male · Young Adult` · `static/avatars/heritage_hunter/male-young_adult.webp` → DB `avatars/heritage_hunter/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing a rust-orange kurta with a canvas shoulder bag and a vintage camera around his neck, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`03 — Heritage Hunter · Male · Adult` · `static/avatars/heritage_hunter/male-adult.webp` → DB `avatars/heritage_hunter/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing a deep-ochre panjabi with a leather satchel and a vintage camera slung over one shoulder, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`04 — Heritage Hunter · Male · Mature Adult` · `static/avatars/heritage_hunter/male-mature_adult.webp` → DB `avatars/heritage_hunter/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing an olive panjabi with a lightweight shawl over one shoulder and a rolled-up guidebook in one hand, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`05 — Heritage Hunter · Male · Senior` · `static/avatars/heritage_hunter/male-senior.webp` → DB `avatars/heritage_hunter/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing a cream panjabi with an ochre shawl and a small leather-bound book in one hand, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`06 — Heritage Hunter · Female · Teen` · `static/avatars/heritage_hunter/female-teen.webp` → DB `avatars/heritage_hunter/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with black hair in a simple ponytail and smooth youthful features, wearing a coral kurta with a mustard dupatta and a small camera on a strap, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`07 — Heritage Hunter · Female · Young Adult` · `static/avatars/heritage_hunter/female-young_adult.webp` → DB `avatars/heritage_hunter/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with long black hair and bright eyes, wearing a terracotta saree with a woven shoulder bag and a vintage camera around her neck, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`08 — Heritage Hunter · Female · Adult` · `static/avatars/heritage_hunter/female-adult.webp` → DB `avatars/heritage_hunter/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with black hair in a low bun and subtle smile lines, wearing a maroon kurta set with a rust dupatta and a vintage camera in one hand, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`09 — Heritage Hunter · Female · Mature Adult` · `static/avatars/heritage_hunter/female-mature_adult.webp` → DB `avatars/heritage_hunter/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with hair showing soft grey streaks in a loose bun and gentle laugh lines, wearing an olive-and-rust saree with a cream shawl and a rolled-up guidebook in one hand, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`10 — Heritage Hunter · Female · Senior` · `static/avatars/heritage_hunter/female-senior.webp` → DB `avatars/heritage_hunter/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a neat bun and a warm smile with visible smile lines, wearing a cream saree with a mustard border and a small leather-bound book in one hand, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

### Beach Lover (11–20)

`11 — Beach Lover · Male · Teen` · `static/avatars/beach_lover/male-teen.webp` → DB `avatars/beach_lover/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing a sunny-yellow t-shirt under an open white shirt with sunglasses pushed up on his head, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`12 — Beach Lover · Male · Young Adult` · `static/avatars/beach_lover/male-young_adult.webp` → DB `avatars/beach_lover/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing an open aqua linen shirt over a white tee with a shell necklace and sunglasses on, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`13 — Beach Lover · Male · Adult` · `static/avatars/beach_lover/male-adult.webp` → DB `avatars/beach_lover/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing a white linen shirt with the sleeves rolled up and sunglasses on, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`14 — Beach Lover · Male · Mature Adult` · `static/avatars/beach_lover/male-mature_adult.webp` → DB `avatars/beach_lover/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing a sky-blue polo shirt with a straw hat and sunglasses, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`15 — Beach Lover · Male · Senior` · `static/avatars/beach_lover/male-senior.webp` → DB `avatars/beach_lover/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing a cream linen shirt with a straw hat and sunglasses hanging from his collar, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`16 — Beach Lover · Female · Teen` · `static/avatars/beach_lover/female-teen.webp` → DB `avatars/beach_lover/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with black hair in a simple ponytail and smooth youthful features, wearing a sunny-yellow sundress with a shell necklace and sunglasses pushed up on her head, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`17 — Beach Lover · Female · Young Adult` · `static/avatars/beach_lover/female-young_adult.webp` → DB `avatars/beach_lover/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with long black hair and bright eyes, wearing an aqua sundress with a wide-brim straw hat and sunglasses, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`18 — Beach Lover · Female · Adult` · `static/avatars/beach_lover/female-adult.webp` → DB `avatars/beach_lover/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with black hair in a low bun and subtle smile lines, wearing a white-and-teal maxi dress with a light scarf and a shell pendant, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`19 — Beach Lover · Female · Mature Adult` · `static/avatars/beach_lover/female-mature_adult.webp` → DB `avatars/beach_lover/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with hair showing soft grey streaks in a loose bun and gentle laugh lines, wearing a sky-blue kurti with a cream scarf and a straw sun hat, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`20 — Beach Lover · Female · Senior` · `static/avatars/beach_lover/female-senior.webp` → DB `avatars/beach_lover/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a neat bun and a warm smile with visible smile lines, wearing a cream sundress with a coral scarf and a straw hat, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

### Adventure Seeker (21–30)

`21 — Adventure Seeker · Male · Teen` · `static/avatars/adventure_seeker/male-teen.webp` → DB `avatars/adventure_seeker/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing an orange windbreaker over a grey tee with a small daypack and a baseball cap, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`22 — Adventure Seeker · Male · Young Adult` · `static/avatars/adventure_seeker/male-young_adult.webp` → DB `avatars/adventure_seeker/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing a teal trekking jacket with a daypack, a carabiner clipped to the strap and a steel water bottle in one hand, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`23 — Adventure Seeker · Male · Adult` · `static/avatars/adventure_seeker/male-adult.webp` → DB `avatars/adventure_seeker/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing a forest-green softshell jacket with a compact backpack and a steel water bottle in one hand, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`24 — Adventure Seeker · Male · Mature Adult` · `static/avatars/adventure_seeker/male-mature_adult.webp` → DB `avatars/adventure_seeker/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing a navy trekking vest over a grey base layer with a backpack and a coiled rope over one shoulder, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`25 — Adventure Seeker · Male · Senior` · `static/avatars/adventure_seeker/male-senior.webp` → DB `avatars/adventure_seeker/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing an olive trekking jacket with a light daypack and a wooden walking pole, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`26 — Adventure Seeker · Female · Teen` · `static/avatars/adventure_seeker/female-teen.webp` → DB `avatars/adventure_seeker/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with black hair in a ponytail and smooth youthful features, wearing an orange windbreaker over a grey tee with a small daypack and a baseball cap, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`27 — Adventure Seeker · Female · Young Adult` · `static/avatars/adventure_seeker/female-young_adult.webp` → DB `avatars/adventure_seeker/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with her hair in a high ponytail and bright eyes, wearing a teal trekking jacket with a daypack and a steel water bottle in one hand, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`28 — Adventure Seeker · Female · Adult` · `static/avatars/adventure_seeker/female-adult.webp` → DB `avatars/adventure_seeker/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with her hair in a ponytail and subtle smile lines, wearing a forest-green softshell jacket with a compact backpack and a steel water bottle in one hand, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`29 — Adventure Seeker · Female · Mature Adult` · `static/avatars/adventure_seeker/female-mature_adult.webp` → DB `avatars/adventure_seeker/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with her hair in a low ponytail showing soft grey streaks and gentle laugh lines, wearing a navy trekking vest over a grey base layer with a backpack, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`30 — Adventure Seeker · Female · Senior` · `static/avatars/adventure_seeker/female-senior.webp` → DB `avatars/adventure_seeker/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a bun and a warm smile with visible smile lines, wearing an olive trekking jacket with a light daypack and a wooden walking pole, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

### Nature Explorer (31–40)

`31 — Nature Explorer · Male · Teen` · `static/avatars/nature_explorer/male-teen.webp` → DB `avatars/nature_explorer/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing a soft-green field shirt with a bucket hat and binoculars on a strap around his neck, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`32 — Nature Explorer · Male · Young Adult` · `static/avatars/nature_explorer/male-young_adult.webp` → DB `avatars/nature_explorer/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing a sage fleece jacket with a small canvas satchel and binoculars around his neck, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`33 — Nature Explorer · Male · Adult` · `static/avatars/nature_explorer/male-adult.webp` → DB `avatars/nature_explorer/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing an olive field jacket with a wide-brim hat and binoculars in one hand, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`34 — Nature Explorer · Male · Mature Adult` · `static/avatars/nature_explorer/male-mature_adult.webp` → DB `avatars/nature_explorer/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing a forest-green fleece with a light scarf and binoculars over one shoulder, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`35 — Nature Explorer · Male · Senior` · `static/avatars/nature_explorer/male-senior.webp` → DB `avatars/nature_explorer/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing a sage jacket with a bucket hat and a wooden walking stick, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`36 — Nature Explorer · Female · Teen` · `static/avatars/nature_explorer/female-teen.webp` → DB `avatars/nature_explorer/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with her hair in a ponytail and smooth youthful features, wearing a soft-green field shirt with a bucket hat and binoculars on a strap around her neck, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`37 — Nature Explorer · Female · Young Adult` · `static/avatars/nature_explorer/female-young_adult.webp` → DB `avatars/nature_explorer/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with her hair in a ponytail and bright eyes, wearing a sage fleece jacket with a small canvas satchel and binoculars around her neck, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`38 — Nature Explorer · Female · Adult` · `static/avatars/nature_explorer/female-adult.webp` → DB `avatars/nature_explorer/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with her hair in a braid and subtle smile lines, wearing an olive field jacket with a wide-brim hat and binoculars in one hand, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`39 — Nature Explorer · Female · Mature Adult` · `static/avatars/nature_explorer/female-mature_adult.webp` → DB `avatars/nature_explorer/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with her hair in a bun showing soft grey streaks and gentle laugh lines, wearing a forest-green fleece with a light scarf and binoculars over one shoulder, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`40 — Nature Explorer · Female · Senior` · `static/avatars/nature_explorer/female-senior.webp` → DB `avatars/nature_explorer/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a bun and a warm smile with visible smile lines, wearing a sage jacket with a wide-brim hat and a wooden walking stick, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

### Urban Explorer (41–50)

`41 — Urban Explorer · Male · Teen` · `static/avatars/urban_explorer/male-teen.webp` → DB `avatars/urban_explorer/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing a denim jacket over a white tee with headphones around his neck and a mustard beanie, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`42 — Urban Explorer · Male · Young Adult` · `static/avatars/urban_explorer/male-young_adult.webp` → DB `avatars/urban_explorer/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing a charcoal bomber jacket with headphones around his neck and a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`43 — Urban Explorer · Male · Adult` · `static/avatars/urban_explorer/male-adult.webp` → DB `avatars/urban_explorer/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing a tailored navy jacket with a canvas tote bag over one shoulder and a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`44 — Urban Explorer · Male · Mature Adult` · `static/avatars/urban_explorer/male-mature_adult.webp` → DB `avatars/urban_explorer/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing a smart dark blazer over a light shirt with a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`45 — Urban Explorer · Male · Senior` · `static/avatars/urban_explorer/male-senior.webp` → DB `avatars/urban_explorer/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing a comfortable charcoal shawl-collar jacket with a canvas tote bag and a takeaway tea cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`46 — Urban Explorer · Female · Teen` · `static/avatars/urban_explorer/female-teen.webp` → DB `avatars/urban_explorer/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with her hair in a high ponytail and smooth youthful features, wearing a denim jacket over a yellow tee with headphones around her neck, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`47 — Urban Explorer · Female · Young Adult` · `static/avatars/urban_explorer/female-young_adult.webp` → DB `avatars/urban_explorer/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with long black hair and bright eyes, wearing a chic black blazer with headphones around her neck and a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`48 — Urban Explorer · Female · Adult` · `static/avatars/urban_explorer/female-adult.webp` → DB `avatars/urban_explorer/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with black hair in a low bun and subtle smile lines, wearing a tailored navy blazer with a leather tote bag and a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`49 — Urban Explorer · Female · Mature Adult` · `static/avatars/urban_explorer/female-mature_adult.webp` → DB `avatars/urban_explorer/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with hair showing soft grey streaks in a loose bun and gentle laugh lines, wearing an elegant dark blazer with a silk scarf and a takeaway coffee cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`50 — Urban Explorer · Female · Senior` · `static/avatars/urban_explorer/female-senior.webp` → DB `avatars/urban_explorer/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a neat bun and a warm smile with visible smile lines, wearing a charcoal shawl-collar jacket with a canvas tote bag and a takeaway tea cup in one hand, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

### Culture Connector (51–60)

`51 — Culture Connector · Male · Teen` · `static/avatars/culture_connector/male-teen.webp` → DB `avatars/culture_connector/male-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi boy with short black hair and smooth youthful features, wearing a bright coral kurta with a woven market tote and a small marigold garland around his neck, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`52 — Culture Connector · Male · Young Adult` · `static/avatars/culture_connector/male-young_adult.webp` → DB `avatars/culture_connector/male-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi man with neat black hair and bright eyes, wearing a marigold kurta with a cane market basket and a small clay tea cup in one hand, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`53 — Culture Connector · Male · Adult` · `static/avatars/culture_connector/male-adult.webp` → DB `avatars/culture_connector/male-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi man with short black hair, a light beard and subtle smile lines, wearing a deep-red kurta with a woven shoulder bag and a cane market basket, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`54 — Culture Connector · Male · Mature Adult` · `static/avatars/culture_connector/male-mature_adult.webp` → DB `avatars/culture_connector/male-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi man with salt-and-pepper hair, a trimmed grey-flecked beard and gentle laugh lines, wearing a mustard kurta with a patterned gamcha scarf over one shoulder and a cane basket, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`55 — Culture Connector · Male · Senior` · `static/avatars/culture_connector/male-senior.webp` → DB `avatars/culture_connector/male-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi man with grey hair, a neat white beard and a warm smile with visible smile lines, wearing a cream kurta with a marigold shawl and a clay tea cup in one hand, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind him, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`56 — Culture Connector · Female · Teen` · `static/avatars/culture_connector/female-teen.webp` → DB `avatars/culture_connector/female-teen.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 15-year-old Bangladeshi girl with black hair in a simple ponytail and smooth youthful features, wearing a coral kurti with a marigold dupatta and a woven market tote, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`57 — Culture Connector · Female · Young Adult` · `static/avatars/culture_connector/female-young_adult.webp` → DB `avatars/culture_connector/female-young_adult.webp`

```text
Modern flat vector illustration in stylized character art: a cheerful 24-year-old Bangladeshi woman with long black hair and bright eyes, wearing a vibrant marigold saree with a cane market basket and a clay tea cup in one hand, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`58 — Culture Connector · Female · Adult` · `static/avatars/culture_connector/female-adult.webp` → DB `avatars/culture_connector/female-adult.webp`

```text
Modern flat vector illustration in stylized character art: a confident 38-year-old Bangladeshi woman with black hair in a low bun and subtle smile lines, wearing a red-and-gold saree with a woven shoulder bag and a cane market basket, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`59 — Culture Connector · Female · Mature Adult` · `static/avatars/culture_connector/female-mature_adult.webp` → DB `avatars/culture_connector/female-mature_adult.webp`

```text
Modern flat vector illustration in stylized character art: a warm 56-year-old Bangladeshi woman with hair showing soft grey streaks in a loose bun and gentle laugh lines, wearing a mustard-and-red saree with a patterned shawl and a cane basket, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`60 — Culture Connector · Female · Senior` · `static/avatars/culture_connector/female-senior.webp` → DB `avatars/culture_connector/female-senior.webp`

```text
Modern flat vector illustration in stylized character art: a kind 72-year-old Bangladeshi woman with grey hair in a neat bun and a warm smile with visible smile lines, wearing a cream saree with a marigold border and a clay tea cup in one hand, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind her, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

## 6. Tool notes — Gemini / Imagen and Flux

The prompts above are written to work in both. Differences worth knowing:

**Gemini / Imagen**

- Paste one prompt per message and add: *"Make it a square 1:1 image."*
- Imagen has no negative-prompt or seed field. If unwanted text, borders or
  clutter appear, iterate conversationally: *"same image, remove all text and
  keep the background clean and plain"* — don't edit the prompt file.
- Image-to-image is the strongest consistency tool: once the first avatar of a
  persona is accepted, upload it with *"keep the exact same illustration style,
  character design language and palette; now render:"* + the next prompt for
  the remaining nine.

**Flux**

- Same prompt text, render at 1024×1024.
- Fix one seed per persona to stabilize the look; suggested base seeds:
  Heritage Hunter `1001`, Beach Lover `2001`, Adventure Seeker `3001`,
  Nature Explorer `4001`, Urban Explorer `5001`, Culture Connector `6001`.
  Add the variant number (01–10) to the base seed.
- If the tool supports image prompting/reference, use the first accepted avatar
  of a persona as the style reference for the rest.

**Both**

- Keep the style clause word-for-word across all 60 images; do not paraphrase
  between generations.
- If results drift photorealistic: append *"stylized illustration, fictional
  character, not a photograph"*.
- If the face is clipped or too large: *"pull the camera back, more headroom,
  subject smaller in frame"*.
- Change one thing per iteration; keep the best result and move on.

## 7. Generation order & quality checks

Generate **persona by persona**, in prompt order (male teen → male senior, then
female teen → female senior). Do not jump around: working one persona at a time
keeps that persona's style locked before moving on.

Per-image QA before saving:

- [ ] Face and hair fully inside the center 70% — the rounded-square crop (28px radius at 192px, 44px at 380px) must not clip anything important
- [ ] Shrink test: reads clearly at 192×192 as a kiosk avatar
- [ ] Age and gender read as intended (teen looks like a teen; mature/senior show the cues from §3)
- [ ] Warm friendly expression, eyes open, no distortions in hands/straps
- [ ] Background is the intended gradient + faint motif, nothing busy
- [ ] Zero text, logos, watermarks or borders
- [ ] Palette matches the persona row in §4

Export: resize to 512×512 (LANCZOS), save as WebP quality ~80, target ≤150KB.

## 8. Wiring the finished assets

1. Save each file under the exact path shown in its heading, e.g.
   `static/avatars/heritage_hunter/male-teen.webp`.
2. Register the 60 rows. Either add them in **Admin → PersonaAvatar**
   (persona + gender + age group + image path; leave `is_default` unchecked),
   or run once in `python manage.py shell`:

   ```python
   from apps.experience.models import AgeGroup, Persona, PersonaAvatar

   AGE_KEYS = {
       "Teen": "teen",
       "Young Adult": "young_adult",
       "Adult": "adult",
       "Mature Adult": "mature_adult",
       "Senior": "senior",
   }

   for persona in Persona.objects.all():
       for gender in ("male", "female"):
           for group in AgeGroup.objects.all():
               PersonaAvatar.objects.update_or_create(
                   persona=persona,
                   gender=gender,
                   age_group=group,
                   defaults={
                       "image": f"avatars/{persona.slug}/{gender}-{AGE_KEYS[group.name]}.webp",
                       "is_default": False,
                   },
               )
   ```

3. Collect static files:
   `docker compose exec web python manage.py collectstatic --noinput`
   (or `python manage.py collectstatic --noinput` outside Docker).
4. Verify:
   - exact match: complete a flow as male/female in each age group → the matching `*.webp` is shown
   - `prefer_not_to_say` → the persona `neutral.svg` is shown (existing rows stay `is_default=True`)
   - a deliberately missing file → `avatars/global-default.svg` is shown, never a broken image
5. Update the avatar line in `docs/exhibition-checklist.md` once all 60 are confirmed.

`is_default` stays `False` on the 60 age-specific rows: the fallback chain
(`apps/experience/services/avatars.py`) only uses `is_default` for the
blank-age-group rows, and those existing persona-neutral rows must remain the
defaults.

## 9. Optional appendix — persona neutral avatars (A1–A6)

These replace the placeholder `neutral.svg` files used by
`prefer_not_to_say` (and as the persona-level fallback). File path:
`static/avatars/<persona_slug>/neutral.webp`, DB `avatars/<persona_slug>/neutral.webp`.
If you generate these, update those six existing rows' `image` field and keep
`is_default=True`; skip them and everything keeps working with the SVG
placeholders.

`A1 — Heritage Hunter · Neutral` · `static/avatars/heritage_hunter/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing a mustard panjabi-style tunic with a leather satchel and a vintage camera on a strap, head-and-shoulders portrait centered with generous margin, warm sandstone gradient background with a faint terracotta Mughal arch silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`A2 — Beach Lover · Neutral` · `static/avatars/beach_lover/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing an open white linen shirt over a light tee with sunglasses and a shell pendant, head-and-shoulders portrait centered with generous margin, soft aqua-to-teal gradient background with a faint setting-sun-over-gentle-waves silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`A3 — Adventure Seeker · Neutral` · `static/avatars/adventure_seeker/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing a teal trekking jacket with a daypack and a steel water bottle, head-and-shoulders portrait centered with generous margin, deep teal-to-navy gradient background with a faint jagged mountain range silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`A4 — Nature Explorer · Neutral` · `static/avatars/nature_explorer/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing a sage field jacket with binoculars and a bucket hat, head-and-shoulders portrait centered with generous margin, soft sage-to-forest-green gradient background with a faint pine-forest-and-rolling-hills silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`A5 — Urban Explorer · Neutral` · `static/avatars/urban_explorer/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing a charcoal jacket with headphones around the neck and a takeaway coffee cup, head-and-shoulders portrait centered with generous margin, deep navy-to-charcoal gradient background with a faint skyline-with-warm-lit-windows silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

`A6 — Culture Connector · Neutral` · `static/avatars/culture_connector/neutral.webp`

```text
Modern flat vector illustration in stylized character art: a friendly gender-neutral Bangladeshi adult traveller in their thirties with short black hair, wearing a marigold tunic with a cane market basket, head-and-shoulders portrait centered with generous margin, warm marigold-to-red gradient background with a faint festival-bunting-and-market-canopies silhouette behind them, clean geometric shapes, minimal cel shading, warm friendly smile, crisp edges, flat design, 1:1 square, no text, no logos, no watermark, no border.
```

Optional further upgrade: persona + gender defaults (12 files named
`male.webp` / `female.webp` per persona, registered with a blank age group and
`is_default=True`) would add a graceful fallback if an age-specific file is ever
missing; not required, because the persona-neutral default already covers it.
