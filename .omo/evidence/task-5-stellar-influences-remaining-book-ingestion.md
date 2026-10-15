# Task 5 - Hans Niggemann sample-manifest decision

## Manifest output summary

The existing probe was run for the required three samples:

- `Meridian plus Venus`
- `Moon plus Saturn`
- `Poseidon plus Poseidon`

The exact command requested by the handoff failed before PDF parsing because the script directory `.omo` became `sys.path[0]`, so the repo-local `tools` package was not importable. The probe was then rerun without editing it by adding the repository root to `PYTHONPATH`.

### Exact requested command output

Command:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B .omo/task_5_niggemann_probe.py
```

Output:

```text
Traceback (most recent call last):
  File "W:\Stellar Influences\.omo\task_5_niggemann_probe.py", line 24, in <module>
    from tools.wiki_identity import normalize_axis
ModuleNotFoundError: No module named 'tools'
```

### Parser-backed rerun output

Command:

```powershell
$env:PYTHONPATH=(Get-Location).Path; & 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' -B .omo/task_5_niggemann_probe.py
```

Output:

```text
# Hans Niggemann Sample Manifest
- pdf_path: W:\books references etc\!master list astro\midpoints - Hans Niggemann - Rules for planetary pictures.pdf
- page_count: 283
- abbreviation_map_entries: 44

## Meridian plus Venus
- pdf_page: 33
- raw_heading: Mandlan plus Vetiu ^
- canonical_axis_helper_display: Venus/MC
- canonical_axis_slug: venus-mc
- summary_line_count: 2
- parsed_entry_rows: 23
- expected_activation_rows: 20
- unknown_or_ocr_broken_tokens: 2
  - '1' at row 12 -> expected Pluto
  - 'Za' at row 15 -> expected Zeus
- token_conflicts: 0
- missing_expected_rows: 0
- extra_rows: 3
  - 'Note?': all experience in life comes over the consc'o's. Therefore the planet Keroary th
  - 'his': position m the horoscope is equ-sl* itnpvrtem, as the porsor.el pc.nts. Very mut
  - 'Hades': . Mercury and hades causes drstc way cf expre s5on, t.i nkmg, ml stakes, superfi
- first_rows:
  - row 1: token='Ar', mapped=Vernal Point, expected_by_order=Vernal Point, text=Popularity. General inclinations (preferenoes), To send nwch love to the general publie.
  - row 2: token='Su', mapped=Sun, expected_by_order=Sun, text=Self-love, vanity.
  - row 3: token='As', mapped=Asc, expected_by_order=Asc, text=To be in love with another person, to give preference to a certain place, to be in or longing for that place. 
  - row 4: token='Mo', mapped=Moon, expected_by_order=Moon, text=Preference for female persons. When equals Aries, a "skirt chaser".
  - row 5: token='No', mapped=Node, expected_by_order=Node, text=To bestow affection on somebody. To make acquamcence easily.

## Moon plus Saturn
- pdf_page: 115
- raw_heading: loon pxus ^.aturn
- canonical_axis_helper_display: Moon/Saturn
- canonical_axis_slug: moon-saturn
- summary_line_count: 4
- parsed_entry_rows: 19
- expected_activation_rows: 20
- unknown_or_ocr_broken_tokens: 8
  - 'To' at row 1 -> expected MC
  - 'sc' at row 4 -> expected Asc
  - '1o' at row 5 -> expected Node
  - 'to' at row 6 -> expected Mercury
  - 'Ye' at row 7 -> expected Venus
  - 'Ke' at row 11 -> expected Neptune
  - 'PI' at row 12 -> expected Pluto
  - 'r' at row 19 -> expected Vulcanus
- token_conflicts: 2
  - 'Ju' maps to Jupiter, but row order expects Sun
  - 'Vu' maps to Vulcanus, but row order expects Admetos
- missing_expected_rows: 1
  - Poseidon
- extra_rows: 0
- first_rows:
  - row 1: token='To', mapped=<unknown>, expected_by_order=MC, text=To retire, to be rn reserve. To keep distant� to be conservative, Man deserted by his wife. Mentally depressed
  - row 2: token='Ar', mapped=Vernal Point, expected_by_order=Vernal Point, text=La bonne people (classes), suffering, suppressed populace. Losses in the populace- The general happening in th
  - row 3: token='Ju', mapped=Jupiter, expected_by_order=Sun, text=The r.5&n s widow. Divorced wotian. Daily repeating hours of being alone. To be moody or depressed because of 
  - row 4: token='sc', mapped=<unknown>, expected_by_order=Asc, text=,sc Associating with country people, rustic surroundings. Acquaintance with widows or with the old, unfortunat
  - row 5: token='1o', mapped=<unknown>, expected_by_order=Node, text=Connections9 wnich overwhelmingly dominate the evening hours. Connection v/ith the sick and old. Separation of

## Poseidon plus Poseidon
- pdf_page: 283
- raw_heading: 255
- canonical_axis_helper_display: Poseidon/Poseidon
- canonical_axis_slug: poseidon-poseidon
- summary_line_count: 1
- parsed_entry_rows: 22
- expected_activation_rows: 21
- unknown_or_ocr_broken_tokens: 5
  - 'Spirit' at row 1 -> expected MC
  - 'Aso' at row 5 -> expected Moon
  - 'Ko' at row 7 -> expected Mercury
  - 'PI' at row 15 -> expected Cupido
  - 'Kx' at row 19 -> expected Apollon
