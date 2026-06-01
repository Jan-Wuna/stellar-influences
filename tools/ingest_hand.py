from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.hand_source import (
    FRAMEWORK_SCOPE as HAND_FRAMEWORK_SCOPE,
    SOURCE_FILE,
    SOURCE_SLUG,
    SOURCE_TITLE,
    HandAxisBlock,
    HandFactorBlock,
    generate_factor_models,
    generate_models,
)
from tools.rebuild_index import build_index
from tools.wiki_identity import astronomicon_token, factor_slug, normalize_axis
from tools.wiki_pages import WikiPage, load_frontmatter, load_page


UPDATED_AT = "2026-04-22"
DEFAULT_DERIVED_TEXT = ""
DEFAULT_FACTOR_CONTRADICTIONS = (
    "- Source differences on this factor page are preserved as framework emphasis rather than forced contradiction.\n"
    "- This page keeps the contributing source chapters side by side instead of treating one as a gloss on the other."
)

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
MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"

SOURCE_ORDER = [
    WITTE_SLUG,
    EBERTIN_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SANDBACH_SLUG,
    SOURCE_SLUG,
    MCBROOM_SLUG,
]

SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    EBERTIN_SLUG: EBERTIN_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SANDBACH_SLUG: SANDBACH_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
    MCBROOM_SLUG: MCBROOM_TITLE,
}

SOURCE_SLUGS_BY_TITLE = {title: slug for slug, title in SOURCE_TITLES.items()}
VERNAL_POINT_TERM_RE = re.compile(r"\b(?:Aries|Aides)\s+[Pp]oint\b")


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _legacy_factor_slug(name: str) -> str:
    slug = factor_slug(name)
    return "aries" if slug == "vernal-point" else slug


def _legacy_axis_slug(axis_slug: str) -> str:
    return axis_slug.replace("vernal-point", "aries")


def _factor_template_path(factor_dir: Path, factor: str) -> Path:
    canonical = factor_dir / f"{factor_slug(factor)}.md"
    if canonical.exists():
        return canonical
    legacy = factor_dir / f"{_legacy_factor_slug(factor)}.md"
    if legacy.exists():
        return legacy
    raise FileNotFoundError(f"missing canonical or legacy factor template for {factor}")


def _axis_template_path(axis_dir: Path, factor_a: str, factor_b: str) -> Path:
    axis = normalize_axis(factor_a, factor_b)
    canonical = axis_dir / f"{axis.slug}.md"
    if canonical.exists():
        return canonical
    legacy = axis_dir / f"{_legacy_axis_slug(axis.slug)}.md"
    if legacy.exists():
        return legacy
    raise FileNotFoundError(f"missing canonical or legacy axis template for {axis.display}")


def _load_head_page(path: Path) -> WikiPage | None:
    root = Path.cwd()
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        return None
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    meta, body = load_frontmatter(result.stdout)
    return WikiPage(path=path, meta=meta, body=body)


def _factor_template_page(path: Path) -> WikiPage:
    page = load_page(path)
    if SOURCE_SLUG not in list(page.meta.get("source_pages", []) or []):
        return page
    head_page = _load_head_page(path)
    return head_page or page


def _source_entries(body: str) -> list[str]:
    match = re.search(r"## Source Entries\n\n(.*?)\n\n## Comparative Schema\n", body, re.S)
    if not match:
        raise ValueError("could not parse source entries block")
    return [entry.strip() for entry in re.split(r"(?m)(?=^### )", match.group(1).strip()) if entry.strip()]


