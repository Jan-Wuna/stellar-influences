from pathlib import Path

from tools.wiki_pages import load_page


def test_corpus_coverage_uses_vernal_point_canonical_name():
    page = load_page(Path("wiki/derived/corpus-coverage-witte-vs-ebertin.md"))

    assert "Vernal Point" in page.body
    assert "`Aries`" not in page.body


def test_munkasey_analysis_uses_vernal_point_canonical_name():
    page = load_page(Path("wiki/derived/munkasey-unleashing-the-power-of-the-planets-ingest-analysis.md"))

    assert "Vernal Point" in page.body
    assert "`Aries`" not in page.body
