from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import re

import fitz


PDF_START_PAGE = 8
FACTOR_KEYWORD_PAGE = 7
PAGE_WIDTH_SPLIT = 500

FACTOR_SEQUENCE = [
    "Vernal Point",
    "MC",
    "Asc",
    "Sun",
    "Moon",
    "Node",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Cupido",
    "Hades",
    "Zeus",
    "Kronos",
    "Apollon",
    "Admetos",
    "Vulcanus",
    "Poseidon",
]

LEFT_ENTRY_FACTORS = FACTOR_SEQUENCE[:10]
RIGHT_ENTRY_FACTORS = FACTOR_SEQUENCE[10:]
AXIS_PAIRS = list(combinations(FACTOR_SEQUENCE, 2))

SOURCE_FACTOR_HEADINGS = {
    "Widder, WI": "Vernal Point",
    "Meridian, MC": "MC",
    "Aszendent, AS": "Asc",
    "Sonne, SO": "Sun",
    "Mond, MO": "Moon",
    "Mondknoten, KN": "Node",
    "Merkur, ME": "Mercury",
    "Venus, VE": "Venus",
    "Mars, MA": "Mars",
    "Jupiter, JU": "Jupiter",
    "Saturn, SA": "Saturn",
    "Uranus, UR": "Uranus",
    "Neptun, NE": "Neptune",
    "Pluto, PL": "Pluto",
    "Cupido, CU": "Cupido",
    "Hades, HA": "Hades",
    "Zeus, ZE": "Zeus",
    "Kronos, KR": "Kronos",
    "Apollon, AP": "Apollon",
    "Admetos, AD": "Admetos",
    "Vulkanus, VU": "Vulcanus",
    "Poseidon, PO": "Poseidon",
}

SOURCE_FACTOR_NAMES = {
    "Vernal Point": "Widder",
    "MC": "Meridian",
    "Asc": "Aszendent",
    "Sun": "Sonne",
    "Moon": "Mond",
    "Node": "Mondknoten",
    "Mercury": "Merkur",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
    "Uranus": "Uranus",
    "Neptune": "Neptun",
    "Pluto": "Pluto",
    "Cupido": "Cupido",
    "Hades": "Hades",
    "Zeus": "Zeus",
    "Kronos": "Kronos",
    "Apollon": "Apollon",
    "Admetos": "Admetos",
    "Vulcanus": "Vulkanus",
    "Poseidon": "Poseidon",
}


@dataclass(frozen=True)
class LineRecord:
    pdf_page: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


@dataclass(frozen=True)
class FactorBlock:
    factor: str
    source_heading: str
    page: int
    text: str


@dataclass(frozen=True)
class ActivationEntry:
    activated_by: str
    token: str
    text: str
    page: int


@dataclass(frozen=True)
class AxisBlock:
    factor_a: str
    factor_b: str
    source_heading: str
    pdf_page: int
    page_range: str
    page: int
    summary: str
    activation_entries: list[ActivationEntry]


@dataclass(frozen=True)
class RawEntry:
    token: str
    text: str


def source_factor_name(factor: str) -> str:
    return SOURCE_FACTOR_NAMES[factor]


def source_axis_heading(factor_a: str, factor_b: str) -> str:
    return f"{source_factor_name(factor_a)} + {source_factor_name(factor_b)}"


def _clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    text = text.replace("A llgemeinheit", "Allgemeinheit")
    return " ".join(text.split())


def _join_lines(lines: list[str]) -> str:
    buffer: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if buffer and buffer[-1].endswith("-"):
            buffer[-1] = buffer[-1][:-1] + stripped
            continue
        buffer.append(stripped)
    text = " ".join(buffer)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip()


