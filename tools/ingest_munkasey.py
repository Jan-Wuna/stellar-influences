from __future__ import annotations

from pathlib import Path
import re
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
from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token
from tools.wiki_identity import normalize_axis
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-22"
DEFAULT_DERIVED_TEXT = "- None yet beyond source structuring."
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
}


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _section_body(body: str, heading: str, next_heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\n\n(.*?)\n\n{re.escape(next_heading)}\n", body, re.S)
    if not match:
        raise ValueError(f"could not parse section {heading}")
    return match.group(1).strip()


def _parse_legacy_witte_entry(body: str, entry: str) -> str:
    heading_match = re.search(r"- Source heading: `([^`]+)`", body)
    page_match = re.search(r"- Source page: `([^`]+)`", body)
    summary_match = re.search(r"#### Pair Summary\s+(.*)", entry, re.S)
    if not heading_match or not page_match or not summary_match:
        raise ValueError("could not normalize legacy Witte axis entry")
    return "\n".join(
        [
            f"### {WITTE_TITLE}",
            "",
            f"- Source heading: `{heading_match.group(1)}`",
            f"- Source page: `{page_match.group(1)}`",
            "",
            "#### Pair Summary",
            "",
            summary_match.group(1).strip(),
        ]
    )


def _source_entries(body: str) -> list[str]:
    entries_text = _section_body(body, "## Source Entries", "## Comparative Schema")
    entries = [entry.strip() for entry in re.split(r"(?m)(?=^### )", entries_text) if entry.strip()]
    if not entries:
        raise ValueError("could not parse source entries block")
    normalized: list[str] = []
    for entry in entries:
        if entry.startswith(f"### {WITTE_TITLE}\n") and "- Source heading:" not in entry:
            normalized.append(_parse_legacy_witte_entry(body, entry))
            continue
        normalized.append(entry)
    return normalized


def _render_munkasey_entry(block: MunkaseyAxisBlock) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    return "\n".join(
        [
            f"### {SOURCE_TITLE}",
            "",
            f"- Source heading: `{block.source_heading}`",
            f"- Source page: `{block.axis_page}`",
            "",
            "#### Basic Ideas",
            "",
            block.basic_ideas,
            "",
            "#### In Your Personal Life",
            "",
            f"- Thesis: {block.personal_thesis}",
            f"- Anti: {block.personal_anti}",
            "",
            "#### In Your Relationships",
            "",
            f"- Thesis: {block.relationship_thesis}",
            f"- Anti: {block.relationship_anti}",
            "",
            "#### With Body or Mind",
            "",
            block.body_mind,
            "",
            "#### In Politics or Business",
            "",
            f"- Thesis: {block.politics_business_thesis}",
            f"- Anti: {block.politics_business_anti}",
            "",
            "#### Munkasey Concepts Companion",
            "",
            f"- [Michael Munkasey - {axis.display} Concepts](../derived/munkasey-{axis.slug}-concepts.md)",
        ]
    )


def _comparative_schema() -> str:
    return """- core meaning: source-native axis statements from each ingested source are preserved side by side above.
- psychology: aphoristic, experiential, aspect-family, and thesis/anti formulations remain source-native instead of being flattened together.
- body/health: sources that isolate bodily implications keep them inside their own entries, and Munkasey adds an explicit `With Body or Mind` field.
- social/relationship: interpersonal implications remain inside their source blocks, and Munkasey's relationship thesis/anti stays separate.
- events/manifestations: Munkasey adds politics/business axis emphases, Carter remains axis-level aspect doctrine where present, and oriented activation pages stay unchanged.
- conflicts/notes: source `+` headings are normalized as midpoint-axis identities, and Munkasey's page-3 `CONCEPTS` list lives on the linked companion page instead of being merged into doctrine."""


def _contradictions_text() -> str:
    return """- No direct contradiction is recorded yet among the ingested source entries on this axis.
- Differences are preserved as distinct source voices, emphases, and source structures rather than flattened into one wording."""


def _render_links(factors: list[str], source_pages: list[str]) -> str:
    lines = [
        f"- [{factor}](../factors/{factor.lower()}.md)"
        for factor in factors
    ]
    for slug in source_pages:
        lines.append(f"- [{SOURCE_TITLES[slug]}](../sources/{slug}.md)")
    return "\n".join(lines)


def _render_axis_page(axis_path: Path, block: MunkaseyAxisBlock) -> str:
    page = load_page(axis_path)
    meta = page.meta
    axis = normalize_axis(block.factor_a, block.factor_b)
    astronomicon_axis = f"{astronomicon_token(axis.factors[0])}/{astronomicon_token(axis.factors[1])}"
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != axis.display
        else ""
    )
    entries = _source_entries(page.body)
    entries = [entry for entry in entries if not entry.startswith(f"### {SOURCE_TITLE}\n")]
    entries.append(_render_munkasey_entry(block))
    source_pages = list(meta.get("source_pages", []) or [])
    if SOURCE_SLUG not in source_pages:
        source_pages.append(SOURCE_SLUG)
    related_activations = list(meta.get("related_activations", []) or [])
    related_triad_hubs = list(meta.get("related_triad_hubs", []) or [])
    aliases = list(meta.get("aliases", []) or [])
    derived_text = _section_body(page.body, "## Derived Synthesis", "## Links")
    entries_text = "\n\n".join(entries)
    related_links = "\n".join(
        f"- [{name}](../activations/{name.lower().replace('/', '-').replace(' = ', '-equals-').replace(' ', '-')}.md)"
        for name in related_activations
    )
    return f"""---
title: {axis.display}
page_type: axis
slug: {meta['slug']}
status: source_ingested
framework_scope: comparative
factors:
{_yaml_list(list(meta['factors']), indent=2)}
normalized_axis: {meta['normalized_axis']}
factor_a: {meta['factor_a']}
factor_b: {meta['factor_b']}
related_activations:
{_yaml_list(related_activations, indent=2)}
related_triad_hubs:
{_yaml_list(related_triad_hubs, indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Axis: `{axis.display}`
{astronomicon_line}- Canonical page type: comparative axis page grounded in source-native pair entries.

## Source Entries

{entries_text}

## Comparative Schema

{_comparative_schema()}

## Related Activations

{related_links}

## Contradictions

{_contradictions_text()}

## Derived Synthesis

{derived_text or DEFAULT_DERIVED_TEXT}

## Links

{_render_links(list(meta["factors"]), source_pages)}
"""


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
    factor_links = "\n".join(f"- [{factor}](../factors/{factor.lower()}.md)" for factor in factors)
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

