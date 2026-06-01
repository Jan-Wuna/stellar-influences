from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_seventeenth_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_seventeenth_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Moon/Apollon = Admetos](../activations/moon-apollon-equals-admetos.md)" not in page.body
    assert "[Moon/Apollon = Vulcanus](../activations/moon-apollon-equals-vulcanus.md)" not in page.body
    assert "[Moon/Admetos = MC](../activations/moon-admetos-equals-mc.md)" not in page.body
    assert "[Moon/Admetos = Asc](../activations/moon-admetos-equals-asc.md)" not in page.body
    assert "[Moon/Vulcanus = MC](../activations/moon-vulcanus-equals-mc.md)" not in page.body
    assert "[Moon/Vulcanus = Venus](../activations/moon-vulcanus-equals-venus.md)" not in page.body
    assert "[Moon/Vulcanus = Jupiter](../activations/moon-vulcanus-equals-jupiter.md)" not in page.body
    assert "[Moon/Vulcanus = Saturn](../activations/moon-vulcanus-equals-saturn.md)" not in page.body
    assert "[Moon/Vulcanus = Neptune](../activations/moon-vulcanus-equals-neptune.md)" not in page.body
    assert "[Moon/Vulcanus = Apollon](../activations/moon-vulcanus-equals-apollon.md)" not in page.body
    assert "[Moon/Vulcanus = Admetos](../activations/moon-vulcanus-equals-admetos.md)" not in page.body
    assert "[Moon/Poseidon = Neptune](../activations/moon-poseidon-equals-neptune.md)" not in page.body


def test_moon_apollon_equals_admetos_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-apollon-equals-admetos.md"))

    assert "blocked economy of a people" in page.body
    assert "condensation of emotional knowledge" in page.body
    assert "Handels Blockade for ein people" not in page.body


def test_moon_vulcanus_equals_saturn_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-vulcanus-equals-saturn.md"))

    assert "tremendous tasks for a people" in page.body
    assert "hour of separation from the woman" in page.body
    assert "Gewaltige tasks for ein people" not in page.body


def test_moon_vulcanus_equals_apollon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-vulcanus-equals-apollon.md"))

    assert "expansion of emotional power" in page.body
    assert "power through emotional knowledge" in page.body
    assert "Ausdehnung the GemOts Kraft" not in page.body


def test_moon_poseidon_equals_neptune_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/moon-poseidon-equals-neptune.md"))

    assert "disappointment through a spiritual woman" in page.body
    assert "deceptive emotional influence" in page.body
    assert "Enttauschung through eine geistvolle women" not in page.body


def test_batch_seventeen_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/moon-apollon-equals-admetos.md"))
    comparative_page = load_page(Path("wiki/factors/admetos.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1




