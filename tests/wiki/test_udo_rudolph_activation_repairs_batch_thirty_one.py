from pathlib import Path

from tools.wiki_pages import load_page


QA_SLUG = "udo-rudolph-abc-translation-qa"


def test_rudolph_translation_qa_counts_drop_after_thirty_first_activation_batch():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "- Flagged factor keyword entries: `0`." in page.body
    assert "- Flagged axis pair summaries: `0`." in page.body
    assert "- Flagged activation entries: `0`." in page.body
    assert "- Total flagged source entries: `0`." in page.body


def test_rudolph_translation_qa_page_drops_thirty_first_activation_batch_entries():
    page = load_page(Path("wiki/derived") / f"{QA_SLUG}.md")

    assert "[Cupido/Admetos = Jupiter](../activations/cupido-admetos-equals-jupiter.md)" not in page.body
    assert "[Cupido/Admetos = Vulcanus](../activations/cupido-admetos-equals-vulcanus.md)" not in page.body
    assert "[Cupido/Vulcanus = MC](../activations/cupido-vulcanus-equals-mc.md)" not in page.body
    assert "[Cupido/Vulcanus = Moon](../activations/cupido-vulcanus-equals-moon.md)" not in page.body
    assert "[Cupido/Poseidon = Vernal Point](../activations/cupido-poseidon-equals-vernal-point.md)" not in page.body
    assert "[Cupido/Poseidon = Sun](../activations/cupido-poseidon-equals-sun.md)" not in page.body
    assert "[Cupido/Poseidon = Neptune](../activations/cupido-poseidon-equals-neptune.md)" not in page.body
    assert "[Hades/Zeus = Pluto](../activations/hades-zeus-equals-pluto.md)" not in page.body
    assert "[Hades/Zeus = Vulcanus](../activations/hades-zeus-equals-vulcanus.md)" not in page.body
    assert "[Hades/Kronos = Vernal Point](../activations/hades-kronos-equals-vernal-point.md)" not in page.body
    assert "[Hades/Admetos = Moon](../activations/hades-admetos-equals-moon.md)" not in page.body
    assert "[Hades/Vulcanus = Vernal Point](../activations/hades-vulcanus-equals-vernal-point.md)" not in page.body


def test_cupido_admetos_equals_jupiter_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-admetos-equals-jupiter.md"))

    assert "blocked financial community" in page.body
    assert "shared success through endurance" in page.body
    assert "Blockierte Finanz community" not in page.body


def test_cupido_vulcanus_equals_mc_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/cupido-vulcanus-equals-mc.md"))

    assert "shared psychic influence" in page.body
    assert "soulful strength of a community" in page.body
    assert "Gemcinsamcr seclischer Eintlu/3" not in page.body


def test_hades_admetos_equals_moon_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/hades-admetos-equals-moon.md"))

    assert "lack of endurance of a woman" in page.body
    assert "deepening into the past of a people" in page.body
    assert "Ausdauer Mangel a women" not in page.body


def test_hades_vulcanus_equals_vernal_point_uses_reviewed_abc_activation_translation():
    page = load_page(Path("wiki/activations/hades-vulcanus-equals-vernal-point.md"))

    assert "influence of the past in public life" in page.body
    assert "hidden power in public life" in page.body
    assert "Einfluss the Vcrgangenhcit irn Mfentlichcn Lchcn" not in page.body


def test_batch_thirty_one_pages_keep_a_single_derived_synthesis_anchor():
    activation_page = load_page(Path("wiki/activations/hades-vulcanus-equals-vernal-point.md"))
    comparative_page = load_page(Path("wiki/factors/hades.md"))

    assert activation_page.body.count('<a id="derived-synthesis"></a>') == 1
    assert comparative_page.body.count('<a id="derived-synthesis"></a>') == 1

