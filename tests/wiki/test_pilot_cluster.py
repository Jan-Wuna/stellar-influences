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


def test_axis_pages_cover_all_activation_axes():
    activation_paths = [
        Path("wiki/activations/sun-moon-equals-venus.md"),
        Path("wiki/activations/sun-venus-equals-moon.md"),
        Path("wiki/activations/moon-venus-equals-sun.md"),
    ]
    for activation_path in activation_paths:
        activation = load_page(activation_path)
        axis_slug = activation.meta["axis"].lower().replace("/", "-")
        axis_path = Path("wiki/axes") / f"{axis_slug}.md"
        assert axis_path.exists(), f"missing axis page for {activation_path.name}"
