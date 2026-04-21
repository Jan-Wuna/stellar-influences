from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
import re

import fitz


SOURCE_FILE = "Book_2012_Michelle Falis_AstroFix_Planet Combinations- Astrological Brainstorms_kindle.pdf"
SOURCE_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
SOURCE_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
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
]


@dataclass(frozen=True)
class AxisBlock:
    factor_a: str
    factor_b: str
    page: int
    text: str


def _expected_axes() -> list[tuple[str, str]]:
    return list(combinations(FACTOR_SEQUENCE, 2))


SECTION_START_PAGES = {
    ("Sun", "Moon"): 3,
    ("Sun", "Mercury"): 5,
    ("Sun", "Venus"): 7,
    ("Sun", "Mars"): 8,
    ("Sun", "Jupiter"): 10,
    ("Sun", "Saturn"): 12,
    ("Sun", "Uranus"): 14,
    ("Sun", "Neptune"): 16,
    ("Sun", "Pluto"): 18,
    ("Moon", "Mercury"): 20,
    ("Moon", "Venus"): 22,
    ("Moon", "Mars"): 23,
    ("Moon", "Jupiter"): 25,
    ("Moon", "Saturn"): 26,
    ("Moon", "Uranus"): 28,
    ("Moon", "Neptune"): 30,
    ("Moon", "Pluto"): 32,
    ("Mercury", "Venus"): 33,
    ("Mercury", "Mars"): 35,
    ("Mercury", "Jupiter"): 37,
    ("Mercury", "Saturn"): 38,
    ("Mercury", "Uranus"): 40,
    ("Mercury", "Neptune"): 41,
    ("Mercury", "Pluto"): 42,
    ("Venus", "Mars"): 43,
    ("Venus", "Jupiter"): 45,
    ("Venus", "Saturn"): 47,
    ("Venus", "Uranus"): 49,
    ("Venus", "Neptune"): 51,
    ("Venus", "Pluto"): 53,
    ("Mars", "Jupiter"): 55,
    ("Mars", "Saturn"): 57,
    ("Mars", "Uranus"): 59,
    ("Mars", "Neptune"): 61,
    ("Mars", "Pluto"): 63,
    ("Jupiter", "Saturn"): 65,
    ("Jupiter", "Uranus"): 67,
    ("Jupiter", "Neptune"): 68,
    ("Jupiter", "Pluto"): 69,
    ("Saturn", "Uranus"): 71,
    ("Saturn", "Neptune"): 73,
    ("Saturn", "Pluto"): 75,
    ("Uranus", "Neptune"): 77,
    ("Uranus", "Pluto"): 79,
    ("Neptune", "Pluto"): 81,
}


def _letters_only(text: str) -> str:
    clean = (
        text.replace("\xa0", " ")
        .replace("\u00ad", "")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    return re.sub(r"[^a-z]+", "", clean.casefold())


def _line_records(pdf_path: Path) -> list[list[str]]:
    doc = fitz.open(pdf_path)
    pages: list[list[str]] = []
    for page in doc:
        text = (
            page.get_text()
            .replace("\xa0", " ")
            .replace("\u00ad", "")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
        )
        pages.append([line.rstrip() for line in text.splitlines()])
    return pages


_HEADING_KEYS = {_letters_only(f"{factor_a}/{factor_b}") for factor_a, factor_b in _expected_axes()}


def _append_line(buffer: list[str], line: str) -> None:
    clean = " ".join(line.split())
    if not clean:
        if buffer and buffer[-1]:
            buffer.append("")
        return
    if buffer and buffer[-1] and buffer[-1][-1].isalnum() and clean[:1].islower():
        buffer[-1] = f"{buffer[-1]} {clean}"
        return
    if buffer and buffer[-1] and buffer[-1].endswith("-"):
        buffer[-1] = f"{buffer[-1][:-1]}{clean}"
        return
    if buffer and buffer[-1]:
        buffer[-1] = f"{buffer[-1]} {clean}"
        return
    buffer.append(clean)


def _trim_last_section(lines: list[str]) -> list[str]:
    trimmed: list[str] = []
    for line in lines:
        normalized = _letters_only(line)
        if normalized.startswith("bibliogra") or normalized == "about":
            break
        trimmed.append(line)
    return trimmed


def _looks_like_heading(line: str) -> bool:
    normalized = _letters_only(line)
    if not normalized:
        return False
    if normalized in _HEADING_KEYS:
        return True
    if len(line.strip()) <= 40:
        best_score = max(SequenceMatcher(None, normalized, key).ratio() for key in _HEADING_KEYS)
        if best_score >= 0.72:
            return True
    return normalized.startswith("bibliogra") or normalized == "about"


def _section_from_page_range(
    pages: list[list[str]],
    start_page: int,
    end_page: int,
) -> tuple[int, str]:
    raw_lines: list[str] = []
    for page_number in range(start_page, end_page + 1):
        lines = pages[page_number - 1]
        if page_number == end_page:
            lines = _trim_last_section(lines)
        for line in lines:
            if _looks_like_heading(line):
                continue
            raw_lines.append(line)

    buffer: list[str] = []
    for line in raw_lines:
        _append_line(buffer, line)

    paragraphs = [paragraph for paragraph in buffer if paragraph]
    if not paragraphs:
        raise ValueError(f"no content extracted between pages {start_page}-{end_page}")
    return start_page, "\n\n".join(paragraphs).strip()


def generate_models(pdf_path: Path) -> list[AxisBlock]:
    pages = _line_records(pdf_path)
    blocks: list[AxisBlock] = []
    expected_axes = _expected_axes()
    for index, (factor_a, factor_b) in enumerate(expected_axes):
        start_page = SECTION_START_PAGES[(factor_a, factor_b)]
        if index + 1 < len(expected_axes):
            next_axis = expected_axes[index + 1]
            end_page = SECTION_START_PAGES[next_axis] - 1
        else:
            end_page = len(pages) - 1
        page, text = _section_from_page_range(pages, start_page, end_page)
        blocks.append(
            AxisBlock(
                factor_a=factor_a,
                factor_b=factor_b,
                page=page,
                text=text,
            )
        )
    return blocks
