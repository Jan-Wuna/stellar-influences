from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_fifth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_fifth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Jupiter/Zeus = Asc](../activations/jupiter-zeus-equals-asc.md)" not in page.body
    assert "[Jupiter/Kronos = Moon](../activations/jupiter-kronos-equals-moon.md)" not in page.body
    assert "[Jupiter/Kronos = Cupido](../activations/jupiter-kronos-equals-cupido.md)" not in page.body
    assert "[Jupiter/Apollon = Vernal Point](../activations/jupiter-apollon-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Apollon = Asc](../activations/jupiter-apollon-equals-asc.md)" not in page.body
    assert "[Jupiter/Apollon = Moon](../activations/jupiter-apollon-equals-moon.md)" not in page.body
    assert "[Jupiter/Apollon = Cupido](../activations/jupiter-apollon-equals-cupido.md)" not in page.body
    assert "[Jupiter/Admetos = Cupido](../activations/jupiter-admetos-equals-cupido.md)" not in page.body
    assert "[Jupiter/Vulcanus = Asc](../activations/jupiter-vulcanus-equals-asc.md)" not in page.body
    assert "[Saturn/Neptune = Node](../activations/saturn-neptune-equals-node.md)" not in page.body
    assert "[Saturn/Neptune = Cupido](../activations/saturn-neptune-equals-cupido.md)" not in page.body
    assert "[Saturn/Pluto = Cupido](../activations/saturn-pluto-equals-cupido.md)" not in page.body


def test_jupiter_zeus_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-zeus-equals-asc.md"))

    assert "successful striving toward goals of a place" in page.body
    assert "performance successes of the partner" in page.body
    assert "Erft)lgreichcs Zielstrcbcn cincs 0 1ies" not in page.body


def test_jupiter_apollon_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-apollon-equals-vernal-point.md"))

    assert "successful expansion in public" in page.body
    assert "commercial advantages in public" in page.body
    assert "money Handel in the public" not in page.body


def test_saturn_neptune_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-neptune-equals-cupido.md"))

    assert "burdened future of the community" in page.body
    assert "shared air problems" in page.body
    assert "Belastete future the community" not in page.body


def test_saturn_pluto_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-pluto-equals-cupido.md"))

    assert "patient development of a community" in page.body
    assert "change of a community through separation" in page.body
    assert "Geduldige development of a community" not in page.body


def test_batch_twenty_five_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/saturn-neptune-equals-cupido.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




