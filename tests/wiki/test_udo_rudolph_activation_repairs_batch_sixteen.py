from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_sixteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_sixteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Hades = Vulcanus](../activations/moon-hades-equals-vulcanus.md)" not in page.body
    assert "[Moon/Zeus = Vernal Point](../activations/moon-zeus-equals-vernal-point.md)" not in page.body
    assert "[Moon/Zeus = MC](../activations/moon-zeus-equals-mc.md)" not in page.body
    assert "[Moon/Zeus = Asc](../activations/moon-zeus-equals-asc.md)" not in page.body
    assert "[Moon/Zeus = Sun](../activations/moon-zeus-equals-sun.md)" not in page.body
    assert "[Moon/Zeus = Saturn](../activations/moon-zeus-equals-saturn.md)" not in page.body
    assert "[Moon/Zeus = Uranus](../activations/moon-zeus-equals-uranus.md)" not in page.body
    assert "[Moon/Zeus = Pluto](../activations/moon-zeus-equals-pluto.md)" not in page.body
    assert "[Moon/Zeus = Cupido](../activations/moon-zeus-equals-cupido.md)" not in page.body
    assert "[Moon/Kronos = MC](../activations/moon-kronos-equals-mc.md)" not in page.body
    assert "[Moon/Kronos = Mars](../activations/moon-kronos-equals-mars.md)" not in page.body
    assert "[Moon/Apollon = MC](../activations/moon-apollon-equals-mc.md)" not in page.body


def test_moon_hades_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-hades-equals-vulcanus.md"))

    assert "criminal violence against women" in page.body
    assert "hidden emotional influence" in page.body
    assert "kriminelle force against women" not in page.body


def test_moon_zeus_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-zeus-equals-mc.md"))

    assert "leadership of my woman" in page.body
    assert "my creative emotional nature" in page.body
    assert "FUhrung my women" not in page.body


def test_moon_kronos_equals_mars_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-kronos-equals-mars.md"))

    assert "authority of the will of a woman" in page.body
    assert "preferential treatment of the woman" in page.body
    assert "authority the Willens a women" not in page.body


def test_moon_apollon_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-apollon-equals-mc.md"))

    assert "ensouled emotional knowledge" in page.body
    assert "hour of my success" in page.body
    assert "Freiheit my people" not in page.body


def test_batch_sixteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/moon-hades-equals-vulcanus.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




