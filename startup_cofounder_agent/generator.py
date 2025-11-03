"""Core generation functions for the Startup Co‑Founder Agent.

This module wraps calls to the OpenAI API to generate:

* Market analysis
* Pricing tiers
* Landing page copy
* Pitch deck outlines

The functions here accept a business idea as input and optionally an
OpenAI API key. If no API key is provided, the key is read from
the ``OPENAI_API_KEY`` environment variable. Each function returns
raw strings; the CLI transforms these into files.

Note: This module does not attempt to parse or validate the OpenAI
response beyond returning the generated text. For production usage
you may wish to add more robust parsing.
"""

from __future__ import annotations

import os
from typing import List, Dict, Tuple

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # OpenAI is optional; the user must install it separately.

DEFAULT_MODEL = "gpt-4"


def _ensure_openai(api_key: str | None) -> None:
    """Ensure the OpenAI package is available and the API key is set.

    Args:
        api_key: An explicit API key or ``None`` to read from the
            ``OPENAI_API_KEY`` environment variable.

    Raises:
        RuntimeError: If the ``openai`` package is unavailable or no
            API key is configured.
    """
    if openai is None:
        raise RuntimeError(
            "The openai package is not installed. Install it with `pip install openai`."
        )
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "No OpenAI API key was provided. Set the OPENAI_API_KEY environment variable or pass api_key explicitly."
        )
    openai.api_key = key


