from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.munkasey_source import (
    FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    MunkaseyAxisBlock,
    generate_models,
)
from tools.wiki_identity import normalize_axis


UPDATED_AT = "2026-04-22"


def render_source_page(blocks: list[MunkaseyAxisBlock]) -> str:
    factors = [
        "Sun",
        "Moon",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Pluto",
        "Node",
        "Asc",
        "MC",
    ]
    factor_links = "\n".join(f"- {factor}" for factor in factors)
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
  - Sun
  - Moon
  - Mercury
  - Venus
  - Mars
  - Jupiter
  - Saturn
  - Uranus
  - Neptune
  - Pluto
  - Node
  - Asc
  - MC
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Michael Munkasey
- Title: *Midpoints: Unleashing the Power of the Planets*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This preservation slice stores the source's page-3 `CONCEPTS` corpus as separate companion pages under `wiki/derived/`.
- The page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`.
- The page-4 MWA example tables were intentionally omitted.
- This pass does not yet merge Munkasey's page-1 axis prose into canonical axis pages.

## Factors Covered

{factor_links}

## Concepts Companion Pages

- Concepts companion pages generated: `{len(blocks)}`.
- Browse `wiki/derived/` or [Index](../index.md) for the full set.

## Ingestion History

- 2026-04-22: Preserved Munkasey's page-3 `CONCEPTS` corpus as source-grounded companion pages and intentionally omitted the page-4 MWA example tables.
"""


def render_concepts_page(block: MunkaseyAxisBlock) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    concepts = "\n".join(f"- {item}" for item in block.concepts)
    return f"""---
title: "Michael Munkasey - {axis.display} Concepts"
page_type: derived
slug: munkasey-{axis.slug}-concepts
status: source_grounded
framework_scope: {FRAMEWORK_SCOPE}
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Purpose

Preserve Munkasey's page-3 concept phrases for `{axis.display}` as source-native image material.

## Evidence Base

- [{axis.display}](../axes/{axis.slug}.md)
- [Michael Munkasey - Midpoints: Unleashing the Power of the Planets](../sources/{SOURCE_SLUG}.md)
- Source concept page: `{block.concepts_page}`

## Source Concepts

{concepts}

## Notes On Use

- These phrases are preserved as source-native concept prompts, not as comparative doctrine.
- They are kept off the canonical axis page's comparative schema to avoid conflating image phrases with formal delineation.
"""


def write_concepts_pages(blocks: list[MunkaseyAxisBlock], derived_dir: Path) -> None:
    derived_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        path = derived_dir / f"munkasey-{axis.slug}-concepts.md"
        path.write_text(render_concepts_page(block), encoding="utf-8")


def write_source_page(blocks: list[MunkaseyAxisBlock], sources_dir: Path) -> None:
    sources_dir.mkdir(parents=True, exist_ok=True)
    path = sources_dir / f"{SOURCE_SLUG}.md"
    path.write_text(render_source_page(blocks), encoding="utf-8")


def main() -> None:
    root = Path(".")
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    blocks = generate_models(pdf_path)
    write_source_page(blocks, root / "wiki" / "sources")
    write_concepts_pages(blocks, root / "wiki" / "derived")


if __name__ == "__main__":
    main()
