from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
import re

import fitz


SOURCE_FILE = "Book_2015_John Sandbach_Midpoints_A Kabbalistic Compendium of Meanings for Astrological Midpoints.pdf"
SOURCE_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
SOURCE_TITLE = "John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints"
FRAMEWORK_SCOPE = "modern_astrology"

FACTOR_SEQUENCE = [
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Chiron",
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
    "Chiron": "Chiron",
    "Uranus": "Uranus",
    "Neptune": "Neptune",
    "Pluto": "Pluto",
    "Node": "Node",
    "Asc": "Ascendant",
    "MC": "Midheaven",
}


@dataclass(frozen=True)
class ActivationEntry:
    activated_by: str
    text: str


@dataclass(frozen=True)
class AxisBlock:
    factor_a: str
    factor_b: str
    page: int
    source_heading: str
    principle: str
    process: str
    activation_entries: tuple[ActivationEntry, ...]


@dataclass(frozen=True)
class HeadingPosition:
    factor_a: str
    factor_b: str
    page_index: int
    line_index: int

    @property
    def page(self) -> int:
        return self.page_index + 1


def _normalize_text(text: str) -> str:
    return (
        text.replace("\xa0", " ")
        .replace("\u00ad", "")
        .replace("â€™", "'")
        .replace("â€œ", '"')
        .replace("â€ť", '"')
        .replace("â€“", "-")
        .replace("â€”", "-")
        .replace("ﬁ", "fi")
        .replace("ﬂ", "fl")
    )


def _letters_only(text: str) -> str:
    cleaned = _normalize_text(text)
    cleaned = cleaned.replace("M id heaven", "Midheaven")
    cleaned = cleaned.replace("Mercurv", "Mercury")
    cleaned = cleaned.replace("A/enus", "Venus")
    return re.sub(r"[^a-z]+", "", cleaned.casefold())


def _source_heading(factor_a: str, factor_b: str) -> str:
    return f"Planets activating the {SOURCE_FACTOR_NAMES[factor_a]}/{SOURCE_FACTOR_NAMES[factor_b]} midpoint"


EXPECTED_AXES = list(combinations(FACTOR_SEQUENCE, 2))
EXPECTED_HEADINGS = {
    _letters_only(_source_heading(factor_a, factor_b)): (factor_a, factor_b)
    for factor_a, factor_b in EXPECTED_AXES
}

SECTION_LABELS = {"Principle": "principle", "Process": "process"}
ENTRY_LABELS = {
    SOURCE_FACTOR_NAMES[factor]: factor
    for factor in FACTOR_SEQUENCE
}


def _page_lines(pdf_path: Path) -> list[list[str]]:
    doc = fitz.open(pdf_path)
    pages: list[list[str]] = []
    for page in doc:
        text = _normalize_text(page.get_text())
        pages.append([line.rstrip() for line in text.splitlines()])
    return pages


def _match_heading(line: str, next_line: str = "") -> tuple[str, str] | None:
    if not line.strip().casefold().startswith("planets"):
        return None

    candidates = [line]
    if next_line and "midpoint" not in line.casefold():
        candidates.append(f"{line} {next_line}")
    best_score = 0.0
    best_axis: tuple[str, str] | None = None
    for candidate in candidates:
        normalized = _letters_only(candidate)
        if "planetsactivatingthe" not in normalized or "midpoint" not in normalized:
            continue
        for expected, axis in EXPECTED_HEADINGS.items():
            score = SequenceMatcher(None, normalized, expected).ratio()
            if score > best_score:
                best_score = score
                best_axis = axis
    if best_score >= 0.94:
        return best_axis
    return None


def _heading_positions(pages: list[list[str]]) -> list[HeadingPosition]:
    positions: list[HeadingPosition] = []
    for page_index in range(5, len(pages)):
        lines = pages[page_index]
        for line_index, line in enumerate(lines):
            next_line = lines[line_index + 1] if line_index + 1 < len(lines) else ""
            matched = _match_heading(line, next_line)
            if matched is None:
                continue
            position = HeadingPosition(
                factor_a=matched[0],
                factor_b=matched[1],
                page_index=page_index,
                line_index=line_index,
            )
            if positions and (
                positions[-1].factor_a,
                positions[-1].factor_b,
                positions[-1].page_index,
                positions[-1].line_index,
            ) == (
                position.factor_a,
                position.factor_b,
                position.page_index,
                position.line_index,
            ):
                continue
            positions.append(position)

    completed: list[HeadingPosition] = []
    found_index = 0
    for expected in EXPECTED_AXES:
        if found_index < len(positions) and (positions[found_index].factor_a, positions[found_index].factor_b) == expected:
            completed.append(positions[found_index])
            found_index += 1
            continue
        previous = completed[-1] if completed else None
        following = positions[found_index] if found_index < len(positions) else None
        completed.append(_infer_missing_heading(expected, pages, previous, following))

    found = [(item.factor_a, item.factor_b) for item in completed]
    if found != EXPECTED_AXES:
        raise ValueError(
            "Sandbach pair coverage mismatch: "
            f"expected={len(EXPECTED_AXES)} found={len(found)}"
        )
    return completed


