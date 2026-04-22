from pathlib import Path

from tools.wiki_pages import load_page


SOURCE_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_munkasey_source_page_exists_and_mentions_mwa_omission():
    page = load_page(Path("wiki/sources") / f"{SOURCE_SLUG}.md")
    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`" in page.body
    assert "page-4 MWA example tables were intentionally omitted" in page.body


def test_sun_moon_concepts_companion_page_exists():
    page = load_page(Path("wiki/derived/munkasey-sun-moon-concepts.md"))
    assert page.meta["page_type"] == "derived"
    assert page.meta["slug"] == "munkasey-sun-moon-concepts"
    assert "## Source Concepts" in page.body
    assert "- Arrogant Approval" in page.body
    assert "Jerry Rubin" not in page.body
