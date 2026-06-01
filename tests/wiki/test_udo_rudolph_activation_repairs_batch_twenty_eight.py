from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_eighth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_eighth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Neptune/Admetos = Asc](../activations/neptune-admetos-equals-asc.md)" not in page.body
    assert "[Neptune/Admetos = Saturn](../activations/neptune-admetos-equals-saturn.md)" not in page.body
    assert "[Neptune/Vulcanus = Asc](../activations/neptune-vulcanus-equals-asc.md)" not in page.body
    assert "[Neptune/Vulcanus = Sun](../activations/neptune-vulcanus-equals-sun.md)" not in page.body
    assert "[Neptune/Vulcanus = Moon](../activations/neptune-vulcanus-equals-moon.md)" not in page.body
    assert "[Neptune/Vulcanus = Mercury](../activations/neptune-vulcanus-equals-mercury.md)" not in page.body
    assert "[Neptune/Vulcanus = Venus](../activations/neptune-vulcanus-equals-venus.md)" not in page.body
    assert "[Neptune/Vulcanus = Jupiter](../activations/neptune-vulcanus-equals-jupiter.md)" not in page.body
    assert "[Neptune/Vulcanus = Saturn](../activations/neptune-vulcanus-equals-saturn.md)" not in page.body
    assert "[Neptune/Vulcanus = Hades](../activations/neptune-vulcanus-equals-hades.md)" not in page.body
    assert "[Neptune/Vulcanus = Zeus](../activations/neptune-vulcanus-equals-zeus.md)" not in page.body
    assert "[Neptune/Vulcanus = Kronos](../activations/neptune-vulcanus-equals-kronos.md)" not in page.body


def test_neptune_admetos_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-admetos-equals-asc.md"))

    assert "dissolution of depressions in the partner" in page.body
    assert "water congestion in a place" in page.body
    assert "Auflosung of Depressionen beim partner" not in page.body


def test_neptune_vulcanus_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-vulcanus-equals-sun.md"))

    assert "subtle energy of a person" in page.body
    assert "strong personal intuition" in page.body
    assert "feinstoffliche Energie the people" not in page.body


def test_neptune_vulcanus_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-vulcanus-equals-saturn.md"))

    assert "energy loss of the water" in page.body
    assert "creeping loss of power" in page.body
    assert "Energie loss the Wassers" not in page.body


def test_neptune_vulcanus_equals_kronos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-vulcanus-equals-kronos.md"))

    assert "special subtle energy" in page.body
    assert "important influence of metaphysics" in page.body
    assert "Besondere feinstoffliche Energie" not in page.body


def test_batch_twenty_eight_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/neptune-vulcanus-equals-kronos.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




