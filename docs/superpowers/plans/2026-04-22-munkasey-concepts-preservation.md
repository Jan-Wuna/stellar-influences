# Munkasey Concepts Preservation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve Michael Munkasey's page-3 `CONCEPTS` corpus as separate source-grounded companion pages linked from the canonical axis pages, while explicitly dropping all page-4 MWA example tables.

**Architecture:** Build a dedicated Munkasey parser that extracts only the page-1 axis prose and page-3 concepts lists for the 78 covered midpoint pairs. Feed those models into an idempotent Munkasey ingest script that writes one source page, 78 derived concepts pages, and one Munkasey source entry plus concepts companion link into each covered axis page, then rebuild the index and verify that no MWA example-table text leaks into the wiki.

**Tech Stack:** Markdown with YAML frontmatter, Python via `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`, `pytest`, `PyMuPDF (fitz)`, `rg`, Git

---

## Assumptions

- The approved spec in [2026-04-22-munkasey-concepts-preservation-design.md](/W:/Stellar%20Influences/docs/superpowers/specs/2026-04-22-munkasey-concepts-preservation-design.md) is the source of truth.
- Raw files under `Stellar Influences Vault/` remain immutable.
- This plan implements only the Munkasey concepts-preservation slice plus the minimum axis-page integration needed to make it usable.
- This plan does not create Munkasey activation pages, factor pages, or any MWA evidence pages.
- MWA example-table material from page 4 is intentionally discarded.
- The current worktree is already dirty with unrelated changes. Implementation must not revert, reformat, or otherwise disturb files outside the ones listed here.

## File Structure

### Files To Create

- `tools/munkasey_source.py`
- `tools/ingest_munkasey.py`
- `tests/tools/test_munkasey_source.py`
- `tests/wiki/test_munkasey_concepts_ingest.py`
- `wiki/sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md`
- `docs/superpowers/plans/2026-04-22-munkasey-concepts-preservation.md`

### Files To Modify

- `wiki/index.md`
- `wiki/log.md`
- Axis pages listed in `Appendix A`

### Files To Create During Ingest

- Concepts companion pages listed in `Appendix B`

### Files To Read During Implementation

- `AGENTS.md`
- `docs/superpowers/specs/2026-04-22-munkasey-concepts-preservation-design.md`
- `tools/sandbach_source.py`
- `tools/ingest_sandbach.py`
- `tools/wiki_identity.py`
- `tools/wiki_pages.py`
- `tools/rebuild_index.py`
- `tools/lint_wiki.py`
- `tests/wiki/test_sandbach_ingest.py`
- `wiki/axes/sun-moon.md`
- `wiki/axes/venus-saturn.md`
- `wiki/axes/asc-mc.md`
- `wiki/derived/munkasey-unleashing-the-power-of-the-planets-ingest-analysis.md`

### File Responsibilities

- `tools/munkasey_source.py`
  - parse the PDF into structured pair-level models for page-1 axis prose and page-3 concepts only
- `tools/ingest_munkasey.py`
  - merge one Munkasey source entry into each covered axis page, write the source page, and generate the 78 concepts companion pages idempotently
- `tests/tools/test_munkasey_source.py`
  - prove the parser extracts the expected pair headings, page-1 prose fields, ordered concepts lists, and excludes MWA tables
- `tests/wiki/test_munkasey_concepts_ingest.py`
  - prove the ingest writes the source page and concepts pages, inserts exactly one companion link per touched axis page, and never renders MWA example-table text
- `wiki/sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md`
  - provenance hub for the source and explicit statement that concepts are preserved while MWA tables are omitted
- `wiki/axes/*.md` from `Appendix A`
  - retain current comparative doctrine while gaining one explicit Munkasey source entry plus one concepts companion link
- `wiki/derived/munkasey-*-concepts.md` from `Appendix B`
  - preserve Munkasey's page-3 phrase material as source-grounded companion sheets
- `wiki/index.md`
  - rebuilt by `tools/rebuild_index.py`
