"""Command line interface for the Startup Co‑Founder Agent.

This module provides an entry point to generate all deliverables given a
business idea. The CLI writes out the market analysis, pricing tiers,
landing page copy and pitch deck to the specified output directory.

Example usage:

.. code-block:: bash

    python -m startup_cofounder_agent.cli "AI‑powered personal finance coach"

Optionally specify an output directory and OpenAI API key:

.. code-block:: bash

    python -m startup_cofounder_agent.cli \
        --output-dir /tmp/outputs \
        --api-key sk-...

If the API key is not provided as a flag, it must be available in the
``OPENAI_API_KEY`` environment variable.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import generator, ppt_generator


def parse_args() -> argparse.Namespace:
    """Define and parse command line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate market analysis, pricing tiers, landing page copy and pitch deck for a startup idea."
    )
    parser.add_argument(
        "idea",
        help="A short description of your business idea.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where output files will be written (default: current working directory).",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Explicit OpenAI API key. If omitted, the OPENAI_API_KEY environment variable is used.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI.

    Parses arguments, generates all deliverables, writes them to files,
    and prints a summary. Any exceptions from the generator module are
    propagated to the console.
    """
    args = parse_args()
    idea: str = args.idea
    output_dir = Path(args.output_dir).expanduser().resolve()
    api_key = args.api_key
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    # Generate content
    print("Generating market analysis...")
    market_analysis = generator.generate_market_analysis(idea, api_key=api_key)
    print("Generating pricing tiers...")
    pricing_tiers = generator.generate_pricing_tiers(idea, api_key=api_key)
    print("Generating landing page copy...")
    landing_page = generator.generate_landing_page_copy(idea, api_key=api_key)
    print("Generating pitch deck outline...")
    slides = generator.generate_pitch_deck_outline(idea, api_key=api_key)
    # Write outputs
    analysis_path = output_dir / "market_analysis.txt"
    pricing_path = output_dir / "pricing_tiers.txt"
    landing_path = output_dir / "landing_page.txt"
    deck_path = output_dir / "pitch_deck.pptx"
    analysis_path.write_text(market_analysis, encoding="utf-8")
    pricing_path.write_text(pricing_tiers, encoding="utf-8")
    landing_path.write_text(landing_page, encoding="utf-8")
    # Create the PowerPoint
    ppt_generator.create_pitch_deck(slides, str(deck_path))
    # Print summary
    print(f"\n✔ Market analysis written to {analysis_path}")
    print(f"✔ Pricing tiers written to {pricing_path}")
    print(f"✔ Landing page copy written to {landing_path}")
    print(f"✔ Pitch deck written to {deck_path}")


if __name__ == "__main__":  # pragma: no cover
    main()