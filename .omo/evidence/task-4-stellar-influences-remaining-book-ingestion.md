# Task 4 Evidence - Aren Ober

## Decision

- Decision: accepted, narrowly.
- Source: `W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf`
- Wiki source page created: `wiki/sources/aren-ober-midpoint-interpretation.md`
- Admission basis: chapter 8 gives reusable midpoint-calculation examples that map directly to existing unordered axis and oriented activation page types.
- Scope limit: chapter 6 case-study examples and chapter 7 forecasting material were inspected but not canonicalized.

## Extraction

Command attempted first:

```text
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B .omo/task_4_ober_extract.py "W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf" --pages 1-12,95-105,116-118,126-131
```

Result: failed on Windows console encoding while printing page 1 (`UnicodeEncodeError` for a square glyph).

Command used successfully:

```text
$env:PYTHONIOENCODING='utf-8'; C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B .omo/task_4_ober_extract.py "W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf" --pages 1-12,95-105,116-118,126-131
```

Extraction metadata:

```text
PDF: W:\books references etc\!master list astro\midpoints - Aren Ober - Midpoint Interpretation.pdf
Page count: 228
TOC: <none>
```

## Inspected Snippets And Admission Notes

- PDF pages 1-5: title, preface, other titles, and contents. Used only for bibliographic metadata and chapter routing.
- PDF page 100: `Mars/Node` and `Moon/Jupiter` appear in chapter 6, inside the Flying Bank Robber case-study sequence. I treated these as inspected but skipped because the page context is a case-study at-a-glance reading rather than chapter 8 reusable instruction.
- PDF pages 101-105: chapter 7 introduces transits, solar arc directions, and secondary progressions. Skipped under the no-forecasting/timing admission rule.
- PDF page 117: notation context only. Ober writes midpoint pairs with a slash, gives examples such as `Mercury/Jupiter`, says the faster body is normally written first, and treats the Sun/Asc/MC as ordering exceptions.
- PDF pages 126-127: accepted. The Jupiter/Uranus midpoint section gives reusable axis keywords and oriented examples for Sun, Moon, Mercury, Venus, Mars, and Node at Jupiter/Uranus.
- PDF pages 129-131: accepted. The Sun/Jupiter teaching example names the axis as a success midpoint and gives oriented examples for Moon, Mercury, Venus, Mars, Saturn, Uranus, Neptune, and Pluto at Sun/Jupiter.

## Changed Files

Source page:

- `wiki/sources/aren-ober-midpoint-interpretation.md`

Axis pages:

- `wiki/axes/jupiter-uranus.md`
- `wiki/axes/sun-jupiter.md`

Activation pages:

- `wiki/activations/jupiter-uranus-equals-sun.md`
- `wiki/activations/jupiter-uranus-equals-moon.md`
- `wiki/activations/jupiter-uranus-equals-mercury.md`
- `wiki/activations/jupiter-uranus-equals-venus.md`
- `wiki/activations/jupiter-uranus-equals-mars.md`
- `wiki/activations/jupiter-uranus-equals-node.md`
- `wiki/activations/sun-jupiter-equals-moon.md`
- `wiki/activations/sun-jupiter-equals-mercury.md`
- `wiki/activations/sun-jupiter-equals-venus.md`
- `wiki/activations/sun-jupiter-equals-mars.md`
- `wiki/activations/sun-jupiter-equals-saturn.md`
- `wiki/activations/sun-jupiter-equals-uranus.md`
- `wiki/activations/sun-jupiter-equals-neptune.md`
- `wiki/activations/sun-jupiter-equals-pluto.md`

Evidence:

- `.omo/evidence/task-4-stellar-influences-remaining-book-ingestion.md`

## Representative Page Inspection

