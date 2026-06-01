from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirty_third_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirty_third_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Kronos/Poseidon = Uranus](../activations/kronos-poseidon-equals-uranus.md)" not in page.body
    assert "[Kronos/Poseidon = Neptune](../activations/kronos-poseidon-equals-neptune.md)" not in page.body
    assert "[Kronos/Poseidon = Cupido](../activations/kronos-poseidon-equals-cupido.md)" not in page.body
    assert "[Apollon/Vulcanus = Vernal Point](../activations/apollon-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Apollon/Vulcanus = Pluto](../activations/apollon-vulcanus-equals-pluto.md)" not in page.body
    assert "[Apollon/Poseidon = Vulcanus](../activations/apollon-poseidon-equals-vulcanus.md)" not in page.body
    assert "[Vulcanus/Poseidon = Vernal Point](../activations/vulcanus-poseidon-equals-vernal-point.md)" not in page.body
    assert "[Vulcanus/Poseidon = MC](../activations/vulcanus-poseidon-equals-mc.md)" not in page.body
    assert "[Vulcanus/Poseidon = Asc](../activations/vulcanus-poseidon-equals-asc.md)" not in page.body
    assert "[Vulcanus/Poseidon = Sun](../activations/vulcanus-poseidon-equals-sun.md)" not in page.body
    assert "[Vulcanus/Poseidon = Mars](../activations/vulcanus-poseidon-equals-mars.md)" not in page.body
    assert "[Vulcanus/Poseidon = Jupiter](../activations/vulcanus-poseidon-equals-jupiter.md)" not in page.body


def test_kronos_poseidon_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/kronos-poseidon-equals-uranus.md"))

    assert "spiritual impulses of authority" in page.body
    assert "independent cultural reform" in page.body
    assert "spiritual Impulse the Obrigkeit" not in page.body


def test_kronos_poseidon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/kronos-poseidon-equals-neptune.md"))

    assert "especially clear water" in page.body
    assert "sensitivity of a spiritual authority" in page.body
    assert "Besonders klares water" not in page.body


def test_apollon_poseidon_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/apollon-poseidon-equals-vulcanus.md"))

    assert "successful cultural power" in page.body
    assert "increase of spiritual force" in page.body
    assert "erfolgreiche culture power" not in page.body


def test_vulcanus_poseidon_equals_jupiter_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-jupiter.md"))

    assert "influential financial idea" in page.body
    assert "truth through legal power" in page.body
    assert "Einflufireiche Finanz Idee" not in page.body


def test_batch_thirty_three_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/vulcanus-poseidon-equals-jupiter.md"))
    comparative_page = load_page(Path("wiki/factors/poseidon.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1
