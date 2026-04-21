# Stellar Influences Wiki Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the Stellar Influences markdown wiki, helper tooling, and pilot ingest slice so the approved identity model is proven on the `Sun/Moon/Venus` cluster before broader ingestion.

**Architecture:** Build a markdown-first wiki with strict YAML frontmatter, page templates, and lightweight Python helper tooling. Keep structural normalization separate from doctrine by treating factor pages, axis pages, activation pages, and triad hubs as distinct page types, then prove the model on one Ebertin-backed pilot cluster.

**Tech Stack:** Markdown with YAML frontmatter, Python via `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`, `pytest`, `PyYAML`, Git

---

## Assumptions

- The approved spec in [2026-04-21-stellar-influences-llm-wiki-design.md](/W:/Stellar%20Influences/docs/superpowers/specs/2026-04-21-stellar-influences-llm-wiki-design.md) is the source of truth for implementation.
- Raw files under `Stellar Influences Vault/` remain immutable.
- V1 ingests only explicit combination formulas, not standalone factor chapters.
- The pilot slice must include three axis pages:
  - `Sun/Moon`
  - `Sun/Venus`
  - `Moon/Venus`
  This is a necessary consequence of the approved identity model, not scope creep.
- The repo should persist its own `AGENTS.md` so future sessions have a local schema/workflow reference instead of relying on conversation-only instructions.

## File Structure

### Files To Create

