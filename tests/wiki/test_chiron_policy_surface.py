from pathlib import Path

from tools.query_manifest import build_query_manifest
from tools.wiki_pages import load_page


def test_chiron_factor_page_is_explicitly_source_bounded_and_non_doctrinal():
    page = load_page(Path("wiki/factors/chiron.md"))
    identity = page.body.split("\n## Identity\n", 1)[1].split("\n## ", 1)[0]
    sources = page.body.split("\n## Source Entries\n", 1)[1].split("\n## ", 1)[0]

    assert page.meta["framework_scope"] == "modern_astrology"
    assert page.meta["structural_only"] is True
    assert page.meta["source_pages"] == [
        "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
    ]
    assert "Sandbach's modern midpoint corpus" in identity
    assert "formula lookup rather than standalone factor doctrine" in identity
    assert "No standalone factor chapter material from this source is ingested" in sources

    record = next(
        record
        for record in build_query_manifest(Path("wiki"))["pages"]
        if record["slug"] == "chiron"
    )
    assert record["retrieval_role"] == "structural_only"
    assert record["structural_only"] is True
    assert record["answer_surface"] is False


def test_chiron_derived_note_frames_the_layer_as_single_source_modern_scope():
    page = load_page(Path("wiki/derived/chiron-in-sandbach-midpoint-corpus.md"))

    assert "Sandbach is the only live source in this repo that currently makes `Chiron` a first-class participant" in page.body
    assert "This establishes a single-source modern layer, not cross-source `Chiron` doctrine." in page.body
    assert "The present issue is source asymmetry, not contradiction." in page.body
    assert "That means `Chiron` is both a doctrine topic and a corpus-boundary marker" not in page.body


def test_factor_manifest_routes_only_explicit_structural_metadata_to_lookup(tmp_path: Path) -> None:
    # Given: a structural factor and an ordinary factor share the canonical page type.
    wiki = tmp_path / "wiki"
    factors = wiki / "factors"
    factors.mkdir(parents=True)
    for name, marker in (("Chiron", "structural_only: true\n"), ("Sun", "")):
        (factors / f"{name.casefold()}.md").write_text(
            "---\n"
            f"title: {name}\n"
            "page_type: factor\n"
            f"slug: {name.casefold()}\n"
            f"{marker}"
            "---\n",
            encoding="utf-8",
        )

    # When: the retrieval manifest is built.
    manifest = build_query_manifest(wiki)
    records = {page["slug"]: page for page in manifest["pages"]}

    # Then: the explicit structural flag changes only that factor's answer role.
    assert records["chiron"]["retrieval_role"] == "structural_only"
    assert records["chiron"]["answer_surface"] is False
    assert records["chiron"]["structural_only"] is True
    assert records["sun"]["retrieval_role"] == "canonical_answer"
    assert records["sun"]["answer_surface"] is True
    assert records["sun"]["structural_only"] is False
