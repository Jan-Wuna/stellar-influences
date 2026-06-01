from __future__ import annotations

import json
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ebertin_source import AxisBlock, FactorBlock, generate_models
from tools.rebuild_index import build_index
from tools.wiki_identity import (
    astronomicon_token,
    factor_slug,
    normalize_activation,
    normalize_axis,
    normalize_factor,
    normalize_triad,
)
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-22"
DEFAULT_DERIVED_TEXT = ""
DEFAULT_FACTOR_CONTRADICTIONS = (
    "- Source differences on this factor page are preserved as framework emphasis rather than forced contradiction.\n"
    "- This page keeps the contributing source chapters side by side instead of treating one as a gloss on the other."
)
DEFAULT_AXIS_CONTRADICTIONS = (
    "- No direct contradiction is recorded yet among the ingested source entries on this axis.\n"
    "- Differences are preserved as distinct source voices and framework emphases rather than flattened into one wording."
)
DEFAULT_ACTIVATION_CONTRADICTIONS = "- No direct contradiction is recorded yet among the ingested source entries on this activation."

SOURCE_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
SOURCE_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"
SOURCE_FRAMEWORK_SCOPE = "cosmobiology"
UNRESOLVED_REVIEW_SLUG = "ebertin-unresolved-activation-review"
UNRESOLVED_REVIEW_TITLE = "Ebertin Unresolved Activation Review"

WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
SANDBACH_TITLE = "John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"

SOURCE_ORDER = [
    WITTE_SLUG,
    SOURCE_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SANDBACH_SLUG,
    HAND_SLUG,
    MCBROOM_SLUG,
]

SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SANDBACH_SLUG: SANDBACH_TITLE,
    HAND_SLUG: HAND_TITLE,
    MCBROOM_SLUG: MCBROOM_TITLE,
}

SOURCE_SLUGS_BY_TITLE = {title: slug for slug, title in SOURCE_TITLES.items()}

