from pathlib import Path

from tools.wiki_identity import normalize_activation
from tools.witte_source import FACTOR_SEQUENCE, LineRecord, _entry_start, generate_models


PDF_PATH = Path(
    "Stellar Influences Vault/planetary expressions - Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures 2020.pdf"
)


def test_witte_factor_meanings_include_transneptunians():
    factors, _ = generate_models(PDF_PATH)

    cupido = next(block for block in factors if block.factor == "Cupido")
    poseidon = next(block for block in factors if block.factor == "Poseidon")

    assert cupido.page == 29
    assert "Family. Sociability. Societies." in cupido.text
    assert "Mental power. Idea. Cognition." in poseidon.text


def test_witte_factor_blocks_are_canonical_and_trimmed_to_factor_chapters():
    factors, _ = generate_models(PDF_PATH)

    assert [block.factor for block in factors] == FACTOR_SEQUENCE

    aries = next(block for block in factors if block.factor == "Vernal Point")
    pluto = next(block for block in factors if block.factor == "Pluto")
    poseidon = next(block for block in factors if block.factor == "Poseidon")

    assert aries.page == 27
    assert aries.text.startswith("— as representative of equinoxes and solstices")
    assert "1 x Star:" not in aries.text
    assert pluto.page == 28
    assert pluto.text.startswith("Development. Transformation. Turnaround.")
    assert "Meaning of the hypothetical Planets" not in pluto.text
    assert poseidon.page == 29
    assert poseidon.text.endswith("Floods.")
    assert "Meaning of the Houses" not in poseidon.text
    assert "Other persons, forbears, ancestors" not in poseidon.text


def test_witte_rule_page_assigns_ocr_noisy_entries_by_factor_order():
    _, pair_blocks = generate_models(PDF_PATH)

    aries_venus = next(
        block for block in pair_blocks if block.factor_a == "Vernal Point" and block.factor_b == "Venus"
    )

    entries = {entry.activated_by: entry.text for entry in aries_venus.activation_entries}

    assert aries_venus.page == 41
    assert aries_venus.summary.startswith("Attraction in general. Love in general.")
    assert entries["Mercury"].startswith("Beauty of thought.")
    assert entries["Mars"].startswith("Mating time.")
    assert entries["Poseidon"].startswith("Insights for a peaceful world.")


def test_witte_rule_page_keeps_repeated_pair_pages():
    _, pair_blocks = generate_models(PDF_PATH)

    meridian_self = next(block for block in pair_blocks if block.factor_a == "MC" and block.factor_b == "MC")
    entries = {entry.activated_by: entry.text for entry in meridian_self.activation_entries}

    assert meridian_self.page == 56
    assert meridian_self.summary.startswith("The personality of the native.")
    assert meridian_self.activation_entries[0].activated_by == "Vernal Point"
    assert entries["Sun"].startswith("Body and soul.")
    assert entries["Poseidon"].startswith("The divine spark in men.")


def test_witte_rule_page_recovers_missing_saturn_entry_from_continuation_line():
    _, pair_blocks = generate_models(PDF_PATH)

    aries_meridian = next(
        block for block in pair_blocks if block.factor_a == "Vernal Point" and block.factor_b == "MC"
    )
    entries = {entry.activated_by: entry.text for entry in aries_meridian.activation_entries}

    assert entries["Saturn"].startswith("To be mournful with others.")


def test_witte_rule_page_does_not_absorb_next_page_symbol_header():
    _, pair_blocks = generate_models(PDF_PATH)

    meridian_sun = next(block for block in pair_blocks if block.factor_a == "MC" and block.factor_b == "Sun")

    assert meridian_sun.page == 59
    assert meridian_sun.activation_entries[-1].activated_by == "Poseidon"
    assert meridian_sun.activation_entries[-1].text.startswith(
        "Union of a delicate body and a delicate, highly sensitive soul."
    )


def test_witte_rule_page_recovers_multiple_missing_entries_from_continuation_lines():
    _, pair_blocks = generate_models(PDF_PATH)

    meridian_poseidon = next(
        block for block in pair_blocks if block.factor_a == "MC" and block.factor_b == "Poseidon"
    )
    entries = {entry.activated_by: entry.text for entry in meridian_poseidon.activation_entries}

    assert entries["Mercury"].startswith("Idealistic way of thinking.")
    assert entries["Venus"].startswith("Inclination or attitude toward freedom, religion or the beauty.")


def test_witte_rule_page_does_not_treat_plain_words_as_tokens():
    _, pair_blocks = generate_models(PDF_PATH)

    asc_venus = next(block for block in pair_blocks if block.factor_a == "Asc" and block.factor_b == "Venus")
    entries = {entry.activated_by: entry.text for entry in asc_venus.activation_entries}

    assert entries["MC"].endswith("upon the mind.")
    assert entries["Admetos"].startswith("Harmonious community in a small circle.")


