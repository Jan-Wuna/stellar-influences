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
    MunkaseyActivationEntry,
    MunkaseyAxisBlock,
    MunkaseyFactorBlock,
    generate_factor_models,
    generate_models,
)
from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token
from tools.wiki_identity import factor_slug, normalize_activation, normalize_axis, normalize_factor, normalize_triad
from tools.wiki_pages import load_page


UPDATED_AT = "2026-05-06"
DEFAULT_DERIVED_TEXT = ""
_MISSING = object()
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
UDO_SLUG = "udo-rudolph-abc-fur-planetenbilder"
UDO_TITLE = "Udo Rudolph - ABC for Planetary Pictures"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
EBERTIN_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
SANDBACH_TITLE = "John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"
SOURCE_ORDER = [
    WITTE_SLUG,
    UDO_SLUG,
    EBERTIN_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SANDBACH_SLUG,
    HAND_SLUG,
    MCBROOM_SLUG,
    SOURCE_SLUG,
]
SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    UDO_SLUG: UDO_TITLE,
    EBERTIN_SLUG: EBERTIN_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SANDBACH_SLUG: SANDBACH_TITLE,
    HAND_SLUG: HAND_TITLE,
    MCBROOM_SLUG: MCBROOM_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
}
FRAMEWORK_BY_SOURCE = {
    WITTE_SLUG: "hamburg_school",
    UDO_SLUG: "hamburg_school",
    EBERTIN_SLUG: "cosmobiology",
    FALIS_SLUG: "modern_astrology",
    CARTER_SLUG: "classical_aspects",
    SANDBACH_SLUG: "modern_astrology",
    HAND_SLUG: "modern_astrology",
    MCBROOM_SLUG: "modern_astrology",
    SOURCE_SLUG: FRAMEWORK_SCOPE,
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


def _keyword_lines(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _section_body(body: str, heading: str, next_heading: str) -> str:
    if next_heading:
        pattern = rf"{re.escape(heading)}\n\n(.*?)\n\n{re.escape(next_heading)}\n"
    else:
        pattern = rf"{re.escape(heading)}\n\n(.*)\Z"
    match = re.search(pattern, body, re.S)
    if not match:
        raise ValueError(f"could not parse section {heading}")
    return match.group(1).strip()


def _section_body_between(body: str, heading: str, next_headings: list[str], default: object = _MISSING) -> str:
    for next_heading in next_headings:
        try:
            return _section_body(body, heading, next_heading)
        except ValueError:
            pass
    if default is not _MISSING:
        return str(default)
    raise ValueError(f"could not parse section {heading}")


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
    entries_text = _section_body_between(
        body,
        "## Source Entries",
        ["## Comparative Schema", "## Related Activations", '<a id="derived-synthesis"></a>', "## Derived Synthesis"],
    )
    entries = [entry.strip() for entry in re.split(r"(?m)(?=^### )", entries_text) if entry.strip()]
    if not entries:
        raise ValueError("could not parse source entries block")
    normalized: list[str] = []
    for entry in entries:
        if entry.startswith(f"### {WITTE_TITLE}\n") and "- Source heading:" not in entry:
            try:
                normalized.append(_parse_legacy_witte_entry(body, entry))
            except ValueError:
                normalized.append(entry)
            continue
        normalized.append(entry)
    return normalized


def _append_source_entry(existing: str, addition: str, title: str) -> str:
    addition = addition.strip()
    if not existing.strip():
        return addition
    pattern = rf"(?ms)^### {re.escape(title)}\n\n.*?(?=\n\n### |\Z)"
    if re.search(pattern, existing):
        return re.sub(pattern, addition, existing.strip()).strip()
    return f"{existing.rstrip()}\n\n{addition}"


def _activation_slug(display: str) -> str:
    left, right = display.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    return normalize_activation(factor_a, factor_b, right.strip()).slug


def _activation_link(display: str) -> str:
    return f"- [{display}](../activations/{_activation_slug(display)}.md)"


def _source_page_refs(body: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    entries_text = _section_body(body, "## Source Entries", "## Comparative Schema")
    for match in re.finditer(r"### (.+?)\s+(.*?)(?=\n### |\Z)", entries_text, re.S):
        title = match.group(1).strip()
        block = match.group(2)
        page_match = re.search(r"- Source page: `([^`]+)`", block)
        if page_match:
            refs.append((title, page_match.group(1)))
    return refs


def _render_keyword_section(title: str, items: tuple[str, ...]) -> str:
    return "\n".join(
        [
            f"#### {title}",
            "",
            _keyword_lines(items),
        ]
    )


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
        f"- [{factor}](../factors/{factor_slug(factor)}.md)"
        for factor in factors
    ]
    for slug in source_pages:
        lines.append(f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)")
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
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
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
framework_scope: {_framework_scope_for_sources(source_pages)}
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

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived_text or DEFAULT_DERIVED_TEXT}

## Links

{_render_links(list(meta["factors"]), source_pages)}
"""


def _render_munkasey_factor_entry(block: MunkaseyFactorBlock) -> str:
    return "\n".join(
        [
            f"### {SOURCE_TITLE}",
            "",
            f"- Source heading: `{block.source_heading}`",
            f"- Source page: `{block.page}`",
            "",
            _render_keyword_section("Basic Ideas", block.basic_ideas),
            "",
            _render_keyword_section("In Your Relationships", block.relationships),
            "",
            _render_keyword_section("With Body or Mind", block.body_mind),
            "",
            _render_keyword_section("In Politics or Business", block.politics_business),
        ]
    )


def _render_factor_page(factor_path: Path, block: MunkaseyFactorBlock) -> str:
    page = load_page(factor_path)
    meta = page.meta
    factor = normalize_factor(block.factor)
    source_entries = _append_source_entry(
        _section_body_between(
            page.body,
            "## Source Entries",
            ["## Comparative Schema", '<a id="derived-synthesis"></a>', "## Derived Synthesis"],
        ),
        _render_munkasey_factor_entry(block),
        SOURCE_TITLE,
    )
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    contradictions = _section_body_between(
        page.body,
        "## Contradictions and Framework Notes",
        ['<a id="derived-synthesis"></a>'],
        "- None recorded yet.",
    )
    derived_text = _section_body(page.body, "## Derived Synthesis", "## Related Axes")
    related_axes = _section_body_between(page.body, "## Related Axes", ["## Related Activations", "## Related Sources"])
    related_activations = _section_body_between(
        page.body,
        "## Related Activations",
        ["## Related Sources"],
        "- None recorded yet.",
    )
    related_sources = _section_body_between(page.body, "## Related Sources", ["## Open Questions", ""], "")
    munkasey_source_link = f"- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)"
    if munkasey_source_link not in related_sources:
        related_sources = f"{related_sources.rstrip()}\n{munkasey_source_link}"
    open_questions = _section_body_between(page.body, "## Open Questions", [""], "- None recorded yet.")
    astronomicon = astronomicon_token(factor.display)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor.display
        else ""
    )
    return f"""---
title: {factor.display}
page_type: factor
slug: {meta['slug']}
status: source_ingested
framework_scope: {_framework_scope_for_sources(source_pages)}
factors:
{_yaml_list([factor.display], indent=2)}
aliases:
{_yaml_list(list(meta.get('aliases', []) or []), indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Factor: {factor.display}
{astronomicon_line}- Canonical page type: comparative factor page grounded in standalone source entries.

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native factor entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened.
- body/health: bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: source-specific extensions remain attached to the source entry that states them.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Contradictions and Framework Notes

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived_text or DEFAULT_DERIVED_TEXT}

## Related Axes

{related_axes}

## Related Activations

{related_activations}

## Related Sources

{related_sources}

## Open Questions

{open_questions}
"""


def _render_munkasey_activation_entry(
    block: MunkaseyAxisBlock,
    entry: MunkaseyActivationEntry,
    source_heading: str,
    source_page: int,
) -> str:
    return "\n".join(
        [
            f"### {SOURCE_TITLE}",
            "",
            f"- Source heading: `{source_heading}`",
            f"- Source page: `{source_page}`",
            "",
            "#### Munkasey Entry",
            "",
            entry.text,
        ]
    )


def _render_activation_page(
    activation_path: Path,
    block: MunkaseyAxisBlock,
    entry: MunkaseyActivationEntry,
    source_heading: str,
    source_page: int,
) -> str:
    identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
    source_entry = _render_munkasey_activation_entry(block, entry, source_heading, source_page)
    if activation_path.exists():
        page = load_page(activation_path)
        aliases = list(page.meta.get("aliases", []) or [])
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _append_source_entry(
            _section_body_between(
                page.body,
                "## Source Entries",
                ["## Comparative Schema", '<a id="derived-synthesis"></a>', "## Derived Synthesis"],
            ),
            source_entry,
            SOURCE_TITLE,
        )
        contradictions = _section_body_between(
            page.body,
            "## Contradictions",
            ['<a id="derived-synthesis"></a>'],
            "- None recorded yet.",
        )
        derived_text = _section_body(page.body, "## Derived Synthesis", "## Links")
    else:
        aliases = []
        source_pages = [SOURCE_SLUG]
        source_entries = source_entry
        contradictions = "- None recorded yet for this source-only page."
        derived_text = DEFAULT_DERIVED_TEXT

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
    if identity.has_distinct_triad:
        triad_identity_line = (
            f"- Triad hub: [{' '.join(identity.triad_set)}]"
            f"(../triads/{normalize_triad(identity.triad_set).slug}.md)"
        )
        links_block = "\n".join(
            [
                f"- [{identity.axis.factors[0]}](../factors/{factor_slug(identity.axis.factors[0])}.md)",
                f"- [{identity.axis.factors[1]}](../factors/{factor_slug(identity.axis.factors[1])}.md)",
                f"- [{identity.activated_by}](../factors/{factor_slug(identity.activated_by)}.md)",
                f"- [{identity.axis.display}](../axes/{identity.axis.slug}.md)",
                f"- [{' '.join(identity.triad_set)}](../triads/{normalize_triad(identity.triad_set).slug}.md)",
                *[
                    f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)"
                    for slug in source_pages
                ],
            ]
        )
    else:
        triad_identity_line = "- Repeated-pair identity: no distinct triad hub exists for this activation."
        links_block = "\n".join(
            [
                f"- [{identity.axis.factors[0]}](../factors/{factor_slug(identity.axis.factors[0])}.md)",
                f"- [{identity.axis.factors[1]}](../factors/{factor_slug(identity.axis.factors[1])}.md)",
                f"- [{identity.activated_by}](../factors/{factor_slug(identity.activated_by)}.md)",
                f"- [{identity.axis.display}](../axes/{identity.axis.slug}.md)",
                *[
                    f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)"
                    for slug in source_pages
                ],
            ]
        )

    return f"""---
title: {identity.display}
page_type: activation
slug: {identity.slug}
status: source_ingested
framework_scope: {_framework_scope_for_sources(source_pages)}
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
{triad_identity_line}

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

{derived_text or DEFAULT_DERIVED_TEXT}

## Links

{links_block}
"""


def _render_triad_page(triad_factors: tuple[str, str, str], activation_dir: Path) -> str:
    identity = normalize_triad(triad_factors)
    activation_pages = []
    orientation_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_slug(orientation)}.md"
        if activation_path.exists():
            activation_pages.append(load_page(activation_path))
            orientation_lines.append(_activation_link(orientation))
        else:
            orientation_lines.append(f"- `{orientation}` (activation page not available)")

    source_pages = _ordered_source_pages(
        [source for page in activation_pages for source in list(page.meta.get("source_pages", []) or [])]
    )
    coverage_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_slug(orientation)}.md"
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
framework_scope: {_framework_scope_for_sources(source_pages)}
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

{chr(10).join(f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in identity.factors)}
{chr(10).join(f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)" for slug in source_pages)}
"""

def write_factor_pages(blocks: list[MunkaseyFactorBlock], factor_dir: Path) -> None:
    factor_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        factor = normalize_factor(block.factor)
        path = factor_dir / f"{factor.slug}.md"
        path.write_text(_render_factor_page(path, block), encoding="utf-8")


def write_activation_pages(blocks: list[MunkaseyAxisBlock], activation_dir: Path) -> None:
    activation_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        for entry in block.activation_entries:
            identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            path = activation_dir / f"{identity.slug}.md"
            path.write_text(
                _render_activation_page(
                    path,
                    block,
                    entry,
                    f"{block.source_heading} with Planets and Points",
                    block.activations_page,
                ),
                encoding="utf-8",
            )
        for entry in block.with_itself_entries:
            identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            path = activation_dir / f"{identity.slug}.md"
            path.write_text(
                _render_activation_page(
                    path,
                    block,
                    entry,
                    f"{block.source_heading} With Itself",
                    block.with_itself_page,
                ),
                encoding="utf-8",
            )


def write_triad_pages(blocks: list[MunkaseyAxisBlock], triad_dir: Path, activation_dir: Path) -> None:
    triad_dir.mkdir(parents=True, exist_ok=True)
    triad_sets: set[tuple[str, str, str]] = set()
    for block in blocks:
        for entry in block.activation_entries:
            identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            if identity.has_distinct_triad:
                triad_sets.add(tuple(identity.triad_set))
    for triad_factors in triad_sets:
        triad = normalize_triad(triad_factors)
        path = triad_dir / f"{triad.slug}.md"
        path.write_text(_render_triad_page(triad.factors, activation_dir), encoding="utf-8")


def render_source_page(blocks: list[MunkaseyAxisBlock], factor_blocks: list[MunkaseyFactorBlock]) -> str:
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
    factor_links = "\n".join(f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in factors)
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
- The source's factor keyword chapters are merged into the canonical factor pages.
- The page-2 activation entries are merged into canonical activation pages.
- The page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`.
- The page-4 `With Itself` activations are merged into canonical activation pages.
- The page-4 MWA example tables were intentionally omitted.

## Factors Covered

{factor_links}

- Canonical factor pages updated or created: `{len(factor_blocks)}`.

## Axes Covered

- Canonical axis pages updated or created: `{len(blocks)}`.
- Page-1 axis prose was merged into the canonical axis pages for every explicit midpoint pair in the source.

## Concepts Companion Pages

- Concepts companion pages generated: `{len(blocks)}`.
- Browse `wiki/derived/` or [Index](../index.md) for the full set.

## Activations Covered

- Canonical activation pages updated or created: `{sum(len(block.activation_entries) + len(block.with_itself_entries) for block in blocks)}`.
- Distinct-factor activation pages from page-2 `with Planets and Points`: `{sum(len(block.activation_entries) for block in blocks)}`.
- Repeated-pair activation pages from page-4 `With Itself`: `{sum(len(block.with_itself_entries) for block in blocks)}`.

## Triad Hubs Covered

- Canonical triad hubs updated or created: `{len({normalize_triad(normalize_activation(block.factor_a, block.factor_b, entry.activated_by).triad_set).slug for block in blocks for entry in block.activation_entries})}`.

## Ingestion History

- 2026-04-22: Ingested Munkasey's page-1 axis prose into canonical axis pages, preserved the page-3 `CONCEPTS` corpus as source-grounded companion pages, and intentionally omitted the page-4 MWA example tables.
- 2026-05-06: Expanded the Munkasey ingest to merge factor keyword chapters, page-2 activation entries, and page-4 `With Itself` activations into the canonical factor and activation layers while still omitting the page-4 MWA example tables.
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


def write_source_page(blocks: list[MunkaseyAxisBlock], factor_blocks: list[MunkaseyFactorBlock], sources_dir: Path) -> None:
    sources_dir.mkdir(parents=True, exist_ok=True)
    path = sources_dir / f"{SOURCE_SLUG}.md"
    path.write_text(render_source_page(blocks, factor_blocks), encoding="utf-8")


def write_axis_pages(blocks: list[MunkaseyAxisBlock], axis_dir: Path) -> None:
    axis_dir.mkdir(parents=True, exist_ok=True)
    for block in blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        path = axis_dir / f"{axis.slug}.md"
        path.write_text(_render_axis_page(path, block), encoding="utf-8")


def append_log_entry(
    log_path: Path,
    factor_count: int,
    axis_count: int,
    activation_count: int,
    triad_count: int,
) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    entry = (
        f"- {UPDATED_AT}: Expanded Michael Munkasey's ingest across `{factor_count}` factor pages, "
        f"`{axis_count}` axis pages, `{activation_count}` activation pages, and `{triad_count}` triad hubs; "
        f"preserved `{axis_count}` page-3 concepts companion pages; intentionally omitted the page-4 MWA example tables; "
        "and rebuilt the index."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path(".")
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    factor_blocks = generate_factor_models(pdf_path)
    blocks = generate_models(pdf_path)
    wiki_root = root / "wiki"
    write_factor_pages(factor_blocks, wiki_root / "factors")
    write_axis_pages(blocks, wiki_root / "axes")
    write_activation_pages(blocks, wiki_root / "activations")
    write_triad_pages(blocks, wiki_root / "triads", wiki_root / "activations")
    write_source_page(blocks, factor_blocks, wiki_root / "sources")
    write_concepts_pages(blocks, wiki_root / "derived")
    append_log_entry(
        wiki_root / "log.md",
        len(factor_blocks),
        len(blocks),
        sum(len(block.activation_entries) + len(block.with_itself_entries) for block in blocks),
        len({normalize_triad(normalize_activation(block.factor_a, block.factor_b, entry.activated_by).triad_set).slug for block in blocks for entry in block.activation_entries}),
    )
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
