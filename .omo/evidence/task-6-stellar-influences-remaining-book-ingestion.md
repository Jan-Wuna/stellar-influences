# Task 6 - Feist Reverse-Lexicon Decision/Import

## Decision

- Decision: `held`
- Date: 2026-06-20
- Source PDF: `W:/books references etc/!master list astro/planetary expression - Michael Feist - Lexicon for Planetary Pictures.pdf`
- Potential source page: `wiki/sources/michael-feist-lexicon-for-planetary-pictures.md`
- Product wiki changes: none

## Probe Run

Command:

```powershell
$env:PYTHONIOENCODING='utf-8'; & 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' -B .omo/task_6_feist_probe.py
```

Result: exit code `0`. UTF-8 console handling was sufficient; no probe code change was needed.

## Manifest Summary

- `parsed_current_schema_rows`: `37711`
- `unique_activation_pages`: `4616`
- `duplicate_witte_page_rows`: `37711`
- `rejected_formula_like_rows`: `1299`
- Top reject reasons:
  - `unknown:pi`: `1037`
  - `unknown:mi`: `45`
  - `unknown:vii`: `27`
  - `unknown:an`: `17`
  - `unknown:mr`: `13`
  - `unknown:p`: `12`
  - `unknown:mt`: `10`
  - `grammar`: `8`
  - `unknown:w`: `8`
  - `unknown:u`: `6`
  - `four-factor/out-of-schema`: `3`

## Sample Highlights

All sampled current-schema rows mapped to activation pages that already contain the Witte/Rudolph/Lefeldt source slug.

- p. 4: `MA+VU-AR` -> `Mars/Vulcanus = Vernal Point`; keyword: `sensitive point`; Witte page exists: `True`
- p. 4: `MA+VU-AR` -> `Mars/Vulcanus = Vernal Point`; keyword: `(climate ... extreme heat)`; Witte page exists: `True`
- p. 7: `Ne+Kr-Ha` -> `Neptune/Kronos = Hades`; keyword: `~ ruined by misfortune`; Witte page exists: `True`
- p. 7: `Ju+Cu-Ve` -> `Jupiter/Cupido = Venus`; keyword: `Balanced financial condition of a ~`; Witte page exists: `True`
- p. 7: `Ma+Ad-Cu` -> `Mars/Admetos = Cupido`; keyword: `Bankruptcies of ~`; Witte page exists: `True`
- p. 7: `Cu+Ap-Ma` -> `Cupido/Apollon = Mars`; keyword: `Business management of a~`; Witte page exists: `True`
- p. 13: `Sa+Ur-Ap` -> `Saturn/Uranus = Apollon`; keyword: `~ an approved method`; Witte page exists: `True`
- p. 13: `Su+Ad-Ne` -> `Sun/Admetos = Neptune`; keyword: `~ed estate`; Witte page exists: `True`

Rejected sample rows included obvious false positives and unresolved tokens:

- p. 4: `done-for-you` skipped as `grammar`
- p. 6: `A+B-C` skipped as `unknown:a,b,c`
- p. 14: `ed-Ur+Pl-Ha` skipped as `four-factor/out-of-schema`
- p. 17: `AS+Mo-Pi` skipped as `unknown:pi`

## `Ve+Vu-Ju` Search Result

- `Ve+Vu-Ju` matches: `13`
- `Ve + Vu - Ju` matches: `0`
- `Vu-Ju` matches: `96`

Exact `Ve+Vu-Ju` family rows found by the probe:

- p. 39: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `wields`; Witte page exists: `True`
- p. 57: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `Optimism ~d by luck and success`; Witte page exists: `True`
- p. 191: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `tappiness of love`; Witte page exists: `True`
- p. 199: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `Great - of love`; Witte page exists: `True`
- p. 200: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `Joy ana ~ of a reunion`; Witte page exists: `True`
- p. 236: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `~ and happiness of a reunion`; Witte page exists: `True`
- p. 237: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `which one wields`; Witte page exists: `True`
- p. 254: `Ve+Vu-Ju` -> `Venus/Vulcanus = Jupiter`; keyword: `Great happiness of -`; Witte page exists: `True`

Existing page inspected: `wiki/activations/venus-vulcanus-equals-jupiter.md`.

- Existing Witte entry already covers: joy through power of attraction one wields; great happiness of love; optimism caused by luck and success; joy and happiness of a reunion.
- Feist hits reproduce the same language as a reverse lookup/index, with OCR loss in several keywords.

## Hold Reasons

1. The distinct-contribution requirement is not met: `37711` of `37711` parsed current-schema rows point to activation pages already backed by Witte/Rudolph/Lefeldt.
2. The source behaves like a reverse lexicon/index over already-ingested Witte-style meanings, not a separate activation doctrine source with clean standalone entries.
3. Parser confidence is not high enough for import: `1299` formula-like rejects remain, dominated by probable OCR/token ambiguity such as `Pi` versus `Pl`, plus false positives like `done-for-you` and schematic examples like `A+B-C`.
4. Exact PDF pages are available from extraction, but importing them would mostly add duplicate noisy page references rather than new canonical activation/axis content.
5. Acceptance criteria require reliable token grammar, five clean current-schema rows, exact pages, and a meaningful distinct contribution. The exact-page and row-count gates pass, but the token-reliability and distinct-contribution gates do not.

## Verification Outputs

Held verification after probe cleanup and evidence write:

```powershell
git diff --name-only -- wiki
```

Output: no output.

```powershell
git status --short -- wiki/sources/michael-feist-lexicon-for-planetary-pictures.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-6-stellar-influences-remaining-book-ingestion.md .omo/task_6_feist_probe.py
```

Output:

```text
?? .omo/evidence/task-6-stellar-influences-remaining-book-ingestion.md
```

## Cleanup Receipt

- Deleted `.omo/task_6_feist_probe.py`.
- `Get-ChildItem -LiteralPath '.omo' -Filter 'task_6_feist_*' | Select-Object -ExpandProperty Name` returned no output after cleanup.
- No `.omo/task_6_feist_*` temp outputs remain.

## Unresolved Parser/Schema Decisions

- Decide whether Feist should ever be represented as a source page when held as a reverse lexicon rather than ingested into canonical pages.
- Decide whether duplicate reverse-index page references are useful as a source companion/index artifact, separate from activation doctrine pages.
- Resolve token ambiguity before any future import, especially high-volume `Pi` hits that may be OCR for `Pl` and other unknowns such as `Mi`, `Mr`, `Mt`, `An`, and `Vii`.
- Decide whether future parsing should exclude introductory schematic examples and prose hyphen compounds before formula tokenization.
