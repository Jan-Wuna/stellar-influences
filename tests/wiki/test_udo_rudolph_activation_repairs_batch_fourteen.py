from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_fourteenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_fourteenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Mars = Sun](../activations/moon-mars-equals-sun.md)" not in page.body
    assert "[Moon/Mars = Mercury](../activations/moon-mars-equals-mercury.md)" not in page.body
    assert "[Moon/Mars = Uranus](../activations/moon-mars-equals-uranus.md)" not in page.body
    assert "[Moon/Mars = Pluto](../activations/moon-mars-equals-pluto.md)" not in page.body
    assert "[Moon/Mars = Vulcanus](../activations/moon-mars-equals-vulcanus.md)" not in page.body
    assert "[Moon/Jupiter = Pluto](../activations/moon-jupiter-equals-pluto.md)" not in page.body
    assert "[Moon/Saturn = Asc](../activations/moon-saturn-equals-asc.md)" not in page.body
    assert "[Moon/Uranus = Vernal Point](../activations/moon-uranus-equals-vernal-point.md)" not in page.body
    assert "[Moon/Uranus = Asc](../activations/moon-uranus-equals-asc.md)" not in page.body
    assert "[Moon/Uranus = Saturn](../activations/moon-uranus-equals-saturn.md)" not in page.body
    assert "[Moon/Uranus = Kronos](../activations/moon-uranus-equals-kronos.md)" not in page.body
    assert "[Moon/Uranus = Vulcanus](../activations/moon-uranus-equals-vulcanus.md)" not in page.body


def test_moon_mars_equals_sun_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mars-equals-sun.md"))

    assert "efforts of the man for the woman" in page.body
    assert "creative people of a people" in page.body
    assert "Bemtihungen the man um of women" not in page.body


def test_moon_mars_equals_uranus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-mars-equals-uranus.md"))

    assert "work reform for women" in page.body
    assert "sudden actions of a people" in page.body
    assert "work Refonn for women" not in page.body


def test_moon_saturn_equals_asc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-saturn-equals-asc.md"))

    assert "tasks of the woman at the place" in page.body
    assert "loss of the woman as partner" in page.body
    assert "Aufgabcn of women at the place" not in page.body


def test_moon_uranus_equals_vulcanus_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-uranus-equals-vulcanus.md"))

    assert "dynamic power of a woman" in page.body
    assert "strong emotional impulses" in page.body
    assert "Dynamische power a women" not in page.body


def test_batch_fourteen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/moon-mars-equals-sun.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