def test_witte_rule_page_keeps_short_alpha_ocr_tokens():
    _, pair_blocks = generate_models(PDF_PATH)

    aries_admetos = next(
        block for block in pair_blocks if block.factor_a == "Vernal Point" and block.factor_b == "Admetos"
    )
    entries = {entry.activated_by: entry.text for entry in aries_admetos.activation_entries}

    assert entries["Neptune"].startswith("To make solid.")


def test_witte_rule_page_keeps_three_letter_ocr_tokens():
    _, pair_blocks = generate_models(PDF_PATH)

    aries_poseidon = next(
        block for block in pair_blocks if block.factor_a == "Vernal Point" and block.factor_b == "Poseidon"
    )
    entries = {entry.activated_by: entry.text for entry in aries_poseidon.activation_entries}

    assert entries["MC"].startswith("Personally influenced by the ideas of the current time.")


def test_witte_rule_page_accepts_late_book_marker_lines_with_wider_indent():
    _, pair_blocks = generate_models(PDF_PATH)

    mercury_mars = next(
        block for block in pair_blocks if block.factor_a == "Mercury" and block.factor_b == "Mars"
    )
    entries = {entry.activated_by: entry.text for entry in mercury_mars.activation_entries}

    assert entries["Vulcanus"].startswith("Hasty and fast action, to conceive something fast.")
    assert entries["Poseidon"].startswith("Hasty and overly-hurried action")


def test_witte_rule_page_uses_ocr_fallback_for_sun_cupido():
    _, pair_blocks = generate_models(PDF_PATH)

    sun_cupido = next(block for block in pair_blocks if block.factor_a == "Sun" and block.factor_b == "Cupido")
    entries = {entry.activated_by: entry.text for entry in sun_cupido.activation_entries}

    assert sun_cupido.summary.startswith("Member of family, association, community or a group.")
    assert entries["MC"].startswith(
        "The native as a member of the family, as an artist, or member of an association."
    )
    assert entries["Poseidon"].startswith("The spiritually minded artist.")


def test_witte_rule_page_uses_ocr_fallback_for_sun_poseidon():
    _, pair_blocks = generate_models(PDF_PATH)

    sun_poseidon = next(block for block in pair_blocks if block.factor_a == "Sun" and block.factor_b == "Poseidon")
    entries = {entry.activated_by: entry.text for entry in sun_poseidon.activation_entries}

    assert sun_poseidon.summary.startswith("One’s own education and intellectual capacity.")
    assert entries["Vernal Point"].startswith("Men who are high minded in general.")
    assert entries["MC"].startswith("Mental and spiritual inclinations.")
    assert entries["Vulcanus"].startswith("Mental power or influence.")


def test_witte_rule_page_keeps_summary_before_first_activation_entry():
    _, pair_blocks = generate_models(PDF_PATH)

    sun_node = next(block for block in pair_blocks if block.factor_a == "Sun" and block.factor_b == "Node")
    entries = {entry.activated_by: entry.text for entry in sun_node.activation_entries}

    assert sun_node.summary.startswith("A physical union. Connections with the public.")
    assert entries["Vernal Point"].startswith("General unions or connections.")
    assert entries["MC"].startswith("Soul unions.")


def test_witte_rule_page_recovers_multiple_unmarked_entries_inside_a_block():
    _, pair_blocks = generate_models(PDF_PATH)

    neptune_cupido = next(
        block for block in pair_blocks if block.factor_a == "Neptune" and block.factor_b == "Cupido"
    )
    entries = {entry.activated_by: entry.text for entry in neptune_cupido.activation_entries}

    assert entries["Mercury"].startswith("Professional breach of promise (of marriage).")
    assert entries["Venus"].startswith("Dissonances in love marriage.")
    assert entries["Mars"].startswith("Impotence or infection of the husband.")


def test_witte_rule_page_does_not_absorb_top_of_next_page_noise():
    _, pair_blocks = generate_models(PDF_PATH)

    neptune_zeus = next(block for block in pair_blocks if block.factor_a == "Neptune" and block.factor_b == "Zeus")
    entries = {entry.activated_by: entry.text for entry in neptune_zeus.activation_entries}

    assert entries["Vulcanus"].startswith("Mighty but useless and wasted efforts.")
    assert entries["Poseidon"].startswith("Fruidess ideas, dangerous ideas.")


