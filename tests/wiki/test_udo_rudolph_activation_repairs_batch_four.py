from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_fourth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_fourth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Vernal Point/Zeus = Saturn](../activations/vernal-point-zeus-equals-saturn.md)" not in page.body
    assert "[Vernal Point/Zeus = Uranus](../activations/vernal-point-zeus-equals-uranus.md)" not in page.body
    assert "[Vernal Point/Zeus = Hades](../activations/vernal-point-zeus-equals-hades.md)" not in page.body
    assert "[Vernal Point/Kronos = Asc](../activations/vernal-point-kronos-equals-asc.md)" not in page.body
    assert "[Vernal Point/Apollon = Cupido](../activations/vernal-point-apollon-equals-cupido.md)" not in page.body
    assert "[Vernal Point/Apollon = Hades](../activations/vernal-point-apollon-equals-hades.md)" not in page.body
    assert "[Vernal Point/Admetos = Uranus](../activations/vernal-point-admetos-equals-uranus.md)" not in page.body
    assert "[Vernal Point/Admetos = Neptune](../activations/vernal-point-admetos-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Vulcanus = Asc](../activations/vernal-point-vulcanus-equals-asc.md)" not in page.body
    assert "[Sun/MC = Vernal Point](../activations/sun-mc-equals-vernal-point.md)" not in page.body
    assert "[Sun/MC = Vulcanus](../activations/sun-mc-equals-vulcanus.md)" not in page.body
    assert "[Moon/MC = Saturn](../activations/moon-mc-equals-saturn.md)" not in page.body


def test_vernal_point_zeus_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-zeus-equals-saturn.md"))

    assert "disturbed public leadership" in page.body
    assert "loss heavy efforts in public" in page.body
    assert "Community programme" not in page.body


def test_vernal_point_apollon_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-apollon-equals-cupido.md"))

    assert "expansion of a community in public life" in page.body
    assert "public economic community" in page.body
    assert "economic statistics" not in page.body


def test_sun_mc_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-mc-equals-vernal-point.md"))

    assert "my day in public" in page.body
    assert "soul of the man in public life" in page.body
    assert "sound of munich" not in page.body


def test_moon_mc_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mc-equals-saturn.md"))

    assert "tasks of the female soul" in page.body
    assert "emotional pain of the woman" in page.body
    assert "strangled people's soul" not in page.body




