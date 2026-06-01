from pathlib import Path

from tools.ingest_udo_rudolph_abc import (
    SOURCE_TITLE,
    _assert_translation_coverage,
    _activation_source_entry,
    _axis_source_entry,
    _clean_english_translation,
    _derived_activation_synthesis,
    _derived_axis_synthesis,
    _derived_factor_synthesis,
    _derived_schema_theme_line,
    _factor_source_entry,
    _merge_source_entries,
    _normalize_translation_source_text,
    _ordered_source_pages,
    _query_anchor_line,
    _render_activation_page,
    _render_coverage_map_page,
    _render_triad_page,
    _render_source_page,
    _render_translation_qa_page,
    _sibling_orientation_line,
    _triad_derived_synthesis,
    _translation_qa_counts,
)
from tools.udo_rudolph_abc_source import ActivationEntry, AxisBlock, FactorBlock


def test_ordered_source_pages_places_udo_after_witte():
    ordered = _ordered_source_pages(
        [
            "reinhold-ebertin-the-combination-of-stellar-influences",
            "udo-rudolph-abc-fur-planetenbilder",
            "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
        ]
    )

    assert ordered == [
        "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
        "udo-rudolph-abc-fur-planetenbilder",
        "reinhold-ebertin-the-combination-of-stellar-influences",
    ]


def test_merge_source_entries_keeps_existing_entries_and_inserts_udo_after_witte():
    body = """## Source Entries

### Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures

Witte entry.

### Reinhold Ebertin - The Combination of Stellar Influences

Ebertin entry.

## Comparative Schema
"""

    merged = _merge_source_entries(body, f"### {SOURCE_TITLE}\n\nUdo entry.", SOURCE_TITLE)

    assert merged.index("### Alfred Witte") < merged.index(f"### {SOURCE_TITLE}")
    assert merged.index(f"### {SOURCE_TITLE}") < merged.index("### Reinhold Ebertin")
    assert "Witte entry." in merged
    assert "Ebertin entry." in merged


def test_merge_source_entries_replaces_legacy_mojibake_udo_heading():
    body = """## Source Entries

### Udo Rudolph - ABC fĂĽr Planetenbilder

Old Udo block.

## Comparative Schema
"""

    merged = _merge_source_entries(body, f"### {SOURCE_TITLE}\n\nNew Udo block.", SOURCE_TITLE)

    assert "fĂĽr" not in merged
    assert merged.count(f"### {SOURCE_TITLE}") == 1
    assert "New Udo block." in merged
    assert "Old Udo block." not in merged


def test_activation_source_entry_adds_cue_based_schema_mapping():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    entry = ActivationEntry(
        activated_by="Sun",
        token="0",
        text=(
            "Beseelte offentliche Meinung, korperliche Bewegung in der Offentlichkeit, "
            "Partner im offentlichen Verkehr, offentliche Finanz-Tatigkeit"
        ),
        page=18,
    )

    translations = {
        entry.text: (
            "Animated public opinion, physical movement in public, "
            "partners in public traffic, public financial activity"
        )
    }

    source_entry = _activation_source_entry(axis, entry, translation_lookup=translations)

    assert "#### ABC Schema Mapping" in source_entry
    assert "- core meaning: Animated public opinion" in source_entry
    assert "- psychology: Animated public opinion" in source_entry
    assert "- body/health: physical movement in public" in source_entry
    assert "- social/relationship: partners in public traffic" in source_entry
    assert "- events/manifestations: public financial activity" in source_entry
    assert "Beseelte offentliche Meinung" not in source_entry


def test_axis_source_entry_adds_source_factor_context_when_available():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    factors = {
        "Vernal Point": FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit, Offentlichkeit"),
        "MC": FactorBlock("MC", "Meridian, MC", 16, "Ich, meine Seele"),
    }

    translations = {
        axis.summary: "Animated public life.",
        "Allgemeinheit, Offentlichkeit": "Generality, public life",
        "Ich, meine Seele": "I, my soul",
    }

    source_entry = _axis_source_entry(axis, factors, translations)

    assert "#### ABC Factor Context" in source_entry
    assert "- Axis factor `Vernal Point` (source keyword page `16`): Generality, public life" in source_entry
    assert "- Axis factor `MC` (source keyword page `16`): I, my soul" in source_entry
    assert "Allgemeinheit" not in source_entry
    assert "Widder" not in source_entry


