from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Protocol
from urllib.parse import unquote

import markdown
from bs4 import BeautifulSoup

from tools.wiki_pages import WikiPage


PAGE_TYPES = ("factor", "axis", "activation")
PAGE_LABELS = {
    "factor": "Factors",
    "axis": "Axes",
    "activation": "Planetary Pictures",
}
PAGE_DIRS = {
    "factor": "factors",
    "axis": "axes",
    "activation": "activations",
}


class StaticExportPage(Protocol):
    source: Path
    output: Path
    root_url: str
    page: WikiPage


def _page_title(page: WikiPage) -> str:
    return str(page.meta.get("title") or page.path.stem)


def _page_type(page: WikiPage) -> str:
    return str(page.meta.get("page_type") or "")


def _root_prefix(output: Path, out_dir: Path) -> str:
    depth = len(output.relative_to(out_dir).parents) - 1
    return "../" * depth


def _asset_tags(prefix: str) -> str:
    return "\n".join(
        [
            f'<link rel="stylesheet" href="{prefix}assets/styles.css">',
            f'<script defer src="{prefix}assets/search-data.js"></script>',
            f'<script defer src="{prefix}assets/site.js"></script>',
        ],
    )


def _search_box() -> str:
    return (
        '<div class="search">'
        '<label for="site-search">Search</label>'
        '<input id="site-search" data-search-input type="search" '
        'placeholder="Sun/Moon = Venus" autocomplete="off">'
        '<div class="search-results" data-search-results aria-live="polite"></div>'
        "</div>"
    )


def _layout(title: str, main_html: str, prefix: str) -> str:
    safe_title = html.escape(title)
    nav = "".join(
        f'<a href="{prefix}{folder}/index.html">{label}</a>'
        for folder, label in (("factors", "Factors"), ("axes", "Axes"), ("activations", "Planetary Pictures"))
    )
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{safe_title} - Stellar Influences</title>\n"
        f'{_asset_tags(prefix)}\n'
        "</head>\n"
        f'<body data-root="{prefix}">\n'
        '<a class="skip-link" href="#content">Skip to content</a>\n'
        '<header class="site-header"><div class="site-header__inner">\n'
        f'<a class="brand" href="{prefix}index.html">Stellar Influences</a>\n'
        f'<nav class="site-nav" aria-label="Primary">{nav}</nav>\n'
        f"{_search_box()}\n"
        "</div></header>\n"
        f'<main id="content" class="site-main">{main_html}</main>\n'
        '<footer class="site-footer">Portable static export generated from the local wiki.</footer>\n'
        "</body>\n"
        "</html>\n"
    )


def _badge_row(page: WikiPage) -> str:
    badges: list[str] = []
    for key in ("normalized_formula", "normalized_axis", "axis", "activated_by", "slug"):
        value = page.meta.get(key)
        if value:
            badges.append(f'<span class="meta-badge">{html.escape(str(value))}</span>')
    source_pages = page.meta.get("source_pages")
    if isinstance(source_pages, list):
        badges.append(f'<span class="meta-badge">{len(source_pages)} source page links</span>')
    return f'<div class="meta-row">{"".join(badges)}</div>' if badges else ""


def _rewrite_links(soup: BeautifulSoup, export_page: StaticExportPage, source_map: dict[Path, StaticExportPage]) -> None:
    for link in soup.find_all("a", href=True):
        href = str(link["href"])
        if "://" in href or href.startswith(("mailto:", "#")):
            continue
        target, marker, anchor = href.partition("#")
        if not target.endswith(".md"):
            continue
        target_path = (export_page.source.parent / unquote(target)).resolve()
        mapped = source_map.get(target_path)
        if mapped is None:
            classes = link.get("class", [])
            link["class"] = [*classes, "unavailable-link"]
            link["href"] = "#"
            link["title"] = "Supporting page is outside this primary static export."
            continue
        rel = Path(os.path.relpath(mapped.output, start=export_page.output.parent)).as_posix()
        link["href"] = f"{rel}{marker}{anchor}" if marker else rel


def render_markdown_page(export_page: StaticExportPage, source_map: dict[Path, StaticExportPage]) -> str:
    page = export_page.page
    rendered = markdown.markdown(page.body, extensions=["extra", "sane_lists", "toc"])
    soup = BeautifulSoup(rendered, "html.parser")
    _rewrite_links(soup, export_page, source_map)
    page_type = html.escape(_page_type(page))
    title = html.escape(_page_title(page))
    main_html = (
        '<div class="page-shell"><article>'
        '<header class="page-header">'
        f'<span class="type-badge">{page_type}</span>'
        f"<h1>{title}</h1>"
        f"{_badge_row(page)}"
        "</header>"
        f'<div class="markdown-body">{soup}</div>'
        "</article>"
        '<aside class="page-aside"><h2>Navigation</h2>'
        '<p>Use the search field to jump between factors, axes, and oriented planetary pictures.</p>'
        f'<p><a href="{_root_prefix(export_page.output, export_page.output.parents[1])}index.html">Back to root index</a></p>'
        "</aside></div>"
    )
    return _layout(_page_title(page), main_html, _root_prefix(export_page.output, export_page.output.parents[1]))


def _directory_items(pages: list[StaticExportPage], base_output: Path) -> str:
    items: list[str] = []
    for item in pages:
        rel = Path(os.path.relpath(item.output, start=base_output.parent)).as_posix()
        items.append(f'<li class="directory-entry"><a href="{rel}">{html.escape(_page_title(item.page))}</a></li>')
    return "\n".join(items)


def _grouped_pages(pages: list[StaticExportPage]) -> dict[str, list[StaticExportPage]]:
    grouped = {page_type: [] for page_type in PAGE_TYPES}
    for page in pages:
        grouped[_page_type(page.page)].append(page)
    for page_type in PAGE_TYPES:
        grouped[page_type].sort(key=lambda item: _page_title(item.page).casefold())
    return grouped


def render_home(pages: list[StaticExportPage], out_dir: Path) -> str:
    grouped = _grouped_pages(pages)
    total = sum(len(items) for items in grouped.values())
    stats = "".join(
        f'<div class="stat"><strong>{len(grouped[key])}</strong><span>{PAGE_LABELS[key]}</span></div>'
        for key in PAGE_TYPES
    )
    sections: list[str] = []
    for key in PAGE_TYPES:
        label = PAGE_LABELS[key]
        sections.append(
            '<section class="directory-section">'
            f'<div class="directory-heading"><h2>{label}</h2>'
            f'<a href="{PAGE_DIRS[key]}/index.html">Open {label}</a></div>'
            f'<ol class="directory-grid">{_directory_items(grouped[key], out_dir / "index.html")}</ol>'
            "</section>",
        )
    main_html = (
        '<section class="intro"><h1>Stellar Influences Static Wiki</h1>'
        f'<p>A portable HTML export of {total} canonical factor, axis, and planetary picture pages.</p>'
        f'<div class="stats">{stats}</div></section>'
        f'{"".join(sections)}'
    )
    return _layout("Index", main_html, "")


def render_section(page_type: str, pages: list[StaticExportPage], out_dir: Path) -> str:
    output = out_dir / PAGE_DIRS[page_type] / "index.html"
    label = PAGE_LABELS[page_type]
    main_html = (
        f'<section class="intro"><h1>{label}</h1>'
        f'<p>{len(pages)} exported {label.lower()} pages.</p></section>'
        f'<section class="directory-section"><ol class="directory-grid">{_directory_items(pages, output)}</ol></section>'
    )
    return _layout(label, main_html, "../")


