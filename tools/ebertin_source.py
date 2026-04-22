from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import re

import fitz

from tools.wiki_identity import (
    astronomicon_token,
    factor_slug,
    normalize_activation,
    normalize_axis,
    triad_slug,
)


CANONICAL_FACTORS = [
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

SOURCE_FACTOR_NAMES = {
    "Sun": "Sun",
    "Moon": "Moon",
    "Mercury": "Mercury",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
    "Uranus": "Uranus",
    "Neptune": "Neptune",
    "Pluto": "Pluto",
    "Node": "Dragon's Head",
    "Asc": "Ascendant",
    "MC": "Medium Coeli",
}

SOURCE_FACTOR_CHAPTER_HEADINGS = {
    "The Moon": "Moon",
    "The Sun": "Sun",
    "Mercury": "Mercury",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
    "Uranus": "Uranus",
    "Neptune": "Neptune",
    "Pluto": "Pluto",
    "The Dragon's Head": "Node",
    "The Ascendant": "Asc",
    "The Medium Coeli (MC)": "MC",
}

AXIS_SECTION_HEADINGS = {
    f"{SOURCE_FACTOR_NAMES[left]}/{SOURCE_FACTOR_NAMES[right]}"
    for left, right in combinations(CANONICAL_FACTORS, 2)
}

FACTOR_SECTION_HEADINGS = [
    "Principle",
    "Psychological Correspondence",
    "Biological Correspondence",
    "Sociological Correspondence",
    "Position in Houses and Signs",
    "Position in the Signs",
]

AXIS_SECTION_NAMES = [
    "Principle",
    "Psychological Correspondence",
    "Biological Correspondence",
    "Sociological Correspondence",
    "Probable Manifestations",
]

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

ENTRY_PATTERN = re.compile(r"(?ms)^\s*(\d{4})\s*(?:=\s*)?([^\s\n]+)?\s*\n?(.*?)(?=^\s*\d{4}\b|\Z)")
SIGN_ENTRY_PATTERN = re.compile(r"(?ms)^\s*[^\n]*?(\d{4})[^\n]*\n?(.*?)(?=^\s*[^\n]*?\d{4}\b|\Z)")

GLYPH_TOKEN_FACTORS = {
    "O": {"Sun"},
    "0": {"Sun"},
    "\u00a9": {"Sun"},
    "o": {"Sun"},
    "D": {"Moon"},
    "])": {"Moon"},
    "3)": {"Moon"},
    "1)": {"Moon"},
    "J)": {"Moon"},
    "\u00bb": {"Moon"},
    "))": {"Moon"},
    "5": {"Mercury"},
    "\u00a7": {"Mercury"},
    "9": {"Venus"},
    'O"': {"Mars"},
    '0"': {"Mars"},
    "Cf": {"Mars"},
    "cr": {"Mars"},
    "CT": {"Mars"},
    'd"': {"Mars"},
    '0*': {"Mars"},
    "U": {"Jupiter"},
    "4": {"Jupiter"},
    "1+": {"Jupiter"},
    "H": {"Jupiter"},
    "i+": {"Jupiter"},
    "It-": {"Jupiter"},
    "it-": {"Jupiter"},
    "^4": {"Jupiter"},
    "h": {"Saturn"},
    "f": {"Pluto"},
    "%": {"Pluto"},
    "\u00a5": {"Pluto"},
    "&": {"Node"},
    "A": {"Asc"},
    "M": {"MC"},
}


@dataclass(frozen=True)
class PageRecord:
    printed_page: int | None
    text: str


@dataclass(frozen=True)
class SignEntry:
    sign: str
    code: str
    text: str
    page: int | None


@dataclass(frozen=True)
class ActivationEntry:
    code: str
    activated_by: str
    text: str
    page: int | None


@dataclass(frozen=True)
class UnresolvedActivationEntry:
    code: str
    token: str
    excerpt: str
    page: int | None


@dataclass(frozen=True)
class FactorBlock:
    factor: str
    source_heading: str
    page: int | None
    sections: dict[str, str]
    sign_entries: list[SignEntry]


@dataclass(frozen=True)
class AxisBlock:
    factor_a: str
    factor_b: str
    source_heading: str
    page: int | None
    sections: dict[str, str]
    activation_entries: list[ActivationEntry]
    unresolved_activation_entries: list[UnresolvedActivationEntry]


def canonicalize_source_factor(name: str) -> str:
    clean = name.strip()
    clean = clean.removeprefix("The ").strip()
    clean = clean.replace("(MC)", "").strip()
    if clean == "Dragon's Head":
        return "Node"
    if clean == "Ascendant":
        return "Asc"
    if clean == "Medium Coeli":
        return "MC"
    return clean


def source_factor_name(factor: str) -> str:
    return SOURCE_FACTOR_NAMES[factor]


def factor_aliases(factor: str) -> list[str]:
    aliases = {
        "Node": ["Dragon's Head"],
        "Asc": ["Ascendant"],
        "MC": ["Medium Coeli"],
    }
    return aliases.get(factor, [])


def _clean_pdf_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    text = text.replace("MiKTeX requires Windows 10 (or greater): https://miktex.org/announcement/legacy-windows-deprecation", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    return text


def _printed_page(text: str) -> int | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines[-12:]):
        if re.fullmatch(r"\d{1,3}", line):
            return int(line)
    return None


def extract_page_records(pdf_path: Path) -> list[PageRecord]:
    doc = fitz.open(pdf_path)
    records = []
    for page in doc:
        text = _clean_pdf_text(page.get_text())
        records.append(PageRecord(printed_page=_printed_page(text), text=text))
    return records


def _normalize_heading_text(line: str) -> str:
    clean = " ".join(line.strip().split())
    clean = re.sub(r"(?<=\D)\d+$", "", clean).strip()
    return clean


def _looks_like_heading(line: str) -> tuple[str, str] | None:
    normalized = _normalize_heading_text(line)
    if normalized in SOURCE_FACTOR_CHAPTER_HEADINGS:
        return ("factor", normalized)
    if normalized in AXIS_SECTION_HEADINGS:
        return ("axis", normalized)
    return None


def _line_records(pages: list[PageRecord]) -> list[tuple[int | None, str]]:
    records: list[tuple[int | None, str]] = []
    for page in pages:
        if page.printed_page is None or page.printed_page < 44:
            continue
        for line in page.text.splitlines():
            records.append((page.printed_page, line.rstrip()))
    return records


def page_lookup(pages: list[PageRecord]) -> dict[str, int | None]:
    lookup: dict[str, int | None] = {}
    for page in pages:
        for match in re.finditer(r"(?m)^\s*[^\n]*?(\d{4})\b", page.text):
            lookup.setdefault(match.group(1), page.printed_page)
    return lookup


def _collect_blocks(pages: list[PageRecord]) -> list[dict]:
    blocks: list[dict] = []
    current: dict | None = None
    for page, line in _line_records(pages):
        heading = _looks_like_heading(line)
        if heading:
            kind, normalized = heading
            if current is not None and current["heading"] == normalized:
                continue
            if current is not None:
                blocks.append(current)
            current = {"kind": kind, "heading": normalized, "page": page, "lines": []}
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        blocks.append(current)
    return blocks


def _normalize_block_text(lines: list[str], block_heading: str) -> str:
    filtered: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            filtered.append("")
            continue
        if _normalize_heading_text(stripped) == block_heading:
            continue
        if re.fullmatch(r"\d{1,3}", stripped):
            continue
        filtered.append(stripped)
    return "\n".join(filtered).strip()


def _join_paragraphs(lines: list[str]) -> str:
    paragraphs: list[str] = []
    buffer: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
            continue
        if buffer and buffer[-1].endswith("-") and stripped[:1].islower():
            buffer[-1] = buffer[-1][:-1] + stripped
            continue
        buffer.append(stripped)
    if buffer:
        paragraphs.append(" ".join(buffer))
    return "\n\n".join(paragraphs).strip()


def _excerpt(text: str, limit: int = 160) -> str:
    clean = text.strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def _clean_glyph_token(token: str | None) -> str:
    if token is None:
        return ""
    clean = token.strip().lstrip("=")
    clean = clean.rstrip(".,;:")
    clean = re.sub(r"(?<=\D)\d+$", "", clean)
    return clean


def _decode_glyph_token(token: str | None) -> set[str]:
    clean = _clean_glyph_token(token)
    if not clean:
        return set()
    return set(GLYPH_TOKEN_FACTORS.get(clean, set()))


def _split_sections(text: str, headings: list[str]) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    heading_set = set(headings)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in heading_set:
            if current is not None:
                sections[current] = _join_paragraphs(buffer)
            current = stripped
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = _join_paragraphs(buffer)
    return sections


def _split_section_lines(text: str, headings: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    buffer: list[str] = []
    heading_set = set(headings)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in heading_set:
            if current is not None:
                sections[current] = buffer[:]
            current = stripped
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = buffer[:]
    return sections


def parse_sign_entries(position_text: str, code_pages: dict[str, int | None]) -> list[SignEntry]:
    entries: list[SignEntry] = []
    for sign, match in zip(SIGNS, SIGN_ENTRY_PATTERN.finditer(position_text)):
        code = match.group(1)
        text = _join_paragraphs(match.group(2).splitlines())
        entries.append(SignEntry(sign=sign, code=code, text=text, page=code_pages.get(code)))
    return entries


def parse_activation_entries(
    factor_a: str,
    factor_b: str,
    entry_text: str,
    code_pages: dict[str, int | None],
    return_unresolved: bool = False,
) -> list[ActivationEntry] | tuple[list[ActivationEntry], list[UnresolvedActivationEntry]]:
    remaining = [factor for factor in CANONICAL_FACTORS if factor not in {factor_a, factor_b}]
    matches = list(ENTRY_PATTERN.finditer(entry_text))
    entries: list[ActivationEntry] = []
    unresolved: list[UnresolvedActivationEntry] = []
    if len(matches) >= len(remaining):
        for activated_by, match in zip(remaining, matches):
            code = match.group(1)
            text = _join_paragraphs(match.group(3).splitlines())
            entries.append(
                ActivationEntry(
                    code=code,
                    activated_by=activated_by,
                    text=text,
                    page=code_pages.get(code),
                )
            )
        if return_unresolved:
            return entries, unresolved
        return entries

    next_index = 0
    for match in matches:
        code = match.group(1)
        token = _clean_glyph_token(match.group(2))
        text = _join_paragraphs(match.group(3).splitlines())
        candidates = _decode_glyph_token(token)
        activated_by: str | None = None
        if candidates:
            for index in range(next_index, len(remaining)):
                if remaining[index] in candidates:
                    activated_by = remaining[index]
                    next_index = index + 1
                    break
        if activated_by is None:
            unresolved.append(
                UnresolvedActivationEntry(
                    code=code,
                    token=token,
                    excerpt=_excerpt(text),
                    page=code_pages.get(code),
                )
            )
            continue
        entries.append(
            ActivationEntry(
                code=code,
                activated_by=activated_by,
                text=text,
                page=code_pages.get(code),
            )
        )
        if next_index >= len(remaining):
            break
    if return_unresolved:
        return entries, unresolved
    return entries


def parse_factor_blocks(pages: list[PageRecord]) -> list[FactorBlock]:
    code_pages = page_lookup(pages)
    factors: list[FactorBlock] = []
    for block in _collect_blocks(pages):
        if block["kind"] != "factor":
            continue
        canonical = SOURCE_FACTOR_CHAPTER_HEADINGS[block["heading"]]
        normalized_text = _normalize_block_text(block["lines"], block["heading"])
        raw_sections = _split_section_lines(normalized_text, FACTOR_SECTION_HEADINGS)
        sections = {
            heading: _join_paragraphs(lines)
            for heading, lines in raw_sections.items()
        }
        position_lines = raw_sections.get("Position in Houses and Signs") or raw_sections.get("Position in the Signs") or []
        position_text = "\n".join(position_lines).strip()
        sign_entries = parse_sign_entries(position_text, code_pages)
        factors.append(
            FactorBlock(
                factor=canonical,
                source_heading=block["heading"],
                page=block["page"],
                sections=sections,
                sign_entries=sign_entries,
            )
        )
    return factors


def parse_axis_blocks(pages: list[PageRecord]) -> list[AxisBlock]:
    code_pages = page_lookup(pages)
    axes: list[AxisBlock] = []
    for block in _collect_blocks(pages):
        if block["kind"] != "axis":
            continue
        left, right = block["heading"].split("/")
        factor_a = canonicalize_source_factor(left)
        factor_b = canonicalize_source_factor(right)
        normalized_text = _normalize_block_text(block["lines"], block["heading"])
        lines = normalized_text.splitlines()
        entry_indices = [
            index for index, line in enumerate(lines) if re.match(r"^\s*\d{4}\b", line)
        ]
        first_entry_index = entry_indices[0] if entry_indices else len(lines)
        section_lines = lines[:first_entry_index]
        entry_text = "\n".join(lines[first_entry_index:])
        if entry_indices and "=" not in lines[first_entry_index]:
            second_entry_index = entry_indices[1] if len(entry_indices) > 1 else len(lines)
            section_lines.extend(lines[first_entry_index + 1 : second_entry_index])
            entry_text = "\n".join(lines[second_entry_index:])
        section_text = "\n".join(section_lines)
        sections = _split_sections(section_text, AXIS_SECTION_NAMES)
        activation_entries, unresolved_entries = parse_activation_entries(
            factor_a,
            factor_b,
            entry_text,
            code_pages,
            return_unresolved=True,
        )
        axes.append(
            AxisBlock(
                factor_a=factor_a,
                factor_b=factor_b,
                source_heading=block["heading"],
                page=block["page"],
                sections=sections,
                activation_entries=activation_entries,
                unresolved_activation_entries=unresolved_entries,
            )
        )
    return axes


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _format_section(title: str, text: str) -> str:
    if not text:
        return f"#### {title}\n\n- None extracted.\n"
    return f"#### {title}\n\n{text}\n"


def _astronomicon_axis(factor_a: str, factor_b: str) -> str:
    return f"{astronomicon_token(factor_a)}/{astronomicon_token(factor_b)}"


def _astronomicon_activation(factor_a: str, factor_b: str, activated_by: str) -> str:
    return f"{_astronomicon_axis(factor_a, factor_b)} = {astronomicon_token(activated_by)}"


def _astronomicon_triad(factors: tuple[str, str, str]) -> str:
    return " ".join(astronomicon_token(factor) for factor in factors)


def _activation_page_text(axis: AxisBlock, entry: ActivationEntry, updated_at: str) -> str:
    identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
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
    factors_yaml = "\n".join(f"  - {name}" for name in [axis.factor_a, axis.factor_b, entry.activated_by])
    triad_yaml = "\n".join(f"  - {name}" for name in identity.triad_set)
    return f"""---
title: {identity.display}
page_type: activation
slug: {identity.slug}
status: source_ingested
framework_scope: cosmobiology
factors:
{factors_yaml}
normalized_formula: {identity.display}
axis: {identity.axis.display}
activated_by: {entry.activated_by}
triad_set:
{triad_yaml}
aliases: []
source_pages:
  - reinhold-ebertin-the-combination-of-stellar-influences
updated_at: {updated_at}
---

## Identity

- Formula: `{identity.display}`
{astronomicon_line}- Axis page: [{identity.axis.display}](../axes/{identity.axis.slug}.md)
- Triad hub: [{' '.join(identity.triad_set)}](../triads/{triad_slug(identity.triad_set)}.md)

## Source Entries

### Reinhold Ebertin - The Combination of Stellar Influences

- Entry: `{entry.code}`
- Source page: `{entry.page}`

#### Ebertin Entry

{entry.text}

## Comparative Schema

- core meaning: {entry.text}
- psychology: source-backed meaning retained in the entry above.
- body/health: no separate body-specific bucket is isolated automatically at ingest time.
- social/relationship: source-backed meaning retained in the entry above.
- events/manifestations: source-backed meaning retained in the entry above.
- conflicts/notes: orientation-specific meaning preserved as its own canonical page.

## Contradictions

- None recorded yet for this source-only page.

## Derived Synthesis

- None yet beyond source structuring.

## Links

- [{axis.factor_a}](../factors/{factor_slug(axis.factor_a)}.md)
- [{axis.factor_b}](../factors/{factor_slug(axis.factor_b)}.md)
- [{entry.activated_by}](../factors/{factor_slug(entry.activated_by)}.md)
- [{identity.axis.display}](../axes/{identity.axis.slug}.md)
- [{' '.join(identity.triad_set)}](../triads/{triad_slug(identity.triad_set)}.md)
"""


def _axis_page_text(axis: AxisBlock, updated_at: str) -> str:
    identity = normalize_axis(axis.factor_a, axis.factor_b)
    astronomicon_axis = _astronomicon_axis(identity.factors[0], identity.factors[1])
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != identity.display
        else ""
    )
    factors_yaml = "\n".join(f"  - {name}" for name in identity.factors)
    related_activations = [
        normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
        for entry in axis.activation_entries
    ]
    related_activation_yaml = "\n".join(f"  - {item.display}" for item in related_activations)
    triad_names = sorted({" ".join(item.triad_set) for item in related_activations})
    triad_yaml = "\n".join(f"  - {name}" for name in triad_names)
    related_links = "\n".join(
        f"- [{item.display}](../activations/{item.slug}.md)" for item in related_activations
    )
    return f"""---
title: {identity.display}
page_type: axis
slug: {identity.slug}
status: source_ingested
framework_scope: cosmobiology
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
  - reinhold-ebertin-the-combination-of-stellar-influences
updated_at: {updated_at}
---

## Identity

- Axis: `{identity.display}`
{astronomicon_line}- Source heading: `{axis.source_heading}`
- Source page: `{axis.page}`

## Source Entries

### Reinhold Ebertin - The Combination of Stellar Influences

{_format_section("Principle", axis.sections.get("Principle", ""))}
{_format_section("Psychological Correspondence", axis.sections.get("Psychological Correspondence", ""))}
{_format_section("Biological Correspondence", axis.sections.get("Biological Correspondence", ""))}
{_format_section("Sociological Correspondence", axis.sections.get("Sociological Correspondence", ""))}
{_format_section("Probable Manifestations", axis.sections.get("Probable Manifestations", ""))}

## Comparative Schema

- core meaning: {axis.sections.get("Principle", "None extracted.")}
- psychology: {axis.sections.get("Psychological Correspondence", "None extracted.")}
- body/health: {axis.sections.get("Biological Correspondence", "None extracted.")}
- social/relationship: {axis.sections.get("Sociological Correspondence", "None extracted.")}
- events/manifestations: {axis.sections.get("Probable Manifestations", "None extracted.")}
- conflicts/notes: source-only ingest; no cross-source contradictions are recorded yet.

## Related Activations

{related_links}

## Contradictions

- None recorded yet for this source-only page.

## Derived Synthesis

- None yet beyond source structuring.

## Links

- [{identity.factors[0]}](../factors/{factor_slug(identity.factors[0])}.md)
- [{identity.factors[1]}](../factors/{factor_slug(identity.factors[1])}.md)
- [Reinhold Ebertin - The Combination of Stellar Influences](../sources/reinhold-ebertin-the-combination-of-stellar-influences.md)
"""


def _factor_page_text(
    factor: FactorBlock,
    axis_blocks: list[AxisBlock],
    activation_count: int,
    updated_at: str,
) -> str:
    related_axes = [
        normalize_axis(axis.factor_a, axis.factor_b)
        for axis in axis_blocks
        if factor.factor in {axis.factor_a, axis.factor_b}
    ]
    related_axis_links = "\n".join(
        f"- [{axis.display}](../axes/{axis.slug}.md)" for axis in related_axes
    )
    sign_section_name = "Position in Houses and Signs" if factor.sign_entries else "Position in the Signs"
    sign_lines = "\n".join(
        f"- {entry.sign} (`{entry.code}`, page `{entry.page}`): {entry.text}"
        for entry in factor.sign_entries
    ) or "- None extracted."
    aliases = factor_aliases(factor.factor)
    astronomicon = astronomicon_token(factor.factor)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor.factor
        else ""
    )
    aliases_frontmatter = (
        "aliases:\n" + "\n".join(f"  - {item}" for item in aliases)
        if aliases
        else "aliases: []"
    )
    return f"""---
title: {factor.factor}
page_type: factor
slug: {factor_slug(factor.factor)}
status: source_ingested
framework_scope: cosmobiology
factors:
  - {factor.factor}
{aliases_frontmatter}
source_pages:
  - reinhold-ebertin-the-combination-of-stellar-influences
updated_at: {updated_at}
---

## Identity

- Factor: {factor.factor}
{astronomicon_line}- Source heading: `{factor.source_heading}`
- Source page: `{factor.page}`

## Source Entries

### Reinhold Ebertin - The Combination of Stellar Influences

{_format_section("Principle", factor.sections.get("Principle", ""))}
{_format_section("Psychological Correspondence", factor.sections.get("Psychological Correspondence", ""))}
{_format_section("Biological Correspondence", factor.sections.get("Biological Correspondence", ""))}
{_format_section("Sociological Correspondence", factor.sections.get("Sociological Correspondence", ""))}
#### {sign_section_name}

{sign_lines}

## Comparative Schema

- core meaning: {factor.sections.get("Principle", "None extracted.")}
- psychology: {factor.sections.get("Psychological Correspondence", "None extracted.")}
- body/health: {factor.sections.get("Biological Correspondence", "None extracted.")}
- social/relationship: {factor.sections.get("Sociological Correspondence", "None extracted.")}
- events/manifestations: source-native sign-position material is preserved above.
- conflicts/notes: this factor page now includes the standalone Ebertin factor chapter as source material.

## Derived Synthesis

- None yet beyond source structuring.

## Related Axes

{related_axis_links}

## Related Activations

- Generated activation pages involving `{factor.factor}`: `{activation_count}`.
- Browse [Index](../index.md) or the `wiki/activations/` folder for the full set.

## Related Sources

- [Reinhold Ebertin - The Combination of Stellar Influences](../sources/reinhold-ebertin-the-combination-of-stellar-influences.md)

## Open Questions

- None recorded yet.
"""