@lru_cache(maxsize=None)
def _extract_line_records(pdf_path: Path) -> tuple[LineRecord, ...]:
    doc = fitz.open(pdf_path)
    records: list[LineRecord] = []
    for page_index, page in enumerate(doc, start=1):
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = _clean_text("".join(span["text"] for span in spans))
                if not text:
                    continue
                records.append(
                    LineRecord(
                        pdf_page=page_index,
                        x0=min(span["bbox"][0] for span in spans),
                        y0=min(span["bbox"][1] for span in spans),
                        x1=max(span["bbox"][2] for span in spans),
                        y1=max(span["bbox"][3] for span in spans),
                        text=text,
                    )
                )
    return tuple(records)


def _records_for_page(records: tuple[LineRecord, ...], pdf_page: int) -> list[LineRecord]:
    return [record for record in records if record.pdf_page == pdf_page]


def _fallback_left_printed_page(pdf_page: int) -> int:
    return pdf_page * 2 + 2


def _printed_pages(page_records: list[LineRecord], pdf_page: int) -> tuple[int, int]:
    left: int | None = None
    right: int | None = None
    for record in page_records:
        stripped = record.text.strip()
        if record.y0 < 650 or not stripped.isdigit():
            continue
        if record.x0 < PAGE_WIDTH_SPLIT:
            left = int(stripped)
        else:
            right = int(stripped)
    if left is None:
        left = _fallback_left_printed_page(pdf_page)
    if right is None:
        right = left + 1
    return left, right


def _is_page_number(record: LineRecord) -> bool:
    return record.y0 > 650 and record.text.strip().isdigit()


def _is_noise(record: LineRecord, side: str) -> bool:
    compact = record.text.replace(" ", "")
    if _is_page_number(record):
        return True
    if compact in {"I", "|"} and (record.y1 - record.y0) > 40:
        return True
    if record.y0 > 640 and len(compact) <= 3:
        return True
    if side == "left" and record.x0 > 500 and len(compact) <= 3:
        return True
    if side == "right" and record.x0 > 900 and len(compact) <= 3:
        return True
    return False


def _side_records(page_records: list[LineRecord], side: str) -> list[LineRecord]:
    selected = []
    for record in page_records:
        if side == "left" and record.x0 >= PAGE_WIDTH_SPLIT:
            continue
        if side == "right" and record.x0 < PAGE_WIDTH_SPLIT:
            continue
        if _is_noise(record, side):
            continue
        selected.append(record)
    return sorted(selected, key=lambda record: (record.y0, record.x0))


def _column_edge(records: list[LineRecord]) -> float | None:
    if not records:
        return None
    x_positions = sorted(record.x0 for record in records)
    for index, x0 in enumerate(x_positions[:-1]):
        if index < 4 and x_positions[index + 1] - x0 > 20:
            return x_positions[index + 1]
    return x_positions[0]


def _entry_start(record: LineRecord, side: str, threshold: float | None = None) -> tuple[str, str] | None:
    if threshold is None:
        threshold = 76 if side == "left" else 580
    if record.x0 > threshold:
        return None
    raw = record.text.strip()
    if not raw:
        return None
    parts = raw.split(maxsplit=1)
    token = parts[0].strip()
    opening = parts[1].strip() if len(parts) > 1 else ""
    normalized_token = token.strip(".,;:!?-'’`´·")
    checked_token = re.sub(r"[.'’`´·-]", "", normalized_token) or normalized_token
    if checked_token.isalpha():
        if len(checked_token) > 2 and not (len(checked_token) <= 3 and checked_token.isupper()):
            return None
        if len(checked_token) == 2 and not (
            checked_token.isupper() or checked_token in {"Ct", "cb", "cf", "lJ", "lf"}
        ):
            return None
    if checked_token.isalnum() and len(checked_token) > 3:
        return None
    if len(checked_token) > 4:
        return None
    return normalized_token, opening


