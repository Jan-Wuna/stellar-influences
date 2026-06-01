from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_axis_layer_is_cleared():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body
    assert "[Vernal Point/Saturn](../axes/vernal-point-saturn.md)" not in page.body
    assert "[Sun/Cupido](../axes/sun-cupido.md)" not in page.body
    assert "[Cupido/Poseidon](../axes/cupido-poseidon.md)" not in page.body


def test_vernal_point_saturn_axis_uses_reviewed_abc_pair_summary():
    page = load_page(Path("wiki/axes/vernal-point-saturn.md"))

    assert "Burdens for the public" in page.body
    assert "public tasks" in page.body
    assert "free movement of persons" not in page.body


def test_sun_cupido_axis_uses_reviewed_abc_pair_summary():
    page = load_page(Path("wiki/axes/sun-cupido.md"))

    assert "Center of community" in page.body
    assert "man of art" in page.body
    assert "EC Court of Justice" not in page.body


def test_cupido_poseidon_axis_uses_reviewed_abc_pair_summary():
    page = load_page(Path("wiki/axes/cupido-poseidon.md"))

    assert "Community of insight" in page.body
    assert "shared truth" in page.body
    assert "economic statistics" not in page.body




