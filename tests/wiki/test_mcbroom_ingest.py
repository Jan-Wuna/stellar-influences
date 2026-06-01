from pathlib import Path

from tools.wiki_pages import load_page


MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"
UDO_RUDOLPH_SLUG = "udo-rudolph-abc-fur-planetenbilder"


def test_mcbroom_source_page_exists_with_bounded_scope():
    page = load_page(Path("wiki/sources") / f"{MCBROOM_SLUG}.md")

    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "methodology-heavy midpoint text" in page.body
    assert "Canonical axis pages updated or created: `2`." in page.body
    assert "Canonical activation pages updated or created: `2`." in page.body
    assert "transits/progressions/solar arcs" in page.body


def test_sun_moon_axis_includes_mcbroom_entry():
    page = load_page(Path("wiki/axes/sun-moon.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [
        "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
        UDO_RUDOLPH_SLUG,
        "reinhold-ebertin-the-combination-of-stellar-influences",
        "michelle-falis-planet-combinations-astrological-brainstorms",
        "charles-carter-the-astrological-aspects",
        "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints",
        HAND_SLUG,
        MCBROOM_SLUG,
        MUNKASEY_SLUG,
    ]
    assert f"### {MCBROOM_TITLE}" in page.body
    assert "- Source heading: `The Sun/Moon Midpoint`" in page.body
    assert "Sun/Moon midpoint will often dominate the life" in page.body
    assert "When a Focal Point is within orb" not in page.body


def test_asc_mc_axis_includes_mcbroom_entry():
    page = load_page(Path("wiki/axes/asc-mc.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [
        "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
        UDO_RUDOLPH_SLUG,
        "reinhold-ebertin-the-combination-of-stellar-influences",
        "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints",
        HAND_SLUG,
        MCBROOM_SLUG,
        MUNKASEY_SLUG,
    ]
    assert f"### {MCBROOM_TITLE}" in page.body
    assert "- Source heading: `The Ascendant/Midheaven Midpoint`" in page.body
    assert "represents an area of the chart where our personal and public sides can come together" in page.body
    assert "Intimately associated with our definition and expression of personal identity" not in page.body


def test_sun_moon_equals_mercury_includes_mcbroom_entry_without_example_list():
    page = load_page(Path("wiki/activations/sun-moon-equals-mercury.md"))

    assert MCBROOM_SLUG in page.meta["source_pages"]
    assert f"### {MCBROOM_TITLE}" in page.body
    assert "- Source heading: `Mercury at the Sun/Moon Midpoint`" in page.body
    assert "thoughts, ideas, and communication will be involved as the central unifying focus" in page.body
    assert "Famous people with this placement include" not in page.body
    assert "*" not in page.body.split("#### McBroom Entry", 1)[1].split("## Comparative Schema", 1)[0]


def test_asc_mc_equals_mercury_includes_mcbroom_entry_without_example_list():
    page = load_page(Path("wiki/activations/asc-mc-equals-mercury.md"))

    assert MCBROOM_SLUG in page.meta["source_pages"]
    assert f"### {MCBROOM_TITLE}" in page.body
    assert "- Source heading: `Mercury = Asc/Mc`" in page.body
    assert "Thoughts, ideas, and communication come naturally" in page.body
    assert "Some people are as drawn to the communication style" in page.body
    assert "Famous people with this placement include" not in page.body
    assert "SIGNIFICANT MIDPOINTS" not in page.body


def test_unrelated_activation_does_not_gain_mcbroom_source():
    page = load_page(Path("wiki/activations/sun-venus-equals-moon.md"))

    assert MCBROOM_SLUG not in (page.meta.get("source_pages") or [])
    assert f"### {MCBROOM_TITLE}" not in page.body
