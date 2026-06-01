from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token, factor_slug, normalize_activation, normalize_axis, triad_slug
from tools.witte_source import ActivationEntry, FACTOR_SEQUENCE, FactorBlock, PairBlock, generate_models


UPDATED_AT = "2026-04-21"
SOURCE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
SOURCE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
SOURCE_FILE = "planetary expressions - Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures 2020.pdf"
FRAMEWORK_SCOPE = "hamburg_school"

FACTOR_INDEX = {name: index for index, name in enumerate(FACTOR_SEQUENCE)}
FACTOR_ALIASES = {
    "Vernal Point": ["VP"],
    "MC": ["Meridian"],
    "Asc": ["Ascendant"],
    "Node": ["Lunar Nodes"],
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _clear_markdown_files(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for file_path in path.glob("*.md"):
        file_path.unlink()


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _factor_sort_key(name: str) -> tuple[int, str]:
    return (FACTOR_INDEX.get(name, 10_000), name.casefold())


def _entry_sort_key(entry: ActivationEntry) -> tuple[int, str]:
    return _factor_sort_key(entry.activated_by)


def _canonical_factor_blocks(factor_blocks: list[FactorBlock] | tuple[FactorBlock, ...]) -> list[FactorBlock]:
    best_blocks: dict[str, FactorBlock] = {}
    for block in factor_blocks:
        current = best_blocks.get(block.factor)
        if current is None:
            best_blocks[block.factor] = block
            continue
        if (block.page, len(block.text.strip())) >= (current.page, len(current.text.strip())):
            best_blocks[block.factor] = block
    return [
        best_blocks.get(factor, FactorBlock(factor=factor, page=0, text=""))
        for factor in FACTOR_SEQUENCE
    ]


def _text_quality(text: str) -> tuple[int, int]:
    letters = sum(character.isalpha() for character in text)
    weird = sum(
        not (character.isalnum() or character.isspace() or character in ".,;:'\"!?()-")
        for character in text
    )
    junk_tokens = len(re.findall(r"\b(?:g|x|www)\b", text.lower()))
    truncated = int(bool(text.strip()) and text.strip()[-1] not in ".!?")
    score = letters - (weird * 20) - (junk_tokens * 20) - (truncated * 10)
    return score, len(text.strip())


def _better_text(left: str, right: str) -> str:
    return right if _text_quality(right) >= _text_quality(left) else left


def _better_entry(left: ActivationEntry, right: ActivationEntry) -> ActivationEntry:
    return right if _text_quality(right.text) >= _text_quality(left.text) else left


def _coalesce_pair_blocks(pair_blocks: list[PairBlock]) -> list[PairBlock]:
    grouped: dict[str, list[PairBlock]] = {}
    order: list[str] = []
    for block in pair_blocks:
        slug = normalize_axis(block.factor_a, block.factor_b).slug
        if slug not in grouped:
            grouped[slug] = []
            order.append(slug)
        grouped[slug].append(block)

    merged_blocks: list[PairBlock] = []
    for slug in order:
        blocks = grouped[slug]
        if len(blocks) == 1:
            block = blocks[0]
            merged_blocks.append(
                PairBlock(
                    factor_a=block.factor_a,
                    factor_b=block.factor_b,
                    source_heading=block.source_heading,
                    page=block.page,
                    summary=block.summary,
                    activation_entries=sorted(block.activation_entries, key=_entry_sort_key),
                )
            )
            continue

        best_block = max(blocks, key=lambda block: (_text_quality(block.summary), block.page))
        best_summary = best_block.summary
        entry_map: dict[str, ActivationEntry] = {}
        for block in blocks:
            best_summary = _better_text(best_summary, block.summary)
            for entry in block.activation_entries:
                current = entry_map.get(entry.activated_by)
                entry_map[entry.activated_by] = entry if current is None else _better_entry(current, entry)

        merged_blocks.append(
            PairBlock(
                factor_a=best_block.factor_a,
                factor_b=best_block.factor_b,
                source_heading=best_block.source_heading,
                page=best_block.page,
                summary=best_summary,
                activation_entries=sorted(entry_map.values(), key=_entry_sort_key),
            )
        )
    return merged_blocks


def _group_triads(pair_blocks: list[PairBlock]) -> dict[tuple[str, str, str], list[tuple[PairBlock, ActivationEntry]]]:
    triads: dict[tuple[str, str, str], list[tuple[PairBlock, ActivationEntry]]] = defaultdict(list)
    for block in pair_blocks:
        for entry in block.activation_entries:
            identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            if not identity.has_distinct_triad:
                continue
            triads[identity.triad_set].append((block, entry))
    return dict(triads)


def _astronomicon_axis(factor_a: str, factor_b: str) -> str:
    return f"{astronomicon_token(factor_a)}/{astronomicon_token(factor_b)}"


def _astronomicon_activation(factor_a: str, factor_b: str, activated_by: str) -> str:
    return f"{_astronomicon_axis(factor_a, factor_b)} = {astronomicon_token(activated_by)}"


def _astronomicon_triad(factors: tuple[str, str, str]) -> str:
    return " ".join(astronomicon_token(factor) for factor in factors)


def _activation_page_text(pair: PairBlock, entry: ActivationEntry, updated_at: str) -> str:
    identity = normalize_activation(pair.factor_a, pair.factor_b, entry.activated_by)
    astronomicon_formula = _astronomicon_activation(
        identity.axis.factors[0],
        identity.axis.factors[1],
        identity.activated_by,
    )
    astronomicon_line = (
        f"- Astronomicon formula: `{astronomicon_formula}`\n"
        if astronomicon_formula != identity.display
        else ""
    )
    factors_yaml = "\n".join(f"  - {name}" for name in [pair.factor_a, pair.factor_b, entry.activated_by])
    triad_yaml = "\n".join(f"  - {name}" for name in identity.triad_set)
    triad_link = ""
    if identity.has_distinct_triad:
        triad_link = f"- Triad hub: [{' '.join(identity.triad_set)}](../triads/{triad_slug(identity.triad_set)}.md)\n"
    else:
        triad_link = "- Repeated-pair identity: no distinct triad hub exists for this activation.\n"
    return f"""---
title: {identity.display}
page_type: activation
slug: {identity.slug}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
{factors_yaml}
normalized_formula: {identity.display}
axis: {identity.axis.display}
activated_by: {entry.activated_by}
triad_set:
{triad_yaml}
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {updated_at}
---

## Identity

- Formula: `{identity.display}`
{astronomicon_line}- Axis page: [{identity.axis.display}](../axes/{identity.axis.slug}.md)
{triad_link}
## Source Entries

### {SOURCE_TITLE}

- Source heading: `{pair.source_heading}`
- Source page: `{entry.page}`
#### Witte Entry

{entry.text}

## Comparative Schema

- core meaning: {entry.text}
- psychology: source-backed meaning retained in the entry above.
- body/health: no separate body-specific bucket is isolated automatically at ingest time.
- social/relationship: source-backed meaning retained in the entry above.
- events/manifestations: source-backed meaning retained in the entry above.
- conflicts/notes: orientation-specific meaning is preserved on its own page; source `+` headings are normalized as midpoint-axis identities here.

## Contradictions

- None recorded yet for this source-only page.

<a id="derived-synthesis"></a>

## Derived Synthesis


## Links

- [{identity.axis.factors[0]}](../factors/{factor_slug(identity.axis.factors[0])}.md)
- [{identity.axis.factors[1]}](../factors/{factor_slug(identity.axis.factors[1])}.md)
- [{entry.activated_by}](../factors/{factor_slug(entry.activated_by)}.md)
- [{identity.axis.display}](../axes/{identity.axis.slug}.md)
"""


def _axis_page_text(pair: PairBlock, updated_at: str) -> str:
    identity = normalize_axis(pair.factor_a, pair.factor_b)
    astronomicon_axis = _astronomicon_axis(identity.factors[0], identity.factors[1])
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != identity.display
        else ""
    )
    factors_yaml = "\n".join(f"  - {name}" for name in identity.factors)
    related_activations = [
        normalize_activation(pair.factor_a, pair.factor_b, entry.activated_by)
        for entry in pair.activation_entries
    ]
    related_activation_yaml = _yaml_list([item.display for item in related_activations], indent=2)
    triad_names = sorted(
        {" ".join(item.triad_set) for item in related_activations if item.has_distinct_triad},
        key=str.casefold,
    )
    triad_yaml = _yaml_list(triad_names, indent=2)
    related_links = "\n".join(
        f"- [{item.display}](../activations/{item.slug}.md)" for item in related_activations
    )
    return f"""---
title: {identity.display}
page_type: axis
slug: {identity.slug}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
{factors_yaml}
normalized_axis: {identity.display}
factor_a: {identity.factors[0]}
factor_b: {identity.factors[1]}
related_activations:
{related_activation_yaml}
related_triad_hubs:
{triad_yaml}
aliases:
  - {identity.factors[1]}/{identity.factors[0]}
source_pages:
  - {SOURCE_SLUG}
updated_at: {updated_at}
---

## Identity

- Axis: `{identity.display}`
{astronomicon_line}- Source heading: `{pair.source_heading}`
- Source page: `{pair.page}`

## Source Entries

### {SOURCE_TITLE}

#### Pair Summary

{pair.summary}

## Comparative Schema

- core meaning: {pair.summary}
- psychology: no separate source-native subdivision is present on the pair-summary page.
- body/health: no separate source-native subdivision is present on the pair-summary page.
- social/relationship: no separate source-native subdivision is present on the pair-summary page.
- events/manifestations: see the orientation-specific activation entries linked below.
- conflicts/notes: source `+` headings are normalized as midpoint-axis identities; orientation-specific meanings remain on distinct activation pages.

## Related Activations

{related_links}

## Contradictions

- None recorded yet for this source-only page.

<a id="derived-synthesis"></a>

## Derived Synthesis


## Links

- [{identity.factors[0]}](../factors/{factor_slug(identity.factors[0])}.md)
- [{identity.factors[1]}](../factors/{factor_slug(identity.factors[1])}.md)
- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
"""


def _factor_page_text(
    factor: FactorBlock,
    pair_blocks: list[PairBlock],
    activation_count: int,
    updated_at: str,
) -> str:
    related_axes = sorted(
        {
            normalize_axis(block.factor_a, block.factor_b)
            for block in pair_blocks
            if factor.factor in {block.factor_a, block.factor_b}
        },
        key=lambda identity: (_factor_sort_key(identity.factors[0]), _factor_sort_key(identity.factors[1])),
    )
    related_axis_links = "\n".join(
        f"- [{axis.display}](../axes/{axis.slug}.md)" for axis in related_axes
    ) or "- None generated."
    aliases = FACTOR_ALIASES.get(factor.factor, [])
    astronomicon = astronomicon_token(factor.factor)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor.factor
        else ""
    )
    aliases_frontmatter = (
        "aliases:\n" + _yaml_list(aliases, indent=2)
        if aliases
        else "aliases: []"
    )
    source_page_line = (
        f"- Source factor chapter page: `{factor.page}`\n"
        if factor.page
        else "- Source factor chapter page: not resolved from the parser.\n"
    )
    factor_entry = factor.text or "None extracted."
    return f"""---
title: {factor.factor}
page_type: factor
slug: {factor_slug(factor.factor)}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
  - {factor.factor}
{aliases_frontmatter}
source_pages:
  - {SOURCE_SLUG}
updated_at: {updated_at}
---

## Identity

- Factor: {factor.factor}
{astronomicon_line}{source_page_line}

## Source Entries

### {SOURCE_TITLE}

#### Witte Factor Entry

{factor_entry}

## Comparative Schema

- core meaning: {factor_entry}
- psychology: no separate source-native subdivision is present in the standalone factor chapter.
- body/health: no separate source-native subdivision is present in the standalone factor chapter.
- social/relationship: no separate source-native subdivision is present in the standalone factor chapter.
- events/manifestations: browse related axis and activation pages for explicit formulas involving `{factor.factor}`.
- conflicts/notes: this page preserves the standalone factor chapter as sourced doctrine from Witte.

## Related Axes

{related_axis_links}

## Related Activations

- Generated activation pages involving `{factor.factor}`: `{activation_count}`.
- Browse [Index](../index.md) or the `wiki/activations/` folder for the full set.

## Related Sources

- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
"""


