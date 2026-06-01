from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Node = Jupiter](../activations/moon-node-equals-jupiter.md)" not in page.body
    assert "[Moon/Node = Neptune](../activations/moon-node-equals-neptune.md)" not in page.body
    assert "[Moon/Node = Pluto](../activations/moon-node-equals-pluto.md)" not in page.body
    assert "[Moon/Node = Cupido](../activations/moon-node-equals-cupido.md)" not in page.body
    assert "[Moon/Node = Admetos](../activations/moon-node-equals-admetos.md)" not in page.body
    assert "[Moon/Mercury = Vernal Point](../activations/moon-mercury-equals-vernal-point.md)" not in page.body
    assert "[Moon/Mercury = Asc](../activations/moon-mercury-equals-asc.md)" not in page.body
    assert "[Moon/Mercury = Neptune](../activations/moon-mercury-equals-neptune.md)" not in page.body
    assert "[Moon/Mercury = Pluto](../activations/moon-mercury-equals-pluto.md)" not in page.body
    assert "[Moon/Mercury = Cupido](../activations/moon-mercury-equals-cupido.md)" not in page.body
    assert "[Moon/Mars = Vernal Point](../activations/moon-mars-equals-vernal-point.md)" not in page.body
    assert "[Moon/Mars = MC](../activations/moon-mars-equals-mc.md)" not in page.body


def test_moon_node_equals_jupiter_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-node-equals-jupiter.md"))

    assert "financial relationships to peoples" in page.body
    assert "advantage through connections among peoples" in page.body
    assert "Finanz relationships to Volkem" not in page.body


def test_moon_node_equals_admetos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-node-equals-admetos.md"))

    assert "blockade in emotional relationships" in page.body
    assert "deepening of contacts with the woman" in page.body
    assert "Blockade in feelings relationships" not in page.body


def test_moon_mercury_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mercury-equals-neptune.md"))

    assert "disappointing news for the people" in page.body
    assert "confused opinion of the people" in page.body
    assert "enttauschcnde Nachrichtcn for the people" not in page.body


def test_moon_mars_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mars-equals-mc.md"))

    assert "soulful emotional actions" in page.body
    assert "will of my people" in page.body
    assert "Bcseelte Gcfuhls-Handlungcn" not in page.body


def test_batch_thirteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/moon-node-equals-jupiter.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




