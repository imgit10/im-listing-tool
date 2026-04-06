"""
gemini.py — Gemini API wrapper for text generation.

Usage:
    from tools.gemini import generate
    text = generate("Write a product description for...", system="You are a copywriter")
"""

import os

# Load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"


def generate(prompt, system=None, max_tokens=2000, json_mode=False, temperature=0.3):
    """Generate text via Gemini API.

    Args:
        prompt: The user prompt text
        system: Optional system prompt (prepended to prompt)
        max_tokens: Max output tokens
        json_mode: If True, request JSON output
        temperature: Sampling temperature

    Returns:
        str: The generated text

    Raises:
        RuntimeError: If Gemini API call fails
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GOOGLE_GEMINI_API_KEY not set. "
            "Copy .env.example to .env and add your API key. "
            "Get one free at https://aistudio.google.com/app/apikey"
        )

    from google import genai
    from google.genai import types

    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    if json_mode:
        config.response_mime_type = "application/json"

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=full_prompt,
        config=config,
    )
    return response.text
