# Carter Ingest Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest Charles Carter's *The Astrological Aspects* into the existing canonical axis pages as clearly labeled Carter aspect-family source entries, without modifying activation pages, triad hubs, or factor pages.

**Architecture:** Build a dedicated Carter parser that extracts unordered planetary pair chapters, their three aspect-family sections, and family-grouped example lists from the PDF. Feed those models into an idempotent Carter ingest script that updates only the 36 covered axis pages plus one Carter source page, then verify that the midpoint corpus remains intact and that Carter never bleeds into activation or factor doctrine.

**Tech Stack:** Markdown with YAML frontmatter, Python via `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`, `pytest`, `PyMuPDF (fitz)`, Git

---

## Assumptions

- The approved spec in [2026-04-21-carter-ingest-design.md](/W:/Stellar%20Influences/docs/superpowers/specs/2026-04-21-carter-ingest-design.md) is the source of truth.
- Raw files under `Stellar Influences Vault/` remain immutable.
- Carter content is collapsed only into axis pages and the Carter source page.
- Carter does not create or update activation pages, triad hubs, or factor pages in the first pass.
- The current worktree is already dirty with unrelated wiki work; implementation must not revert or overwrite unrelated edits outside the files listed in this plan.

## File Structure

### Files To Create

- `tools/carter_source.py`
- `tools/ingest_carter.py`
- `tests/tools/test_carter_source.py`
- `tests/wiki/test_carter_axis_ingest.py`
- `wiki/sources/charles-carter-the-astrological-aspects.md`
- `docs/superpowers/plans/2026-04-21-carter-ingest.md`

### Files To Modify

- `wiki/axes/sun-moon.md`
- `wiki/axes/sun-mercury.md`
- `wiki/axes/sun-venus.md`
- `wiki/axes/sun-mars.md`
- `wiki/axes/sun-jupiter.md`
- `wiki/axes/sun-saturn.md`
- `wiki/axes/sun-uranus.md`
- `wiki/axes/sun-neptune.md`
- `wiki/axes/moon-mercury.md`
- `wiki/axes/moon-venus.md`
- `wiki/axes/moon-mars.md`
- `wiki/axes/moon-jupiter.md`
- `wiki/axes/moon-saturn.md`
- `wiki/axes/moon-uranus.md`
- `wiki/axes/moon-neptune.md`
- `wiki/axes/mercury-venus.md`
- `wiki/axes/mercury-mars.md`
- `wiki/axes/mercury-jupiter.md`
- `wiki/axes/mercury-saturn.md`
- `wiki/axes/mercury-uranus.md`
- `wiki/axes/mercury-neptune.md`
- `wiki/axes/venus-mars.md`
- `wiki/axes/venus-jupiter.md`
- `wiki/axes/venus-saturn.md`
- `wiki/axes/venus-uranus.md`
- `wiki/axes/venus-neptune.md`
- `wiki/axes/mars-jupiter.md`
- `wiki/axes/mars-saturn.md`
- `wiki/axes/mars-uranus.md`
- `wiki/axes/mars-neptune.md`
- `wiki/axes/jupiter-saturn.md`
- `wiki/axes/jupiter-uranus.md`
- `wiki/axes/jupiter-neptune.md`
- `wiki/axes/saturn-uranus.md`
- `wiki/axes/saturn-neptune.md`
- `wiki/axes/uranus-neptune.md`
- `wiki/index.md`
- `wiki/log.md`

### Files To Read During Implementation

- `AGENTS.md`
- `tools/wiki_identity.py`
- `tools/wiki_pages.py`
- `tools/rebuild_index.py`
- `tools/lint_wiki.py`
- `tools/falis_source.py`
- `tools/ingest_falis.py`
- `wiki/axes/sun-moon.md`
- `wiki/axes/moon-mercury.md`
- `wiki/activations/sun-moon-equals-venus.md`

### File Responsibilities

- `tools/carter_source.py`
  - parse Carter pair chapters into structured pair-level models with exact page references and three aspect families
