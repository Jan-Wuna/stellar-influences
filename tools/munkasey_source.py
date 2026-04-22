from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import re

import fitz


SOURCE_FILE = "midpoints - Michael Munkasey - Unleashing the Power of the Planets.pdf"
SOURCE_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"
SOURCE_TITLE = "Michael Munkasey - Midpoints: Unleashing the Power of the Planets"
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
]

SOURCE_FACTOR_NAMES = {
    "Sun": "SUN",
    "Moon": "MOON",
    "Mercury": "MERCURY",
    "Venus": "VENUS",
    "Mars": "MARS",
    "Jupiter": "JUPITER",
    "Saturn": "SATURN",
    "Uranus": "URANUS",
    "Neptune": "NEPTUNE",
    "Pluto": "PLUTO",
    "Node": "NODE",
    "Asc": "ASCENDANT",
    "MC": "MIDHEAVEN",
}

MIDPOINT_START_PAGE_INDEX = 55
PAGES_PER_BLOCK = 4


@dataclass(frozen=True)
class MunkaseyAxisBlock:
    factor_a: str
    factor_b: str
    axis_page: int
    concepts_page: int
    source_heading: str
    basic_ideas: str
    personal_thesis: str
    personal_anti: str
    relationship_thesis: str
    relationship_anti: str
    body_mind: str
    politics_business_thesis: str
    politics_business_anti: str
    concepts: tuple[str, ...]


def _normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = text.replace("thru", "thru")
    return text


def _printed_page(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:5]:
        if re.fullmatch(r"\d{1,3}", line):
            return int(line)
    for line in lines[-5:]:
        if re.fullmatch(r"\d{1,3}", line):
            return int(line)
    raise ValueError("Could not detect printed page number")


def _clean_page_text(text: str) -> str:
    text = _normalize_text(text)
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "Midpoints: Unleashing the Power of the Planets":
            continue
        if re.fullmatch(r"\d{1,3}", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def _collapse(text: str) -> str:
    return " ".join(text.split()).strip()


def _parse_axis_page(text: str) -> tuple[str, str, str, str, str, str, str, str]:
    clean = _clean_page_text(text)
    match = re.search(
        r"Basic Ideas:\s*(.*?)\s*In Your Personal Life:\s*Thesis\s*(.*?)\s*Anti\s*(.*?)\s*"
        r"In Your Relationships:\s*Thesis\s*(.*?)\s*Anti\s*(.*?)\s*"
        r"With Body or Mind:\s*(.*?)\s*In Politics or Business:\s*Thesis\s*(.*?)\s*Anti\s*(.*)$",
        clean,
        re.S,
    )
    if match is None:
        raise ValueError("Could not parse Munkasey axis page")
    return tuple(_collapse(group) for group in match.groups())  # type: ignore[return-value]


def _parse_concepts_page(text: str, source_heading: str) -> tuple[str, ...]:
    clean = _clean_page_text(text)
    concepts: list[str] = []
    for raw_line in clean.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == f"{source_heading} CONCEPTS":
            continue
        concepts.append(_collapse(line))
    if not concepts:
        raise ValueError(f"No concepts extracted for {source_heading}")
    return tuple(concepts)


def generate_models(pdf_path: Path) -> list[MunkaseyAxisBlock]:
    doc = fitz.open(pdf_path)
    expected_pairs = list(combinations(FACTOR_SEQUENCE, 2))
    blocks: list[MunkaseyAxisBlock] = []
    for index, (factor_a, factor_b) in enumerate(expected_pairs):
        axis_page_index = MIDPOINT_START_PAGE_INDEX + (index * PAGES_PER_BLOCK)
        concepts_page_index = axis_page_index + 2
        axis_page = doc[axis_page_index]
        concepts_page = doc[concepts_page_index]
        source_heading = f"{SOURCE_FACTOR_NAMES[factor_a]}/{SOURCE_FACTOR_NAMES[factor_b]}"
        axis_text = _normalize_text(axis_page.get_text())
        if source_heading not in axis_text:
            raise ValueError(f"Expected heading {source_heading} not found on page index {axis_page_index}")
        (
            basic_ideas,
            personal_thesis,
            personal_anti,
            relationship_thesis,
            relationship_anti,
            body_mind,
            politics_business_thesis,
            politics_business_anti,
        ) = _parse_axis_page(axis_text)
        concepts_text = _normalize_text(concepts_page.get_text())
        concepts = _parse_concepts_page(concepts_text, source_heading)
        blocks.append(
            MunkaseyAxisBlock(
                factor_a=factor_a,
                factor_b=factor_b,
                axis_page=_printed_page(axis_text),
                concepts_page=_printed_page(concepts_text),
                source_heading=source_heading,
                basic_ideas=basic_ideas,
                personal_thesis=personal_thesis,
                personal_anti=personal_anti,
                relationship_thesis=relationship_thesis,
                relationship_anti=relationship_anti,
                body_mind=body_mind,
                politics_business_thesis=politics_business_thesis,
                politics_business_anti=politics_business_anti,
                concepts=concepts,
            )
        )
    return blocks
