#!/usr/bin/env python3
"""
edit_images.py — Batch edit product images via Gemini image-in → image-out.

Usage:
    python3 tools/edit_images.py \
        --input  photos/my-product/originals \
        --output photos/my-product/edited \
        --prompt "Make the lamp surface completely matte and non-reflective. Keep the color and shape identical."

The script feeds each image to Gemini as a reference and applies your
edit prompt, saving the results as WebP.

Requirements:
    pip install google-genai pillow
    GOOGLE_GEMINI_API_KEY set in .env or environment
"""
from __future__ import annotations

import argparse
import io
import os
import sys

# Load .env
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from google import genai
from PIL import Image

API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY", "")
IMAGE_MODEL = "gemini-2.5-flash-image"
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def convert_to_webp(img: Image.Image, target_min_kb: int = 400, target_max_kb: int = 800) -> bytes:
    """Binary-search WebP quality to hit 400–800 KB. Hard floor: quality 70."""
    max_dim = 2400
    if max(img.width, img.height) > max_dim:
        ratio = max_dim / max(img.width, img.height)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)

    lo, hi = 70, 95
    best = b""
    quality = hi
    for _ in range(8):
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=6)
        size_kb = buf.tell() // 1024
        best = buf.getvalue()
        if target_min_kb <= size_kb <= target_max_kb:
            break
        if size_kb > target_max_kb:
            hi = quality - 1
        else:
            lo = quality + 1
        quality = (lo + hi) // 2
        if lo > hi:
            break
    return best


def edit_image(client: genai.Client, prompt: str, src_path: str) -> Image.Image | None:
    """Send one image to Gemini and return the edited PIL image, or None on failure."""
    pil_img = Image.open(src_path).convert("RGB")
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=95)
    img_bytes = buf.getvalue()

    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}},
                ],
            }
        ],
        config={"response_modalities": ["TEXT", "IMAGE"]},
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            return Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-edit product images via Gemini.")
    parser.add_argument("--input", required=True, help="Folder of source images")
    parser.add_argument("--output", required=True, help="Folder to save edited images")
    parser.add_argument("--prompt", required=True, help="Edit instruction for every image")
    parser.add_argument("--prefix", default="", help="Optional filename prefix for outputs")
    args = parser.parse_args()

    if not API_KEY:
        sys.exit(
            "ERROR: GOOGLE_GEMINI_API_KEY not set.\n"
            "Copy .env.example to .env and add your key from https://aistudio.google.com/app/apikey"
        )

    os.makedirs(args.output, exist_ok=True)
    client = genai.Client(api_key=API_KEY)

    inputs = sorted(
        f
        for f in os.listdir(args.input)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS
    )

    if not inputs:
        sys.exit(f"No supported images found in {args.input}")

    print(f"Editing {len(inputs)} images → {args.output}\n")

    for i, fname in enumerate(inputs, 1):
        src = os.path.join(args.input, fname)
        stem = os.path.splitext(fname)[0]
        out_name = f"{args.prefix}{stem}.webp" if args.prefix else f"{stem}_edited.webp"
        out_path = os.path.join(args.output, out_name)

        if os.path.exists(out_path):
            print(f"[{i}/{len(inputs)}] SKIP (exists): {out_name}")
            continue

        print(f"[{i}/{len(inputs)}] {fname} → {out_name} ...", end=" ", flush=True)

        try:
            result = edit_image(client, args.prompt, src)
            if result is None:
                print("WARN: no image returned")
                continue
            webp = convert_to_webp(result)
            with open(out_path, "wb") as f:
                f.write(webp)
            print(f"OK ({len(webp) // 1024} KB)")
        except Exception as e:
            print(f"ERROR: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