- `tools/ingest_carter.py`
  - merge Carter source entries into existing axis pages idempotently and write the Carter source page
- `tests/tools/test_carter_source.py`
  - prove the parser can extract section bodies, example groups, and pair normalization from the PDF
- `tests/wiki/test_carter_axis_ingest.py`
  - prove Carter lands only where intended in the live wiki and that rerendering does not duplicate entries
- `wiki/axes/*.md`
  - preserve current midpoint-derived material while gaining one explicit Carter source entry per covered pair
- `wiki/sources/charles-carter-the-astrological-aspects.md`
  - provenance hub for the Carter source and its collapse strategy
- `wiki/index.md`
  - refreshed by `tools/rebuild_index.py`
- `wiki/log.md`
  - append-only record of pilot and full Carter ingest

## Chunk 1: Carter Parser Pilot

### Task 1: Build The Carter Pair Parser For A Sun/Moon Pilot

**Files:**
- Create: `tools/carter_source.py`
- Test: `tests/tools/test_carter_source.py`

- [ ] **Step 1: Write the failing parser tests**

```python
from pathlib import Path

from tools.carter_source import generate_models


SOURCE_PATH = Path("Stellar Influences Vault/Book_2000_Charles Carter_The Astrological Aspects.pdf")


def test_carter_parser_extracts_sun_moon_families():
    blocks = generate_models(SOURCE_PATH, limit_pairs=[("Sun", "Moon")])
    block = blocks[0]
    assert (block.factor_a, block.factor_b) == ("Sun", "Moon")
    assert "good health supported by a strong constitution" in block.harmonious_text
    assert "The Conjunction" not in block.harmonious_text
    assert "It is thought by many that even bad aspects are to be preferred" in block.inharmonious_text


def test_carter_parser_extracts_family_grouped_examples():
    blocks = generate_models(SOURCE_PATH, limit_pairs=[("Moon", "Mercury")])
    block = blocks[0]
    assert "Kant" in block.harmonious_examples
    assert "Baden-Powell" in block.conjunction_examples
    assert "Shelley" in block.inharmonious_examples
```

- [ ] **Step 2: Run the parser tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_carter_source.py -v`

Expected: FAIL with import errors or missing parser symbols for `tools.carter_source`

- [ ] **Step 3: Write the minimal parser implementation**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CarterAxisBlock:
    factor_a: str
    factor_b: str
    page: int
    heading: str
    harmonious_text: str
    conjunction_text: str
    inharmonious_text: str
    harmonious_examples: str
    conjunction_examples: str
    inharmonious_examples: str
```

Implementation notes:
- Parse only the nine Carter bodies: `Sun`, `Moon`, `Mercury`, `Venus`, `Mars`, `Jupiter`, `Saturn`, `Uranus`, `Neptune`.
- Normalize TOC and body headings like `ASPECTS OF THE MOON & MERCURY` and `ASPECTS OF THE SUN AND MOON` into canonical axis order.
- Respect the source's printed page numbers, not the zero-based PDF page index.
- Keep section extraction bounded by the explicit all-caps family headers and the `EXAMPLES FOR <PAIR>` block.
- Add a temporary `limit_pairs` argument only if it materially simplifies pilot-first testing; remove it later if it becomes dead code.

- [ ] **Step 4: Run the parser tests to verify they pass**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_carter_source.py -v`

Expected: PASS for `Sun/Moon` family extraction and `Moon/Mercury` example grouping

- [ ] **Step 5: Commit**

```bash
git add tools/carter_source.py tests/tools/test_carter_source.py
git commit -m "feat: add Carter aspect parser"
```

## Chunk 2: Pilot Merge Into One Axis Page

### Task 2: Implement An Idempotent Sun/Moon Carter Merge

**Files:**
- Create: `tools/ingest_carter.py`
- Create: `wiki/sources/charles-carter-the-astrological-aspects.md`
- Modify: `wiki/axes/sun-moon.md`
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`
- Test: `tests/wiki/test_carter_axis_ingest.py`

