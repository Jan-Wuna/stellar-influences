import sqlite3
from pathlib import Path

from tools.local_query_core import (
    AnswerPage,
    RankedPage,
    build_index,
    chunks_for_page,
    classify_section,
    fallback_query_plan,
    rank_pages,
    render_llm_results,
)


def test_classify_section_prioritizes_derived_and_body_sections():
    assert classify_section("Derived Synthesis") == ("derived_synthesis", 3.0)
    assert classify_section("Biological Correspondence") == ("body_health", 2.5)
    assert classify_section("Probable Manifestations") == ("events_manifestations", 2.0)


def test_chunks_for_page_keeps_page_identity_and_section_weights(tmp_path: Path):
    page = AnswerPage(
        title="Mars/Zeus = Saturn",
        slug="mars-zeus-equals-saturn",
        path=tmp_path / "wiki" / "activations" / "mars-zeus-equals-saturn.md",
        page_type="activation",
        retrieval_role="canonical_answer",
        answer_priority=112,
        factors=("Mars", "Zeus", "Saturn"),
        source_count=3,
        body=(
            "## Identity\n"
            "- Formula: `Mars/Zeus = Saturn`\n"
            "\n"
            "## Derived Synthesis\n"
            "- Controlled force, disciplined conflict, and restrained combat technique.\n"
            "\n"
            "## Biological Correspondence\n"
            "- Bodily strain, injury, inflammation, and pressure on muscular systems.\n"
        ),
    )

    chunks = chunks_for_page(page)

    assert {chunk.section_kind for chunk in chunks} == {"derived_synthesis", "body_health"}
    assert all(chunk.page_title == "Mars/Zeus = Saturn" for chunk in chunks)
    assert all(chunk.factors == ("Mars", "Zeus", "Saturn") for chunk in chunks)


def test_build_index_filters_to_canonical_answer_pages_and_supports_fts(tmp_path: Path):
    wiki = tmp_path / "wiki"
    activation = wiki / "activations" / "mars-zeus-equals-saturn.md"
    activation.parent.mkdir(parents=True)
    activation.write_text(
        "---\n"
        "title: Mars/Zeus = Saturn\n"
        "page_type: activation\n"
        "slug: mars-zeus-equals-saturn\n"
        "factors:\n"
        "  - Mars\n"
        "  - Zeus\n"
        "  - Saturn\n"
        "---\n"
        "\n"
        "## Derived Synthesis\n"
        "- Martial discipline, controlled fighting, training, and restrained combat pressure.\n"
        "\n"
        "## Biological Correspondence\n"
        "- Muscular strain and injury during forceful exertion.\n",
        encoding="utf-8",
    )
    triad = wiki / "triads" / "mars-zeus-saturn.md"
    triad.parent.mkdir(parents=True)
    triad.write_text(
        "---\n"
        "title: Mars Zeus Saturn\n"
        "page_type: triad_hub\n"
        "slug: mars-zeus-saturn\n"
        "---\n"
        "\n"
        "## Identity\n"
        "- This page is structural only.\n",
        encoding="utf-8",
    )
    (wiki / "query-manifest.json").write_text(
        """{
  "pages": [
    {
      "title": "Mars/Zeus = Saturn",
      "slug": "mars-zeus-equals-saturn",
      "path": "wiki/activations/mars-zeus-equals-saturn.md",
      "page_type": "activation",
      "retrieval_role": "canonical_answer",
      "answer_priority": 112,
      "factors": ["Mars", "Zeus", "Saturn"],
      "source_count": 3
    },
    {
      "title": "Mars Zeus Saturn",
      "slug": "mars-zeus-saturn",
      "path": "wiki/triads/mars-zeus-saturn.md",
      "page_type": "triad_hub",
      "retrieval_role": "structural_only",
      "answer_priority": 20,
      "factors": ["Mars", "Zeus", "Saturn"],
      "source_count": 1
    }
  ]
}""",
        encoding="utf-8",
    )
    db_path = tmp_path / "index.sqlite"

    chunk_count = build_index(wiki, db_path, with_embeddings=False)

    assert chunk_count == 2
    with sqlite3.connect(db_path) as connection:
        page_types = {row[0] for row in connection.execute("SELECT DISTINCT page_type FROM chunks")}
    assert page_types == {"activation"}

    ranked = rank_pages(db_path, fallback_query_plan("martial arts combat training"), limit=3)

    assert len(ranked) == 1
    assert ranked[0].title == "Mars/Zeus = Saturn"
    assert ranked[0].page_type == "activation"
    assert "combat" in ranked[0].snippets[0]


