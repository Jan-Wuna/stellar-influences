from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_third_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_third_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Vernal Point/Uranus = Kronos](../activations/vernal-point-uranus-equals-kronos.md)" not in page.body
    assert "[Vernal Point/Neptune = MC](../activations/vernal-point-neptune-equals-mc.md)" not in page.body
    assert "[Vernal Point/Neptune = Asc](../activations/vernal-point-neptune-equals-asc.md)" not in page.body
    assert "[Vernal Point/Pluto = Uranus](../activations/vernal-point-pluto-equals-uranus.md)" not in page.body
    assert "[Vernal Point/Pluto = Neptune](../activations/vernal-point-pluto-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Cupido = Moon](../activations/vernal-point-cupido-equals-moon.md)" not in page.body
    assert "[Vernal Point/Cupido = Saturn](../activations/vernal-point-cupido-equals-saturn.md)" not in page.body
    assert "[Vernal Point/Cupido = Neptune](../activations/vernal-point-cupido-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Cupido = Pluto](../activations/vernal-point-cupido-equals-pluto.md)" not in page.body
    assert "[Vernal Point/Cupido = Kronos](../activations/vernal-point-cupido-equals-kronos.md)" not in page.body
    assert "[Vernal Point/Cupido = Admetos](../activations/vernal-point-cupido-equals-admetos.md)" not in page.body
    assert "[Vernal Point/Zeus = Mercury](../activations/vernal-point-zeus-equals-mercury.md)" not in page.body


def test_vernal_point_uranus_equals_kronos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-uranus-equals-kronos.md"))

    assert "special excitement in public" in page.body
    assert "important renewals in public life" in page.body
    assert "impulsive authoritat" not in page.body


def test_vernal_point_neptune_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-neptune-equals-mc.md"))

    assert "my disappointments in public life" in page.body
    assert "my uncertainty in public" in page.body
    assert "Enquiries" not in page.body


def test_vernal_point_cupido_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-cupido-equals-moon.md"))

    assert "women's communities in public life" in page.body
    assert "people's art in public" in page.body
    assert "hour the community" not in page.body


def test_vernal_point_zeus_equals_mercury_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-zeus-equals-mercury.md"))

    assert "leadership talks in public" in page.body
    assert "news about public achievements" in page.body
    assert "FUhrungs conversation" not in page.body




