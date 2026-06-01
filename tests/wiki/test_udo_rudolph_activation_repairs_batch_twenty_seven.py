from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twenty_seventh_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twenty_seventh_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Uranus/Pluto = Vernal Point](../activations/uranus-pluto-equals-vernal-point.md)" not in page.body
    assert "[Uranus/Cupido = Pluto](../activations/uranus-cupido-equals-pluto.md)" not in page.body
    assert "[Uranus/Cupido = Admetos](../activations/uranus-cupido-equals-admetos.md)" not in page.body
    assert "[Uranus/Hades = Vernal Point](../activations/uranus-hades-equals-vernal-point.md)" not in page.body
    assert "[Uranus/Kronos = Vernal Point](../activations/uranus-kronos-equals-vernal-point.md)" not in page.body
    assert "[Uranus/Kronos = Asc](../activations/uranus-kronos-equals-asc.md)" not in page.body
    assert "[Uranus/Kronos = Cupido](../activations/uranus-kronos-equals-cupido.md)" not in page.body
    assert "[Uranus/Poseidon = Vernal Point](../activations/uranus-poseidon-equals-vernal-point.md)" not in page.body
    assert "[Uranus/Poseidon = Mars](../activations/uranus-poseidon-equals-mars.md)" not in page.body
    assert "[Neptune/Pluto = Moon](../activations/neptune-pluto-equals-moon.md)" not in page.body
    assert "[Neptune/Cupido = Pluto](../activations/neptune-cupido-equals-pluto.md)" not in page.body
    assert "[Neptune/Apollon = Vulcanus](../activations/neptune-apollon-equals-vulcanus.md)" not in page.body


def test_uranus_pluto_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/uranus-pluto-equals-vernal-point.md"))

    assert "exciting changes in public" in page.body
    assert "growing tensions in public life" in page.body
    assert "development public Unruhe" not in page.body


def test_uranus_kronos_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/uranus-kronos-equals-cupido.md"))

    assert "shared steering of technology" in page.body
    assert "important shared events" in page.body
    assert "common Lenkung derTechnik" not in page.body


def test_neptune_pluto_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-pluto-equals-moon.md"))

    assert "dissolving developments of a people" in page.body
    assert "growing expectations of a woman" in page.body
    assert "Auflosungs Entwicklungen a people" not in page.body


def test_neptune_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/neptune-apollon-equals-vulcanus.md"))

    assert "expansion of water power" in page.body
    assert "feign knowledge and power" in page.body
    assert "Ausdehnung of water Kraft" not in page.body


def test_batch_twenty_seven_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/neptune-apollon-equals-vulcanus.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