def test_activation_source_entry_adds_axis_and_activator_factor_context():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    entry = ActivationEntry("Sun", "0", "Beseelter Mensch im offentlichen Leben.", 18)
    factors = {
        "Vernal Point": FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit, Offentlichkeit"),
        "MC": FactorBlock("MC", "Meridian, MC", 16, "Ich, meine Seele"),
        "Sun": FactorBlock("Sun", "Sonne, SO", 16, "Korper, Tag, Mann"),
    }

    translations = {
        entry.text: "Animated man in public life.",
        "Allgemeinheit, Offentlichkeit": "Generality, public life",
        "Ich, meine Seele": "I, my soul",
        "Korper, Tag, Mann": "Body, day, man",
    }

    source_entry = _activation_source_entry(axis, entry, factors, translations)

    assert "- Axis factor `Vernal Point` (source keyword page `16`): Generality, public life" in source_entry
    assert "- Axis factor `MC` (source keyword page `16`): I, my soul" in source_entry
    assert "- Activator `Sun` (source keyword page `16`): Body, day, man" in source_entry
    assert "Korper" not in source_entry
    assert "Sonne" not in source_entry


def test_factor_source_entry_renders_english_only_keyword_entry():
    block = FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit, Offentlichkeit")
    source_entry = _factor_source_entry(block, {block.text: "Generality, public life"})

    assert "#### ABC Keyword Entry" in source_entry
    assert "Generality and public life" in source_entry
    assert "Allgemeinheit" not in source_entry


def test_factor_source_entry_suppresses_ocr_heavy_cached_keywords():
    block = FactorBlock("Neptune", "Neptun, NE", 17, "Unbekannt, Sensibilitat")

    source_entry = _factor_source_entry(
        block,
        {
            block.text: (
                "Unbekannt, Uncertainty, Fine Flill, Sensibilitat, FIUssigkeit, water, "
                "Gestaltloses, Verneinigung"
            )
        },
    )

    assert "#### Translation QA" in source_entry
    assert "English-only translation flagged for QA" in source_entry
    assert "Unbekannt" not in source_entry
    assert "FIUssigkeit" not in source_entry


def test_derived_factor_synthesis_uses_vetted_translated_keywords():
    block = FactorBlock("Venus", "Venus, VE", 16, "Freude, Frieden, Harmonie, Liebe, Kunst")
    synthesis = _derived_factor_synthesis(block, {block.text: "joy, peace, harmony, love, art"}, 120)

    assert "`Venus`" in synthesis
    assert "Rudolph delineation" in synthesis
    assert "joy, peace, harmony, love, and art" in synthesis
    assert "120 orientation-specific activation pages" in synthesis
    assert "Query anchors" not in synthesis
    assert "Freude" not in synthesis


def test_derived_schema_theme_line_compacts_mapped_categories():
    line = _derived_schema_theme_line(
        "Animated public opinion, physical movement in public, partners in public traffic, public financial activity"
    )

    assert line == (
        "- Retrieval themes: psychology: Animated public opinion; "
        "body/health: physical movement in public; "
        "social/relationship: partners in public traffic; "
        "events/manifestations: public financial activity."
    )


def test_query_anchor_line_formats_factor_axis_and_activation_surfaces():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    entry = ActivationEntry("Sun", "0", "Beseelter Mensch im offentlichen Leben.", 18)

    assert _query_anchor_line(factor="Venus") == (
        "- Query anchors: factor `Venus`; source `Udo Rudolph`; use as factor keyword field, not as a merged formula."
    )
    assert _query_anchor_line(axis=axis) == (
        "- Query anchors: axis `Vernal Point/MC`; factors `Vernal Point`, `MC`; unordered midpoint pair; use linked activations for third-factor specification."
    )
    assert _query_anchor_line(axis=axis, entry=entry) == (
        "- Query anchors: formula `Vernal Point/MC = Sun`; axis `Vernal Point/MC`; activator `Sun`; orientation-specific activation; triad hub `Vernal Point Sun MC`."
    )


def test_sibling_orientation_line_lists_distinct_triads_without_merging():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    entry = ActivationEntry("Sun", "0", "Beseelter Mensch im offentlichen Leben.", 18)

    line = _sibling_orientation_line(axis, entry)

    assert line == (
        "- Sibling orientations: compare `Vernal Point/Sun = MC` and `Sun/MC = Vernal Point` as separate pages for the same triad; these are lookup neighbors, not merged meanings."
    )


