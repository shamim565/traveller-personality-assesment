# Avatar Generation Prompts

AI image-generation prompts for the 36 persona avatars
(6 personas × 3 age groups × 2 genders). Avatars are **pre-generated static
assets** — nothing in this repo calls an image model at runtime. Generate the
images off-line (Gemini/Imagen or Flux), save them with the exact filenames
below, then register the rows in **Admin → PersonaAvatar** (or run the snippet
in §8).

**How to use this file:** copy **one prompt at a time**, in the order listed in
§7, and save each result under the file path shown above the prompt. Keep the
style and composition clauses word-for-word across all 36 prompts — that is
what keeps the set visually consistent.

**Never ask the model for a 512×512 WebP.** Image models output PNG/JPEG, not
WebP. Generate a 1:1 square at 1024×1024, then downscale in the export step of
§7 — that is what produces the 512×512 WebP the app ships.

## Quick facts

| | |
|---|---|
| Count | 36 (6 personas × 3 age groups × 2 genders) |
| Style | Modern flat vector avatar illustration, polished modern travel-app character design |
| Composition | Half-body / waist-up, torso cropped by the bottom edge, full square background |
| Generate at | 1024×1024 |
| Export | 512×512 WebP, quality ~80, ≤150KB |
| Tools | Gemini / Imagen or Flux (off-line, one prompt at a time) |

## 1. Asset contract

| Item | Rule |
|---|---|
| Aspect / size | 1:1 square; generate at 1024×1024, export at 512×512 |
| Composition | Half-body waist-up; the torso extends naturally to and is cropped by the bottom edge. No circular frame, no floating bust, no avatar badge, no isolated cutout, no empty space below the body |
| Background | Full square environmental background fills the canvas; subtle persona motif(s) behind the subject |
| Forbidden | Text, letters, numbers, logos, watermarks, borders, frames, circular frames/badges, busy scenes, texture noise |
| Palette | Per-persona palette in §4 |
| Subject | Bangladeshi, warm friendly expression, eyes open |
| File names | `static/avatars/<persona_slug>/<gender>-<age_key>.webp` |
| DB `image` value | `avatars/<persona_slug>/<gender>-<age_key>.webp` |
| Slugs | `heritage_hunter`, `beach_lover`, `adventure_seeker`, `culture_connector`, `nature_explorer`, `urban_explorer` |
| Age keys | `teen`, `young`, `adult` |
| Gender keys | `male`, `female` (`prefer_not_to_say` → persona `neutral.svg`, §9) |

## 2. Shared style block

Every prompt below embeds the same composition rule (shown here in its canonical
form) plus the per-persona description:

> Half-body waist-up composition, torso extending naturally to the bottom edge
> and cropped by the bottom border. No circular frame, no circular background,
> no floating bust, no avatar badge, no isolated cutout, no empty space below
> the body. Full square background fills the canvas. Character centered with
> comfortable space above the head. Clean geometric shapes, minimal cel
> shading, crisp edges, polished modern travel-app character style,
> 1:1 square, no text, no logo, no watermark, no border.

## 3. Age guidance

| Key | Group | Age | Cues |
|---|---|---|---|
| `teen` | Teen | 10–20 | 14–15-year-old, smooth youthful features |
| `young` | Young | 21–40 | 25–27-year-old, bright eyes, full hair |
| `adult` | Adult | 41+ | Mature, experienced, subtle smile lines |

Gender presentation (wardrobe cut and hair only — no stereotyping, keep every
expression warm and friendly):

| Key | Cues |
|---|---|
| `male` | Male garment cut, short hair |
| `female` | Female garment cut, longer hair worn loose, tied or styled per the persona brief |

## 4. Persona briefs

Wardrobe, props, background motifs and palette per persona:

| Persona | Wardrobe | Props | Background + motifs | Palette |
|---|---|---|---|---|
| Heritage Hunter | Mustard/olive casual shirts; elegant earth-toned travel shirts with a lightweight scarf (adult) | Crossbody travel bag, folded heritage map, guidebook; reading glasses (adult) | Bengali terracotta temple, ancient arches, palace ruins, archaeological structures | Warm earthy brown, antique gold, mustard, rust, muted orange |
| Beach Lover | Aqua/turquoise beach shirts over white tees; teal linen shirt/blouse (adult) | Sunglasses on head, shell bracelet/necklace, subtle beach accessories | Ocean waves, sandy shoreline, palm leaves, seashells, glowing sunset | Aqua, turquoise, coral, sand, golden yellow |
| Adventure Seeker | Sporty to premium trekking jackets in orange and charcoal with backpack straps; adventure cap | Backpack straps, sports watch, sunglasses on head, outdoor gear | Mountain peaks, rocky trails, suspension bridge, dramatic clouds, distant paraglider | Burnt orange, crimson, charcoal, navy, deep teal |
| Culture Connector | Colorful contemporary outfits with subtle Bengali textile patterns; woven accessory | Small camera (hand or neck), woven accessory | Festival lanterns, market stalls, performers, crafts, decorative lights, food stalls | Magenta/purple, saffron, burgundy, turquoise, gold |
| Nature Explorer | Forest-green/teal outdoor shirts and trekking jackets with daypack straps | Binoculars around the neck, small daypack, reusable steel water bottle | Forest trees, rolling hills, river, waterfall, birds, tropical leaves | Forest green, emerald, olive, teal, sky/cool blue |
| Urban Explorer | Modern streetwear/travel jackets; smart-casual dark navy (adult) | Headphones around the neck, compact crossbody bag, smartphone; wireless earbuds (adult) | Contemporary skyline, metro train/line, café signs, street lights, subtle neon, geometric buildings | Electric blue, indigo, violet, cyan, dark navy |

