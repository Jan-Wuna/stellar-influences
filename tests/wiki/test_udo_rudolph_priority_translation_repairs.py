from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_priority_repairs():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_repaired_priority_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon](../factors/moon.md)" not in page.body
    assert "[Neptune](../factors/neptune.md)" not in page.body
    assert "[Sun/MC](../axes/sun-mc.md)" not in page.body
    assert "[Sun/Neptune](../axes/sun-neptune.md)" not in page.body
    assert "[Moon/Node](../axes/moon-node.md)" not in page.body
    assert "[Sun/Moon = MC](../activations/sun-moon-equals-mc.md)" not in page.body
    assert "[Sun/MC = Neptune](../activations/sun-mc-equals-neptune.md)" not in page.body
    assert "[Sun/Node = MC](../activations/sun-node-equals-mc.md)" not in page.body
    assert "[Moon/Node = Asc](../activations/moon-node-equals-asc.md)" not in page.body
    assert "[Node/Asc = Moon](../activations/node-asc-equals-moon.md)" not in page.body
    assert "[Sun/Neptune = MC](../activations/sun-neptune-equals-mc.md)" not in page.body


def test_neptune_factor_uses_reviewed_abc_keyword_translation():
    page = load_page(Path("wiki/factors/neptune.md"))

    assert "#### ABC Keyword Entry" in page.body
    assert "unknown, lack of clarity, uncertainty" in page.body
    assert "Unklarheit, Unsicherheit" not in page.body


def test_sun_mc_axis_uses_reviewed_abc_pair_summary():
    page = load_page(Path("wiki/axes/sun-mc.md"))

    assert "#### ABC Pair Summary" in page.body
    assert "self in the day" in page.body
    assert "center of the soul" in page.body
    assert "ich at the Tage" not in page.body
    assert "Zcntrum" not in page.body


def test_sun_moon_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/sun-moon-equals-mc.md"))

    assert "#### ABC Entry" in page.body
    assert "personal feelings" in page.body
    assert "day hour minute" in page.body
    assert "EC Treaty" not in page.body