def test_sibling_orientation_line_handles_repeated_pair_identity():
    axis = AxisBlock(
        factor_a="Sun",
        factor_b="Sun",
        source_heading="Sonne + Sonne",
        pdf_page=1,
        page_range="1",
        page=1,
        summary="Life.",
        activation_entries=[],
    )
    entry = ActivationEntry("Moon", "R", "Women.", 1)

    assert _sibling_orientation_line(axis, entry) == (
        "- Sibling orientations: repeated-pair activation; no distinct three-factor sibling pages exist."
    )


def test_derived_axis_synthesis_uses_vetted_axis_delineation():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    factors = {
        "Vernal Point": FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit, Offentlichkeit"),
        "MC": FactorBlock("MC", "Meridian, MC", 16, "Ich, meine Seele"),
    }
    translations = {
        axis.summary: "Animated public life.",
        "Allgemeinheit, Offentlichkeit": "generality, public life",
        "Ich, meine Seele": "I, my soul",
    }

    synthesis = _derived_axis_synthesis(axis, factors, translations)

    assert "`Vernal Point/MC`" in synthesis
    assert "Rudolph delineation" in synthesis
    assert "Animated public life" in synthesis
    assert "activation pages" in synthesis
    assert "Query anchors" not in synthesis
    assert "Beseelte" not in synthesis


def test_derived_activation_synthesis_uses_vetted_orientation_delineation():
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[],
    )
    entry = ActivationEntry("Sun", "0", "Beseelter Mensch im offentlichen Leben.", 18)
    factors = {
        "Vernal Point": FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit, Offentlichkeit"),
        "MC": FactorBlock("MC", "Meridian, MC", 16, "Ich, meine Seele"),
        "Sun": FactorBlock("Sun", "Sonne, SO", 16, "Korper, Tag, Mann"),
    }
    translations = {
        axis.summary: "Animated public life.",
        entry.text: "Soulful person in public life.",
        "Allgemeinheit, Offentlichkeit": "generality, public life",
        "Ich, meine Seele": "I, my soul",
        "Korper, Tag, Mann": "body, day, man",
    }

    synthesis = _derived_activation_synthesis(axis, entry, factors, translations)

    assert "`Vernal Point/MC = Sun`" in synthesis
    assert "Rudolph delineation" in synthesis
    assert "Soulful person in public life" in synthesis
    assert "Sun specifies the axis" in synthesis
    assert "- Sibling orientations: compare `Vernal Point/Sun = MC` and `Sun/MC = Vernal Point`" in synthesis
    assert "do not merge it with sibling orientations" in synthesis
    assert "Query anchors" not in synthesis
    assert "Beseelter" not in synthesis


def test_derived_axis_synthesis_filters_noisy_cached_clauses_but_keeps_good_claims():
    axis = AxisBlock(
        factor_a="Sun",
        factor_b="Moon",
        source_heading="Sonne + Mond",
        pdf_page=68,
        page_range="138-139",
        page=138,
        summary="Frau und Mann, Gefiihle des Mannes.",
        activation_entries=[],
    )

    synthesis = _derived_axis_synthesis(
        axis,
        None,
        {
            axis.summary: (
                "Woman and Man, Man's Fables, Cern i.its Man, Woman's Body, "
                "People's Corps, Human Cefiihle"
            )
        },
    )

    assert "`Sun/Moon`" in synthesis
    assert "Woman and Man" in synthesis
    assert "Woman's Body" in synthesis
    assert "Man's Fables" not in synthesis
    assert "Cern i.its" not in synthesis
    assert "Cefiihle" not in synthesis


def test_derived_activation_synthesis_filters_noisy_cached_clauses_but_keeps_good_claims():
    axis = AxisBlock(
        factor_a="Sun",
        factor_b="Moon",
        source_heading="Sonne + Mond",
        pdf_page=68,
        page_range="138-139",
        page=138,
        summary="Frau und Mann, Gefiihle des Mannes.",
        activation_entries=[],
    )
    entry = ActivationEntry("Mars", "T", "Gefilhls-Impulse des Mannes.", 139)

    synthesis = _derived_activation_synthesis(
        axis,
        entry,
        None,
        {
            axis.summary: "Woman and Man, Man's Fables, Cern i.its Man.",
            entry.text: "Treatment of women's body, activating man's ailments, men of yolks.",
        },
    )

    assert "`Sun/Moon = Mars`" in synthesis
    assert "Treatment of women's body" in synthesis
    assert "Man's Fables" not in synthesis
    assert "ailments" not in synthesis
    assert "yolks" not in synthesis


