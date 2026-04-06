# Interior Moderna — Listing & Photo Tool

Generate premium product listings and gallery-quality image prompts for Interior Moderna using Claude Code.

## Setup

### 1. Clone this repo

```bash
git clone https://github.com/imgit10/im-listing-tool.git
cd im-listing-tool
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key

```bash
cp .env.example .env
```

Edit `.env` and add your Google Gemini API key. Get one free at https://aistudio.google.com/app/apikey

### 4. Open in Claude Code

Open this folder in Claude Code (CLI, desktop app, or IDE extension). The `CLAUDE.md` file auto-loads and gives Claude all the brand context.

## What You Can Do

### Create a Product Listing

> "Create a listing for a black marble wall mirror, 36 inches diameter, brushed brass frame"

Claude generates a complete Shopify-ready listing with HTML description, SEO fields, SKU, and tags — saved to `outputs/`.

### Enhance an Image Prompt

> "Enhance this image prompt: photo of a modern lamp on a table"

Claude rewrites it into a professional photo brief with camera specs, lighting, surface, color grade, and mood — ready to paste into Google AI Studio.

### Convert Photos to WebP

Drop photos into `photos/`, then ask:

> "Convert all photos in the photos folder to WebP"

Claude uses `tools/image_converter.py` to optimize them (max 700KB, max 2400px, EXIF stripped).

## File Structure

```
skills/          Brand voice, listing standards, image enhancement guide
tools/           Python utilities (WebP converter, Gemini wrapper)
photos/          Drop product photos here
outputs/         Generated listings and converted images
```