FRAMEWORK_BY_SOURCE = {
    WITTE_SLUG: "hamburg_school",
    SOURCE_SLUG: SOURCE_FRAMEWORK_SCOPE,
    FALIS_SLUG: "modern_astrology",
    CARTER_SLUG: "classical_aspects",
    SANDBACH_SLUG: "modern_astrology",
    HAND_SLUG: "modern_astrology",
    MCBROOM_SLUG: "modern_astrology",
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
    return FRAMEWORK_BY_SOURCE.get(ordered[0], SOURCE_FRAMEWORK_SCOPE)


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


def _source_page_refs(body: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for block in _source_entry_blocks(body):
        title = _entry_title(block)
        page_match = re.search(r"- Source page: `([^`]+)`", block)
        if page_match:
            refs.append((title, page_match.group(1)))
    return refs


def _factor_link(name: str) -> str:
    factor = normalize_factor(name)
    return f"- [{factor.display}](../factors/{factor.slug}.md)"


def _source_links(source_pages: list[str]) -> str:
    return "\n".join(
        f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)"
        for slug in _ordered_source_pages(source_pages)
    )


def _activation_identity_from_display(display: str):
    left, right = display.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    activated_by = right.strip()
    return normalize_activation(factor_a, factor_b, activated_by)


def _activation_link(display: str) -> str:
    identity = _activation_identity_from_display(display)
    return f"- [{identity.display}](../activations/{identity.slug}.md)"


def _triad_names_from_activations(activations: list[str]) -> list[str]:
    names = {
        " ".join(_activation_identity_from_display(display).triad_set)
        for display in activations
        if _activation_identity_from_display(display).has_distinct_triad
    }
    return sorted(names, key=str.casefold)


def _format_source_section(title: str, text: str) -> str:
    if not text:
        return f"#### {title}\n\n- None extracted."
    return f"#### {title}\n\n{text}"


def _unresolved_activation_rows(axis_blocks: list[AxisBlock]) -> list[dict[str, str | int | None]]:
    rows: list[dict[str, str | int | None]] = []
    for block in axis_blocks:
        axis_identity = normalize_axis(block.factor_a, block.factor_b)
        for entry in block.unresolved_activation_entries:
            rows.append(
                {
                    "axis": axis_identity.display,
                    "source_heading": block.source_heading,
                    "entry": entry.code,
                    "source_page": entry.page,
                    "raw_token": entry.token,
                    "excerpt": entry.excerpt,
                }
            )
    return sorted(
        rows,
        key=lambda row: (
            str(row["axis"]).casefold(),
            str(row["entry"]),
        ),
    )


def _render_unresolved_review_page(rows: list[dict[str, str | int | None]]) -> str:
    if rows:
        status_lines = [
            f"- Unresolved activation entries skipped pending decode: `{len(rows)}`.",
            f"- Machine-readable manifest: `{UNRESOLVED_REVIEW_SLUG}.json`.",
        ]
        review_blocks = []
        for row in rows:
            token = row["raw_token"] or "(blank)"
            review_blocks.append(
                f"""### {row["axis"]}

- Source heading: `{row["source_heading"]}`
- Entry: `{row["entry"]}`
- Source page: `{row["source_page"]}`
- Raw token: `{token}`
- Excerpt: {row["excerpt"]}"""
            )
        review_list = "\n\n".join(review_blocks)
    else:
        status_lines = [
            "- No unresolved Ebertin activation entries are currently blocked.",
            f"- Machine-readable manifest: `{UNRESOLVED_REVIEW_SLUG}.json`.",
        ]
        review_list = "- None."

    return f"""---
title: {UNRESOLVED_REVIEW_TITLE}
page_type: derived
slug: {UNRESOLVED_REVIEW_SLUG}
status: source_ingested
framework_scope: {SOURCE_FRAMEWORK_SCOPE}
factors: []
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Purpose

- This page lists Ebertin activation entries that were skipped during canonical ingest because the activator token could not be decoded confidently.
- Decoded axis summaries and activation entries are still merged into the live comparative corpus.

## Status

{chr(10).join(status_lines)}

## Review List

{review_list}

## Links

- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
"""


def _render_unresolved_review_manifest(rows: list[dict[str, str | int | None]]) -> str:
    return json.dumps(
        {
            "source_slug": SOURCE_SLUG,
            "source_title": SOURCE_TITLE,
            "updated_at": UPDATED_AT,
            "unresolved_entries": rows,
        },
        indent=2,
    ) + "\n"


def _ebertin_axis_entry(block: AxisBlock) -> str:
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`

{_format_source_section("Principle", block.sections.get("Principle", ""))}

{_format_source_section("Psychological Correspondence", block.sections.get("Psychological Correspondence", ""))}

{_format_source_section("Biological Correspondence", block.sections.get("Biological Correspondence", ""))}

{_format_source_section("Sociological Correspondence", block.sections.get("Sociological Correspondence", ""))}

{_format_source_section("Probable Manifestations", block.sections.get("Probable Manifestations", ""))}""".strip()


def _ebertin_activation_entry(block: AxisBlock, entry) -> str:
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{entry.page}`
- Entry: `{entry.code}`

#### Ebertin Entry

{entry.text}""".strip()


def _ebertin_factor_entry(block: FactorBlock) -> str:
    sign_section_name = "Position in Houses and Signs" if block.sign_entries else "Position in the Signs"
    sign_lines = "\n".join(
        f"- {entry.sign} (`{entry.code}`, page `{entry.page}`): {entry.text}"
        for entry in block.sign_entries
    ) or "- None extracted."
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`

{_format_source_section("Principle", block.sections.get("Principle", ""))}

{_format_source_section("Psychological Correspondence", block.sections.get("Psychological Correspondence", ""))}

{_format_source_section("Biological Correspondence", block.sections.get("Biological Correspondence", ""))}

{_format_source_section("Sociological Correspondence", block.sections.get("Sociological Correspondence", ""))}

#### {sign_section_name}

{sign_lines}""".strip()


def _render_factor_page(path: Path, block: FactorBlock) -> str:
    page = load_page(path)
    factor = normalize_factor(block.factor)
    aliases = list(page.meta.get("aliases", []) or [])
    source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    source_entries = _merge_source_entries(page.body, _ebertin_factor_entry(block), SOURCE_TITLE)
    contradictions = (
        _section_body(page.body, "Contradictions and Framework Notes") or DEFAULT_FACTOR_CONTRADICTIONS
    )
    derived = _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT
    related_axes = _section_body(page.body, "Related Axes") or "- None generated."
    related_activations = _section_body(page.body, "Related Activations") or "- None."
    open_questions = _section_body(page.body, "Open Questions") or "- None recorded yet."
    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon = astronomicon_token(factor.display)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor.display
        else ""
    )

    return f"""---
title: {factor.display}
page_type: factor
slug: {factor.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list([factor.display], indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Factor: {factor.display}
{astronomicon_line}- Canonical page type: comparative factor page grounded in standalone source chapters.

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native factor entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened.
- body/health: bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: sign-position or chapter-level extensions remain attached to the source entry that states them.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Contradictions and Framework Notes

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Related Axes

{related_axes}

## Related Activations

{related_activations}

## Related Sources

{_source_links(source_pages)}

## Open Questions

{open_questions}
"""