def test_derived_activation_synthesis_falls_back_to_cleaned_source_when_cache_is_corrupt():
    axis = AxisBlock(
        factor_a="Mercury",
        factor_b="Pluto",
        source_heading="Merkur + Pluto",
        pdf_page=122,
        page_range="252-253",
        page=252,
        summary=(
            "Entwicklung de.- Jugend, Denken entwickeln, Gesprache iiber Evolution, "
            "MedienEntwicklung, Meinungs-Anderungen, Meinungs-Entfaltung, "
            "Sprach-Entwicklung, Veranderungen im Denken, wachsender Verkehr, Wort-Wechsel"
        ),
        activation_entries=[],
    )
    entry = ActivationEntry(
        "Vernal Point",
        "A",
        (
            "Entwicklung dcr Jugcnd in dcr ()ffentlichkeit, Gcsprache Uber offentliche Entwicklung, "
            "Yerandcrung dcr Mfcntlichcn Meinung, Meinungs-Entfaltung in der Offentlichkeit, "
            "Yeranderungen im offcntlichcn Dcnkcn, Wort-Wcchsel in der Offentlichkeit"
        ),
        252,
    )

    synthesis = _derived_activation_synthesis(
        axis,
        entry,
        None,
        {
            axis.summary: (
                "Development de.- Youth, Developing thinking, Language iiber Evolution, "
                "MediaDevelopment, Opinion changes, Opinion development, Language development, "
                "Changing thinking, Growing traffic, Word change"
            ),
            entry.text: "Community law, EC Court of Justice, EC Court of First Instance",
        },
    )

    assert "`Mercury/Pluto = Vernal Point`" in synthesis
    assert "public development" in synthesis
    assert "opinion development in the public" in synthesis
    assert "word exchange in the public" in synthesis
    assert "EC Court" not in synthesis
    assert "dcr" not in synthesis


def test_activation_source_and_deepening_filter_runaway_repeated_translation():
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Cupido",
        source_heading="Mond + Cupido",
        pdf_page=95,
        page_range="192-193",
        page=192,
        summary="Frauen-Gemeinschaft.",
        activation_entries=[],
    )
    entry = ActivationEntry(
        "MC",
        "M",
        (
            "lkscelte Frauen-Gcmeinschafl, besceltcs Gemeinschafts-Geflihl, "
            "beseelte Kunst der Frau, Kunst meincs Volkcs, Kunst meiner Frau, "
            "mein Gemeinschafts-Geflihl meine Volks-Gemeinschaft, "
            "Seelcn- und Gemuts-Gemeinschat1, Synthcse der Yolks-Seele"
        ),
        192,
    )
    translations = {
        axis.summary: "Fraucn community, gemeinsame mother, GemiitsGcmeinschaft, art the women",
        entry.text: "Women's " + " ".join(["collective"] * 80),
    }

    source_entry = _activation_source_entry(axis, entry, translation_lookup=translations)
    synthesis = _derived_activation_synthesis(axis, entry, None, translations)

    assert "collective collective" not in source_entry
    assert "collective collective" not in synthesis
    assert "women community" in source_entry.casefold()
    assert "women community" in synthesis.casefold()
    assert "community feeling" in synthesis.casefold()
    assert "' '" not in source_entry
    assert "' '" not in synthesis
    assert "gemeinsame" not in synthesis


def test_activation_source_entry_suppresses_suspicious_cached_translation():
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Mars",
        source_heading="Mond + Mars",
        pdf_page=89,
        page_range="180-181",
        page=180,
        summary="Arbeits-Stunde.",
        activation_entries=[],
    )
    entry = ActivationEntry("MC", "M", "Bcseelte Gcfuhls-Handlungcn.", 180)

    source_entry = _activation_source_entry(
        axis,
        entry,
        translation_lookup={
            entry.text: (
                "Mr President, ladies and gentlemen, I should like to begin by thanking the President in Office "
                "of the Council for his excellent report"
            )
        },
    )

    assert "#### Translation QA" not in source_entry
    assert "soulful feelings actions" in source_entry
    assert "#### ABC Schema Mapping" in source_entry
    assert "Mr President" not in source_entry
    assert "Bcseelte" not in source_entry


