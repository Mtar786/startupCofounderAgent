# Startup Co‑Founder Agent

**Transform a raw business idea into actionable artefacts.**  
This tool is designed for entrepreneurs and innovators who need a quick
overview of their market, a polished landing page, sensible pricing tiers
and a simple pitch deck. It leverages the OpenAI API to draft
professional content and uses python‑pptx to produce a ready‑to‑present
PowerPoint file.



## Features

- **Market analysis** – Generates a concise report covering demand,
  market size, relevant economic indicators, geographic considerations,
  market saturation and typical pricing strategies. It also includes a
  competitive analysis that outlines key players, their strengths and
  weaknesses, opportunities for differentiation and barriers to entry.  
  The underlying prompt is inspired by the U.S. Small Business
  Administration’s guidance on market research and competitive
  analysis【416805499245247†L273-L309】【416805499245247†L340-L359】.
- **Tiered pricing model** – Proposes at least three pricing tiers
  (e.g. Basic, Pro and Premium) with increasing value and decreasing
  per‑unit cost, based on established strategies for tiered pricing
 【238728335597137†L330-L344】. The generator considers cost analysis,
  customer segmentation, value propositions and clear differentiation
  between tiers【238728335597137†L346-L410】.
- **Landing page copy** – Produces persuasive marketing text for a
  homepage. The copy includes a headline, a short description of
  benefits and a call to action.
- **Pitch deck** – Creates a 10‑slide presentation following a widely
  accepted structure: business overview, problem, solution & value
  proposition, market size & analysis, product & business model,
  go‑to‑market strategy, competitive analysis, team, financials &
  traction, and the ask【529464131840874†L218-L380】. The tool uses
  python‑pptx to assemble these slides into a `.pptx` file.

## Installation

This project requires Python 3.8 or later. Install the dependencies
using pip:

```bash
pip install openai python-pptx
```

It is recommended to use a virtual environment.

## Usage

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...
```

Run the CLI with your business idea:

```bash
python -m startup_cofounder_agent.cli "AI‑powered personal finance coach" --output-dir ./outputs
```

This command will generate the following files in the specified output
directory:

| File | Contents |
| --- | --- |
| `market_analysis.txt` | A market research report covering demand, market size, economics, location, saturation, pricing and competitor analysis |
| `pricing_tiers.txt` | A tiered pricing model with package names, prices and included features |
| `landing_page.txt` | A short piece of marketing copy suitable for a homepage |
| `pitch_deck.pptx` | A 10‑slide PowerPoint presentation based on the outlined deck structure |

If you prefer to supply the API key on the command line, use the
`--api-key` option.

## How it works

The CLI orchestrates four calls to the OpenAI ChatCompletion API using
carefully constructed prompts. The prompts are informed by best
practices:

1. **Market analysis prompt** – Requests information on customer
   demand, total addressable market, economic factors, geography,
   saturation, pricing and competitor analysis, aligned with SBA
   guidelines【416805499245247†L273-L309】【416805499245247†L340-L359】.
2. **Pricing prompt** – Asks for a tiered pricing model, drawing on
   strategies where per‑unit cost decreases at higher tiers and each
   tier targets a different customer segment【238728335597137†L330-L344】,
   and is built via cost analysis and segmentation【238728335597137†L346-L410】.
3. **Landing page prompt** – Instructs the model to write a compelling
   headline, description and call‑to‑action for the idea.
4. **Pitch deck prompt** – Requests a ten‑slide outline based on a
   widely used pitch deck template that covers the essential topics
   investors expect【529464131840874†L218-L380】. The resulting outline is
   passed to python‑pptx to produce a polished `.pptx` file.

## Research and methodology

This agent draws on established entrepreneurial resources:

* The U.S. Small Business Administration advises founders to gather
  demographic information, evaluate demand, estimate market size, study
  economic indicators, assess geographic considerations, check market
  saturation and think through pricing strategies【416805499245247†L273-L309】. It also
  recommends analysing competitors by assessing market share, strengths,
  weaknesses, opportunities and barriers【416805499245247†L340-L359】. These
  principles inform the market analysis prompt.
* Stripe’s guidance on tiered pricing explains that multi‑tier
  structures set a base price with increasing value at higher tiers,
  where per‑unit cost decreases as customers buy more【238728335597137†L330-L344】. It
  emphasises starting with cost analysis, market research to understand
  price sensitivities, defining customer segments, clearly
  differentiating tiers, and reviewing and adjusting after launch【238728335597137†L346-L410】.
  These steps are built into the pricing prompt.
* A widely adopted pitch deck template suggests ten slides: business
  overview, problem, solution, market size, product & business model,
  go‑to‑market strategy, competitive analysis, team, financials &
  traction, and the ask【529464131840874†L218-L380】. The agent uses this
  structure to outline the deck and then uses python‑pptx to assemble
  it.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the MIT License.