def _section_body(body: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", body, re.S)
    return match.group(1).strip() if match else ""


def _ordered_source_pages(items: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return sorted(
        unique,
        key=lambda slug: (SOURCE_ORDER.index(slug) if slug in SOURCE_ORDER else 999, slug),
    )


def _entry_title(entry: str) -> str:
    match = re.match(r"^### ([^\n]+)", entry)
    if match is None:
        raise ValueError("source entry block is missing a title heading")
    return match.group(1).strip()


def _merge_source_entries(body: str, addition: str, title: str) -> str:
    entries = _source_entries(body)
    existing_index = {_entry_title(entry): index for index, entry in enumerate(entries)}
    by_title = {_entry_title(entry): entry for entry in entries}
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


def _source_links(source_pages: list[str]) -> str:
    return "\n".join(
        f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)"
        for slug in _ordered_source_pages(source_pages)
    )


def _render_hand_entry(block: HandAxisBlock) -> str:
    return "\n".join(
        [
            f"### {SOURCE_TITLE}",
            "",
            f"- Source heading: `{block.heading}`",
            f"- Source page: `{block.page}`",
            "",
            "#### Pair Delineation",
            "",
            block.text,
        ]
    ).strip()


def _render_hand_factor_entry(block: HandFactorBlock) -> str:
    heading = block.heading
    text = block.text
    if block.factor == "Vernal Point":
        heading = "The Vernal Point"
        text = VERNAL_POINT_TERM_RE.sub("Vernal Point", text)
    return "\n".join(
        [
            f"### {SOURCE_TITLE}",
            "",
            f"- Source heading: `{heading}`",
            f"- Source page: `{block.page}`",
            "",
            "#### Hand Factor Entry",
            "",
            text,
        ]
    ).strip()


def _render_source_page(factor_blocks: list[HandFactorBlock], axis_blocks: list[HandAxisBlock]) -> str:
    factors = [block.factor for block in factor_blocks]
    factor_links = "\n".join(f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in factors)
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {HAND_FRAMEWORK_SCOPE}
factors:
{_yaml_list(factors, indent=2)}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Robert Hand
- Title: *Horoscope Symbols*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This source now contributes standalone factor material plus the Chapter 9 pair-delineation chapter.
- Factor coverage is limited to the ten planet chapters plus Hand's reusable treatments of the lunar nodes, Ascendant, Midheaven, and the `Vernal Point` (`00 Aries`).
- The shared `The Ascendant and Midheaven` section is attached to both factor pages because the source treats them jointly in one section.
- The pair chapter covers `91` unordered pair descriptions built from the same fourteen-factor inventory.
- Neither the factor material nor Chapter 9 states oriented `A/B = C` activation formulas, so no activation or triad pages are changed by this ingest.
- The chapters on aspects, signs, houses, and midpoint technique are broader reference material that do not map cleanly to the current wiki page model.
- The rest of `Other Points in the Chart` still mixes reusable `Node`, `Asc`, `MC`, and `Vernal Point` factor material with asteroids, Chiron, fixed stars, hypothetical planets, and picture-point methodology that would require separate scope decisions.

## Factors Covered

- Canonical factor pages updated or created: `{len(factor_blocks)}`.
- Browse [Index](../index.md) or `wiki/factors/` for the full set.

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{len(axis_blocks)}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- None. Hand factor chapters and chapter 9 remain out of oriented `A/B = C` activation pages.

## Ingestion History

- {UPDATED_AT}: Ingested Robert Hand's factor chapters into canonical factor pages and extended the source page coverage beyond the earlier axis-only chapter 9 ingest.
"""


def _render_axis_page(existing_path: Path, block: HandAxisBlock) -> str:
    page = load_page(existing_path)
    meta = page.meta
    axis = normalize_axis(block.factor_a, block.factor_b)
    astronomicon_axis = f"{astronomicon_token(axis.factors[0])}/{astronomicon_token(axis.factors[1])}"
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != axis.display
        else ""
    )
    entries_text = _merge_source_entries(page.body, _render_hand_entry(block), SOURCE_TITLE)
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    related_activations = list(meta.get("related_activations", []) or [])
    related_triad_hubs = list(meta.get("related_triad_hubs", []) or [])
    aliases = list(meta.get("aliases", []) or [])
    derived_text = _section_body(page.body, "## Derived Synthesis") or DEFAULT_DERIVED_TEXT

    related_links = "\n".join(
        f"- [{name}](../activations/{name.lower().replace('/', '-').replace(' = ', '-equals-').replace(' ', '-')}.md)"
        for name in related_activations
    )
    source_links_text = _source_links(source_pages)
    return f"""---
title: {axis.display}
page_type: axis
slug: {axis.slug}
status: source_ingested
framework_scope: comparative
factors:
{_yaml_list(list(axis.factors), indent=2)}
normalized_axis: {axis.display}
factor_a: {axis.factors[0]}
factor_b: {axis.factors[1]}
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

- core meaning: source-native pair entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened.
- body/health: source-native biological or bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: see the source entries above and the orientation-specific activation pages linked below.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Related Activations

{related_links}

## Contradictions

- No direct contradiction is recorded yet among the ingested source entries on this axis.
- Differences are preserved as distinct source voices and framework emphases rather than flattened into one interpretation.

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived_text}

