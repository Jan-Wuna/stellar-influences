from pathlib import Path

from tools.udo_rudolph_abc_source import (
    FACTOR_SEQUENCE,
    PDF_START_PAGE,
    generate_models,
)


PDF_PATH = Path("Stellar Influences Vault/Udo-Rudolph_ABC-fur-Planetenbilder.pdf")


def test_udo_abc_factor_keywords_are_extracted_from_keyword_spread():
    factors, _ = generate_models(PDF_PATH)

    assert [block.factor for block in factors] == FACTOR_SEQUENCE

    vernal_point = next(block for block in factors if block.factor == "Vernal Point")
    poseidon = next(block for block in factors if block.factor == "Poseidon")

    assert vernal_point.page == 16
    assert "Allgemeinheit" in vernal_point.text
    assert "Offentlichkeit" in vernal_point.text
    assert poseidon.page == 17
    assert "Einsicht" in poseidon.text
    assert "Kultur" in poseidon.text


def test_udo_abc_axis_spreads_follow_distinct_factor_pair_sequence():
    _, axes = generate_models(PDF_PATH)

    first = axes[0]
    last = axes[-1]

    assert len(axes) == 231
    assert first.pdf_page == PDF_START_PAGE
    assert first.factor_a == "Vernal Point"
    assert first.factor_b == "MC"
    assert first.page_range == "18-19"
    assert first.summary.startswith("Beseelte Offent")
    assert last.factor_a == "Vulcanus"
    assert last.factor_b == "Poseidon"
    assert last.page_range == "478-479"
    assert last.summary.startswith("Einflu")


def test_udo_abc_activation_entries_skip_axis_factors_and_keep_printed_pages():
    _, axes = generate_models(PDF_PATH)

    first = axes[0]
    entries = {entry.activated_by: entry for entry in first.activation_entries}

    assert len(first.activation_entries) == 20
    assert "Vernal Point" not in entries
    assert "MC" not in entries
    assert entries["Sun"].page == 18
    assert entries["Sun"].text.startswith("Beseelter Mensch")
    assert entries["Saturn"].page == 19
    assert entries["Saturn"].text.startswith("Beseelter Abend")


def test_udo_abc_generates_full_orientation_entry_count():
    _, axes = generate_models(PDF_PATH)

    assert sum(len(axis.activation_entries) for axis in axes) == 4620
