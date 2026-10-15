from __future__ import annotations

# How to run:
# C:/pyMADMAX2/miniconda3/envs/deep11/python.exe .codex_tmp/ingest_banzhaf_haebler.py

from pathlib import Path
import re
import sys
from typing import Final, TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_identity import factor_slug, normalize_axis


UPDATED_AT: Final = "2026-06-20"
SOURCE_TITLE: Final = "Hajo Banzhaf and Anna Haebler - Keywords for Astrology"
SOURCE_SLUG: Final = "hajo-banzhaf-anna-haebler-keywords-for-astrology"
SOURCE_LINK: Final = f"- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)"
PDF_PATH: Final = "W:/books references etc/!master list astro/Keywords for Astrology Hajo Banzhaf and Anna Haebler 2024.pdf"


class FactorEntry(TypedDict):
    factor: str
    pages: str
    bullets: tuple[str, ...]


class PairEntry(TypedDict):
    axis_slug: str
    source_heading: str
    pages: str
    bullets: tuple[tuple[str, str], ...]


FACTOR_ENTRIES: Final[tuple[FactorEntry, ...]] = (
    {
        "factor": "Sun",
        "pages": "28-29",
        "bullets": (
            "Archetype: hero, father, king.",
            "Shadow: overbearing person, megalomaniac.",
            "Principle: intrinsic character, central concerns, path and goal, yang principle, consciousness, will, vital energy, creativity, self-realization, warmth, courage, and optimism.",
            "Strength: self-confident, lively, warm, magnanimous, creative, independent, and striking in personal presence.",
            "Problem area: inflated arrogance and self-aggrandizement, or weak-willed difficulty developing one's own essence.",
            "Goal: become what one is; seek wholeness, the inner center, true identity, and the hero's journey.",
            "Representatives: fathers, rulers, authorities, politicians, organizers, aristocracy; also egotists, tyrants, swindlers, and megalomaniacs.",
            "Physical correlations: heart, spinal cord, blood circulation, solar plexus, respiratory system.",
        ),
    },
    {
        "factor": "Moon",
        "pages": "30-32",
        "bullets": (
            "Archetype: mother, child.",
            "Shadow: the monster that devours everything.",
            "Principle: inner nature, feeling realm, unconscious, instinctive reactions, contact, closeness, security, home, memories, family, and mother-child experience.",
            "Strength: soulful emotional openness, trust in unconscious guidance, security, family rootedness, and healthy relation to mothering.",
            "Problem area: emotional wounds, reticence, mistrust, fear, touchiness, moods, unpredictability, vanity, smugness, laziness, and lethargy.",
            "Goal: develop feelings and fantasies, emotional security, closeness, female nature, family or clan life, and popularity.",
            "Representatives: caregivers and helpers, doctors, healers, nurses, spiritual counselors, therapists, and dream or fantasy artists.",
            "Physical correlations: stomach, uterus, lymph system, female breasts, circulation of fluids, autonomous nervous system.",
        ),
    },
    {
        "factor": "Mercury",
        "pages": "33-34",
        "bullets": (
            "Archetype: trader, navigator, scout.",
            "Shadow: crook, liar.",
            "Principle: mind, intellect, combinations, speech, communication, mediation, tactics, knowledge, mental flexibility, orientation, analysis, logic, judgment, and decisions.",
            "Strength: cleverness, quick grasp, observation, adaptability, curiosity, language skill, negotiation, doubt, and careful testing for usefulness.",
            "Problem area: trickster superficiality, cunning, corruptibility, craftiness, audacity, falseness, and inability to see the whole picture.",
            "Goal: collect, mediate, and distribute knowledge; search for new perceptions and paths; critically examine ideas and theories.",
            "Representatives: teachers, students, poets, salespeople, analysts, doctors, critics, scientists, researchers, journalists, linguists, orators, translators, attorneys, and swindlers.",
            "Physical correlations: respiratory system, nervous system, speech center.",
        ),
    },
    {
        "factor": "Venus",
        "pages": "35-36",
        "bullets": (
            "Archetype: muse, lover, beautiful one.",
            "Shadow: Persephone, femme fatale, whore.",
            "Principle: love, feeling, harmony, give-and-take, relationship, partnership, erotic devotion, longing for union, aesthetic perception, art, taste, and sensory pleasure.",
            "Strength: vivacious relationship, harmony, reconciliation, warm empathy, devotion, elegance, good manners, sociability, grace, taste, art, and sensuous enjoyment.",
            "Problem area: easy separations, vanity, superficiality, bad taste, seduction, greed, compulsion, laziness, jealousy, cruelty, snobbery, and depravity.",
            "Goal: seek and create relationships; cultivate love, eroticism, beauty, art, harmony, style, manners, and fine taste.",
            "Representatives: painters, sculptors, actors, authors, musicians, designers, cosmeticians, architects, loving people, and entertainers.",
            "Physical correlations: equilibrium, mucous membranes, veins, kidneys, inner sex organs, sweat glands, erogenous zones.",
        ),
    },
    {
        "factor": "Mars",
        "pages": "37-39",
        "bullets": (
            "Archetype: hero and conqueror.",
            "Shadow: violent person, destroyer.",
            "Principle: will, conquest, stamina, fighting obstacles, determination, conflict readiness, risk, aggression, drive, passion, youthful masculinity, lover, and hothead.",
            "Strength: resolute, goal-oriented action with staying power, commitment, courage, controlled drives, and satisfying sexuality.",
            "Problem area: uncontrolled discharge of aggression, outbursts, impatience, brutality, destructiveness, self-destruction, and frustrated sexuality.",
            "Goal: actualize essential nature, protect and safeguard oneself, win what is one's own, be first, and seek sexual satisfaction.",
            "Representatives: pioneers, conquerors, warriors, entrepreneurs, leaders, adventurers, soldiers, athletes, competitors, knife users, destroyers, fanatics, and tyrants.",
            "Physical correlations: muscles, gallbladder, blood, red blood cells, heat regulation, male sexual organs.",
        ),
    },
    {
        "factor": "Jupiter",
        "pages": "40-41",
        "bullets": (
            "Archetype: high priest, missionary, just person.",
            "Shadow: Pharisee, complacent person, self-righteous individual.",
            "Principle: trust in life, meaning, ideals, values, growth, good fortune, prosperity, horizon-broadening, dignity, wisdom, belief, hope, morals, grace, wealth, optimism, expansion, justice, and abundance.",
            "Strength: morality, ethics, trust, generosity, responsibility, justice, goodness, compassion, reverence, forgiveness, broad understanding, and luck.",
            "Problem area: overestimated personality, high-handedness, vanity, pleasure addiction, hypocrisy, fanaticism, self-aggrandizement, extravagant standards, and intolerance.",
            "Goal: truth, higher understanding, commonly binding principles, personal God, meaningful fulfillment, fortune, and being carried by meaning.",
            "Representatives: teachers, educators, priests, prophets, philosophers, poets, scholars, legal experts, judges, doctors, healers, adventurers, world travelers, and patrons.",
            "Physical correlations: liver, cell growth, fat reserves.",
        ),
    },
    {
        "factor": "Saturn",
        "pages": "42-44",
        "bullets": (
            "Archetype: old wise man, hermit.",
            "Shadow: embittered person, adversary.",
            "Principle: structure, steadfastness, limitation, security, stability, boundaries, time, endings, separations, seclusion, conscience, form, compression, obligation, deceleration, law, and order.",
            "Strength: humility, authenticity, difficult work, endurance, discipline, duty, dependability, maturity, responsibility, patience, wisdom, and modesty.",
            "Problem area: fear of life and failure, authority conflict, hard ambition, cold need for admiration, depression, rigidity, inferiority, loneliness, and lack of warmth.",
            "Goal: autonomous personality, steadfast character, experience, wisdom, self-control, restraint, naked reality, and concentration on essentials.",
            "Representatives: philosophers, elders, hermits, monks, ancestors, lawmakers, judges, critics, bosses, mentors, sculptors, architects, and builders.",
            "Physical correlations: skeleton, bone marrow, calcium balance, teeth, structural and connective tissue, spleen, ears.",
        ),
    },
    {
        "factor": "Uranus",
        "pages": "45-46",
        "bullets": (
            "Archetype: wise fool, hero of freedom.",
            "Shadow: revolutionary, traitor.",
            "Principle: freedom, equality, brotherhood, genius, independence, liberation, surprising change, flashes of inspiration, and sudden upheaval.",
            "Strength: individualism, freedom on mental, emotional, and material levels, spontaneous solutions, discovery, expanded consciousness, originality, experiment, and a seventh sense.",
            "Problem area: restlessness, constant charge, search for novelty, revolution, subversion, arbitrariness, unpredictability, destructiveness, willfulness, and breach of commitment.",
            "Goal: democracy, freedom, human rights, overcoming old structures, liberation from old ties, and disintegration of bonds.",
            "Representatives: inventors, technicians, pilots, artists, revolutionaries, anarchists, astrologers, futurists, mental acrobats, yogis, eccentrics, philosophers, and recluses.",
            "Physical correlations: nervous system, tension and release of tension, rhythm.",
        ),
    },
    {
        "factor": "Neptune",
        "pages": "47-49",
        "bullets": (
            "Archetype: mystic, visionary, martyr.",
            "Shadow: crackpot, addict, alcoholic.",
            "Principle: dissolving boundaries, subtle perception, transcendence, hidden correlations, future trends, longing beyond everyday consciousness, spiritual aspiration, and possible confusion with intoxication.",
            "Strength: mediumistic receptivity, divine conviction, compassion, devotion, mystic experience, guidance, visionary ability, intuition, emotional images, and imagination.",
            "Problem area: seduction, addiction, mass currents, victimhood, charlatanry, instability, weak boundaries, drifting, irresponsibility, confusion, self-deception, and lack of orientation.",
            "Goal: go beyond the self, merge into a we-feeling, be touched or redeemed by the divine, find true spirituality, and witness the divine in the world.",
            "Representatives: inspired artists, actors, musicians, poets, priests, mystics, occultists, chemists, nurses, doctors, psychologists, trend researchers, forecasters, addicts, and swindlers.",
            "Physical correlations: pineal gland.",
        ),
    },
    {
        "factor": "Pluto",
        "pages": "50-52",
        "bullets": (
            "Archetype: magician, shaman.",
            "Shadow: black magician.",
            "Principle: deepest transformation, black alchemical gold, archaic depth-source, archetypal forces, power and helplessness, dependency, subjection, emotional entanglement, and obsession.",
            "Strength: powers of the soul, suggestion, hypnosis, healing force, creative potency, intense will, fundamental transformation, and willingness to face abysses.",
            "Problem area: misuse of power, sadism, tyranny, possession by unconscious complexes, compulsion, destructiveness, pathological control, inability to let go, and lack of distance.",
            "Goal: radical transformation in favor of deep truth, recognizing that every beginning already contains ending and rebirth.",
            "Representatives: analysts, doctors, researchers, dictators, scientists, speculators, violent criminals, charismatic leaders, demagogues, hypnotists, and occultists.",
            "Physical correlations: sexual organs, regenerative ability.",
        ),
    },
    {
        "factor": "Node",
        "pages": "53-54",
        "bullets": (
            "Source scope: Moon's Node axis, not separate North Node and South Node factor pages.",
            "Principle: the crucial point in a person's life, showing tasks to be mastered and the purpose of existence.",
            "South Node: past, old patterns, and behaviors the soul has already brought along; the descending node can obstruct development as a brake.",
            "North Node: future direction and the tasks waiting to be resolved; the ascending node indicates the challenging new direction.",
            "Integration: both nodal themes must be meaningfully connected; aspects to the nodes show supportive or inhibiting powers.",
            "Chart role: the nodal axis gives a direct insight into the horoscope's tasks and reduces the chart to a common denominator or quintessence.",
        ),
    },
)


