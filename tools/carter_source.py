from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import re

import fitz

from tools.wiki_identity import normalize_axis


SOURCE_FILE = "Book_2000_Charles Carter_The Astrological Aspects.pdf"
SOURCE_SLUG = "charles-carter-the-astrological-aspects"
SOURCE_TITLE = "Charles Carter - The Astrological Aspects"
FRAMEWORK_SCOPE = "classical_aspects"

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
]

SECTION_HEADINGS = (
    "THE HARMONIOUS ASPECTS",
    "THE CONJUNCTION",
    "THE INHARMONIOUS ASPECTS",
)


@dataclass(frozen=True)
class CarterSection:
    heading: str
    text: str


@dataclass(frozen=True)
class CarterExampleGroup:
    label: str
    text: str


@dataclass(frozen=True)
class CarterAxisBlock:
    factor_a: str
    factor_b: str
    page: int
    heading: str
    intro_text: str
    sections: tuple[CarterSection, ...]
    example_groups: tuple[CarterExampleGroup, ...]

    def _section_text(self, heading: str) -> str:
        for section in self.sections:
            if section.heading == heading:
                return section.text
        return ""

    def _example_text(self, label_prefix: str) -> str:
        prefix = label_prefix.casefold()
        for group in self.example_groups:
            if group.label.casefold().startswith(prefix):
                return group.text
        return ""

    @property
    def harmonious_text(self) -> str:
        return self._section_text("THE HARMONIOUS ASPECTS")

    @property
    def conjunction_text(self) -> str:
        return self._section_text("THE CONJUNCTION")

    @property
    def inharmonious_text(self) -> str:
        return self._section_text("THE INHARMONIOUS ASPECTS")

    @property
    def harmonious_examples(self) -> str:
        return self._example_text("Harmonious")

    @property
    def conjunction_examples(self) -> str:
        return self._example_text("The Conjunction")

    @property
    def inharmonious_examples(self) -> str:
        return self._example_text("Inharmonious")


@dataclass(frozen=True)
class _PageRecord:
    page: int
    blocks: tuple[str, ...]


@dataclass(frozen=True)
class _ChapterMarker:
    page_index: int
    block_index: int
    heading: str
    factor_a: str
    factor_b: str


def _expected_pairs() -> list[tuple[str, str]]:
    return list(combinations(FACTOR_SEQUENCE, 2))


def _normalize_text(text: str) -> str:
    return (
        text.replace("\xa0", " ")
        .replace("\u00ad", "")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace("ﬁ", "fi")
        .replace("ﬂ", "fl")
    )


def _paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    for chunk in re.split(r"\n\s*\n+", _normalize_text(text)):
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


def _printed_page_number(page: fitz.Page) -> int:
    for block in page.get_text("blocks"):
        paragraphs = _paragraphs(block[4])
        if paragraphs and paragraphs[0].isdigit():
            return int(paragraphs[0])
    return page.number + 1


def _parse_heading(text: str) -> tuple[str, str] | None:
    paragraphs = _paragraphs(text)
    if len(paragraphs) != 1:
        return None
    heading = paragraphs[0]
    if not heading.startswith("ASPECTS OF "):
        return None
    pair_text = heading.removeprefix("ASPECTS OF ").strip()
    if pair_text.startswith("THE "):
        pair_text = pair_text.removeprefix("THE ").strip()
    if " AND " in pair_text:
        left_text, right_text = pair_text.split(" AND ", 1)
    elif " & " in pair_text:
        left_text, right_text = pair_text.split(" & ", 1)
    else:
        return None
    left = left_text.title()
    right = right_text.title()
    if left not in FACTOR_SEQUENCE or right not in FACTOR_SEQUENCE:
        return None
    return left, right


def _load_pages(pdf_path: Path) -> list[_PageRecord]:
    doc = fitz.open(pdf_path)
    pages: list[_PageRecord] = []
    for page in doc:
        printed_page = _printed_page_number(page)
        if printed_page < 5:
            continue
        blocks = tuple(_normalize_text(block[4]) for block in page.get_text("blocks"))
        pages.append(_PageRecord(page=printed_page, blocks=blocks))
    return pages


def _chapter_markers(pages: list[_PageRecord]) -> list[_ChapterMarker]:
    markers: list[_ChapterMarker] = []
    for page_index, page in enumerate(pages):
        for block_index, block in enumerate(page.blocks):
            parsed = _parse_heading(block)
            if parsed is None:
                continue
            axis = normalize_axis(*parsed)
            markers.append(
                _ChapterMarker(
                    page_index=page_index,
                    block_index=block_index,
                    heading=_paragraphs(block)[0],
                    factor_a=axis.factors[0],
                    factor_b=axis.factors[1],
                )
            )
    return markers


