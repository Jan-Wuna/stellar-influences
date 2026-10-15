from __future__ import annotations

from pathlib import Path
import sys
from typing import Final

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_pages import iter_wiki_pages
from tools.wiki_links import relative_link_target


SECTION_TITLES = {
    "factor": "Factors",
    "axis": "Axes",
    "activation": "Activations",
    "triad_hub": "Triad Hubs",
    "source": "Sources",
    "derived": "Derived Pages",
}

SECTION_NOTES: Final[dict[str, str]] = {
    "triad_hub": "Use these structural hubs for orientation maps and sibling lookup. Read each exact activation separately for its meaning.",
    "source": "Use these catalogs for bibliography, admitted source material, provenance, and coverage limits.",
    "derived": "This list includes synthesis notes, source companions, and research notes. Check the [Query Guide](query-guide.md) for each role before using a note as an answer surface.",
}


def _relative_label(index_path: Path, page_path: Path) -> str:
    return relative_link_target(index_path, page_path)


def build_index(root: Path) -> str:
    index_path = root / "index.md"
    grouped: dict[str, list[tuple[str, str]]] = {key: [] for key in SECTION_TITLES}
    for page in iter_wiki_pages(root):
        page_type = page.meta.get("page_type")
        if page_type not in SECTION_TITLES:
            continue
        title = page.meta.get("title", page.path.stem)
        grouped[page_type].append((title, _relative_label(index_path, page.path)))

    lines = [
        "# Index",
        "",
        "Use [Query Guide](query-guide.md) for answer-first retrieval and [`query-manifest.json`](query-manifest.json) for machine-readable page roles.",
        "",
        "## Choose a Reading Route",
        "",
        "- **Exact formula:** browse [Activations](#activations). Keep the factor after `=` in its stated position; sibling orientations have separate meanings.",
        "- **Shared pair:** browse [Axes](#axes). The two factors form one unordered pair.",
        "- **Recurring factor:** browse [Factors](#factors) for standalone evidence, documented scope limits, and related combinations.",
        "- **Orientation siblings:** browse [Triad Hubs](#triad-hubs) for the orientation map. These hubs are structural and do not merge interpretations.",
        "- **Evidence and limits:** use [Sources](#sources) for admitted scope and provenance, and the [Query Guide](query-guide.md#evidence-and-limits) for the evidence-reading route.",
        "- **Synthesis and research:** browse [Derived Pages](#derived-pages), then check the guide's [page roles](query-guide.md#using-the-manifest) to distinguish answer notes from companions and audits.",
        "",
        "On a canonical page, start with **Derived Synthesis**, then follow its source-entry links for the passages and qualifications behind the reading.",
        "",
    ]
    for page_type, heading in SECTION_TITLES.items():
        lines.append(f"## {heading}")
        lines.append("")
        if note := SECTION_NOTES.get(page_type):
            lines.extend([note, ""])
        entries = sorted(grouped[page_type], key=lambda item: item[0].casefold())
        if not entries:
            lines.append("- None")
        else:
            for title, relpath in entries:
                lines.append(f"- [{title}]({relpath})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    root = Path("wiki")
    index_path = root / "index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(build_index(root), encoding="utf-8")


if __name__ == "__main__":
    main()
