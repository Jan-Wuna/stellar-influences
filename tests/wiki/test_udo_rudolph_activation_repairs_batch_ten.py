from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_tenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_tenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Sun/Mars = Pluto](../activations/sun-mars-equals-pluto.md)" not in page.body
    assert "[Sun/Jupiter = Uranus](../activations/sun-jupiter-equals-uranus.md)" not in page.body
    assert "[Sun/Jupiter = Pluto](../activations/sun-jupiter-equals-pluto.md)" not in page.body
    assert "[Sun/Jupiter = Cupido](../activations/sun-jupiter-equals-cupido.md)" not in page.body
    assert "[Sun/Saturn = Neptune](../activations/sun-saturn-equals-neptune.md)" not in page.body
    assert "[Sun/Saturn = Pluto](../activations/sun-saturn-equals-pluto.md)" not in page.body
    assert "[Sun/Saturn = Cupido](../activations/sun-saturn-equals-cupido.md)" not in page.body
    assert "[Sun/Uranus = MC](../activations/sun-uranus-equals-mc.md)" not in page.body
    assert "[Sun/Uranus = Cupido](../activations/sun-uranus-equals-cupido.md)" not in page.body
    assert "[Sun/Uranus = Admetos](../activations/sun-uranus-equals-admetos.md)" not in page.body
    assert "[Sun/Neptune = Vernal Point](../activations/sun-neptune-equals-vernal-point.md)" not in page.body
    assert "[Sun/Neptune = Jupiter](../activations/sun-neptune-equals-jupiter.md)" not in page.body


def test_sun_mars_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-mars-equals-pluto.md"))

    assert "developmental work of a man" in page.body
    assert "daily changes in the work" in page.body
    assert "Entwicklungs work a man" not in page.body


def test_sun_jupiter_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-jupiter-equals-uranus.md"))

    assert "excitement in the financial center" in page.body
    assert "surprising human joy" in page.body
    assert "Aufregung in the Gcld Zcntrum" not in page.body


def test_sun_uranus_equals_admetos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-uranus-equals-admetos.md"))

    assert "stimulation of the body's circulation" in page.body
    assert "resistance against human reforms" in page.body
    assert "Dynamisierung the body Kreislaufes" not in page.body


def test_sun_neptune_equals_jupiter_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-neptune-equals-jupiter.md"))

    assert "financial weakness of the man" in page.body
    assert "uncertain legal matters for the person" in page.body
    assert "Finanz Schwache the man" not in page.body


def test_batch_ten_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/sun-mars-equals-pluto.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




