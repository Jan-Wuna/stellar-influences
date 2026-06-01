from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_eighth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_eighth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Asc/Cupido = Sun](../activations/asc-cupido-equals-sun.md)" not in page.body
    assert "[Asc/Cupido = Pluto](../activations/asc-cupido-equals-pluto.md)" not in page.body
    assert "[Asc/Hades = Uranus](../activations/asc-hades-equals-uranus.md)" not in page.body
    assert "[Asc/Hades = Vulcanus](../activations/asc-hades-equals-vulcanus.md)" not in page.body
    assert "[Asc/Zeus = Vernal Point](../activations/asc-zeus-equals-vernal-point.md)" not in page.body
    assert "[Asc/Zeus = Cupido](../activations/asc-zeus-equals-cupido.md)" not in page.body
    assert "[Asc/Kronos = Vernal Point](../activations/asc-kronos-equals-vernal-point.md)" not in page.body
    assert "[Asc/Apollon = Sun](../activations/asc-apollon-equals-sun.md)" not in page.body
    assert "[Asc/Admetos = Uranus](../activations/asc-admetos-equals-uranus.md)" not in page.body
    assert "[Asc/Vulcanus = Vernal Point](../activations/asc-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Asc/Vulcanus = Apollon](../activations/asc-vulcanus-equals-apollon.md)" not in page.body
    assert "[Sun/Moon = Neptune](../activations/sun-moon-equals-neptune.md)" not in page.body


def test_asc_cupido_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/asc-cupido-equals-sun.md"))

    assert "community center on the spot" in page.body
    assert "personal partner community" in page.body
    assert "community center at the place" not in page.body


def test_asc_hades_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/asc-hades-equals-uranus.md"))

    assert "excitements because of a polluted environment" in page.body
    assert "reform against environmental criminality" in page.body
    assert "Aufregungen wegen vcrschmutzter environment" not in page.body


def test_asc_zeus_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/asc-zeus-equals-vernal-point.md"))

    assert "fire in the environment of public life" in page.body
    assert "public environmental goals" in page.body
    assert "fire in the Umfcld the public Lcbens" not in page.body


def test_sun_moon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-moon-equals-neptune.md"))

    assert "bodily weakness of the woman" in page.body
    assert "uncertainty between woman and man" in page.body
    assert "karperlichc Schwache of women" not in page.body


def test_batch_eight_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/asc-cupido-equals-sun.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




