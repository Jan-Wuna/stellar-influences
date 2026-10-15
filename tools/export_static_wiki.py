from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.static_wiki_render import render_home, render_markdown_page, render_section
from tools.wiki_pages import WikiPage, iter_wiki_pages


PAGE_TYPES = ("factor", "axis", "activation")
PAGE_DIRS = {
    "factor": "factors",
    "axis": "axes",
    "activation": "activations",
}
ASSET_SOURCE_DIR = Path(__file__).with_name("static_wiki_assets")


@dataclass(frozen=True, slots=True)
class ExportPage:
    source: Path
    output: Path
    root_url: str
    page: WikiPage


@dataclass(frozen=True, slots=True)
class ExportResult:
    output_dir: Path
    zip_path: Path
    primary_counts: dict[str, int]
    page_count: int


class ExportPathKind(StrEnum):
    WIKI_ROOT = "wiki root"
    INSIDE_WIKI = "inside wiki root"
    REPO_ROOT = "repository root"
    OUTPUT_DIR = "output directory"


class UnsafeExportPathError(ValueError):
    def __init__(self, path: Path, kind: ExportPathKind) -> None:
        super().__init__(f"refusing to clear {kind}: {path}")
        self.path = path
        self.kind = kind


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _validate_output_dir(wiki_root: Path, out_dir: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if out_dir == wiki_root:
        raise UnsafeExportPathError(out_dir, ExportPathKind.WIKI_ROOT)
    if _is_relative_to(out_dir, wiki_root):
        raise UnsafeExportPathError(out_dir, ExportPathKind.INSIDE_WIKI)
    if out_dir == repo_root:
        raise UnsafeExportPathError(out_dir, ExportPathKind.REPO_ROOT)


def _validate_zip_path(wiki_root: Path, out_dir: Path, zip_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if zip_path == wiki_root:
        raise UnsafeExportPathError(zip_path, ExportPathKind.WIKI_ROOT)
    if _is_relative_to(zip_path, wiki_root):
        raise UnsafeExportPathError(zip_path, ExportPathKind.INSIDE_WIKI)
    if zip_path == repo_root:
        raise UnsafeExportPathError(zip_path, ExportPathKind.REPO_ROOT)
    if zip_path == out_dir or _is_relative_to(zip_path, out_dir):
        raise UnsafeExportPathError(zip_path, ExportPathKind.OUTPUT_DIR)


def _page_title(page: WikiPage) -> str:
    return str(page.meta.get("title") or page.path.stem)


def _page_type(page: WikiPage) -> str:
    return str(page.meta.get("page_type") or "")


def _html_path(page: WikiPage, wiki_root: Path, out_dir: Path) -> Path:
    return out_dir / page.path.relative_to(wiki_root).with_suffix(".html")


def _selected_pages(wiki_root: Path, out_dir: Path) -> list[ExportPage]:
    pages: list[ExportPage] = []
    for page in iter_wiki_pages(wiki_root):
        if _page_type(page) not in PAGE_TYPES:
            continue
        output = _html_path(page, wiki_root, out_dir)
        pages.append(
            ExportPage(
                source=page.path.resolve(),
                output=output,
                root_url=output.relative_to(out_dir).as_posix(),
                page=page,
            ),
        )
    return sorted(pages, key=lambda item: (_page_type(item.page), _page_title(item.page).casefold()))


def _grouped_pages(pages: list[ExportPage]) -> dict[str, list[ExportPage]]:
    grouped = {page_type: [] for page_type in PAGE_TYPES}
    for page in pages:
        grouped[_page_type(page.page)].append(page)
    for page_type in PAGE_TYPES:
        grouped[page_type].sort(key=lambda item: _page_title(item.page).casefold())
    return grouped


def _search_row(item: ExportPage) -> dict[str, str]:
    page = item.page
    parts = [_page_title(page), _page_type(page), str(page.meta.get("slug") or "")]
    for key in ("normalized_formula", "normalized_axis", "axis", "activated_by", "factors"):
        value = page.meta.get(key)
        if isinstance(value, list):
            parts.extend(str(part) for part in value)
        elif value:
            parts.append(str(value))
    plain = re.sub(r"\s+", " ", re.sub(r"[#*_`>\-\[\]()]", " ", page.body)).strip()
    return {
        "title": _page_title(page),
        "type": _page_type(page),
        "url": item.root_url,
        "keywords": " ".join(parts),
        "excerpt": plain[:180],
    }


def _write_assets(out_dir: Path, pages: list[ExportPage], counts: dict[str, int]) -> None:
    assets_dir = out_dir / "assets"
    shutil.copytree(ASSET_SOURCE_DIR, assets_dir, dirs_exist_ok=True)
    rows = [_search_row(page) for page in pages]
    data = "window.STELLAR_SEARCH_DATA = " + json.dumps(rows, ensure_ascii=False) + ";\n"
    (assets_dir / "search-data.js").write_text(data, encoding="utf-8")
    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "page_count": len(pages),
        "counts": counts,
        "included_page_types": list(PAGE_TYPES),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _zip_dir(out_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(out_dir.rglob("*")):
            if path.is_file() and path.resolve() != zip_path.resolve():
                archive.write(path, path.relative_to(out_dir).as_posix())


def build_static_wiki(wiki_root: Path, out_dir: Path, zip_path: Path) -> ExportResult:
    wiki_root = wiki_root.resolve()
    out_dir = out_dir.resolve()
    zip_path = zip_path.resolve()
    _validate_output_dir(wiki_root, out_dir)
    _validate_zip_path(wiki_root, out_dir, zip_path)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    pages = _selected_pages(wiki_root, out_dir)
    counts = {page_type: 0 for page_type in PAGE_TYPES}
    for page in pages:
        counts[_page_type(page.page)] += 1
    source_map = {page.source: page for page in pages}
    grouped = _grouped_pages(pages)
    (out_dir / "index.html").write_text(render_home(pages, out_dir), encoding="utf-8")
    for page_type, type_pages in grouped.items():
        section_dir = out_dir / PAGE_DIRS[page_type]
        section_dir.mkdir(parents=True, exist_ok=True)
        (section_dir / "index.html").write_text(render_section(page_type, type_pages, out_dir), encoding="utf-8")
    for page in pages:
        page.output.parent.mkdir(parents=True, exist_ok=True)
        page.output.write_text(render_markdown_page(page, source_map), encoding="utf-8")
    _write_assets(out_dir, pages, counts)
    _zip_dir(out_dir, zip_path)
    return ExportResult(output_dir=out_dir, zip_path=zip_path, primary_counts=counts, page_count=len(pages))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export factor, axis, and planetary-picture wiki pages to static HTML.")
    parser.add_argument("--wiki-root", type=Path, default=Path("wiki"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/static-wiki"))
    parser.add_argument("--zip", dest="zip_path", type=Path, default=Path("outputs/stellar-influences-static-wiki.zip"))
    args = parser.parse_args()
    result = build_static_wiki(args.wiki_root, args.out_dir, args.zip_path)
    print(f"Exported {result.page_count} pages to {result.output_dir}")
    print(f"Created portable zip: {result.zip_path}")


if __name__ == "__main__":
    main()
