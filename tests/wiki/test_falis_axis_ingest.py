from pathlib import Path

from tools.wiki_pages import load_page


FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_falis_source_page_exists():
    page = load_page(Path("wiki/sources") / f"{FALIS_SLUG}.md")

    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "axis-only" in page.body


def test_sun_moon_axis_includes_falis_entry():
    page = load_page(Path("wiki/axes/sun-moon.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [
        "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
        FALIS_SLUG,
        CARTER_SLUG,
        MUNKASEY_SLUG,
    ]
    assert "Michelle Falis - Planet Combinations: Astrological Brainstorms" in page.body
    assert "Strong parental influence." in page.body


def test_neptune_pluto_axis_includes_falis_entry():
    page = load_page(Path("wiki/axes/neptune-pluto.md"))

    assert "Michelle Falis - Planet Combinations: Astrological Brainstorms" in page.body
    assert "Deeply unconscious and difficult to define processes." in page.body