def _collect_chapter_text(
    pages: list[_PageRecord],
    marker: _ChapterMarker,
    next_marker: _ChapterMarker | None,
) -> str:
    chunks: list[str] = []
    last_page_index = next_marker.page_index if next_marker is not None else len(pages) - 1
    for page_index in range(marker.page_index, last_page_index + 1):
        page = pages[page_index]
        start_block = marker.block_index + 1 if page_index == marker.page_index else 0
        end_block = next_marker.block_index if next_marker is not None and page_index == next_marker.page_index else len(page.blocks)
        for block in page.blocks[start_block:end_block]:
            paragraphs = _paragraphs(block)
            if paragraphs and all(paragraph.isdigit() for paragraph in paragraphs):
                continue
            chunks.append(block)
    return "\n\n".join(chunks).strip()


def _parse_sections(paragraphs: list[str]) -> tuple[str, tuple[CarterSection, ...]]:
    intro: list[str] = []
    sections: list[CarterSection] = []
    active_heading: str | None = None
    active_lines: list[str] = []
    for paragraph in paragraphs:
        if paragraph in SECTION_HEADINGS:
            if active_heading is None:
                intro = list(active_lines)
            else:
                sections.append(CarterSection(heading=active_heading, text="\n\n".join(active_lines).strip()))
            active_heading = paragraph
            active_lines = []
            continue
        active_lines.append(paragraph)

    if active_heading is None:
        intro = list(active_lines)
    else:
        sections.append(CarterSection(heading=active_heading, text="\n\n".join(active_lines).strip()))

    return "\n\n".join(intro).strip(), tuple(section for section in sections if section.text)


def _looks_like_example_label(paragraph: str) -> bool:
    if "," in paragraph or "." in paragraph:
        return False
    return len(paragraph) <= 40


def _parse_examples(paragraphs: list[str]) -> tuple[CarterExampleGroup, ...]:
    if not paragraphs:
        return ()
    if not paragraphs[0].startswith("EXAMPLES FOR "):
        return ()
    groups: list[CarterExampleGroup] = []
    active_label: str | None = None
    active_lines: list[str] = []
    for paragraph in paragraphs[1:]:
        if _looks_like_example_label(paragraph):
            if active_label is not None and active_lines:
                groups.append(CarterExampleGroup(label=active_label, text="\n\n".join(active_lines).strip()))
            active_label = paragraph
            active_lines = []
            continue
        active_lines.append(paragraph)
    if active_label is not None and active_lines:
        groups.append(CarterExampleGroup(label=active_label, text="\n\n".join(active_lines).strip()))
    return tuple(groups)


def _build_block(marker: _ChapterMarker, page: int, raw_text: str) -> CarterAxisBlock:
    paragraphs = _paragraphs(raw_text)
    example_index = next((index for index, paragraph in enumerate(paragraphs) if paragraph.startswith("EXAMPLES FOR ")), None)
    if example_index is None:
        body_paragraphs = paragraphs
        example_paragraphs: list[str] = []
    else:
        body_paragraphs = paragraphs[:example_index]
        example_paragraphs = paragraphs[example_index:]
    intro_text, sections = _parse_sections(body_paragraphs)
    example_groups = _parse_examples(example_paragraphs)
    return CarterAxisBlock(
        factor_a=marker.factor_a,
        factor_b=marker.factor_b,
        page=page,
        heading=marker.heading,
        intro_text=intro_text,
        sections=sections,
        example_groups=example_groups,
    )


def generate_models(
    pdf_path: Path,
    limit_pairs: list[tuple[str, str]] | None = None,
) -> list[CarterAxisBlock]:
    pages = _load_pages(pdf_path)
    markers = _chapter_markers(pages)
    blocks: list[CarterAxisBlock] = []
    for index, marker in enumerate(markers):
        next_marker = markers[index + 1] if index + 1 < len(markers) else None
        raw_text = _collect_chapter_text(pages, marker, next_marker)
        blocks.append(_build_block(marker, pages[marker.page_index].page, raw_text))

    expected = {normalize_axis(*pair).factors for pair in _expected_pairs()}
    found = {(block.factor_a, block.factor_b) for block in blocks}
    if found != expected:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        raise ValueError(f"Carter pair coverage mismatch: missing={missing} extra={extra}")

    if limit_pairs is None:
        return blocks

    wanted = {normalize_axis(*pair).factors for pair in limit_pairs}
    return [block for block in blocks if (block.factor_a, block.factor_b) in wanted]