## 5. The 36 prompts

### Heritage Hunter (01–06)

`01 — Heritage Hunter · Teen · Male` · `static/avatars/heritage_hunter/male-teen.webp` → DB `avatars/heritage_hunter/male-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi boy, Heritage Hunter persona, curious, observant, and fascinated by history. He wears a mustard-yellow casual shirt with a small crossbody travel bag and holds a folded heritage-site map. His personality should suggest someone who enjoys old architecture, monuments, museums, historical stories, and archaeological sites. Background features subtle silhouettes of a Bengali terracotta temple, ancient arches, palace ruins, and historic architecture. Warm earthy brown, antique gold, mustard, and muted orange palette. Friendly youthful expression with curious eyes. Half-body waist-up composition, character shown from approximately the waist upward, torso extending naturally all the way to the bottom edge and cropped by the bottom border. No circular frame, no circular background, no floating bust, no avatar badge, no isolated cutout, no empty space below the body. Full square background fills the canvas. Character centered with comfortable space above the head. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`02 — Heritage Hunter · Teen · Female` · `static/avatars/heritage_hunter/female-teen.webp` → DB `avatars/heritage_hunter/female-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi girl, Heritage Hunter persona, curious, thoughtful, and fascinated by history. She wears a mustard and olive casual outfit with a small crossbody travel bag and holds a folded heritage map. Her personality should suggest someone who loves monuments, museums, old buildings, archaeology, and learning the stories behind historical places. Background features subtle silhouettes of a Bengali terracotta temple, ancient archways, palace ruins, and heritage architecture. Warm earthy brown, antique gold, mustard, olive, and muted orange palette. Friendly youthful expression with bright curious eyes. Half-body waist-up composition, torso extending naturally to the bottom edge of the square image and cropped by the bottom border. No circular frame, no circle behind the character, no floating bust, no badge shape, no empty space below the body. Full square environmental background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`03 — Heritage Hunter · Young · Male` · `static/avatars/heritage_hunter/male-young.webp` → DB `avatars/heritage_hunter/male-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi man, Heritage Hunter persona, thoughtful, intellectually curious, and interested in history. He wears an olive overshirt over a neutral T-shirt with a leather-style crossbody travel bag and holds a small heritage guidebook. His personality should clearly represent someone who enjoys ancient civilizations, architecture, monuments, museums, and historical exploration. Background features subtle silhouettes of a Bengali terracotta temple, historic palace, archaeological ruins, and old decorative arches. Warm brown, antique gold, rust, olive, and muted orange palette. Calm, fascinated expression. Half-body waist-up composition, torso reaching and naturally cropping at the bottom edge of the square image. No circular frame, no circular background, no floating bust, no cutout badge, no empty lower margin. Full environmental background fills the canvas. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`04 — Heritage Hunter · Young · Female` · `static/avatars/heritage_hunter/female-young.webp` → DB `avatars/heritage_hunter/female-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi woman, Heritage Hunter persona, intelligent, thoughtful, and deeply curious about history. She wears an elegant olive overshirt with a neutral inner top, a small crossbody travel bag, and holds a heritage guidebook. She should represent someone who enjoys museums, monuments, architecture, archaeology, old cities, and historical stories. Background features subtle silhouettes of a Bengali terracotta temple, palace architecture, historical archways, and archaeological structures. Warm brown, antique gold, olive, rust, and muted orange palette. Calm, interested, intelligent expression. Half-body waist-up composition, torso extending fully to and naturally cropped by the bottom edge. No circle, no circular backdrop, no floating portrait, no badge frame, and no empty space beneath the body. Full square background fills the canvas. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`05 — Heritage Hunter · Adult · Male` · `static/avatars/heritage_hunter/male-adult.webp` → DB `avatars/heritage_hunter/male-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi man, Heritage Hunter persona, mature, knowledgeable, and deeply interested in history. He wears an elegant earth-toned travel shirt with a lightweight scarf and carries a heritage guidebook, with subtle reading glasses as an accessory. He represents someone who appreciates architecture, archaeology, museums, historical monuments, and cultural preservation. Background features silhouettes of an ancient Bengali palace, terracotta temple, historical arches, and archaeological structures. Rich earthy brown, antique gold, burgundy, and muted orange palette. Warm, reflective, experienced expression. Half-body waist-up composition, torso naturally touching and cropped by the bottom edge. No circular frame, no floating bust, no circular graphic behind the character, no empty lower space. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app avatar style, 1:1 square, no text, no logo, no watermark, no border.
```

