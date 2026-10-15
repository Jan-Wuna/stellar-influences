from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AXES = ROOT / "wiki" / "axes"


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def banzhaf_dangling() -> list[str]:
    problems: list[str] = []
    incomplete = re.compile(
        r"(?:,\s*|\b(?:and|or|with|without|of|to|for|from|by|in|into|as|the|a|an)\s*)$",
        re.IGNORECASE,
    )
    for path in sorted(AXES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^### Hajo Banzhaf and Anna Haebler - Keywords for Astrology\n(?P<body>.*?)(?=^## |\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        ):
            body = match.group("body")
            base = match.start("body")
            for rel, line in enumerate(body.splitlines(), start=0):
                stripped = line.strip()
                if re.match(r"^- (?:harmony|discord):", stripped, re.IGNORECASE):
                    value = stripped.split(":", 1)[1].strip()
                    if incomplete.search(value):
                        problems.append(
                            f"{path.relative_to(ROOT)}:{line_number(text, base) + rel}: {stripped}"
                        )
    return problems


def comparative_schema_headings() -> list[str]:
    files = [
        AXES / "jupiter-neptune.md",
        AXES / "mercury-asc.md",
        AXES / "venus-node.md",
    ]
    problems: list[str] = []
    for path in files:
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if "## Comparative Schema" in line and line != "## Comparative Schema":
                problems.append(f"{path.relative_to(ROOT)}:{index}: {line}")
    return problems


def carter_samples() -> list[str]:
    samples = [
        ("mars-jupiter.md", 127, "science, though as regards the last, it is what may be called"),
        ("mars-uranus.md", 143, "Paralysis must sometimes be feared from the tensions of Uranus."),
        ("moon-jupiter.md", 155, "energy, the afflictions of Moon-Jupiter give direction to it."),
        ("sun-moon.md", 164, "re-adjustment ensues speedily and"),
        ("sun-moon.md", 166, "readily. Many of the benefits"),
        ("sun-saturn.md", 149, "Similarly in cases of severe dental trouble."),
    ]
    out: list[str] = []
    for filename, expected_line, needle in samples:
        path = AXES / filename
        lines = path.read_text(encoding="utf-8").splitlines()
        found = [
            index
            for index, line in enumerate(lines, start=1)
            if needle in line
        ]
        if found:
            line_no = found[0]
            line = lines[line_no - 1]
            continuation = ""
            if filename == "sun-moon.md" and expected_line == 164:
                continuation = f" | next line: {lines[line_no].strip()}"
            out.append(
                f"FOUND {path.relative_to(ROOT)}:{line_no}: {line.strip()}{continuation}"
            )
        else:
            out.append(f"MISSING {path.relative_to(ROOT)} expected around line {expected_line}: {needle}")
    return out


def main() -> int:
    dangling = banzhaf_dangling()
    headings = comparative_schema_headings()
    samples = carter_samples()

    print("Banzhaf/Haebler dangling Harmony/Discord count:", len(dangling))
    for item in dangling:
        print("DANGLING", item)

    print("Comparative Schema embedded/indented heading count:", len(headings))
    for item in headings:
        print("BAD_HEADING", item)

    print("Carter sample inspection:")
    for item in samples:
        print(item)

    if dangling or headings or any(item.startswith("MISSING") for item in samples):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
