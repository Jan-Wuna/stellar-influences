from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_fourth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_fourth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Mars/Vulcanus = Sun](../activations/mars-vulcanus-equals-sun.md)" not in page.body
    assert "[Mars/Vulcanus = Cupido](../activations/mars-vulcanus-equals-cupido.md)" not in page.body
    assert "[Jupiter/Uranus = Vernal Point](../activations/jupiter-uranus-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Neptune = Vernal Point](../activations/jupiter-neptune-equals-vernal-point.md)" not in page.body
    assert "[Jupiter/Neptune = Hades](../activations/jupiter-neptune-equals-hades.md)" not in page.body
    assert "[Jupiter/Cupido = MC](../activations/jupiter-cupido-equals-mc.md)" not in page.body
    assert "[Jupiter/Cupido = Sun](../activations/jupiter-cupido-equals-sun.md)" not in page.body
    assert "[Jupiter/Cupido = Mars](../activations/jupiter-cupido-equals-mars.md)" not in page.body
    assert "[Jupiter/Cupido = Pluto](../activations/jupiter-cupido-equals-pluto.md)" not in page.body
    assert "[Jupiter/Cupido = Hades](../activations/jupiter-cupido-equals-hades.md)" not in page.body
    assert "[Jupiter/Cupido = Admetos](../activations/jupiter-cupido-equals-admetos.md)" not in page.body
    assert "[Jupiter/Cupido = Vulcanus](../activations/jupiter-cupido-equals-vulcanus.md)" not in page.body


def test_mars_vulcanus_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mars-vulcanus-equals-sun.md"))

    assert "work of a center of power" in page.body
    assert "personal strength of will" in page.body
    assert "work a power Zentrums" not in page.body


def test_jupiter_uranus_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-uranus-equals-vernal-point.md"))

    assert "success impulses in public" in page.body
    assert "advantages through technology in public life" in page.body
    assert "Aufregung wcgcn public Gelder" not in page.body


def test_jupiter_cupido_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-cupido-equals-mc.md"))

    assert "shared joy of the soul" in page.body
    assert "my rights in the community" in page.body
    assert "gllicklichc Scclcn--community" not in page.body


def test_jupiter_cupido_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/jupiter-cupido-equals-vulcanus.md"))

    assert "influence of a legal community" in page.body
    assert "strong financial community" in page.body
    assert "erfolgreiche power the community" not in page.body


def test_batch_twenty_four_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/jupiter-cupido-equals-vulcanus.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