def test_derived_factor_synthesis_flags_suspicious_keywords_without_echoing():
    block = FactorBlock("Moon", "Mond, MO", 16, "Frau, Mutter, Fleisch, Gemut")

    synthesis = _derived_factor_synthesis(block, {block.text: "Woman, Mother, Flesh, GemUt, Hour"}, 120)

    assert "`Moon`" in synthesis
    assert "Woman, Mother" in synthesis
    assert "emotional" in synthesis
    assert "GemUt" not in synthesis


def test_derived_axis_synthesis_flags_suspicious_summary_without_echoing():
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Mars",
        source_heading="Mond + Mars",
        pdf_page=89,
        page_range="180-181",
        page=180,
        summary="Arbeits-Stunde.",
        activation_entries=[],
    )

    synthesis = _derived_axis_synthesis(
        axis,
        None,
        {axis.summary: "Work hour, women work, manJiche's principle in women"},
    )

    assert "`Moon/Mars`" in synthesis
    assert "work hour" in synthesis
    assert "manJiche" not in synthesis


def test_derived_activation_synthesis_flags_suspicious_entry_without_echoing():
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Mars",
        source_heading="Mond + Mars",
        pdf_page=89,
        page_range="180-181",
        page=180,
        summary="Arbeits-Stunde.",
        activation_entries=[],
    )
    entry = ActivationEntry("MC", "M", "Bcseelte Gcfuhls-Handlungcn.", 180)

    synthesis = _derived_activation_synthesis(
        axis,
        entry,
        None,
        {
            axis.summary: "Work hour and active feeling.",
            entry.text: "Community law, EC Court of Justice, EC Court of Justice",
        },
    )

    assert "`Moon/Mars = MC`" in synthesis
    assert "soulful feelings actions" in synthesis
    assert "- Sibling orientations: compare `Moon/MC = Mars` and `Mars/MC = Moon`" in synthesis
    assert "EC Court" not in synthesis


def test_derived_activation_synthesis_flags_ocr_fragment_entry_without_echoing():
    axis = AxisBlock(
        factor_a="Sun",
        factor_b="Neptune",
        source_heading="Sonne + Neptun",
        pdf_page=1,
        page_range="1",
        page=1,
        summary="Unklarer Mensch.",
        activation_entries=[],
    )
    entry = ActivationEntry("Hades", "C", "Gefahrdeter Mensch.", 1)

    synthesis = _derived_activation_synthesis(
        axis,
        entry,
        None,
        {
            axis.summary: "Shapeless body, corpedic sensibi!itat, personal insecurity.",
            entry.text: "Man replaced by need, dangerous body FIUsability, corporal deficiency and weak.",
        },
    )

    assert "`Sun/Neptune = Hades`" in synthesis
    assert "endangered people" in synthesis
    assert "FIUsability" not in synthesis
    assert "sensibi!itat" not in synthesis


def test_triad_derived_synthesis_maps_rudolph_orientations_without_merging(tmp_path: Path):
    activation_dir = tmp_path / "activations"
    activation_dir.mkdir()
    (activation_dir / "vernal-point-mc-equals-sun.md").write_text(
        f"""---
title: Vernal Point/MC = Sun
page_type: activation
slug: vernal-point-mc-equals-sun
source_pages:
  - udo-rudolph-abc-fur-planetenbilder
---

## Source Entries

### {SOURCE_TITLE}

- Source formula: `Vernal Point/MC = Sun`
- Source page: `18`

#### ABC Entry

Soulful person in public life, animated center in public, my person in public, my life in public
""",
        encoding="utf-8",
    )
    (activation_dir / "vernal-point-sun-equals-mc.md").write_text(
        f"""---
title: Vernal Point/Sun = MC
page_type: activation
slug: vernal-point-sun-equals-mc
source_pages:
  - udo-rudolph-abc-fur-planetenbilder
---

## Source Entries

### {SOURCE_TITLE}

- Source formula: `Vernal Point/Sun = MC`
- Source page: `22`

#### ABC Entry

I live in public, public life of the soul, public selfhood
""",
        encoding="utf-8",
    )

    synthesis = _triad_derived_synthesis(("Vernal Point", "Sun", "MC"), activation_dir)

    assert "### Udo Rudolph Orientation Map" in synthesis
    assert "- Triad role: `Vernal Point Sun MC` is a structural lookup hub" in synthesis
    assert "- Orientation `Vernal Point/MC = Sun`: Soulful person in public life, animated center in public, my person in public, and my life in public." in synthesis
    assert "- Orientation `Vernal Point/Sun = MC`: I live in public, public life of the soul, and public selfhood." in synthesis
    assert "- Orientation `Sun/MC = Vernal Point`: activation page not available." in synthesis
    assert "- Query anchors: triad hub `Vernal Point Sun MC`; source `Udo Rudolph`; compare sibling activation pages without merging their meanings." in synthesis
    assert "Beseelter" not in synthesis


