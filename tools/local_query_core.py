from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
import struct
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from tools.wiki_pages import load_page


DEFAULT_DB_PATH = Path(".stellar-query") / "local-query.sqlite"
DEFAULT_EMBED_MODEL = "embeddinggemma"
DEFAULT_CHAT_MODEL = "qwen3:8b"
ANSWER_PAGE_TYPES = {"activation", "axis", "factor"}


@dataclass(frozen=True)
class AnswerPage:
    title: str
    slug: str
    path: Path
    page_type: str
    retrieval_role: str
    answer_priority: int
    factors: tuple[str, ...]
    source_count: int
    body: str


@dataclass(frozen=True)
class Chunk:
    page_slug: str
    page_title: str
    page_type: str
    page_path: str
    retrieval_role: str
    answer_priority: int
    factors: tuple[str, ...]
    source_count: int
    section_title: str
    section_kind: str
    text: str
    weight: float


@dataclass(frozen=True)
class QueryPlan:
    query: str
    interpreted_query: str
    concepts: tuple[str, ...]
    synonyms: tuple[str, ...]
    factor_hypotheses: tuple[str, ...]
    avoid: tuple[str, ...]

    @property
    def retrieval_text(self) -> str:
        parts = [self.query, self.interpreted_query]
        parts.extend(self.concepts)
        parts.extend(self.synonyms)
        parts.extend(self.factor_hypotheses)
        return " ".join(part for part in parts if part).strip()


@dataclass(frozen=True)
class RankedPage:
    title: str
    path: str
    page_type: str
    factors: tuple[str, ...]
    score: float
    reasons: tuple[str, ...]
    snippets: tuple[str, ...]


def load_manifest_answer_pages(wiki_root: Path) -> list[AnswerPage]:
    manifest_path = wiki_root / "query-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing query manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages: list[AnswerPage] = []
    for record in manifest["pages"]:
        if record.get("page_type") not in ANSWER_PAGE_TYPES:
            continue
        if record.get("retrieval_role") != "canonical_answer":
            continue
        path = Path(record["path"])
        if not path.is_absolute():
            path = wiki_root.parent / path
        page = load_page(path)
        pages.append(
            AnswerPage(
                title=str(record.get("title", page.meta.get("title", path.stem))),
                slug=str(record.get("slug", page.meta.get("slug", path.stem))),
                path=path,
                page_type=str(record.get("page_type", page.meta.get("page_type", ""))),
                retrieval_role=str(record.get("retrieval_role", "")),
                answer_priority=int(record.get("answer_priority", 0)),
                factors=tuple(str(factor) for factor in record.get("factors", []) or []),
                source_count=int(record.get("source_count", 0)),
                body=page.body,
            )
        )
    return pages


def chunks_for_page(page: AnswerPage) -> list[Chunk]:
    sections = split_markdown_sections(page.body)
    chunks: list[Chunk] = []
    for title, text in sections:
        clean = normalize_text(text)
        if len(clean) < 40:
            continue
        kind, weight = classify_section(title)
        chunks.append(
            Chunk(
                page_slug=page.slug,
                page_title=page.title,
                page_type=page.page_type,
                page_path=page.path.as_posix(),
                retrieval_role=page.retrieval_role,
                answer_priority=page.answer_priority,
                factors=page.factors,
                source_count=page.source_count,
                section_title=title,
                section_kind=kind,
                text=clean,
                weight=weight,
            )
        )
    return chunks


def split_markdown_sections(body: str) -> list[tuple[str, str]]:
    normalized = body.replace("\r\n", "\n")
    matches = list(re.finditer(r"^(#{2,4})\s+(.+?)\s*$", normalized, flags=re.MULTILINE))
    if not matches:
        return [("Page", normalized)]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        sections.append((title, normalized[start:end].strip()))
    return sections


def classify_section(title: str) -> tuple[str, float]:
    lower = title.casefold()
    if "derived synthesis" in lower:
        return "derived_synthesis", 3.0
    if any(token in lower for token in ("biological", "body", "health", "medical")):
        return "body_health", 2.5
    if any(token in lower for token in ("manifestation", "event", "probable")):
        return "events_manifestations", 2.0
    if any(token in lower for token in ("psychological", "sociological", "relationship", "social")):
        return "psychology_social", 1.8
    if any(token in lower for token in ("principle", "summary", "entry", "meaning")):
        return "source_entry", 1.5
    if "comparative schema" in lower:
        return "comparative_schema", 1.2
    return "general", 1.0


