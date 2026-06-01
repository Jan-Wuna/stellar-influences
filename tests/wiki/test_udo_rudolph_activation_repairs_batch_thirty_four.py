from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirty_fourth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirty_fourth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Vulcanus/Poseidon = Neptune](../activations/vulcanus-poseidon-equals-neptune.md)" not in page.body
    assert "[Vulcanus/Poseidon = Pluto](../activations/vulcanus-poseidon-equals-pluto.md)" not in page.body
    assert "[Vulcanus/Poseidon = Apollon](../activations/vulcanus-poseidon-equals-apollon.md)" not in page.body


def test_vulcanus_poseidon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-neptune.md"))

    assert "insights into a future energy" in page.body
    assert "subtle spiritual energy" in page.body
    assert "insight about cine zukUnftige Energie" not in page.body


def test_vulcanus_poseidon_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-pluto.md"))

    assert "unfold spiritual energies" in page.body
    assert "growing cultural influence" in page.body
    assert "lung, spiritual Energien entfalten" not in page.body


def test_vulcanus_poseidon_equals_apollon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-apollon.md"))

    assert "expansion of a spiritual influence" in page.body
    assert "reasonable experiences of power" in page.body
    assert "Ausdehnung a spirit Einflusses" not in page.body


def test_batch_thirty_four_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-apollon.md"))
    comparative_page = load_page(Path("wiki/factors/vulcanus.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1
