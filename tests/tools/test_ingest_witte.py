from tools.ingest_witte import (
    _activation_page_text,
    _canonical_factor_blocks,
    _coalesce_pair_blocks,
    _factor_page_text,
    _group_triads,
)
from tools.witte_source import ActivationEntry, FactorBlock, PairBlock


def test_coalesce_pair_blocks_prefers_cleaner_duplicate_entries():
    noisy = PairBlock(
        factor_a="Hades",
        factor_b="Admetos",
        source_heading="Hades + Admetos",
        page=282,
        summary="Scantness. Frugality. Lack &",
        activation_entries=[
            ActivationEntry("Aries", "A", "General pessimism. &", 282),
            ActivationEntry("Poseidon", "X", "past times.", 282),
        ],
    )
    clean = PairBlock(
        factor_a="Hades",
        factor_b="Admetos",
        source_heading="Hades + Admetos",
        page=284,
        summary="Scantness. Frugality. Great and deep sadness.",
        activation_entries=[
            ActivationEntry("Aries", "A", "General pessimism.", 284),
            ActivationEntry(
                "Poseidon",
                "X",
                "Ignorance and mental indifference. To occupy one's mind with remote antiquity.",
                284,
            ),
        ],
    )

    merged = _coalesce_pair_blocks([noisy, clean])

    assert len(merged) == 1
    entry_map = {entry.activated_by: entry for entry in merged[0].activation_entries}
    assert merged[0].summary == clean.summary
    assert entry_map["Aries"].text == clean.activation_entries[0].text
    assert entry_map["Poseidon"].text == clean.activation_entries[1].text


def test_group_triads_skips_repeated_pair_activations():
    repeated_pair = PairBlock(
        factor_a="Aries",
        factor_b="Aries",
        source_heading="Aries + Aries",
        page=33,
        summary="The world public.",
        activation_entries=[ActivationEntry("MC", "M", "Public prominence.", 33)],
    )
    distinct_pair = PairBlock(
        factor_a="Aries",
        factor_b="MC",
        source_heading="Aries + Meridian",
        page=35,
        summary="Public life.",
        activation_entries=[ActivationEntry("Sun", "S", "Public leadership.", 35)],
    )

    triads = _group_triads([repeated_pair, distinct_pair])

    assert list(triads) == [("Aries", "Sun", "MC")]
    assert len(triads[("Aries", "Sun", "MC")]) == 1


def test_witte_factor_pages_remain_structural_only():
    factor = FactorBlock(
        factor="Aries",
        page=27,
        text="Sensitive point of the world and the general public.",
    )
    pair = PairBlock(
        factor_a="Aries",
        factor_b="MC",
        source_heading="Aries + Meridian",
        page=35,
        summary="Public life.",
        activation_entries=[ActivationEntry("Sun", "S", "Public leadership.", 35)],
    )

    page = _factor_page_text(factor, [pair], activation_count=1, updated_at="2026-04-21")

    assert "#### Witte Factor Entry" in page
    assert "Sensitive point of the world and the general public." in page
    assert "No standalone factor chapter material from this source is ingested on this page." not in page


def test_repeated_pair_activation_page_does_not_link_a_fake_triad_hub():
    pair = PairBlock(
        factor_a="Aries",
        factor_b="Aries",
        source_heading="Aries + Aries",
        page=33,
        summary="The world public.",
        activation_entries=[ActivationEntry("MC", "M", "Public prominence.", 33)],
    )

    page = _activation_page_text(pair, pair.activation_entries[0], updated_at="2026-04-21")

    assert "Triad hub:" not in page
    assert "Repeated-pair identity: no distinct triad hub exists for this activation." in page


def test_activation_page_omits_low_value_source_markers():
    pair = PairBlock(
        factor_a="Sun",
        factor_b="Admetos",
        source_heading="Sun + Admetos",
        page=200,
        summary="Lasting body.",
        activation_entries=[ActivationEntry("Neptune", "iff", "Psychic solidity.", 200)],
    )

    page = _activation_page_text(pair, pair.activation_entries[0], updated_at="2026-04-21")

    assert "Source marker:" not in page


def test_canonical_factor_blocks_keep_best_source_text_and_restore_missing_factors():
    parsed = [
        FactorBlock("Aries", 26, "preface"),
        FactorBlock("Aries", 27, "doctrine"),
        FactorBlock("MC", 29, "meridian"),
        FactorBlock("Pluto", 28, "pluto"),
    ]

    factors = _canonical_factor_blocks(parsed)
    lookup = {factor.factor: factor for factor in factors}

    assert len(factors) == 22
    assert lookup["Aries"].page == 27
    assert lookup["Aries"].text == "doctrine"
    assert lookup["MC"].page == 29
    assert lookup["Pluto"].page == 28
    assert lookup["Pluto"].text == "pluto"
