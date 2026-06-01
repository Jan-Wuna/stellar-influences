from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_second_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_second_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Vernal Point/Mars = Hades](../activations/vernal-point-mars-equals-hades.md)" not in page.body
    assert "[Vernal Point/Jupiter = Uranus](../activations/vernal-point-jupiter-equals-uranus.md)" not in page.body
    assert "[Vernal Point/Jupiter = Cupido](../activations/vernal-point-jupiter-equals-cupido.md)" not in page.body
    assert "[Vernal Point/Saturn = Uranus](../activations/vernal-point-saturn-equals-uranus.md)" not in page.body
    assert "[Vernal Point/Saturn = Neptune](../activations/vernal-point-saturn-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Saturn = Pluto](../activations/vernal-point-saturn-equals-pluto.md)" not in page.body
    assert "[Vernal Point/Saturn = Cupido](../activations/vernal-point-saturn-equals-cupido.md)" not in page.body
    assert "[Vernal Point/Uranus = Moon](../activations/vernal-point-uranus-equals-moon.md)" not in page.body
    assert "[Vernal Point/Uranus = Jupiter](../activations/vernal-point-uranus-equals-jupiter.md)" not in page.body
    assert "[Vernal Point/Uranus = Saturn](../activations/vernal-point-uranus-equals-saturn.md)" not in page.body
    assert "[Vernal Point/Uranus = Neptune](../activations/vernal-point-uranus-equals-neptune.md)" not in page.body
    assert "[Vernal Point/Uranus = Cupido](../activations/vernal-point-uranus-equals-cupido.md)" not in page.body


def test_vernal_point_jupiter_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-jupiter-equals-cupido.md"))

    assert "Successful community in public" in page.body
    assert "shared joy in public" in page.body
    assert "Community financing" not in page.body


def test_vernal_point_saturn_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-saturn-equals-uranus.md"))

    assert "Serious tensions in public" in page.body
    assert "sudden separation from public life" in page.body
    assert "Court of Justice" not in page.body


def test_vernal_point_uranus_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-uranus-equals-moon.md"))

    assert "emotional excitement in public" in page.body
    assert "public reforms for a people" in page.body
    assert "Geftiehl" not in page.body


def test_vernal_point_uranus_equals_cupido_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/vernal-point-uranus-equals-cupido.md"))

    assert "Excited communities in public" in page.body
    assert "shared renewals of public life" in page.body
    assert "research and development" not in page.body