def test_triad_derived_synthesis_flags_suspicious_cached_translation(tmp_path: Path):
    activation_dir = tmp_path / "activations"
    activation_dir.mkdir()
    (activation_dir / "vernal-point-mc-equals-sun.md").write_text(
        f"""---
title: Vernal Point/MC = Sun
page_type: activation
slug: vernal-point-mc-equals-sun
source_pages:
  - udo-rudolph-abc-fur-planetenbilder
---

## Source Entries

### {SOURCE_TITLE}

- Source formula: `Vernal Point/MC = Sun`
- Source page: `18`

#### ABC Entry

Community law, EC Court of Justice, EC Court of Justice, EC Court of Justice
""",
        encoding="utf-8",
    )

    synthesis = _triad_derived_synthesis(("Vernal Point", "Sun", "MC"), activation_dir)

    assert "- Orientation `Vernal Point/MC = Sun`: ABC entry present; cached English preview is flagged for translation QA." in synthesis
    assert "EC Court of Justice" not in synthesis


def test_triad_derived_synthesis_treats_qa_placeholder_as_flagged(tmp_path: Path):
    activation_dir = tmp_path / "activations"
    activation_dir.mkdir()
    (activation_dir / "vernal-point-mc-equals-sun.md").write_text(
        f"""---
title: Vernal Point/MC = Sun
page_type: activation
slug: vernal-point-mc-equals-sun
source_pages:
  - udo-rudolph-abc-fur-planetenbilder
---

## Source Entries

### {SOURCE_TITLE}

- Source formula: `Vernal Point/MC = Sun`
- Source page: `18`

#### ABC Entry

English-only translation flagged for QA; cached wording is not rendered until reviewed.
""",
        encoding="utf-8",
    )

    synthesis = _triad_derived_synthesis(("Vernal Point", "Sun", "MC"), activation_dir)

    assert "- Orientation `Vernal Point/MC = Sun`: ABC entry present; cached English preview is flagged for translation QA." in synthesis
    assert "cached wording is not rendered" not in synthesis


def test_render_triad_page_includes_rudolph_derived_synthesis(tmp_path: Path):
    activation_dir = tmp_path / "activations"
    activation_dir.mkdir()
    for slug, formula, entry in (
        (
            "sun-mc-equals-vernal-point",
            "Sun/MC = Vernal Point",
            "Public body and public conduct",
        ),
        (
            "vernal-point-mc-equals-sun",
            "Vernal Point/MC = Sun",
            "Soulful person in public life",
        ),
        (
            "vernal-point-sun-equals-mc",
            "Vernal Point/Sun = MC",
            "I live in public",
        ),
    ):
        (activation_dir / f"{slug}.md").write_text(
            f"""---
title: {formula}
page_type: activation
slug: {slug}
source_pages:
  - udo-rudolph-abc-fur-planetenbilder
---

## Source Entries

### {SOURCE_TITLE}

- Source formula: `{formula}`
- Source page: `18`

#### ABC Entry

{entry}
""",
            encoding="utf-8",
        )

    rendered = _render_triad_page(("Vernal Point", "Sun", "MC"), activation_dir)

    assert "## Derived Synthesis" in rendered
    assert "### Udo Rudolph Orientation Map" in rendered
    assert "- Orientation `Sun/MC = Vernal Point`: Public body and public conduct." in rendered
    assert "This page is structural only" in rendered
    assert "without merging their meanings" in rendered


def test_translation_normalization_and_cleanup_remove_common_german_ocr_artifacts():
    source = "Kilnstlerische Menschen in der Offentlichkeit, Manner-Gemeinschaft fur die Offentlichkeit"
    rendered = "Kilnstlerische Menschen in der Offentlichkeit, Manner-Gemeinschaft für die Offentlichkeit"

    normalized = _normalize_translation_source_text(source)
    cleaned = _clean_english_translation(rendered)

    assert "Künstlerische" in normalized
    assert "Öffentlichkeit" in normalized
    assert cleaned == "artistic people in the public, men community for the public"


