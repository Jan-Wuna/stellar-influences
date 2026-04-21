from tools.ebertin_source import (
    PageRecord,
    canonicalize_source_factor,
    parse_axis_blocks,
    parse_factor_blocks,
    parse_activation_entries,
    parse_sign_entries,
)


def test_canonicalize_source_factor_handles_special_names():
    assert canonicalize_source_factor("Dragon's Head") == "Node"
    assert canonicalize_source_factor("Ascendant") == "Asc"
    assert canonicalize_source_factor("Medium Coeli") == "MC"


def test_parse_activation_entries_assigns_remaining_factors_in_order():
    sample = """
0183 = 5
One's attitude and thoughts in relation to the male and female principles.
0184 = 9
Harmonious coordination between spiritual and emotional dispositions.
0185 = cr
The urge to bring ideals to fruition.
""".strip()

    entries = parse_activation_entries("Sun", "Moon", sample, {})

    assert [entry.activated_by for entry in entries] == ["Mercury", "Venus", "Mars"]
    assert entries[1].code == "0184"
    assert "Harmonious coordination" in entries[1].text


def test_parse_sign_entries_assigns_zodiac_order():
    sample = """
T 0014 I
Storming and urging nature, leading character.
G 0015 II
Rich soul life, perseverance, endurance.
X0016 III
Vivacious, joy of life, versatile.
""".strip()

    entries = parse_sign_entries(sample, {})

    assert [entry.sign for entry in entries] == ["Aries", "Taurus", "Gemini"]
    assert entries[0].code == "0014"
    assert "Storming and urging nature" in entries[0].text


def test_parse_factor_blocks_preserves_multiple_sign_entries():
    sample = """
The Moon
Principle
Soul, the female principle.
Psychological Correspondence
Motherly, domestic.
Biological Correspondence
Fertility.
Sociological Correspondence
Mother, wife, family.
Position in Houses and Signs
T 0027 I
Storming and urging nature, leading character.
G 0028 II
Rich soul life, perseverance, endurance.
X 0029 III
Vivacious, joy of life, versatile.
48
""".strip()

    blocks = parse_factor_blocks([PageRecord(printed_page=48, text=sample)])

    assert len(blocks) == 1
    assert [entry.sign for entry in blocks[0].sign_entries] == ["Aries", "Taurus", "Gemini"]
    assert blocks[0].sign_entries[1].code == "0028"
    assert "Rich soul life" in blocks[0].sign_entries[1].text


def test_parse_sign_entries_rejoins_line_break_hyphenation():
    sample = """
T 0027 I
Storming and urging nature, impulsive-
ness and over-eagerness.
G 0028 II
Rich soul life.
""".strip()

    entries = parse_sign_entries(sample, {})

    assert "impulsiveness" in entries[0].text
    assert "impulsive- ness" not in entries[0].text


def test_parse_axis_blocks_skips_coded_axis_summary_before_activations():
    sample = """
Ascendant/Medium Coeli
1106 A/M
Principle
Relationship between the ego and the lower self.
Psychological Correspondence
The living being, the individual synthesis.
Biological Correspondence
The phenotype.
Sociological Correspondence
The personality as directed by ego-consciousness.
Probable Manifestations
Important periods of life.
1107 = O
The relationship between body and soul.
1108 = D
One's personal attitude to life as governed by feeling.
306
""".strip()

    blocks = parse_axis_blocks([PageRecord(printed_page=306, text=sample)])

    assert len(blocks) == 1
    assert blocks[0].sections["Principle"] == "Relationship between the ego and the lower self."
    assert [entry.code for entry in blocks[0].activation_entries] == ["1107", "1108"]
    assert [entry.activated_by for entry in blocks[0].activation_entries] == ["Sun", "Moon"]