- [ ] **Step 1: Write the failing pilot ingest tests**

```python
from pathlib import Path

from tools.wiki_pages import load_page


def test_carter_source_page_exists():
    page = load_page(Path("wiki/sources/charles-carter-the-astrological-aspects.md"))
    assert page.meta["page_type"] == "source"


def test_sun_moon_axis_includes_carter_family_headings():
    page = load_page(Path("wiki/axes/sun-moon.md"))
    assert "### Charles Carter - The Astrological Aspects" in page.body
    assert "#### Harmonious Aspects" in page.body
    assert "#### The Conjunction" in page.body
    assert "#### Inharmonious Aspects" in page.body


def test_activation_pages_do_not_gain_carter_source_pages():
    page = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))
    assert "charles-carter-the-astrological-aspects" not in page.meta["source_pages"]
```

- [ ] **Step 2: Run the pilot ingest tests to verify they fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_carter_axis_ingest.py -v`

Expected: FAIL because the Carter source page and the Carter axis entry do not exist yet

- [ ] **Step 3: Write the minimal Carter ingest implementation for Sun/Moon**

```python
def render_carter_entry(block: CarterAxisBlock) -> str:
    return f"""### Charles Carter - The Astrological Aspects

- Source heading: `{block.heading}`
- Source starting page: `{block.page}`

#### Harmonious Aspects

{block.harmonious_text}

#### The Conjunction

{block.conjunction_text}

#### Inharmonious Aspects

{block.inharmonious_text}

#### Examples

- Harmonious: {block.harmonious_examples}
- The Conjunction: {block.conjunction_examples}
- Inharmonious: {block.inharmonious_examples}
"""
```

Implementation notes:
- Preserve the existing Witte/Falis/Ebertin text in `wiki/axes/sun-moon.md`; only append or replace the Carter block.
- Replace an existing Carter block if present instead of appending a second one.
- Add `charles-carter-the-astrological-aspects` to the axis page's `source_pages`.
- Set `framework_scope: comparative` if the page is not already comparative.
- Write a source page that explicitly says this is an aspect-based source intentionally collapsed into canonical axis pages.
- Append one pilot-specific entry to `wiki/log.md`.

- [ ] **Step 4: Run the pilot ingest, rebuild the index, and rerun the tests**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/ingest_carter.py --pairs Sun/Moon`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/wiki/test_carter_axis_ingest.py -v`

Expected:
- the Carter source page exists
- `wiki/axes/sun-moon.md` contains exactly one Carter entry with all three family headings
- activation page frontmatter remains unchanged

- [ ] **Step 5: Commit**

```bash
git add tools/ingest_carter.py tests/wiki/test_carter_axis_ingest.py wiki/sources/charles-carter-the-astrological-aspects.md wiki/axes/sun-moon.md wiki/index.md wiki/log.md
git commit -m "feat: add Carter Sun/Moon pilot ingest"
```

## Chunk 3: Expand From Pilot To Full Carter Coverage

### Task 3: Generalize The Parser And Ingest To All 36 Carter Pairs

**Files:**
- Modify: `tools/carter_source.py`
- Modify: `tools/ingest_carter.py`
- Modify: `tests/tools/test_carter_source.py`
- Modify: `tests/wiki/test_carter_axis_ingest.py`
- Modify:
  - `wiki/axes/sun-mercury.md`
  - `wiki/axes/sun-venus.md`
  - `wiki/axes/sun-mars.md`
  - `wiki/axes/sun-jupiter.md`
  - `wiki/axes/sun-saturn.md`
  - `wiki/axes/sun-uranus.md`
  - `wiki/axes/sun-neptune.md`
  - `wiki/axes/moon-mercury.md`
  - `wiki/axes/moon-venus.md`
  - `wiki/axes/moon-mars.md`
  - `wiki/axes/moon-jupiter.md`
  - `wiki/axes/moon-saturn.md`
  - `wiki/axes/moon-uranus.md`
  - `wiki/axes/moon-neptune.md`
  - `wiki/axes/mercury-venus.md`
  - `wiki/axes/mercury-mars.md`
  - `wiki/axes/mercury-jupiter.md`
  - `wiki/axes/mercury-saturn.md`
  - `wiki/axes/mercury-uranus.md`
  - `wiki/axes/mercury-neptune.md`
  - `wiki/axes/venus-mars.md`
  - `wiki/axes/venus-jupiter.md`
  - `wiki/axes/venus-saturn.md`
  - `wiki/axes/venus-uranus.md`
  - `wiki/axes/venus-neptune.md`
  - `wiki/axes/mars-jupiter.md`
  - `wiki/axes/mars-saturn.md`
  - `wiki/axes/mars-uranus.md`
  - `wiki/axes/mars-neptune.md`
  - `wiki/axes/jupiter-saturn.md`
  - `wiki/axes/jupiter-uranus.md`
  - `wiki/axes/jupiter-neptune.md`
  - `wiki/axes/saturn-uranus.md`
  - `wiki/axes/saturn-neptune.md`
  - `wiki/axes/uranus-neptune.md`
- Modify: `wiki/sources/charles-carter-the-astrological-aspects.md`
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

- [ ] **Step 1: Extend the failing tests from pilot to full coverage**

```python
def test_carter_parser_extracts_all_36_pairs():
    blocks = generate_models(Path("Stellar Influences Vault/Book_2000_Charles Carter_The Astrological Aspects.pdf"))
    assert len(blocks) == 36