def clean_text(value: str) -> str:
    replacements = {
        "\f": " ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2014": " - ",
        "\u2013": "-",
        "\u00b0": " degrees",
    }
    result = value
    for old, new in replacements.items():
        result = result.replace(old, new)
    result = re.sub(r"\(\s*\)", "", result)
    result = re.sub(r"\s+([,.;:])", r"\1", result)
    return re.sub(r"\s+", " ", result).strip()


def clipped(value: str, limit: int = 340) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    selected = ""
    for sentence in sentences:
        candidate = f"{selected} {sentence}".strip()
        if selected and len(candidate) > limit:
            break
        selected = candidate
        if len(selected) >= 160 and selected.endswith("."):
            break
    if selected:
        return selected
    return f"{cleaned[:limit].rsplit(' ', 1)[0]}."


def page_ranges(text: str, first_page: int) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    offset = 0
    for index, page in enumerate(text.split("\f")):
        ranges.append((offset, first_page + index))
        offset += len(page) + 1
    return ranges


def page_at(ranges: list[tuple[int, int]], position: int) -> int:
    current = ranges[0][1]
    for offset, page in ranges:
        if offset > position:
            break
        current = page
    return current


def format_pages(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}-{end}"


def extract_archetype_shadow(block: str) -> tuple[str, str]:
    lines = block.splitlines()
    for index, line in enumerate(lines[:10]):
        if "ARCHETYPE:" not in line or "SHADOW:" not in line:
            continue
        column = line.index("SHADOW:")
        archetype = line[:column].split("ARCHETYPE:", 1)[1].strip()
        shadow = line[column:].split("SHADOW:", 1)[1].strip()
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].strip():
            if "COMPARISON" in lines[cursor] or ":" in lines[cursor]:
                break
            archetype = f"{archetype} {lines[cursor][:column].strip()}"
            shadow = f"{shadow} {lines[cursor][column:].strip()}"
            cursor += 1
        return clean_text(archetype), clean_text(shadow)
    return "", ""


