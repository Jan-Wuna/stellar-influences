from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import fitz


SOURCE_FILE = "Book_2007_Don Mcbroom_Midpoints.pdf"
SOURCE_SLUG = "don-mcbroom-midpoints"
SOURCE_TITLE = "Don McBroom - Midpoints"
FRAMEWORK_SCOPE = "modern_astrology"


@dataclass(frozen=True)
class SourceBlock:
    page_type: str
    slug: str
    source_heading: str
    page: int
    text: str


SECTION_SPECS = (
    {
        "page_type": "axis",
        "slug": "sun-moon",
        "source_heading": "The Sun/Moon Midpoint",
        "pages": (58, 59),
        "start_marker": "Not surprisingly, then, we would expect that the",
        "stop_marker": "When a Focal Point is within orb of the",
    },
    {
        "page_type": "axis",
        "slug": "asc-mc",
        "source_heading": "The Ascendant/Midheaven Midpoint",
        "pages": (71, 72),
        "start_marker": "Regardless of the specific definitions we choose for the Ascendant and Midheaven,",
        "stop_marker": "If a Focal Point is within orb of the Ascendant/Midheaven midpoint",
    },
    {
        "page_type": "activation",
        "slug": "sun-moon-equals-mercury",
        "source_heading": "Mercury at the Sun/Moon Midpoint",
        "pages": (60, 60),
        "start_marker": "When Mercury is the Focal Point of a midpoint picture relating to the Sun/Moon,",
        "stop_marker": "* With Mercury as the Focal Point of his Sun/Moon midpoint",
    },
    {
        "page_type": "activation",
        "slug": "asc-mc-equals-mercury",
        "source_heading": "Mercury = Asc/Mc",
        "pages": (73, 74),
        "start_marker": "When Mercury is located at the Asc/Mc midpoint,",
        "stop_marker": "Famous people with this placement include",
    },
)


def _strip_page_artifacts(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("SIGNIFICANT MIDPOINTS"):
            continue
        if re.fullmatch(r"\d+\s+CHAPTER THREE", stripped):
            continue
        if re.fullmatch(r"[0-9Il]{1,3}", stripped):
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)


def _normalized_pages(pdf_path: Path, start_page: int, end_page: int) -> str:
    doc = fitz.open(pdf_path)
    text = "\n".join(
        _strip_page_artifacts(doc.load_page(page_number - 1).get_text("text"))
        for page_number in range(start_page, end_page + 1)
    )
    return (
        text.replace("\xa0", " ")
        .replace("\u00ad", "")
        .replace("—", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("‘", "'")
        .replace("…", "...")
        .replace("•", "*")
        .replace("©/2>", "Sun/Moon")
        .replace("©/D", "Sun/Moon")
        .replace("O/D", "Sun/Moon")
        .replace("©-2) Blend", "Sun-Moon Blend")
        .replace("©-D Blend", "Sun-Moon Blend")
        .replace("Ă˘â‚¬â„˘", "'")
        .replace("Ă˘â‚¬Ĺ“", '"')
        .replace("Ă˘â‚¬ĹĄ", '"')
        .replace("Ă˘â‚¬â€ť", "-")
    )


def _clean_excerpt(text: str) -> str:
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = (
        text.replace("A scenda n t/Midbea ven", "Ascendant/Midheaven")
        .replace("Fiyde", "Hyde")
        .replace("Somehow people", "Some people")
        .replace("SomeSIGNIFICANT MIDPOINTS 63 how", "Somehow")
        .replace("around-and", "around - and")
        .replace("relationships-whether", "relationships - whether")
        .replace("symbiotic-and", "symbiotic - and")
        .replace("synergistic-relationship", "synergistic - relationship")
        .replace("people-and", "people - and")
    )
    text = re.sub(r",\d+\b", "", text)
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def _extract_block(spec: dict[str, object], pdf_path: Path) -> SourceBlock:
    start_page, end_page = spec["pages"]
    raw_text = _normalized_pages(pdf_path, start_page, end_page)
    search_text = _clean_excerpt(raw_text)
    pattern = re.compile(
        rf"{re.escape(spec['start_marker'])}\s*(.*?){re.escape(spec['stop_marker'])}",
        re.S,
    )
    match = pattern.search(search_text)
    if match is None:
        raise ValueError(f"Could not extract McBroom block for {spec['slug']}")
    text = _clean_excerpt(match.group(1))
    return SourceBlock(
        page_type=str(spec["page_type"]),
        slug=str(spec["slug"]),
        source_heading=str(spec["source_heading"]),
        page=int(start_page),
        text=text,
    )


def generate_models(pdf_path: Path) -> list[SourceBlock]:
    return [_extract_block(spec, pdf_path) for spec in SECTION_SPECS]
