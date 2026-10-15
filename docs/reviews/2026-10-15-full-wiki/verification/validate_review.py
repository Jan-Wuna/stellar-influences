# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2", "pyyaml"]
# ///
# ─── How to run ───
# PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe <this file>
# The repository requires this interpreter; do not substitute a uv environment.
from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError

REVIEW: Final = Path(__file__).resolve().parents[1]
ROOT: Final = REVIEW.parents[2]
OUT: Final = Path(__file__).resolve().parent
CATEGORIES: Final = ("core meaning", "psychology", "body/health", "social/relationship", "events/manifestations", "conflicts/notes")
LOADER: Final = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


class Record(BaseModel):
    model_config = ConfigDict(frozen=True)
    path: str
    page_type: str
    sha256: str


class Baseline(BaseModel):
    model_config = ConfigDict(frozen=True)
    pages: tuple[Record, ...]
    templates: tuple[Record, ...]
    protected_files: dict[str, str]
    manifest_excluded_live_pages: tuple[str, ...]


class Ledger(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="allow")
    __pydantic_extra__: dict[str, JsonValue] = Field(init=False)
    path: str
    reviewer: str = Field(min_length=1)
    full_read: Literal[True]
    status: Literal["reviewed"]
    outcome: Literal["changed", "unchanged"]
    problems: tuple[str, ...]
    changes: tuple[str, ...]
    verification: tuple[str, ...] = Field(min_length=1)
    unresolved: tuple[str, ...]
    evidence: tuple[str | dict[str, JsonValue], ...] = Field(min_length=1)


class Page(BaseModel):
    model_config = ConfigDict(frozen=True)
    path: str
    metadata: dict[str, JsonValue]
    body: str
    sha256: str


class Check(BaseModel):
    model_config = ConfigDict(frozen=True)
    checked: int
    failures: tuple[str, ...]


