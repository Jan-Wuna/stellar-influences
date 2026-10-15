from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_pages import WikiPage, iter_wiki_pages
from tools.wiki_links import relative_link_target


PLACEHOLDER_DERIVED_TEXT = "- None yet beyond source structuring."
STRUCTURAL_ONLY_TEXT = "This page is structural only. It does not merge the meanings of its orientations."

ROLE_PRIORITY = {
    "canonical_answer": 100,
    "synthesis_note": 80,
    "research_note": 50,
    "source_catalog": 40,
    "source_companion": 30,
    "structural_only": 20,
    "maintenance": 10,
}


def _section_body(body: str, heading: str) -> str:
    normalized = body.replace("\r\n", "\n")
    marker = f"## {heading}\n"
    if marker not in normalized:
        return ""
    section = normalized.split(marker, 1)[1]
    next_sections = re.split(r"\n## ", section, maxsplit=1)
    return next_sections[0].strip()


def _has_real_derived_synthesis(body: str) -> bool:
    section = _section_body(body, "Derived Synthesis")
    return bool(section and section != PLACEHOLDER_DERIVED_TEXT)


def _retrieval_role(page: WikiPage) -> str:
    page_type = page.meta.get("page_type")
    title_slug = f"{page.meta.get('title', '')} {page.meta.get('slug', '')}".casefold()

    if page.meta.get("structural_only") is True:
        return "structural_only"

    if page_type in {"activation", "axis", "factor"}:
        return "canonical_answer"

    if page_type == "triad_hub" or STRUCTURAL_ONLY_TEXT in page.body:
        return "structural_only"

    if page_type == "derived":
        if "source companion" in title_slug or "source-companion" in title_slug:
            return "source_companion"
        if "## Source Concepts" in page.body or title_slug.endswith("concepts"):
            return "source_companion"
        if any(
            token in title_slug
            for token in ("-vs-", " coverage", "review", "ingest-analysis", "corpus", "unresolved", "translation-qa")
        ):
            return "research_note"
        return "synthesis_note"

    if page_type == "source":
        return "source_catalog"

    return "maintenance"


def _answer_surface(role: str) -> bool:
    return role in {"canonical_answer", "synthesis_note"}


def _structural_only(role: str) -> bool:
    return role == "structural_only"


def _tags(page: WikiPage, role: str) -> list[str]:
    tags: list[str] = [role]
    page_type = page.meta.get("page_type")
    if page_type:
        tags.append(str(page_type))
    factors = page.meta.get("factors", []) or []
    for factor in factors:
        tags.append(str(factor))
    for key in ("normalized_formula", "normalized_axis", "axis", "activated_by"):
        value = page.meta.get(key)
        if value:
            tags.append(str(value))
    return sorted(set(tags), key=str.casefold)


def _page_record(page: WikiPage) -> dict:
    source_pages = list(page.meta.get("source_pages", []) or [])
    source_count = len(source_pages)
    role = _retrieval_role(page)
    has_real_derived_synthesis = _has_real_derived_synthesis(page.body)
    score = ROLE_PRIORITY[role] + min(source_count, 9) + (10 if has_real_derived_synthesis else 0)

    return {
        "title": page.meta.get("title", page.path.stem),
        "slug": page.meta.get("slug", page.path.stem),
        "path": page.path.as_posix(),
        "page_type": page.meta.get("page_type", "special"),
        "framework_scope": page.meta.get("framework_scope", ""),
        "retrieval_role": role,
        "answer_surface": _answer_surface(role),
        "structural_only": _structural_only(role),
        "source_pages": source_pages,
        "source_count": source_count,
        "single_source_only": source_count <= 1,
        "has_real_derived_synthesis": has_real_derived_synthesis,
        "answer_priority": score,
        "factors": list(page.meta.get("factors", []) or []),
        "tags": _tags(page, role),
    }


def build_query_manifest(root: Path) -> dict:
    pages = [
        _page_record(page)
        for page in iter_wiki_pages(root)
        if page.path.name != "query-guide.md"
    ]
    pages.sort(key=lambda item: (-item["answer_priority"], item["title"].casefold(), item["path"]))

    counts = Counter(page["retrieval_role"] for page in pages)
    return {
        "generated_at": date.today().isoformat(),
        "root": root.as_posix(),
        "summary": dict(sorted(counts.items())),
        "retrieval_order": [
            {"role": "canonical_answer", "use_for": "Direct interpretation of explicit formulas, axes, and factors."},
            {"role": "synthesis_note", "use_for": "Compact synthesis notes that clarify how to read combinations."},
            {"role": "structural_only", "use_for": "Orientation safety, sibling lookups, and documented structural factor identity only."},
            {"role": "source_companion", "use_for": "Supplemental source artifacts, not default answer surfaces."},
            {"role": "research_note", "use_for": "Coverage audits and comparison notes, not default answers."},
            {"role": "source_catalog", "use_for": "Bibliographic scope and ingest coverage."},
        ],
        "pages": pages,
    }


