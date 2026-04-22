from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.carter_source import (
    FRAMEWORK_SCOPE as CARTER_FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    CarterAxisBlock,
    generate_models,
)
from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token, factor_slug, normalize_axis
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-21"
DEFAULT_DERIVED_TEXT = "- None yet beyond source structuring."


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _display_section_heading(heading: str) -> str:
    mapping = {
        "THE HARMONIOUS ASPECTS": "Harmonious Aspects",
        "THE CONJUNCTION": "The Conjunction",
        "THE INHARMONIOUS ASPECTS": "Inharmonious Aspects",
    }
    return mapping.get(heading, heading.title())


def _source_entries(body: str) -> list[str]:
    match = re.search(r"## Source Entries\n\n(.*?)\n\n## Comparative Schema\n", body, re.S)
    if not match:
        raise ValueError("could not parse source entries block")
    return [entry.strip() for entry in re.split(r"(?m)(?=^### )", match.group(1).strip()) if entry.strip()]


def _section_body(body: str, heading: str, next_heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\n\n(.*?)\n\n{re.escape(next_heading)}\n", body, re.S)
    if not match:
        return ""
    return match.group(1).strip()


def _render_carter_entry(block: CarterAxisBlock) -> str:
    parts = [
        f"### {SOURCE_TITLE}",
        "",
        f"- Source heading: `{block.heading}`",
        f"- Source page: `{block.page}`",
    ]
    if block.intro_text:
        parts.extend(
            [
                "",
                "#### Pair Overview",
                "",
                block.intro_text,
            ]
        )
    for section in block.sections:
        parts.extend(
            [
                "",
                f"#### {_display_section_heading(section.heading)}",
                "",
                section.text,
            ]
        )
    if block.example_groups:
        parts.extend(["", "#### Examples", ""])
        for group in block.example_groups:
            parts.append(f"- {group.label}: {group.text}")
    return "\n".join(parts).strip()


def _render_source_page(blocks: list[CarterAxisBlock]) -> str:
    factors = sorted({item.factor_a for item in blocks} | {item.factor_b for item in blocks}, key=str.casefold)
    factor_links = "\n".join(f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in factors)
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {CARTER_FRAMEWORK_SCOPE}
factors:
{_yaml_list(factors, indent=2)}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Charles Carter
- Title: *The Astrological Aspects*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This is an aspect-based source rather than a midpoint-source corpus.
- It is intentionally collapsed into canonical axis pages so Carter can sit beside the existing midpoint-axis entries.
- Carter does not create activation pages, triad hubs, or factor pages in this ingest.
- Pair overviews, aspect-family sections, and family-grouped example lists are preserved where the source provides them.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{len(blocks)}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- None. Carter is ingested only into axis pages and remains out of oriented `A/B = C` activation pages.

## Ingestion History

- {UPDATED_AT}: Ingested Carter aspect material into canonical axis pages, preserving the source's pair introductions, family sections, and example lists.
"""


def _render_axis_page(existing_path: Path, block: CarterAxisBlock) -> str:
    page = load_page(existing_path)
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
    entries.append(_render_carter_entry(block))
    source_pages = list(meta.get("source_pages", []) or [])
    if SOURCE_SLUG not in source_pages:
        source_pages.append(SOURCE_SLUG)
    related_activations = list(meta.get("related_activations", []) or [])
    related_triad_hubs = list(meta.get("related_triad_hubs", []) or [])
    aliases = list(meta.get("aliases", []) or [])
    derived_text = _section_body(page.body, "## Derived Synthesis", "## Links") or DEFAULT_DERIVED_TEXT
    related_links = "\n".join(
        f"- [{name}](../activations/{name.lower().replace('/', '-').replace(' = ', '-equals-').replace(' ', '-')}.md)"
        for name in related_activations
    )
    source_titles = [entry.splitlines()[0].removeprefix("### ").strip() for entry in entries]
    source_links = []
    for slug, title in zip(source_pages, source_titles, strict=False):
        source_links.append(f"- [{title}](../sources/{slug}.md)")
    entries_text = "\n\n".join(entries)
    source_links_text = "\n".join(source_links)
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

- core meaning: source-native Witte, Falis, and Carter statements are preserved side by side above on the same canonical axis page.
- psychology: Witte remains compressed and aphoristic, Falis remains experiential, and Carter adds explicit aspect-family distinctions when the source supplies them.
- body/health: Carter sometimes states health and bodily outcomes directly by aspect family; the other sources remain less sectioned here.
- social/relationship: each source keeps interpersonal implications inside its own source block instead of being silently merged.
- events/manifestations: Carter remains axis-level aspect doctrine only; activation pages stay orientation-specific and unchanged.
- conflicts/notes: this page intentionally mixes midpoint-axis doctrine and Carter's planetary-aspect doctrine because Carter was approved for collapse into the canonical axis page.

## Related Activations

{related_links}

## Contradictions

- No direct contradiction is recorded yet among the ingested source entries on this axis.
- Differences are preserved as distinct source voices and aspect-family emphases rather than flattened into one wording.

## Derived Synthesis

{derived_text}

## Links

- [{axis.factors[0]}](../factors/{factor_slug(axis.factors[0])}.md)
- [{axis.factors[1]}](../factors/{factor_slug(axis.factors[1])}.md)
{source_links_text}
"""


def _append_log_entry(log_path: Path, pair_count: int) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    if pair_count == 1:
        entry = "- 2026-04-21: Pilot-ingested Charles Carter's Sun/Moon aspect material into the canonical axis page and added the Carter source page."
    else:
        entry = "- 2026-04-21: Ingested Charles Carter's aspect source into 36 canonical axis pages as Carter family subsections, added the Carter source page, and kept activation pages unchanged."
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def _parse_pair_arg(value: str) -> tuple[str, str]:
    parts = [part.strip() for part in value.split("/") if part.strip()]
    if len(parts) != 2:
        raise ValueError(f"invalid pair argument: {value}")
    axis = normalize_axis(parts[0], parts[1])
    return axis.factors


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--pairs", nargs="*")
    args = parser.parse_args()

    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    wiki_root = root / "wiki"
    axis_dir = wiki_root / "axes"
    source_dir = wiki_root / "sources"

    limit_pairs = None
    if args.pairs:
        limit_pairs = [_parse_pair_arg(pair) for pair in args.pairs]

    blocks = generate_models(pdf_path, limit_pairs=limit_pairs)
    for block in blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        axis_path = axis_dir / f"{axis.slug}.md"
        axis_path.write_text(_render_axis_page(axis_path, block), encoding="utf-8")

    source_path = source_dir / f"{SOURCE_SLUG}.md"
    source_path.write_text(_render_source_page(blocks), encoding="utf-8")

    _append_log_entry(wiki_root / "log.md", len(blocks))
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