def _triad_page_text(orientation_entries: list[tuple[PairBlock, ActivationEntry]], updated_at: str) -> str:
    first_pair, first_entry = orientation_entries[0]
    first_identity = normalize_activation(first_pair.factor_a, first_pair.factor_b, first_entry.activated_by)
    title = " ".join(first_identity.triad_set)
    slug = triad_slug(first_identity.triad_set)
    astronomicon_triad = _astronomicon_triad(first_identity.triad_set)
    astronomicon_line = (
        f"- Astronomicon triad-set: `{astronomicon_triad}`\n"
        if astronomicon_triad != title
        else ""
    )
    ordered_entries = sorted(
        orientation_entries,
        key=lambda item: normalize_activation(item[0].factor_a, item[0].factor_b, item[1].activated_by).display,
    )
    orientation_lines = []
    coverage_lines = []
    for pair, entry in ordered_entries:
        identity = normalize_activation(pair.factor_a, pair.factor_b, entry.activated_by)
        orientation_lines.append(
            f"- [{identity.display}](../activations/{identity.slug}.md)\n"
            f"  Source page `{entry.page}`"
        )
        coverage_lines.append(f"- `{identity.display}`: page `{entry.page}`")
    orientations_yaml = _yaml_list(
        [
            normalize_activation(pair.factor_a, pair.factor_b, entry.activated_by).display
            for pair, entry in ordered_entries
        ],
        indent=2,
    )
    factors_yaml = _yaml_list(list(first_identity.triad_set), indent=2)
    links = "\n".join(
        f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in first_identity.triad_set
    )
    return f"""---
title: {title}
page_type: triad_hub
slug: {slug}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
{factors_yaml}
triad_set:
{factors_yaml}
orientations:
{orientations_yaml}
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {updated_at}
---

## Identity

- Triad-set: `{title}`
{astronomicon_line}- This page is structural only. It does not merge the meanings of its orientations.

## Orientation Map

{chr(10).join(orientation_lines)}

## Source Coverage

- Source: [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
{chr(10).join(coverage_lines)}

## Contradictions Across Orientations

- None recorded yet.
- Distinct meanings across orientations are preserved as orientation differences, not collapsed into one interpretation.

## Links

{links}
"""


