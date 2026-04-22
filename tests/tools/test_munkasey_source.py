from pathlib import Path

from tools.munkasey_source import SOURCE_FILE, generate_models


SOURCE_PATH = Path("Stellar Influences Vault") / SOURCE_FILE


def test_munkasey_parser_extracts_sun_moon_axis_fields():
    blocks = generate_models(SOURCE_PATH)
    sun_moon = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Sun", "Moon"))
    assert sun_moon.axis_page == 55
    assert "direction and focus of your personal awareness" in sun_moon.basic_ideas
    assert "The attention you place on whatever is important to you in life" in sun_moon.personal_thesis
    assert "Your lack of will or enthusiasm shown when caring about others" in sun_moon.personal_anti
    assert "The approval you give or receive to or with another" in sun_moon.relationship_thesis
    assert "Chemical, Ph, and mineral balances within the body" in sun_moon.body_mind


def test_munkasey_parser_extracts_ordered_concepts_without_examples():
    blocks = generate_models(SOURCE_PATH)
    sun_moon = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Sun", "Moon"))
    assert sun_moon.concepts_page == 57
    assert sun_moon.concepts[:5] == (
        "Arrogant Approval",
        "Emotional Pretension",
        "Flowery Imagination",
        "Celebrated Caring",
        "Special Sensitivities",
    )
    assert "STRONG:" not in sun_moon.concepts
    assert "EVENTS:" not in sun_moon.concepts


def test_munkasey_parser_extracts_venus_saturn_concepts_page():
    blocks = generate_models(SOURCE_PATH)
    venus_saturn = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Venus", "Saturn"))
    assert venus_saturn.concepts_page == 197
    assert venus_saturn.concepts[:4] == (
        "Prolongs Love",
        "Prefers Plainness",
        "Stable Affections",
        "A Serious Artist",
    )


def test_munkasey_parser_covers_all_78_pairs():
    blocks = generate_models(SOURCE_PATH)
    assert len(blocks) == 78
    assert blocks[0].source_heading == "SUN/MOON"
    assert blocks[-1].source_heading == "ASCENDANT/MIDHEAVEN"


def test_munkasey_parser_never_leaks_page_four_mwa_text_into_concepts():
    blocks = generate_models(SOURCE_PATH)
    all_concepts = "\n".join(item for block in blocks for item in block.concepts)
    assert "STRONG:" not in all_concepts
    assert "WEAK:" not in all_concepts
    assert "EVENTS:" not in all_concepts
    assert "Significant Examples of People and Events" not in all_concepts
