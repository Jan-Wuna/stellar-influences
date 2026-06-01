from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_ninth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_ninth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Sun/Node = Vernal Point](../activations/sun-node-equals-vernal-point.md)" not in page.body
    assert "[Sun/Node = Asc](../activations/sun-node-equals-asc.md)" not in page.body
    assert "[Sun/Node = Pluto](../activations/sun-node-equals-pluto.md)" not in page.body
    assert "[Sun/Node = Cupido](../activations/sun-node-equals-cupido.md)" not in page.body
    assert "[Sun/Mercury = Vernal Point](../activations/sun-mercury-equals-vernal-point.md)" not in page.body
    assert "[Sun/Mercury = Saturn](../activations/sun-mercury-equals-saturn.md)" not in page.body
    assert "[Sun/Mercury = Uranus](../activations/sun-mercury-equals-uranus.md)" not in page.body
    assert "[Sun/Mercury = Neptune](../activations/sun-mercury-equals-neptune.md)" not in page.body
    assert "[Sun/Mercury = Pluto](../activations/sun-mercury-equals-pluto.md)" not in page.body
    assert "[Sun/Mercury = Cupido](../activations/sun-mercury-equals-cupido.md)" not in page.body
    assert "[Sun/Mars = MC](../activations/sun-mars-equals-mc.md)" not in page.body
    assert "[Sun/Mars = Uranus](../activations/sun-mars-equals-uranus.md)" not in page.body


def test_sun_node_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-node-equals-vernal-point.md"))

    assert "human bonds in public life" in page.body
    assert "connection to the public center" in page.body
    assert "Personcn Bcziehungen in the public life" not in page.body


def test_sun_node_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-node-equals-pluto.md"))

    assert "development of a personal connection" in page.body
    assert "changing personal connections" in page.body
    assert "connection to a Entwicklungs center" not in page.body


def test_sun_mercury_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-mercury-equals-neptune.md"))

    assert "reports about subtle bodies" in page.body
    assert "uncertainty in personal conversations" in page.body
    assert "Bcrichte about feinstoffliche body" not in page.body


def test_sun_mars_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-mars-equals-uranus.md"))

    assert "exciting workday" in page.body
    assert "technical work center" in page.body
    assert "Aufregender work day" not in page.body


def test_batch_nine_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/sun-node-equals-vernal-point.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