class Allowance(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    path: str
    before_sha256: str
    after_sha256: str
    ledger: str
    reason: str = Field(min_length=1)
    evidence: tuple[str, ...] = Field(min_length=1)
    verified_by: str = Field(min_length=1)


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_page(location: tuple[Path, str]) -> Page:
    base, relative = location
    raw = (base / relative).read_bytes()
    text = raw.decode("utf-8").replace("\r\n", "\n")
    metadata, body = {}, text
    if text.startswith("---\n"):
        _, header, body = text.split("---", 2)
        metadata = yaml.load(header, Loader=LOADER) or {}
    return Page.model_validate({"path": relative, "metadata": json.loads(json.dumps(metadata, default=str)), "body": body, "sha256": hashlib.sha256(raw).hexdigest()})


def source_section(body: str) -> str:
    found = re.search(r"^## Source Entries\s*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    return re.sub(r'(?:\n<a id="[^"]+"></a>\s*)+\Z', "", found.group(1)).strip() if found else ""


def write_report(filename: str, report: JsonValue) -> None:
    (OUT / filename).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    baseline = Baseline.model_validate_json((REVIEW / "baseline.json").read_bytes())
    records = (*baseline.pages, *baseline.templates)
    expected = {row.path: row for row in records}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "wiki").rglob("*.md")}
    checks: dict[str, Check] = {}
    checks["inventory"] = Check(checked=len(actual), failures=tuple(sorted(actual ^ expected.keys())))
    checks["baseline_counts"] = Check(checked=len(records), failures=tuple(label for label, valid in (("live != 7491", len(baseline.pages) == 7491), ("templates != 6", len(baseline.templates) == 6), ("protected != 6036", len(baseline.protected_files) == 6036)) if not valid))
    assignments = [p for f in sorted((REVIEW / "assignments").glob("*.json")) for p in json.loads(f.read_text(encoding="utf-8"))]
    assigned = Counter(assignments)
    assignment_errors = [p for p, count in assigned.items() if count != 1]
    assignment_errors.extend(sorted(set(assignments) ^ {r.path for r in baseline.pages}))
    checks["assignment_partition"] = Check(checked=len(assignments), failures=tuple(assignment_errors))
    print("Loading current pages and baseline copies", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        current = {p.path: p for p in pool.map(load_page, ((ROOT, p) for p in sorted(actual)))}
        before = {p.path: p for p in pool.map(load_page, ((REVIEW / "before", p) for p in expected))}
    checks["baseline_copies"] = Check(checked=len(before), failures=tuple(p for p, page in before.items() if page.sha256 != expected[p].sha256))
    print("Validating ledger records and page outcomes", flush=True)
    ledger_rows: dict[str, list[tuple[str, Ledger]]] = {}
    ledger_errors: list[str] = []
    for shard in sorted((REVIEW / "ledgers").glob("*.jsonl")):
        for number, line in enumerate(shard.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    row = Ledger.model_validate_json(line)
                except ValidationError as error:
                    ledger_errors.append(f"{shard.name}:{number}: {error}")
                    continue
                ledger_rows.setdefault(row.path, []).append((shard.name, row))
    checks["ledger_schema"] = Check(checked=sum(map(len, ledger_rows.values())) + len(ledger_errors), failures=tuple(ledger_errors))
    coverage_errors = [f"{p}: records={len(ledger_rows.get(p, []))}" for p in expected if len(ledger_rows.get(p, [])) != 1]
    coverage_errors.extend(f"unexpected ledger path: {p}" for p in ledger_rows.keys() - expected.keys())
    checks["ledger_coverage"] = Check(checked=len(expected), failures=tuple(coverage_errors))
    outcome_errors: list[str] = []
    for p, entries in ledger_rows.items():
        if p in before and p in current and len(entries) == 1:
            row = entries[0][1]
            changed = before[p].sha256 != current[p].sha256
            if changed != (row.outcome == "changed"):
                outcome_errors.append(f"{p}: {row.outcome}, bytes_changed={changed}")
            if not changed and not (row.changes or row.verification):
                outcome_errors.append(f"{p}: unchanged reason absent")
    checks["ledger_outcomes"] = Check(checked=len(ledger_rows), failures=tuple(outcome_errors))
    meta_errors: list[str] = []
    anchor_errors: list[str] = []
    schema_errors: list[str] = []
    filler_errors: list[str] = []
    candidates: list[dict[str, JsonValue]] = []
    allowances_path = OUT / "source-repair-allowances.json"
    allowances = [Allowance.model_validate(row) for row in json.loads(allowances_path.read_text(encoding="utf-8"))] if allowances_path.exists() else []
    approved = {(a.path, a.before_sha256, a.after_sha256): a for a in allowances}
    repair_errors: list[str] = []
    canonical = [p for p, row in expected.items() if row.page_type in {"factor", "axis", "activation"} and "/_templates/" not in p]
    print("Checking metadata, schema, anchors, and live source sections", flush=True)
    for p in sorted(current.keys() & before.keys()):
        page, old = current[p], before[p]
        prior, revised = dict(old.metadata), dict(page.metadata)
        prior.pop("updated_at", None)
        revised.pop("updated_at", None)
        if p in {"wiki/factors/chiron.md", "wiki/activations/jupiter-mc-equals-chiron.md", "wiki/activations/neptune-node-equals-chiron.md", "wiki/activations/uranus-asc-equals-chiron.md"} and revised.get("structural_only") is True:
            prior["structural_only"] = True
        if p in {"wiki/activations/mercury-asc-equals-node.md", "wiki/activations/moon-asc-equals-mercury.md", "wiki/activations/moon-asc-equals-node.md", "wiki/activations/venus-neptune-equals-moon.md"}:
            # Exact complete-chapter omission proofs are recorded in metadata-repair-decisions.md.
            sources = prior.get("source_pages")
            sandbach = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
            if isinstance(sources, list) and revised.get("source_pages") == [s for s in sources if s != sandbach]:
                prior["source_pages"] = revised["source_pages"]
        if revised.get("page_type") == "triad_hub":
            prior.pop("source_pages", None)
            revised.pop("source_pages", None)
        if revised.get("page_type") == "axis":
            related = revised.get("related_activations")
            formulas = {f for linked in current.values() if linked.metadata.get("page_type") == "activation" and linked.metadata.get("axis") == revised.get("normalized_axis") if isinstance(f := linked.metadata.get("normalized_formula"), str)}
            if isinstance(related, list) and all(isinstance(f, str) for f in related) and set(related) == formulas and len(related) == len(formulas):
                prior["related_activations"] = related
            related_hubs = revised.get("related_triad_hubs")
            pair = {revised.get("factor_a"), revised.get("factor_b")}
            hubs = {title for linked in current.values() if linked.metadata.get("page_type") == "triad_hub" and pair <= set(linked.metadata.get("factors", [])) if isinstance(title := linked.metadata.get("title"), str)}
            if len(pair) == 2 and isinstance(related_hubs, list) and set(related_hubs) == hubs and len(related_hubs) == len(hubs):
                prior["related_triad_hubs"] = related_hubs
        if prior != revised:
            meta_errors.append(f"{p}: " + ", ".join(sorted(k for k in prior.keys() | revised.keys() if prior.get(k) != revised.get(k))))
        if p in canonical:
            if '<a id="derived-synthesis"></a>\n## Derived Synthesis' not in page.body:
                anchor_errors.append(p)
            schema = re.search(r"^## Comparative Schema\s*\n(.*?)(?=^## |\Z)", page.body, re.M | re.S)
            labels = re.sub(r"[*_`]+", "", schema.group(1)).lower() if schema else ""
            absent = [c for c in CATEGORIES if not re.search(r"^\s*(?:[-*+]\s+|#{1,6}\s+)?" + re.escape(c) + r"\s*:", labels, re.M)]
            if absent:
                schema_errors.append(f"{p}: {', '.join(absent)}")
            if re.search(r"source-native .*preserved side by side|implications remain embedded|interpersonal implications remain attached|source-specific wording remains|each source keeps its own phrasing|this page preserves the activation as|None recorded yet", labels, re.I):
                filler_errors.append(p)
        original, replacement = source_section(old.body), source_section(page.body)
        blocks = [part.strip() for part in re.split(r"\n\s*\n", original) if part.strip()]
        if "/_templates/" not in p and (original or replacement) and original != replacement:
            first, last = (hashlib.sha256(s.encode()).hexdigest() for s in (original, replacement))
            owners = ledger_rows.get(p, [])
            owner = owners[0][0] if len(owners) == 1 else ""
            allowed = approved.get((p, first, last))
            if allowed is None or allowed.ledger != owner:
                repair_errors.append(p)
            candidates.append({"path": p, "before_sha256": first, "after_sha256": last, "before_page_sha256": old.sha256, "after_page_sha256": page.sha256, "original_blocks_retained": all(block in replacement for block in blocks), "ledger": owner, "ledger_record": owners[0][1].model_dump(mode="json") if len(owners) == 1 else None, "source_proof_pointers": [f"docs/reviews/2026-10-15-full-wiki/evidence/{Path(owner).stem}.jsonl: path={p}"] if owner else [], "approved": allowed is not None and allowed.ledger == owner, "diff": "".join(difflib.unified_diff(original.splitlines(True), replacement.splitlines(True), fromfile="before Source Entries", tofile="current Source Entries"))})
    for name, failures, total in (("metadata_preservation", meta_errors, len(current)), ("immediate_synthesis_anchor", anchor_errors, len(canonical)), ("six_schema_categories", schema_errors, len(canonical)), ("storage_filler", filler_errors, len(canonical)), ("source_entry_preservation", repair_errors, len(canonical))):
        checks[name] = Check(checked=total, failures=tuple(failures))
    write_report("source-repair-candidates.json", {"generated_at": datetime.now(UTC).isoformat(), "candidates": candidates, "hash_contract": "SHA256 of UTF-8 Source Entries content after CRLF to LF normalization, removal of terminal standalone anchors preceding the next section, and outer strip; page hashes use exact file bytes.", "scope": "Live source section differences; candidates do not establish repair correctness. Ledger extras are retained. Parser evidence pointers are leads, not verification of glyph boundaries or wording."})
    print(f"Source repair candidates written: {len(candidates)}; hashing protected files", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        protected = list(pool.map(lambda p: digest(ROOT / p) if (ROOT / p).is_file() else "MISSING", baseline.protected_files))
    checks["protected_initial_files"] = Check(checked=len(protected), failures=tuple(p for (p, expected_hash), found in zip(baseline.protected_files.items(), protected, strict=True) if expected_hash != found))
    checks["historical_log"] = Check(checked=1, failures=() if current["wiki/log.md"].sha256 == before["wiki/log.md"].sha256 else ("wiki/log.md changed",))
    report = {"generated_at": datetime.now(UTC).isoformat(), "interpreter": sys.executable, "scope": "Mechanical validation only. Ledger assertions are not independent proof of full reading or doctrinal correctness.", "counts": {"live": len(baseline.pages), "templates": len(baseline.templates), "canonical": len(canonical), "ledger_records": sum(map(len, ledger_rows.values())), "source_repair_candidates": len(candidates)}, "checks": {name: {"checked": check.checked, "passed": not check.failures, "failures": list(check.failures)} for name, check in checks.items()}}
    write_report("review-validation.json", report)
    print(json.dumps({name: len(check.failures) for name, check in checks.items()}, sort_keys=True))
    return int(any(check.failures for check in checks.values()))


if __name__ == "__main__":
    raise SystemExit(main())