def normalize_text(text: str) -> str:
    without_links = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    without_markup = re.sub(r"<[^>]+>", " ", without_links)
    return re.sub(r"\s+", " ", without_markup).strip()


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        DROP TABLE IF EXISTS meta;
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS chunk_embeddings;
        DROP TABLE IF EXISTS chunk_fts;

        CREATE TABLE meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY,
            page_slug TEXT NOT NULL,
            page_title TEXT NOT NULL,
            page_type TEXT NOT NULL,
            page_path TEXT NOT NULL,
            retrieval_role TEXT NOT NULL,
            answer_priority INTEGER NOT NULL,
            factors_json TEXT NOT NULL,
            source_count INTEGER NOT NULL,
            section_title TEXT NOT NULL,
            section_kind TEXT NOT NULL,
            text TEXT NOT NULL,
            weight REAL NOT NULL
        );

        CREATE TABLE chunk_embeddings (
            chunk_id INTEGER PRIMARY KEY REFERENCES chunks(id) ON DELETE CASCADE,
            model TEXT NOT NULL,
            dimensions INTEGER NOT NULL,
            vector BLOB NOT NULL
        );

        CREATE VIRTUAL TABLE chunk_fts USING fts5(
            page_title,
            factors,
            section_title,
            text,
            chunk_id UNINDEXED
        );
        """
    )


def build_index(
    wiki_root: Path,
    db_path: Path,
    embed_model: str = DEFAULT_EMBED_MODEL,
    batch_size: int = 16,
    with_embeddings: bool = True,
) -> int:
    pages = load_manifest_answer_pages(wiki_root)
    chunks = [chunk for page in pages for chunk in chunks_for_page(page)]

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        create_schema(connection)
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
            [
                (
                    chunk.page_slug,
                    chunk.page_title,
                    chunk.page_type,
                    chunk.page_path,
                    chunk.retrieval_role,
                    chunk.answer_priority,
                    json.dumps(chunk.factors),
                    chunk.source_count,
                    chunk.section_title,
                    chunk.section_kind,
                    chunk.text,
                    chunk.weight,
                )
                for chunk in chunks
            ],
        )
        connection.executemany(
            """
            INSERT INTO chunk_fts(rowid, page_title, factors, section_title, text, chunk_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    chunk_id,
                    chunk.page_title,
                    " ".join(chunk.factors),
                    chunk.section_title,
                    chunk.text,
                    str(chunk_id),
                )
                for chunk_id, chunk in enumerate(chunks, start=1)
            ],
        )
        connection.executemany(
            "INSERT INTO meta(key, value) VALUES (?, ?)",
            [
                ("generated_at", str(time.time())),
                ("wiki_root", wiki_root.as_posix()),
                ("embed_model", embed_model if with_embeddings else ""),
                ("chunk_count", str(len(chunks))),
            ],
        )

        if with_embeddings:
            for offset in range(0, len(chunks), batch_size):
                batch = chunks[offset : offset + batch_size]
                vectors = ollama_embed([embedding_text(chunk) for chunk in batch], embed_model)
                connection.executemany(
                    """
                    INSERT INTO chunk_embeddings(chunk_id, model, dimensions, vector)
                    VALUES (?, ?, ?, ?)
                    """,
                    [
                        (
                            offset + index + 1,
                            embed_model,
                            len(vector),
                            pack_vector(vector),
                        )
                        for index, vector in enumerate(vectors)
                    ],
                )
                connection.commit()
                print(f"embedded {min(offset + batch_size, len(chunks))}/{len(chunks)} chunks", file=sys.stderr)

    return len(chunks)


def embedding_text(chunk: Chunk) -> str:
    factors = ", ".join(chunk.factors)
    return (
        f"{chunk.page_title}\n"
        f"Page type: {chunk.page_type}\n"
        f"Factors: {factors}\n"
        f"Section: {chunk.section_title}\n"
        f"{chunk.text}"
    )


