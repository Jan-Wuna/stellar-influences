from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirty_second_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirty_second_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Hades/Vulcanus = Node](../activations/hades-vulcanus-equals-node.md)" not in page.body
    assert "[Hades/Vulcanus = Poseidon](../activations/hades-vulcanus-equals-poseidon.md)" not in page.body
    assert "[Zeus/Kronos = Cupido](../activations/zeus-kronos-equals-cupido.md)" not in page.body
    assert "[Zeus/Apollon = Vulcanus](../activations/zeus-apollon-equals-vulcanus.md)" not in page.body
    assert "[Zeus/Vulcanus = Vernal Point](../activations/zeus-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Zeus/Vulcanus = Venus](../activations/zeus-vulcanus-equals-venus.md)" not in page.body
    assert "[Zeus/Vulcanus = Jupiter](../activations/zeus-vulcanus-equals-jupiter.md)" not in page.body
    assert "[Zeus/Vulcanus = Admetos](../activations/zeus-vulcanus-equals-admetos.md)" not in page.body
    assert "[Zeus/Poseidon = Vernal Point](../activations/zeus-poseidon-equals-vernal-point.md)" not in page.body
    assert "[Zeus/Poseidon = Cupido](../activations/zeus-poseidon-equals-cupido.md)" not in page.body
    assert "[Kronos/Apollon = Cupido](../activations/kronos-apollon-equals-cupido.md)" not in page.body
    assert "[Kronos/Apollon = Vulcanus](../activations/kronos-apollon-equals-vulcanus.md)" not in page.body


def test_hades_vulcanus_equals_node_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/hades-vulcanus-equals-node.md"))

    assert "energy deficiency in connections" in page.body
    assert "secret connections to power" in page.body
    assert "Energie Mangel in connection" not in page.body


def test_zeus_kronos_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/zeus-kronos-equals-cupido.md"))

    assert "reputation through shared striving toward goals" in page.body
    assert "state leadership community" in page.body
    assert "Ansehen through common Zielstreben" not in page.body


def test_zeus_vulcanus_equals_venus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/zeus-vulcanus-equals-venus.md"))

    assert "fiery influence of love" in page.body
    assert "creative influence of beauty" in page.body
    assert "Feuriger love Einfluss" not in page.body


def test_kronos_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/kronos-apollon-equals-vulcanus.md"))

    assert "special power successes" in page.body
    assert "important increase of power" in page.body
    assert "besondere power Erfolge" not in page.body


def test_batch_thirty_two_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/kronos-apollon-equals-vulcanus.md"))
    comparative_page = load_page(Path("wiki/factors/kronos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1