def extract_comparison(block: str) -> str:
    match = re.search(r"COMPARISON:\s*(.*?)(?=GENERAL:|HARMONY:|DISCORD:|CONJUNCTION:|\Z)", block, re.S)
    if match is None:
        return ""
    pairs: list[str] = []
    for line in match.group(1).replace("\f", "").splitlines():
        if not line.strip():
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 2:
            pairs.append(f"{clean_text(parts[0])} / {clean_text(parts[-1])}")
    return "; ".join(pairs[:8])


def extract_labeled(block: str, label: str) -> str:
    match = re.search(
        rf"{label}:\s*(.*?)(?=\s*(?:GENERAL|HARMONY|DISCORD|CONJUNCTION):|\Z)",
        block,
        re.S,
    )
    return clipped(match.group(1), 420 if label == "GENERAL" else 340) if match else ""


def parse_pair_entries(path: Path) -> list[PairEntry]:
    text = path.read_text(encoding="utf-8")
    aspect_end = text.find("An ILLUSTRATED")
    if aspect_end == -1:
        raise RuntimeError("could not locate end of aspect section")
    aspect_text = text[:aspect_end]
    ranges = page_ranges(text, 279)
    pattern = re.compile(
        r"(?m)^\s+([A-Z][a-z]+)-(Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|Ascendant|Medium Coeli)(?::|\s*$)"
    )
    headings = [(match.group(1), match.group(2), match.start(), match.end()) for match in pattern.finditer(aspect_text)]
    right_map = {"North Node": "Node", "Ascendant": "Asc", "Medium Coeli": "MC"}
    entries: list[PairEntry] = []
    for index, (left, raw_right, start, end) in enumerate(headings):
        next_start = headings[index + 1][2] if index + 1 < len(headings) else aspect_end
        block = aspect_text[end:next_start]
        source_heading = f"{left}-{raw_right}"
        axis = normalize_axis(left, right_map.get(raw_right, raw_right))
        archetype, shadow = extract_archetype_shadow(block)
        bullets: list[tuple[str, str]] = []
        if archetype:
            bullets.append(("Archetype", archetype))
        if shadow:
            bullets.append(("Shadow", shadow))
        comparison = extract_comparison(block)
        if comparison:
            bullets.append(("Comparison", comparison))
        for label in ("CONJUNCTION", "GENERAL", "HARMONY", "DISCORD"):
            value = extract_labeled(block, label)
            if value:
                bullets.append((label.title(), value))
        entries.append(
            {
                "axis_slug": axis.slug,
                "source_heading": source_heading,
                "pages": format_pages(page_at(ranges, start), page_at(ranges, next_start - 1)),
                "bullets": tuple(bullets),
            }
        )
    if len(entries) != 75:
        raise RuntimeError(f"expected 75 pair entries, found {len(entries)}")
    return entries


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise RuntimeError("missing frontmatter")
    _, raw, body = text.split("---\n", 2)
    return raw, body


