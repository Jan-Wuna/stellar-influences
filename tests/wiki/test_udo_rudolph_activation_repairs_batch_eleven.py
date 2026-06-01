from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_eleventh_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_eleventh_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Sun/Neptune = Hades](../activations/sun-neptune-equals-hades.md)" not in page.body
    assert "[Sun/Neptune = Kronos](../activations/sun-neptune-equals-kronos.md)" not in page.body
    assert "[Sun/Pluto = Vernal Point](../activations/sun-pluto-equals-vernal-point.md)" not in page.body
    assert "[Sun/Pluto = Asc](../activations/sun-pluto-equals-asc.md)" not in page.body
    assert "[Sun/Pluto = Uranus](../activations/sun-pluto-equals-uranus.md)" not in page.body
    assert "[Sun/Pluto = Neptune](../activations/sun-pluto-equals-neptune.md)" not in page.body
    assert "[Sun/Pluto = Cupido](../activations/sun-pluto-equals-cupido.md)" not in page.body
    assert "[Sun/Cupido = Vernal Point](../activations/sun-cupido-equals-vernal-point.md)" not in page.body
    assert "[Sun/Cupido = Uranus](../activations/sun-cupido-equals-uranus.md)" not in page.body
    assert "[Sun/Cupido = Neptune](../activations/sun-cupido-equals-neptune.md)" not in page.body
    assert "[Sun/Cupido = Pluto](../activations/sun-cupido-equals-pluto.md)" not in page.body
    assert "[Sun/Cupido = Admetos](../activations/sun-cupido-equals-admetos.md)" not in page.body


def test_sun_neptune_equals_hades_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-neptune-equals-hades.md"))

    assert "man disappointed through hardship" in page.body
    assert "hidden bodily poison" in page.body
    assert "through Not enttauschter man" not in page.body


def test_sun_pluto_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-pluto-equals-vernal-point.md"))

    assert "developmental center in public life" in page.body
    assert "personal changes in public life" in page.body
    assert "Jahrcs exchange in the public" not in page.body


def test_sun_pluto_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-pluto-equals-neptune.md"))

    assert "disappointing development of the person" in page.body
    assert "growing refinement of the body" in page.body
    assert "Enttauschende development of the people" not in page.body


def test_sun_cupido_equals_admetos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-cupido-equals-admetos.md"))

    assert "depressed human community" in page.body
    assert "personal restrictions in the community" in page.body
    assert "Deprimierte menschliche community" not in page.body


def test_batch_eleven_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/sun-neptune-equals-hades.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




