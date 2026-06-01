from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_sixth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_sixth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[MC/Cupido = Pluto](../activations/mc-cupido-equals-pluto.md)" not in page.body
    assert "[MC/Hades = Moon](../activations/mc-hades-equals-moon.md)" not in page.body
    assert "[MC/Zeus = Vulcanus](../activations/mc-zeus-equals-vulcanus.md)" not in page.body
    assert "[MC/Vulcanus = Asc](../activations/mc-vulcanus-equals-asc.md)" not in page.body
    assert "[MC/Vulcanus = Moon](../activations/mc-vulcanus-equals-moon.md)" not in page.body
    assert "[MC/Poseidon = Vulcanus](../activations/mc-poseidon-equals-vulcanus.md)" not in page.body
    assert "[Moon/Asc = Neptune](../activations/moon-asc-equals-neptune.md)" not in page.body
    assert "[Moon/Asc = Pluto](../activations/moon-asc-equals-pluto.md)" not in page.body
    assert "[Node/Asc = Vernal Point](../activations/node-asc-equals-vernal-point.md)" not in page.body
    assert "[Node/Asc = Neptune](../activations/node-asc-equals-neptune.md)" not in page.body
    assert "[Mercury/Asc = Vernal Point](../activations/mercury-asc-equals-vernal-point.md)" not in page.body
    assert "[Venus/Asc = Vernal Point](../activations/venus-asc-equals-vernal-point.md)" not in page.body


def test_mc_cupido_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mc-cupido-equals-pluto.md"))

    assert "Inspired artistic development" in page.body
    assert "inner growth of a community" in page.body
    assert "soulful art" not in page.body


def test_mc_hades_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mc-hades-equals-moon.md"))

    assert "Deprivation regarding the woman" in page.body
    assert "hidden soul of the woman" in page.body
    assert "getahrdete soul of women" not in page.body


def test_node_asc_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-asc-equals-neptune.md"))

    assert "Dissolution of a partner relationship" in page.body
    assert "contacts with the metaphysical environment" in page.body
    assert "Auflosung a partner relationships" not in page.body


def test_mercury_asc_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mercury-asc-equals-vernal-point.md"))

    assert "Conversation partners in public" in page.body
    assert "environmental reports for the public" in page.body
    assert "Gcsprachs Partncr in the public" not in page.body