def test_assert_translation_coverage_requires_every_rudolph_delineation():
    factor = FactorBlock("Vernal Point", "Widder, WI", 16, "Allgemeinheit")
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[ActivationEntry("Sun", "0", "Beseelter Mensch.", 18)],
    )

    try:
        _assert_translation_coverage((factor,), (axis,), {"Allgemeinheit": "Generality"})
    except ValueError as error:
        message = str(error)
    else:
        raise AssertionError("missing translations should raise")

    assert "Beseelte Offentlichkeit." in message
    assert "Beseelter Mensch." in message


def test_translation_qa_counts_flag_suspicious_factor_axis_and_activation_entries():
    factor = FactorBlock("Neptune", "Neptun, NE", 17, "Unbekannt, Sensibilitat")
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Mars",
        source_heading="Mond + Mars",
        pdf_page=89,
        page_range="180-181",
        page=180,
        summary="Arbeits-Stunde.",
        activation_entries=[
            ActivationEntry("MC", "M", "Bcseelte Gcfuhls-Handlungcn.", 180),
            ActivationEntry("Sun", "0", "Beseelter Mensch.", 181),
        ],
    )
    translations = {
        factor.text: "Unbekannt, Sensibilitat, FIUssigkeit",
        axis.summary: "Work hour, women work, manJiche's principle in women",
        axis.activation_entries[0].text: "Community law, EC Court of Justice",
        axis.activation_entries[1].text: "Soulful person.",
    }

    counts = _translation_qa_counts((factor,), (axis,), translations)

    assert counts == {
        "factor": 1,
        "axis": 1,
        "activation": 1,
        "total": 3,
    }


def test_render_translation_qa_page_lists_review_targets_without_source_text():
    factor = FactorBlock("Neptune", "Neptun, NE", 17, "Unbekannt, Sensibilitat")
    axis = AxisBlock(
        factor_a="Moon",
        factor_b="Mars",
        source_heading="Mond + Mars",
        pdf_page=89,
        page_range="180-181",
        page=180,
        summary="Arbeits-Stunde.",
        activation_entries=[
            ActivationEntry("MC", "M", "Bcseelte Gcfuhls-Handlungcn.", 180),
            ActivationEntry("Sun", "0", "Beseelter Mensch.", 181),
        ],
    )
    translations = {
        factor.text: "Unbekannt, Sensibilitat, FIUssigkeit",
        axis.summary: "Work hour, women work, manJiche's principle in women",
        axis.activation_entries[0].text: "Community law, EC Court of Justice",
        axis.activation_entries[1].text: "Soulful person.",
    }

    rendered = _render_translation_qa_page((factor,), (axis,), translations)

    assert "page_type: derived" in rendered
    assert "slug: udo-rudolph-abc-translation-qa" in rendered
    assert "- Flagged factor keyword entries: `1`." in rendered
    assert "- Flagged axis pair summaries: `1`." in rendered
    assert "- Flagged activation entries: `1`." in rendered
    assert "- Total flagged source entries: `3`." in rendered
    assert "- [Neptune](../factors/neptune.md): factor keyword page `17`." in rendered
    assert "- [Moon/Mars](../axes/moon-mars.md): ABC pair summary pages `180-181`; PDF page `89`." in rendered
    assert "- [Moon/Mars = MC](../activations/moon-mars-equals-mc.md): source page `180`; PDF page `89`." in rendered
    assert "German original" in rendered
    assert "Unbekannt" not in rendered
    assert "EC Court" not in rendered
    assert "Bcseelte" not in rendered


def test_render_coverage_map_page_summarizes_factor_axis_activation_geometry():
    factors = (
        FactorBlock("Sun", "Sonne, SO", 16, "Korper"),
        FactorBlock("Moon", "Mond, MO", 16, "Frau"),
        FactorBlock("Venus", "Venus, VE", 16, "Liebe"),
    )
    axes = (
        AxisBlock(
            factor_a="Sun",
            factor_b="Moon",
            source_heading="Sonne + Mond",
            pdf_page=1,
            page_range="10-11",
            page=10,
            summary="Marriage.",
            activation_entries=[ActivationEntry("Venus", "V", "Love marriage.", 10)],
        ),
        AxisBlock(
            factor_a="Sun",
            factor_b="Venus",
            source_heading="Sonne + Venus",
            pdf_page=2,
            page_range="12-13",
            page=12,
            summary="Joy.",
            activation_entries=[ActivationEntry("Moon", "M", "Woman's joy.", 12)],
        ),
        AxisBlock(
            factor_a="Moon",
            factor_b="Venus",
            source_heading="Mond + Venus",
            pdf_page=3,
            page_range="14-15",
            page=14,
            summary="Feeling love.",
            activation_entries=[ActivationEntry("Sun", "S", "Loving person.", 14)],
        ),
    )

    rendered = _render_coverage_map_page(factors, axes)

    assert "page_type: derived" in rendered
    assert "slug: udo-rudolph-abc-coverage-map" in rendered
    assert "- Factor keyword pages: `3`." in rendered
    assert "- Distinct unordered axes: `3`." in rendered
    assert "- Orientation-specific activation entries: `3`." in rendered
    assert "- Distinct triad hubs: `1`." in rendered
    assert "- [Sun](../factors/sun.md): axes `2`; activation pages involving factor `3`; activator entries `1`; triad hubs involving factor `1`." in rendered
    assert "- [Moon](../factors/moon.md): axes `2`; activation pages involving factor `3`; activator entries `1`; triad hubs involving factor `1`." in rendered
    assert "- [Venus](../factors/venus.md): axes `2`; activation pages involving factor `3`; activator entries `1`; triad hubs involving factor `1`." in rendered
    assert "Triad hubs are structural only" in rendered


