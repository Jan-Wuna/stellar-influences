from pathlib import Path

from tools.wiki_pages import load_page


SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
HAND_SLUG = "robert-hand-horoscope-symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_sandbach_source_page_exists():
    source_path = Path("wiki/sources") / f"{SANDBACH_SLUG}.md"

    assert source_path.exists()
    page = load_page(source_path)
    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "Canonical axis pages updated or created: `91`." in page.body
    assert "Canonical activation pages updated or created: `1092`." in page.body
    assert "Canonical triad hubs updated or created: `364`." in page.body
    assert "The extractable PDF text is missing `8` activator labels" in page.body
    assert "Those gaps are preserved as structural placeholder activation pages" in page.body


def test_chiron_factor_page_exists_as_structural_stub():
    factor_path = Path("wiki/factors/chiron.md")

    assert factor_path.exists()
    page = load_page(factor_path)
    assert page.meta["page_type"] == "factor"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert page.meta["factors"] == ["Chiron"]
    assert "No standalone factor chapter material from this source is ingested on this page." in page.body


def test_sun_moon_axis_includes_sandbach_entry():
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
    assert "### John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints" in page.body
    assert "#### Principle" in page.body
    assert "The flow of energy and information from the subconscious to the conscious" in page.body
    assert "#### Process" in page.body
    assert "One becomes aware of each and every emotion as it arises" in page.body


def test_sun_chiron_axis_is_created():
    axis_path = Path("wiki/axes/sun-chiron.md")

    assert axis_path.exists()
    page = load_page(axis_path)
    assert page.meta["framework_scope"] == "modern_astrology"
    assert page.meta["source_pages"] == [SANDBACH_SLUG]
    assert "Letting go of all things of lesser importance" in page.body
    assert "The process of ceasing to base one’s self-worth on outer or superfi cial criteria" in page.body


def test_existing_activation_page_gains_sandbach_entry():
    page = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, EBERTIN_SLUG, SANDBACH_SLUG]
    assert "### John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints" in page.body
    assert "To feel a full and complete love when one loves." in page.body


def test_sun_chiron_equals_mars_activation_is_created():
    activation_path = Path("wiki/activations/sun-chiron-equals-mars.md")

    assert activation_path.exists()
    page = load_page(activation_path)
    assert page.meta["framework_scope"] == "modern_astrology"
    assert page.meta["source_pages"] == [SANDBACH_SLUG]
    assert "To be able to clear anger by seeing the meaning and purpose behind it." in page.body


def test_missing_sandbach_activation_creates_structural_placeholder_page():
    activation_path = Path("wiki/activations/neptune-node-equals-chiron.md")

    assert activation_path.exists()
    page = load_page(activation_path)
    assert page.meta["framework_scope"] == "modern_astrology"
    assert page.meta["source_pages"] == [SANDBACH_SLUG]
    assert "No extractable activation entry text is available in the current PDF text for this expected Sandbach orientation." in page.body
    assert "this structural placeholder preserves the canonical orientation slot without inventing doctrine." in page.body


def test_existing_witte_activation_can_absorb_sandbach_extraction_gap_note():
    page = load_page(Path("wiki/activations/moon-asc-equals-mercury.md"))

    assert page.meta["framework_scope"] == "comparative"
    assert page.meta["source_pages"] == [WITTE_SLUG, SANDBACH_SLUG]
    assert "### John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints" in page.body
    assert "No extractable activation entry text is available in the current PDF text for this expected Sandbach orientation." in page.body
