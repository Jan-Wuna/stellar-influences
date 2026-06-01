from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.rebuild_index import build_index
from tools.sandbach_source import (
    FACTOR_SEQUENCE,
    FRAMEWORK_SCOPE as SANDBACH_FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    ActivationEntry,
    AxisBlock,
    SOURCE_FACTOR_NAMES,
    generate_models,
)
from tools.wiki_identity import (
    CANONICAL_FACTORS,
    astronomicon_token,
    normalize_activation,
    normalize_axis,
    normalize_factor,
    normalize_triad,
)
from tools.wiki_pages import load_page


UPDATED_AT = "2026-04-21"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
EBERTIN_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"

SOURCE_ORDER = [
    WITTE_SLUG,
    EBERTIN_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SOURCE_SLUG,
    HAND_SLUG,
    MCBROOM_SLUG,
]

SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    EBERTIN_SLUG: EBERTIN_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
    HAND_SLUG: HAND_TITLE,
    MCBROOM_SLUG: MCBROOM_TITLE,
}

SOURCE_SLUGS_BY_TITLE = {title: slug for slug, title in SOURCE_TITLES.items()}
MISSING_ACTIVATION_TEXT = "Sandbach's visible source page omits a text-bearing entry for this activator; no activation paragraph is available to ingest."

FRAMEWORK_BY_SOURCE = {
    WITTE_SLUG: "hamburg_school",
    EBERTIN_SLUG: "cosmobiology",
    FALIS_SLUG: "modern_astrology",
    CARTER_SLUG: "classical_aspects",
    SOURCE_SLUG: SANDBACH_FRAMEWORK_SCOPE,
    HAND_SLUG: "modern_astrology",
    MCBROOM_SLUG: "modern_astrology",
}


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _ordered_source_pages(items: list[str]) -> list[str]:
    unique = []
    seen = set()
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


def _append_source_entry(existing: str, addition: str, title: str) -> str:
    if title in existing:
        return existing.strip()
    if not existing.strip():
        return addition.strip()
    return f"{existing.rstrip()}\n\n{addition.strip()}"


def _factor_link(name: str) -> str:
    factor = normalize_factor(name)
    return f"- [{factor.display}](../factors/{factor.slug}.md)"


def _axis_link(display: str) -> str:
    axis = normalize_axis(*display.split("/"))
    return f"- [{axis.display}](../axes/{axis.slug}.md)"


def _activation_link(display: str) -> str:
    left, right = display.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    activated_by = right.strip()
    identity = normalize_activation(factor_a, factor_b, activated_by)
    return f"- [{identity.display}](../activations/{identity.slug}.md)"


def _triad_link(display: str) -> str:
    identity = normalize_triad(display.split())
    return f"- [{identity.display}](../triads/{identity.slug}.md)"


def _source_links(source_pages: list[str]) -> str:
    return "\n".join(
        f"- [{SOURCE_TITLES[slug]}](../sources/{slug}.md)"
        for slug in _ordered_source_pages(source_pages)
    )


def _activation_identity_from_display(display: str):
    left, right = display.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    activated_by = right.strip()
    return normalize_activation(factor_a, factor_b, activated_by)


def _triad_names_from_activations(activations: list[str]) -> list[str]:
    names = set()
    for display in activations:
        identity = _activation_identity_from_display(display)
        if identity.has_distinct_triad:
            names.add(" ".join(identity.triad_set))
    return sorted(names, key=str.casefold)


def _source_page_refs(body: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    source_entries = _section_body(body, "Source Entries")
    for match in re.finditer(r"### (.+?)\s+(.*?)(?=\n### |\Z)", source_entries, re.S):
        title = match.group(1).strip()
        block = match.group(2)
        page_match = re.search(r"- Source page: `([^`]+)`", block)
        if page_match:
            refs.append((title, page_match.group(1)))
    return refs


def _axis_identity_block(axis_display: str) -> str:
    factor_a, factor_b = axis_display.split("/")
    identity = normalize_axis(factor_a, factor_b)
    astronomicon_axis = f"{astronomicon_token(identity.factors[0])}/{astronomicon_token(identity.factors[1])}"
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != identity.display
        else ""
    )
    return (
        f"- Axis: `{identity.display}`\n"
        f"{astronomicon_line}"
        "- Canonical page type: comparative axis page grounded in source-native pair entries."
    )


