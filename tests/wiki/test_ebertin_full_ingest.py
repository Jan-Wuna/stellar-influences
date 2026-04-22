from pathlib import Path

from tools.wiki_pages import load_page


EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
EBERTIN_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"


def test_full_ingest_includes_standalone_factor_pages():
    mercury = Path("wiki/factors/mercury.md")
    assert mercury.exists()
    assert "Position in Houses and Signs" in mercury.read_text(encoding="utf-8")


def test_full_ingest_creates_nonpilot_activation_pages():
    page = load_page(Path("wiki/activations/sun-mercury-equals-venus.md"))
    assert page.meta["normalized_formula"] == "Sun/Mercury = Venus"


def test_live_wiki_keeps_axis_summary_and_activation_entries_separate():
    axis = load_page(Path("wiki/axes/sun-mercury.md"))
    activation = load_page(Path("wiki/activations/sun-mercury-equals-moon.md"))

    assert "A body in motion." in axis.body
    assert "The young mate (marriage partner)." in activation.body
    assert "A body in motion." not in activation.body


def test_live_axis_page_includes_ebertin_entry():
    axis = load_page(Path("wiki/axes/sun-mercury.md"))

    assert EBERTIN_SLUG in axis.meta["source_pages"]
    assert f"### {EBERTIN_TITLE}" in axis.body
    assert "Mind and common sense, a thinking being, the power of thought, understanding and knowledge." in axis.body


def test_live_activation_page_includes_ebertin_entry():
    activation = load_page(Path("wiki/activations/sun-mercury-equals-venus.md"))

    assert EBERTIN_SLUG in activation.meta["source_pages"]
    assert f"### {EBERTIN_TITLE}" in activation.body
    assert "One's outlook and attitude in relation to love and sex, thoughts on sex. Love union, youth love." in activation.body


def test_live_triad_page_includes_ebertin_source_coverage():
    triad = load_page(Path("wiki/triads/sun-mercury-venus.md"))

    assert EBERTIN_SLUG in triad.meta["source_pages"]
    assert f"`Sun/Mercury = Venus`: {EBERTIN_TITLE}, page `81`" in triad.body


def test_ebertin_source_page_reports_live_axis_activation_and_triad_coverage():
    source_page = load_page(Path("wiki/sources/reinhold-ebertin-the-combination-of-stellar-influences.md"))

    assert "Canonical axis pages updated or created: `76`." in source_page.body
    assert "Canonical activation pages updated or created: `836`." in source_page.body
    assert "Canonical triad hubs updated or created: `286`." in source_page.body


def test_ebertin_source_page_links_unresolved_review_artifact():
    source_page = load_page(Path("wiki/sources/reinhold-ebertin-the-combination-of-stellar-influences.md"))

    assert "[Ebertin unresolved activation review](../derived/ebertin-unresolved-activation-review.md)" in source_page.body


def test_ebertin_unresolved_review_page_exists():
    review = load_page(Path("wiki/derived/ebertin-unresolved-activation-review.md"))

    assert review.meta["page_type"] == "derived"
    assert "No unresolved Ebertin activation entries are currently blocked." in review.body


def test_full_ingest_expands_page_counts():
    assert len(list(Path("wiki/axes").glob("*.md"))) >= 70
    assert len(list(Path("wiki/activations").glob("*.md"))) >= 800
    assert len(list(Path("wiki/triads").glob("*.md"))) >= 250