def _triad_page_text(orientation_entries: list[tuple[AxisBlock, ActivationEntry]], updated_at: str) -> str:
    first_axis, first_entry = orientation_entries[0]
    first_identity = normalize_activation(first_axis.factor_a, first_axis.factor_b, first_entry.activated_by)
    title = " ".join(first_identity.triad_set)
    slug = triad_slug(first_identity.triad_set)
    astronomicon_triad = _astronomicon_triad(first_identity.triad_set)
    astronomicon_line = (
        f"- Astronomicon triad-set: `{astronomicon_triad}`\n"
        if astronomicon_triad != title
        else ""
    )
    orientation_lines = []
    coverage_lines = []
    for axis, entry in sorted(
        orientation_entries,
        key=lambda item: normalize_activation(item[0].factor_a, item[0].factor_b, item[1].activated_by).display,
    ):
        identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
        orientation_lines.append(
            f"- [{identity.display}](../activations/{identity.slug}.md)\n"
            f"  Source page `{entry.page}`, entry `{entry.code}`"
        )
        coverage_lines.append(f"- `{identity.display}`: page `{entry.page}`, entry `{entry.code}`")
    orientations_yaml = "\n".join(
        f"  - {normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by).display}"
        for axis, entry in sorted(
            orientation_entries,
            key=lambda item: normalize_activation(item[0].factor_a, item[0].factor_b, item[1].activated_by).display,
        )
    )
    factors_yaml = "\n".join(f"  - {name}" for name in first_identity.triad_set)
    links = "\n".join(
        f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in first_identity.triad_set
    )
    return f"""---
title: {title}
page_type: triad_hub
slug: {slug}
status: source_ingested
framework_scope: cosmobiology
factors:
{factors_yaml}
triad_set:
{factors_yaml}
orientations:
{orientations_yaml}
aliases: []
source_pages:
  - reinhold-ebertin-the-combination-of-stellar-influences
updated_at: {updated_at}
---

## Identity

- Triad-set: `{title}`
{astronomicon_line}- This page is structural only. It does not merge the meanings of its orientations.

## Orientation Map

{chr(10).join(orientation_lines)}

## Source Coverage

- Source: [Reinhold Ebertin - The Combination of Stellar Influences](../sources/reinhold-ebertin-the-combination-of-stellar-influences.md)
{chr(10).join(coverage_lines)}

## Contradictions Across Orientations

- None recorded yet.
- Distinct meanings across orientations are preserved as orientation differences, not collapsed into one interpretation.

## Links

{links}
"""


