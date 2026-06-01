from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_seventh_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_seventh_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Venus/Asc = Vulcanus](../activations/venus-asc-equals-vulcanus.md)" not in page.body
    assert "[Mars/Asc = Vernal Point](../activations/mars-asc-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Asc = Vernal Point](../activations/jupiter-asc-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Asc = Moon](../activations/jupiter-asc-equals-moon.md)" not in page.body
    assert "[Saturn/Asc = Vernal Point](../activations/saturn-asc-equals-vernal-point.md)" not in page.body
    assert "[Saturn/Asc = Sun](../activations/saturn-asc-equals-sun.md)" not in page.body
    assert "[Uranus/Asc = Vernal Point](../activations/uranus-asc-equals-vernal-point.md)" not in page.body
    assert "[Uranus/Asc = Cupido](../activations/uranus-asc-equals-cupido.md)" not in page.body
    assert "[Neptune/Asc = Vernal Point](../activations/neptune-asc-equals-vernal-point.md)" not in page.body
    assert "[Pluto/Asc = Cupido](../activations/pluto-asc-equals-cupido.md)" not in page.body
    assert "[Asc/Cupido = Vernal Point](../activations/asc-cupido-equals-vernal-point.md)" not in page.body
    assert "[Asc/Cupido = MC](../activations/asc-cupido-equals-mc.md)" not in page.body


def test_venus_asc_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/venus-asc-equals-vulcanus.md"))

    assert "harmonious energies on the spot" in page.body
    assert "love power of the partner" in page.body
    assert "harmonische Energien at the place" not in page.body


def test_mars_asc_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-asc-equals-vernal-point.md"))

    assert "work in public places" in page.body
    assert "will of the public on the spot" in page.body
    assert "Arbcit an public places" not in page.body


def test_jupiter_asc_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-asc-equals-vernal-point.md"))

    assert "Success in the public environment" in page.body
    assert "place of public joy" in page.body
    assert "Frfolg in the Umfcld Jcr public" not in page.body


def test_asc_cupido_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/asc-cupido-equals-vernal-point.md"))

    assert "shared environment in public" in page.body
    assert "partner community in public" in page.body
    assert "n cmcinsamc lJrn world in the C)ffcntlichkcit" not in page.body


def test_udo_rudolph_pages_keep_a_single_derived_synthesis_anchor():
    factor_page = load_page(Path("wiki/factors/admetos.md"))
    activation_page = load_page(Path("wiki/activations/venus-asc-equals-vulcanus.md"))

    assert factor_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1