def _chat_completion(prompt: str, api_key: str | None = None, model: str = DEFAULT_MODEL) -> str:
    """Send a prompt to the OpenAI ChatCompletion endpoint and return the result.

    This helper hides API boilerplate and centralises the error handling.

    Args:
        prompt: The text prompt to send to the model.
        api_key: Optional API key; if omitted the ``OPENAI_API_KEY``
            environment variable is used.
        model: The OpenAI model name (default: ``gpt‑4``).

    Returns:
        The content of the assistant's reply as a string.

    Raises:
        RuntimeError: If the OpenAI API is unavailable or fails.
    """
    _ensure_openai(api_key)
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert startup consultant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
    except Exception as exc:  # Catch broad exceptions to surface them nicely
        raise RuntimeError(f"Failed to call OpenAI API: {exc}") from exc
    # Extract the assistant reply
    try:
        return completion["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        raise RuntimeError(f"Unexpected response format from OpenAI API: {exc}") from exc


def generate_market_analysis(idea: str, *, api_key: str | None = None) -> str:
    """Generate a market analysis for the given business idea.

    The prompt instructs the model to perform market research, including
    demand, market size, economic indicators, location considerations,
    market saturation and pricing, along with a competitive analysis of
    existing players. The result is returned as a human‑readable report.

    Args:
        idea: A short description of the startup concept.
        api_key: Optional OpenAI API key.

    Returns:
        A string containing the market analysis.
    """
    prompt = (
        "You are assisting a founder in understanding their market. "
        "Given the business idea below, perform a concise market analysis. "
        "Your analysis should cover:\n"
        "- Demand: describe who the customers are and their pain points.\n"
        "- Market size: estimate the addressable market size and growth.\n"
        "- Economic indicators: mention relevant economic factors (e.g. disposable income, technology adoption).\n"
        "- Location and saturation: note any geographic considerations and whether the market is crowded.\n"
        "- Pricing considerations: discuss typical pricing strategies in this space.\n"
        "- Competitor analysis: identify a few key competitors, their strengths and weaknesses, opportunities, and barriers to entry.\n\n"
        f"Business idea: {idea}\n\n"
        "Respond in a professional tone with headings for each section."
    )
    return _chat_completion(prompt, api_key=api_key)


def generate_pricing_tiers(idea: str, *, api_key: str | None = None) -> str:
    """Generate a tiered pricing model for the given business idea.

    The prompt instructs the model to propose at least three pricing tiers. It
    suggests segmenting customers by value, assigning appropriate features
    to each tier, and specifying the price point. The resulting text
    outlines each tier with a name, description and price.

    Args:
        idea: A short description of the startup concept.
        api_key: Optional OpenAI API key.

    Returns:
        A string describing the pricing tiers.
    """
    prompt = (
        "You are a pricing strategist. Propose a tiered pricing structure for "
        "the following business idea. Provide at least three tiers (e.g. Basic, "
        "Pro, Premium), with a clear name, monthly price in USD, and the key "
        "features or usage limits each tier includes. Consider cost analysis, "
        "market research for price sensitivities, segmentation, and value "
        "proposition for each customer group. Highlight how each tier adds "
        "additional value compared with the lower tier.\n\n"
        f"Business idea: {idea}\n\n"
        "Present your answer in a bullet list where each tier starts with the tier name and price, followed by a colon and its features."
    )
    return _chat_completion(prompt, api_key=api_key)


def generate_landing_page_copy(idea: str, *, api_key: str | None = None) -> str:
    """Generate landing page copy for the given business idea.

    This function asks the model to write a short, engaging piece of copy
    suitable for a landing page. It should include a headline, a brief
    description of the value proposition, and a call to action. The tone
    should be persuasive yet informative.

    Args:
        idea: A short description of the startup concept.
        api_key: Optional OpenAI API key.

    Returns:
        A string containing the landing page copy.
    """
    prompt = (
        "You are a marketing copywriter. Write concise and persuasive landing page "
        "copy for the business idea below. Include:\n"
        "- A bold headline summarising the core value proposition.\n"
        "- A short paragraph describing the product or service and its benefits.\n"
        "- A clear call to action encouraging visitors to sign up or learn more.\n\n"
        f"Business idea: {idea}\n\n"
        "Use an enthusiastic yet professional tone."
    )
    return _chat_completion(prompt, api_key=api_key)


def generate_pitch_deck_outline(idea: str, *, api_key: str | None = None) -> List[Dict[str, str]]:
    """Generate a pitch deck outline with slide titles and bullet points.

    The prompt requests the standard ten slides of a startup pitch deck. It
    instructs the model to produce a list of slides, each with a title and a
    short list of bullet points. The result is parsed into a list of
    dictionaries with keys ``title`` and ``content``. If parsing fails, the
    raw response is returned as a single slide.

    Args:
        idea: A short description of the startup concept.
        api_key: Optional OpenAI API key.

    Returns:
        A list of slides, where each slide is a dict with ``title`` and
        ``content`` (string of bullet points separated by newlines).
    """
    prompt = (
        "You are an expert pitch deck designer. Create an outline for a 10‑slide "
        "pitch deck for the startup idea below. Follow this structure: (1) "
        "Business Overview, (2) Problem, (3) Solution & Value Proposition, "
        "(4) Market Size & Analysis, (5) Product & Business Model, (6) Go‑to‑Market "
        "Strategy, (7) Competitive Analysis, (8) Team, (9) Financials & Traction, "
        "(10) Ask & Use of Funds. For each slide, provide a title and 3–5 bullet "
        "points summarising the key messages you would include on that slide.\n\n"
        f"Business idea: {idea}\n\n"
        "Respond in a structured format. Use numbered slides followed by the title and its bullet points."
    )
    raw = _chat_completion(prompt, api_key=api_key)
    slides: List[Dict[str, str]] = []
    # Simple parser to interpret numbered lists into slide dicts
    try:
        for line in raw.splitlines():
            # Expect lines like "1. Title: point1; point2; point3"
            if not line.strip():
                continue
            # Split on the first dot to separate the number
            if "." in line:
                number, rest = line.split(".", 1)
                rest = rest.strip()
                # Further split on ':' to separate title and content
                if ":" in rest:
                    title, content = rest.split(":", 1)
                    title = title.strip()
                    content = content.strip().lstrip("- ")
                    slides.append({"title": title, "content": content})
        # If we didn't parse anything, fall back to returning raw content
        if not slides:
            slides.append({"title": "Pitch Deck", "content": raw})
    except Exception:
        slides = [{"title": "Pitch Deck", "content": raw}]
    return slides