def render_source_page(
    factors: list[FactorBlock],
    axis_blocks: list[AxisBlock],
    triad_count: int,
    activation_count: int,
    updated_at: str,
) -> str:
    factor_links = "\n".join(f"- [{factor.factor}](../factors/{factor_slug(factor.factor)}.md)" for factor in factors)
    return f"""---
title: Reinhold Ebertin - The Combination of Stellar Influences
page_type: source
slug: reinhold-ebertin-the-combination-of-stellar-influences
status: source_ingested
framework_scope: cosmobiology
factors:
{_yaml_list([factor.factor for factor in factors], indent=2)}
aliases:
  - COSI
source_pages: []
updated_at: {updated_at}
---

## Bibliographic Metadata

- Author: Reinhold Ebertin
- Title: *The Combination of Stellar Influences*
- Vault file: `Stellar Influences Vault/planetary expressions - Reinhold Ebertin - The Combination Of Stellar Influences.pdf`

## Scope Notes

- This source page currently reflects the live merged comparative wiki rather than the standalone one-source ingest output.
- Live comparative coverage now preserves the standalone Ebertin factor chapters.
- The repo still contains a standalone Ebertin ingest pipeline capable of generating axis, activation, and triad pages in isolation, but that output has not yet been merged into the current comparative corpus.
- Canonical wiki identities still preserve orientation-specific activation meanings separately.

## Factors Covered

{factor_links}

## Axes Covered

- No live axis pages currently carry explicit Ebertin source attribution in the merged comparative wiki.

## Activations Covered

- No live activation or triad pages currently carry explicit Ebertin source attribution in the merged comparative wiki.

## Ingestion History

- {updated_at}: Ebertin factor chapters are live in the comparative wiki, while the standalone full-source ingest remains available in tooling but is not yet merged into the live axis, activation, and triad corpus.
"""


def generate_models(pdf_path: Path) -> tuple[list[FactorBlock], list[AxisBlock]]:
    pages = extract_page_records(pdf_path)
    return parse_factor_blocks(pages), parse_axis_blocks(pages)