def render_source_page(
    factors: list[FactorBlock],
    raw_pair_blocks: list[PairBlock],
    pair_blocks: list[PairBlock],
    triad_count: int,
    activation_count: int,
    updated_at: str,
) -> str:
    factor_links = "\n".join(f"- [{factor.factor}](../factors/{factor_slug(factor.factor)}.md)" for factor in factors)
    duplicate_count = len(raw_pair_blocks) - len(pair_blocks)
    return f"""---
title: {SOURCE_TITLE}
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {FRAMEWORK_SCOPE}
factors:
{_yaml_list([factor.factor for factor in factors], indent=2)}
aliases: []
source_pages: []
updated_at: {updated_at}
---

## Bibliographic Metadata

- Authors: Alfred Witte, Ludwig Rudolph, Hermann Lefeldt
- Title: *Rules for Planetary Pictures*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This ingest includes standalone factor chapters, explicit pair-summary pages, and explicit activation meanings from the source.
- Source `A + B` headings are normalized into unordered midpoint-axis pages `A/B`.
- Repeated-pair activations such as `A/A = B` remain valid activation pages but do not generate triad hubs.
- Duplicate source pair blocks coalesced during ingest: `{duplicate_count}`.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages generated: `{len(pair_blocks)}`.
- Raw parsed pair blocks before coalescing duplicates: `{len(raw_pair_blocks)}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- Canonical activation pages generated: `{activation_count}`.
- Triad hubs generated: `{triad_count}`.
- Browse [Index](../index.md), `wiki/activations/`, and `wiki/triads/` for the full set.

## Ingestion History

- {updated_at}: Full Witte ingest generated from the source PDF, including standalone factor chapters, pair summaries, and activation meanings.
"""