def test_rank_pages_combines_fixture_semantic_scores_without_ollama(tmp_path: Path, monkeypatch):
    db_path = tmp_path / "index.sqlite"
    build_test_db_with_embeddings(db_path)

    monkeypatch.setattr(
        "tools.local_query_core.ollama_embed",
        lambda texts, model: [[1.0, 0.0]],
    )

    ranked = rank_pages(db_path, fallback_query_plan("digestive tract"), limit=2, embed_model="fixture")

    assert ranked[0].title == "Moon/Hades"
    assert ranked[0].score > ranked[1].score


def test_render_llm_results_dedupes_paths_and_uses_candidate_metadata():
    candidates = [
        RankedPage(
            title="Moon",
            path="wiki/factors/moon.md",
            page_type="factor",
            factors=("Moon",),
            score=1.0,
            reasons=(),
            snippets=(),
        ),
        RankedPage(
            title="Moon",
            path="wiki/factors/moon.md",
            page_type="factor",
            factors=("Moon",),
            score=0.9,
            reasons=(),
            snippets=(),
        ),
        RankedPage(
            title="Moon/Mars",
            path="wiki/axes/moon-mars.md",
            page_type="axis",
            factors=("Moon", "Mars"),
            score=0.8,
            reasons=(),
            snippets=(),
        ),
    ]

    rendered = render_llm_results(
        [
            {"candidate_id": 1, "why": "stomach", "evidence": "Stomach", "confidence": "high"},
            {"candidate_id": 2, "why": "duplicate", "evidence": "Stomach", "confidence": "high"},
            {"candidate_id": 3, "why": "acid conditions", "evidence": "stomach ulcers", "confidence": "medium"},
        ],
        candidates,
    )

    assert rendered.count("wiki/factors/moon.md") == 1
    assert "Moon/Mars" in rendered


def build_test_db_with_embeddings(db_path: Path) -> None:
    from tools.local_query_core import create_schema, pack_vector

    with sqlite3.connect(db_path) as connection:
        create_schema(connection)
        rows = [
            (
                "moon-hades",
                "Moon/Hades",
                "axis",
                "wiki/axes/moon-hades.md",
                "canonical_answer",
                110,
                '["Moon", "Hades"]',
                2,
                "Biological Correspondence",
                "body_health",
                "Digestive weakness, stomach trouble, and bodily waste processes.",
                2.5,
            ),
            (
                "mars-zeus",
                "Mars/Zeus",
                "axis",
                "wiki/axes/mars-zeus.md",
                "canonical_answer",
                110,
                '["Mars", "Zeus"]',
                2,
                "Pair Summary",
                "source_entry",
                "Fighting force, combat, fire, weapons, and energetic action.",
                1.5,
            ),
        ]
        connection.executemany(
            """
            INSERT INTO chunks (
                page_slug,
                page_title,
                page_type,
                page_path,
                retrieval_role,
                answer_priority,
                factors_json,
                source_count,
                section_title,
                section_kind,
                text,
                weight
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.executemany(
            "INSERT INTO chunk_fts(rowid, page_title, factors, section_title, text, chunk_id) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "Moon/Hades", "Moon Hades", "Biological Correspondence", rows[0][-2], "1"),
                (2, "Mars/Zeus", "Mars Zeus", "Pair Summary", rows[1][-2], "2"),
            ],
        )
        connection.executemany(
            "INSERT INTO chunk_embeddings(chunk_id, model, dimensions, vector) VALUES (?, ?, ?, ?)",
            [
                (1, "fixture", 2, pack_vector([1.0, 0.0])),
                (2, "fixture", 2, pack_vector([0.0, 1.0])),
            ],
        )
        connection.execute("INSERT INTO meta(key, value) VALUES ('embed_model', 'fixture')")
