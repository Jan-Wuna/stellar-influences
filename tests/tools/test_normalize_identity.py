from tools.wiki_identity import (
    normalize_activation,
    normalize_axis,
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


def test_triad_orientations_lists_all_three_distinct_forms():
    orientations = triad_orientations(["Sun", "Moon", "Venus"])
    assert orientations == [
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    ]
