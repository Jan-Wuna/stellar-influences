from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirtieth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirtieth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Cupido/Hades = Asc](../activations/cupido-hades-equals-asc.md)" not in page.body
    assert "[Cupido/Hades = Moon](../activations/cupido-hades-equals-moon.md)" not in page.body
    assert "[Cupido/Hades = Pluto](../activations/cupido-hades-equals-pluto.md)" not in page.body
    assert "[Cupido/Zeus = Sun](../activations/cupido-zeus-equals-sun.md)" not in page.body
    assert "[Cupido/Zeus = Uranus](../activations/cupido-zeus-equals-uranus.md)" not in page.body
    assert "[Cupido/Zeus = Kronos](../activations/cupido-zeus-equals-kronos.md)" not in page.body
    assert "[Cupido/Kronos = Vernal Point](../activations/cupido-kronos-equals-vernal-point.md)" not in page.body
    assert "[Cupido/Kronos = Jupiter](../activations/cupido-kronos-equals-jupiter.md)" not in page.body
    assert "[Cupido/Kronos = Hades](../activations/cupido-kronos-equals-hades.md)" not in page.body
    assert "[Cupido/Apollon = Vernal Point](../activations/cupido-apollon-equals-vernal-point.md)" not in page.body
    assert "[Cupido/Apollon = Moon](../activations/cupido-apollon-equals-moon.md)" not in page.body
    assert "[Cupido/Apollon = Uranus](../activations/cupido-apollon-equals-uranus.md)" not in page.body


def test_cupido_hades_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-hades-equals-asc.md"))

    assert "old place of art" in page.body
    assert "shared secret with the partner" in page.body
    assert "old age art" not in page.body


def test_cupido_zeus_equals_kronos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-zeus-equals-kronos.md"))

    assert "special efforts of a community" in page.body
    assert "goals of a hierarchical community" in page.body
    assert "Besondere Anstrengungen of a community" not in page.body


def test_cupido_kronos_equals_jupiter_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-kronos-equals-jupiter.md"))

    assert "reputation of a legal community" in page.body
    assert "leadership of a financial community" in page.body
    assert "Ansehen a legal" not in page.body


def test_cupido_apollon_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-apollon-equals-uranus.md"))

    assert "dynamic trading community" in page.body
    assert "scientific reform community" in page.body
    assert "Dynamische Handels community" not in page.body


def test_batch_thirty_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/cupido-apollon-equals-uranus.md"))
    comparative_page = load_page(Path("wiki/factors/cupido.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1


