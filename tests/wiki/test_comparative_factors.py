from pathlib import Path

from tools.wiki_pages import load_page


SHARED_FACTORS = [
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
    "node",
    "asc",
    "mc",
]


def test_shared_factor_pages_reference_both_sources():
    for slug in SHARED_FACTORS:
        page = load_page(Path("wiki/factors") / f"{slug}.md")
        assert page.meta["source_pages"] == [
            "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures",
            "reinhold-ebertin-the-combination-of-stellar-influences",
            "robert-hand-horoscope-symbols",
        ]
        assert "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures" in page.body
        assert "Reinhold Ebertin - The Combination of Stellar Influences" in page.body
        assert "Robert Hand - Horoscope Symbols" in page.body
        assert "Contradictions and Framework Notes" in page.body
