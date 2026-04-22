from pathlib import Path

from tools.wiki_pages import load_page


HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_hand_source_page_exists():
    page = load_page(Path("wiki/sources") / f"{HAND_SLUG}.md")

    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "Canonical factor pages updated or created: `14`." in page.body
    assert "Canonical axis pages updated or created: `91`." in page.body
    assert "shared `The Ascendant and Midheaven` section is attached to both factor pages" in page.body
    assert "The chapters on aspects, signs, houses, and midpoint technique" in page.body


def test_sun_moon_axis_includes_hand_entry():
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
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `Sun/Moon`" in page.body
    assert "The balance of male and female within the psyche" in page.body


def test_vernal_point_sun_axis_becomes_comparative_with_hand_entry():
    page = load_page(Path("wiki/axes/vernal-point-sun.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, HAND_SLUG]
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `Sun/Aries`" in page.body
    assert "The desire to make connections in the larger world" in page.body


def test_node_asc_axis_includes_hand_entry():
    page = load_page(Path("wiki/axes/node-asc.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [
        WITTE_SLUG,
        EBERTIN_SLUG,
        SANDBACH_SLUG,
        HAND_SLUG,
        MUNKASEY_SLUG,
    ]
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `Nodes/Ascendant`" in page.body
    assert "Connections of a personal nature" in page.body


def test_activation_pages_do_not_gain_hand_source_pages():
    page = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))

    assert HAND_SLUG not in page.meta["source_pages"]


def test_sun_factor_includes_hand_entry():
    page = load_page(Path("wiki/factors/sun.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, EBERTIN_SLUG, HAND_SLUG]
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `The Sun`" in page.body
    assert "It is the basic energy of Being." in page.body


def test_asc_factor_includes_hand_shared_entry():
    page = load_page(Path("wiki/factors/asc.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, EBERTIN_SLUG, HAND_SLUG]
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `The Ascendant and Midheaven`" in page.body
    assert "exchange with the environment" in page.body


def test_vernal_point_factor_becomes_comparative_with_hand_entry():
    page = load_page(Path("wiki/factors/vernal-point.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, HAND_SLUG]
    assert page.meta["aliases"] == ["VP"]
    assert f"### {HAND_TITLE}" in page.body
    assert "- Source heading: `The Vernal Point`" in page.body
    assert "most impersonal but also the oddest social contacts" in page.body
    assert "Aries Point" not in page.body
    assert "Aides Point" not in page.body
