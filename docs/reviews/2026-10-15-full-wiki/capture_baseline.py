# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
# How to run: C:/pyMADMAX2/miniconda3/envs/deep11/python.exe docs/reviews/2026-10-15-full-wiki/capture_baseline.py
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Final, TypedDict

import yaml

ROOT: Final = Path(__file__).resolve().parents[3]
REVIEW: Final = Path(__file__).resolve().parent


class PageRecord(TypedDict):
    path: str
    page_type: str
    role: str
    bytes: int
    lines: int
    sha256: str


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def main() -> None:
    if (REVIEW / "baseline.json").exists():
        raise FileExistsError(REVIEW / "baseline.json")
    manifest = json.loads((ROOT / "wiki/query-manifest.json").read_text(encoding="utf-8"))
    manifest_records = {row["path"]: row for row in manifest["pages"]}
    records: list[PageRecord] = []
    templates: list[PageRecord] = []
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        metadata = yaml.safe_load(text.split("---", 2)[1]) if text.startswith("---\n") else {}
        record: PageRecord = {
            "path": relative,
            "page_type": str((metadata or {}).get("page_type", "navigation")),
            "role": manifest_records.get(relative, {}).get("retrieval_role", "maintenance"),
            "bytes": path.stat().st_size,
            "lines": len(text.splitlines()),
            "sha256": digest(path),
        }
        (templates if "_templates" in path.parts else records).append(record)
        destination = REVIEW / "before" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

    protected: dict[str, str] = {}
    dirty = git("diff", "--name-only", "-z").decode().split("\0")
    staged = git("diff", "--cached", "--name-only", "-z").decode().split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    vault = [p.relative_to(ROOT).as_posix() for p in (ROOT / "Stellar Influences Vault").rglob("*") if p.is_file()]
    for relative in sorted(set(dirty + staged + untracked + vault)):
        path = ROOT / relative
        if relative and path.is_file() and REVIEW not in path.parents:
            protected[relative] = digest(path)

    live = {row["path"] for row in records}
    baseline = {
        "head": git("rev-parse", "HEAD").decode().strip(),
        "git_status": "\n".join(line for line in git("status", "--porcelain=v1", "--untracked-files=all").decode().splitlines() if "docs/reviews/2026-10-15-full-wiki/" not in line),
        "pages": records,
        "templates": templates,
        "protected_files": protected,
        "manifest_summary": manifest["summary"],
        "manifest_excluded_live_pages": sorted(live - manifest_records.keys()),
        "manifest_missing_on_disk": sorted(manifest_records.keys() - live),
    }
    (REVIEW / "baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (REVIEW / "initial-tracked.diff").write_bytes(git("diff", "--binary"))
    (REVIEW / "initial-staged.diff").write_bytes(git("diff", "--cached", "--binary"))
    assignments = REVIEW / "assignments"
    assignments.mkdir(exist_ok=True)
    (REVIEW / "ledgers").mkdir(exist_ok=True)
    (REVIEW / "verification").mkdir(exist_ok=True)
    families: dict[str, list[PageRecord]] = {}
    for row in records:
        directory = Path(row["path"]).parent.name
        families.setdefault(directory, []).append(row)
    limits = {"activations": (55, 150000), "axes": (10, 110000), "factors": (4, 70000), "triads": (70, 150000), "derived": (16, 75000), "sources": (15, 70000), "wiki": (1, 600000)}
    batches: list[dict[str, str | int]] = []
    for family, rows in families.items():
        count_limit, byte_limit = limits[family]
        batch: list[str] = []
        byte_count = 0
        index = 0
        for row in rows:
            if batch and (len(batch) >= count_limit or byte_count + row["bytes"] > byte_limit):
                index += 1
                name = f"{family}-{index:03}"
                (assignments / f"{name}.json").write_text(json.dumps(batch, indent=2) + "\n", encoding="utf-8")
                batches.append({"name": name, "family": family, "count": len(batch), "bytes": byte_count})
                batch = []
                byte_count = 0
            batch.append(row["path"])
            byte_count += row["bytes"]
        if batch:
            index += 1
            name = f"{family}-{index:03}"
            (assignments / f"{name}.json").write_text(json.dumps(batch, indent=2) + "\n", encoding="utf-8")
            batches.append({"name": name, "family": family, "count": len(batch), "bytes": byte_count})
    (REVIEW / "batches.json").write_text(json.dumps(batches, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"live": len(records), "templates": len(templates), "protected": len(protected), "batches": dict(Counter(str(row["family"]) for row in batches)), "manifest_exclusions": sorted(live - manifest_records.keys())}, indent=2))


if __name__ == "__main__":
    main()