`06 — Heritage Hunter · Adult · Female` · `static/avatars/heritage_hunter/female-adult.webp` → DB `avatars/heritage_hunter/female-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi woman, Heritage Hunter persona, mature, knowledgeable, graceful, and deeply interested in history and cultural heritage. She wears an elegant earth-toned travel outfit with a lightweight scarf and carries a heritage guidebook. She should represent someone who enjoys historic architecture, museums, ancient settlements, monuments, and cultural preservation. Background features subtle silhouettes of a Bengali palace, terracotta temple, historical arches, and archaeological ruins. Rich earthy brown, antique gold, burgundy, and muted orange palette. Warm, thoughtful, experienced expression. Half-body waist-up composition, torso extending naturally to and cropped by the bottom edge. No circle, no floating portrait, no badge-style frame, no empty space below the character. Background fills the full square canvas. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

### Beach Lover (07–12)

`07 — Beach Lover · Teen · Male` · `static/avatars/beach_lover/male-teen.webp` → DB `avatars/beach_lover/male-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi boy, Beach Lover persona, cheerful, carefree, playful, and energetic. He wears a bright aqua beach shirt over a white T-shirt, with sunglasses resting on his head and a small shell bracelet. He should clearly represent someone who loves swimming, sunshine, sandy beaches, ocean waves, and seaside holidays. Background features gentle ocean waves, sandy shoreline, palm leaves, seashells, and a glowing sunset. Fresh aqua, turquoise, coral, and golden-yellow palette. Big relaxed smile. Half-body waist-up composition, torso reaching naturally to the bottom edge and cropped there. No circular frame, no circular background, no floating bust, no badge shape, no empty lower margin. Full square seaside background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`08 — Beach Lover · Teen · Female` · `static/avatars/beach_lover/female-teen.webp` → DB `avatars/beach_lover/female-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi girl, Beach Lover persona, cheerful, sunny, carefree, and playful. She wears a bright turquoise beach top with a light open overshirt, sunglasses resting on her head, and a subtle shell bracelet. She should represent someone who loves beaches, swimming, sea breezes, sunsets, and tropical vacations. Background features ocean waves, sandy shoreline, palm leaves, seashells, and a glowing sunset. Fresh aqua, turquoise, coral, peach, and golden-yellow palette. Bright, joyful smile. Half-body waist-up composition, torso extending to and naturally cropped at the bottom edge. No circle, no floating bust, no badge frame, no empty space beneath the body. Full square background fills the canvas. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`09 — Beach Lover · Young · Male` · `static/avatars/beach_lover/male-young.webp` → DB `avatars/beach_lover/male-young.webp`

```text
Modern flat vector avatar illustration of a 25-year-old Bangladeshi man, Beach Lover persona, relaxed, social, cheerful, and easygoing. He wears an open aqua linen shirt over a white T-shirt, sunglasses, and a subtle shell necklace. He represents someone who enjoys swimming, sunsets, coastal food, tropical beaches, and slow seaside vacations. Background features turquoise ocean waves, sandy beach, palm trees, and a setting sun. Aqua, teal, coral, sand, and warm gold palette. Relaxed friendly smile. Half-body waist-up composition, lower torso naturally touching and cropped by the bottom border. No circular avatar frame, no circle backdrop, no floating portrait, no empty lower space. Full square beach background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`10 — Beach Lover · Young · Female` · `static/avatars/beach_lover/female-young.webp` → DB `avatars/beach_lover/female-young.webp`

```text
Modern flat vector avatar illustration of a 25-year-old Bangladeshi woman, Beach Lover persona, relaxed, cheerful, stylish, and social. She wears a lightweight teal beach shirt over a simple white top, sunglasses on her head, and a subtle shell necklace or bracelet. She represents someone who loves swimming, sandy beaches, seaside cafés, sunsets, tropical holidays, and relaxed coastal travel. Background features turquoise ocean waves, palm trees, sandy shoreline, and a warm setting sun. Aqua, turquoise, coral, sand, and golden palette. Warm relaxed smile. Half-body waist-up composition, torso extends completely to and is cropped by the bottom edge. No circular frame, no floating bust, no badge, no empty area under the torso. Full square coastal background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`11 — Beach Lover · Adult · Male` · `static/avatars/beach_lover/male-adult.webp` → DB `avatars/beach_lover/male-adult.webp`

```text
Modern flat vector avatar illustration of a 41-year-old Bangladeshi man, Beach Lover persona, calm, relaxed, sophisticated, and comfortable. He wears a light breathable teal linen shirt with stylish sunglasses. He represents someone who appreciates quiet beaches, ocean views, coastal dining, sunsets, and peaceful seaside resorts. Background features calm waves, tropical palm leaves, sandy coastline, and warm sunset light. Deep aqua, turquoise, sand, coral, and sunset-orange palette. Peaceful confident smile. Half-body waist-up composition, torso extending naturally to the bottom edge and cropped there. No circular frame, no floating avatar, no circle backdrop, no empty space below the body. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`12 — Beach Lover · Adult · Female` · `static/avatars/beach_lover/female-adult.webp` → DB `avatars/beach_lover/female-adult.webp`

