from pathlib import Path

from tools.wiki_pages import load_page


def test_required_templates_exist():
    assert Path("wiki/_templates/factor.md").exists()
    assert Path("wiki/_templates/activation.md").exists()
    assert Path("AGENTS.md").exists()


def test_three_activation_pages_are_distinct():
    left = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))
    middle = load_page(Path("wiki/activations/sun-venus-equals-moon.md"))
    right = load_page(Path("wiki/activations/moon-venus-equals-sun.md"))
    assert left.meta["normalized_formula"] != middle.meta["normalized_formula"]
    assert middle.meta["normalized_formula"] != right.meta["normalized_formula"]


def test_triad_hub_links_all_orientations():
    triad = load_page(Path("wiki/triads/sun-moon-venus.md"))
    assert triad.meta["orientations"] == [
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    ]