- This preservation slice merges the source's page-1 axis prose into canonical axis pages.
- The page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`.
- The page-2 activations and page-4 `With Itself` activations are intentionally deferred in this slice.
- The page-4 MWA example tables were intentionally omitted.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{len(blocks)}`.
- Page-1 axis prose was merged into the canonical axis pages for every explicit midpoint pair in the source.

## Concepts Companion Pages

- Concepts companion pages generated: `{len(blocks)}`.
- Browse `wiki/derived/` or [Index](../index.md) for the full set.

## Activations Covered

- None. This preservation slice intentionally stops at page-1 axis prose and page-3 concepts.

## Ingestion History

- 2026-04-22: Ingested Munkasey's page-1 axis prose into canonical axis pages, preserved the page-3 `CONCEPTS` corpus as source-grounded companion pages, and intentionally omitted the page-4 MWA example tables.
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


def write_axis_pages(blocks: list[MunkaseyAxisBlock], axis_dir: Path) -> None:
    for block in blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        path = axis_dir / f"{axis.slug}.md"
        path.write_text(_render_axis_page(path, block), encoding="utf-8")


def append_log_entry(log_path: Path, axis_count: int) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        f"- {UPDATED_AT}: Ingested Michael Munkasey's page-1 axis prose into `{axis_count}` canonical axis pages, "
        f"preserved `{axis_count}` page-3 concepts companion pages, intentionally omitted the page-4 MWA example tables, "
        "and rebuilt the index."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path(".")
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    blocks = generate_models(pdf_path)
    wiki_root = root / "wiki"
    write_axis_pages(blocks, wiki_root / "axes")
    write_source_page(blocks, wiki_root / "sources")
    write_concepts_pages(blocks, wiki_root / "derived")
    append_log_entry(wiki_root / "log.md", len(blocks))
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
