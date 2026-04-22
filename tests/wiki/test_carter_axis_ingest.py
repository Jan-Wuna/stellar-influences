from pathlib import Path

from tools.wiki_pages import load_page


CARTER_SLUG = "charles-carter-the-astrological-aspects"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_carter_source_page_exists():
    page = load_page(Path("wiki/sources") / f"{CARTER_SLUG}.md")

    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "classical_aspects"
    assert "collapsed into canonical axis pages" in page.body


def test_sun_moon_axis_includes_carter_family_headings():
    page = load_page(Path("wiki/axes/sun-moon.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [
        WITTE_SLUG,
        EBERTIN_SLUG,
        FALIS_SLUG,
        CARTER_SLUG,
        SANDBACH_SLUG,
        HAND_SLUG,
        MCBROOM_SLUG,
        MUNKASEY_SLUG,
    ]
    assert "### Charles Carter - The Astrological Aspects" in page.body
    assert "#### Pair Overview" in page.body
    assert "#### Harmonious Aspects" in page.body
    assert "#### The Conjunction" in page.body
    assert "#### Inharmonious Aspects" in page.body
    assert "good health supported by a strong constitution" in page.body


def test_mercury_venus_axis_includes_carter_nonstandard_examples():
    page = load_page(Path("wiki/axes/mercury-venus.md"))

    assert page.meta["source_pages"] == [
        WITTE_SLUG,
        EBERTIN_SLUG,
        FALIS_SLUG,
        CARTER_SLUG,
        SANDBACH_SLUG,
        HAND_SLUG,
        MUNKASEY_SLUG,
    ]
    assert "### Charles Carter - The Astrological Aspects" in page.body
    assert "#### Pair Overview" in page.body
    assert "Harmonious (Sextile)" in page.body
    assert "Mrs. Eddy" in page.body


def test_carter_source_page_reports_full_axis_coverage():
    page = load_page(Path("wiki/sources") / f"{CARTER_SLUG}.md")

    assert "Canonical axis pages updated or created: `36`." in page.body


def test_activation_pages_do_not_gain_carter_source_pages():
    page = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))

    assert CARTER_SLUG not in page.meta["source_pages"]
