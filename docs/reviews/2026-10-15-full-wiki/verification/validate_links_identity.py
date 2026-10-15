# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2", "pyyaml", "markdown-it-py"]
# ///
# ─── How to run ───
# PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe <this file>
# The repository requires this interpreter; do not substitute a uv environment.
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Final
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from pydantic import BaseModel, ConfigDict

from validate_review import Baseline, Check, OUT, ROOT, REVIEW, load_page, write_report

MARKDOWN: Final = MarkdownIt("commonmark").enable("table")


class Surface(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[str] = []
        self.links: list[str] = []
        self.headings: list[str] = []
        self.heading: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.anchors.extend(value for key, value in attrs if key in {"id", "name"} and value)
        self.links.extend(value for key, value in attrs if key in {"href", "src"} and value)
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = ""

    def handle_data(self, data: str) -> None:
        if self.heading is not None:
            self.heading += data

    def handle_endtag(self, tag: str) -> None:
        if re.fullmatch(r"h[1-6]", tag) and self.heading is not None:
            self.headings.append(self.heading)
            self.heading = None


class Identity(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str = ""
    slug: str = ""
    page_type: str = "navigation"
    factors: tuple[str, ...] = ()
    normalized_axis: str = ""
    normalized_formula: str = ""
    factor_a: str = ""
    factor_b: str = ""
    axis: str = ""
    activated_by: str = ""
    triad_set: tuple[str, ...] = ()
    orientations: tuple[str, ...] = ()
    related_activations: tuple[str, ...] = ()
    related_triad_hubs: tuple[str, ...] = ()
    source_pages: tuple[str, ...] = ()
    structural_only: bool = False


class ManifestRow(Identity):
    path: str
    retrieval_role: str
    answer_surface: bool


class Manifest(BaseModel):
    model_config = ConfigDict(frozen=True)
    pages: tuple[ManifestRow, ...]
    summary: dict[str, int]


def heading_anchors(headings: list[str]) -> set[str]:
    used: set[str] = set()
    for heading in headings:
        slug = "".join(c for c in heading.lower() if c in "_- " or unicodedata.category(c)[0] not in {"P", "S", "C"}).replace(" ", "-")
        candidate, counter = slug, 0
        while candidate in used:
            counter += 1
            candidate = f"{slug}-{counter}"
        used.add(candidate)
    return used


def render(body: str) -> Surface:
    surface = Surface()
    surface.feed(MARKDOWN.render(body))
    surface.close()
    return surface


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from tools.wiki_identity import normalize_activation, normalize_axis, normalize_factor, normalize_triad

    assert heading_anchors(["One / Two", "One / Two", "One--Two-1"]) == {"one--two", "one--two-1", "one--two-1-1"}
    fixture = render("## Linked *heading*\n\n[local](target.md#part)\n\n`[code](missing.md)`\n\n<a id='explicit'></a>")
    assert fixture.links == ["target.md#part"] and fixture.headings == ["Linked heading"] and fixture.anchors == ["explicit"]
    baseline = Baseline.model_validate_json((REVIEW / "baseline.json").read_bytes())
    paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "wiki").rglob("*.md"))
    print(f"Loading and rendering {len(paths)} Markdown files", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        pages = {p.path: p for p in pool.map(load_page, ((ROOT, p) for p in paths))}
    surfaces = {p: render(page.body) for p, page in pages.items()}
    anchors = {p: set(s.anchors) | heading_anchors(s.headings) for p, s in surfaces.items()}
    link_errors: list[str] = []
    fragment_errors: list[str] = []
    duplicate_ids = [f"{p}#{anchor}" for p, s in surfaces.items() for anchor, count in Counter(s.anchors).items() if count > 1]
    link_count = 0
    for p, surface in surfaces.items():
        for href in surface.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            link_count += 1
            target = ((ROOT / url.path.lstrip("/")) if url.path.startswith("/") else (ROOT / p).parent / unquote(url.path)).resolve() if url.path else (ROOT / p).resolve()
            if not target.exists():
                link_errors.append(f"{p}: {href}")
                continue
            if url.fragment and target.suffix.lower() == ".md":
                try:
                    relative = target.relative_to(ROOT).as_posix()
                except ValueError:
                    fragment_errors.append(f"{p}: outside-repository Markdown target: {href}")
                    continue
                if relative not in anchors:
                    linked = render(load_page((ROOT, relative)).body)
                    anchors[relative] = set(linked.anchors) | heading_anchors(linked.headings)
                if unquote(url.fragment) not in anchors[relative]:
                    fragment_errors.append(f"{p}: {href}")
    checks = {"internal_file_links": Check(checked=link_count, failures=tuple(link_errors)), "internal_fragments": Check(checked=link_count, failures=tuple(fragment_errors)), "duplicate_explicit_ids": Check(checked=len(pages), failures=tuple(duplicate_ids))}
    live = {p for p in pages if "/_templates/" not in p}
    manifest = Manifest.model_validate_json((ROOT / "wiki/query-manifest.json").read_bytes())
    indexed = {row.path for row in manifest.pages}
    manifest_errors = sorted((live - {"wiki/query-guide.md"}) ^ indexed)
    manifest_errors.extend(f"duplicate manifest path: {p}" for p, count in Counter(row.path for row in manifest.pages).items() if count > 1)
    if Counter(row.retrieval_role for row in manifest.pages) != manifest.summary:
        manifest_errors.append("manifest summary differs from row retrieval_role counts")
    if baseline.manifest_excluded_live_pages != ("wiki/query-guide.md",):
        manifest_errors.append("baseline intentional query-guide exclusion changed")
    nodes = {p: Identity.model_validate(page.metadata) for p, page in pages.items() if "/_templates/" not in p}
    for row in manifest.pages:
        if row.path in nodes:
            node = nodes[row.path]
            metadata, body = pages[row.path].metadata, pages[row.path].body
            expected = {
                "title": metadata.get("title", Path(row.path).stem),
                "slug": metadata.get("slug", Path(row.path).stem),
                "page_type": metadata.get("page_type", "special"),
                "factors": node.factors, "source_pages": node.source_pages,
                "structural_only": node.structural_only or node.page_type == "triad_hub" or "This page is structural only. It does not merge the meanings of its orientations." in body,
            }
            for key, value in expected.items():
                if getattr(row, key) != value:
                    manifest_errors.append(f"{row.path}: stale manifest {key}")
    checks["manifest_coverage_metadata"] = Check(checked=len(manifest.pages), failures=tuple(manifest_errors))
    factors = {node.title: p for p, node in nodes.items() if node.page_type == "factor"}
    axes = {node.normalized_axis: p for p, node in nodes.items() if node.page_type == "axis"}
    activations = {node.normalized_formula: p for p, node in nodes.items() if node.page_type == "activation"}
    triads = {node.triad_set: p for p, node in nodes.items() if node.page_type == "triad_hub"}
    identity_errors: list[str] = []
    relation_errors: list[str] = []
    coverage_errors: list[str] = []
    for name, p in factors.items():
        node, canonical = nodes[p], normalize_factor(name)
        if (node.title, node.slug, node.factors) != (canonical.display, canonical.slug, (canonical.display,)):
            identity_errors.append(f"{p}: factor identity")
    for name, p in axes.items():
        node = nodes[p]
        if len(node.factors) != 2:
            identity_errors.append(f"{p}: axis factor arity")
            continue
        canonical = normalize_axis(*node.factors)
        if (node.title, name, node.slug, node.factor_a, node.factor_b) != (canonical.display, canonical.display, canonical.slug, *canonical.factors):
            identity_errors.append(f"{p}: axis identity")
        actual = {n.normalized_formula for n in nodes.values() if n.page_type == "activation" and n.axis == name}
        if set(node.related_activations) != actual:
            relation_errors.append(f"{p}: related_activations differs from actual axis activation set")
        relation_errors.extend(f"{p}: missing factor {factor}" for factor in node.factors if factor not in factors)
    for formula, p in activations.items():
        node = nodes[p]
        if len(node.factors) != 3:
            identity_errors.append(f"{p}: activation factor arity")
            continue
        canonical = normalize_activation(*node.factors)
        if (node.title, formula, node.slug, node.axis, node.activated_by, node.triad_set) != (canonical.display, canonical.display, canonical.slug, canonical.axis.display, canonical.activated_by, canonical.triad_set):
            identity_errors.append(f"{p}: oriented activation identity")
        relation_errors.extend(f"{p}: missing factor {factor}" for factor in node.factors if factor not in factors)
        if node.axis not in axes:
            relation_errors.append(f"{p}: missing base axis {node.axis}")
        if len(node.triad_set) == 3 and node.triad_set not in triads:
            relation_errors.append(f"{p}: missing triad hub")
    for factorset, p in triads.items():
        node = nodes[p]
        canonical = normalize_triad(list(factorset))
        if (node.title, node.slug, node.factors, node.orientations) != (canonical.display, canonical.slug, canonical.factors, canonical.orientations):
            identity_errors.append(f"{p}: triad identity/orientations")
        related = [nodes[activations[f]] for f in canonical.orientations if f in activations]
        if len(related) != 3:
            relation_errors.append(f"{p}: existing orientation pages={len(related)}")
        union = {source for n in related for source in n.source_pages}
        if set(node.source_pages) != union:
            coverage_errors.append(f"{p}: source_pages differs from linked orientation union: missing={sorted(union - set(node.source_pages))}, extra={sorted(set(node.source_pages) - union)}")
        section = re.search(r"^## Source Coverage\s*\n(.*?)(?=^## |\Z)", pages[p].body, re.M | re.S)
        coverage = section.group(1) if section else ""
        if any(f not in coverage for f in canonical.orientations):
            coverage_errors.append(f"{p}: coverage omits an oriented formula")
        if re.search(r":\s*(?:Michael|Udo)(?:,|\s+page\b)", coverage):
            coverage_errors.append(f"{p}: ambiguous given-name source label")
    checks["canonical_identities"] = Check(checked=len(factors) + len(axes) + len(activations) + len(triads), failures=tuple(identity_errors))
    checks["cross_page_relationships"] = Check(checked=len(axes) + len(activations) + len(triads), failures=tuple(relation_errors))
    checks["triad_source_coverage"] = Check(checked=len(triads), failures=tuple(coverage_errors))
    write_report("links-identity-validation.json", {"generated_at": datetime.now(UTC).isoformat(), "interpreter": sys.executable, "scope": "Rendered CommonMark links; GFM-style heading anchors with duplicate suffixes; explicit HTML IDs; formula identities and actual triad source unions. No substantive review coverage is inferred.", "counts": {"markdown_files": len(pages), "live": len(live), "links": link_count, "factors": len(factors), "axes": len(axes), "activations": len(activations), "triads": len(triads)}, "checks": {name: {"checked": check.checked, "passed": not check.failures, "failures": list(check.failures)} for name, check in checks.items()}})
    print(json.dumps({name: len(check.failures) for name, check in checks.items()}, sort_keys=True))
    return int(any(check.failures for check in checks.values()))


if __name__ == "__main__":
    raise SystemExit(main())
