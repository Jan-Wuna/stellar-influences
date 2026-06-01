from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_first_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_first_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Mercury/Cupido = Uranus](../activations/mercury-cupido-equals-uranus.md)" not in page.body
    assert "[Mercury/Cupido = Neptune](../activations/mercury-cupido-equals-neptune.md)" not in page.body
    assert "[Mercury/Cupido = Pluto](../activations/mercury-cupido-equals-pluto.md)" not in page.body
    assert "[Mercury/Hades = Vernal Point](../activations/mercury-hades-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Kronos = Vernal Point](../activations/mercury-kronos-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Apollon = Uranus](../activations/mercury-apollon-equals-uranus.md)" not in page.body
    assert "[Mercury/Vulcanus = Vernal Point](../activations/mercury-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Mercury/Vulcanus = MC](../activations/mercury-vulcanus-equals-mc.md)" not in page.body
    assert "[Mercury/Vulcanus = Venus](../activations/mercury-vulcanus-equals-venus.md)" not in page.body
    assert "[Mercury/Poseidon = Pluto](../activations/mercury-poseidon-equals-pluto.md)" not in page.body
    assert "[Venus/Mars = Vernal Point](../activations/venus-mars-equals-vernal-point.md)" not in page.body
    assert "[Venus/Jupiter = Vernal Point](../activations/venus-jupiter-equals-vernal-point.md)" not in page.body


def test_mercury_cupido_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-cupido-equals-uranus.md"))

    assert "excited conversations in the community" in page.body
    assert "innovations in media communities" in page.body
    assert "Aufregungen about eine youth community" not in page.body


def test_mercury_cupido_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-cupido-equals-neptune.md"))

    assert "foreign language community" in page.body
    assert "evolutionary conversations in the community" in page.body
    assert "Fremde language community" not in page.body


def test_mercury_vulcanus_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-vulcanus-equals-mc.md"))

    assert "influential soul language" in page.body
    assert "my thought power" in page.body
    assert "ich schreibe about power" not in page.body


def test_venus_jupiter_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/venus-jupiter-equals-vernal-point.md"))

    assert "successful beautifications in public life" in page.body
    assert "advantage in public life through beauty" in page.body
    assert "Erfolgreichc Vcrschoncrungcn in the public life" not in page.body


def test_batch_twenty_one_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/mercury-vulcanus-equals-mc.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