def _sandbach_axis_entry(block: AxisBlock) -> str:
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`

#### Principle

{block.principle}

#### Process

{block.process}"""


def _sandbach_activation_entry(block: AxisBlock, entry: ActivationEntry) -> str:
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`
- Activator: `{SOURCE_FACTOR_NAMES[entry.activated_by]}`

#### Sandbach Entry

{entry.text}"""


def _sandbach_missing_activation_entry(block: AxisBlock, activated_by: str) -> str:
    missing_text = MISSING_ACTIVATION_TEXT
    if activated_by == "Chiron":
        missing_text = (
            "Sandbach's visible source page omits a text-bearing `Chiron` activator entry "
            "for this orientation; no activation paragraph is available to ingest."
        )
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.page}`
- Activator: `{SOURCE_FACTOR_NAMES[activated_by]}`

#### Sandbach Entry

- {missing_text}"""


def _render_axis_page(path: Path, block: AxisBlock) -> str:
    axis_identity = normalize_axis(block.factor_a, block.factor_b)
    new_activations = [
        normalize_activation(block.factor_a, block.factor_b, entry.activated_by).display
        for entry in block.activation_entries
    ]
    aliases = [f"{axis_identity.factors[1]}/{axis_identity.factors[0]}"]
    source_entries = _sandbach_axis_entry(block)
    source_pages = [SOURCE_SLUG]
    existing_related: list[str] = []
    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or aliases)
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _append_source_entry(_section_body(page.body, "Source Entries"), source_entries, SOURCE_TITLE)
        existing_related = list(page.meta.get("related_activations", []) or [])

    related_activations = sorted(set(existing_related) | set(new_activations), key=str.casefold)
    related_triad_hubs = _triad_names_from_activations(related_activations)
    related_links = "\n".join(_activation_link(item) for item in related_activations)
    framework_scope = _framework_scope_for_sources(source_pages)

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

{_axis_identity_block(axis_identity.display)}

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native pair entries are preserved side by side above.
- psychology: Sandbach contributes an explicit `Principle` and `Process` layer, while other sources retain their own native structure and vocabulary.
- body/health: bodily or vitality implications remain embedded inside each source entry when present.
- social/relationship: interpersonal implications remain attached to the source-native wording above instead of being flattened into one paraphrase.
- events/manifestations: see the source entries above and the orientation-specific activation pages linked below.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Related Activations

{related_links}

## Contradictions

- No direct contradiction is recorded yet among the ingested source entries on this axis.
- Differences are preserved as distinct source voices and framework emphases rather than flattened into one interpretation.

<a id="derived-synthesis"></a>

## Derived Synthesis


## Links

{_factor_link(axis_identity.factors[0])}
{_factor_link(axis_identity.factors[1])}
{_source_links(source_pages)}
"""


def _render_activation_page(
    path: Path,
    block: AxisBlock,
    entry: ActivationEntry | None,
    activated_by: str | None = None,
) -> str:
    if entry is not None:
        activated_by = entry.activated_by
        sandbach_entry = _sandbach_activation_entry(block, entry)
        sandbach_entry_is_placeholder = False
    else:
        assert activated_by is not None
        sandbach_entry = _sandbach_missing_activation_entry(block, activated_by)
        sandbach_entry_is_placeholder = True

    identity = normalize_activation(block.factor_a, block.factor_b, activated_by)
    source_pages = [SOURCE_SLUG]
    aliases: list[str] = []
    source_entries = sandbach_entry
    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or [])
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _append_source_entry(_section_body(page.body, "Source Entries"), sandbach_entry, SOURCE_TITLE)

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
    if sandbach_entry_is_placeholder and source_pages == [SOURCE_SLUG]:
        if identity.activated_by == "Chiron":
            comparative_schema = """- core meaning: Sandbach's visible source page omits a text-bearing `Chiron` activator entry for this expected orientation.