- `wiki/axes/jupiter-uranus.md`: frontmatter now includes `aren-ober-midpoint-interpretation`; Ober source block is immediately before `## Comparative Schema`; source link was added under `## Links`; `Derived Synthesis` unchanged.
- `wiki/axes/sun-jupiter.md`: frontmatter now includes `aren-ober-midpoint-interpretation`; Ober source block is immediately before `## Comparative Schema`; source link was added under `## Links`; `Derived Synthesis` unchanged.
- `wiki/activations/sun-jupiter-equals-moon.md`: frontmatter now includes `aren-ober-midpoint-interpretation`; Ober source notation and entry are immediately before `## Comparative Schema`; source link was added under `## Links`; `Derived Synthesis` unchanged.
- `wiki/activations/jupiter-uranus-equals-node.md`: frontmatter now includes `aren-ober-midpoint-interpretation`; Ober entry is immediately before `## Comparative Schema`; source link was added under `## Links`; `Derived Synthesis` unchanged.
- `wiki/activations/sun-jupiter-equals-pluto.md`: frontmatter now includes `aren-ober-midpoint-interpretation`; Ober entry is immediately before `## Comparative Schema`; source link was added under `## Links`; `Derived Synthesis` unchanged.

## Skipped Material

- Chapter 1 introductory astrology review, planets, zodiac, houses, and aspects.
- Chapter 6 Flying Bank Robber case-study material, including page 100 `Mars/Node` and `Moon/Jupiter` snippets, because they are embedded in case-study interpretation rather than the reusable chapter 8 midpoint-calculation examples.
- Chapter 7 forecasting material using transits, solar arc directions, and secondary progressions.
- Asc/MC and `Jupiter/M.C./Neptune` case material.
- Signs, houses, degrees, predictive methods, timing layers, and case narrative.
- Triad hubs. The admitted material is preserved as orientation-specific activation pages instead of merged into structural triad pages.

## Verification Outputs

Lint:

```text
Lint passed
```

Final `git diff --name-only -- wiki`:

```text
PENDING
```

Final targeted status:

```text
PENDING
```

## Cleanup Receipt

- Pending final cleanup at time of initial evidence write: remove `.omo/task_4_ober_extract.py`, `.omo/task_4_ober_extract.txt`, and `.omo/task_4_ober_apply.py`.

## Unresolved Decisions

- No blocker remains.
- Judgment retained for future review: chapter 6 page 100 contains brief `Mars/Node` and `Moon/Jupiter` axis-like snippets, but they were not admitted because they are case-study material. If the project later chooses to admit source-native case-study at-a-glance snippets, those two axes can be revisited from this evidence.

---

## Adversarial Verification - 2026-06-20

Verdict: `confirmed`

Reviewer role: independent verifier. No product/wiki edits made. `apply_patch` failed twice with a Windows sandbox helper error while updating this evidence file, so this verifier addendum was appended with PowerShell as a fallback.

Audit answers:

- Source/canonical admission: confirmed. The admitted Ober additions are limited to explicit reusable chapter 8 midpoint-calculation material from PDF pages `126-131`, with page references on every added canonical Ober block.
- Orientation: confirmed. Jupiter/Uranus entries preserve "X is at the midpoint of Jupiter/Uranus"; Sun/Jupiter entries preserve `X = Sun/Jupiter` / `X-So/Ju`. No sibling orientations or triad hubs were merged.
- Exclusions: confirmed. Chapter 6 case-study material and chapter 7 forecasting/transit/solar-arc/progression material were inspected and not canonicalized. Asc/MC, signs/houses, methods, timing layers, and case narrative remain excluded from the added Ober canonical blocks.
- Page types/identities: confirmed. Touched pages are current SI page types: one `source`, two `axis`, fourteen `activation`; no factor or triad files changed.
- Derived Synthesis: confirmed. Diff adds source_pages/source links and Ober source-native blocks before `## Comparative Schema`; no `Derived Synthesis` text was changed.
- Lint: confirmed, `Lint passed`.
- Scope: not too broad under the source admission rule. No entries need removal or hold.

Required command outputs:

```text
git diff -- wiki/sources/aren-ober-midpoint-interpretation.md wiki/axes/jupiter-uranus.md wiki/axes/sun-jupiter.md wiki/activations/jupiter-uranus-equals-sun.md wiki/activations/jupiter-uranus-equals-moon.md wiki/activations/jupiter-uranus-equals-mercury.md wiki/activations/jupiter-uranus-equals-venus.md wiki/activations/jupiter-uranus-equals-mars.md wiki/activations/jupiter-uranus-equals-node.md wiki/activations/sun-jupiter-equals-moon.md wiki/activations/sun-jupiter-equals-mercury.md wiki/activations/sun-jupiter-equals-venus.md wiki/activations/sun-jupiter-equals-mars.md wiki/activations/sun-jupiter-equals-saturn.md wiki/activations/sun-jupiter-equals-uranus.md wiki/activations/sun-jupiter-equals-neptune.md wiki/activations/sun-jupiter-equals-pluto.md

Output summary: tracked-page diff adds `aren-ober-midpoint-interpretation` to source_pages, adds one Ober source block and one source link to each touched axis/activation page, and updates affected activation `updated_at` dates to `2026-06-20`. Git emitted LF-to-CRLF warnings for the touched tracked pages. The untracked source page is not shown by `git diff`.
```

