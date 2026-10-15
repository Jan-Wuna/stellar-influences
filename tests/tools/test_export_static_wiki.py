from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from bs4 import BeautifulSoup

from tools.export_static_wiki import UnsafeExportPathError, build_static_wiki


def _write_page(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_static_wiki_exports_primary_wiki_pages_and_rewrites_links(tmp_path):
    wiki = tmp_path / "wiki"
    _write_page(
        wiki / "factors" / "sun.md",
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: sun\n"
        "---\n\n"
        "## Identity\n\n"
        "- Factor: Sun\n",
    )
    _write_page(
        wiki / "axes" / "sun-moon.md",
        "---\n"
        "title: Sun/Moon\n"
        "page_type: axis\n"
        "slug: sun-moon\n"
        "---\n\n"
        "## Identity\n\n"
        "- Axis: `Sun/Moon`\n",
    )
    _write_page(
        wiki / "activations" / "sun-moon-equals-venus.md",
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "axis: Sun/Moon\n"
        "activated_by: Venus\n"
        "factors:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "---\n\n"
        "## Identity\n\n"
        "- Formula: `Sun/Moon = Venus`\n"
        "- Axis page: [Sun/Moon](../axes/sun-moon.md)\n",
    )
    _write_page(
        wiki / "_templates" / "activation.md",
        "---\n"
        "title: Template\n"
        "page_type: activation\n"
        "---\n",
    )

    result = build_static_wiki(wiki, tmp_path / "site", tmp_path / "site.zip")

    assert result.primary_counts == {"factor": 1, "axis": 1, "activation": 1}
    assert (tmp_path / "site" / "index.html").exists()
    assert (tmp_path / "site" / "axes" / "index.html").exists()
    assert (tmp_path / "site" / "activations" / "sun-moon-equals-venus.html").exists()
    assert (tmp_path / "site.zip").exists()

    activation_html = (tmp_path / "site" / "activations" / "sun-moon-equals-venus.html").read_text(
        encoding="utf-8",
    )
    soup = BeautifulSoup(activation_html, "html.parser")

    assert soup.find("h1").get_text(strip=True) == "Sun/Moon = Venus"
    assert soup.find("a", href="../axes/sun-moon.html") is not None
    assert ".md" not in activation_html


def test_build_static_wiki_zip_contains_portable_assets(tmp_path):
    wiki = tmp_path / "wiki"
    _write_page(
        wiki / "factors" / "moon.md",
        "---\n"
        "title: Moon\n"
        "page_type: factor\n"
        "slug: moon\n"
        "---\n\n"
        "## Identity\n\n"
        "- Factor: Moon\n",
    )

    result = build_static_wiki(wiki, tmp_path / "site", tmp_path / "site.zip")

    with ZipFile(result.zip_path) as archive:
        names = set(archive.namelist())

    assert "index.html" in names
    assert "factors/moon.html" in names
    assert "assets/styles.css" in names
    assert "assets/site.js" in names
    assert "assets/search-data.js" in names


def test_build_static_wiki_rejects_output_inside_wiki_root_without_deleting_pages(tmp_path):
    wiki = tmp_path / "wiki"
    page = wiki / "factors" / "sun.md"
    _write_page(
        page,
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: sun\n"
        "---\n\n"
        "## Identity\n\n"
        "- Factor: Sun\n",
    )

    with pytest.raises(UnsafeExportPathError):
        build_static_wiki(wiki, wiki / "static-export", tmp_path / "site.zip")

    assert page.exists()


def test_build_static_wiki_rejects_zip_path_inside_wiki_root_without_overwriting_page(tmp_path):
    wiki = tmp_path / "wiki"
    page = wiki / "factors" / "sun.md"
    original_text = (
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: sun\n"
        "---\n\n"
        "## Identity\n\n"
        "- Factor: Sun\n"
    )
    _write_page(page, original_text)

    with pytest.raises(UnsafeExportPathError):
        build_static_wiki(wiki, tmp_path / "site", page)

    assert page.read_text(encoding="utf-8") == original_text
