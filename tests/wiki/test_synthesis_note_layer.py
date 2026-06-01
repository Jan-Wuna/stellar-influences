import json
from pathlib import Path

from tools.wiki_pages import load_page


def test_shared_factor_throughline_note_is_present_in_query_artifacts():
    guide = Path("wiki/query-guide.md").read_text(encoding="utf-8")
    manifest = json.loads(Path("wiki/query-manifest.json").read_text(encoding="utf-8"))

    assert "- Count: `5`" in guide
    assert "- Shared Factor Throughline: Witte and Ebertin" in guide
    assert "- Axis Reading Throughline: Falis and Carter" in guide
    assert "- Orientation Reading Throughline: Witte and Sandbach" in guide
    assert "- Midpoint Methodology Layer: McBroom" in guide

    by_slug = {page["slug"]: page for page in manifest["pages"]}
    record = by_slug["shared-factor-throughline-witte-ebertin"]
    assert record["retrieval_role"] == "synthesis_note"
    assert record["answer_surface"] is True
    assert record["has_real_derived_synthesis"] is True

    axis_record = by_slug["axis-reading-throughline-falis-carter"]
    assert axis_record["retrieval_role"] == "synthesis_note"
    assert axis_record["answer_surface"] is True
    assert axis_record["has_real_derived_synthesis"] is True

    orientation_record = by_slug["orientation-reading-throughline-witte-sandbach"]
    assert orientation_record["retrieval_role"] == "synthesis_note"
    assert orientation_record["answer_surface"] is True
    assert orientation_record["has_real_derived_synthesis"] is True

    methodology_record = by_slug["midpoint-methodology-layer-mcbroom"]
    assert methodology_record["retrieval_role"] == "synthesis_note"
    assert methodology_record["answer_surface"] is True


def test_shared_factor_throughline_note_stays_answer_facing():
    page = load_page(Path("wiki/derived/shared-factor-throughline-witte-ebertin.md"))

    assert page.meta["page_type"] == "derived"
    assert page.meta["framework_scope"] == "comparative"
    assert "Read the `13` shared Witte/Ebertin factor pages as a two-layer surface" in page.body
    assert "Witte supplies the compressed operational core." in page.body
    assert "Ebertin supplies the explanatory expansion." in page.body
    assert "## Derived Synthesis" in page.body


def test_axis_reading_throughline_note_stays_answer_facing():
    page = load_page(Path("wiki/derived/axis-reading-throughline-falis-carter.md"))

    assert page.meta["page_type"] == "derived"
    assert page.meta["framework_scope"] == "comparative"
    assert "Read the shared Falis/Carter axis pages as a dual reading surface" in page.body
    assert "Falis supplies associative reach." in page.body
    assert "Carter supplies tonal discrimination." in page.body
    assert "## Derived Synthesis" in page.body


def test_orientation_reading_throughline_note_stays_answer_facing():
    page = load_page(Path("wiki/derived/orientation-reading-throughline-witte-sandbach.md"))

    assert page.meta["page_type"] == "derived"
    assert page.meta["framework_scope"] == "comparative"
    assert "Read shared Witte/Sandbach activation pages orientation by orientation" in page.body
    assert "Witte supplies the compressed outcome-key." in page.body
    assert "Sandbach supplies the process expansion." in page.body
    assert "## Derived Synthesis" in page.body