def test_witte_rule_page_recovers_unmarked_first_entry_after_summary():
    _, pair_blocks = generate_models(PDF_PATH)

    apollon_admetos = next(
        block for block in pair_blocks if block.factor_a == "Apollon" and block.factor_b == "Admetos"
    )
    entries = {entry.activated_by: entry.text for entry in apollon_admetos.activation_entries}

    assert entries["Vernal Point"].startswith("General tranquility. To be carefree. General contentment.")
    assert entries["MC"].startswith("The contented man.")


def test_witte_rule_page_recovers_markerless_tail_entries_on_apollon_poseidon():
    _, pair_blocks = generate_models(PDF_PATH)

    apollon_poseidon = next(
        block for block in pair_blocks if block.factor_a == "Apollon" and block.factor_b == "Poseidon"
    )
    entries = {entry.activated_by: entry.text for entry in apollon_poseidon.activation_entries}

    assert entries["Hades"].startswith(
        "Wanting in comradeship. To be disgusted with colleagues comrades or people of the same destiny."
    )
    assert entries["Zeus"].startswith("To be a leader through one’s activity with similar minded people.")
    assert entries["Kronos"].startswith(
        "To be outstandingly cultured among cultured people and rated as an example by them."
    )
    assert entries["Admetos"].startswith("Great conviction and steadfastness. Exclusive circle of similar minded people.")
    assert entries["Vulcanus"].startswith(
        "To gain great success through colleagues and comrades. To be noted or to create a sensation."
    )


def test_witte_rule_page_ignores_stray_period_before_admetos_poseidon_tail_entries():
    _, pair_blocks = generate_models(PDF_PATH)

    admetos_poseidon = next(
        block for block in pair_blocks if block.factor_a == "Admetos" and block.factor_b == "Poseidon"
    )
    entries = {entry.activated_by: entry.text for entry in admetos_poseidon.activation_entries}

    assert entries["Kronos"].startswith(
        "To be subjected to a special education or training. Specially gifted as trainer or teacher."
    )
    assert entries["Apollon"].startswith(
        "Educated and trained with many. Satisfactory state of education or training."
    )
    assert entries["Vulcanus"].startswith(
        "Mighty and lasting influence of education. To be affected that way, or to affect others that way."
    )


def test_witte_rule_page_repairs_aries_aries_poseidon_ocr_garble():
    _, pair_blocks = generate_models(PDF_PATH)

    aries_self = next(
        block
        for block in pair_blocks
        if block.factor_a == "Vernal Point" and block.factor_b == "Vernal Point"
    )
    entries = {entry.activated_by: entry.text for entry in aries_self.activation_entries}

    assert entries["Poseidon"].startswith(
        "Ideas, spirit, education, cognition, understanding and culture in the general public."
    )


def test_witte_rule_page_does_not_absorb_about_us_tail_into_poseidon_poseidon():
    _, pair_blocks = generate_models(PDF_PATH)

    poseidon_self = next(
        block for block in pair_blocks if block.factor_a == "Poseidon" and block.factor_b == "Poseidon"
    )
    entries = {entry.activated_by: entry.text for entry in poseidon_self.activation_entries}

    assert entries["Apollon"].startswith("People with the same mindset. Congenial.")
    assert entries["Admetos"].startswith("Creative education. Mental depth.")
    assert entries["Vulcanus"].startswith("State of mind. Sense of honor.")
    assert "About Us" not in entries["Apollon"]
    assert "Witte-Verlag" not in entries["Admetos"]


def test_entry_start_keeps_known_three_letter_ocr_token_fragments():
    entry = _entry_start(LineRecord(page=1, x0=50, y0=10, text="~ ffr Good luck and happiness"), allow_alpha=True)

    assert entry == ("ffr", "Good luck and happiness")


def test_entry_start_ignores_plain_lowercase_continuation_words_without_marker():
    entry = _entry_start(LineRecord(page=1, x0=60, y0=10, text="or acts which are not discovered."), allow_alpha=True)

    assert entry is None


def test_entry_start_allows_first_uppercase_token_without_marker_on_late_pages():
    entry = _entry_start(
        LineRecord(page=1, x0=44, y0=10, text="A To live in a peaceful and tranquil environment."),
        allow_alpha=False,
    )

    assert entry == ("A", "To live in a peaceful and tranquil environment.")


def test_entry_start_rejects_unmarked_summary_sentence_before_entries():
    entry = _entry_start(
        LineRecord(page=1, x0=42, y0=10, text="A physical union. Connections with the public."),
        allow_alpha=False,
    )

    assert entry is None


def test_repeated_pair_activation_normalizes_without_a_distinct_triad():
    activation = normalize_activation("MC", "MC", "Sun")

    assert activation.display == "MC/MC = Sun"
    assert activation.axis.display == "MC/MC"
    assert activation.triad_set == ("Sun", "MC")