```text
Modern flat vector avatar illustration of a 41-year-old Bangladeshi woman, Beach Lover persona, calm, elegant, relaxed, and sophisticated. She wears a lightweight teal linen blouse with stylish sunglasses and subtle beach-inspired accessories. She represents someone who loves calm beaches, ocean views, relaxing resorts, sunsets, coastal dining, and peaceful vacations. Background features calm ocean waves, palm leaves, sandy beach, and warm sunset horizon. Deep aqua, turquoise, sand, coral, and sunset-orange palette. Peaceful, confident expression. Half-body waist-up composition with lower torso naturally touching and cropped by the bottom border. No circular frame, no circular background, no floating portrait, no empty space underneath. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

### Adventure Seeker (13–18)

`13 — Adventure Seeker · Teen · Male` · `static/avatars/adventure_seeker/male-teen.webp` → DB `avatars/adventure_seeker/male-teen.webp`

```text
Modern flat vector avatar illustration of a 15-year-old Bangladeshi boy, Adventure Seeker persona, energetic, fearless, excited, and active. He wears a sporty trekking jacket with backpack straps and an adventure cap. He represents hiking, climbing, rafting, camping, mountain trails, and thrilling outdoor experiences. Background features mountain peaks, rocky trails, rope bridge, and dramatic clouds. Bold orange, red, charcoal, teal, and navy palette. Excited determined expression. Half-body waist-up composition, torso reaches and is naturally cropped by the bottom edge. No circle, no circular frame, no floating bust, no badge shape, no empty lower margin. Full square adventurous landscape background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`14 — Adventure Seeker · Teen · Female` · `static/avatars/adventure_seeker/female-teen.webp` → DB `avatars/adventure_seeker/female-teen.webp`

```text
Modern flat vector avatar illustration of a 15-year-old Bangladeshi girl, Adventure Seeker persona, energetic, fearless, confident, and excited. She wears a sporty orange-and-teal trekking jacket with backpack straps and a lightweight adventure cap. She should clearly represent hiking, mountain exploration, rafting, climbing, camping, and exciting outdoor challenges. Background features dramatic mountain peaks, rocky trail, suspension bridge, and clouds. Bold orange, crimson, charcoal, teal, and navy palette. Brave, enthusiastic expression. Half-body waist-up composition, torso touching and cropped naturally at the bottom edge. No circular frame, no floating bust, no badge-style presentation, no empty space below the character. Full square mountain background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`15 — Adventure Seeker · Young · Male` · `static/avatars/adventure_seeker/male-young.webp` → DB `avatars/adventure_seeker/male-young.webp`

```text
Modern flat vector avatar illustration of a 27-year-old Bangladeshi man, Adventure Seeker persona, confident, energetic, fearless, and adventurous. He wears a rugged orange-and-charcoal trekking jacket with backpack straps, sports watch, and adventure sunglasses resting on his head. Background features dramatic mountains, rocky trail, suspension bridge, and distant paraglider. Burnt orange, crimson, charcoal, deep blue, and teal palette. Determined enthusiastic expression. Half-body waist-up composition, torso extending naturally to the bottom edge and cropped there. No circular frame, no circle background, no floating portrait, no empty lower space. Full square adventure environment. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`16 — Adventure Seeker · Young · Female` · `static/avatars/adventure_seeker/female-young.webp` → DB `avatars/adventure_seeker/female-young.webp`

```text
Modern flat vector avatar illustration of a 27-year-old Bangladeshi woman, Adventure Seeker persona, confident, athletic, energetic, and fearless. She wears a rugged orange-and-charcoal trekking jacket with backpack straps, sports watch, and adventure sunglasses resting on her head. She represents hiking, trekking, climbing, rafting, camping, and high-energy outdoor travel. Background features rugged mountain peaks, rocky trails, a suspension bridge, and distant paraglider. Burnt orange, crimson, charcoal, teal, and deep blue palette. Determined, enthusiastic expression. Half-body waist-up composition, torso naturally reaches and crops at the bottom edge. No circle, no circular frame, no floating bust, no avatar badge, no empty lower area. Full square environment. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`17 — Adventure Seeker · Adult · Male` · `static/avatars/adventure_seeker/male-adult.webp` → DB `avatars/adventure_seeker/male-adult.webp`

```text
Modern flat vector avatar illustration of a 43-year-old Bangladeshi man, Adventure Seeker persona, experienced, strong, calm, and adventurous. He wears a premium trekking jacket with sturdy backpack straps, sports watch, and practical outdoor gear. Background features rugged mountains, high-altitude trails, rocky cliffs, and a suspension bridge. Burnt orange, dark red, slate gray, navy, and deep teal palette. Confident, composed expression. Half-body waist-up composition, lower torso naturally touching and cropped by the bottom edge. No circular frame, no floating avatar, no circle backdrop, no empty area beneath the torso. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`18 — Adventure Seeker · Adult · Female` · `static/avatars/adventure_seeker/female-adult.webp` → DB `avatars/adventure_seeker/female-adult.webp`