def ollama_embed(texts: list[str], model: str) -> list[list[float]]:
    payload = {"model": model, "input": texts}
    result = post_ollama_json("/api/embed", payload, timeout=300)
    embeddings = result.get("embeddings")
    if not isinstance(embeddings, list):
        raise RuntimeError(f"Ollama embed response missing embeddings: {result}")
    return embeddings


def ollama_chat_json(messages: list[dict], model: str = DEFAULT_CHAT_MODEL) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.0, "num_predict": 1200},
    }
    result = post_ollama_json("/api/chat", payload, timeout=300)
    message = result.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"Ollama chat response missing message content: {result}")
    return content


def post_ollama_json(path: str, payload: dict, timeout: int) -> dict:
    request = urllib.request.Request(
        f"http://localhost:11434{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama request failed for {path}: {exc}") from exc


def pack_vector(vector: Iterable[float]) -> bytes:
    values = list(vector)
    return struct.pack(f"<{len(values)}f", *values)


def unpack_vector(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype="<f4")


def plan_query(query: str, model: str = DEFAULT_CHAT_MODEL) -> QueryPlan:
    messages = [
        {
            "role": "system",
            "content": (
                "You expand user queries for a local astrological-combination retrieval tool. "
                "Return JSON only. Do not invent final combinations. Keep factor_hypotheses tentative."
                " If the user names a specific body system, activity, or object, expand to concrete parts, functions, and adjacent synonyms; do not broaden to parent categories unless the query itself is broad."
            ),
        },
        {
            "role": "user",
            "content": (
                "Query: "
                + query
                + "\nReturn this JSON shape: "
                '{"interpreted_query": "...", "concepts": ["..."], "synonyms": ["..."], '
                '"factor_hypotheses": ["..."], "avoid": ["..."]}'
            ),
        },
    ]
    try:
        parsed = parse_json_object(ollama_chat_json(messages, model=model))
    except Exception:
        return fallback_query_plan(query)

    return QueryPlan(
        query=query,
        interpreted_query=str(parsed.get("interpreted_query", query)),
        concepts=string_tuple(parsed.get("concepts")),
        synonyms=string_tuple(parsed.get("synonyms")),
        factor_hypotheses=string_tuple(parsed.get("factor_hypotheses")),
        avoid=string_tuple(parsed.get("avoid")),
    )


def fallback_query_plan(query: str) -> QueryPlan:
    tokens = tuple(dict.fromkeys(tokenize_for_fts(query)))
    return QueryPlan(
        query=query,
        interpreted_query=query,
        concepts=tokens,
        synonyms=(),
        factor_hypotheses=(),
        avoid=(),
    )


def string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def parse_json_object(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"no JSON object found: {text}")
    return json.loads(stripped[start : end + 1])


def tokenize_for_fts(text: str) -> list[str]:
    return [token.casefold() for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)]


def fts_query(plan: QueryPlan) -> str:
    terms = tokenize_for_fts(plan.retrieval_text)
    unique = list(dict.fromkeys(terms))[:24]
    return " OR ".join(f"{term}*" for term in unique)