- psychology: no source-backed Sandbach wording is available to classify without inventing Chiron doctrine.
- body/health: no source-backed Sandbach wording is available to classify without inventing Chiron doctrine.
- social/relationship: no source-backed Sandbach wording is available to classify without inventing Chiron doctrine.
- events/manifestations: this source-omission slot marks a canonically expected orientation without adding doctrine.
- conflicts/notes: this page is parked as Sandbach-only and should not be expanded interpretively without a new source-scope decision."""
        else:
            comparative_schema = f"""- core meaning: Sandbach's visible source page omits a text-bearing entry for this expected orientation.
- psychology: no source-backed Sandbach wording is available to classify without inventing doctrine.
- body/health: no source-backed Sandbach wording is available to classify without inventing doctrine.
- social/relationship: no source-backed Sandbach wording is available to classify without inventing doctrine.
- events/manifestations: this source-omission slot marks a canonically expected orientation without adding doctrine.
- conflicts/notes: this source-omission slot preserves the canonical orientation without inventing doctrine."""
        contradictions = "- Sandbach's visible source page omits this activator entry; no contradiction can be assessed."
    else:
        comparative_schema = """- core meaning: source-native activation entries are preserved side by side above.
- psychology: each source keeps its own phrasing and emphasis for the same orientation-specific formula.
- body/health: bodily implications remain embedded inside the source-native entry when present.
- social/relationship: interpersonal implications remain attached to each source entry instead of being collapsed.
- events/manifestations: this page preserves the activation as an orientation-specific formula with source-backed statements only.
- conflicts/notes: orientation-specific meaning is preserved on its own page and not merged into the triad hub."""
        contradictions = "- No direct contradiction is recorded yet among the ingested source entries on this activation."

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

{comparative_schema}

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis


## Links

{_factor_link(identity.axis.factors[0])}
{_factor_link(identity.axis.factors[1])}
{_factor_link(identity.activated_by)}
- [{identity.axis.display}](../axes/{identity.axis.slug}.md)
- [{' '.join(identity.triad_set)}](../triads/{normalize_triad(identity.triad_set).slug}.md)
{_source_links(source_pages)}
"""


def _render_triad_page(path: Path, triad_factors: tuple[str, str, str], activation_dir: Path) -> str:
    identity = normalize_triad(triad_factors)
    activation_pages = []
    orientation_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if activation_path.exists():
            activation_pages.append(load_page(activation_path))
            orientation_lines.append(_activation_link(orientation))
        else:
            orientation_lines.append(f"- `{orientation}` (activation page not available from the current extracted source coverage)")
    source_pages = _ordered_source_pages(
        [source for page in activation_pages for source in list(page.meta.get("source_pages", []) or [])]
    )
    framework_scope = _framework_scope_for_sources(source_pages)
    coverage_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if not activation_path.exists():
            coverage_lines.append(f"- `{orientation}`: no activation page is currently available from the extracted source set.")
            continue
        page = load_page(activation_path)
        for title, source_page in _source_page_refs(page.body):
            coverage_lines.append(f"- `{orientation}`: {title}, page `{source_page}`")
    if not coverage_lines:
        coverage_lines.append("- Source coverage is documented on the linked activation pages.")
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


def _render_chiron_factor_page(related_axes: list[str], activation_count: int) -> str:
    factor = normalize_factor("Chiron")
    return f"""---
title: {factor.display}
page_type: factor
slug: {factor.slug}
status: source_ingested
framework_scope: {SANDBACH_FRAMEWORK_SCOPE}
factors:
  - {factor.display}
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Identity

- Factor: {factor.display}
- Canonical page type: structural factor page created because the source treats `{factor.display}` as a first-class participant in axis and activation formulas.
- This page is source-bounded to Sandbach's modern midpoint corpus.
- Do not read it as a comparative factor doctrine page.
- This factor page should not be used as standalone `{factor.display}` doctrine.

## Source Entries

### {SOURCE_TITLE}

- No standalone factor chapter material from this source is ingested on this page.
- `{factor.display}` appears canonically through Sandbach axis pages, activation pages, and triad hubs.

## Comparative Schema

- core meaning: no standalone factor chapter is present in this source.
- psychology: Sandbach expresses `{factor.display}` through axis principles, processes, and activator entries rather than through a dedicated factor chapter.
- body/health: any bodily implications remain embedded inside the axis and activation pages where `{factor.display}` participates.
- social/relationship: relational implications remain embedded inside the linked axis and activation pages.
- events/manifestations: browse the related axes and activations below for the explicit formulas.
- conflicts/notes: this page is structural only until another source contributes standalone `{factor.display}` doctrine.

## Derived Synthesis

- None yet beyond structural placement in the canonical factor inventory.

## Related Axes

{chr(10).join(_axis_link(axis) for axis in related_axes)}

## Related Activations

- Generated activation pages involving `{factor.display}`: `{activation_count}`.
- Browse [Index](../index.md) or the `wiki/activations/` folder for the full set.

## Related Sources

- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)

## Open Questions

- None recorded yet.
"""


