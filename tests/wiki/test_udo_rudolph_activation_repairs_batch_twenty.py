from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twentieth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twentieth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Node/Poseidon = Pluto](../activations/node-poseidon-equals-pluto.md)" not in page.body
    assert "[Node/Poseidon = Cupido](../activations/node-poseidon-equals-cupido.md)" not in page.body
    assert "[Mercury/Venus = Vulcanus](../activations/mercury-venus-equals-vulcanus.md)" not in page.body
    assert "[Mercury/Mars = Pluto](../activations/mercury-mars-equals-pluto.md)" not in page.body
    assert "[Mercury/Mars = Cupido](../activations/mercury-mars-equals-cupido.md)" not in page.body
    assert "[Mercury/Saturn = Cupido](../activations/mercury-saturn-equals-cupido.md)" not in page.body
    assert "[Mercury/Uranus = Cupido](../activations/mercury-uranus-equals-cupido.md)" not in page.body
    assert "[Mercury/Pluto = Vernal Point](../activations/mercury-pluto-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Cupido = Vernal Point](../activations/mercury-cupido-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Cupido = MC](../activations/mercury-cupido-equals-mc.md)" not in page.body
    assert "[Mercury/Cupido = Asc](../activations/mercury-cupido-equals-asc.md)" not in page.body
    assert "[Mercury/Cupido = Mars](../activations/mercury-cupido-equals-mars.md)" not in page.body


def test_node_poseidon_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-poseidon-equals-pluto.md"))

    assert "clear development of a connection" in page.body
    assert "changing ideas in a connection" in page.body
    assert "ner reason relationships" not in page.body


def test_mercury_venus_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-venus-equals-vulcanus.md"))

    assert "influence of media art" in page.body
    assert "beauty as moving energy" in page.body
    assert "Einfluss the media art" not in page.body


def test_mercury_uranus_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-uranus-equals-cupido.md"))

    assert "exciting conversations in the community" in page.body
    assert "technical media community" in page.body
    assert "Aufregende conversation in the community" not in page.body


def test_mercury_cupido_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-cupido-equals-mc.md"))

    assert "ensouled thoughts about the community" in page.body
    assert "my thinking about the community" in page.body
    assert "soulful thoughts to the community" not in page.body


def test_batch_twentieth_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/mercury-cupido-equals-mc.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