def rank_pages(
    db_path: Path,
    plan: QueryPlan,
    limit: int = 12,
    candidate_chunks: int = 80,
    embed_model: str | None = None,
) -> list[RankedPage]:
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        fts_scores = load_fts_scores(connection, plan, candidate_chunks)
        semantic_scores = load_semantic_scores(connection, plan, candidate_chunks, embed_model)
        chunk_ids = set(fts_scores) | set(semantic_scores)
        if not chunk_ids:
            return []

        placeholders = ",".join("?" for _ in chunk_ids)
        rows = connection.execute(
            f"SELECT * FROM chunks WHERE id IN ({placeholders})",
            tuple(chunk_ids),
        ).fetchall()

    by_page: dict[str, dict] = {}
    for row in rows:
        chunk_id = int(row["id"])
        semantic = semantic_scores.get(chunk_id, 0.0)
        lexical = fts_scores.get(chunk_id, 0.0)
        base = 0.55 * semantic + 0.35 * lexical
        base += 0.05 * float(row["weight"])
        base += 0.0005 * float(row["answer_priority"])
        if row["page_type"] == "activation":
            base += 0.08
        elif row["page_type"] == "axis":
            base += 0.04

        page = by_page.setdefault(
            str(row["page_path"]),
            {
                "title": str(row["page_title"]),
                "path": str(row["page_path"]),
                "page_type": str(row["page_type"]),
                "factors": tuple(json.loads(row["factors_json"])),
                "score": 0.0,
                "reasons": [],
                "snippets": [],
            },
        )
        page["score"] = max(float(page["score"]), base)
        if semantic:
            page["reasons"].append(f"semantic {semantic:.2f} in {row['section_title']}")
        if lexical:
            page["reasons"].append(f"keyword {lexical:.2f} in {row['section_title']}")
        page["snippets"].append(make_snippet(str(row["text"])))

    ranked = sorted(by_page.values(), key=lambda item: item["score"], reverse=True)
    return [
        RankedPage(
            title=item["title"],
            path=item["path"],
            page_type=item["page_type"],
            factors=item["factors"],
            score=item["score"],
            reasons=tuple(dict.fromkeys(item["reasons"]))[:4],
            snippets=tuple(dict.fromkeys(item["snippets"]))[:3],
        )
        for item in ranked[:limit]
    ]


