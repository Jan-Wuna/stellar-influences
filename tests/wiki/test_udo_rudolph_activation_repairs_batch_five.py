from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_fifth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_fifth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/MC = Pluto](../activations/moon-mc-equals-pluto.md)" not in page.body
    assert "[Moon/MC = Vulcanus](../activations/moon-mc-equals-vulcanus.md)" not in page.body
    assert "[Moon/MC = Poseidon](../activations/moon-mc-equals-poseidon.md)" not in page.body
    assert "[Node/MC = Neptune](../activations/node-mc-equals-neptune.md)" not in page.body
    assert "[Mars/MC = Moon](../activations/mars-mc-equals-moon.md)" not in page.body
    assert "[Saturn/MC = Vernal Point](../activations/saturn-mc-equals-vernal-point.md)" not in page.body
    assert "[Saturn/MC = Neptune](../activations/saturn-mc-equals-neptune.md)" not in page.body
    assert "[Neptune/MC = Vernal Point](../activations/neptune-mc-equals-vernal-point.md)" not in page.body
    assert "[Neptune/MC = Saturn](../activations/neptune-mc-equals-saturn.md)" not in page.body
    assert "[Neptune/MC = Kronos](../activations/neptune-mc-equals-kronos.md)" not in page.body
    assert "[Pluto/MC = Neptune](../activations/pluto-mc-equals-neptune.md)" not in page.body
    assert "[MC/Cupido = Vernal Point](../activations/mc-cupido-equals-vernal-point.md)" not in page.body


def test_moon_mc_equals_pluto_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mc-equals-pluto.md"))

    assert "emotional psychic development" in page.body
    assert "change of the female psyche" in page.body
    assert "mcinc development als women" not in page.body


def test_node_mc_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/node-mc-equals-neptune.md"))

    assert "Dissolution of psychic contacts" in page.body
    assert "my encounter with metaphysics" in page.body
    assert "my enttauschenden connection" not in page.body


def test_saturn_mc_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/saturn-mc-equals-neptune.md"))

    assert "Old soul in subtle substance" in page.body
    assert "my developmental tasks" in page.body
    assert "Alte soul in the Feinstoff" not in page.body


def test_mc_cupido_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/mc-cupido-equals-vernal-point.md"))

    assert "Inspired community in public" in page.body
    assert "shared actions in public life" in page.body
    assert "EC internal market" not in page.body




