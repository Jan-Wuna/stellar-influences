from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_ninth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_ninth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Neptune/Vulcanus = Apollon](../activations/neptune-vulcanus-equals-apollon.md)" not in page.body
    assert "[Neptune/Vulcanus = Admetos](../activations/neptune-vulcanus-equals-admetos.md)" not in page.body
    assert "[Neptune/Vulcanus = Poseidon](../activations/neptune-vulcanus-equals-poseidon.md)" not in page.body
    assert "[Neptune/Poseidon = Moon](../activations/neptune-poseidon-equals-moon.md)" not in page.body
    assert "[Neptune/Poseidon = Uranus](../activations/neptune-poseidon-equals-uranus.md)" not in page.body
    assert "[Neptune/Poseidon = Cupido](../activations/neptune-poseidon-equals-cupido.md)" not in page.body
    assert "[Pluto/Cupido = Sun](../activations/pluto-cupido-equals-sun.md)" not in page.body
    assert "[Pluto/Cupido = Saturn](../activations/pluto-cupido-equals-saturn.md)" not in page.body
    assert "[Pluto/Cupido = Vulcanus](../activations/pluto-cupido-equals-vulcanus.md)" not in page.body
    assert "[Pluto/Apollon = Moon](../activations/pluto-apollon-equals-moon.md)" not in page.body
    assert "[Pluto/Admetos = Vulcanus](../activations/pluto-admetos-equals-vulcanus.md)" not in page.body
    assert "[Pluto/Poseidon = Neptune](../activations/pluto-poseidon-equals-neptune.md)" not in page.body


def test_neptune_vulcanus_equals_apollon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-vulcanus-equals-apollon.md"))

    assert "influence through refinement of knowledge" in page.body
    assert "increase of water energy" in page.body
    assert "Energie Wirtschaft with feinen Staffen" not in page.body


def test_neptune_poseidon_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-poseidon-equals-moon.md"))

    assert "disappointing hour of truth" in page.body
    assert "refinement of emotional clarity" in page.body
    assert "Enttauschende Stun de the truth" not in page.body


def test_pluto_cupido_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/pluto-cupido-equals-saturn.md"))

    assert "serious developmental community" in page.body
    assert "problematic community developments" in page.body
    assert "serious Entwicklungs community" not in page.body


def test_pluto_poseidon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/pluto-poseidon-equals-neptune.md"))

    assert "disappointing cultural development" in page.body
    assert "growing clarity through refinement" in page.body
    assert "Enttauschende culture development" not in page.body


def test_batch_twenty_nine_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/pluto-poseidon-equals-neptune.md"))
    comparative_page = load_page(Path("wiki/factors/poseidon.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1