def load_fts_scores(connection: sqlite3.Connection, plan: QueryPlan, limit: int) -> dict[int, float]:
    query = fts_query(plan)
    if not query:
        return {}
    try:
        rows = connection.execute(
            """
            SELECT CAST(chunk_id AS INTEGER) AS chunk_id, bm25(chunk_fts, 5.0, 2.0, 2.0, 1.0) AS score
            FROM chunk_fts
            WHERE chunk_fts MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        return {}
    if not rows:
        return {}
    scores = [abs(float(row["score"])) for row in rows]
    maximum = max(scores) or 1.0
    return {int(row["chunk_id"]): abs(float(row["score"])) / maximum for row in rows}


def load_semantic_scores(
    connection: sqlite3.Connection,
    plan: QueryPlan,
    limit: int,
    embed_model: str | None,
) -> dict[int, float]:
    model = embed_model or meta_value(connection, "embed_model")
    if not model:
        return {}
    query_vector = np.array(ollama_embed([plan.retrieval_text], model)[0], dtype=np.float32)
    query_norm = np.linalg.norm(query_vector)
    if query_norm == 0:
        return {}
    query_vector = query_vector / query_norm

    rows = connection.execute(
        "SELECT chunk_id, vector FROM chunk_embeddings WHERE model = ?",
        (model,),
    ).fetchall()
    scored: list[tuple[int, float]] = []
    for row in rows:
        vector = unpack_vector(row["vector"])
        norm = np.linalg.norm(vector)
        if norm == 0:
            continue
        similarity = float(np.dot(query_vector, vector / norm))
        scored.append((int(row["chunk_id"]), similarity))

    scored.sort(key=lambda item: item[1], reverse=True)
    return {chunk_id: max(0.0, score) for chunk_id, score in scored[:limit]}


def meta_value(connection: sqlite3.Connection, key: str) -> str:
    row = connection.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return str(row["value"]) if row else ""


def make_snippet(text: str, length: int = 320) -> str:
    text = normalize_text(text)
    if len(text) <= length:
        return text
    cut = text[:length].rsplit(" ", 1)[0]
    return cut + "..."


def rerank_with_llm(
    query: str,
    plan: QueryPlan,
    candidates: list[RankedPage],
    model: str = DEFAULT_CHAT_MODEL,
) -> str:
    payload = [
        {
            "id": index + 1,
            "title": candidate.title,
            "page_type": candidate.page_type,
            "factors": list(candidate.factors),
            "path": candidate.path,
            "retrieval_score": round(candidate.score, 4),
            "snippets": list(candidate.snippets),
        }
        for index, candidate in enumerate(candidates)
    ]
    messages = [
        {
            "role": "system",
            "content": (
                "You rerank local Stellar Influences wiki retrieval candidates. "
                "Pick only from the provided candidates. Preserve activation orientation. "
                "Do not repeat the same path. Prefer specific activations and axes over broad factor pages when evidence is comparable. "
                "Prefer evidence that names the query's concrete domain over broad adjacent evidence. "
                "Explain relevance using candidate snippets; mark weak evidence honestly. Return JSON only."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Original query: {query}\n"
                f"Expanded plan: {json.dumps(plan.__dict__, ensure_ascii=False)}\n"
                f"Candidates: {json.dumps(payload, ensure_ascii=False)}\n"
                "Return this JSON shape with the best 8 or fewer unique candidates: "
                '{"results":[{"candidate_id":1,"why":"...","evidence":"...","confidence":"high|medium|low"}]}'
            ),
        },
    ]
    content = ollama_chat_json(messages, model=model).strip()
    try:
        parsed = parse_json_object(content)
    except Exception:
        return content
    results = parsed.get("results")
    if not isinstance(results, list):
        return content
    return render_llm_results(results, candidates)


def render_llm_results(results: list, candidates: list[RankedPage]) -> str:
    by_id = {index + 1: candidate for index, candidate in enumerate(candidates)}
    seen_paths: set[str] = set()
    lines: list[str] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        try:
            candidate_id = int(item.get("candidate_id"))
        except (TypeError, ValueError):
            continue
        candidate = by_id.get(candidate_id)
        if candidate is None or candidate.path in seen_paths:
            continue
        seen_paths.add(candidate.path)
        why = str(item.get("why", "")).strip()
        evidence = str(item.get("evidence", "")).strip()
        confidence = str(item.get("confidence", "")).strip()
        lines.append(f"- **{candidate.title}** `{candidate.path}`")
        if why:
            lines.append(f"  - Why: {why}")
        if evidence:
            lines.append(f"  - Evidence: {evidence}")
        if confidence:
            lines.append(f"  - Confidence: {confidence}")
    if not lines:
        return ""
    return "\n".join(lines)


def print_ranked_pages(candidates: list[RankedPage]) -> None:
    for index, candidate in enumerate(candidates, start=1):
        factors = ", ".join(candidate.factors)
        print(f"{index}. {candidate.title} [{candidate.page_type}]")
        print(f"   path: {candidate.path}")
        print(f"   score: {candidate.score:.3f}")
        if factors:
            print(f"   factors: {factors}")
        if candidate.reasons:
            print(f"   signals: {'; '.join(candidate.reasons)}")
        for snippet in candidate.snippets[:2]:
            print(f"   evidence: {snippet}")
        print()


def build_index_main() -> None:
    parser = argparse.ArgumentParser(description="Build a local semantic query index for the Stellar Influences wiki.")
    parser.add_argument("--wiki", type=Path, default=Path("wiki"))
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--no-embeddings", action="store_true")
    args = parser.parse_args()

    count = build_index(
        wiki_root=args.wiki,
        db_path=args.db,
        embed_model=args.embed_model,
        batch_size=args.batch_size,
        with_embeddings=not args.no_embeddings,
    )
    print(f"indexed {count} chunks into {args.db}")


def query_main() -> None:
    parser = argparse.ArgumentParser(description="Query the local Stellar Influences semantic index.")
    parser.add_argument("query")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--embed-model", default=None)
    parser.add_argument("--chat-model", default=DEFAULT_CHAT_MODEL)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--candidate-chunks", type=int, default=80)
    parser.add_argument("--no-llm", action="store_true")
    args = parser.parse_args()

    if not args.db.exists():
        raise SystemExit(f"index not found: {args.db}. Run tools/build_local_query_index.py first.")

    plan = plan_query(args.query, model=args.chat_model)
    candidates = rank_pages(
        db_path=args.db,
        plan=plan,
        limit=args.limit,
        candidate_chunks=args.candidate_chunks,
        embed_model=args.embed_model,
    )
    print(f"Query plan: {plan.interpreted_query}")
    if plan.concepts:
        print(f"Concepts: {', '.join(plan.concepts)}")
    if plan.synonyms:
        print(f"Synonyms: {', '.join(plan.synonyms)}")
    if plan.factor_hypotheses:
        print(f"Factor hypotheses: {', '.join(plan.factor_hypotheses)}")
    print()

    if args.no_llm:
        print_ranked_pages(candidates)
    else:
        print(rerank_with_llm(args.query, plan, candidates, model=args.chat_model))


if __name__ == "__main__":
    query_main()
