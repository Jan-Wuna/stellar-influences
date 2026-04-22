from __future__ import annotations

from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.falis_source import (
    FRAMEWORK_SCOPE as FALIS_FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    AxisBlock,
    generate_models,
)
from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token, factor_slug, normalize_axis
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-21"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _axis_link(name: str) -> str:
    return f"../axes/{name.lower().replace('/', '-').replace(' ', '-')}.md"


def _parse_witte_entry(body: str) -> tuple[str, str, str]:
    summary_match = re.search(
        r"### Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures\s+"
        r"- Source heading: `([^`]+)`\s+"
        r"- Source page: `([^`]+)`\s+"
        r"#### Pair Summary\s+(.*?)\s+(?:### Michelle Falis - Planet Combinations: Astrological Brainstorms|## Comparative Schema)",
        body,
        re.S,
    )
    if summary_match:
        return summary_match.group(1), summary_match.group(2), summary_match.group(3).strip()

    heading_match = re.search(r"- Source heading: `([^`]+)`", body)
    page_match = re.search(r"- Source page: `([^`]+)`", body)
    summary_match = re.search(
        r"### Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures\s+#### Pair Summary\s+(.*?)\s+## Comparative Schema",
        body,
        re.S,
    )
    if not heading_match or not page_match or not summary_match:
        raise ValueError("could not parse existing Witte axis entry")
    return heading_match.group(1), page_match.group(1), summary_match.group(1).strip()


def _render_axis_page(existing_path: Path, falis_block: AxisBlock) -> str:
    page = load_page(existing_path)
    meta = page.meta
    witte_heading, witte_page, witte_summary = _parse_witte_entry(page.body)
    axis = normalize_axis(falis_block.factor_a, falis_block.factor_b)
    astronomicon_axis = f"{astronomicon_token(axis.factors[0])}/{astronomicon_token(axis.factors[1])}"
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != axis.display
        else ""
    )
    source_pages = list(meta.get("source_pages", []) or [])
    if SOURCE_SLUG not in source_pages:
        source_pages.append(SOURCE_SLUG)
    related_activations = list(meta.get("related_activations", []) or [])
    related_triad_hubs = list(meta.get("related_triad_hubs", []) or [])
    aliases = list(meta.get("aliases", []) or [])
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

### {WITTE_TITLE}

- Source heading: `{witte_heading}`
- Source page: `{witte_page}`

#### Pair Summary

{witte_summary}

### {SOURCE_TITLE}

- Source heading: `{axis.display}`
- Source page: `{falis_block.page}`

#### Falis Entry

{falis_block.text}

## Comparative Schema

- core meaning: source-native Witte and Falis axis statements are preserved side by side above.
- psychology: Falis leans more heavily into experiential and psychological phrasing, while Witte stays compressed and aphoristic.
- body/health: no dedicated body or health subsection is isolated by either source on this axis page.
- social/relationship: both sources keep interpersonal implications inside the axis entry itself when relevant.
- events/manifestations: see the source entries above and the orientation-specific activation pages linked below; Falis remains axis-only here.
- conflicts/notes: this page preserves distinct source voices side by side instead of flattening them into one wording.

## Related Activations

{related_links}

## Contradictions

- No direct contradiction is recorded yet between Witte and Falis on this axis.
- Differences are currently treated as emphasis and vocabulary, not as silently merged doctrine.

## Derived Synthesis

- None yet beyond source structuring.

## Links

- [{axis.factors[0]}](../factors/{factor_slug(axis.factors[0])}.md)
- [{axis.factors[1]}](../factors/{factor_slug(axis.factors[1])}.md)
- [{WITTE_TITLE}](../sources/{WITTE_SLUG}.md)
- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
"""


def _render_source_page(blocks: list[AxisBlock]) -> str:
    factor_links = "\n".join(
        f"- [{factor}](../factors/{factor_slug(factor)}.md)"
        for factor in sorted({item.factor_a for item in blocks} | {item.factor_b for item in blocks}, key=str.casefold)
    )
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {FALIS_FRAMEWORK_SCOPE}
factors:
{_yaml_list(sorted({item.factor_a for item in blocks} | {item.factor_b for item in blocks}, key=str.casefold), indent=2)}
aliases:
  - AstroFix
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Michelle Falis
- Title: *Planet Combinations: Astrological Brainstorms*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This source is axis-only; it does not provide oriented activation formulas or standalone factor chapters.
- Ingest coverage is limited to the explicit two-factor midpoint pair sections from `Sun/Moon` through `Neptune/Pluto`.
- Source headings are normalized into unordered canonical axis identities.
- Falis wording is preserved on the canonical axis pages as source-native brainstorm text.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{len(blocks)}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- None. This source is axis-only and does not state oriented `A/B = C` formulas.

## Ingestion History

- {UPDATED_AT}: Ingested all explicit midpoint pair sections from the Falis source into canonical axis pages.
"""


def _append_log_entry(log_path: Path) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        "- 2026-04-21: Ingested Michelle Falis's axis-only midpoint source into 45 canonical axis pages, "
        "added the new source page, and rebuilt the index without changing the in-progress comparative factor pages."
    )
    if entry not in text:
        text = f"{text}\n{entry}\n"
        log_path.write_text(text, encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    wiki_root = root / "wiki"
    axis_dir = wiki_root / "axes"
    source_dir = wiki_root / "sources"

    blocks = generate_models(pdf_path)
    for block in blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        axis_path = axis_dir / f"{axis.slug}.md"
        axis_path.write_text(_render_axis_page(axis_path, block), encoding="utf-8")

    source_path = source_dir / f"{SOURCE_SLUG}.md"
    source_path.write_text(_render_source_page(blocks), encoding="utf-8")

    _append_log_entry(wiki_root / "log.md")
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