- `wiki/log.md`
  - append-only record of the concepts-preservation ingest

## Chunk 1: Munkasey Parser

### Task 1: Build The Pair Parser For Page-1 And Page-3 Content

**Files:**
- Create: `tools/munkasey_source.py`
- Test: `tests/tools/test_munkasey_source.py`

- [ ] **Step 1: Write the failing parser tests for `Sun/Moon` and `Venus/Saturn`**

```python
from pathlib import Path

from tools.munkasey_source import SOURCE_FILE, generate_models


SOURCE_PATH = Path("Stellar Influences Vault") / SOURCE_FILE


def test_munkasey_parser_extracts_sun_moon_axis_fields():
    blocks = generate_models(SOURCE_PATH)
    sun_moon = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Sun", "Moon"))
    assert sun_moon.axis_page == 55
    assert "direction and focus of your personal awareness" in sun_moon.basic_ideas
    assert "The attention you place on whatever is important to you in life" in sun_moon.personal_thesis
    assert "Your lack of will or enthusiasm shown when caring about others" in sun_moon.personal_anti
    assert "The approval you give or receive to or with another" in sun_moon.relationship_thesis
    assert "Chemical, Ph, and mineral balances within the body" in sun_moon.body_mind


def test_munkasey_parser_extracts_ordered_concepts_without_examples():
    blocks = generate_models(SOURCE_PATH)
    sun_moon = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Sun", "Moon"))
    assert sun_moon.concepts_page == 57
    assert sun_moon.concepts[:5] == (
        "Arrogant Approval",
        "Emotional Pretension",
        "Flowery Imagination",
        "Celebrated Caring",
        "Special Sensitivities",
    )
    assert "STRONG:" not in sun_moon.concepts
    assert "EVENTS:" not in sun_moon.concepts


def test_munkasey_parser_extracts_venus_saturn_concepts_page():
    blocks = generate_models(SOURCE_PATH)
    venus_saturn = next(block for block in blocks if (block.factor_a, block.factor_b) == ("Venus", "Saturn"))
    assert venus_saturn.concepts_page == 197
    assert venus_saturn.concepts[:4] == (
        "Prolongs Love",
        "Prefers Plainness",
        "Stable Affections",
        "A Serious Artist",
    )
```

- [ ] **Step 2: Run the parser tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_munkasey_source.py -v`

Expected: FAIL with import errors or missing parser symbols for `tools.munkasey_source`

- [ ] **Step 3: Write the minimal parser model and heading detection**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class MunkaseyAxisBlock:
    factor_a: str
    factor_b: str
    axis_page: int
    concepts_page: int
    source_heading: str
    basic_ideas: str
    personal_thesis: str
    personal_anti: str
    relationship_thesis: str
    relationship_anti: str
    body_mind: str
    politics_business_thesis: str
    politics_business_anti: str
    concepts: tuple[str, ...]
```

Implementation notes:
- Reuse the same canonical factor order used in the PDF: `Sun`, `Moon`, `Mercury`, `Venus`, `Mars`, `Jupiter`, `Saturn`, `Uranus`, `Neptune`, `Pluto`, `Node`, `Asc`, `MC`.
- Detect the 78 midpoint headings from the page-1 title lines such as `SUN/MOON            (a/s)`.
- Treat each midpoint as a 4-page unit and extract only page 1 and page 3.
- Preserve printed page numbers, not zero-based PDF indices.
- Normalize PDF line wrapping and soft hyphens conservatively.
- Ignore page 4 entirely except for using its existence to bound the page-3 extraction window.

- [ ] **Step 4: Run the parser tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_munkasey_source.py -v`

Expected: PASS for `Sun/Moon` axis fields, `Sun/Moon` concepts ordering, and `Venus/Saturn` concepts extraction

- [ ] **Step 5: Commit**

```bash
git add tools/munkasey_source.py tests/tools/test_munkasey_source.py
git commit -m "feat: add Munkasey concepts parser"
```

### Task 2: Expand Parser Coverage To The Full 78-Pair Corpus

**Files:**
- Modify: `tools/munkasey_source.py`
- Modify: `tests/tools/test_munkasey_source.py`

- [ ] **Step 1: Add failing full-coverage and anti-MWA tests**

```python
def test_munkasey_parser_covers_all_78_pairs():
    blocks = generate_models(SOURCE_PATH)
    assert len(blocks) == 78
    assert blocks[0].source_heading == "SUN/MOON"
    assert blocks[-1].source_heading == "ASCENDANT/MIDHEAVEN"


