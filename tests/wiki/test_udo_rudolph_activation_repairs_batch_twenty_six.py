from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_sixth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_sixth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Saturn/Hades = Vernal Point](../activations/saturn-hades-equals-vernal-point.md)" not in page.body
    assert "[Saturn/Zeus = Admetos](../activations/saturn-zeus-equals-admetos.md)" not in page.body
    assert "[Saturn/Kronos = Vernal Point](../activations/saturn-kronos-equals-vernal-point.md)" not in page.body
    assert "[Saturn/Apollon = Uranus](../activations/saturn-apollon-equals-uranus.md)" not in page.body
    assert "[Saturn/Apollon = Vulcanus](../activations/saturn-apollon-equals-vulcanus.md)" not in page.body
    assert "[Saturn/Admetos = Vernal Point](../activations/saturn-admetos-equals-vernal-point.md)" not in page.body
    assert "[Saturn/Vulcanus = Node](../activations/saturn-vulcanus-equals-node.md)" not in page.body
    assert "[Saturn/Poseidon = MC](../activations/saturn-poseidon-equals-mc.md)" not in page.body
    assert "[Saturn/Poseidon = Asc](../activations/saturn-poseidon-equals-asc.md)" not in page.body
    assert "[Saturn/Poseidon = Neptune](../activations/saturn-poseidon-equals-neptune.md)" not in page.body
    assert "[Saturn/Poseidon = Pluto](../activations/saturn-poseidon-equals-pluto.md)" not in page.body
    assert "[Saturn/Poseidon = Vulcanus](../activations/saturn-poseidon-equals-vulcanus.md)" not in page.body


def test_saturn_hades_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-hades-equals-vernal-point.md"))

    assert "dangerous problems in public" in page.body
    assert "hidden public problems" in page.body
    assert "Konzentration auf public Not" not in page.body


def test_saturn_apollon_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-apollon-equals-uranus.md"))

    assert "tasks of technical science" in page.body
    assert "increase of new duties" in page.body
    assert "tasks the technischen Wissenschaft" not in page.body


def test_saturn_poseidon_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-poseidon-equals-mc.md"))

    assert "mental and emotional disturbances" in page.body
    assert "my concentration on the truth" in page.body
    assert "Geistig- scclischc Storungcn" not in page.body


def test_saturn_poseidon_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-poseidon-equals-vulcanus.md"))

    assert "tasks of a cultural power" in page.body
    assert "concentrated power of the spirit" in page.body
    assert "tasks a culture power" not in page.body


def test_batch_twenty_six_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/saturn-poseidon-equals-vulcanus.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