def test_full_ingest_updates_representative_axes():
    for slug in ["moon-mercury", "venus-neptune", "saturn-neptune"]:
        page = load_page(Path("wiki/axes") / f"{slug}.md")
        assert "### Charles Carter - The Astrological Aspects" in page.body
```

- [ ] **Step 2: Run the focused Carter tests to verify the full-coverage assertions fail**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_carter_source.py tests/wiki/test_carter_axis_ingest.py -v`

Expected: FAIL because only the pilot pair is ingested

- [ ] **Step 3: Generalize the parser and ingest script to all 36 pairs**

```python
CARTER_PAIRS = [
    ("Sun", "Moon"),
    ("Sun", "Mercury"),
    ...
    ("Uranus", "Neptune"),
]
```

Implementation notes:
- Keep pair order canonical and aligned with existing `normalize_axis`.
- Ensure the ingest script only touches the 36 Carter-covered standard-planet axis pages listed above.
- Do not modify any axis page involving `Pluto`, `Node`, `Asc`, `MC`, `Aries`, or Hamburg transneptunians.
- Rebuild the Carter source page counts and coverage notes from the parsed models rather than hardcoding them.
- Keep the Carter entry rendering identical across all touched axis pages.

- [ ] **Step 4: Run the full Carter ingest and focused Carter tests**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/ingest_carter.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_carter_source.py tests/wiki/test_carter_axis_ingest.py -v`

Expected:
- parser returns 36 blocks
- the Carter source page reflects 36 covered pair chapters
- all representative axis pages contain a single Carter entry

- [ ] **Step 5: Commit**

```bash
git add tools/carter_source.py tools/ingest_carter.py tests/tools/test_carter_source.py tests/wiki/test_carter_axis_ingest.py wiki/sources/charles-carter-the-astrological-aspects.md wiki/axes/sun-moon.md wiki/axes/sun-mercury.md wiki/axes/sun-venus.md wiki/axes/sun-mars.md wiki/axes/sun-jupiter.md wiki/axes/sun-saturn.md wiki/axes/sun-uranus.md wiki/axes/sun-neptune.md wiki/axes/moon-mercury.md wiki/axes/moon-venus.md wiki/axes/moon-mars.md wiki/axes/moon-jupiter.md wiki/axes/moon-saturn.md wiki/axes/moon-uranus.md wiki/axes/moon-neptune.md wiki/axes/mercury-venus.md wiki/axes/mercury-mars.md wiki/axes/mercury-jupiter.md wiki/axes/mercury-saturn.md wiki/axes/mercury-uranus.md wiki/axes/mercury-neptune.md wiki/axes/venus-mars.md wiki/axes/venus-jupiter.md wiki/axes/venus-saturn.md wiki/axes/venus-uranus.md wiki/axes/venus-neptune.md wiki/axes/mars-jupiter.md wiki/axes/mars-saturn.md wiki/axes/mars-uranus.md wiki/axes/mars-neptune.md wiki/axes/jupiter-saturn.md wiki/axes/jupiter-uranus.md wiki/axes/jupiter-neptune.md wiki/axes/saturn-uranus.md wiki/axes/saturn-neptune.md wiki/axes/uranus-neptune.md wiki/index.md wiki/log.md
git commit -m "feat: ingest full Carter aspect corpus"
```

## Chunk 4: Final Verification

### Task 4: Verify That Carter Stayed Confined To Axis Pages

**Files:**
- Modify: `tests/wiki/test_carter_axis_ingest.py`
- Modify: `wiki/log.md`
- Modify: `wiki/index.md` if rebuild changes it

- [ ] **Step 1: Add a final guard test against accidental Carter bleed**

```python
def test_carter_does_not_touch_factors_or_activations():
    activation = load_page(Path("wiki/activations/sun-moon-equals-venus.md"))
    factor = load_page(Path("wiki/factors/sun.md"))
    assert "charles-carter-the-astrological-aspects" not in activation.meta["source_pages"]
    assert "Charles Carter - The Astrological Aspects" not in factor.body
