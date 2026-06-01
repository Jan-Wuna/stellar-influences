import json
import subprocess
import sys
from pathlib import Path

from tools.query_manifest import build_query_guide, build_query_manifest


def test_build_query_manifest_classifies_retrieval_roles(tmp_path: Path):
    wiki = tmp_path / "wiki"

    activation = wiki / "activations" / "sun-moon-equals-venus.md"
    activation.parent.mkdir(parents=True)
    activation.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "normalized_formula: Sun/Moon = Venus\n"
        "source_pages:\n"
        "  - source-a\n"
        "  - source-b\n"
        "---\n"
        "\n"
        "## Derived Synthesis\n"
        "\n"
        "- None yet beyond source structuring.\n",
        encoding="utf-8",
    )

    triad = wiki / "triads" / "sun-moon-venus.md"
    triad.parent.mkdir(parents=True)
    triad.write_text(
        "---\n"
        "title: Sun Moon Venus\n"
        "page_type: triad_hub\n"
        "slug: sun-moon-venus\n"
        "framework_scope: comparative\n"
        "factors:\n"
        "  - Sun\n"
        "  - Moon\n"
        "  - Venus\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "## Identity\n"
        "\n"
        "- This page is structural only. It does not merge the meanings of its orientations.\n",
        encoding="utf-8",
    )

    concepts = wiki / "derived" / "munkasey-sun-moon-concepts.md"
    concepts.parent.mkdir(parents=True)
    concepts.write_text(
        "---\n"
        "title: Michael Munkasey - Sun/Moon Concepts\n"
        "page_type: derived\n"
        "slug: munkasey-sun-moon-concepts\n"
        "framework_scope: modern_astrology\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "## Source Concepts\n"
        "\n"
        "- Arrogant Approval\n",
        encoding="utf-8",
    )

    note = wiki / "derived" / "orientation-matters-sun-moon-venus.md"
    note.write_text(
        "---\n"
        'title: "Orientation Matters: Sun Moon Venus"\n'
        "page_type: derived\n"
        "slug: orientation-matters-sun-moon-venus\n"
        "framework_scope: hamburg_school\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "## Analysis\n"
        "\n"
        "- Orientation changes the doctrinal claim.\n",
        encoding="utf-8",
    )

    manifest = build_query_manifest(wiki)
    by_slug = {page["slug"]: page for page in manifest["pages"]}

    assert by_slug["sun-moon-equals-venus"]["retrieval_role"] == "canonical_answer"
    assert by_slug["sun-moon-equals-venus"]["answer_surface"] is True
    assert by_slug["sun-moon-equals-venus"]["source_count"] == 2
    assert by_slug["sun-moon-equals-venus"]["has_real_derived_synthesis"] is False

    assert by_slug["sun-moon-venus"]["retrieval_role"] == "structural_only"
    assert by_slug["sun-moon-venus"]["structural_only"] is True
    assert by_slug["sun-moon-venus"]["answer_surface"] is False

    assert by_slug["munkasey-sun-moon-concepts"]["retrieval_role"] == "source_companion"
    assert by_slug["munkasey-sun-moon-concepts"]["answer_surface"] is False

    assert by_slug["orientation-matters-sun-moon-venus"]["retrieval_role"] == "synthesis_note"
    assert by_slug["orientation-matters-sun-moon-venus"]["answer_surface"] is True


def test_build_query_guide_emphasizes_synthesis_first_usage(tmp_path: Path):
    wiki = tmp_path / "wiki"
    activation = wiki / "activations" / "sun-moon-equals-venus.md"
    activation.parent.mkdir(parents=True)
    activation.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "framework_scope: comparative\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n",
        encoding="utf-8",
    )
    note = wiki / "derived" / "orientation-matters-sun-moon-venus.md"
    note.parent.mkdir(parents=True)
    note.write_text(
        "---\n"
        'title: "Orientation Matters: Sun Moon Venus"\n'
        "page_type: derived\n"
        "slug: orientation-matters-sun-moon-venus\n"
        "framework_scope: hamburg_school\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "## Analysis\n"
        "\n"
        "- Orientation changes the doctrinal claim.\n",
        encoding="utf-8",
    )
    triad = wiki / "triads" / "sun-moon-venus.md"
    triad.parent.mkdir(parents=True)
    triad.write_text(
        "---\n"
        "title: Sun Moon Venus\n"
        "page_type: triad_hub\n"
        "slug: sun-moon-venus\n"
        "framework_scope: comparative\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "## Identity\n"
        "\n"
        "- This page is structural only. It does not merge the meanings of its orientations.\n",
        encoding="utf-8",
    )

    manifest = build_query_manifest(wiki)
    guide = build_query_guide(manifest)

    assert "Use activation pages first for explicit formulas." in guide
    assert "Use triad hubs only to confirm orientation siblings." in guide
    assert "## Canonical Answer Pages" in guide
    assert "## Structural Hubs" in guide


def test_build_query_manifest_treats_empty_crlf_derived_sections_as_empty(tmp_path: Path):
    wiki = tmp_path / "wiki"
    factor = wiki / "factors" / "admetos.md"
    factor.parent.mkdir(parents=True)
    factor.write_text(
        "---\r\n"
        "title: Admetos\r\n"
        "page_type: factor\r\n"
        "slug: admetos\r\n"
        "framework_scope: hamburg_school\r\n"
        "source_pages:\r\n"
        "  - source-a\r\n"
        "---\r\n"
        "\r\n"
        "<a id=\"derived-synthesis\"></a>\r\n"
        "\r\n"
        "## Derived Synthesis\r\n"
        "\r\n"
        "\r\n"
        "## Related Axes\r\n"
        "\r\n"
        "- [Admetos/Admetos](../axes/admetos-admetos.md)\r\n",
        encoding="utf-8",
    )

    manifest = build_query_manifest(wiki)
    record = manifest["pages"][0]

    assert record["title"] == "Admetos"
    assert record["has_real_derived_synthesis"] is False
    assert record["answer_priority"] == 101


def test_build_query_manifest_recognizes_real_anchored_derived_synthesis(tmp_path: Path):
    wiki = tmp_path / "wiki"
    factor = wiki / "factors" / "sun.md"
    factor.parent.mkdir(parents=True)
    factor.write_text(
        "---\n"
        "title: Sun\n"
        "page_type: factor\n"
        "slug: sun\n"
        "framework_scope: comparative\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n"
        "\n"
        "<a id=\"derived-synthesis\"></a>\n"
        "\n"
        "## Derived Synthesis\n"
        "\n"
        "- Vitality and coherent purpose.\n",
        encoding="utf-8",
    )

    manifest = build_query_manifest(wiki)
    record = manifest["pages"][0]

    assert record["title"] == "Sun"
    assert record["has_real_derived_synthesis"] is True
    assert record["answer_priority"] == 111


def test_query_manifest_script_writes_manifest_and_guide(tmp_path: Path):
    wiki = tmp_path / "wiki"
    activation = wiki / "activations" / "sun-moon-equals-venus.md"
    activation.parent.mkdir(parents=True)
    activation.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "framework_scope: comparative\n"
        "source_pages:\n"
        "  - source-a\n"
        "---\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "tools/query_manifest.py", str(wiki)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    manifest_path = wiki / "query-manifest.json"
    guide_path = wiki / "query-guide.md"
    assert manifest_path.exists()
    assert guide_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["summary"]["canonical_answer"] == 1