def test_render_source_page_uses_unicode_title_and_documents_schema_deepening():
    rendered = _render_source_page(
        factor_blocks=(),
        axis_count=231,
        activation_count=4620,
        triad_count=1540,
        translation_qa_count=391,
    )

    assert "ABC for Planetary Pictures" in rendered
    assert "ABC für Planetenbilder" not in rendered
    assert "fĂĽr" not in rendered
    assert "## ABC Schema Mapping Notes" in rendered
    assert "source-native clauses into the shared comparative schema" in rendered
    assert "## Coverage Map" in rendered
    assert "[Udo Rudolph ABC Coverage Map](../derived/udo-rudolph-abc-coverage-map.md)" in rendered
    assert "## Translation QA" in rendered
    assert "Flagged English-only entries withheld from synthesis: `391`." in rendered
    assert "[Udo Rudolph ABC Translation QA](../derived/udo-rudolph-abc-translation-qa.md)" in rendered


def test_render_activation_page_merges_udo_source_entry_into_existing_page(tmp_path: Path):
    page_path = tmp_path / "vernal-point-mc-equals-sun.md"
    page_path.write_text(
        """---
title: Vernal Point/MC = Sun
page_type: activation
slug: vernal-point-mc-equals-sun
status: source_ingested
framework_scope: hamburg_school
factors:
  - Vernal Point
  - MC
  - Sun
normalized_formula: Vernal Point/MC = Sun
axis: Vernal Point/MC
activated_by: Sun
triad_set:
  - Vernal Point
  - Sun
  - MC
aliases: []
source_pages:
  - alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures
updated_at: 2026-04-21
---

## Identity

- Formula: `Vernal Point/MC = Sun`
- Axis page: [Vernal Point/MC](../axes/vernal-point-mc.md)
- Triad hub: [Vernal Point Sun MC](../triads/vernal-point-sun-mc.md)

## Source Entries

### Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures

Witte entry.

## Comparative Schema

- core meaning: existing.

## Contradictions

- None.

## Derived Synthesis


## Links

- [Vernal Point](../factors/vernal-point.md)
""",
        encoding="utf-8",
    )
    axis = AxisBlock(
        factor_a="Vernal Point",
        factor_b="MC",
        source_heading="Widder + Meridian",
        pdf_page=8,
        page_range="18-19",
        page=18,
        summary="Beseelte Offentlichkeit.",
        activation_entries=[
            ActivationEntry(
                activated_by="Sun",
                token="0",
                text="Beseelter Mensch im offentlichen Leben.",
                page=18,
            )
        ],
    )

    rendered = _render_activation_page(
        page_path,
        axis,
        axis.activation_entries[0],
        translation_lookup={
            axis.summary: "Animated public life.",
            axis.activation_entries[0].text: "Soulful person in public life.",
        },
    )

    assert "framework_scope: comparative" in rendered
    assert "  - udo-rudolph-abc-fur-planetenbilder" in rendered
    assert f"### {SOURCE_TITLE}" in rendered
    assert "Witte entry." in rendered
    assert "#### ABC Entry" in rendered
    assert "Soulful person in public life." in rendered
    assert "Beseelter Mensch im offentlichen Leben." not in rendered
    assert "### Udo Rudolph Deepening" in rendered
    assert "`Vernal Point/MC = Sun` indicates Soulful person in public life" in rendered
