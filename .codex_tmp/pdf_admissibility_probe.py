#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

# --- How to run ---
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run pdf_admissibility_probe.py [ARGS]
# 3. Or make executable and run:
#      chmod +x pdf_admissibility_probe.py && ./pdf_admissibility_probe.py
# ------------------

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import fitz


ROOT = Path("W:/books references etc/!master list astro")
SNIPPET_RADIUS = 120


@dataclass(frozen=True, slots=True)
class SourcePdf:
    label: str
    path: Path


SOURCES = (
    SourcePdf(
        "Feist Lexicon",
        ROOT / "planetary expression - Michael Feist - Lexicon for Planetary Pictures.pdf",
    ),
    SourcePdf(
        "Uranian Master-Lexicon",
        ROOT / "planetary expressions - Uranian Astrology - Master-Lexicon v2_1.pdf",
    ),
    SourcePdf(
        "D.M. Baker Colloquialism",
        ROOT / "planetary expressions - D.M. Baker - Colloquialism.pdf",
    ),
    SourcePdf(
        "Aren Ober Midpoint Interpretation",
        ROOT / "midpoints - Aren Ober - Midpoint Interpretation.pdf",
    ),
    SourcePdf(
        "Hans Niggemann Rules",
        ROOT / "midpoints - Hans Niggemann - Rules for planetary pictures.pdf",
    ),
    SourcePdf(
        "Manly P. Hall Keywords",
        ROOT / "varia - Manly P Hall - Astrological Keywords.pdf",
    ),
    SourcePdf(
        "Harding Harvey Working with Astrology",
        ROOT
        / "harmonics - Michael Harding Charles Harvey - Working with astrology_harmonics, midpoints and Astro_Carto_Graphy.pdf",
    ),
    SourcePdf(
        "Zane Stein Quadrant Midpoints",
        ROOT / "midpoints - Zane B Stein The Quadrant Midpoints The Chart's Backbone.pdf",
    ),
)

SEARCH_TERMS = (
    "sun/moon",
    "sun / moon",
    "sun+moon",
    "moon/sun",
    "moon / sun",
    "jupiter/pluto",
    "jupiter / pluto",
    "venus/mars",
    "mars/venus",
    "midpoint",
    "mid-point",
    "planetary picture",
    "planetary pictures",
    "cupido",
    "hades",
    "zeus",
    "kronos",
    "apollon",
    "admetos",
    "vulkanus",
    "poseidon",
    "node",
    "ascendant",
    "m.c.",
    "mc",
)

FORMULA_RE = re.compile(
    r"(?i)(sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto|node|asc(?:endant)?|m\.?c\.?|cupido|hades|zeus|kronos|apollon|admetos|vulkanus|poseidon)"
    r"\s*(?:/|\+|=|-)\s*"
    r"(sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto|node|asc(?:endant)?|m\.?c\.?|cupido|hades|zeus|kronos|apollon|admetos|vulkanus|poseidon)"
)


def compact(text: str) -> str:
    return " ".join(text.split())


def snippet(text: str, start: int) -> str:
    first = max(0, start - SNIPPET_RADIUS)
    last = min(len(text), start + SNIPPET_RADIUS)
    return compact(text[first:last])


def interesting_snippets(text: str) -> list[str]:
    lowered = text.lower()
    snippets: list[str] = []
    for term in SEARCH_TERMS:
        position = lowered.find(term)
        if position >= 0:
            snippets.append(snippet(text, position))
    for match in FORMULA_RE.finditer(text):
        snippets.append(snippet(text, match.start()))
        if len(snippets) >= 5:
            break
    return snippets[:5]


def score_page(text: str) -> int:
    lowered = text.lower()
    term_hits = sum(lowered.count(term) for term in SEARCH_TERMS)
    formula_hits = len(FORMULA_RE.findall(text))
    return term_hits + (formula_hits * 3)


def print_source_summary(source: SourcePdf) -> None:
    print(f"\n## {source.label}")
    print(f"path: {source.path}")
    if not source.path.exists():
        print("missing")
        return
    with fitz.open(source.path) as doc:
        print(f"pages: {doc.page_count}")
        metadata = doc.metadata
        if metadata:
            title = metadata.get("title", "")
            author = metadata.get("author", "")
            print(f"metadata_title: {title}")
            print(f"metadata_author: {author}")
        page_scores: list[tuple[int, int, int, str]] = []
        first_text_pages: list[tuple[int, str]] = []
        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            text = page.get_text("text", sort=True)
            text_length = len(compact(text))
            if text_length > 0 and len(first_text_pages) < 3:
                first_text_pages.append((page_index + 1, compact(text)[:500]))
            page_score = score_page(text)
            if page_score > 0:
                page_scores.append((page_score, page_index + 1, text_length, text))
        print(f"text_pages_sampled: {len(first_text_pages)}")
        for page_number, sample in first_text_pages:
            print(f"first_text p{page_number}: {sample}")
        print("top_signal_pages:")
        for page_score, page_number, text_length, text in sorted(page_scores, reverse=True)[:12]:
            print(f"- p{page_number} score={page_score} chars={text_length}")
            for item in interesting_snippets(text):
                print(f"  snippet: {item}")


def main() -> None:
    for source in SOURCES:
        print_source_summary(source)


if __name__ == "__main__":
    main()
