from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import bisect
import re

import fitz

from tools.wiki_identity import normalize_axis


SOURCE_FILE = "planetary expressions - Robert Hand - Horoscope Symbols.pdf"
SOURCE_SLUG = "robert-hand-horoscope-symbols"
SOURCE_TITLE = "Robert Hand - Horoscope Symbols"
FRAMEWORK_SCOPE = "modern_astrology"

FACTOR_SEQUENCE = [
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
    "Vernal Point",
]

DISPLAY_NAMES = {
    "Node": "Nodes",
    "Asc": "Ascendant",
    "MC": "Midheaven",
    "Vernal Point": "Aries",
}


@dataclass(frozen=True)
class HandAxisBlock:
    factor_a: str
    factor_b: str
    page: int
    heading: str
    text: str


@dataclass(frozen=True)
class HandFactorBlock:
    factor: str
    page: int
    heading: str
    text: str


@dataclass(frozen=True)
class _FactorSectionSpec:
    factors: tuple[str, ...]
    heading: str
    start_page: int
    end_page: int
    stop_heading: str | None = None


def _expected_pairs() -> list[tuple[str, str]]:
    return list(combinations(FACTOR_SEQUENCE, 2))


def _display_name(name: str) -> str:
    return DISPLAY_NAMES.get(name, name)


def _source_heading(factor_a: str, factor_b: str) -> str:
    return f"{_display_name(factor_a)}/{_display_name(factor_b)}"


SOURCE_HEADINGS = [_source_heading(factor_a, factor_b) for factor_a, factor_b in _expected_pairs()]

FACTOR_SECTION_SPECS = (
    _FactorSectionSpec(("Sun",), "The Sun", 52, 56, "The Moon"),
    _FactorSectionSpec(("Moon",), "The Moon", 56, 61, "Mercury"),
    _FactorSectionSpec(("Mercury",), "Mercury", 61, 67, "Venus"),
    _FactorSectionSpec(("Venus",), "Venus", 67, 71, "Mars"),
    _FactorSectionSpec(("Mars",), "Mars", 71, 74, "Jupiter"),
    _FactorSectionSpec(("Jupiter",), "Jupiter", 74, 79, "Saturn"),
    _FactorSectionSpec(("Saturn",), "Saturn", 79, 84, "Uranus"),
    _FactorSectionSpec(("Uranus",), "Uranus", 84, 89, "Neptune"),
    _FactorSectionSpec(("Neptune",), "Neptune", 89, 94, "Pluto"),
    _FactorSectionSpec(("Pluto",), "Pluto", 94, 100, "Other Points in the Chart"),
    _FactorSectionSpec(("Asc", "MC"), "The Ascendant and Midheaven", 102, 104, "Intermediate House Cusps"),
    _FactorSectionSpec(("Node",), "The Lunar Nodes", 105, 107, "Planetary Nodes"),
    _FactorSectionSpec(("Vernal Point",), "The Aries Point", 108, 110, "Body-Type Points"),
)


def _normalize_text(text: str) -> str:
    normalized = (
        text.replace("\xa0", " ")
        .replace("\u00ad", "")
        .replace("â€™", "'")
        .replace("â€ś", '"')
        .replace("â€ť", '"')
        .replace("â€“", "-")
        .replace("â€”", "-")
        .replace("ﬁ", "fi")
        .replace("ﬂ", "fl")
    )
    normalized = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "-", normalized)
    replacements = {
        "TlieMoon": "The Moon",
        "Suii/": "Sun/",
        "Swi/": "Sun/",
        "Pairs with the Swi": "Pairs with the Sun",
    }
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    for heading in sorted(SOURCE_HEADINGS, key=len, reverse=True):
        spaced = r"\s*".join(re.escape(char) for char in heading)
        normalized = re.sub(
            rf"(?m)^(\s*){spaced}(?=\s)",
            rf"\1{heading}",
            normalized,
        )
    return normalized


def _normalized_pages(pdf_path: Path) -> list[str]:
    doc = fitz.open(pdf_path)
    return [_normalize_text(page.get_text("text")) for page in doc]


def _chapter_page_records(pdf_path: Path) -> list[tuple[int, str]]:
    normalized_pages = _normalized_pages(pdf_path)
    chapter_starts = [
        index
        for index, text in enumerate(normalized_pages)
        if "Brief Meanings of Planetary Pairs" in text
    ]
    if not chapter_starts:
        raise ValueError("could not locate Hand planetary-pairs chapter")

    start_index = chapter_starts[-1]
    records: list[tuple[int, str]] = []
    for page_index, text in enumerate(normalized_pages[start_index + 1 :], start=start_index + 1):
        if "The Signs: Introduction" in text:
            break
        if not text.strip():
            continue
        records.append((page_index + 1, text))
    if not records:
        raise ValueError("could not locate Hand planetary-pairs chapter body")
    return records