def update_frontmatter(raw: str) -> str:
    match = re.search(r"(?ms)^source_pages:\n(?P<items>(?:  - .+\n|  \[\]\n)*)", raw)
    if match is None:
        raise RuntimeError("missing source_pages frontmatter")
    slugs = re.findall(r"(?m)^  - (.+)$", match.group("items"))
    if SOURCE_SLUG not in slugs:
        slugs.append(SOURCE_SLUG)
    source_block = "source_pages:\n" + "".join(f"  - {slug}\n" for slug in slugs)
    raw = f"{raw[:match.start()]}{source_block}{raw[match.end():]}"
    return re.sub(r"(?m)^updated_at: .*$", f"updated_at: {UPDATED_AT}", raw)


def upsert_source_entry(body: str, entry: str) -> str:
    pattern = re.compile(rf"(?ms)^### {re.escape(SOURCE_TITLE)}\n\n.*?(?=\n\n### |\n\n## Comparative Schema)")
    if pattern.search(body):
        return pattern.sub(entry.strip(), body)
    marker = "\n\n## Comparative Schema"
    if marker not in body:
        raise RuntimeError("missing Comparative Schema section")
    return body.replace(marker, f"\n\n{entry.strip()}{marker}", 1)


def append_section_link(text: str, heading: str, link: str) -> str:
    if link in text:
        return text
    match = re.search(rf"(?ms)^## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", text)
    if match is None:
        raise RuntimeError(f"missing {heading} section")
    return f"{text[:match.end(1)].rstrip()}\n{link}\n{text[match.end(1):].lstrip()}"