def _render_existing_factor_page(path: Path, related_axes: list[str], activation_count: int) -> str:
    page = load_page(path)
    factor = page.meta["title"]
    identity = _section_body(page.body, "Identity")
    source_entries = _section_body(page.body, "Source Entries")
    comparative_schema = _section_body(page.body, "Comparative Schema")
    contradictions_notes = _section_body(page.body, "Contradictions and Framework Notes")
    derived_synthesis = _section_body(page.body, "Derived Synthesis")
    related_sources = _section_body(page.body, "Related Sources")
    open_questions = _section_body(page.body, "Open Questions")

    contradictions_block = ""
    if not contradictions_notes and page.meta["framework_scope"] == "comparative":
        contradictions_notes = (
            "- Source differences on this factor page are preserved as framework emphasis rather than forced contradiction.\n"
            "- This page keeps the contributing source chapters side by side instead of treating one as a gloss on the other."
        )
    if contradictions_notes:
        contradictions_block = f"\n## Contradictions and Framework Notes\n\n{contradictions_notes}\n"

    return f"""---
title: {page.meta['title']}
page_type: factor
slug: {page.meta['slug']}
status: {page.meta['status']}
framework_scope: {page.meta['framework_scope']}
factors:
{_yaml_list(list(page.meta['factors']), indent=2)}
aliases:
{_yaml_list(list(page.meta.get('aliases', []) or []), indent=2)}
source_pages:
{_yaml_list(list(page.meta.get('source_pages', []) or []), indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

{identity}

## Source Entries

{source_entries}

## Comparative Schema

{comparative_schema}
{contradictions_block}

## Derived Synthesis

{derived_synthesis}

## Related Axes

{chr(10).join(_axis_link(axis) for axis in related_axes)}

## Related Activations

- Generated activation pages involving `{factor}`: `{activation_count}`.
- Browse [Index](../index.md) or the `wiki/activations/` folder for the full set.

## Related Sources

{related_sources}

## Open Questions

{open_questions}
"""


def _render_source_page(axis_count: int, activation_count: int, triad_count: int, missing_count: int) -> str:
    factor_links = "\n".join(_factor_link(factor) for factor in FACTOR_SEQUENCE)
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {SANDBACH_FRAMEWORK_SCOPE}
factors:
{_yaml_list(FACTOR_SEQUENCE, indent=2)}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: John Sandbach
- Title: *Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This source provides unordered midpoint-axis chapters with an explicit `Principle` and `Process` for each axis.
- Each Sandbach axis chapter also supplies explicit activator meanings for every remaining factor in the source inventory.
- This ingest adds `Chiron` to the canonical factor inventory because the source treats it as a full participant in axis and activation structures.
- The source does not provide standalone factor chapters.
- The visible source pages omit `{missing_count}` expected activator entries.
- Those source-omission slots are preserved as structural activation pages rather than speculative doctrine.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{axis_count}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- Canonical activation pages updated or created: `{activation_count}`.
- Of these, `{missing_count}` are source-omission structural pages because the visible source pages omit those activator entries.
- Canonical triad hubs updated or created: `{triad_count}`.
- Browse [Index](../index.md), `wiki/activations/`, and `wiki/triads/` for the full set.

