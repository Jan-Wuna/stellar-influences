from __future__ import annotations

from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.mcbroom_source import (
    FRAMEWORK_SCOPE as MCBROOM_FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    SourceBlock,
    generate_models,
)
from tools.rebuild_index import build_index
from tools.wiki_identity import FACTOR_ORDER, factor_slug, normalize_axis, normalize_triad
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-22"
DEFAULT_DERIVED_TEXT = ""

WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
EBERTIN_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
SANDBACH_TITLE = "John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"

SOURCE_ORDER = [
    WITTE_SLUG,
    EBERTIN_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SANDBACH_SLUG,
    HAND_SLUG,
    SOURCE_SLUG,
]

SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    EBERTIN_SLUG: EBERTIN_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SANDBACH_SLUG: SANDBACH_TITLE,
    HAND_SLUG: HAND_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
}

SOURCE_SLUGS_BY_TITLE = {title: slug for slug, title in SOURCE_TITLES.items()}

FRAMEWORK_BY_SOURCE = {
    WITTE_SLUG: "hamburg_school",
    EBERTIN_SLUG: "cosmobiology",
    FALIS_SLUG: "modern_astrology",
    CARTER_SLUG: "classical_aspects",
    SANDBACH_SLUG: "modern_astrology",
    HAND_SLUG: "modern_astrology",
    SOURCE_SLUG: MCBROOM_FRAMEWORK_SCOPE,
}


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _ordered_source_pages(items: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return sorted(unique, key=lambda slug: (SOURCE_ORDER.index(slug) if slug in SOURCE_ORDER else 999, slug))


def _framework_scope_for_sources(source_pages: list[str]) -> str:
    ordered = _ordered_source_pages(source_pages)
    if len(ordered) > 1:
        return "comparative"
    return FRAMEWORK_BY_SOURCE[ordered[0]]


def _section_body(body: str, heading: str) -> str:
    match = re.search(rf"## {re.escape(heading)}\s+(.*?)(?=\n## |\Z)", body, re.S)
    return match.group(1).strip() if match else ""


def _source_entry_blocks(body: str) -> list[str]:
    section = _section_body(body, "Source Entries")
    if not section:
        return []
    return [block.strip() for block in re.split(r"(?m)(?=^### )", section.strip()) if block.strip()]


def _entry_title(block: str) -> str:
    match = re.match(r"^### ([^\n]+)", block)
    if match is None:
        raise ValueError("source entry block is missing a title heading")
    return match.group(1).strip()


def _merge_source_entries(body: str, addition: str, title: str) -> str:
    blocks = _source_entry_blocks(body)
    existing_index = {_entry_title(block): index for index, block in enumerate(blocks)}
    by_title = {_entry_title(block): block for block in blocks}
    by_title[title] = addition.strip()
    ordered_titles = sorted(
        by_title,
        key=lambda item: (
            SOURCE_ORDER.index(SOURCE_SLUGS_BY_TITLE[item]) if item in SOURCE_SLUGS_BY_TITLE else 999,
            existing_index.get(item, len(existing_index)),
            item.casefold(),
        ),
    )
    return "\n\n".join(by_title[item] for item in ordered_titles)


def _factor_link(name: str) -> str:
    return f"- [{name}](../factors/{factor_slug(name)}.md)"


def _source_links(source_pages: list[str]) -> str:
    return "\n".join(
        f"- [{SOURCE_TITLES[slug]}](../sources/{slug}.md)"
        for slug in _ordered_source_pages(source_pages)
    )


def _mcbroom_entry(block: SourceBlock) -> str:
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`

#### McBroom Entry

{block.text}""".strip()


def _render_axis_page(path: Path, block: SourceBlock) -> str:
    page = load_page(path)
    meta = page.meta
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    source_entries = _merge_source_entries(page.body, _mcbroom_entry(block), SOURCE_TITLE)
    identity = _section_body(page.body, "Identity")
    comparative_schema = _section_body(page.body, "Comparative Schema")
    related_activations = _section_body(page.body, "Related Activations")
    contradictions = _section_body(page.body, "Contradictions")
    derived = _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT
    links = "\n".join(
        [
            _factor_link(factor)
            for factor in meta.get("factors", []) or []
        ]
        + [_source_links(source_pages)]
    )

    return f"""---
title: {meta['title']}
page_type: axis
slug: {meta['slug']}
status: source_ingested
framework_scope: {_framework_scope_for_sources(source_pages)}
factors:
{_yaml_list(list(meta['factors']), indent=2)}
normalized_axis: {meta['normalized_axis']}
factor_a: {meta['factor_a']}
factor_b: {meta['factor_b']}
related_activations:
{_yaml_list(list(meta.get('related_activations', []) or []), indent=2)}
related_triad_hubs:
{_yaml_list(list(meta.get('related_triad_hubs', []) or []), indent=2)}
aliases:
{_yaml_list(list(meta.get('aliases', []) or []), indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

{identity}

## Source Entries

{source_entries}

## Comparative Schema

{comparative_schema}

## Related Activations

{related_activations}

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{links}
"""


def _render_activation_page(path: Path, block: SourceBlock) -> str:
    page = load_page(path)
    meta = page.meta
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    source_entries = _merge_source_entries(page.body, _mcbroom_entry(block), SOURCE_TITLE)
    identity = _section_body(page.body, "Identity")
    comparative_schema = _section_body(page.body, "Comparative Schema")
    contradictions = _section_body(page.body, "Contradictions")
    derived = _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT
    triad = normalize_triad(list(meta["triad_set"]))
    links = "\n".join(
        [
            _factor_link(factor)
            for factor in meta.get("factors", []) or []
        ]
        + [
            f"- [{meta['axis']}](../axes/{meta['axis'].lower().replace('/', '-')}.md)",
            f"- [{triad.display}](../triads/{triad.slug}.md)",
            _source_links(source_pages),
        ]
    )

    return f"""---
title: {meta['title']}
page_type: activation
slug: {meta['slug']}
status: source_ingested
framework_scope: {_framework_scope_for_sources(source_pages)}
factors:
{_yaml_list(list(meta['factors']), indent=2)}
normalized_formula: {meta['normalized_formula']}
axis: {meta['axis']}
activated_by: {meta['activated_by']}
triad_set:
{_yaml_list(list(meta['triad_set']), indent=2)}
aliases:
{_yaml_list(list(meta.get('aliases', []) or []), indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

{identity}

## Source Entries

{source_entries}

## Comparative Schema

{comparative_schema}

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{links}
"""


def _render_source_page(blocks: list[SourceBlock]) -> str:
    factors = sorted(
        {"Sun", "Moon", "Mercury", "Asc", "MC"},
        key=lambda name: (FACTOR_ORDER.get(name, 999), name.casefold()),
    )
    factor_links = "\n".join(_factor_link(factor) for factor in factors)
    axis_count = sum(1 for block in blocks if block.page_type == "axis")
    activation_count = sum(1 for block in blocks if block.page_type == "activation")
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {MCBROOM_FRAMEWORK_SCOPE}
factors:
{_yaml_list(factors, indent=2)}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Don McBroom
- Title: *Midpoints*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This source is a methodology-heavy midpoint text.
- The live ingest is intentionally limited to explicit doctrine on the `Sun/Moon` axis, the `Ascendant/Midheaven` axis, and one pilot focal-point activation on each axis.
- General technique, orb policy, chart-synthesis workflow, unknown-birth-time handling, closest-midpoint-picture logic, special aspect structures, and transits/progressions/solar arcs are excluded from canonical ingest.
- Vernal Point material is excluded from this pilot pending a separate schema decision.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{axis_count}`.
- Browse [Index](../index.md) or `wiki/axes/` for the pilot pages touched by this source.

## Activations Covered

- Canonical activation pages updated or created: `{activation_count}`.
- Browse [Index](../index.md) or `wiki/activations/` for the pilot pages touched by this source.

## Ingestion History

- {UPDATED_AT}: Added a bounded McBroom pilot touching `2` axis pages and `2` activation pages without ingesting methodology or timing chapters.
"""


def _append_log_entry(log_path: Path) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        "- 2026-04-22: Added a bounded Don McBroom pilot ingest touching the `Sun/Moon` and `Asc/MC` axis pages "
        "plus the `Sun/Moon = Mercury` and `Asc/MC = Mercury` activation pages, while excluding methodology and timing chapters."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    wiki_root = root / "wiki"
    blocks = generate_models(pdf_path)

    for block in blocks:
        if block.page_type == "axis":
            path = wiki_root / "axes" / f"{block.slug}.md"
            path.write_text(_render_axis_page(path, block), encoding="utf-8")
        elif block.page_type == "activation":
            path = wiki_root / "activations" / f"{block.slug}.md"
            path.write_text(_render_activation_page(path, block), encoding="utf-8")
        else:
            raise ValueError(f"Unsupported McBroom block type: {block.page_type}")

    source_path = wiki_root / "sources" / f"{SOURCE_SLUG}.md"
    source_path.write_text(_render_source_page(blocks), encoding="utf-8")

    _append_log_entry(wiki_root / "log.md")
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
