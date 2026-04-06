# Product Listing Standards

Read `skills/brand-voice.md` first — all listings must follow brand voice.

## Required Fields

### Title
- Clean, gallery-like
- Variant format: "Product Name: Color Variant" (e.g., "Fabric Fusion: Cinder Halo")
- No generic descriptors ("Modern LED Lamp 2026")

### Description Structure

**HTML Format (CRITICAL):**
```html
<p><strong>Overview<br></strong>5-8 full sentences describing the product. Text flows directly after the br tag within the same p element...</p>
<p><strong>Craftsmanship and Dimensions<br></strong>- Dimension info<br>- Material info<br>- Color/finish<br>- Additional details</p>
```

**Content Requirements:**
1. **Overview** — 5-8 full sentences. Describe form, presence, material reality, light behavior, spatial effect. Mention collection when applicable. No invented features.
2. **Craftsmanship and Dimensions** — Hyphen-separated list with `<br>` tags (NOT `<ul><li>`):
   - Dimensions: inches (primary) + cm (secondary), one decimal max
   - Materials: elevated terminology ("frosted acrylic," "nano-plated finish," "hand-forged stainless steel")
   - Color/finish, functional details, customization notes (only if true)

**Formatting Rules:**
- NO separate `<p>` tags for section headings (NOT `<p><strong>Overview</strong></p><p>Text...</p>`)
- NO `<ul><li>` bullet lists — use hyphens/dashes with `<br>` instead
- NO `<h2>` or other heading tags
- NO `<span>` tags anywhere in descriptions — plain text only, no wrappers
- NO `<meta charset="UTF-8">` or any `<meta>` tags inside body_html
- NO `data-mce-fragment` attributes or `dir="ltr"` on `<p>` tags (editor artifacts)
- Single `<p>` per section with `<strong>Section Name<br></strong>` followed immediately by content
- Dashes (`-` or `-`) for bullet items, separated by `<br>` tags

**Clean HTML Reference (exact accepted format):**
```html
<p><strong>Overview<br></strong>5-8 sentences of description text here. No dimensions in the overview. Text flows directly after the br tag within the same p element. Each sentence carries weight — sculptural, architectural language only.<br></p>
<p><strong>Craftsmanship and Dimensions<br></strong>- Dimensions: 33.5" diameter<br>- Depth: 2.4"<br>- Material: Sculpted high-density foam core with controlled chemical erosion treatment<br>- Color/Finish: Matte charcoal surface with vivid violet relief detailing<br>- Hanging Orientation: Ready for mounting</p>
```

**Banned HTML artifacts (strip these if found):**
```html
<meta charset="UTF-8">
<span>any text</span>
<p dir="ltr">
<strong data-mce-fragment="1">
```

### SEO
- **Meta Title:** "Product Name | Short Descriptor | Interior Moderna" — under 70 chars
- **Meta Description:** 150-160 chars, elegant, keyword-aligned
- **Search Engine Description:** Shorter, more keyword-dense, still on-brand
- **URL Handle:** Lowercase, hyphenated, no stop-word bloat (e.g., "fabric-fusion-cinder-halo")

### SKU System
Pattern: `IM-<CATEGORY>-<PRODUCT>-<VARIANT>-<SIZE>`
- Examples: `IM-LGT-ASKR-SPIRE-BONE-STD`, `IM-ART-FABFUS-CINDER-24`
- Size tokens: furniture = nearest inch length, wall art = `HxxWxx`
- Barcodes: use if provided, never invent. If missing: "Barcode: (blank — assign in Shopify or via GS1)"

### Tags
- 8-15 max
- Mix of: category, material, finish, form, collection, color
- No generic tags ("home decor", "modern")

### Output Template
```
TITLE:
HANDLE:
SKU:
BARCODE:
PRODUCT TYPE:
COLLECTION:
TAGS: (8-15 max, mix of category/material/finish/form/collection/color)
PRICE:
DESCRIPTION (HTML):
SEO META TITLE:
SEO META DESCRIPTION:
SEARCH ENGINE DESCRIPTION:
CRAFTSMANSHIP & DIMENSIONS (bullets):
MISSING INFO (if any):
```

### Quality Checklist (run silently)
- Meta title < 70 chars
- Meta description 150-160 chars
- No invented specs
- Dimensions converted correctly
- Overview 5-8 sentences, premium tone
- Handle clean, SKU follows system
- No banned HTML artifacts
- No banned brand voice words