## Links

- [{axis.factors[0]}](../factors/{factor_slug(axis.factors[0])}.md)
- [{axis.factors[1]}](../factors/{factor_slug(axis.factors[1])}.md)
{source_links_text}
"""


def _render_factor_page(existing_path: Path, block: HandFactorBlock) -> str:
    page = _factor_template_page(existing_path)
    meta = page.meta
    factor = block.factor
    astronomicon = astronomicon_token(factor)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor
        else ""
    )
    source_pages = _ordered_source_pages(list(meta.get("source_pages", []) or []) + [SOURCE_SLUG])
    source_entries = _merge_source_entries(page.body, _render_hand_factor_entry(block), SOURCE_TITLE)
    contradictions = _section_body(page.body, "## Contradictions and Framework Notes") or DEFAULT_FACTOR_CONTRADICTIONS
    derived_text = _section_body(page.body, "## Derived Synthesis") or DEFAULT_DERIVED_TEXT
    related_axes = _section_body(page.body, "## Related Axes") or "- None generated."
    related_activations = _section_body(page.body, "## Related Activations") or "- None."
    open_questions = _section_body(page.body, "## Open Questions") or "- None recorded yet."
    aliases = list(meta.get("aliases", []) or [])
    source_links_text = _source_links(source_pages)
    return f"""---
title: {factor}
page_type: factor
slug: {factor_slug(factor)}
status: source_ingested
framework_scope: comparative
factors:
{_yaml_list([factor], indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Factor: {factor}
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

{derived_text}

## Related Axes

{related_axes}

## Related Activations

{related_activations}

## Related Sources

{source_links_text}

## Open Questions

{open_questions}
"""


def _append_log_entry(log_path: Path) -> None:
    text = log_path.read_text(encoding="utf-8").rstrip()
    axis_entry = (
        "- 2026-04-22: Ingested Robert Hand's chapter 9 pair delineations into 91 canonical axis pages, "
        "added the Hand source page, and noted the book's future factor-ingest candidates versus out-of-model chapters."
    )
    factor_entry = (
        "- 2026-04-22: Merged Robert Hand's factor chapters into 14 canonical factor pages, including the shared "
        "Ascendant/Midheaven section on both factor pages, while leaving the out-of-model chapters un-ingested."
    )
    if axis_entry not in text:
        text = f"{text}\n{axis_entry}"
    if factor_entry not in text:
        text = f"{text}\n{factor_entry}"
    log_path.write_text(f"{text}\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / SOURCE_FILE
    wiki_root = root / "wiki"
    factor_dir = wiki_root / "factors"
    axis_dir = wiki_root / "axes"
    source_dir = wiki_root / "sources"

    axis_blocks = generate_models(pdf_path)
    factor_blocks = generate_factor_models(pdf_path)

    for block in axis_blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        axis_path = axis_dir / f"{axis.slug}.md"
        template_path = _axis_template_path(axis_dir, block.factor_a, block.factor_b)
        axis_path.write_text(_render_axis_page(template_path, block), encoding="utf-8")

    for block in factor_blocks:
        factor_path = factor_dir / f"{factor_slug(block.factor)}.md"
        template_path = _factor_template_path(factor_dir, block.factor)
        factor_path.write_text(_render_factor_page(template_path, block), encoding="utf-8")

    source_path = source_dir / f"{SOURCE_SLUG}.md"
    source_path.write_text(_render_source_page(factor_blocks, axis_blocks), encoding="utf-8")

    _append_log_entry(wiki_root / "log.md")
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()