def _render_axis_page(path: Path, block: AxisBlock) -> str:
    axis_identity = normalize_axis(block.factor_a, block.factor_b)
    default_aliases = [f"{axis_identity.factors[1]}/{axis_identity.factors[0]}"]
    new_activations = [
        normalize_activation(block.factor_a, block.factor_b, entry.activated_by).display
        for entry in block.activation_entries
    ]

    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or default_aliases)
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _merge_source_entries(page.body, _ebertin_axis_entry(block), SOURCE_TITLE)
        existing_related = list(page.meta.get("related_activations", []) or [])
        contradictions = _section_body(page.body, "Contradictions") or DEFAULT_AXIS_CONTRADICTIONS
        derived = _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT
    else:
        aliases = default_aliases
        source_pages = [SOURCE_SLUG]
        source_entries = _ebertin_axis_entry(block)
        existing_related = []
        contradictions = DEFAULT_AXIS_CONTRADICTIONS
        derived = DEFAULT_DERIVED_TEXT

    related_activations = sorted(set(existing_related) | set(new_activations), key=str.casefold)
    related_triad_hubs = _triad_names_from_activations(related_activations)
    related_links = "\n".join(_activation_link(item) for item in related_activations)
    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon_axis = f"{astronomicon_token(axis_identity.factors[0])}/{astronomicon_token(axis_identity.factors[1])}"
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != axis_identity.display
        else ""
    )

    return f"""---
title: {axis_identity.display}
page_type: axis
slug: {axis_identity.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list(list(axis_identity.factors), indent=2)}
normalized_axis: {axis_identity.display}
factor_a: {axis_identity.factors[0]}
factor_b: {axis_identity.factors[1]}
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

- Axis: `{axis_identity.display}`
{astronomicon_line}- Canonical page type: comparative axis page grounded in source-native pair entries.

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native pair entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened.
- body/health: source-native biological or bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: see the source entries above and the orientation-specific activation pages linked below.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Related Activations

{related_links}

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{_factor_link(axis_identity.factors[0])}
{_factor_link(axis_identity.factors[1])}
{_source_links(source_pages)}
"""


