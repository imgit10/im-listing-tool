# Image Enhancement Skill — Interior Moderna

> **For collaborators (Carlos et al.):** This is the public, shared version of
> the Interior Moderna image skill. When Cole pushes updates to this file, run
> `git pull` in your local clone to get them. The `tools/edit_images.py` CLI
> is the canonical batch-edit tool — use it for any product, any prompt.

---

## Non-negotiable rules (updated 2026-04-18)

These came out of real generation runs. Follow them on every run — they override anything in training data.

### 1. Trust the reference photo for color and surface

When a reference photo is attached to your prompt, **do NOT describe the color or surface finish in words.** Adjective-stacking like "saturated tangerine-orange, glossy wet-looking, highly reflective, like a ripe persimmon" forces the model to synthesize its own platonic version of "tangerine" or "glossy" instead of matching what's in the reference. The output drifts from the real product.

Describe only what a photo cannot convey:
- ✅ Dimensions (scale)
- ✅ Silhouette disambiguators (so proportions don't get re-imagined)
- ✅ Scene, setting, lighting, mood (not in the reference)
- ✅ Behavior ("lit from within," "reflects surroundings")
- ✅ "Match the reference exactly — color, surface, finish, silhouette, proportions"
- ❌ Color names ("tangerine," "amber," "orange")
- ❌ Surface adjectives ("glossy," "matte," "wet-looking")
- ❌ Loaded material language ("hand-blown opal glass" → just "glass" or skip)

### 2. Dimensions in every prompt, no exceptions

Every prompt must include the product's real dimensions (cm and inches) and explicit scale category ("tabletop scale, NOT floor lamp"). Without this the model guesses scale — a tabletop lamp renders as a floor lamp, a small mirror renders as a giant wall installation.

Look up dims in Supabase `sku_dimensions` before generating, or ask Cole if missing. Do not generate without them.

### 3. Self-contained prompt blocks — no "universal opener"

Every prompt should be ONE copy-paste block that includes product spec + dims + scene + output format. Never "here's an opener to paste then pick a scene" — users stitch wrong, details get dropped.

### 4. Reference photo ORDER dominates output

Gemini (and ChatGPT) weights earlier images in the attached set more heavily. Put the **truest color reference first.** Dim warehouse shots bias the output warm and muted. Daylight factory shots produce the correct bright ambient color. Always lead with daylight if available.

### 5. Two-tier WebP quality

- **Owner-curated manual / hero picks → LOSSLESS WebP** (`lossless=True, method=6`) — 200–2200 KB per image, pixel-perfect. These ship to Shopify.
- **Bulk variant generation → Q95 lossy**, 400–800 KB target. Disposable variants, owner picks winners.

Mistake to avoid: running manual PNGs through the default Q95 pipeline crushes them to 27–150 KB. Visibly blurry. Use lossless for finals.

### 6. Drive folder discipline + Finder handoff

Generated images must be mirrored into the product's **existing** Google Drive folder under a subfolder called `AI Generated/` (sibling to `Factory/`, `Ready for Listing/`). Never create a parallel folder outside the existing product tree. After mirroring, `open` the folder in macOS Finder so the owner can review — opening Finder IS the handoff, not sending URLs.

### 7. Brand is always Interior Moderna

When building Shopify listings from generated images, the product `vendor` field is always `Interior Moderna`. Never the supplier name (Tonghai, OpenGoods, Jianzhi, etc.). Supplier lives in internal systems only.

### 8. Shopify tag format — Title Case with spaces

`Table Lamp`, not `table-lamp`. `Orange`, not `orange`. `Wall Art`, not `wall-art`. Shopify search is case-insensitive but the tag admin list splits the two forms — you end up with phantom duplicates. Before adding any tag, verify the canonical casing against an existing product.

---

This skill takes a basic AI image prompt (or describes a product) and rewrites it into a prompt that produces expert-level, gallery-quality product photography — eliminating the flat, synthetic "AI slop" look.

---

## When to Use
- Generating product listing photos via Google AI Studio / Gemini
- Creating lifestyle/room-setting shots for Interior Moderna products
- Rewriting a weak image prompt before sending to any AI image generator
- Improving an existing AI-generated image that looks generic

---

## The Enhancement Process

### Step 1 — Diagnose What's Wrong

When given an image prompt or a product to photograph, first identify the "AI slop" failure modes:

**Common AI slop signals:**
- Generic, even lighting (no shadows, no depth)
- No specific time of day or light source named
- No camera/lens specification
- No defined color grade or mood
- Background described as "modern interior" or "clean white" (too vague)
- No texture detail on the product
- No human element or scale reference (where applicable)
- No art direction for the exact feel
- Prompt reads like a product description, not a photo brief

### Step 2 — Rewrite as a Professional Photo Brief

Transform the prompt using this framework. Every element must be SPECIFIC:

**Photography Fundamentals:**
- Camera: `Hasselblad X2D 100C`, `Sony A7R V`, or `Phase One IQ4 150MP`
- Lens: `90mm macro`, `85mm f/1.4`, `50mm f/2`
- Aperture: specify (f/2.8 for soft background, f/8 for product sharpness)
- ISO: low (100-400) for clean, noise-free result

**Light:**
- Source: `north-facing window light`, `single softbox camera left`, `morning golden hour raking across surface`
- Quality: `soft diffused`, `hard directional with defined shadow`, `halo rim light from behind`
- Color temperature: `5500K daylight`, `3200K warm tungsten`
- Shadows: `long shadow casting left at 30 degrees`, `soft shadow pool beneath`

**Set / Environment:**
- Surface: `matte white Italian marble slab`, `raw concrete with micro-texture`, `sand-blasted oak shelf`
- Background: `tonal gradient from warm ecru to deep charcoal`, `architectural void — near-black negative space`, `bleached linen panel`
- Depth of field: `shallow — background dissolves at f/1.8`
- Styling: `single prop — architectural object only`, `minimal negative space, centered`

**Color Grade / Film Style:**
- `Muted earth tones, lifted blacks` (editorial luxury feel)
- `High key with soft blow-out whites` (gallery clean)
- `Desaturated with warm midtones — like a Kinfolk editorial`
- `Deep shadow, rich blacks — fashion editorial`

**Mood Reference:**
- Match Interior Moderna brand: `quiet luxury`, `museum-grade stillness`, `architectural precision`
- Anti-references: no stock-photo brightness, no symmetrical perfection, no gradient backgrounds, no lens flares

### Step 3 — Write the Final Prompt

**Format for Google AI Studio / Gemini:**

```
[PRODUCT DESCRIPTION]
[CAMERA + LENS]
[APERTURE + ISO]
[LIGHT SOURCE + QUALITY + COLOR TEMP]
[SURFACE + BACKGROUND]
[DEPTH OF FIELD]
[COLOR GRADE]
[MOOD + REFERENCES]
[NEGATIVE PROMPTS: no watermarks, no text, no people, no lens flare, not stock photo, not symmetrical, not CGI render]
```

**Example transformation:**

Before (AI slop):
> "Modern wall art piece in a contemporary living room, professional product photography, clean white background"

After (expert-level):
> "Abstract sculptural wall panel in charcoal and raw concrete finish. Shot with Hasselblad X2D 100C, 90mm macro lens, f/5.6, ISO 200. Single north-facing window light, soft diffused, 5500K daylight, casting a long precise shadow at 45 degrees across a matte white Italian marble surface. Background: tonal gradient from warm white to deep warm gray architectural void. Shallow depth — front edge in razor focus, sides dissolving. Color grade: muted earth tones, lifted blacks, no saturation. Mood: museum vitrine, gallery still life, Kinfolk editorial. Negative prompts: no text, no people, no stock photo look, no lens flare, no symmetrical composition."

---

## Category Presets

Apply these based on product category:

### Wall Art / Sculptures
- Surface: matte concrete, linen, or raw plaster
- Light: single directional source, long cast shadow
- Angle: slight off-axis (15 degree tilt) — not perfectly flat
- Background: warm architectural void or tonal fog

### Mirrors
- Light: key light from camera-left at 45 degrees, subtle rim from behind
- Strategy: show partial reflection of a beautiful interior element (window, lamp)
- Surface: dark polished stone or warm bleached oak console

### Lighting / Lamps
- Always photograph ILLUMINATED — show actual light emission
- Shoot in ambient darkness or deep shadow so light pool is visible
- Color temp of emitted light: specify warm (2700K) vs cool (4000K)
- Shoot from slightly below or at product height, never from above

### Furniture
- Shot from 30 degree angle showing form and depth
- Single strong side light to show material texture
- Scale reference: abstract architectural element nearby (not a person)

### Lifestyle / Room Setting
- Full interior scene with one hero product in foreground
- Style: editorial interior, not "perfect show home"

---

## Output Format

When rewriting a prompt, output:

```
ORIGINAL PROMPT:
[paste original]

DIAGNOSIS:
[2-3 bullet points on why it produces AI slop]

ENHANCED PROMPT (Google AI Studio):
[full rewritten prompt]

SUGGESTED VARIATIONS:
1. [lighter/daytime version]
2. [darker/evening version]
3. [close-up detail version]
```

---

## Critical: Structural Anchoring (Prevents Mood Bleed)

When using reference images with Gemini, **soft/warm scene moods can bleed into how the model renders the product itself** — making structured frames look blobby, wavy, or organic when they shouldn't be.

**Always include explicit structural constraints about the product in every prompt**, regardless of the room mood:
- Describe key geometric features: seam lines, angles, symmetry, proportions
- State what the product is NOT: "NOT wavy, NOT blobby, NOT organic/free-form"
- These constraints anchor the model so a "serene bedroom" prompt doesn't turn a structured chrome mirror frame into a melted blob

**Always include real-world dimensions** (e.g. "85cm / 33.5 inches diameter") so the model scales the product correctly relative to furniture, doorways, and people-height references in the scene.

---

## Image Output Rules (NON-NEGOTIABLE)

- **All generated images MUST be square (1:1 aspect ratio)** for product listings
- **All generated images MUST be saved as WebP**, not PNG or JPEG
- **Target file size: 300-800 KB** — optimized for fast page loads
- Conversion pipeline: generate as PNG from API, then convert to WebP with `tools/image_converter.py`
- Max dimensions: 2400x2400px (downscale larger images)
- **Never upload raw PNGs (1-3MB)** — always convert first

---

## Notes
- Always specify negative prompts at the end (no watermarks, no text, no stock photo look)
- For Google AI Studio: paste the enhanced prompt directly into Imagen 3
- After generation: if image still looks flat, the lighting descriptor needs to be more specific — tighten the shadow angle and surface material
- **Always feed actual product reference photos** to Gemini — never rely on text-only descriptions of the product
- **Always confirm product dimensions before generating.** If the user hasn't provided dimensions, ASK before writing any prompts
- **Always apply EXIF rotation when loading reference photos** (`PIL.ImageOps.exif_transpose(img)`). Phone photos have rotation metadata that PIL does NOT apply by default
- **Never include reference photos that show the product in the wrong orientation**

---

## Batch Image Editing (Image-in → Image-out)

Use `tools/edit_images.py` to apply an edit to a whole folder of product photos using Gemini's image editing model (`gemini-2.5-flash-image`).

```bash
python3 tools/edit_images.py \
  --input  photos/my-product/originals \
  --output photos/my-product/edited \
  --prompt "Your edit instruction here"
```

### Proven prompt patterns

**Matte finish (remove gloss):**
> "Make the lamp surface COMPLETELY MATTE and non-reflective. The color MUST stay deep black — NOT grey, NOT beige. Remove all glossy shine and specular highlights. Add a very subtle matte powder-coat texture. Do not change the shape, background, lighting, or composition."

**Color change:**
> "Change the lamp color from black to deep forest green matte. Keep the exact same shape, proportions, background, and lighting. The surface should be matte, not glossy."

**Background cleanup:**
> "Make ONLY the wall more white and clean. Do not change the product, lighting, reflections, shadows, or anything else. The wall should become pure gallery white."

### Critical rules for image editing prompts
- **Always anchor the color explicitly** — if you say "matte clay texture" Gemini will drift the color to grey/beige. Say: "color MUST stay [COLOR] — NOT grey, NOT beige"
- **Always say what NOT to change** — list shape, background, lighting, composition as locked
- **Never use vague style words** like "artisanal" or "raw" without a color lock — they cause color drift
- Outputs save as WebP, 400–800 KB target, max 2400px
