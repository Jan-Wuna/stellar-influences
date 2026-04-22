from tools.wiki_identity import (
    astronomicon_token,
    normalize_activation,
    normalize_axis,
    normalize_factor,
    normalize_triad,
    triad_orientations,
)


def test_normalize_axis_sorts_the_pair_only():
    axis = normalize_axis("Moon", "Sun")
    assert axis.display == "Sun/Moon"
    assert axis.slug == "sun-moon"


def test_activation_orientation_is_preserved():
    left = normalize_activation("Sun", "Moon", "Venus")
    right = normalize_activation("Sun", "Venus", "Moon")
    assert left.display == "Sun/Moon = Venus"
    assert right.display == "Sun/Venus = Moon"
    assert left.display != right.display


def test_normalize_axis_preserves_mc_casing():
    axis = normalize_axis("Moon", "MC")
    assert axis.display == "Moon/MC"
    assert axis.slug == "moon-mc"


def test_normalize_axis_places_chiron_between_saturn_and_uranus():
    axis = normalize_axis("Uranus", "Chiron")
    assert axis.display == "Chiron/Uranus"
    assert axis.slug == "chiron-uranus"


def test_astronomicon_token_preserves_unknowns_and_maps_known_factors():
    assert astronomicon_token("Moon") == "R"
    assert astronomicon_token("Sun") == "S"
    assert astronomicon_token("Mercury") == "T"
    assert astronomicon_token("Venus") == "Q"
    assert astronomicon_token("Pluto") == "Z"
    assert astronomicon_token("Node") == "g"
    assert astronomicon_token("MC") == "MC"


def test_triad_orientations_lists_all_three_distinct_forms():
    orientations = triad_orientations(["Sun", "Moon", "Venus"])
    assert orientations == [
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    ]


def test_normalize_factor_canonicalizes_aliases():
    factor = normalize_factor("dragon's head")
    assert factor.display == "Node"
    assert factor.slug == "node"


def test_normalize_factor_canonicalizes_vernal_point_aliases():
    factor = normalize_factor("Aries Point")
    assert factor.display == "Vernal Point"
    assert factor.slug == "vernal-point"

    abbreviated = normalize_factor("VP")
    assert abbreviated.display == "Vernal Point"
    assert abbreviated.slug == "vernal-point"


def test_normalize_triad_sorts_and_derives_orientations():
    triad = normalize_triad(["Venus", "Sun", "Moon"])
    assert triad.display == "Sun Moon Venus"
    assert triad.slug == "sun-moon-venus"
    assert triad.orientations == (
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    )