def _render_activation_page(path: Path, block: AxisBlock, entry) -> str:
    identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)

    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or [])
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _merge_source_entries(page.body, _ebertin_activation_entry(block, entry), SOURCE_TITLE)
        contradictions = _section_body(page.body, "Contradictions") or DEFAULT_ACTIVATION_CONTRADICTIONS
        derived = _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT
    else:
        aliases = []
        source_pages = [SOURCE_SLUG]
        source_entries = _ebertin_activation_entry(block, entry)
        contradictions = DEFAULT_ACTIVATION_CONTRADICTIONS
        derived = DEFAULT_DERIVED_TEXT

    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon_formula = (
        f"{astronomicon_token(identity.axis.factors[0])}/"
        f"{astronomicon_token(identity.axis.factors[1])} = "
        f"{astronomicon_token(identity.activated_by)}"
    )
    astronomicon_line = (
        f"- Astronomicon formula: `{astronomicon_formula}`\n"
        if astronomicon_formula != identity.display
        else ""
    )

    return f"""---
title: {identity.display}
page_type: activation
slug: {identity.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list([identity.axis.factors[0], identity.axis.factors[1], identity.activated_by], indent=2)}
normalized_formula: {identity.display}
axis: {identity.axis.display}
activated_by: {identity.activated_by}
triad_set:
{_yaml_list(list(identity.triad_set), indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Formula: `{identity.display}`
{astronomicon_line}- Axis page: [{identity.axis.display}](../axes/{identity.axis.slug}.md)
- Triad hub: [{' '.join(identity.triad_set)}](../triads/{normalize_triad(identity.triad_set).slug}.md)

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native activation entries are preserved side by side above.
- psychology: each source keeps its own phrasing and emphasis for the same orientation-specific formula.
- body/health: bodily implications remain embedded inside the source-native entry when present.
- social/relationship: interpersonal implications remain attached to each source entry instead of being collapsed.
- events/manifestations: this page preserves the activation as an orientation-specific formula with source-backed statements only.
- conflicts/notes: orientation-specific meaning is preserved on its own page and not merged into the triad hub.

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{_factor_link(identity.axis.factors[0])}
{_factor_link(identity.axis.factors[1])}
{_factor_link(identity.activated_by)}
- [{identity.axis.display}](../axes/{identity.axis.slug}.md)
- [{' '.join(identity.triad_set)}](../triads/{normalize_triad(identity.triad_set).slug}.md)
{_source_links(source_pages)}
"""


def _render_triad_page(triad_factors: tuple[str, str, str], activation_dir: Path) -> str:
    identity = normalize_triad(triad_factors)
    activation_pages = []
    orientation_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if activation_path.exists():
            activation_pages.append(load_page(activation_path))
            orientation_lines.append(_activation_link(orientation))
        else:
            orientation_lines.append(f"- `{orientation}` (activation page not available)")

    source_pages = _ordered_source_pages(
        [source for page in activation_pages for source in list(page.meta.get("source_pages", []) or [])]
    )
    framework_scope = _framework_scope_for_sources(source_pages)
    coverage_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if not activation_path.exists():
            coverage_lines.append(f"- `{orientation}`: no activation page is currently available.")
            continue
        page = load_page(activation_path)
        for title, source_page in _source_page_refs(page.body):
            coverage_lines.append(f"- `{orientation}`: {title}, page `{source_page}`")

    astronomicon_triad = " ".join(astronomicon_token(factor) for factor in identity.factors)
    astronomicon_line = (
        f"- Astronomicon triad-set: `{astronomicon_triad}`\n"
        if astronomicon_triad != identity.display
        else ""
    )

    return f"""---
title: {identity.display}
page_type: triad_hub
slug: {identity.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list(list(identity.factors), indent=2)}
triad_set:
{_yaml_list(list(identity.factors), indent=2)}
orientations:
{_yaml_list(list(identity.orientations), indent=2)}
aliases: []
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Triad-set: `{identity.display}`
{astronomicon_line}- This page is structural only. It does not merge the meanings of its orientations.

## Orientation Map

{chr(10).join(orientation_lines)}

## Source Coverage

{chr(10).join(coverage_lines)}

## Contradictions Across Orientations

- None recorded yet.
- Distinct meanings across orientations are preserved as orientation differences, not collapsed into one interpretation.

## Links

{chr(10).join(_factor_link(factor) for factor in identity.factors)}
{_source_links(source_pages)}
"""


