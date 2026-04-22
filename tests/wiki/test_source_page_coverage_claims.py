from pathlib import Path
import re

from tools.wiki_pages import iter_wiki_pages, load_page


COUNT_PATTERNS = {
    "axis": [
        re.compile(r"Canonical axis pages (?:updated or created|generated): `(\d+)`\.?"),
        re.compile(r"Axis pages generated: `(\d+)`\.?"),
    ],
    "activation": [
        re.compile(r"Canonical activation pages (?:updated or created|generated): `(\d+)`\.?"),
        re.compile(r"Activation pages generated: `(\d+)`\.?"),
    ],
    "triad_hub": [
        re.compile(r"Canonical triad hubs (?:updated or created|generated): `(\d+)`\.?"),
        re.compile(r"Triad hubs generated: `(\d+)`\.?"),
    ],
}


def _claimed_count(body: str, page_type: str) -> int | None:
    for pattern in COUNT_PATTERNS[page_type]:
        match = pattern.search(body)
        if match:
            return int(match.group(1))
    return None


def test_source_page_coverage_claims_match_live_source_attribution():
    pages = iter_wiki_pages(Path("wiki"))
    counts_by_source: dict[str, dict[str, int]] = {}
    for page in pages:
        for source_slug in page.meta.get("source_pages", []) or []:
            bucket = counts_by_source.setdefault(source_slug, {"axis": 0, "activation": 0, "triad_hub": 0})
            page_type = page.meta.get("page_type")
            if page_type in bucket:
                bucket[page_type] += 1

    for source_path in Path("wiki/sources").glob("*.md"):
        source_page = load_page(source_path)
        source_slug = source_page.meta["slug"]
        live_counts = counts_by_source.get(source_slug, {"axis": 0, "activation": 0, "triad_hub": 0})
        for page_type in ("axis", "activation", "triad_hub"):
            claimed = _claimed_count(source_page.body, page_type)
            if claimed is None:
                continue
            assert claimed == live_counts[page_type], (
                f"{source_slug} claims {claimed} {page_type} pages, "
                f"but live source attribution is {live_counts[page_type]}"
            )
