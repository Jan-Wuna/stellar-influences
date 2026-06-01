from pathlib import Path

from tools.wiki_pages import load_page


SOURCE_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"


def test_munkasey_source_page_exists_and_mentions_mwa_omission():
    page = load_page(Path("wiki/sources") / f"{SOURCE_SLUG}.md")
    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "page-1 axis prose into canonical axis pages" in page.body
    assert "page-2 activation entries are merged into canonical activation pages" in page.body
    assert "page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`" in page.body
    assert "page-4 MWA example tables were intentionally omitted" in page.body
    assert "Canonical activation pages updated or created: `1014`." in page.body


def test_sun_moon_concepts_companion_page_exists():
    page = load_page(Path("wiki/derived/munkasey-sun-moon-concepts.md"))
    assert page.meta["page_type"] == "derived"
    assert page.meta["slug"] == "munkasey-sun-moon-concepts"
    assert "## Source Concepts" in page.body
    assert "- Arrogant Approval" in page.body
    assert "Jerry Rubin" not in page.body


def test_sun_moon_axis_gains_munkasey_source_entry_and_companion_link():
    page = load_page(Path("wiki/axes/sun-moon.md"))
    for slug in (
        WITTE_SLUG,
        EBERTIN_SLUG,
        FALIS_SLUG,
        CARTER_SLUG,
        SANDBACH_SLUG,
        HAND_SLUG,
        MCBROOM_SLUG,
        SOURCE_SLUG,
    ):
        assert slug in page.meta["source_pages"]
    assert "### Michael Munkasey - Midpoints: Unleashing the Power of the Planets" in page.body
    assert "direction and focus of your personal awareness" in page.body
    assert "#### Munkasey Concepts Companion" in page.body
    assert "../derived/munkasey-sun-moon-concepts.md" in page.body


def test_witte_only_axis_becomes_comparative_with_munkasey_entry():
    page = load_page(Path("wiki/axes/sun-node.md"))
    assert page.meta["framework_scope"] == "comparative"
    for slug in (WITTE_SLUG, EBERTIN_SLUG, SANDBACH_SLUG, HAND_SLUG, SOURCE_SLUG):
        assert slug in page.meta["source_pages"]
    assert "### Michael Munkasey - Midpoints: Unleashing the Power of the Planets" in page.body
    assert "../derived/munkasey-sun-node-concepts.md" in page.body


def test_venus_saturn_axis_links_exactly_one_concepts_companion():
    page = load_page(Path("wiki/axes/venus-saturn.md"))
    assert page.body.count("munkasey-venus-saturn-concepts.md") == 1


def test_mwa_example_table_text_is_not_rendered_to_axis_pages():
    page = load_page(Path("wiki/axes/sun-moon.md"))
    assert "Significant Examples of People and Events Using Sun/Moon" not in page.body
    assert "STRONG:" not in page.body
    assert "WEAK:" not in page.body
    assert "EVENTS:" not in page.body


def test_sun_factor_gains_munkasey_keyword_entry():
    page = load_page(Path("wiki/factors/sun.md"))
    assert SOURCE_SLUG in page.meta["source_pages"]
    assert "### Michael Munkasey - Midpoints: Unleashing the Power of the Planets" in page.body
    assert "#### Basic Ideas" in page.body
    assert "- Acceptability" in page.body
    assert "- Symbolic Leaders" in page.body


def test_sun_moon_activation_gains_munkasey_page_two_entry():
    page = load_page(Path("wiki/activations/sun-moon-equals-mars.md"))
    assert SOURCE_SLUG in page.meta["source_pages"]
    assert "### Michael Munkasey - Midpoints: Unleashing the Power of the Planets" in page.body
    assert "- Source heading: `SUN/MOON with Planets and Points`" in page.body
    assert "Becoming more self-reliant" in page.body


def test_sun_moon_repeated_pair_activation_is_created_from_with_itself_page():
    page = load_page(Path("wiki/activations/sun-moon-equals-sun.md"))
    assert page.meta["normalized_formula"] == "Sun/Moon = Sun"
    assert SOURCE_SLUG in page.meta["source_pages"]
    assert "Repeated-pair identity: no distinct triad hub exists for this activation." in page.body
    assert "- Source heading: `SUN/MOON With Itself`" in page.body
    assert "Helps you focus on the efforts you put into daily events" in page.body
