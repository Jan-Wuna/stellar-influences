from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_third_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_third_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Mars/Saturn = Pluto](../activations/mars-saturn-equals-pluto.md)" not in page.body
    assert "[Mars/Saturn = Cupido](../activations/mars-saturn-equals-cupido.md)" not in page.body
    assert "[Mars/Uranus = Vernal Point](../activations/mars-uranus-equals-vernal-point.md)" not in page.body
    assert "[Mars/Uranus = Sun](../activations/mars-uranus-equals-sun.md)" not in page.body
    assert "[Mars/Uranus = Cupido](../activations/mars-uranus-equals-cupido.md)" not in page.body
    assert "[Mars/Pluto = Vernal Point](../activations/mars-pluto-equals-vernal-point.md)" not in page.body
    assert "[Mars/Cupido = Asc](../activations/mars-cupido-equals-asc.md)" not in page.body
    assert "[Mars/Hades = Moon](../activations/mars-hades-equals-moon.md)" not in page.body
    assert "[Mars/Kronos = Cupido](../activations/mars-kronos-equals-cupido.md)" not in page.body
    assert "[Mars/Admetos = Vernal Point](../activations/mars-admetos-equals-vernal-point.md)" not in page.body
    assert "[Mars/Admetos = Pluto](../activations/mars-admetos-equals-pluto.md)" not in page.body
    assert "[Mars/Vulcanus = Vernal Point](../activations/mars-vulcanus-equals-vernal-point.md)" not in page.body


def test_mars_saturn_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-saturn-equals-pluto.md"))

    assert "inhibited unfolding of will" in page.body
    assert "painful change of work" in page.body
    assert "work, gehemmte Willens development" not in page.body


def test_mars_uranus_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-uranus-equals-vernal-point.md"))

    assert "exciting actions in public" in page.body
    assert "technical work in public" in page.body
    assert "J\\ufrcgcnde J\\ktionen in dcr ()flcntlichkeit" not in page.body


def test_mars_cupido_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-cupido-equals-asc.md"))

    assert "shared workplace" in page.body
    assert "environmental work of a community" in page.body
    assert "Gcmeinsamer Arbeits-Platz" not in page.body


def test_mars_admetos_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-admetos-equals-pluto.md"))

    assert "thorough changes in work" in page.body
    assert "growing impulses of depression" in page.body
    assert "developing, grUndliche Veranderungcn in the Arbcit" not in page.body


def test_batch_twenty_three_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/mars-admetos-equals-pluto.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