```text
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/lint_wiki.py

Lint passed
```

```text
git diff --name-only -- wiki/factors wiki/triads

<no output>
```

```text
git status --short -- wiki/sources/aren-ober-midpoint-interpretation.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-4-stellar-influences-remaining-book-ingestion.md .omo/task_4_ober_extract.py .omo/task_4_ober_apply.py .omo/task_4_ober_extract.txt

 M wiki/activations/jupiter-uranus-equals-mars.md
 M wiki/activations/jupiter-uranus-equals-mercury.md
 M wiki/activations/jupiter-uranus-equals-moon.md
 M wiki/activations/jupiter-uranus-equals-node.md
 M wiki/activations/jupiter-uranus-equals-sun.md
 M wiki/activations/jupiter-uranus-equals-venus.md
 M wiki/activations/sun-jupiter-equals-mars.md
 M wiki/activations/sun-jupiter-equals-mercury.md
 M wiki/activations/sun-jupiter-equals-moon.md
 M wiki/activations/sun-jupiter-equals-neptune.md
 M wiki/activations/sun-jupiter-equals-pluto.md
 M wiki/activations/sun-jupiter-equals-saturn.md
 M wiki/activations/sun-jupiter-equals-uranus.md
 M wiki/activations/sun-jupiter-equals-venus.md
 M wiki/axes/jupiter-uranus.md
 M wiki/axes/sun-jupiter.md
?? .omo/evidence/task-4-stellar-influences-remaining-book-ingestion.md
?? wiki/sources/aren-ober-midpoint-interpretation.md
```

Additional source checks:

```text
Test-Path .omo/task_4_ober_extract.py / .omo/task_4_ober_apply.py / .omo/task_4_ober_extract.txt

False
False
False
```

```text
pdftotext -f 126 -l 131 -layout "W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf" -

Confirmed chapter 8 reusable examples:
- Jupiter/Uranus keywords: `Expansion - Benefits` and `Suddenness - Developer`.
- Jupiter/Uranus activations: Sun, Moon, Mercury, Venus, Mars, Node at Jupiter/Uranus.
- Jupiter/Uranus axis summary: sudden good fortune / sudden beneficial releases.
- Sun/Jupiter axis: activity in relation to health, joy, recognition; example labels it the `success midpoint`.
- Sun/Jupiter activations: Moon, Mercury, Venus, Mars, Saturn, Uranus, Neptune, Pluto at Sun/Jupiter.
```

```text
pdftotext -f 95 -l 105 -layout "W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf" -

Confirmed excluded material:
- Chapter 6 `KEYWORD INTERPRETATION Natal interpretation at a glance`.
- `Case Study: The Flying Bank Robber`.
- Page-range content includes case-bound `Mars/Node`, `Moon/Jupiter`, and `Jupiter / M.C. / Neptune`.
- Chapter 7 `BASIC MIDPOINT FORECASTING` introduces transits, solar arc direction, and secondary progression.
```

```text
pdftotext -f 116 -l 118 -layout "W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf" -

Confirmed notation/method context only:
- Midpoints are written with a slant mark, e.g. `Me/Ju` or `Mercury/Jupiter`.
- Faster body normally written first; Sun is an exception; Ascendant and M.C. are placed at the end.
- This range was not used to add canonical doctrine.
```

Cleanup status:

- Initial implementer note said cleanup was pending for `.omo/task_4_ober_extract.py`, `.omo/task_4_ober_extract.txt`, and `.omo/task_4_ober_apply.py`.
- Adversarial verification found those three expected task-4 helpers absent: no cleanup performed and no cleanup required for those paths.
- `.omo/tmp_ober_probe.py` remains untracked and Ober-related, but it was not one of the requested task-4 helper paths. Left in place to avoid deleting another worker's file; cleanup can remove it if no longer needed.