```text
Modern flat vector avatar illustration of a 43-year-old Bangladeshi woman, Adventure Seeker persona, experienced, capable, confident, and adventurous. She wears a premium outdoor trekking jacket with strong backpack straps, sports watch, and practical adventure equipment. She represents challenging hikes, expeditions, rafting, remote destinations, and mountain travel. Background features rugged mountain ranges, cliffs, trail, and suspension bridge. Burnt orange, dark red, slate gray, navy, and teal palette. Calm, confident expression. Half-body waist-up composition, torso extending naturally to and cropped by the bottom edge. No circular frame, no floating portrait, no badge shape, no empty space below. Full square adventure background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

### Culture Connector (19–24)

`19 — Culture Connector · Teen · Male` · `static/avatars/culture_connector/male-teen.webp` → DB `avatars/culture_connector/male-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi boy, Culture Connector persona, friendly, expressive, social, and curious about people and traditions. He wears a colorful contemporary outfit with subtle Bengali-inspired patterns and carries a small camera. Background features festival decorations, lanterns, musical instruments, local market stalls, and people interacting. Vibrant magenta, purple, orange, turquoise, and gold palette. Warm youthful smile. Half-body waist-up composition, torso naturally reaches and is cropped by the bottom edge. No circular frame, no floating bust, no badge, no empty lower space. Full square cultural background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`20 — Culture Connector · Teen · Female` · `static/avatars/culture_connector/female-teen.webp` → DB `avatars/culture_connector/female-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi girl, Culture Connector persona, friendly, expressive, cheerful, and curious about cultures and people. She wears a colorful contemporary outfit with subtle Bengali textile patterns and carries a small camera. Background features festive lanterns, local crafts, music, market stalls, and people socializing. Vibrant purple, magenta, saffron, turquoise, and orange palette. Bright welcoming smile. Half-body waist-up composition with torso extending naturally to the bottom edge and cropped there. No circle, no floating avatar, no badge frame, no empty space beneath the body. Full square festival background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`21 — Culture Connector · Young · Male` · `static/avatars/culture_connector/male-young.webp` → DB `avatars/culture_connector/male-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi man, Culture Connector persona, outgoing, warm, curious, and socially confident. He wears a stylish contemporary outfit with subtle Bengali patterns, a small camera around his neck, and a colorful woven accessory. Background features cultural festival scenes, food stalls, lanterns, musicians, crafts, and people interacting. Vibrant purple, magenta, saffron, turquoise, and warm orange palette. Open welcoming expression. Half-body waist-up composition, torso reaching naturally to the bottom edge. No circular frame, no floating bust, no badge, no empty lower margin. Full square cultural background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`22 — Culture Connector · Young · Female` · `static/avatars/culture_connector/female-young.webp` → DB `avatars/culture_connector/female-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi woman, Culture Connector persona, outgoing, warm, expressive, and socially curious. She wears a stylish modern outfit with subtle Bengali textile patterns, a travel camera around her neck, and a woven accessory. She represents meeting locals, traditional food, festivals, music, arts, crafts, and meaningful cultural exchange. Background features lanterns, festival decorations, local performers, food stalls, and social gatherings. Vibrant purple, magenta, saffron, turquoise, and warm orange palette. Friendly engaging expression. Half-body waist-up composition, torso extends all the way to and is cropped by the bottom border. No circle, no circular backdrop, no floating portrait, no empty lower space. Full square cultural background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`23 — Culture Connector · Adult · Male` · `static/avatars/culture_connector/male-adult.webp` → DB `avatars/culture_connector/male-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi man, Culture Connector persona, warm, approachable, cultured, and genuinely interested in people. He wears an elegant contemporary outfit with understated Bengali textile details and a travel camera strap. Background features traditional performers, artisan markets, decorative lights, local cuisine, and people gathering together. Rich purple, saffron, burgundy, turquoise, and gold palette. Mature welcoming expression. Half-body waist-up composition, lower torso naturally touches and crops at the bottom edge. No circular frame, no floating avatar, no empty space beneath the character. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`24 — Culture Connector · Adult · Female` · `static/avatars/culture_connector/female-adult.webp` → DB `avatars/culture_connector/female-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi woman, Culture Connector persona, warm, elegant, approachable, and culturally curious. She wears a contemporary outfit with tasteful Bengali textile details and a camera strap visible. She represents local traditions, cuisine, arts, music, festivals, crafts, and meaningful conversations with communities. Background features artisan markets, traditional performers, decorative lights, food stalls, and social gatherings. Rich purple, saffron, burgundy, turquoise, and warm gold palette. Mature, welcoming expression. Half-body waist-up composition with torso extending naturally to the bottom edge and cropped there. No circular frame, no circle backdrop, no floating portrait, no empty space underneath. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

### Nature Explorer (25–30)

`25 — Nature Explorer · Teen · Male` · `static/avatars/nature_explorer/male-teen.webp` → DB `avatars/nature_explorer/male-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi boy, Nature Explorer persona, curious, peaceful, enthusiastic, and fascinated by wildlife. He wears a forest-green outdoor shirt with a small daypack and binoculars around his neck. Background features lush forest trees, green hills, flying birds, river, leaves, and waterfall. Fresh forest green, emerald, teal, and sky-blue palette. Bright curious expression. Half-body waist-up composition, torso naturally touching and cropped by the bottom edge. No circle, no floating bust, no avatar badge, no empty lower area. Full square nature background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`26 — Nature Explorer · Teen · Female` · `static/avatars/nature_explorer/female-teen.webp` → DB `avatars/nature_explorer/female-teen.webp`