```

- [ ] **Step 2: Run the full verification suite**

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests -v`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`

Run: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`

Expected:
- all tests PASS
- the linter still passes after the rebuild
- Carter remains confined to axis pages and the Carter source page

- [ ] **Step 3: Append the final Carter ingest verification entry to the log**

Log entry should record:
- date
- source used
- 36 pair chapters collapsed into axis pages
- pilot-first approach completed
- tests run
- lint and index status

- [ ] **Step 4: Inspect the diff for accidental scope growth**

Run: `git diff --stat HEAD~1..HEAD`

Expected:
- only the Carter parser, ingest script, tests, Carter source page, listed axis pages, index, and log changed
- no edits under `Stellar Influences Vault/`
- no activation, triad, or factor pages changed

- [ ] **Step 5: Commit**

```bash
git add tests/wiki/test_carter_axis_ingest.py wiki/log.md wiki/index.md
git commit -m "chore: verify Carter axis-only ingest"
```

## Execution Notes

- Use `apply_patch` for all manual edits.
- Use the exact Python interpreter required by the repo instructions:
  - `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`
- Do not run smoke tests intended for the MADHEX codebase; this repo is not MADHEX.
- Keep the raw source PDF untouched.
- Do not refactor the existing midpoint schema, activation pages, or factor-page comparative work while implementing Carter.
- If Carter parsing reveals OCR or page-boundary ambiguity, fix it in `tools/carter_source.py`; do not solve it by hand-editing multiple axis pages.

## Definition Of Done

The Carter ingest is done when all of the following are true:

- `tools/carter_source.py` and `tools/ingest_carter.py` exist and are rerunnable.
- `tests/tools/test_carter_source.py` and `tests/wiki/test_carter_axis_ingest.py` pass.
- all 36 Carter-covered standard-planet pair pages contain exactly one Carter source entry.
- each Carter entry preserves `Harmonious Aspects`, `The Conjunction`, `Inharmonious Aspects`, and family-grouped examples.
- `wiki/sources/charles-carter-the-astrological-aspects.md` exists and accurately describes the collapse strategy.
- no activation pages, triad hubs, or factor pages are changed by the Carter ingest.
- `pytest`, `tools/lint_wiki.py`, and `tools/rebuild_index.py` pass from the required Python environment.
