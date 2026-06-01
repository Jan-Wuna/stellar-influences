from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_nineteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_nineteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Node/Hades = Vernal Point](../activations/node-hades-equals-vernal-point.md)" not in page.body
    assert "[Node/Kronos = Cupido](../activations/node-kronos-equals-cupido.md)" not in page.body
    assert "[Node/Apollon = Uranus](../activations/node-apollon-equals-uranus.md)" not in page.body
    assert "[Node/Apollon = Vulcanus](../activations/node-apollon-equals-vulcanus.md)" not in page.body
    assert "[Node/Admetos = Vernal Point](../activations/node-admetos-equals-vernal-point.md)" not in page.body
    assert "[Node/Admetos = MC](../activations/node-admetos-equals-mc.md)" not in page.body
    assert "[Node/Vulcanus = Vernal Point](../activations/node-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Node/Vulcanus = Sun](../activations/node-vulcanus-equals-sun.md)" not in page.body
    assert "[Node/Vulcanus = Venus](../activations/node-vulcanus-equals-venus.md)" not in page.body
    assert "[Node/Vulcanus = Pluto](../activations/node-vulcanus-equals-pluto.md)" not in page.body
    assert "[Node/Poseidon = Vernal Point](../activations/node-poseidon-equals-vernal-point.md)" not in page.body
    assert "[Node/Poseidon = Neptune](../activations/node-poseidon-equals-neptune.md)" not in page.body


def test_node_hades_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-hades-equals-vernal-point.md"))

    assert "encounter with the distress of the world" in page.body
    assert "hidden relationships in public" in page.body
    assert "[kgegnung with the Not the world" not in page.body


def test_node_kronos_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-kronos-equals-cupido.md"))

    assert "reputation through art in a connection" in page.body
    assert "state mediation community" in page.body
    assert "Ansehen through art in the connection" not in page.body


def test_node_vulcanus_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-vulcanus-equals-sun.md"))

    assert "encounter with human power" in page.body
    assert "connection to a violent person" in page.body
    assert "Begegnung with menschlicher power" not in page.body


def test_node_poseidon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-poseidon-equals-neptune.md"))

    assert "disappointment in a spiritual connection" in page.body
    assert "spiritual development in a connection" in page.body
    assert "Enttauschung in the spirit connection" not in page.body


def test_batch_nineteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/node-hades-equals-vernal-point.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




