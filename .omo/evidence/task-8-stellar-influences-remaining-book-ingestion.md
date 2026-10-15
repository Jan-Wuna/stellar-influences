# Task 8 Baker Decision Record

## Decision

Status: held

D.M. Baker, _Colloquialism_ is not imported in the current pass. The existing
manifests show zero decoded current-schema rows, unresolved glyph/font mapping,
and high contamination from non-formula material. No source page, factor page,
axis page, activation page, or triad page should be created from this evidence.

Potential source page, if later accepted: `wiki/sources/d-m-baker-colloquialism.md`

## Manifest Summary

Evidence source: existing manifests only; parser/probe scripts were not rerun.

From `.omo/task_8_baker_manifest.json`:

- `page_count`: 168
- `decoded_current_schema_rows`: 0
- `formula_like_lines`: 604
- `rejected_formula_like_rows`: 755
- Top reject reason: `out-of-schema` = 742
- `unknown_glyph_total`: 741
- `sign_house_aspect_contamination_count`: 720
- Font signal includes `Claregate2AstrologicalGlyphs` = 185 lines, plus OCR/font mixing.

From `.omo/task_8_baker_glyph_manifest.json`:

- `glyph_font_line_count`: 185
- `decoded_current_schema_rows`: 0
- Glyph rows by bucket: early 63, mid 60, late 62
- Top raw glyph characters include undecoded/noncanonical characters such as
  `×`, `Ô`, `„`, `¶`, `¹`, `˜`, `‡`, `Ê`, `p`, `z`, `¢`, and `•`.
- Sample rows across early, mid, and late pages all have blank
  `decoded_canonical_identity` and `target_wiki_page_exists: false`.

## Sample Highlights

Main manifest samples:

- PDF p. 84, keyword starts `make a virtue out of necessity, to`; raw formula
  `-`; decoded identity blank; target path blank; target exists false;
  reject reason `out-of-schema`.
- PDF p. 84, keyword starts `assurance double sure`; raw formula `/`; decoded
  identity blank; target exists false; contamination count 2; reject reason
  `out-of-schema`.
- PDF p. 166, keyword starts `Bond written agreement or pledge`; raw formula
  `=`; decoded identity blank; target exists false; reject reason
  `out-of-schema`.
- PDF p. 167, keyword starts `wry jest`; mixed glyph/OCR sample includes
  `Ê× Ê11 Í11 ÔÍ Ô10 ×10`; decoded identity blank; target exists false;
  contamination count 1; reject reason `out-of-schema`.

Glyph manifest samples:

- Early bucket, PDF p. 7: raw glyph formula `×`; colloquialism `Aquarius`;
  decoded canonical identity blank; target wiki page exists false.
- Early bucket, PDF p. 10: raw glyph formula `˜ × ˜`; colloquialism starts
  `alive and kicking, all`; decoded canonical identity blank; target wiki page
  exists false.
- Mid bucket, PDF p. 57: raw glyph formula `Þ ×`; colloquialism starts
  `great ovation, a`; decoded canonical identity blank; target wiki page exists
  false.
- Mid bucket, PDF p. 60: raw glyph formula `„ ×`; colloquialism starts
  `baton, but a torch`; decoded canonical identity blank; target wiki page
  exists false.
- Late bucket, PDF p. 114: raw glyph formula `„ ×`; colloquialism starts
  `put pen to paper, to`; decoded canonical identity blank; target wiki page
  exists false.
- Late bucket, PDF p. 119: raw glyph formula `˜ ×`; colloquialism starts
  `curtain) to be . . . let down by making a bell ring`; decoded canonical
  identity blank; target wiki page exists false.

## Hold Reasons

- The import gate requires decoded current-schema rows; both manifests report
  `decoded_current_schema_rows: 0`.
- The dominant extraction signal is not an importable activation/axis/factor
  identity under the current schema: 742 out-of-schema rejects and 755 rejected
  formula-like rows.
- `sign_house_aspect_contamination_count: 720` indicates that apparent formulas
  are heavily mixed with signs, houses, aspects, numerals, punctuation, and OCR
  artifacts.
- The glyph font rows are not safely mapped to canonical full-name factor
  identities. The top raw glyphs include noncanonical or undecoded characters,
  and sample rows from all page regions retain blank canonical identity fields.
- Creating `wiki/sources/d-m-baker-colloquialism.md` or canonical wiki entries
  now would imply a decoded source identity that the manifests do not support.

## Cleanup Receipt

The following temporary Baker artifacts were removed after this evidence file
captured their decision-level facts:

- `.omo/task_8_baker_manifest.json`
- `.omo/task_8_baker_glyph_manifest.json`
- `.omo/task_8_baker_probe.py`
- `.omo/task_8_baker_glyph_probe.py`

No `.omo/task_8_baker*` files remain after cleanup.

## Verification Outputs

Command:

```powershell
git diff --name-only -- wiki
```

Output:

```text
```

Command:

```powershell
git status --short -- wiki/sources/d-m-baker-colloquialism.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-8-stellar-influences-remaining-book-ingestion.md
```

Output:

```text
?? .omo/evidence/task-8-stellar-influences-remaining-book-ingestion.md
```

Command:

```powershell
Get-ChildItem -LiteralPath .omo -Filter 'task_8_baker*' -Force
```

Output:

```text
```

Lint was not run because no product wiki files were changed.

## Unresolved Parser/Schema Decisions

- Build or verify a Baker-specific glyph-font map before any import attempt.
- Decide how to distinguish real midpoint/factor formulas from sign, house,
  aspect, numeral, punctuation, and OCR contamination in this PDF.
- Decide whether Baker's colloquialism entries fit the V1 source scope of
  explicit combination formulas or require a separate noncanonical keyword/glyph
  reference model.
- Decide whether a source page should exist for a held source without canonical
  decoded entries; current decision keeps it absent.
- Define an acceptance threshold for future retries, at minimum nonzero decoded
  current-schema rows plus sampled rows with nonblank canonical identities and
  correct target wiki page resolution.
