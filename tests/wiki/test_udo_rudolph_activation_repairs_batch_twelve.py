from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_twelfth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_twelfth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Sun/Zeus = Vernal Point](../activations/sun-zeus-equals-vernal-point.md)" not in page.body
    assert "[Sun/Zeus = Asc](../activations/sun-zeus-equals-asc.md)" not in page.body
    assert "[Sun/Apollon = Vernal Point](../activations/sun-apollon-equals-vernal-point.md)" not in page.body
    assert "[Sun/Apollon = Cupido](../activations/sun-apollon-equals-cupido.md)" not in page.body
    assert "[Sun/Apollon = Vulcanus](../activations/sun-apollon-equals-vulcanus.md)" not in page.body
    assert "[Sun/Admetos = MC](../activations/sun-admetos-equals-mc.md)" not in page.body
    assert "[Sun/Admetos = Neptune](../activations/sun-admetos-equals-neptune.md)" not in page.body
    assert "[Sun/Vulcanus = Vernal Point](../activations/sun-vulcanus-equals-vernal-point.md)" not in page.body
    assert "[Sun/Vulcanus = Moon](../activations/sun-vulcanus-equals-moon.md)" not in page.body
    assert "[Sun/Poseidon = Uranus](../activations/sun-poseidon-equals-uranus.md)" not in page.body
    assert "[Sun/Poseidon = Neptune](../activations/sun-poseidon-equals-neptune.md)" not in page.body
    assert "[Sun/Poseidon = Cupido](../activations/sun-poseidon-equals-cupido.md)" not in page.body


def test_sun_zeus_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-zeus-equals-vernal-point.md"))

    assert "fire on the day in public" in page.body
    assert "public performance center" in page.body
    assert "fire at the day in the C)fkntiichkcit" not in page.body


def test_sun_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-apollon-equals-vulcanus.md"))

    assert "expansion of masculine power" in page.body
    assert "growing power of a person" in page.body
    assert "Ausdehnung the mannlichen force" not in page.body


def test_sun_admetos_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-admetos-equals-mc.md"))

    assert "my bodily circulation" in page.body
    assert "soulful depth of a person" in page.body
    assert "my schwerer body" not in page.body


def test_sun_poseidon_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-poseidon-equals-cupido.md"))

    assert "insightful community of persons" in page.body
    assert "reasonable human community" in page.body
    assert "Einsichtige community of persons" not in page.body


def test_batch_twelve_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/sun-zeus-equals-vernal-point.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




