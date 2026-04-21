from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
import shutil

import fitz
from PIL import Image
import pytesseract

from tools.wiki_identity import normalize_axis


FACTOR_SEQUENCE = [
    "Aries",
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

PAIR_HEADING_NAMES = {
    "ARIES": "Aries",
    "MERIDIAN": "MC",
    "ASCENDANT": "Asc",
    "SUN": "Sun",
    "MOON": "Moon",
    "LUNAR NODES": "Node",
    "NODES": "Node",
    "NODE": "Node",
    "MERCURY": "Mercury",
    "VENUS": "Venus",
    "MARS": "Mars",
    "JUPITER": "Jupiter",
    "SATURN": "Saturn",
    "URANUS": "Uranus",
    "NEPTUNE": "Neptune",
    "PLUTO": "Pluto",
    "CUPIDO": "Cupido",
    "HADES": "Hades",
    "ZEUS": "Zeus",
    "KRONOS": "Kronos",
    "APOLLON": "Apollon",
    "ADMETOS": "Admetos",
    "VULCANUS": "Vulcanus",
    "POSEIDON": "Poseidon",
}

PAIR_HEADING_PATTERN = re.compile(
    r"^(?P<left>LUNAR NODES|MERIDIAN|ASCENDANT|APOLLON|ADMETOS|VULCANUS|POSEIDON|JUPITER|SATURN|URANUS|NEPTUNE|MERCURY|CUPIDO|KRONOS|HADES|ARIES|VENUS|PLUTO|ZEUS|MARS|MOON|NODES|NODE|SUN)\s*\+\s*(?P<right>LUNAR NODES|MERIDIAN|ASCENDANT|APOLLON|ADMETOS|VULCANUS|POSEIDON|JUPITER|SATURN|URANUS|NEPTUNE|MERCURY|CUPIDO|KRONOS|HADES|ARIES|VENUS|PLUTO|ZEUS|MARS|MOON|NODES|NODE|SUN)$"
)

FACTOR_HEADINGS = [
    ("Aries", ("ARIES, ARIES POINT",)),
    ("MC", ("MERIDIAN, MC",)),
    ("Asc", ("ASCENDANT, AS",)),
    ("Sun", ("SUN, SU",)),
    ("Moon", ("MOON, MO",)),
    ("Node", ("LUNAR NODES, NO", "LUNAR NODE, NO")),
    ("Mercury", ("MERCURY, ME",)),
    ("Venus", ("VENUS, VE",)),
    ("Mars", ("MARS, MA",)),
    ("Jupiter", ("JUPITER, JU",)),
    ("Saturn", ("SATURN, SA",)),
    ("Uranus", ("URANUS, UR",)),
    ("Neptune", ("NEPTUNE, NE",)),
    ("Pluto", ("PLUTO, PL", "PIUTO, PL")),
    ("Cupido", ("CUPIDO, CU",)),
    ("Hades", ("HADES, HA",)),
    ("Zeus", ("ZEUS, ZE",)),
    ("Kronos", ("KRONOS, KR",)),
    ("Apollon", ("APOLLON, AP",)),
    ("Admetos", ("ADMETOS, AD",)),
    ("Vulcanus", ("VULCANUS, VU",)),
    ("Poseidon", ("POSEIDON, PO",)),
]

FACTOR_SECTION_SKIP_LINES = {
    "Meaning of the Factors and Planets",
    "Meaning of the hypothetical Planets",
    "Alfred Witte",
    "Friedrich Sieggriin",
    "Friedrich Sieggrun",
}

FACTOR_SECTION_END_HEADINGS = {
    "Meaning of the Houses",
}

BODY_STARTERS = {
    "A",
    "An",
    "Being",
    "Body",
    "Connections",
    "Deep",
    "Developments",
    "Education",
    "General",
    "Good",
    "Great",
    "Happiness",
    "Harmonious",
    "Ideas",
    "Knowledge",
    "Life",
    "Men",
    "Mental",
    "One",
    "One's",
    "One’s",
    "People",
    "Power",
    "Professional",
    "Spirit",
    "Sudden",
    "Success",
    "The",
    "Thoughts",
    "To",
    "Women",
}

ALLOWED_ALPHA_TOKENS = {
    "ffr",
    "iff",
}

COMMON_NO_MARKER_WORDS = {
    "a",
    "and",
    "as",
    "at",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "up",
    "with",
    "www.",
}


@dataclass(frozen=True)
class LineRecord:
    page: int
    x0: float
    y0: float
    text: str


@dataclass(frozen=True)
class FactorBlock:
    factor: str
    page: int
    text: str


@dataclass(frozen=True)
class ActivationEntry:
    activated_by: str
    token: str
    text: str
    page: int


@dataclass(frozen=True)
class PairBlock:
    factor_a: str
    factor_b: str
    source_heading: str
    page: int
    summary: str
    activation_entries: list[ActivationEntry]


PAIR_ENTRY_OVERRIDES: dict[tuple[str, str, str], dict[str, object]] = {
    (
        "Kronos",
        "Vulcanus",
        "Pluto",
    ): {
        "text": "Changes and development of the form of government. Reorganization of the state. Changes and transformations in relation to great powers."
    },
    (
        "Aries",
        "Aries",
        "Poseidon",
    ): {
        "text": "Ideas, spirit, education, cognition, understanding and culture in the general public. Water masses or great floods on Earth. Worlds awareness. The world of the civilized."
    },
    (
        "Poseidon",
        "Poseidon",
        "Apollon",
    ): {
        "text": "People with the same mindset. Congenial. Companions of destiny. Fellow sufferers, comrades. Comradeship. Disposition (way of thinking). Spreading of ideas. Insights through experience. People with similar outlook on life. Spiritual science. Humanities. Theological insights."
    },
    (
        "Poseidon",
        "Poseidon",
        "Admetos",
    ): {
        "text": "Creative education. Mental depth. Fine, subtle material. The atom. Radiation, irradiation. Dematerialization. Spirit and matter. The two sides of the same entity.",
        "page": 317,
        "token": "",
    },
    (
        "Poseidon",
        "Poseidon",
        "Vulcanus",
    ): {
        "text": "State of mind. Sense of honor. Self-esteem. Self-confidence. Pride. Dignity. Arrogance. The mental influence, power and forces. The powerful mind. The spiritual power.",
        "page": 317,
        "token": "",
    },
}


def _clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    return " ".join(text.split())


def _is_footer(text: str, x0: float) -> bool:
    if not text:
        return True
    if text.startswith("RULES FOR PLANETARY PICTURES"):
        return True
    if x0 > 500:
        return True
    if text.isdigit() and len(text) <= 3:
        return True
    return False


def _is_bottom_page_noise(text: str, x0: float, y0: float) -> bool:
    compact = text.replace(" ", "")
    if y0 <= 760:
        return False
    return len(compact) == 1 and (x0 < 30 or x0 > 400)


def _is_top_page_noise(text: str, y0: float) -> bool:
    compact = text.replace(" ", "")
    if y0 >= 30:
        return False
    return len(compact) == 1


def _is_margin_noise(text: str, x0: float) -> bool:
    compact = text.replace(" ", "")
    if len(compact) > 4:
        return False
    if x0 < 40 and compact in {".", ",", ":", ";"}:
        return True
    if x0 < 25:
        return True
    if x0 > 400:
        return True
    return False


def _is_inline_garble(text: str, x0: float) -> bool:
    if x0 < 200:
        return False
    if "/" not in text and "\\" not in text:
        return False
    return sum(character.isalpha() for character in text) < 8


def _is_short_symbol_header(text: str, y0: float) -> bool:
    compact = text.replace(" ", "")
    if y0 > 50:
        return False
    if len(compact) > 6:
        return False
    if any(character.islower() for character in compact):
        return False
    if compact.isdigit():
        return False
    return _parse_pair_heading(text) is None


@lru_cache(maxsize=None)
def _extract_line_records(pdf_path: Path) -> tuple[LineRecord, ...]:
    doc = fitz.open(pdf_path)
    records: list[LineRecord] = []
    for page_number in range(doc.page_count):
        data = doc[page_number].get_text("dict")
        for block in data["blocks"]:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = _clean_text("".join(span["text"] for span in spans))
                if not text:
                    continue
                x0 = min(span["bbox"][0] for span in spans)
                y0 = min(span["bbox"][1] for span in spans)
                if _is_footer(text, x0):
                    continue
                if _is_bottom_page_noise(text, x0, y0):
                    continue
                if _is_top_page_noise(text, y0):
                    continue
                if _is_margin_noise(text, x0):
                    continue
                if _is_inline_garble(text, x0):
                    continue
                if _is_short_symbol_header(text, y0):
                    continue
                records.append(LineRecord(page=page_number + 1, x0=x0, y0=y0, text=text))
    return tuple(records)


def _parse_pair_heading(text: str) -> tuple[str, str] | None:
    match = PAIR_HEADING_PATTERN.match(text.upper())
    if match is None:
        return None
    return (
        PAIR_HEADING_NAMES[match.group("left")],
        PAIR_HEADING_NAMES[match.group("right")],
    )


def _is_symbol_heading_line(text: str) -> bool:
    return "+" in text and len(text) <= 10 and _parse_pair_heading(text) is None


def _parse_factor_heading(text: str) -> str | None:
    upper = text.upper()
    for factor, markers in FACTOR_HEADINGS:
        if any(marker in upper for marker in markers):
            return factor
    return None


def _is_factor_section_skip_line(text: str) -> bool:
    return text.strip() in FACTOR_SECTION_SKIP_LINES


def _is_factor_section_end_heading(text: str) -> bool:
    return text.strip() in FACTOR_SECTION_END_HEADINGS


@lru_cache(maxsize=1)
def _resolve_tesseract_cmd() -> str | None:
    found = shutil.which("tesseract")
    if found:
        return found
    default_path = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
    if default_path.exists():
        return str(default_path)
    return None


@lru_cache(maxsize=None)
def _extract_ocr_line_records(pdf_path: Path, page_number: int) -> tuple[LineRecord, ...]:
    tesseract_cmd = _resolve_tesseract_cmd()
    if tesseract_cmd is None:
        return ()

    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    data = pytesseract.image_to_data(
        image,
        lang="eng",
        config="--psm 6",
        output_type=pytesseract.Output.DICT,
    )

    grouped: dict[tuple[int, int, int], list[int]] = {}
    for index, text in enumerate(data["text"]):
        if not text.strip():
            continue
        key = (data["block_num"][index], data["par_num"][index], data["line_num"][index])
        grouped.setdefault(key, []).append(index)

    records: list[LineRecord] = []
    for key in sorted(grouped):
        indices = grouped[key]
        text = _clean_text(" ".join(data["text"][index].strip() for index in indices if data["text"][index].strip()))
        if not text:
            continue
        x0 = min(data["left"][index] for index in indices) / 2
        y0 = min(data["top"][index] for index in indices) / 2
        compact = text.replace(" ", "")
        if x0 > 250 and len(compact) <= 4:
            continue
        if _is_footer(text, x0):
            continue
        if _is_bottom_page_noise(text, x0, y0):
            continue
        if _is_top_page_noise(text, y0):
            continue
        if _is_margin_noise(text, x0):
            continue
        if _is_inline_garble(text, x0):
            continue
        if _is_short_symbol_header(text, y0):
            continue
        if _parse_pair_heading(text) is not None:
            continue
        if x0 < 25 and text[0] in ",.;:":
            x0 = 90
        if text[0].islower():
            x0 = max(x0, 90)
        records.append(LineRecord(page=page_number, x0=x0, y0=y0, text=text))
    return tuple(sorted(records, key=lambda record: (record.y0, record.x0)))


def _entry_start(record: LineRecord, allow_alpha: bool = False) -> tuple[str, str] | None:
    raw = record.text.strip()
    candidate = raw.lstrip("-•■*~'\"“”‘’").strip()
    if not candidate:
        return None
    has_leading_marker = candidate != raw
    if record.x0 > (85 if has_leading_marker else 78):
        return None
    parts = candidate.split()
    first = parts[0]
    if not allow_alpha and raw[0].isalpha() and candidate[0].isalpha():
        second = parts[1] if len(parts) > 1 else ""
        if (
            record.x0 >= 60
            or not second
            or not second[0].isupper()
            or len(first) > 2
            or first.islower()
            or (len(first) > 1 and first in BODY_STARTERS)
        ):
            return None
    if has_leading_marker and (len(first) > 4 or (len(first) > 1 and first in BODY_STARTERS)):
        opening = candidate
        return ("?", opening)
    if not has_leading_marker:
        second = parts[1].casefold() if len(parts) > 1 else ""
        if first == first.lower() and first.casefold() in COMMON_NO_MARKER_WORDS:
            return None
        if first == first.lower() and first.casefold() == "up" and second == "of":
            return None
    if len(first) > 1 and first in BODY_STARTERS:
        return None
    if first.isalpha() and len(first) > 3:
        return None
    if first.isalpha() and len(first) == 3 and first.islower() and first.casefold() not in ALLOWED_ALPHA_TOKENS:
        return None
    if len(parts) == 1 and len(parts[0]) <= 4:
        return (parts[0], "")
    if len(parts[0]) <= 4:
        if len(parts) >= 3 and len(parts[1]) <= 2 and (
            parts[1].islower() or not parts[1].isalpha() or parts[2] in BODY_STARTERS
        ):
            return (f"{parts[0]} {parts[1]}", " ".join(parts[2:]))
        if len(parts) >= 2:
            return (parts[0], " ".join(parts[1:]))
    return None


def _join_parts(parts: list[str]) -> str:
    text = " ".join(part.strip() for part in parts if part.strip()).strip()
    text = re.sub(r"\s+[^\w\s]\s+(?=[a-z])", " ", text)
    text = re.sub(r"([.!?])(?:\s+[A-Za-z0-9]{1,2})+$", r"\1", text)
    return text


def _text_quality_score(text: str) -> int:
    stripped = text.strip()
    letters = sum(character.isalpha() for character in stripped)
    noise = sum(character in "\\|_^~" for character in stripped)
    if re.search(r"[A-Za-z]\^-[A-Za-z]", stripped):
        noise += 3
    if re.search(r"\b[a-z](?:\s+[A-Z]){1,2}$", stripped):
        noise += 3
    if stripped and stripped[-1] not in ".!?":
        noise += 1
    return letters - noise * 5


def _pair_block_needs_ocr_merge(block: PairBlock) -> bool:
    texts = [block.summary, *(entry.text for entry in block.activation_entries)]
    patterns = (
        r"[A-Za-z]\^-[A-Za-z]",
        r"\b[a-z](?:\s+[A-Z]){1,2}$",
        r"\\",
    )
    return any(re.search(pattern, text) for text in texts for pattern in patterns)


def _merge_pair_blocks(primary: PairBlock, secondary: PairBlock) -> PairBlock:
    merged_entries: list[ActivationEntry] = []
    for primary_entry, secondary_entry in zip(primary.activation_entries, secondary.activation_entries):
        use_secondary = _text_quality_score(secondary_entry.text) > _text_quality_score(primary_entry.text)
        merged_entries.append(
            ActivationEntry(
                activated_by=primary_entry.activated_by,
                token=primary_entry.token,
                text=secondary_entry.text if use_secondary else primary_entry.text,
                page=primary_entry.page,
            )
        )
    use_secondary_summary = _text_quality_score(secondary.summary) > _text_quality_score(primary.summary)
    return PairBlock(
        factor_a=primary.factor_a,
        factor_b=primary.factor_b,
        source_heading=primary.source_heading,
        page=primary.page,
        summary=secondary.summary if use_secondary_summary else primary.summary,
        activation_entries=merged_entries,
    )


def _apply_pair_entry_overrides(block: PairBlock) -> PairBlock:
    entries: list[ActivationEntry] = []
    changed = False
    for entry in block.activation_entries:
        override = PAIR_ENTRY_OVERRIDES.get((block.factor_a, block.factor_b, entry.activated_by))
        if override is None:
            entries.append(entry)
            continue
        changed = True
        entries.append(
            ActivationEntry(
                activated_by=entry.activated_by,
                token=str(override.get("token", entry.token)),
                text=str(override["text"]),
                page=int(override.get("page", entry.page)),
            )
        )
    if not changed:
        return block
    return PairBlock(
        factor_a=block.factor_a,
        factor_b=block.factor_b,
        source_heading=block.source_heading,
        page=block.page,
        summary=block.summary,
        activation_entries=entries,
    )


def _placeholder_marker(record: LineRecord, next_record: LineRecord | None) -> bool:
    compact = record.text.replace(" ", "")
    if not compact or len(compact) > 2:
        return False
    if re.fullmatch(r"[^\w]+", compact) is None:
        return False
    if next_record is None:
        return False
    return next_record.x0 >= 74


def _promote_first_entry_after_summary(
    summary_records: list[LineRecord],
    record: LineRecord,
) -> tuple[str, str] | None:
    if not summary_records:
        return None
    previous = summary_records[-1]
    if previous.x0 - record.x0 < 80:
        return None
    if record.x0 > 75:
        return None
    raw = record.text.strip()
    if not raw or not raw[0].isupper():
        return None
    return ("?", raw)


def _repair_missing_entries(
    entries: list[tuple[str, int, list[str], list[LineRecord]]],
    expected_count: int,
    allow_text_layer_repairs: bool = True,
) -> list[tuple[str, int, list[str], list[LineRecord]]]:
    repaired = list(entries)
    split_starters = (
        "To ",
        "Patience.",
        "Being ",
        "General ",
        "Life ",
        "Great ",
        "Depressed ",
        "Thoughts",
        "The mental ",
        "Mental ",
        "Marriage",
        "Power",
        "Knowledge",
        "Education",
        "Ethics ",
        "Union ",
        "Spirit",
        "Spiritualized ",
        "Spiritualization ",
        "Spiritual matter",
        "Body",
        "People",
        "Women",
        "Men",
        "Matrimony ",
        "Connections",
        "Community",
        "Dissonances",
        "Dirty ",
        "Experience ",
        "Ideas",
        "Property",
        "Poverty ",
        "Happiness",
    )
    if allow_text_layer_repairs:
        for index in range(len(repaired) - 1):
            token, page, parts, records = repaired[index]
            next_token, next_page, next_parts, next_records = repaired[index + 1]
            if parts or not next_parts:
                continue
            next_offset = len(next_records) - len(next_parts)
            if not 74 <= next_records[next_offset].x0 <= 85:
                continue
            repaired[index] = (token, page, [next_parts[0]], [next_records[next_offset]])
            repaired[index + 1] = (
                next_token,
                next_page,
                next_parts[1:],
                next_records[:next_offset] + next_records[next_offset + 1 :],
            )
    while len(repaired) < expected_count:
        split_done = False
        for index, (token, page, parts, records) in enumerate(repaired):
            if len(parts) < 2:
                continue
            record_offset = len(records) - len(parts)
            for split_index in range(1, len(parts)):
                previous = parts[split_index - 1]
                current = parts[split_index]
                current_record = records[record_offset + split_index]
                low_indent_starter = 68 <= current_record.x0 <= 80 and current.startswith(split_starters)
                if current_record.x0 <= 80 and not low_indent_starter:
                    continue
                if not previous.endswith("."):
                    continue
                if not current or not current[0].isupper():
                    continue
                if len(current.split()) == 1 and not current.startswith(split_starters):
                    continue
                if len(previous) > 55 and not current.startswith(split_starters):
                    continue
                if (
                    len(previous) > 40
                    and not current.startswith(split_starters)
                    and "." not in current
                ):
                    continue
                repaired[index : index + 1] = [
                    (token, page, parts[:split_index], records[: record_offset + split_index]),
                    ("?", current_record.page, parts[split_index:], records[record_offset + split_index :]),
                ]
                split_done = True
                break
            if split_done:
                break
        if allow_text_layer_repairs and not split_done and expected_count - len(repaired) >= 1:
            for index, (token, page, parts, records) in enumerate(repaired):
                if len(parts) < 2:
                    continue
                record_offset = len(records) - len(parts)
                for split_index in range(1, len(parts)):
                    previous = parts[split_index - 1]
                    current = parts[split_index]
                    current_record = records[record_offset + split_index]
                    if not 74 <= current_record.x0 <= 85:
                        continue
                    if not current.startswith(split_starters):
                        continue
                    if not previous.endswith(".") and not (
                        previous.endswith("Increasing") and current.startswith("Matrimony ")
                    ):
                        continue
                    if len(current.split()) == 1:
                        continue
                    repaired[index : index + 1] = [
                        (token, page, parts[:split_index], records[: record_offset + split_index]),
                        ("?", current_record.page, parts[split_index:], records[record_offset + split_index :]),
                    ]
                    split_done = True
                    break
                if split_done:
                    break
        if not split_done and expected_count - len(repaired) >= 4:
            for index, (token, page, parts, records) in enumerate(repaired):
                if len(parts) < 2:
                    continue
                entry_x0 = records[0].x0
                record_offset = len(records) - len(parts)
                for split_index in range(1, len(parts)):
                    previous = parts[split_index - 1]
                    current = parts[split_index]
                    current_record = records[record_offset + split_index]
                    if entry_x0 < 75 and current_record.x0 <= entry_x0 + 20:
                        continue
                    if not previous.endswith("."):
                        continue
                    if not current or not current[0].isupper():
                        continue
                    repaired[index : index + 1] = [
                        (token, page, parts[:split_index], records[: record_offset + split_index]),
                        ("?", current_record.page, parts[split_index:], records[record_offset + split_index :]),
                    ]
                    split_done = True
                    break
                if split_done:
                    break
        if not split_done:
            break
    return repaired


def _group_pair_pages(records: list[LineRecord]) -> list[dict]:
    blocks: list[dict] = []
    current: dict | None = None
    started = False
    for record in records:
        heading = _parse_pair_heading(record.text)
        if heading is not None:
            started = True
            if current is not None:
                blocks.append(current)
            current = {
                "factor_a": heading[0],
                "factor_b": heading[1],
                "page": record.page,
                "source_heading": f"{heading[0]} + {heading[1]}",
                "records": [],
            }
            continue
        if _is_symbol_heading_line(record.text):
            continue
        if not started:
            continue
        if current is not None:
            current["records"].append(record)
    if current is not None:
        blocks.append(current)
    return blocks


def _split_pair_block(block: dict, allow_text_layer_repairs: bool = True) -> PairBlock:
    summary_parts: list[str] = []
    summary_records: list[LineRecord] = []
    entries: list[tuple[str, int, list[str], list[LineRecord]]] = []
    current_entry: tuple[str, int, list[str], list[LineRecord]] | None = None
    seen_entries = False

    for index, record in enumerate(block["records"]):
        next_record = block["records"][index + 1] if index + 1 < len(block["records"]) else None
        entry = _entry_start(record, allow_alpha=seen_entries)
        if entry is None and _placeholder_marker(record, next_record):
            entry = ("?", "")
        if entry is None and not seen_entries:
            entry = _promote_first_entry_after_summary(summary_records, record)
        if entry is not None:
            token, opening = entry
            if current_entry is not None:
                entries.append(current_entry)
            current_entry = (
                token,
                record.page,
                [opening] if opening else [],
                [record],
            )
            seen_entries = True
            continue
        if seen_entries:
            if current_entry is None:
                continue
            current_entry[2].append(record.text)
            current_entry[3].append(record)
        else:
            summary_parts.append(record.text)
            summary_records.append(record)

    if current_entry is not None:
        entries.append(current_entry)

    expected_factors = [
        factor for factor in FACTOR_SEQUENCE if factor not in {block["factor_a"], block["factor_b"]}
    ]
    entries = _repair_missing_entries(
        entries,
        len(expected_factors),
        allow_text_layer_repairs=allow_text_layer_repairs,
    )
    if len(entries) != len(expected_factors):
        heading = normalize_axis(block["factor_a"], block["factor_b"]).display
        tokens = [token for token, _page, _parts, _records in entries]
        raise ValueError(
            f"{heading} on page {block['page']} yielded {len(entries)} entries, expected {len(expected_factors)}; tokens={tokens}"
        )

    activation_entries = [
        ActivationEntry(
            activated_by=factor,
            token=token,
            text=_join_parts(parts),
            page=page,
        )
        for factor, (token, page, parts, _records) in zip(expected_factors, entries)
    ]
    return PairBlock(
        factor_a=block["factor_a"],
        factor_b=block["factor_b"],
        source_heading=block["source_heading"],
        page=block["page"],
        summary=_join_parts(summary_parts),
        activation_entries=activation_entries,
    )


def _parse_pair_block(block: dict, pdf_path: Path) -> PairBlock:
    try:
        parsed = _split_pair_block(block, allow_text_layer_repairs=True)
    except ValueError as first_error:
        pages = sorted({record.page for record in block["records"]}) or [block["page"]]
        ocr_records = tuple(
            record
            for page in pages
            for record in _extract_ocr_line_records(pdf_path, page)
        )
        if not ocr_records:
            raise first_error
        ocr_block = dict(block)
        ocr_block["records"] = list(ocr_records)
        try:
            return _apply_pair_entry_overrides(
                _split_pair_block(ocr_block, allow_text_layer_repairs=len(pages) > 1)
            )
        except ValueError:
            raise first_error
    if not _pair_block_needs_ocr_merge(parsed):
        return _apply_pair_entry_overrides(parsed)
    pages = sorted({record.page for record in block["records"]}) or [block["page"]]
    ocr_records = tuple(
        record
        for page in pages
        for record in _extract_ocr_line_records(pdf_path, page)
    )
    if not ocr_records:
        return parsed
    ocr_block = dict(block)
    ocr_block["records"] = list(ocr_records)
    try:
        ocr_parsed = _split_pair_block(ocr_block, allow_text_layer_repairs=len(pages) > 1)
    except ValueError:
        return _apply_pair_entry_overrides(parsed)
    return _apply_pair_entry_overrides(_merge_pair_blocks(parsed, ocr_parsed))


@lru_cache(maxsize=None)
def parse_pair_blocks(pdf_path: Path) -> tuple[PairBlock, ...]:
    records = _extract_line_records(pdf_path)
    return tuple(_parse_pair_block(block, pdf_path) for block in _group_pair_pages(list(records)))


@lru_cache(maxsize=None)
def parse_factor_blocks(pdf_path: Path) -> tuple[FactorBlock, ...]:
    records = _extract_line_records(pdf_path)
    pair_start_page = min(block.page for block in parse_pair_blocks(pdf_path))
    blocks: list[FactorBlock] = []
    current_factor: str | None = None
    current_page: int | None = None
    current_lines: list[str] = []

    for record in records:
        if record.page >= pair_start_page:
            break
        if _is_factor_section_end_heading(record.text):
            break
        factor = _parse_factor_heading(record.text)
        if factor is not None:
            if current_factor is not None:
                blocks.append(
                    FactorBlock(
                        factor=current_factor,
                        page=current_page or record.page,
                        text=_join_parts(current_lines),
                    )
                )
            current_factor = factor
            current_page = record.page
            current_lines = []
            continue
        if current_factor is not None and not _is_factor_section_skip_line(record.text):
            current_lines.append(record.text)

    if current_factor is not None:
        blocks.append(FactorBlock(factor=current_factor, page=current_page or 0, text=_join_parts(current_lines)))

    return tuple(blocks)


@lru_cache(maxsize=None)
def generate_models(pdf_path: Path) -> tuple[tuple[FactorBlock, ...], tuple[PairBlock, ...]]:
    path = Path(pdf_path)
    return parse_factor_blocks(path), parse_pair_blocks(path)
