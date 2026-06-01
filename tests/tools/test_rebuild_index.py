import subprocess
import sys
from pathlib import Path

from tools.rebuild_index import build_index


def test_build_index_groups_pages_by_type(tmp_path):
    factor = tmp_path / "wiki" / "factors" / "sun.md"
    factor.parent.mkdir(parents=True)
    factor.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "---\n",
        encoding="utf-8",
    )
    activation = tmp_path / "wiki" / "activations" / "sun-moon-equals-venus.md"
    activation.parent.mkdir(parents=True)
    activation.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "---\n",
        encoding="utf-8",
    )

    index_text = build_index(tmp_path / "wiki")

    assert "## Factors" in index_text
    assert "## Activations" in index_text


def test_build_index_points_to_query_artifacts(tmp_path):
    factor = tmp_path / "wiki" / "factors" / "sun.md"
    factor.parent.mkdir(parents=True)
    factor.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "---\n",
        encoding="utf-8",
    )

    index_text = build_index(tmp_path / "wiki")

    assert "[Query Guide](query-guide.md)" in index_text
    assert "`query-manifest.json`" in index_text


def test_build_index_sorts_titles_within_a_section(tmp_path):
    moon = tmp_path / "wiki" / "factors" / "moon.md"
    moon.parent.mkdir(parents=True)
    moon.write_text(
        "---\n"
        "title: Moon\n"
        "page_type: factor\n"
        "---\n",
        encoding="utf-8",
    )
    sun = tmp_path / "wiki" / "factors" / "sun.md"
    sun.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "---\n",
        encoding="utf-8",
    )

    index_text = build_index(tmp_path / "wiki")

    assert index_text.index("- [Moon]") < index_text.index("- [Sun]")


def test_rebuild_index_script_runs_from_repo_root():
    result = subprocess.run(
        [sys.executable, "tools/rebuild_index.py"],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