def _infer_missing_heading(
    expected: tuple[str, str],
    pages: list[list[str]],
    previous: HeadingPosition | None,
    following: HeadingPosition | None,
) -> HeadingPosition:
    principle_positions: list[tuple[int, int]] = []
    start_page = previous.page_index if previous is not None else 5
    end_page = following.page_index if following is not None else len(pages) - 1
    for page_index in range(start_page, end_page + 1):
        lines = pages[page_index]
        start = previous.line_index + 1 if previous is not None and page_index == previous.page_index else 0
        stop = following.line_index if following is not None and page_index == following.page_index else len(lines)
        for line_index, line in enumerate(lines[start:stop], start=start):
            if line.strip().startswith("Principle:"):
                principle_positions.append((page_index, line_index))
    if not principle_positions:
        raise ValueError(f"Could not infer missing Sandbach heading for {expected[0]}/{expected[1]}")
    page_index, line_index = principle_positions[-1]
    return HeadingPosition(
        factor_a=expected[0],
        factor_b=expected[1],
        page_index=page_index,
        line_index=line_index - 1,
    )


def _collect_chapter_lines(
    pages: list[list[str]],
    current: HeadingPosition,
    following: HeadingPosition | None,
) -> list[str]:
    lines: list[str] = []
    last_page_index = following.page_index if following is not None else len(pages) - 1
    for page_index in range(current.page_index, last_page_index + 1):
        page_lines = pages[page_index]
        start = current.line_index + 1 if page_index == current.page_index else 0
        stop = following.line_index if following is not None and page_index == following.page_index else len(page_lines)
        for line in page_lines[start:stop]:
            stripped = line.strip()
            if re.fullmatch(r"\d{1,3}", stripped):
                continue
            lines.append(line)
    return lines


def _merge_lines(lines: list[str]) -> str:
    merged: list[str] = []
    for line in lines:
        stripped = " ".join(line.split())
        if not stripped:
            continue
        if merged and merged[-1].endswith("-"):
            merged[-1] = f"{merged[-1][:-1]}{stripped}"
            continue
        merged.append(stripped)
    return " ".join(merged).strip()


def _parse_chapter(
    factor_a: str,
    factor_b: str,
    page: int,
    lines: list[str],
) -> AxisBlock:
    remaining = [factor for factor in FACTOR_SEQUENCE if factor not in {factor_a, factor_b}]
    label_map = {**SECTION_LABELS, **{label: ENTRY_LABELS[label] for label in ENTRY_LABELS}}
    current_label: str | None = None
    buffers: dict[str, list[str]] = {"principle": [], "process": []}
    for factor in remaining:
        buffers[factor] = []

    label_names = "Principle|Process|Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Chiron|Uranus|Neptune|Pluto|Node|Ascendant|Midheaven"
    label_pattern = re.compile(rf"^({label_names})[:.]\s*(.*)$")
    embedded_label_pattern = re.compile(rf"\s({label_names})[:.]\s+")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        embedded = embedded_label_pattern.search(stripped)
        if embedded and not label_pattern.match(stripped):
            prefix = stripped[: embedded.start()].strip()
            suffix = stripped[embedded.start() :].strip()
            if prefix and current_label is not None:
                buffers[current_label].append(prefix)
            stripped = suffix
        match = label_pattern.match(stripped)
        if match:
            current_label = label_map[match.group(1)]
            if current_label not in buffers:
                current_label = None
                continue
            rest = match.group(2).strip()
            if rest:
                buffers[current_label].append(rest)
            continue
        if current_label is not None:
            buffers[current_label].append(stripped)

    principle = _merge_lines(buffers["principle"])
    process = _merge_lines(buffers["process"])
    activation_entries = tuple(
        ActivationEntry(activated_by=factor, text=text)
        for factor in remaining
        if (text := _merge_lines(buffers[factor]))
    )
    if not principle or not process:
        raise ValueError(f"Incomplete Sandbach chapter parse for {factor_a}/{factor_b}")

    return AxisBlock(
        factor_a=factor_a,
        factor_b=factor_b,
        page=page,
        source_heading=_source_heading(factor_a, factor_b),
        principle=principle,
        process=process,
        activation_entries=activation_entries,
    )


def generate_models(pdf_path: Path) -> list[AxisBlock]:
    pages = _page_lines(pdf_path)
    headings = _heading_positions(pages)
    blocks: list[AxisBlock] = []
    for index, current in enumerate(headings):
        following = headings[index + 1] if index + 1 < len(headings) else None
        chapter_lines = _collect_chapter_lines(pages, current, following)
        blocks.append(
            _parse_chapter(
                current.factor_a,
                current.factor_b,
                current.page,
                chapter_lines,
            )
        )
    return blocks
