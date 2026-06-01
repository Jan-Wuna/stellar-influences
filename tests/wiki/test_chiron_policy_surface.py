from pathlib import Path

from tools.wiki_pages import load_page


def test_chiron_factor_page_is_explicitly_source_bounded_and_non_doctrinal():
    page = load_page(Path("wiki/factors/chiron.md"))

    assert page.meta["framework_scope"] == "modern_astrology"
    assert "This page is source-bounded to Sandbach's modern midpoint corpus." in page.body
    assert "Do not read it as a comparative factor doctrine page." in page.body
    assert "This factor page should not be used as standalone `Chiron` doctrine." in page.body


def test_chiron_derived_note_frames_the_layer_as_single_source_modern_scope():
    page = load_page(Path("wiki/derived/chiron-in-sandbach-midpoint-corpus.md"))

    assert "Sandbach is the only live source in this repo that currently makes `Chiron` a first-class participant" in page.body
    assert "This establishes a single-source modern layer, not cross-source `Chiron` doctrine." in page.body
    assert "The present issue is source asymmetry, not contradiction." in page.body
    assert "That means `Chiron` is both a doctrine topic and a corpus-boundary marker" not in page.body
