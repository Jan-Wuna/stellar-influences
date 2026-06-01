from pathlib import Path

from tools.wiki_links import (
    DERIVED_SYNTHESIS_ANCHOR,
    derived_synthesis_heading,
    relative_link_target,
)


def test_relative_link_target_uses_current_file_parent():
    current = Path("wiki/factors/sun.md")
    target = Path("wiki/axes/sun-moon.md")

    assert relative_link_target(current, target) == "../axes/sun-moon.md"


def test_relative_link_target_supports_root_pages_and_anchors():
    current = Path("wiki/index.md")
    target = Path("wiki/activations/sun-moon-equals-venus.md")

    assert (
        relative_link_target(current, target, anchor=DERIVED_SYNTHESIS_ANCHOR)
        == "activations/sun-moon-equals-venus.md#derived-synthesis"
    )


def test_derived_synthesis_heading_emits_explicit_anchor():
    assert derived_synthesis_heading() == '<a id="derived-synthesis"></a>\n\n## Derived Synthesis'