def _parse_entry_side_by_bands(
    records: list[LineRecord],
    side: str,
    factors: list[str],
    axis_factors: set[str],
    allow_summary: bool,
    detected_starts: list[float],
    column_edge: float | None,
) -> tuple[str, list[RawEntry]]:
    if not records:
        return "", [RawEntry(token="", text="siehe oben" if factor in axis_factors else "") for factor in factors]

    if detected_starts:
        first_start = detected_starts[0]
        gaps = [
            detected_starts[index + 1] - detected_starts[index]
            for index in range(len(detected_starts) - 1)
            if 35 <= detected_starts[index + 1] - detected_starts[index] <= 80
        ]
        row_gap = sum(gaps) / len(gaps) if gaps else 55
    else:
        first_start = min(record.y0 for record in records)
        row_gap = 55

    starts = [first_start + row_gap * index for index in range(len(factors))]
    lower_bound = starts[0] - row_gap / 2
    upper_bound = starts[-1] + row_gap / 2
    summary_parts: list[str] = []
    rows: list[list[LineRecord]] = [[] for _factor in factors]

    for record in records:
        if column_edge is not None and record.x0 < column_edge - 8:
            continue
        if record.y0 < lower_bound:
            if allow_summary:
                summary_parts.append(record.text)
            continue
        if record.y0 >= upper_bound:
            continue
        row_index = min(
            range(len(starts)),
            key=lambda index: abs(record.y0 - starts[index]),
        )
        rows[row_index].append(record)

    raw_entries: list[RawEntry] = []
    for factor, row_records in zip(factors, rows):
        parts: list[str] = []
        for record in sorted(row_records, key=lambda item: (item.y0, item.x0)):
            start = _entry_start(record, side, record.x0)
            if start is not None:
                _token, opening = start
                if opening:
                    parts.append(opening)
                continue
            parts.append(record.text)
        text = _join_lines(parts)
        if not text and factor in axis_factors:
            text = "siehe oben"
        raw_entries.append(RawEntry(token="", text=text))

    return _join_lines(summary_parts), raw_entries


def _parse_entry_side(
    records: list[LineRecord],
    side: str,
    factors: list[str],
    axis_factors: set[str],
    allow_summary: bool = False,
) -> tuple[str, list[RawEntry]]:
    summary_parts: list[str] = []
    entries: list[tuple[str, list[str], float]] = []
    current: tuple[str, list[str], float] | None = None
    seen_entries = False
    column_edge = _column_edge(records)
    entry_threshold = column_edge + 12 if column_edge is not None else None
    detected_starts: list[float] = []

    for record in records:
        if column_edge is not None and record.x0 < column_edge - 8:
            continue
        start = _entry_start(record, side, entry_threshold)
        if start is not None:
            if current is not None:
                entries.append(current)
            token, opening = start
            current = (token, [opening] if opening else [], record.y0)
            detected_starts.append(record.y0)
            seen_entries = True
            continue
        if seen_entries:
            if current is not None:
                current[1].append(record.text)
        elif allow_summary:
            summary_parts.append(record.text)

    if current is not None:
        entries.append(current)

    expected_count = len(factors)
    if len(entries) < expected_count:
        missing_positions = [index for index, factor in enumerate(factors) if factor in axis_factors]
        missing_count = expected_count - len(entries)
        if missing_count == len(missing_positions):
            raw_entries = [
                RawEntry(token=token, text=_join_lines(parts))
                for token, parts, _start_y in entries
            ]
            for position in missing_positions:
                raw_entries.insert(position, RawEntry(token="", text="siehe oben"))
            return _join_lines(summary_parts), raw_entries

    if len(entries) != expected_count:
        band_summary, band_entries = _parse_entry_side_by_bands(
            records=records,
            side=side,
            factors=factors,
            axis_factors=axis_factors,
            allow_summary=allow_summary,
            detected_starts=detected_starts,
            column_edge=column_edge,
        )
        if len(band_entries) == expected_count:
            return band_summary, band_entries

    if len(entries) != expected_count:
        tokens = [token for token, _parts, _start_y in entries]
        raise ValueError(
            f"PDF side {side} yielded {len(entries)} entries, expected {expected_count}; tokens={tokens}"
        )

    return _join_lines(summary_parts), [
        RawEntry(token=token, text=_join_lines(parts))
        for token, parts, _start_y in entries
    ]