def test_munkasey_parser_never_leaks_page_four_mwa_text_into_concepts():
    blocks = generate_models(SOURCE_PATH)
    all_concepts = "\n".join(item for block in blocks for item in block.concepts)
    assert "STRONG:" not in all_concepts
    assert "WEAK:" not in all_concepts
    assert "EVENTS:" not in all_concepts
    assert "Significant Examples of People and Events" not in all_concepts
```

- [ ] **Step 2: Run the parser tests to verify the new coverage tests fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_munkasey_source.py -v`

Expected: FAIL on pair-count mismatch, heading mismatch, or MWA leakage

- [ ] **Step 3: Tighten chapter-window logic and concepts extraction**

```python
def _concept_lines(page_text: str) -> tuple[str, ...]:
    concepts: list[str] = []
    for raw_line in page_text.splitlines():
        line = " ".join(raw_line.split()).strip()
        if not line:
            continue
        if line.endswith("CONCEPTS"):
            continue
        if re.fullmatch(r"\d{1,3}", line):
            continue
        concepts.append(line)
    return tuple(concepts)
```

Implementation notes:
- Exclude the page header, page number, and `... CONCEPTS` heading.
- Stop concepts extraction at the end of page 3; do not scan page 4 at all.
- Preserve source order exactly.
- Fail loudly if the parser does not find 78 blocks after heading normalization.

- [ ] **Step 4: Run the parser tests to verify full coverage passes**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_munkasey_source.py -v`

Expected: PASS with `78` blocks and zero MWA leakage

- [ ] **Step 5: Commit**

```bash
git add tools/munkasey_source.py tests/tools/test_munkasey_source.py
git commit -m "test: verify full Munkasey concepts coverage"
```

## Chunk 2: Source Page And Concepts Companion Pages

### Task 3: Render The Munkasey Source Page And 78 Concepts Pages

**Files:**
- Create: `tools/ingest_munkasey.py`
- Create: `wiki/sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md`
- Create: files from `Appendix B`
- Test: `tests/wiki/test_munkasey_concepts_ingest.py`

- [ ] **Step 1: Write the failing ingest tests for the source page and one concepts page**

```python
from pathlib import Path

from tools.wiki_pages import load_page


SOURCE_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"


def test_munkasey_source_page_exists_and_mentions_mwa_omission():
    page = load_page(Path("wiki/sources") / f"{SOURCE_SLUG}.md")
    assert page.meta["page_type"] == "source"
    assert page.meta["framework_scope"] == "modern_astrology"
    assert "page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`" in page.body
    assert "page-4 MWA example tables were intentionally omitted" in page.body


def test_sun_moon_concepts_companion_page_exists():
    page = load_page(Path("wiki/derived/munkasey-sun-moon-concepts.md"))
    assert page.meta["page_type"] == "derived"
    assert page.meta["slug"] == "munkasey-sun-moon-concepts"
    assert "## Source Concepts" in page.body
    assert "- Arrogant Approval" in page.body
    assert "Jerry Rubin" not in page.body
```

- [ ] **Step 2: Run the ingest tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_munkasey_concepts_ingest.py -v`

Expected: FAIL because the source page and concepts pages do not exist yet

- [ ] **Step 3: Write the minimal source-page and concepts-page renderers**

