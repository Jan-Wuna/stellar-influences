from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_second_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_second_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Venus/Neptune = Apollon](../activations/venus-neptune-equals-apollon.md)" not in page.body
    assert "[Venus/Pluto = Vernal Point](../activations/venus-pluto-equals-vernal-point.md)" not in page.body
    assert "[Venus/Pluto = Neptune](../activations/venus-pluto-equals-neptune.md)" not in page.body
    assert "[Venus/Cupido = Vernal Point](../activations/venus-cupido-equals-vernal-point.md)" not in page.body
    assert "[Venus/Cupido = Asc](../activations/venus-cupido-equals-asc.md)" not in page.body
    assert "[Venus/Hades = Vernal Point](../activations/venus-hades-equals-vernal-point.md)" not in page.body
    assert "[Mars/Jupiter = Vernal Point](../activations/mars-jupiter-equals-vernal-point.md)" not in page.body
    assert "[Mars/Jupiter = Asc](../activations/mars-jupiter-equals-asc.md)" not in page.body
    assert "[Mars/Jupiter = Cupido](../activations/mars-jupiter-equals-cupido.md)" not in page.body
    assert "[Mars/Jupiter = Vulcanus](../activations/mars-jupiter-equals-vulcanus.md)" not in page.body
    assert "[Mars/Saturn = Sun](../activations/mars-saturn-equals-sun.md)" not in page.body
    assert "[Mars/Saturn = Neptune](../activations/mars-saturn-equals-neptune.md)" not in page.body


def test_venus_neptune_equals_apollon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/venus-neptune-equals-apollon.md"))

    assert "expansion of harmony through sensitivity" in page.body
    assert "refined experiences of love" in page.body
    assert "Enttauschung in the love erfahren" not in page.body


def test_venus_cupido_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/venus-cupido-equals-vernal-point.md"))

    assert "shared joy in public" in page.body
    assert "public art community" in page.body
    assert "Fricdens art in the CJffcntlichkeit" not in page.body


def test_mars_jupiter_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-jupiter-equals-vulcanus.md"))

    assert "successful activity of power" in page.body
    assert "powerful legal actions" in page.body
    assert "erfolgreiche power activity" not in page.body


def test_mars_saturn_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-saturn-equals-neptune.md"))

    assert "disappointing loss of work" in page.body
    assert "patient work with water" in page.body
    assert "Enttauschender loss the work" not in page.body


def test_batch_twenty_two_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/mars-saturn-equals-neptune.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




