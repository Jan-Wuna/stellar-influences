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
