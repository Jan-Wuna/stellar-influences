from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_eighteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_eighteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Poseidon = Pluto](../activations/moon-poseidon-equals-pluto.md)" not in page.body
    assert "[Moon/Poseidon = Cupido](../activations/moon-poseidon-equals-cupido.md)" not in page.body
    assert "[Mercury/Node = Vernal Point](../activations/mercury-node-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Node = Asc](../activations/mercury-node-equals-asc.md)" not in page.body
    assert "[Venus/Node = Vernal Point](../activations/venus-node-equals-vernal-point.md)" not in page.body
    assert "[Venus/Node = Vulcanus](../activations/venus-node-equals-vulcanus.md)" not in page.body
    assert "[Mars/Node = Uranus](../activations/mars-node-equals-uranus.md)" not in page.body
    assert "[Mars/Node = Hades](../activations/mars-node-equals-hades.md)" not in page.body
    assert "[Jupiter/Node = Vernal Point](../activations/jupiter-node-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Node = Asc](../activations/jupiter-node-equals-asc.md)" not in page.body
    assert "[Uranus/Node = Vernal Point](../activations/uranus-node-equals-vernal-point.md)" not in page.body
    assert "[Pluto/Node = Vernal Point](../activations/pluto-node-equals-vernal-point.md)" not in page.body


def test_mercury_node_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-node-equals-asc.md"))

    assert "intellectual partner relationships" in page.body
    assert "connecting conversations about the environment" in page.body
    assert "Partner-Gesprache vermitteln" not in page.body


def test_venus_node_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/venus-node-equals-vulcanus.md"))

    assert "energetic bond through love" in page.body
    assert "benevolent influence of a connection" in page.body
    assert "Energie connection through love" not in page.body


def test_mars_node_equals_hades_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-node-equals-hades.md"))

    assert "dangerous work connection" in page.body
    assert "activating connections from the past" in page.body
    assert "Hcrstellung krimineller contact" not in page.body


def test_pluto_node_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/pluto-node-equals-vernal-point.md"))

    assert "development in public connections" in page.body
    assert "changeable bonds in public" in page.body
    assert "development in public Verbindungcn" not in page.body


def test_batch_eighteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/mercury-node-equals-asc.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




