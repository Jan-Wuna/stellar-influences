from pathlib import Path

from tools.hand_source import generate_factor_models, generate_models


SOURCE_PATH = Path(
    "Stellar Influences Vault/planetary expressions - Robert Hand - Horoscope Symbols.pdf"
)


def test_hand_parser_extracts_sun_moon_axis_text():
    blocks = generate_models(SOURCE_PATH, limit_pairs=[("Sun", "Moon")])

    assert len(blocks) == 1
    block = blocks[0]
    assert (block.factor_a, block.factor_b) == ("Sun", "Moon")
    assert block.page == 201
    assert block.heading == "Sun/Moon"
    assert "The balance of male and female within the psyche" in block.text
    assert "Inner psychological balance." in block.text


def test_hand_parser_extracts_node_asc_and_aries_mc_axes():
    blocks = generate_models(
        SOURCE_PATH,
        limit_pairs=[("Node", "Asc"), ("Vernal Point", "MC")],
    )

    assert [(block.factor_a, block.factor_b) for block in blocks] == [
        ("Node", "Asc"),
        ("Vernal Point", "MC"),
    ]
    assert blocks[0].page == 213
    assert blocks[0].heading == "Nodes/Ascendant"
    assert "Connections of a personal nature" in blocks[0].text
    assert blocks[1].page == 214
    assert blocks[1].heading == "Midheaven/Aries"
    assert "One's own seeking to get ahead in the larger social world." in blocks[1].text


def test_hand_factor_parser_extracts_sun_and_node_blocks():
    blocks = generate_factor_models(SOURCE_PATH, limit_factors=["Sun", "Node"])

    assert [block.factor for block in blocks] == ["Sun", "Node"]
    assert blocks[0].page == 52
    assert blocks[0].heading == "The Sun"
    assert "It is the basic energy of Being." in blocks[0].text
    assert blocks[1].page == 105
    assert blocks[1].heading == "The Lunar Nodes"
    assert "the nodes relate to connections with other people" in blocks[1].text


def test_hand_factor_parser_extracts_shared_asc_mc_and_aries_blocks():
    blocks = generate_factor_models(SOURCE_PATH, limit_factors=["Asc", "MC", "Vernal Point"])

    assert [block.factor for block in blocks] == ["Asc", "MC", "Vernal Point"]
    assert blocks[0].page == 102
    assert blocks[0].heading == "The Ascendant and Midheaven"
    assert "exchange with the environment" in blocks[0].text
    assert blocks[1].page == 102
    assert blocks[1].heading == "The Ascendant and Midheaven"
    assert "\"I, me, mine\"" in blocks[1].text
    assert blocks[2].page == 108
    assert blocks[2].heading == "The Aries Point"
    assert "most impersonal but also the oddest social contacts" in blocks[2].text