def write_updated_page(path: Path, entry: str, link_heading: str) -> None:
    text = path.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    updated = f"---\n{update_frontmatter(raw)}---\n{upsert_source_entry(body, entry)}"
    updated = append_section_link(updated, link_heading, SOURCE_LINK)
    path.write_text(updated, encoding="utf-8")


def render_factor_entry(entry: FactorEntry) -> str:
    bullets = "\n".join(f"- {item}" for item in entry["bullets"])
    return f"""### {SOURCE_TITLE}

- Source heading: `{entry["factor"]}`
- Source pages: `{entry["pages"]}`

#### Banzhaf/Haebler Factor Keywords

{bullets}
"""


def render_pair_entry(entry: PairEntry) -> str:
    bullets = "\n".join(f"- {label}: {value}" for label, value in entry["bullets"])
    return f"""### {SOURCE_TITLE}

- Source heading: `{entry["source_heading"]}`
- Source pages: `{entry["pages"]}`

#### Banzhaf/Haebler Pair Keywords

{bullets}
"""


def render_source_page(pair_count: int) -> str:
    factors = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Node", "Asc", "MC")
    factor_links = "\n".join(f"- [{entry['factor']}](../factors/{factor_slug(entry['factor'])}.md)" for entry in FACTOR_ENTRIES)
    axis_participants = "\n".join(f"- [{factor}](../factors/{factor_slug(factor)}.md)" for factor in factors)
    factors_yaml = "\n".join(f"  - {factor}" for factor in factors)
    return f"""---
title: "{SOURCE_TITLE}"
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: modern_astrology
factors:
{factors_yaml}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Authors: Hajo Banzhaf and Anna Haebler
- Title: *Keywords for Astrology*
- Source file (read-only external collection): `{PDF_PATH}`

## Scope Notes

- This ingest admits only explicit standalone factor meanings and unordered aspect/pair keyword sections.
- Standalone factor coverage is limited to Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, and the Moon's Node axis as canonical `Node`.
- The aspect section is collapsed only into unordered canonical axis pages for the ten planets plus Node, Asc, and MC.
- No oriented `A/B = C` activation pages are created or modified because this source gives aspect/pair meanings, not midpoint activation formulas.
- Sign, house, degree, timing, transit, progression, direction, and illustrated-key material are skipped.

## Factors Covered

- Canonical factor pages updated: `11`.

{factor_links}

## Axis Participants

- Canonical factors appearing in admitted axis entries: `13`.

{axis_participants}

## Axes Covered

- Canonical axis pages updated: `{pair_count}`.
- Coverage includes `45` planet-to-planet pairs plus `30` planet-to-Node/Asc/MC pairs.

## Activations Covered

- None. This source remains out of oriented activation pages and triad hubs.

## Ingestion History

- {UPDATED_AT}: Ingested admitted factor and unordered aspect/pair keyword sections into canonical factor and axis pages only.
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    pair_entries = parse_pair_entries(root / ".codex_tmp" / "banzhaf_pairs.txt")

    source_path = root / "wiki" / "sources" / f"{SOURCE_SLUG}.md"
    source_path.write_text(render_source_page(len(pair_entries)), encoding="utf-8")

    for factor_entry in FACTOR_ENTRIES:
        path = root / "wiki" / "factors" / f"{factor_slug(factor_entry['factor'])}.md"
        write_updated_page(path, render_factor_entry(factor_entry), "Related Sources")

    for pair_entry in pair_entries:
        path = root / "wiki" / "axes" / f"{pair_entry['axis_slug']}.md"
        write_updated_page(path, render_pair_entry(pair_entry), "Links")


if __name__ == "__main__":
    main()
