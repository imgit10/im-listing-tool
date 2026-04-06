"""
image_converter.py — WebP conversion utility for product photos.

Converts images (PNG, JPEG, etc.) to WebP format with:
- Starting quality: 85
- Max file size: 700KB
- Progressive quality reduction if over limit
- EXIF stripping for privacy/size

Usage:
    from tools.image_converter import convert_to_webp, convert_url_to_webp

    # Convert a local file
    result = convert_to_webp("photos/input.png", "outputs/output.webp")

    # Convert from URL
    result = convert_url_to_webp("https://example.com/photo.png", "outputs/output.webp")
"""

import io
import os
import urllib.request

try:
    from PIL import Image
except ImportError:
    Image = None

# ── Configuration ─────────────────────────────────────────────────────────────

MAX_SIZE_BYTES = 700 * 1024   # 700 KB
INITIAL_QUALITY = 85
MIN_QUALITY = 40
QUALITY_STEP = 5


def _ensure_pillow():
    """Raise clear error if Pillow is not installed."""
    if Image is None:
        raise ImportError(
            "Pillow is required for image conversion. "
            "Install it with: pip install Pillow"
        )


def convert_to_webp(
    input_path: str,
    output_path: str,
    max_size: int = MAX_SIZE_BYTES,
    initial_quality: int = INITIAL_QUALITY,
    max_dimension: int = 2400,
) -> dict:
    """Convert an image file to WebP with size cap.

    Args:
        input_path: Path to source image (PNG, JPEG, TIFF, BMP, etc.)
        output_path: Path for the output .webp file
        max_size: Maximum file size in bytes (default 700KB)
        initial_quality: Starting WebP quality (default 85)
        max_dimension: Max width or height in pixels (default 2400)

    Returns:
        dict with keys: path, size_bytes, quality_used, width, height, resized
    """
    _ensure_pillow()

    img = Image.open(input_path)

    # Convert to RGB if needed (e.g., RGBA PNGs, CMYK)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Strip EXIF data
    if hasattr(img, "info"):
        img.info.pop("exif", None)

    # Resize if exceeding max dimension
    resized = False
    w, h = img.size
    if max(w, h) > max_dimension:
        ratio = max_dimension / max(w, h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        resized = True
        w, h = img.size

    # Progressive quality reduction to meet size cap
    quality = initial_quality
    final_data = None

    while quality >= MIN_QUALITY:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=4)
        data = buf.getvalue()

        if len(data) <= max_size:
            final_data = data
            break

        quality -= QUALITY_STEP

    if final_data is None:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=MIN_QUALITY, method=4)
        final_data = buf.getvalue()
        quality = MIN_QUALITY

    # Write output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(final_data)

    return {
        "path": output_path,
        "size_bytes": len(final_data),
        "quality_used": quality,
        "width": w,
        "height": h,
        "resized": resized,
    }


def convert_bytes_to_webp(
    image_bytes: bytes,
    output_path: str,
    max_size: int = MAX_SIZE_BYTES,
    initial_quality: int = INITIAL_QUALITY,
    max_dimension: int = 2400,
) -> dict:
    """Convert raw image bytes to WebP with size cap.

    Args:
        image_bytes: Raw image data (PNG, JPEG, etc.)
        output_path: Path for the output .webp file
        max_size: Maximum file size in bytes (default 700KB)
        initial_quality: Starting WebP quality (default 85)
        max_dimension: Max width or height in pixels (default 2400)

    Returns:
        dict with keys: path, size_bytes, quality_used, width, height, resized
    """
    _ensure_pillow()

    img = Image.open(io.BytesIO(image_bytes))

    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if hasattr(img, "info"):
        img.info.pop("exif", None)

    resized = False
    w, h = img.size
    if max(w, h) > max_dimension:
        ratio = max_dimension / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        resized = True
        w, h = img.size

    quality = initial_quality
    final_data = None

    while quality >= MIN_QUALITY:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=4)
        data = buf.getvalue()
        if len(data) <= max_size:
            final_data = data
            break
        quality -= QUALITY_STEP

    if final_data is None:
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=MIN_QUALITY, method=4)
        final_data = buf.getvalue()
        quality = MIN_QUALITY

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(final_data)

    return {
        "path": output_path,
        "size_bytes": len(final_data),
        "quality_used": quality,
        "width": w,
        "height": h,
        "resized": resized,
    }


def convert_url_to_webp(
    url: str,
    output_path: str,
    max_size: int = MAX_SIZE_BYTES,
    initial_quality: int = INITIAL_QUALITY,
    max_dimension: int = 2400,
) -> dict:
    """Download an image from URL and convert to WebP.

    Args:
        url: URL of the source image
        output_path: Path for the output .webp file
        max_size: Maximum file size in bytes (default 700KB)
        initial_quality: Starting WebP quality (default 85)
        max_dimension: Max width or height in pixels (default 2400)

    Returns:
        dict with keys: path, size_bytes, quality_used, width, height, resized, source_url
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": "ImageConverter/1.0",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        image_bytes = resp.read()

    result = convert_bytes_to_webp(
        image_bytes, output_path,
        max_size=max_size,
        initial_quality=initial_quality,
        max_dimension=max_dimension,
    )
    result["source_url"] = url
    return result
