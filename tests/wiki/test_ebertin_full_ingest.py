from pathlib import Path

from tools.wiki_pages import load_page


def test_full_ingest_includes_standalone_factor_pages():
    mercury = Path("wiki/factors/mercury.md")
    assert mercury.exists()
    assert "Position in Houses and Signs" in mercury.read_text(encoding="utf-8")


def test_full_ingest_creates_nonpilot_activation_pages():
    page = load_page(Path("wiki/activations/sun-mercury-equals-venus.md"))
    assert page.meta["normalized_formula"] == "Sun/Mercury = Venus"


def test_full_ingest_aligns_axis_summary_and_activation_entries():
    axis = load_page(Path("wiki/axes/sun-mercury.md"))
    activation = load_page(Path("wiki/activations/sun-mercury-equals-moon.md"))

    assert "Mind and common sense" in axis.body
    assert "- Entry: `0195`" in activation.body
    assert "Relationship between mind, soul and intellect." in activation.body
    assert "Mind and common sense" not in activation.body


def test_full_ingest_expands_page_counts():
    assert len(list(Path("wiki/axes").glob("*.md"))) >= 70
    assert len(list(Path("wiki/activations").glob("*.md"))) >= 800
    assert len(list(Path("wiki/triads").glob("*.md"))) >= 250