def main() -> None:
    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    wiki_root = root / "wiki"

    parsed_factor_blocks, raw_pair_blocks = generate_models(pdf_path)
    factor_blocks = _canonical_factor_blocks(parsed_factor_blocks)
    pair_blocks = _coalesce_pair_blocks(list(raw_pair_blocks))

    factor_dir = wiki_root / "factors"
    axis_dir = wiki_root / "axes"
    activation_dir = wiki_root / "activations"
    triad_dir = wiki_root / "triads"
    source_dir = wiki_root / "sources"

    for directory in [factor_dir, axis_dir, activation_dir, triad_dir, source_dir]:
        _clear_markdown_files(directory)

    activation_index: dict[str, int] = defaultdict(int)
    triads = _group_triads(pair_blocks)
    for pair in pair_blocks:
        for entry in pair.activation_entries:
            identity = normalize_activation(pair.factor_a, pair.factor_b, entry.activated_by)
            for factor in {pair.factor_a, pair.factor_b, entry.activated_by}:
                activation_index[factor] += 1
            _write(activation_dir / f"{identity.slug}.md", _activation_page_text(pair, entry, UPDATED_AT))

    for pair in pair_blocks:
        identity = normalize_axis(pair.factor_a, pair.factor_b)
        _write(axis_dir / f"{identity.slug}.md", _axis_page_text(pair, UPDATED_AT))

    for factor in factor_blocks:
        _write(
            factor_dir / f"{factor_slug(factor.factor)}.md",
            _factor_page_text(factor, pair_blocks, activation_index[factor.factor], UPDATED_AT),
        )

    for triad_set, orientation_entries in triads.items():
        _write(triad_dir / f"{triad_slug(triad_set)}.md", _triad_page_text(orientation_entries, UPDATED_AT))

    _write(
        source_dir / f"{SOURCE_SLUG}.md",
        render_source_page(
            factor_blocks,
            list(raw_pair_blocks),
            pair_blocks,
            triad_count=len(triads),
            activation_count=sum(len(pair.activation_entries) for pair in pair_blocks),
            updated_at=UPDATED_AT,
        ),
    )

    index_path = wiki_root / "index.md"
    index_path.write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