```text
Modern flat vector avatar illustration of a 14-year-old Bangladeshi girl, Nature Explorer persona, curious, peaceful, adventurous, and fascinated by wildlife. She wears a forest-green outdoor jacket with a small daypack and binoculars around her neck. She represents forests, birds, wildlife, waterfalls, rivers, and quiet outdoor discovery. Background features lush trees, rolling hills, river, birds, tropical leaves, and waterfall. Fresh green, emerald, teal, and sky-blue palette. Bright, peaceful expression. Half-body waist-up composition with torso extending completely to the bottom edge and cropped there. No circular frame, no floating portrait, no badge, no empty lower margin. Full square natural environment. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`27 — Nature Explorer · Young · Male` · `static/avatars/nature_explorer/male-young.webp` → DB `avatars/nature_explorer/male-young.webp`

```text
Modern flat vector avatar illustration of a 27-year-old Bangladeshi man, Nature Explorer persona, calm, adventurous, environmentally conscious, and curious. He wears a deep teal trekking jacket with daypack straps, binoculars around his neck, and holds a reusable steel water bottle. Background features tropical forest, hills, birds, waterfall, river, and large leaves. Deep green, emerald, teal, and cool blue palette. Peaceful enthusiastic expression. Half-body waist-up composition, lower torso naturally touching and cropped by the bottom edge. No circular frame, no circular background, no floating bust, no empty lower space. Full square forest background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`28 — Nature Explorer · Young · Female` · `static/avatars/nature_explorer/female-young.webp` → DB `avatars/nature_explorer/female-young.webp`

```text
Modern flat vector avatar illustration of a 27-year-old Bangladeshi woman, Nature Explorer persona, calm, adventurous, curious, and environmentally conscious. She wears a deep teal trekking jacket with daypack straps, binoculars around her neck, and holds a reusable water bottle. She represents wildlife exploration, forests, waterfalls, eco-tourism, birdwatching, and remote natural landscapes. Background features tropical forest, hills, river, waterfall, birds, and large leaves. Deep green, emerald, teal, and cool blue palette. Peaceful, enthusiastic expression. Half-body waist-up composition, torso naturally extends to and is cropped by the bottom border. No circle, no floating portrait, no badge frame, no empty space beneath the body. Full square nature background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`29 — Nature Explorer · Adult · Male` · `static/avatars/nature_explorer/male-adult.webp` → DB `avatars/nature_explorer/male-adult.webp`

```text
Modern flat vector avatar illustration of a 43-year-old Bangladeshi man, Nature Explorer persona, experienced, calm, observant, and deeply appreciative of nature. He wears a practical forest-green outdoor jacket with binoculars and lightweight backpack straps. Background features dense forest, winding river, hills, birds, waterfall, and tropical vegetation. Rich forest green, olive, emerald, teal, and cool blue palette. Calm content expression. Half-body waist-up composition, torso reaches naturally to and crops at the bottom edge. No circular frame, no floating bust, no empty lower space. Full square background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`30 — Nature Explorer · Adult · Female` · `static/avatars/nature_explorer/female-adult.webp` → DB `avatars/nature_explorer/female-adult.webp`