- token_conflicts: 16
  - 'M' maps to MC, but row order expects Vernal Point
  - 'Ar' maps to Vernal Point, but row order expects Sun
  - 'Su' maps to Sun, but row order expects Asc
  - 'Mo' maps to Moon, but row order expects Node
  - 'Me' maps to Mercury, but row order expects Venus
  - 'Me' maps to Mercury, but row order expects Mars
  - 'Ma' maps to Mars, but row order expects Jupiter
  - 'Ju' maps to Jupiter, but row order expects Saturn
  - 'Sa' maps to Saturn, but row order expects Uranus
  - 'Ur' maps to Uranus, but row order expects Neptune
  - 'Ne' maps to Neptune, but row order expects Pluto
  - 'Cu' maps to Cupido, but row order expects Hades
  - 'Ha' maps to Hades, but row order expects Zeus
  - 'Ze' maps to Zeus, but row order expects Kronos
  - 'Ap' maps to Apollon, but row order expects Admetos
  - 'Ad' maps to Admetos, but row order expects Vulcanus
- missing_expected_rows: 0
- extra_rows: 1
  - 'Vu': Pride. Dignity, Self confidence. Arrogance, The power of the mind.
- first_rows:
  - row 1: token='Spirit', mapped=<unknown>, expected_by_order=MC, text=.. Idea.
  - row 2: token='M', mapped=MC, expected_by_order=Vernal Point, text=Ttw own spiritualization. The godly part in man.
  - row 3: token='Ar', mapped=Vernal Point, expected_by_order=Sun, text=Spirituality, Ideas.
  - row 4: token='Su', mapped=Sun, expected_by_order=Asc, text=The man who becomes spiritualized, who turns to spiritual things. Ghosts.
  - row 5: token='Aso', mapped=<unknown>, expected_by_order=Moon, text=To meet spiritual people, to cultivate their company. The spiritual in the environment.
```

## Decision

Decision: `held`

No product wiki doctrine was written. The manifest is not demonstrably reliable, so `wiki/sources/hans-niggemann-rules-for-planetary-pictures.md` was not created or updated and no factor, axis, activation, or triad pages were imported.

## Hold reasons

- `Meridian plus Venus` has a bad OCR heading (`Mandlan plus Vetiu ^`), 23 parsed rows for 20 expected activation rows, 2 unknown/OCR-broken tokens, and 3 extra rows. The extra rows show the parser is absorbing note/body text as activation rows.
- `Moon plus Saturn` has a bad OCR heading (`loon pxus ^.aturn`), only 19 parsed rows for 20 expected activation rows, 8 unknown/OCR-broken tokens, 2 row-order conflicts, and a missing `Poseidon` row.
- `Poseidon plus Poseidon` has a bad heading/page start (`255`), 22 parsed rows for 21 expected activation rows, 5 unknown/OCR-broken tokens, 16 row-order conflicts, and 1 extra row. The first parsed row (`Spirit`) appears to be summary/body text, shifting the activation alignment.
- The exact requested command currently fails without `PYTHONPATH`, so the sample probe is not directly runnable as handed off.

## Verification outputs

Final verification commands were run after cleanup and evidence writing. Outputs are recorded below.

### `git diff --name-only -- wiki`

```text

```

### `git status --short -- wiki/sources/hans-niggemann-rules-for-planetary-pictures.md wiki/factors wiki/axes wiki/activations wiki/triads .omo/evidence/task-5-stellar-influences-remaining-book-ingestion.md .omo/task_5_niggemann_probe.py .omo/task_5_niggemann_page115.png`

```text
?? .omo/evidence/task-5-stellar-influences-remaining-book-ingestion.md
```

### Lint

`tools/lint_wiki.py` was not run because the source was held and no product wiki files were changed.

## Cleanup receipt

Cleanup command:

```powershell
Get-ChildItem -LiteralPath .omo -Filter 'task_5_niggemann*' -File | ForEach-Object { Write-Output $_.FullName; Remove-Item -LiteralPath $_.FullName }
```

Output:

```text
W:\Stellar Influences\.omo\task_5_niggemann_page115.png
W:\Stellar Influences\.omo\task_5_niggemann_probe.py
```

Leftover check:

```powershell
Get-ChildItem -LiteralPath .omo -Filter 'task_5_niggemann*' -File | Select-Object -ExpandProperty FullName
```

Output:

```text

```

## Unresolved schema/parser decisions

- Decide how Hans headings should be detected and validated before row extraction, especially when OCR produces headings such as `Mandlan plus Vetiu ^`, `loon pxus ^.aturn`, or a page number (`255`) instead of the expected heading.
- Decide whether OCR token normalization may correct source-specific variants such as `Za`/`Ze`, `PI`/`Pl`, `Aso`/`Asc`, `1o`/`No`, or whether those must remain hard failures until verified against page images.
- Add a parser-backed boundary between activation rows and notes/body paragraphs. Page 33 shows note text being parsed as activation rows.
- Resolve how duplicate-factor axes such as `Poseidon/Poseidon` should be validated against source row counts, including whether summary terms like `Spirit` are body text, heading text, or a row label.
- Make the probe directly runnable from the repo root without requiring an external `PYTHONPATH` override if it is kept for future work.