## Ingestion History

- {UPDATED_AT}: Ingested the Sandbach midpoint compendium, including axis-level `Principle` and `Process` statements plus all extractable explicit activator meanings, and expanded the canonical factor inventory to include `Chiron`.
"""


def _append_log_entry(log_path: Path) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        "- 2026-04-21: Ingested John Sandbach's midpoint compendium into 91 canonical axis pages, "
        "1092 activation pages, and 364 triad hubs, added Chiron as a canonical factor, "
        "and preserved Sandbach's axis principles, processes, and extractable activator meanings while materializing 8 extractor gaps as structural placeholder activation pages."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    wiki_root = root / "wiki"
    axis_dir = wiki_root / "axes"
    activation_dir = wiki_root / "activations"
    triad_dir = wiki_root / "triads"
    factor_dir = wiki_root / "factors"
    source_dir = wiki_root / "sources"

    blocks = generate_models(root / "Stellar Influences Vault" / SOURCE_FILE)
    triads_touched: set[tuple[str, str, str]] = set()
    extracted_activation_count = 0
    missing_activation_count = 0
    for block in blocks:
        axis_identity = normalize_axis(block.factor_a, block.factor_b)
        axis_path = axis_dir / f"{axis_identity.slug}.md"
        axis_path.write_text(_render_axis_page(axis_path, block), encoding="utf-8")

        entries_by_factor = {entry.activated_by: entry for entry in block.activation_entries}
        expected_activators = [factor for factor in FACTOR_SEQUENCE if factor not in {block.factor_a, block.factor_b}]
        for activated_by in expected_activators:
            entry = entries_by_factor.get(activated_by)
            activation_identity = normalize_activation(block.factor_a, block.factor_b, activated_by)
            activation_path = activation_dir / f"{activation_identity.slug}.md"
            activation_path.write_text(
                _render_activation_page(activation_path, block, entry, activated_by=activated_by),
                encoding="utf-8",
            )
            triads_touched.add(activation_identity.triad_set)
            if entry is None:
                missing_activation_count += 1
            else:
                extracted_activation_count += 1

    for triad in sorted(triads_touched, key=lambda item: tuple(name.casefold() for name in item)):
        triad_identity = normalize_triad(triad)
        triad_path = triad_dir / f"{triad_identity.slug}.md"
        triad_path.write_text(_render_triad_page(triad_path, triad, activation_dir), encoding="utf-8")

    axis_pages = [load_page(path) for path in axis_dir.glob("*.md")]
    activation_pages = [load_page(path) for path in activation_dir.glob("*.md")]
    related_axes_by_factor: dict[str, list[str]] = defaultdict(list)
    activation_count_by_factor: dict[str, int] = defaultdict(int)
    for page in axis_pages:
        for factor in list(page.meta.get("factors", []) or []):
            related_axes_by_factor[factor].append(page.meta["title"])
    for factor, titles in related_axes_by_factor.items():
        related_axes_by_factor[factor] = sorted(set(titles), key=str.casefold)
    for page in activation_pages:
        for factor in list(page.meta.get("factors", []) or []):
            activation_count_by_factor[factor] += 1

    chiron_path = factor_dir / "chiron.md"
    chiron_path.write_text(
        _render_chiron_factor_page(
            related_axes_by_factor["Chiron"],
            activation_count_by_factor["Chiron"],
        ),
        encoding="utf-8",
    )
    for factor in [name for name in CANONICAL_FACTORS if name != "Chiron"]:
        factor_path = factor_dir / f"{normalize_factor(factor).slug}.md"
        if factor_path.exists():
            factor_path.write_text(
                _render_existing_factor_page(
                    factor_path,
                    related_axes_by_factor[factor],
                    activation_count_by_factor[factor],
                ),
                encoding="utf-8",
            )

    source_path = source_dir / f"{SOURCE_SLUG}.md"
    source_path.write_text(
        _render_source_page(
            len(blocks),
            extracted_activation_count + missing_activation_count,
            len(triads_touched),
            missing_activation_count,
        ),
        encoding="utf-8",
    )

    _append_log_entry(wiki_root / "log.md")
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
