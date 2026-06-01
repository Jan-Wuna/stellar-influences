from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_fifteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_fifteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Uranus = Poseidon](../activations/moon-uranus-equals-poseidon.md)" not in page.body
    assert "[Moon/Neptune = Vernal Point](../activations/moon-neptune-equals-vernal-point.md)" not in page.body
    assert "[Moon/Pluto = Cupido](../activations/moon-pluto-equals-cupido.md)" not in page.body
    assert "[Moon/Pluto = Vulcanus](../activations/moon-pluto-equals-vulcanus.md)" not in page.body
    assert "[Moon/Cupido = Vernal Point](../activations/moon-cupido-equals-vernal-point.md)" not in page.body
    assert "[Moon/Cupido = MC](../activations/moon-cupido-equals-mc.md)" not in page.body
    assert "[Moon/Cupido = Neptune](../activations/moon-cupido-equals-neptune.md)" not in page.body
    assert "[Moon/Cupido = Kronos](../activations/moon-cupido-equals-kronos.md)" not in page.body
    assert "[Moon/Hades = Vernal Point](../activations/moon-hades-equals-vernal-point.md)" not in page.body
    assert "[Moon/Hades = Asc](../activations/moon-hades-equals-asc.md)" not in page.body
    assert "[Moon/Hades = Sun](../activations/moon-hades-equals-sun.md)" not in page.body
    assert "[Moon/Hades = Node](../activations/moon-hades-equals-node.md)" not in page.body


def test_moon_uranus_equals_poseidon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-uranus-equals-poseidon.md"))

    assert "spiritual impulses of the woman" in page.body
    assert "reasonable technique of a people" in page.body
    assert "spiritual Impulse of women" not in page.body


def test_moon_pluto_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-pluto-equals-cupido.md"))

    assert "development of an emotional community" in page.body
    assert "union of women for a development" in page.body
    assert "Entwicklung einer GemUts-Gemeinschaft" not in page.body


def test_moon_cupido_equals_kronos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-cupido-equals-kronos.md"))

    assert "special emotional community" in page.body
    assert "community of respected women" in page.body
    assert "Besondere Gemtits community" not in page.body


def test_moon_hades_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-hades-equals-sun.md"))

    assert "service of the woman to the man" in page.body
    assert "personal renunciation of the woman" in page.body
    assert "Dienst of women at the man" not in page.body


def test_batch_fifteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/moon-uranus-equals-poseidon.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