def _paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    for chunk in re.split(r"\n\s*\n+", text):
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        merged = lines[0]
        for line in lines[1:]:
            if merged.endswith("-"):
                merged = f"{merged[:-1]}{line}"
            else:
                merged = f"{merged} {line}"
        paragraphs.append(re.sub(r"\s+", " ", merged).strip())
    return paragraphs


def _page_for_offset(offset: int, starts: list[int], pages: list[int]) -> int:
    index = bisect.bisect_right(starts, offset) - 1
    return pages[index]


def _extract_section_from_page_range(
    pages: list[str],
    start_page: int,
    end_page: int,
    heading: str,
    stop_heading: str | None,
) -> str:
    combined = "\n".join(pages[start_page - 1 : end_page])
    start_match = re.search(re.escape(heading), combined)
    if start_match is None:
        raise ValueError(f"could not locate Hand factor heading: {heading}")

    body = combined[start_match.end() :]
    if stop_heading is not None:
        stop_match = re.search(re.escape(stop_heading), body)
        if stop_match is not None:
            body = body[: stop_match.start()]

    text = "\n\n".join(_paragraphs(body)).strip()
    if not text:
        raise ValueError(f"empty Hand factor body for {heading}")
    return text


def generate_models(
    pdf_path: Path,
    limit_pairs: list[tuple[str, str]] | None = None,
) -> list[HandAxisBlock]:
    records = _chapter_page_records(pdf_path)
    page_numbers = [page for page, _ in records]
    page_starts: list[int] = []
    chunks: list[str] = []
    cursor = 0
    for page_number, text in records:
        page_starts.append(cursor)
        chunks.append(text)
        cursor += len(text) + 1
    combined = "\n".join(chunks)

    expected = _expected_pairs()
    positions: list[tuple[tuple[str, str], str, int, int]] = []
    search_start = 0
    for factor_a, factor_b in expected:
        heading = _source_heading(factor_a, factor_b)
        pattern = re.compile(rf"(?m)^\s*{re.escape(heading)}\s+")
        match = pattern.search(combined, pos=search_start)
        if match is None:
            raise ValueError(f"could not locate Hand entry heading: {heading}")
        positions.append(((factor_a, factor_b), heading, match.start(), match.end()))
        search_start = match.end()

    blocks: list[HandAxisBlock] = []
    for index, (pair, heading, start, body_start) in enumerate(positions):
        end = positions[index + 1][2] if index + 1 < len(positions) else len(combined)
        raw_body = combined[body_start:end]
        raw_body = re.sub(r"(?m)^\s*Pairs with the [^\n]+\n?", "", raw_body)
        text = "\n\n".join(_paragraphs(raw_body)).strip()
        if not text:
            raise ValueError(f"empty Hand entry body for {heading}")
        page = _page_for_offset(start, page_starts, page_numbers)
        axis = normalize_axis(*pair)
        blocks.append(
            HandAxisBlock(
                factor_a=axis.factors[0],
                factor_b=axis.factors[1],
                page=page,
                heading=heading,
                text=text,
            )
        )

    found = {(block.factor_a, block.factor_b) for block in blocks}
    expected_axes = {normalize_axis(*pair).factors for pair in expected}
    if found != expected_axes:
        missing = sorted(expected_axes - found)
        extra = sorted(found - expected_axes)
        raise ValueError(f"Hand pair coverage mismatch: missing={missing} extra={extra}")

    if limit_pairs is None:
        return blocks

    allowed = {normalize_axis(*pair).factors for pair in limit_pairs}
    return [block for block in blocks if (block.factor_a, block.factor_b) in allowed]


def generate_factor_models(
    pdf_path: Path,
    limit_factors: list[str] | None = None,
) -> list[HandFactorBlock]:
    pages = _normalized_pages(pdf_path)
    blocks: list[HandFactorBlock] = []
    for spec in FACTOR_SECTION_SPECS:
        text = _extract_section_from_page_range(
            pages,
            spec.start_page,
            spec.end_page,
            spec.heading,
            spec.stop_heading,
        )
        for factor in spec.factors:
            blocks.append(
                HandFactorBlock(
                    factor=factor,
                    page=spec.start_page,
                    heading=spec.heading,
                    text=text,
                )
            )

    found = {block.factor for block in blocks}
    expected = set(FACTOR_SEQUENCE)
    if found != expected:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        raise ValueError(f"Hand factor coverage mismatch: missing={missing} extra={extra}")

    if limit_factors is None:
        return blocks

    allowed = set(limit_factors)
    return [block for block in blocks if block.factor in allowed]
