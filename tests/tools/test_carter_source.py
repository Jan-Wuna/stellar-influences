from pathlib import Path

from tools.carter_source import generate_models


SOURCE_PATH = Path(
    "Stellar Influences Vault/Book_2000_Charles Carter_The Astrological Aspects.pdf"
)


def test_carter_parser_extracts_sun_moon_sections():
    blocks = generate_models(SOURCE_PATH, limit_pairs=[("Sun", "Moon")])

    assert len(blocks) == 1
    block = blocks[0]
    assert (block.factor_a, block.factor_b) == ("Sun", "Moon")
    assert block.page == 5
    assert block.heading == "ASPECTS OF THE SUN AND MOON"
    assert "good health supported by a strong constitution" in block.intro_text
    assert "These are conducive to happiness and tranquility." in block.harmonious_text
    assert "It is thought by many that even bad aspects are to be preferred" in block.intro_text
    assert "It makes for unpopularity" in block.inharmonious_text


def test_carter_parser_extracts_family_grouped_examples():
    blocks = generate_models(SOURCE_PATH, limit_pairs=[("Moon", "Mercury")])

    assert len(blocks) == 1
    block = blocks[0]
    assert "Kant" in block.harmonious_examples
    assert "Baden-Powell" in block.conjunction_examples
    assert "Shelley" in block.inharmonious_examples
