from pathlib import Path

from tools.falis_source import generate_models


SOURCE_PATH = Path(
    "Stellar Influences Vault/Book_2012_Michelle Falis_AstroFix_Planet Combinations- Astrological Brainstorms_kindle.pdf"
)


def test_falis_extracts_all_axis_sections():
    blocks = generate_models(SOURCE_PATH)

    assert len(blocks) == 45
    assert (blocks[0].factor_a, blocks[0].factor_b) == ("Sun", "Moon")
    assert "Strong parental influence." in blocks[0].text
    assert (blocks[-1].factor_a, blocks[-1].factor_b) == ("Neptune", "Pluto")
    assert "Deeply unconscious and difficult to define processes." in blocks[-1].text
