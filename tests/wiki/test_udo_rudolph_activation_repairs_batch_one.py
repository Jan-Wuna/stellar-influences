from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_first_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_first_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Vernal Point/MC = Saturn](../activations/vernal-point-mc-equals-saturn.md)" not in page.body
    assert "[Vernal Point/Asc = Neptune](../activations/vernal-point-asc-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Asc = Pluto](../activations/vernal-point-asc-equals-pluto.md)" not in page.body
    assert "[Vernal Point/Asc = Hades](../activations/vernal-point-asc-equals-hades.md)" not in page.body
    assert "[Vernal Point/Sun = Asc](../activations/vernal-point-sun-equals-asc.md)" not in page.body
    assert "[Vernal Point/Node = Pluto](../activations/vernal-point-node-equals-pluto.md)" not in page.body
    assert "[Vernal Point/Node = Cupido](../activations/vernal-point-node-equals-cupido.md)" not in page.body
    assert "[Vernal Point/Mercury = Neptune](../activations/vernal-point-mercury-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Venus = Cupido](../activations/vernal-point-venus-equals-cupido.md)" not in page.body
    assert "[Vernal Point/Venus = Vulcanus](../activations/vernal-point-venus-equals-vulcanus.md)" not in page.body
    assert "[Vernal Point/Mars = Asc](../activations/vernal-point-mars-equals-asc.md)" not in page.body
    assert "[Vernal Point/Mars = Cupido](../activations/vernal-point-mars-equals-cupido.md)" not in page.body


def test_vernal_point_mc_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-mc-equals-saturn.md"))

    assert "my burden in public" in page.body
    assert "my losses in public" in page.body
    assert "In public, in public" not in page.body


def test_vernal_point_asc_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-asc-equals-neptune.md"))

    assert "false partner in public life" in page.body
    assert "water in the public environment" in page.body
    assert "free movement of persons" not in page.body


def test_vernal_point_venus_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-venus-equals-vulcanus.md"))

    assert "artistic influence in public" in page.body
    assert "power of joy in public life" in page.body
    assert "influence3" not in page.body


def test_vernal_point_mars_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-mars-equals-cupido.md"))

    assert "public action community" in page.body
    assert "public community work" in page.body
    assert "J\\k -tions" not in page.body