- `AGENTS.md`
- `tools/__init__.py`
- `tools/wiki_identity.py`
- `tools/wiki_pages.py`
- `tools/normalize_identity.py`
- `tools/rebuild_index.py`
- `tools/lint_wiki.py`
- `tests/conftest.py`
- `tests/tools/test_normalize_identity.py`
- `tests/tools/test_rebuild_index.py`
- `tests/tools/test_lint_wiki.py`
- `tests/wiki/test_pilot_cluster.py`
- `wiki/_templates/factor.md`
- `wiki/_templates/axis.md`
- `wiki/_templates/activation.md`
- `wiki/_templates/triad_hub.md`
- `wiki/_templates/source.md`
- `wiki/derived/.gitkeep`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/factors/sun.md`
- `wiki/factors/moon.md`
- `wiki/factors/venus.md`
- `wiki/axes/sun-moon.md`
- `wiki/axes/sun-venus.md`
- `wiki/axes/moon-venus.md`
- `wiki/activations/sun-moon-equals-venus.md`
- `wiki/activations/sun-venus-equals-moon.md`
- `wiki/activations/moon-venus-equals-sun.md`
- `wiki/triads/sun-moon-venus.md`
- `wiki/sources/reinhold-ebertin-the-combination-of-stellar-influences.md`

### File Responsibilities

- `AGENTS.md`
  - local operating schema for ingest, query, write-back, and lint rules
- `tools/wiki_identity.py`
  - pure identity helpers for factor, axis, activation, and triad-set normalization
- `tools/wiki_pages.py`
  - shared markdown/frontmatter loading and wiki page enumeration
- `tools/normalize_identity.py`
  - CLI for inspecting normalized identities and sibling orientation mapping
- `tools/rebuild_index.py`
  - regenerate `wiki/index.md` from page metadata
- `tools/lint_wiki.py`
  - validate required frontmatter, page link integrity, and orientation-safe identity rules
- `tests/tools/*.py`
  - unit coverage for helpers and CLI behavior
- `tests/wiki/test_pilot_cluster.py`
  - integration checks for the concrete pilot wiki pages
- `wiki/_templates/*.md`
  - canonical page skeletons for each page type
- `wiki/index.md`
  - content catalog
- `wiki/log.md`
  - append-only operational log
- `wiki/derived/.gitkeep`
  - keeps the empty derived-pages directory present in git from the initial bootstrap
- `wiki/factors/*.md`
  - doctrine pages for factors touched by the pilot cluster
- `wiki/axes/*.md`
  - doctrine pages for midpoint axes used by the pilot cluster
- `wiki/activations/*.md`
  - doctrine pages for orientation-specific formulas
- `wiki/triads/*.md`
  - structural hubs for unordered three-factor sets
- `wiki/sources/*.md`
  - provenance hub pages per source document

## Chunk 1: Core Tooling

### Task 1: Implement Identity Normalization Core

**Files:**
- Create: `tools/__init__.py`
- Create: `tools/wiki_identity.py`
- Create: `tools/normalize_identity.py`
- Test: `tests/tools/test_normalize_identity.py`

- [ ] **Step 1: Write the failing identity tests**

```python
from tools.wiki_identity import (
    normalize_axis,
    normalize_activation,
    triad_orientations,
)


def test_normalize_axis_sorts_the_pair_only():
    axis = normalize_axis("Moon", "Sun")
    assert axis.display == "Sun/Moon"
    assert axis.slug == "sun-moon"


def test_activation_orientation_is_preserved():
    left = normalize_activation("Sun", "Moon", "Venus")
    right = normalize_activation("Sun", "Venus", "Moon")
    assert left.display == "Sun/Moon = Venus"
    assert right.display == "Sun/Venus = Moon"
    assert left.display != right.display


def test_triad_orientations_lists_all_three_distinct_forms():
    orientations = triad_orientations(["Sun", "Moon", "Venus"])
    assert orientations == [
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    ]
```

- [ ] **Step 2: Run the identity tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_normalize_identity.py -v`

Expected: FAIL with import or missing symbol errors for `tools.wiki_identity`

- [ ] **Step 3: Write the minimal identity implementation**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class AxisIdentity:
    display: str
    slug: str


def normalize_axis(a: str, b: str) -> AxisIdentity:
    left, right = sorted([a.strip(), b.strip()], key=str.casefold)
    return AxisIdentity(display=f"{left}/{right}", slug=f"{left.lower()}-{right.lower()}")
```

Implementation notes:
- Keep factor names human-readable and title-cased.
- Sort midpoint pairs only inside the axis.
- Preserve the activated factor as the right side of the formula.
- Provide one helper that returns the three distinct orientation formulas for a triad-set.

- [ ] **Step 4: Run the identity tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_normalize_identity.py -v`

Expected: PASS for all identity tests

- [ ] **Step 5: Commit**

```bash
git add tools/__init__.py tools/wiki_identity.py tools/normalize_identity.py tests/tools/test_normalize_identity.py
git commit -m "feat: add wiki identity normalization helpers"
```

### Task 2: Implement Wiki Page Loading And Linting

**Files:**
- Create: `tools/wiki_pages.py`
- Create: `tools/lint_wiki.py`
- Create: `tests/conftest.py`
- Test: `tests/tools/test_lint_wiki.py`

- [ ] **Step 1: Write the failing lint tests**

```python
from pathlib import Path

from tools.lint_wiki import lint_wiki


def test_lint_rejects_activation_missing_axis(tmp_path: Path):
    page = tmp_path / "wiki" / "activations" / "sun-moon-equals-venus.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "---\n"
        "title: Sun/Moon = Venus\n"
        "page_type: activation\n"
        "slug: sun-moon-equals-venus\n"
        "---\n",
        encoding="utf-8",
    )
    problems = lint_wiki(tmp_path / "wiki")
    assert "missing required field 'axis'" in "\n".join(problems)


def test_lint_rejects_false_orientation_aliases(tmp_path: Path):
    # Alias should not collapse Sun/Moon = Venus into Sun/Venus = Moon.
    ...
```

- [ ] **Step 2: Run the lint tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_lint_wiki.py -v`

Expected: FAIL because `lint_wiki` and shared page loaders do not exist yet

- [ ] **Step 3: Write the minimal loader and linter**

```python
import yaml


def load_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    _, raw, body = text.split("---\n", 2)
    return yaml.safe_load(raw) or {}, body
```

Implementation notes:
- Keep frontmatter parsing in `tools/wiki_pages.py`, not duplicated in each script.
- Exclude `wiki/_templates/` from live-page enumeration.
- Validate required fields per `page_type`.
- Validate that activation pages include `axis`, `activated_by`, and `triad_set`.
- Validate that aliases do not contain a different oriented activation formula for the same triad-set.

- [ ] **Step 4: Run the lint tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_lint_wiki.py -v`

Expected: PASS for required-field and false-equivalence checks

- [ ] **Step 5: Commit**

```bash
git add tools/wiki_pages.py tools/lint_wiki.py tests/conftest.py tests/tools/test_lint_wiki.py
git commit -m "feat: add wiki page loader and linter"
```

### Task 3: Implement Index Rebuild Tool

**Files:**
- Create: `tools/rebuild_index.py`
- Test: `tests/tools/test_rebuild_index.py`

- [ ] **Step 1: Write the failing index rebuild tests**

```python
from tools.rebuild_index import build_index


def test_build_index_groups_pages_by_type(tmp_path):
    # Create a minimal factor and activation page under tmp_path/wiki
    index_text = build_index(tmp_path / "wiki")
    assert "## Factors" in index_text
    assert "## Activations" in index_text
```

- [ ] **Step 2: Run the index tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_rebuild_index.py -v`

Expected: FAIL because `build_index` is not implemented yet

- [ ] **Step 3: Write the minimal index builder**

```python
SECTION_TITLES = {
    "factor": "Factors",
    "axis": "Axes",
    "activation": "Activations",
    "triad_hub": "Triad Hubs",
    "source": "Sources",
    "derived": "Derived Pages",
}
```

Implementation notes:
- Read page metadata through `tools/wiki_pages.py`.
- Ignore `wiki/_templates/` when generating the live index.
- Sort entries by title within each section.
- Use one-line summaries if available; otherwise fall back to page type and title.
- Make this tool write deterministic output so git diffs stay clean.

- [ ] **Step 4: Run the index tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_rebuild_index.py -v`

Expected: PASS for sectioning and deterministic ordering

- [ ] **Step 5: Commit**

```bash
git add tools/rebuild_index.py tests/tools/test_rebuild_index.py
git commit -m "feat: add wiki index rebuild tool"
```

## Chunk 2: Repo Scaffold And Pilot Content

### Task 4: Create The Local Schema And Wiki Templates

**Files:**
- Create: `AGENTS.md`
- Create: `tests/wiki/test_pilot_cluster.py`
- Create: `wiki/_templates/factor.md`
- Create: `wiki/_templates/axis.md`
- Create: `wiki/_templates/activation.md`
- Create: `wiki/_templates/triad_hub.md`
- Create: `wiki/_templates/source.md`
- Create: `wiki/derived/.gitkeep`
- Create: `wiki/index.md`
- Create: `wiki/log.md`

- [ ] **Step 1: Write the failing scaffold integration test**

```python
from pathlib import Path


def test_required_templates_exist():
    assert Path("wiki/_templates/factor.md").exists()
    assert Path("wiki/_templates/activation.md").exists()
    assert Path("AGENTS.md").exists()
```

- [ ] **Step 2: Run the scaffold test to verify it fails**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_pilot_cluster.py::test_required_templates_exist -v`

Expected: FAIL because the scaffold files do not exist yet

- [ ] **Step 3: Create the schema and template files**

Template requirements:
- Each template must include YAML frontmatter matching the approved spec.
- `AGENTS.md` must encode:
  - raw-source immutability
  - page-type identity rules
  - ingest workflow
  - query/write-back boundaries
  - contradiction handling
  - lint/index maintenance expectations
- `wiki/index.md` should start with placeholder section headings matching the rebuild tool.
- `wiki/log.md` should start with a top-level heading and one bootstrap entry.

- [ ] **Step 4: Run the scaffold test and repo lint to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_pilot_cluster.py::test_required_templates_exist -v`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Expected:
- the scaffold test passes
- the linter reports no structural errors for the new templates and seed wiki files

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md wiki/_templates wiki/derived/.gitkeep wiki/index.md wiki/log.md tests/wiki/test_pilot_cluster.py
git commit -m "feat: add wiki schema and template scaffold"
```

### Task 5: Create The Ebertin Pilot Source And Canonical Pages

**Files:**
- Create: `wiki/sources/reinhold-ebertin-the-combination-of-stellar-influences.md`
- Create: `wiki/factors/sun.md`
- Create: `wiki/factors/moon.md`
- Create: `wiki/factors/venus.md`
- Create: `wiki/axes/sun-moon.md`
- Create: `wiki/axes/sun-venus.md`
- Create: `wiki/axes/moon-venus.md`
- Create: `wiki/activations/sun-moon-equals-venus.md`
- Create: `wiki/activations/sun-venus-equals-moon.md`
- Create: `wiki/activations/moon-venus-equals-sun.md`
- Create: `wiki/triads/sun-moon-venus.md`
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`
- Test: `tests/wiki/test_pilot_cluster.py`

- [ ] **Step 1: Write the failing pilot-content integration tests**

```python
from pathlib import Path

from tools.wiki_pages import load_page


def test_three_activation_pages_are_distinct():
    left = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))
    middle = load_page(Path("wiki/activations/sun-venus-equals-moon.md"))
    right = load_page(Path("wiki/activations/moon-venus-equals-sun.md"))
    assert left.meta["normalized_formula"] != middle.meta["normalized_formula"]
    assert middle.meta["normalized_formula"] != right.meta["normalized_formula"]


def test_triad_hub_links_all_orientations():
    triad = load_page(Path("wiki/triads/sun-moon-venus.md"))
    assert triad.meta["orientations"] == [
        "Moon/Venus = Sun",
        "Sun/Moon = Venus",
        "Sun/Venus = Moon",
    ]
```

- [ ] **Step 2: Run the pilot-content tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_pilot_cluster.py -v`

Expected: FAIL because the pilot wiki pages do not exist yet

- [ ] **Step 3: Create the pilot source and wiki pages**

Content requirements:
- Source page:
  - bibliographic metadata for Ebertin
  - scope notes that V1 ingests only explicit formulas
  - links to the pilot factor, axis, activation, and triad pages
- Activation pages:
  - exact normalized formula in frontmatter
  - exact source page references
  - source-native entries separated from comparative schema
  - no collapsing of the three orientations
- Axis pages:
  - `Sun/Moon`, `Sun/Venus`, and `Moon/Venus` each present as separate doctrine pages
- Triad hub:
  - structural map only
  - all three orientation siblings linked
  - no merged doctrinal interpretation
- Factor pages:
  - populated only by formula-derived pilot material
  - no standalone chapter synthesis

- [ ] **Step 4: Rebuild the index and run all tests**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools tests/wiki/test_pilot_cluster.py -v`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Expected:
- the index is regenerated deterministically
- all tool and pilot integration tests pass
- the linter reports no missing fields, broken links, or false-equivalence problems

- [ ] **Step 5: Commit**

```bash
git add wiki/sources wiki/factors wiki/axes wiki/activations wiki/triads wiki/index.md wiki/log.md tests/wiki/test_pilot_cluster.py
git commit -m "feat: add Ebertin pilot wiki cluster"
```

### Task 6: Perform Final Verification And Document The Bootstrap Baseline

**Files:**
- Modify: `wiki/log.md`
- Modify: `wiki/index.md` if rebuild changes it

- [ ] **Step 1: Add a final bootstrap verification test if coverage is still missing**

```python
def test_axis_pages_cover_all_activation_axes():
    # Every pilot activation should point to an existing axis page.
    ...
```

- [ ] **Step 2: Run the full verification suite**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests -v`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Expected:
- all tests PASS
- index rebuild is idempotent
- lint still passes after the rebuild

- [ ] **Step 3: Append the verified pilot bootstrap entry to the log**

Log entry should record:
- date
- source used
- pages created
- tests run
- lint/index status
- open follow-up work, if any

- [ ] **Step 4: Inspect the git diff for accidental scope growth**

Run: `git diff --stat HEAD~1..HEAD`

Expected:
- only planned files changed
- no edits under `Stellar Influences Vault/`

- [ ] **Step 5: Commit**

```bash
git add wiki/log.md wiki/index.md tests/wiki/test_pilot_cluster.py
git commit -m "chore: verify wiki bootstrap baseline"
```

## Execution Notes

- Use `apply_patch` for all file creation and edits.
- Use the exact Python interpreter required by the repo instructions:
  - `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`
- Do not run smoke tests intended for the MADHEX codebase; this repo is not MADHEX.
- Keep the raw source PDFs untouched.
- Do not ingest the Witte source yet. The Ebertin pilot must pass first.

## Definition Of Done

The bootstrap is done when all of the following are true:

- `AGENTS.md`, templates, index, and log exist and match the approved schema.
- Identity helpers normalize axes but preserve activation orientation.
- Index rebuild and lint tools pass against the live wiki.
- The pilot cluster contains three distinct activation pages, three corresponding axis pages, one triad hub, one source page, and the affected factor pages.
- Every claim on pilot canonical pages points to exact Ebertin source pages.
- The triad hub links the three orientations without merging their meanings.
- `pytest` and `lint_wiki.py` pass from the required Python environment.
