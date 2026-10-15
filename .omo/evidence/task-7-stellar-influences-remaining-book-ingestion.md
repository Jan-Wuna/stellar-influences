# Task 7 - Uranian Master-Lexicon Decision/Import

## Decision

- Decision: `held`
- Date: 2026-06-20
- Source: Uranian Astrology Master-Lexicon probe artifacts
- Potential source page: `wiki/sources/uranian-astrology-master-lexicon.md`
- Product wiki changes: none

## Manifest Summary

Existing probe artifacts reported:

- `parsed_current_schema_rows`: `6506`
- `unique_activation_pages`: `2195`
- `rows_with_existing_activation_page`: `6403`
- `duplicate_witte_page_rows`: `6402`
- `rows_without_witte_source`: `104`
- `rejected_formula_like_rows`: `17830`
- Top rejected-token reasons:
  - `unknown:a`: `1383`
  - `unknown:ho`: `883`
  - `unknown:lr`: `836`
  - `unknown:llo`: `789`
  - `unknown:lla`: `678`
  - `unknown:h`: `571`
  - `unknown:he`: `475`
  - `unknown:za`: `389`

## Sample Highlights

- Sample rows contained many `~` keyword placeholders, so the captured text was not clean enough for product wiki doctrine.
- Sample contexts were corrupted by OCR/glyph errors, making source-native wording unreliable without page-by-page manual repair.
- The large overlap with existing activation pages means the current-schema rows mostly behave as duplicate reverse-lexicon references rather than distinct new doctrine.
- `6402` rows were duplicate Witte-backed page rows, while only `104` parsed rows lacked Witte source backing.

## Rejected-Token Evidence

The reject volume is high relative to accepted rows: `17830` formula-like rows were rejected versus `6506` parsed current-schema rows.

The top rejects are not minor edge cases. They include high-volume unknown tokens such as `a`, `ho`, `lr`, `llo`, `lla`, `h`, `he`, and `za`, which indicates unresolved OCR/token-boundary problems rather than a small missing abbreviation table.

## `Ve+Vu-Ju` Search Result

- Exact `Ve+Vu-Ju` matches: `2`
- Both exact matches normalized to `Venus/Vulcanus = Jupiter`.
- Both exact matches were Witte-backed.

This does not establish a reliable, distinct current-schema contribution from the Master-Lexicon; it confirms the specific requested family is already represented by existing Witte-backed activation content.

## Hold Reasons

1. The decision gate defaults to hold unless the source proves reliable, distinct current-schema contribution. The existing manifest does not meet that gate.
2. `6403` of `6506` parsed rows point to existing activation pages, and `6402` rows are duplicate Witte-backed page rows.
3. The reject surface is too large and too noisy for import: `17830` formula-like rows were rejected, with high-volume unknown tokens and probable OCR/glyph corruption.
4. Sample row text is not product-ready because many keywords contain `~` placeholders and corrupted contexts.
5. The targeted `Ve+Vu-Ju` check found only two exact rows, both already normalized to the existing Witte-backed `Venus/Vulcanus = Jupiter` activation.
6. Creating `wiki/sources/uranian-astrology-master-lexicon.md` would add a source shell without reliable imported doctrine and would not satisfy the distinct-contribution requirement.

## Verification Outputs

Final verification commands were run after evidence writing and cleanup. Outputs are recorded below.

### `git diff --name-only -- wiki`

```text

```

### `git status --short -- wiki/sources/uranian-astrology-master-lexicon.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-7-stellar-influences-remaining-book-ingestion.md`

```text
?? .omo/evidence/task-7-stellar-influences-remaining-book-ingestion.md
```

### Leftover check

Command:

```powershell
Get-ChildItem -LiteralPath .omo -Filter 'task_7_master_lexicon*' -Force
```

Output:

```text

```

### Lint

`tools/lint_wiki.py` was not run because the source was held and no product wiki files were changed.

## Cleanup Receipt

- Expected cleanup targets: `.omo/task_7_master_lexicon_manifest.json`, `.omo/task_7_master_lexicon_word_dump.txt`, `.omo/task_7_master_lexicon_probe.py`, `.omo/task_7_master_lexicon_inspect.py`, and `.omo/task_7_master_lexicon_page_*.png`.
- Cleanup command produced no output because no `.omo/task_7_master_lexicon*` files were present.
- The leftover check produced no output after cleanup.
- No product wiki files were written.

## Unresolved Parser/Schema Decisions

- Decide whether the Master-Lexicon should ever be represented as a held source/index artifact separate from canonical activation doctrine pages.
- Decide whether duplicate Witte-backed reverse-lexicon rows should be retained anywhere, or omitted to avoid noisy duplicate page references.
- Resolve high-volume unknown token classes before any future import attempt, especially `a`, `ho`, `lr`, `llo`, `lla`, `h`, `he`, and `za`.
- Decide whether `~` placeholder keywords and corrupted contexts can be repaired from page images, or whether they should remain an import blocker.
- Define an acceptance threshold for sources where most parsed current-schema rows already point to existing Witte-backed activation pages.

## Final Verification Addendum

Independent parent verification after worker shutdown:

```powershell
git diff --name-only -- wiki
```

Output: no output.

```powershell
git status --short -- wiki/sources/uranian-astrology-master-lexicon.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-7-stellar-influences-remaining-book-ingestion.md
```

Output:

```text
?? .omo/evidence/task-7-stellar-influences-remaining-book-ingestion.md
```

```powershell
Get-ChildItem -LiteralPath .omo -Filter 'task_7_master_lexicon*' -Force | Select-Object Name,Length
```

Output: no output.

Cleanup result: verified; no `.omo/task_7_master_lexicon*` files remain.