def build_query_guide(manifest: dict) -> str:
    guide_path = Path(manifest["root"]) / "query-guide.md"
    grouped: dict[str, list[dict]] = {}
    for page in manifest["pages"]:
        grouped.setdefault(page["retrieval_role"], []).append(page)

    def list_titles(role: str, limit: int = 12) -> str:
        items = grouped.get(role, [])
        if not items:
            return "- None"
        shown = items[:limit]
        lines = [
            f"- [{item['title']}]({relative_link_target(guide_path, Path(item['path']))})"
            for item in shown
        ]
        if len(items) > limit:
            lines.append(f"- ... and {len(items) - limit} more")
        return "\n".join(lines)

    def count(role: str) -> int:
        return len(grouped.get(role, []))

    return f"""# Query Guide

Use this guide and [`query-manifest.json`](query-manifest.json) before opening large numbers of pages.

## Find a Page

- **Exact formula:** open [Activations](index.md#activations). Preserve the factor after `=`; the other orientations of the same three factors remain separate pages.
- **Shared pair:** open [Axes](index.md#axes). A pair has one identity regardless of factor order.
- **Recurring factor:** open [Factors](index.md#factors) for standalone evidence, documented scope limits, and related combinations.
- **Orientation siblings:** open [Triad Hubs](index.md#triad-hubs) for structural lookup.
- **Source scope:** open [Sources](index.md#sources) for admitted material, provenance, and coverage limits.

## Retrieval Order

1. Use activation pages first for explicit formulas.
2. Use axis pages second for shared pair meaning.
3. Use factor pages third for recurring factors that repeat across the question.
4. Use triad hubs only to confirm orientation siblings.
5. Use synthesis notes when a compact explanation clarifies how multiple pages fit together.
6. Use source companions, research notes, and source catalogs only when canonical pages leave a real gap.

## Answer Style

- Synthesize overlapping motifs into one interpretation.
- Elevate repeated factors and repeated themes instead of listing page-by-page meanings.
- Mention source differences only when they materially change the answer or the user asks.
- Avoid using structural-only pages as doctrine.

## Evidence and Limits

On a factor, axis, or activation page, read **Derived Synthesis** for the integrated explanation, then follow its source-entry links into **Source Entries**. Those entries retain source-native categories and exact passage references. **Comparative Schema** groups the claims without replacing that evidence.

Read the page's contradiction notes, qualifications, and open questions where present. Missing coverage does not establish an absence of meaning, and repeated wording does not establish independent corroboration. Use source companions, research notes, catalogs, and finally the raw source only to resolve a specific gap. Historical health or gender claims remain attributed statements, not diagnoses or universal facts.

## Using the Manifest

Filter `pages` by `page_type`, `factors`, or an exact formula in `tags`, then open the record's `path`. `retrieval_role` identifies the page's purpose; `answer_surface` marks default interpretation surfaces, while `structural_only` marks structural lookup pages. `has_real_derived_synthesis` records populated synthesis text, not a quality verdict.

`answer_priority` orders retrieval, not evidential strength. `source_count` counts source-page links; check the entries themselves for independent support. The counts below describe the current generated inventory, not complete coverage of every possible combination.

## Canonical Answer Pages

- Count: `{count("canonical_answer")}`
- These are the default answer surfaces for delineation.

## Synthesis Notes

- Count: `{count("synthesis_note")}`
{list_titles("synthesis_note")}

## Structural Hubs

- Count: `{count("structural_only")}`
- Use triad hubs only to confirm orientation siblings.
- Explicitly marked structural factor pages establish identity and scope without supplying standalone factor doctrine.

## Source Companions

- Count: `{count("source_companion")}`
- These are preserved source artifacts and should be down-ranked during answer generation.

## Research Notes

- Count: `{count("research_note")}`
{list_titles("research_note")}

## Source Catalogs

- Count: `{count("source_catalog")}`
- Use these for scope and provenance, not for first-pass interpretation.
"""


def write_query_artifacts(root: Path) -> None:
    manifest = build_query_manifest(root)
    (root / "query-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "query-guide.md").write_text(build_query_guide(manifest), encoding="utf-8")


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("wiki")
    write_query_artifacts(root)


if __name__ == "__main__":
    main()