```python
def render_concepts_page(block: MunkaseyAxisBlock) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    concepts = "\n".join(f"- {item}" for item in block.concepts)
    return f"""---
title: "Michael Munkasey - {axis.display} Concepts"
page_type: derived
slug: munkasey-{axis.slug}-concepts
status: source_grounded
framework_scope: modern_astrology
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Purpose

Preserve Munkasey's page-3 concept phrases for `{axis.display}` as source-native image material.

## Evidence Base

- [{axis.display}](../axes/{axis.slug}.md)
- [Michael Munkasey - Midpoints: Unleashing the Power of the Planets](../sources/{SOURCE_SLUG}.md)
- Source concept page: `{block.concepts_page}`

## Source Concepts

{concepts}

## Notes On Use

- These phrases are preserved as source-native concept prompts, not as comparative doctrine.
- They are kept off the canonical axis page's comparative schema to avoid conflating image phrases with formal delineation.
"""
```

Implementation notes:
- Generate all 78 pages from the parsed blocks in one pass.
- Reuse `normalize_axis()` for display and slug consistency.
- Do not write any `Derived Synthesis` section to these pages.
- Keep the source page body explicit about the omission of MWA tables.

- [ ] **Step 4: Run the ingest tests to verify the source page and concepts page pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_munkasey_concepts_ingest.py -v`

Expected: PASS for source-page existence, concepts-page existence, and absence of MWA names in the companion page

- [ ] **Step 5: Commit**

```bash
git add tools/ingest_munkasey.py tests/wiki/test_munkasey_concepts_ingest.py wiki/sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md wiki/derived/munkasey-*-concepts.md
git commit -m "feat: render Munkasey concepts companion pages"
```

## Chunk 3: Axis-Page Integration And Verification

### Task 4: Merge Munkasey Axis Entries And Concepts Links Into The 78 Axis Pages

**Files:**
- Modify: files from `Appendix A`
- Modify: `tools/ingest_munkasey.py`
- Modify: `tests/wiki/test_munkasey_concepts_ingest.py`

- [ ] **Step 1: Add failing tests for axis-page merge and idempotent linking**

```python
def test_sun_moon_axis_gains_munkasey_source_entry_and_companion_link():
    page = load_page(Path("wiki/axes/sun-moon.md"))
    assert "### Michael Munkasey - Midpoints: Unleashing the Power of the Planets" in page.body
    assert "direction and focus of your personal awareness" in page.body
    assert "#### Munkasey Concepts Companion" in page.body
    assert "../derived/munkasey-sun-moon-concepts.md" in page.body


def test_venus_saturn_axis_links_exactly_one_concepts_companion():
    page = load_page(Path("wiki/axes/venus-saturn.md"))
    assert page.body.count("munkasey-venus-saturn-concepts.md") == 1


def test_mwa_example_table_text_is_not_rendered_to_axis_pages():
    page = load_page(Path("wiki/axes/sun-moon.md"))
    assert "Significant Examples of People and Events Using Sun/Moon" not in page.body
    assert "STRONG:" not in page.body
    assert "WEAK:" not in page.body
    assert "EVENTS:" not in page.body
```

- [ ] **Step 2: Run the axis-page ingest tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_munkasey_concepts_ingest.py -v`

Expected: FAIL because the axis pages do not yet contain Munkasey entries or companion links

- [ ] **Step 3: Implement idempotent axis-page rendering and link insertion**

```python
def _munkasey_axis_entry(block: MunkaseyAxisBlock) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    companion_slug = f"munkasey-{axis.slug}-concepts"
    return f"""### {SOURCE_TITLE}

- Source heading: `{block.source_heading}`
- Source page: `{block.axis_page}`

#### Basic Ideas

{block.basic_ideas}

#### In Your Personal Life

- Thesis: {block.personal_thesis}
- Anti: {block.personal_anti}

#### In Your Relationships

- Thesis: {block.relationship_thesis}
- Anti: {block.relationship_anti}

#### With Body or Mind

{block.body_mind}

#### In Politics or Business

- Thesis: {block.politics_business_thesis}
- Anti: {block.politics_business_anti}

#### Munkasey Concepts Companion

- [Michael Munkasey - {axis.display} Concepts](../derived/{companion_slug}.md)
"""
```