```text
Modern flat vector avatar illustration of a 43-year-old Bangladeshi woman, Nature Explorer persona, experienced, calm, observant, and deeply connected to nature. She wears a practical forest-green outdoor jacket with binoculars and lightweight backpack straps. She represents wildlife, eco-tourism, forests, scenic landscapes, rivers, birdwatching, and nature photography. Background features dense forest, river, hills, birds, waterfall, and tropical vegetation. Rich forest green, olive, emerald, teal, and cool blue palette. Peaceful, experienced expression. Half-body waist-up composition, lower torso extending naturally to and cropped by the bottom edge. No circular frame, no floating portrait, no badge shape, no empty space below. Full square natural background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

### Urban Explorer (31–36)

`31 — Urban Explorer · Teen · Male` · `static/avatars/urban_explorer/male-teen.webp` → DB `avatars/urban_explorer/male-teen.webp`

```text
Modern flat vector avatar illustration of a 15-year-old Bangladeshi boy, Urban Explorer persona, trendy, energetic, curious, and tech-savvy. He wears a modern streetwear jacket, casual headphones around his neck, and a compact crossbody bag. He represents exploring city streets, cafés, shopping areas, entertainment venues, technology, and modern architecture. Background features a vibrant skyline, metro train, café signs, street lights, and geometric buildings. Electric blue, violet, cyan, and dark navy palette. Confident youthful smile. Half-body waist-up composition, torso extending naturally to the bottom edge and cropped there. No circular frame, no floating bust, no badge, no empty lower area. Full square city background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app style, 1:1 square, no text, no logo, no watermark, no border.
```

`32 — Urban Explorer · Teen · Female` · `static/avatars/urban_explorer/female-teen.webp` → DB `avatars/urban_explorer/female-teen.webp`

```text
Modern flat vector avatar illustration of a 15-year-old Bangladeshi girl, Urban Explorer persona, trendy, energetic, curious, and tech-savvy. She wears a modern streetwear jacket with headphones around her neck and a compact crossbody bag. She represents cafés, shopping streets, city attractions, technology, modern architecture, and discovering hidden urban places. Background features modern skyline, metro train, café signs, street lights, and geometric architecture. Electric blue, violet, cyan, and dark navy palette. Confident, curious smile. Half-body waist-up composition, lower torso naturally touching and cropped at the bottom border. No circle, no floating avatar, no badge frame, no empty space beneath the body. Full square urban background. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`33 — Urban Explorer · Young · Male` · `static/avatars/urban_explorer/male-young.webp` → DB `avatars/urban_explorer/male-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi man, Urban Explorer persona, stylish, independent, energetic, curious, and tech-savvy. He wears a modern navy streetwear jacket with a crossbody bag, wireless headphones around his neck, and a smartphone subtly visible. He represents neighborhoods, cafés, nightlife, architecture, shopping, technology, and hidden city experiences. Background features contemporary skyline, metro line, cafés, subtle neon signs, and shopping streets. Electric blue, indigo, violet, cyan, and dark navy palette. Confident interested expression. Half-body waist-up composition, torso extends naturally to and is cropped by the bottom edge. No circular frame, no circular backdrop, no floating portrait, no empty lower margin. Full square urban background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
```

`34 — Urban Explorer · Young · Female` · `static/avatars/urban_explorer/female-young.webp` → DB `avatars/urban_explorer/female-young.webp`

```text
Modern flat vector avatar illustration of a 26-year-old Bangladeshi woman, Urban Explorer persona, stylish, independent, energetic, curious, and tech-savvy. She wears a modern navy streetwear jacket with a compact crossbody bag, wireless headphones, and a smartphone subtly visible. She represents discovering neighborhoods, cafés, nightlife, shopping districts, architecture, technology, and urban culture. Background features contemporary skyline, metro line, cafés, modern buildings, and subtle neon signs. Electric blue, indigo, violet, cyan, and dark navy palette. Confident social expression. Half-body waist-up composition, lower torso naturally touching and cropped by the bottom edge. No circular frame, no floating bust, no avatar badge, no empty space below. Full square city environment. Clean geometric shapes, minimal cel shading, crisp edges, polished travel-app design, 1:1 square, no text, no logo, no watermark, no border.
```

`35 — Urban Explorer · Adult · Male` · `static/avatars/urban_explorer/male-adult.webp` → DB `avatars/urban_explorer/male-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi man, Urban Explorer persona, sophisticated, confident, curious, and comfortable navigating modern cities. He wears a smart-casual dark navy travel jacket with a minimalist crossbody bag and wireless earbuds. He represents architecture, restaurants, museums, cafés, neighborhoods, shopping districts, technology, nightlife, and public transport. Background features sophisticated skyline, metro station, modern buildings, café terrace, and illuminated urban streets. Deep navy, royal blue, violet, cyan, and subtle silver palette. Calm confident expression. Half-body waist-up composition, torso extending naturally all the way to the bottom border and cropped there. No circular frame, no floating portrait, no badge frame, no empty lower space. Full square city background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character style, 1:1 square, no text, no logo, no watermark, no border.
```

`36 — Urban Explorer · Adult · Female` · `static/avatars/urban_explorer/female-adult.webp` → DB `avatars/urban_explorer/female-adult.webp`

