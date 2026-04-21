from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_pages import iter_wiki_pages


SECTION_TITLES = {
    "factor": "Factors",
    "axis": "Axes",
    "activation": "Activations",
    "triad_hub": "Triad Hubs",
    "source": "Sources",
    "derived": "Derived Pages",
}


def _relative_label(root: Path, page_path: Path) -> str:
    return page_path.relative_to(root).as_posix()


def build_index(root: Path) -> str:
    grouped: dict[str, list[tuple[str, str]]] = {key: [] for key in SECTION_TITLES}
    for page in iter_wiki_pages(root):
        page_type = page.meta.get("page_type")
        if page_type not in SECTION_TITLES:
            continue
        title = page.meta.get("title", page.path.stem)
        grouped[page_type].append((title, _relative_label(root, page.path)))

    lines = ["# Index", ""]
    for page_type, heading in SECTION_TITLES.items():
        lines.append(f"## {heading}")
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