def _render_source_page(
    factors: list[FactorBlock],
    axis_count: int,
    activation_count: int,
    triad_count: int,
    unresolved_count: int,
) -> str:
    factor_links = "\n".join(
        _factor_link(factor.factor)
        for factor in factors
    )
    return f"""---
title: {SOURCE_TITLE}
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {SOURCE_FRAMEWORK_SCOPE}
factors:
{_yaml_list([factor.factor for factor in factors], indent=2)}
aliases:
  - COSI
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Reinhold Ebertin
- Title: *The Combination of Stellar Influences*
- Vault file: `Stellar Influences Vault/planetary expressions - Reinhold Ebertin - The Combination Of Stellar Influences.pdf`

## Scope Notes

- This source contributes standalone factor chapters plus explicit midpoint-axis and orientation-specific activation entries.
- The live comparative wiki now preserves Ebertin's source-native axis summaries and activation entries on canonical axis and activation pages.
- Triad hubs remain structural pages; Ebertin triad coverage is derived from the linked orientation-specific activation pages.
- Canonical wiki identities still preserve orientation-specific activation meanings separately.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{axis_count}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- Canonical activation pages updated or created: `{activation_count}`.
- Canonical triad hubs updated or created: `{triad_count}`.
- Browse [Index](../index.md), `wiki/activations/`, and `wiki/triads/` for the full set.

## Review Queue

- Unresolved activation entries skipped pending decode: `{unresolved_count}`.
- Review list: [Ebertin unresolved activation review](../derived/{UNRESOLVED_REVIEW_SLUG}.md)
- Machine-readable manifest: `wiki/derived/{UNRESOLVED_REVIEW_SLUG}.json`

## Ingestion History

- 2026-04-21: Ebertin factor chapters were restored to the live comparative wiki.
- {UPDATED_AT}: Merged Ebertin axis summaries and orientation-specific activation entries into the live comparative axis, activation, and triad corpus.
"""


def _append_log_entry(log_path: Path, axis_count: int, activation_count: int, triad_count: int) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        f"- {UPDATED_AT}: Merged Reinhold Ebertin's axis summaries and orientation-specific activation entries "
        f"into the live comparative wiki, updating {axis_count} canonical axis pages, {activation_count} activation pages, "
        f"and {triad_count} triad hubs without collapsing activation orientations."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    wiki_root = root / "wiki"
    factor_dir = wiki_root / "factors"
    axis_dir = wiki_root / "axes"
    activation_dir = wiki_root / "activations"
    triad_dir = wiki_root / "triads"
    derived_dir = wiki_root / "derived"
    source_dir = wiki_root / "sources"

    factor_blocks, axis_blocks = generate_models(
        root / "Stellar Influences Vault" / "planetary expressions - Reinhold Ebertin - The Combination Of Stellar Influences.pdf"
    )
    unresolved_rows = _unresolved_activation_rows(axis_blocks)

    for block in factor_blocks:
        factor_identity = normalize_factor(block.factor)
        (factor_dir / f"{factor_identity.slug}.md").write_text(
            _render_factor_page(factor_dir / f"{factor_identity.slug}.md", block),
            encoding="utf-8",
        )

    triads_touched: set[tuple[str, str, str]] = set()
    activation_count = 0
    for block in axis_blocks:
        axis_identity = normalize_axis(block.factor_a, block.factor_b)
        (axis_dir / f"{axis_identity.slug}.md").write_text(
            _render_axis_page(axis_dir / f"{axis_identity.slug}.md", block),
            encoding="utf-8",
        )

        for entry in block.activation_entries:
            activation_identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            (activation_dir / f"{activation_identity.slug}.md").write_text(
                _render_activation_page(activation_dir / f"{activation_identity.slug}.md", block, entry),
                encoding="utf-8",
            )
            triads_touched.add(activation_identity.triad_set)
            activation_count += 1

    for triad in sorted(triads_touched, key=lambda item: tuple(name.casefold() for name in item)):
        triad_identity = normalize_triad(triad)
        (triad_dir / f"{triad_identity.slug}.md").write_text(
            _render_triad_page(triad, activation_dir),
            encoding="utf-8",
        )

    (derived_dir / f"{UNRESOLVED_REVIEW_SLUG}.md").write_text(
        _render_unresolved_review_page(unresolved_rows),
        encoding="utf-8",
    )
    (derived_dir / f"{UNRESOLVED_REVIEW_SLUG}.json").write_text(
        _render_unresolved_review_manifest(unresolved_rows),
        encoding="utf-8",
    )

    (source_dir / f"{SOURCE_SLUG}.md").write_text(
        _render_source_page(
            factor_blocks,
            len(axis_blocks),
            activation_count,
            len(triads_touched),
            len(unresolved_rows),
        ),
        encoding="utf-8",
    )

    _append_log_entry(wiki_root / "log.md", len(axis_blocks), activation_count, len(triads_touched))
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