Implementation notes:
- Append or replace the Munkasey source entry using the same idempotent source-entry merge pattern used in `tools/ingest_sandbach.py`.
- Add the Munkasey slug to `source_pages` on each touched axis page.
- Preserve existing `framework_scope: comparative` behavior if multiple sources are present.
- Keep the companion link inside the Munkasey source entry so reruns can replace one contiguous block rather than splice free-floating links.
- Do not add any Munkasey content to activation pages, factor pages, or triad hubs in this slice.

- [ ] **Step 4: Run the axis-page ingest tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_munkasey_concepts_ingest.py -v`

Expected: PASS for Munkasey source entry insertion, single companion-link insertion, and absence of MWA text

- [ ] **Step 5: Commit**

```bash
git add tools/ingest_munkasey.py tests/wiki/test_munkasey_concepts_ingest.py wiki/axes/*.md
git commit -m "feat: link Munkasey concepts from axis pages"
```

### Task 5: Run Full Verification And Refresh Generated Index

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

- [ ] **Step 1: Add a failing end-to-end verification test**

```python
def test_all_78_munkasey_concepts_pages_exist():
    paths = sorted(Path("wiki/derived").glob("munkasey-*-concepts.md"))
    assert len(paths) == 78
```

- [ ] **Step 2: Run the focused wiki tests to verify the new end-to-end assertion fails before the full ingest run**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_munkasey_concepts_ingest.py -v`

Expected: FAIL until the full ingest has been executed against the repo

- [ ] **Step 3: Execute the full ingest, rebuild the index, and append the wiki log**

Run:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/ingest_munkasey.py
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py
```

Implementation notes:
- `tools/ingest_munkasey.py` should own the `wiki/log.md` append for this feature.
- The log entry should state that page-3 concepts were preserved as companion pages and that MWA tables were omitted.
- Rebuild `wiki/index.md` after the wiki write completes.

- [ ] **Step 4: Run verification**

Run:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_munkasey_source.py tests/wiki/test_munkasey_concepts_ingest.py -v
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py
```

Expected:
- all focused Munkasey parser and ingest tests PASS
- `tools/lint_wiki.py` prints `Lint passed`

- [ ] **Step 5: Run a final leak check for discarded MWA table markers**

Run: `rg -n "Significant Examples of People and Events|^STRONG:|^WEAK:|^EVENTS:" wiki/axes wiki/derived wiki/sources`

Expected:
- no matches inside Munkasey-generated wiki content
- any matches outside the Munkasey slice should be inspected before proceeding

- [ ] **Step 6: Commit**

```bash
git add wiki/index.md wiki/log.md wiki/axes/*.md wiki/derived/munkasey-*-concepts.md wiki/sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md
git commit -m "feat: preserve Munkasey concepts as companion pages"
```

## Appendix A: Exact Axis Pages To Modify

- `wiki/axes/sun-moon.md`
- `wiki/axes/sun-mercury.md`
- `wiki/axes/sun-venus.md`
- `wiki/axes/sun-mars.md`
- `wiki/axes/sun-jupiter.md`
- `wiki/axes/sun-saturn.md`
- `wiki/axes/sun-uranus.md`
- `wiki/axes/sun-neptune.md`
- `wiki/axes/sun-pluto.md`
- `wiki/axes/sun-node.md`
- `wiki/axes/sun-asc.md`
- `wiki/axes/sun-mc.md`
- `wiki/axes/moon-mercury.md`
- `wiki/axes/moon-venus.md`
- `wiki/axes/moon-mars.md`
- `wiki/axes/moon-jupiter.md`
- `wiki/axes/moon-saturn.md`
- `wiki/axes/moon-uranus.md`
- `wiki/axes/moon-neptune.md`
- `wiki/axes/moon-pluto.md`
- `wiki/axes/moon-node.md`
- `wiki/axes/moon-asc.md`
- `wiki/axes/moon-mc.md`
- `wiki/axes/mercury-venus.md`
- `wiki/axes/mercury-mars.md`
- `wiki/axes/mercury-jupiter.md`
- `wiki/axes/mercury-saturn.md`
- `wiki/axes/mercury-uranus.md`
- `wiki/axes/mercury-neptune.md`
- `wiki/axes/mercury-pluto.md`
- `wiki/axes/mercury-node.md`
- `wiki/axes/mercury-asc.md`
- `wiki/axes/mercury-mc.md`
- `wiki/axes/venus-mars.md`
- `wiki/axes/venus-jupiter.md`
- `wiki/axes/venus-saturn.md`
- `wiki/axes/venus-uranus.md`
- `wiki/axes/venus-neptune.md`
- `wiki/axes/venus-pluto.md`
- `wiki/axes/venus-node.md`
- `wiki/axes/venus-asc.md`
- `wiki/axes/venus-mc.md`
- `wiki/axes/mars-jupiter.md`
- `wiki/axes/mars-saturn.md`
- `wiki/axes/mars-uranus.md`
- `wiki/axes/mars-neptune.md`
- `wiki/axes/mars-pluto.md`
- `wiki/axes/mars-node.md`
- `wiki/axes/mars-asc.md`
- `wiki/axes/mars-mc.md`
- `wiki/axes/jupiter-saturn.md`
- `wiki/axes/jupiter-uranus.md`
- `wiki/axes/jupiter-neptune.md`
- `wiki/axes/jupiter-pluto.md`
- `wiki/axes/jupiter-node.md`
- `wiki/axes/jupiter-asc.md`
- `wiki/axes/jupiter-mc.md`
- `wiki/axes/saturn-uranus.md`
- `wiki/axes/saturn-neptune.md`
- `wiki/axes/saturn-pluto.md`
- `wiki/axes/saturn-node.md`
- `wiki/axes/saturn-asc.md`
- `wiki/axes/saturn-mc.md`
- `wiki/axes/uranus-neptune.md`
- `wiki/axes/uranus-pluto.md`
- `wiki/axes/uranus-node.md`
- `wiki/axes/uranus-asc.md`
- `wiki/axes/uranus-mc.md`
- `wiki/axes/neptune-pluto.md`
- `wiki/axes/neptune-node.md`
- `wiki/axes/neptune-asc.md`
- `wiki/axes/neptune-mc.md`
- `wiki/axes/pluto-node.md`
- `wiki/axes/pluto-asc.md`
- `wiki/axes/pluto-mc.md`
- `wiki/axes/node-asc.md`
- `wiki/axes/node-mc.md`
- `wiki/axes/asc-mc.md`

## Appendix B: Exact Concepts Pages To Create

- `wiki/derived/munkasey-sun-moon-concepts.md`
- `wiki/derived/munkasey-sun-mercury-concepts.md`
- `wiki/derived/munkasey-sun-venus-concepts.md`
- `wiki/derived/munkasey-sun-mars-concepts.md`
- `wiki/derived/munkasey-sun-jupiter-concepts.md`
- `wiki/derived/munkasey-sun-saturn-concepts.md`
- `wiki/derived/munkasey-sun-uranus-concepts.md`
- `wiki/derived/munkasey-sun-neptune-concepts.md`
- `wiki/derived/munkasey-sun-pluto-concepts.md`
- `wiki/derived/munkasey-sun-node-concepts.md`
- `wiki/derived/munkasey-sun-asc-concepts.md`
- `wiki/derived/munkasey-sun-mc-concepts.md`
- `wiki/derived/munkasey-moon-mercury-concepts.md`
- `wiki/derived/munkasey-moon-venus-concepts.md`
- `wiki/derived/munkasey-moon-mars-concepts.md`
- `wiki/derived/munkasey-moon-jupiter-concepts.md`
- `wiki/derived/munkasey-moon-saturn-concepts.md`
- `wiki/derived/munkasey-moon-uranus-concepts.md`
- `wiki/derived/munkasey-moon-neptune-concepts.md`
- `wiki/derived/munkasey-moon-pluto-concepts.md`
- `wiki/derived/munkasey-moon-node-concepts.md`
- `wiki/derived/munkasey-moon-asc-concepts.md`
- `wiki/derived/munkasey-moon-mc-concepts.md`
- `wiki/derived/munkasey-mercury-venus-concepts.md`
- `wiki/derived/munkasey-mercury-mars-concepts.md`
- `wiki/derived/munkasey-mercury-jupiter-concepts.md`
- `wiki/derived/munkasey-mercury-saturn-concepts.md`
- `wiki/derived/munkasey-mercury-uranus-concepts.md`
- `wiki/derived/munkasey-mercury-neptune-concepts.md`
- `wiki/derived/munkasey-mercury-pluto-concepts.md`
- `wiki/derived/munkasey-mercury-node-concepts.md`
- `wiki/derived/munkasey-mercury-asc-concepts.md`
- `wiki/derived/munkasey-mercury-mc-concepts.md`
- `wiki/derived/munkasey-venus-mars-concepts.md`
- `wiki/derived/munkasey-venus-jupiter-concepts.md`
- `wiki/derived/munkasey-venus-saturn-concepts.md`
- `wiki/derived/munkasey-venus-uranus-concepts.md`
- `wiki/derived/munkasey-venus-neptune-concepts.md`
- `wiki/derived/munkasey-venus-pluto-concepts.md`
- `wiki/derived/munkasey-venus-node-concepts.md`
- `wiki/derived/munkasey-venus-asc-concepts.md`
- `wiki/derived/munkasey-venus-mc-concepts.md`
- `wiki/derived/munkasey-mars-jupiter-concepts.md`
- `wiki/derived/munkasey-mars-saturn-concepts.md`
- `wiki/derived/munkasey-mars-uranus-concepts.md`
- `wiki/derived/munkasey-mars-neptune-concepts.md`
- `wiki/derived/munkasey-mars-pluto-concepts.md`
- `wiki/derived/munkasey-mars-node-concepts.md`
- `wiki/derived/munkasey-mars-asc-concepts.md`
- `wiki/derived/munkasey-mars-mc-concepts.md`
- `wiki/derived/munkasey-jupiter-saturn-concepts.md`
- `wiki/derived/munkasey-jupiter-uranus-concepts.md`
- `wiki/derived/munkasey-jupiter-neptune-concepts.md`
- `wiki/derived/munkasey-jupiter-pluto-concepts.md`
- `wiki/derived/munkasey-jupiter-node-concepts.md`
- `wiki/derived/munkasey-jupiter-asc-concepts.md`
- `wiki/derived/munkasey-jupiter-mc-concepts.md`
- `wiki/derived/munkasey-saturn-uranus-concepts.md`
- `wiki/derived/munkasey-saturn-neptune-concepts.md`
- `wiki/derived/munkasey-saturn-pluto-concepts.md`
- `wiki/derived/munkasey-saturn-node-concepts.md`
- `wiki/derived/munkasey-saturn-asc-concepts.md`
- `wiki/derived/munkasey-saturn-mc-concepts.md`
- `wiki/derived/munkasey-uranus-neptune-concepts.md`
- `wiki/derived/munkasey-uranus-pluto-concepts.md`
- `wiki/derived/munkasey-uranus-node-concepts.md`
- `wiki/derived/munkasey-uranus-asc-concepts.md`
- `wiki/derived/munkasey-uranus-mc-concepts.md`
- `wiki/derived/munkasey-neptune-pluto-concepts.md`
- `wiki/derived/munkasey-neptune-node-concepts.md`
- `wiki/derived/munkasey-neptune-asc-concepts.md`
- `wiki/derived/munkasey-neptune-mc-concepts.md`
- `wiki/derived/munkasey-pluto-node-concepts.md`
- `wiki/derived/munkasey-pluto-asc-concepts.md`
- `wiki/derived/munkasey-pluto-mc-concepts.md`
- `wiki/derived/munkasey-node-asc-concepts.md`
- `wiki/derived/munkasey-node-mc-concepts.md`
- `wiki/derived/munkasey-asc-mc-concepts.md`
