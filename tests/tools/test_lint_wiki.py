import subprocess
import sys
from pathlib import Path

from tools.lint_wiki import lint_wiki


def test_lint_rejects_activation_missing_axis(tmp_path: Path):
    page = tmp_path / "wiki" / "activations" / "sun-moon-equals-venus.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    assert "missing required field 'axis'" in "\n".join(problems)


def test_lint_rejects_factor_identity_mismatch(tmp_path: Path):
    page = tmp_path / "wiki" / "factors" / "sun.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: venus\n"
        "status: source_ingested\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Moon\n"
        "aliases: []\n"
        "source_pages:\n"
        "  - source-a\n"
        "updated_at: 2026-04-21\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    joined = "\n".join(problems)
    assert "factor title and factors[0] must match canonically" in joined
    assert "factor slug must match canonical factor title" in joined


def test_lint_rejects_axis_identity_mismatch(tmp_path: Path):
    page = tmp_path / "wiki" / "axes" / "sun-moon.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Moon/Sun\n"
        "page_type: axis\n"
        "slug: moon-sun\n"
        "status: source_ingested\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Moon\n"
        "  - Sun\n"
        "normalized_axis: Moon/Sun\n"
        "factor_a: Moon\n"
        "factor_b: Sun\n"
        "related_activations: []\n"
        "related_triad_hubs: []\n"
        "aliases: []\n"
        "source_pages:\n"
        "  - source-a\n"
        "updated_at: 2026-04-21\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    joined = "\n".join(problems)
    assert "axis title must match canonical normalized axis" in joined
    assert "axis slug must match canonical normalized axis" in joined


def test_lint_rejects_false_orientation_aliases(tmp_path: Path):
    page = tmp_path / "wiki" / "activations" / "sun-moon-equals-venus.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "normalized_formula: Sun/Moon = Venus\n"
        "axis: Sun/Moon\n"
        "activated_by: Venus\n"
        "triad_set:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "aliases:\n"
        "  - Sun/Venus = Moon\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    assert "aliases must not collapse distinct orientations" in "\n".join(problems)


def test_lint_rejects_triad_orientation_mismatch(tmp_path: Path):
    page = tmp_path / "wiki" / "triads" / "sun-moon-venus.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun Moon Venus\n"
        "page_type: triad_hub\n"
        "slug: sun-moon-venus\n"
        "status: source_ingested\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "triad_set:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "orientations:\n"
        "  - Sun/Moon = Venus\n"
        "aliases: []\n"
        "source_pages:\n"
        "  - source-a\n"
        "updated_at: 2026-04-21\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    joined = "\n".join(problems)
    assert "triad orientations must list the canonical three distinct orientations" in joined


def test_lint_rejects_derived_missing_updated_at(tmp_path: Path):
    page = tmp_path / "wiki" / "derived" / "example.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Example\n"
        "page_type: derived\n"
        "slug: example\n"
        "status: draft\n"
        "framework_scope: comparative\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    assert "missing required field 'updated_at'" in "\n".join(problems)


def test_lint_rejects_canonical_page_missing_derived_synthesis_anchor(tmp_path: Path):
    page = tmp_path / "wiki" / "factors" / "sun.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: sun\n"
        "status: source_ingested\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Sun\n"
        "aliases: []\n"
        "source_pages:\n"
        "  - source-a\n"
        "updated_at: 2026-05-05\n"
        "---\n"
        "\n"
        "## Identity\n"
        "\n"
        "## Derived Synthesis\n",
        encoding="utf-8",
    )

    problems = lint_wiki(tmp_path / "wiki")

    assert "canonical pages must include an explicit derived-synthesis anchor" in "\n".join(problems)


def test_lint_script_runs_from_repo_root():
    result = subprocess.run(
        [sys.executable, "tools/lint_wiki.py"],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