def parse_factor_blocks(pdf_path: Path) -> tuple[FactorBlock, ...]:
    records = _extract_line_records(Path(pdf_path))
    page_records = _records_for_page(records, FACTOR_KEYWORD_PAGE)
    left_page, right_page = _printed_pages(page_records, FACTOR_KEYWORD_PAGE)
    parsed: dict[str, FactorBlock] = {}

    for side, printed_page in (("left", left_page), ("right", right_page)):
        current_factor: str | None = None
        current_heading: str | None = None
        current_parts: list[str] = []
        for record in _side_records(page_records, side):
            if record.text.startswith("- "):
                continue
            heading = next(
                (
                    marker
                    for marker in SOURCE_FACTOR_HEADINGS
                    if marker.casefold() in record.text.casefold()
                ),
                None,
            )
            if heading is not None:
                if current_factor is not None and current_heading is not None:
                    parsed[current_factor] = FactorBlock(
                        factor=current_factor,
                        source_heading=current_heading,
                        page=printed_page,
                        text=_join_lines(current_parts),
                    )
                current_factor = SOURCE_FACTOR_HEADINGS[heading]
                current_heading = heading
                current_parts = []
                continue
            if current_factor is not None:
                current_parts.append(record.text)
        if current_factor is not None and current_heading is not None:
            parsed[current_factor] = FactorBlock(
                factor=current_factor,
                source_heading=current_heading,
                page=printed_page,
                text=_join_lines(current_parts),
            )

    missing = [factor for factor in FACTOR_SEQUENCE if factor not in parsed]
    if missing:
        raise ValueError(f"missing factor keyword entries: {missing}")
    return tuple(parsed[factor] for factor in FACTOR_SEQUENCE)


def _parse_axis_page(pdf_path: Path, pdf_page: int, factor_a: str, factor_b: str) -> AxisBlock:
    records = _extract_line_records(Path(pdf_path))
    page_records = _records_for_page(records, pdf_page)
    left_page, right_page = _printed_pages(page_records, pdf_page)
    summary, left_entries = _parse_entry_side(
        _side_records(page_records, "left"),
        "left",
        factors=LEFT_ENTRY_FACTORS,
        axis_factors={factor_a, factor_b},
        allow_summary=True,
    )
    _right_summary, right_entries = _parse_entry_side(
        _side_records(page_records, "right"),
        "right",
        factors=RIGHT_ENTRY_FACTORS,
        axis_factors={factor_a, factor_b},
        allow_summary=False,
    )

    activation_entries: list[ActivationEntry] = []
    for factor, raw_entry in zip(LEFT_ENTRY_FACTORS, left_entries):
        if factor in {factor_a, factor_b}:
            continue
        activation_entries.append(
            ActivationEntry(
                activated_by=factor,
                token=raw_entry.token,
                text=raw_entry.text,
                page=left_page,
            )
        )
    for factor, raw_entry in zip(RIGHT_ENTRY_FACTORS, right_entries):
        if factor in {factor_a, factor_b}:
            continue
        activation_entries.append(
            ActivationEntry(
                activated_by=factor,
                token=raw_entry.token,
                text=raw_entry.text,
                page=right_page,
            )
        )

    return AxisBlock(
        factor_a=factor_a,
        factor_b=factor_b,
        source_heading=source_axis_heading(factor_a, factor_b),
        pdf_page=pdf_page,
        page_range=f"{left_page}-{right_page}",
        page=left_page,
        summary=summary,
        activation_entries=activation_entries,
    )


def parse_axis_blocks(pdf_path: Path) -> tuple[AxisBlock, ...]:
    path = Path(pdf_path)
    return tuple(
        _parse_axis_page(path, PDF_START_PAGE + index, factor_a, factor_b)
        for index, (factor_a, factor_b) in enumerate(AXIS_PAIRS)
    )


@lru_cache(maxsize=None)
def generate_models(pdf_path: Path) -> tuple[tuple[FactorBlock, ...], tuple[AxisBlock, ...]]:
    path = Path(pdf_path)
    return parse_factor_blocks(path), parse_axis_blocks(path)