```text
Modern flat vector avatar illustration of a 42-year-old Bangladeshi woman, Urban Explorer persona, sophisticated, confident, stylish, curious, and comfortable navigating modern cities. She wears a smart-casual dark navy travel jacket with a minimalist crossbody bag and wireless earbuds. She represents architecture, museums, restaurants, cafés, shopping districts, technology, nightlife, neighborhoods, and modern city culture. Background features a sophisticated skyline, metro station, modern architecture, café terrace, and illuminated streets. Deep navy, royal blue, violet, cyan, and subtle silver palette. Calm confident expression. Half-body waist-up composition, torso naturally reaches the bottom edge and is cropped by the bottom border. No circle, no circular background, no floating bust, no badge shape, no empty space underneath. Full square city background. Clean geometric shapes, minimal cel shading, crisp edges, polished modern travel-app character design, 1:1 square, no text, no logo, no watermark, no border.
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
  the remaining five.

**Flux**

- Same prompt text, render at 1024×1024.
- Fix one seed per persona to stabilize the look; suggested base seeds:
  Heritage Hunter `1001`, Beach Lover `2001`, Adventure Seeker `3001`,
  Culture Connector `4001`, Nature Explorer `5001`, Urban Explorer `6001`.
  Add the variant number to the base seed. Not every host exposes `seed` —
  Cloudflare Workers AI rejects it despite the docs schema, so use a host that
  supports it if reproducibility matters.
- If the tool supports image prompting/reference, use the first accepted avatar
  of a persona as the style reference for the rest.

**Both**

- Keep the composition rule word-for-word across all 36 images; do not
  paraphrase between generations.
- Don't request a WebP or 512×512 render: generate the largest 1:1 square the
  tool offers (1024×1024) and convert with the export step in §7.
- If results drift photorealistic: append *"stylized illustration, fictional
  character, not a photograph"*.
- If the torso does not reach the bottom edge, or a circle/badge appears:
  append *"half-body waist-up, torso cropped by the bottom edge, no circle, no
  floating bust, full square background"*.
- Change one thing per iteration; keep the best result and move on.

## 7. Generation order & quality checks

Generate **persona by persona**, in prompt order (teen male → teen female, young
male → young female, then adult male → adult female). Do not jump around:
working one persona at a time keeps that persona's style locked before moving
on.

Per-image QA before saving:

- [ ] Half-body waist-up: torso reaches the bottom edge, no empty space under the body, no circle/badge/floating bust
- [ ] Head and hair fully inside the frame with comfortable space above
- [ ] Shrink test: reads clearly at 192×192 as a kiosk avatar
- [ ] Age and gender read as intended (teen looks like a teen; adult shows the cues from §3)
- [ ] Warm friendly expression, eyes open, no distortions in hands/straps
- [ ] Background is the intended persona motif(s), full square, nothing busy
- [ ] Zero text, logos, watermarks or borders
- [ ] Palette matches the persona row in §4

### Export to 512×512 WebP

This step — not the prompt — is what produces the shipped file. Center-crop to
a square in case the model returned a non-square frame, resize with LANCZOS and
save as WebP:

```python
from pathlib import Path
from PIL import Image

SRC = Path("generated.png")  # whatever the model produced
DST = Path("static/avatars/heritage_hunter/male-teen.webp")

image = Image.open(SRC).convert("RGB")
side = min(image.size)
left, top = (image.width - side) // 2, (image.height - side) // 2
image = image.crop((left, top, left + side, top + side))
image = image.resize((512, 512), Image.LANCZOS)
DST.parent.mkdir(parents=True, exist_ok=True)
image.save(DST, "WEBP", quality=80, method=6)

size_kb = DST.stat().st_size / 1024
assert size_kb <= 150, f"{DST} is {size_kb:.0f}KB, over the 150KB target"
```

The backgrounds are opaque, so `RGB` is correct; use `convert("RGBA")` only if
an avatar ever needs transparency.

## 8. Wiring the finished assets

1. Save each file under the exact path shown in its heading, e.g.
   `static/avatars/heritage_hunter/male-teen.webp`.
2. Register the 36 rows. Either add them in **Admin → PersonaAvatar**
   (persona + gender + age group + image path; leave `is_default` unchecked),
   or run once in `python manage.py shell`:

   ```python
   from apps.experience.models import AgeGroup, Persona, PersonaAvatar

   AGE_KEYS = {
       "Teen": "teen",
       "Young": "young",
       "Adult": "adult",
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

`is_default` stays `False` on the 36 age-specific rows: the fallback chain
(`apps/experience/services/avatars.py`) only uses `is_default` for the
blank-age-group rows, and the existing persona-neutral rows remain the defaults.

## 9. Persona neutral placeholders

`prefer_not_to_say` falls back to each persona's existing `neutral.svg` via the
resolver chain in `apps/experience/services/avatars.py`. No new assets are
required; optionally regenerate those six placeholders later in the same
half-body style.
