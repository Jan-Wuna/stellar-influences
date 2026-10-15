# Factor review verification — 2026-10-15

All 23 assigned factor pages were fully read by their owning reviewers and revised. Coverage is complete for `assignments/factors-001.json` through `factors-007.json`: 23 reviewed, 23 changed, 0 unchanged, 0 unreviewed. The seven JSONL ledgers contain exactly one page-specific record per assignment, with no omissions or duplicates.

| Assignment | Reviewed | Changed | Unchanged | Pages with unresolved items | Unresolved issue records |
| --- | ---: | ---: | ---: | ---: | ---: |
| factors-001 | 4 | 4 | 0 | 3 | 10 |
| factors-002 | 4 | 4 | 0 | 4 | 8 |
| factors-003 | 3 | 3 | 0 | 3 | 8 |
| factors-004 | 3 | 3 | 0 | 3 | 15 |
| factors-005 | 3 | 3 | 0 | 3 | 8 |
| factors-006 | 4 | 4 | 0 | 4 | 14 |
| factors-007 | 2 | 2 | 0 | 2 | 2 |
| Total | 23 | 23 | 0 | 22 | 65 |

These are issue records, not 65 independently established doctrinal errors. Some records group several related transcription defects; others distinguish a known PDF passage locator from an unavailable printed folio. The complete page-specific wording is in the ledgers.

## Editorial result

Every factor page now has an Identity shortcut to the single Derived Synthesis, the required immediately adjacent synthesis anchor, six substantive Comparative Schema categories, and a connected explanation grounded in the page's own source entries. Sparse factors remain bounded by their short evidence. Unsupported generic liabilities were removed rather than supplemented from astrological background knowledge.

The review preserves uncommon meanings and qualifications: Admetos's raw materials and circulation; Apollon's cultural and commercial reach; Poseidon's water masses and floods; the Moon's visual/public range; Mercury's inhibited expression as well as quickness; Venus's economics and wealth; and the Vernal Point's qualification that combinations do not ensure fame. Node retains the material disagreement about life-purpose and karmic claims, with Hand's relational and joining/separating limits visible. Historical health and gender claims remain attributed.

Chiron remains a structural exception. Its six categories and synthesis explain the lack of a standalone factor chapter without inventing doctrine. The requested `structural_only: true` flag is present. The navigation owner is responsible for recognizing that flag in generated query artifacts; this factor review does not claim that generator integration was completed.

## Source preservation and verified exceptions

Seventeen Source Entries regions remain identical to the captured baseline after newline normalization. Six differ only through explicitly recorded, scan-verified repairs or verified source-locator metadata:

- Cupido: ABC `artist` corrected to `art`, checked against `Kunst`, printed p. 17 / PDF p. 7; verified rulebook PDF p. 29 locator added.
- Hades: the omitted ABC tail — disadvantage, danger, criminality, dirt — restored from the same original keyword spread; verified rulebook PDF p. 29 locator added.
- Jupiter: ABC damaged/untranslated luck and kindness wording repaired; Ebertin `Hannony`/`hannony` corrected to `Harmony`/`harmony` against printed p. 57 / PDF p. 59; Hand's truncated sentence completed only through its verified ending on PDF p. 77. The preserved Hand excerpt is explicitly located at PDF pp. 74–77, separately from the broader model section range of pp. 74–79. Remaining OCR and mixed house/sign material were retained.
- Kronos: damaged/untranslated ABC terms and the omitted closing meanings restored against printed p. 17 / PDF p. 7; verified rulebook PDF p. 29 locator added.
- Vulcanus: ABC `Strong` changed to `Strength`, and `Force` restored for `Kraft`, against the German printed p. 17 / PDF p. 7 line. The rulebook entry was personally confirmed at PDF p. 29 under Friedrich Sieggrün's subsection.
- Zeus: untranslated `Grundung` and `Schopfung` rendered as `Founding` and `Creation`, and the omitted beginning, leadership, and goal-setting terms restored against the German printed p. 17 / PDF p. 7 line. The unchanged rulebook wording was personally confirmed at PDF p. 29 under Alfred Witte's subsection.

The supervisor personally inspected the full original rulebook PDF p. 29 render and ABC PDF p. 7 spread used for the two inline repairs. Durable copies of those original-page renders are [Rules PDF p. 29](factors-original-rules-pdf29.png) and [ABC PDF p. 7](factors-original-abc-pdf7.png). Other raw-page checks and exact old/new repairs are documented by factors-002. Parser/model locators are explicitly distinguished from scan verification in the other ledgers; no printed page numbers were invented.

## Final scoped checks

The supervisor read all revised Identity, Comparative Schema, contradiction-note, Derived Synthesis, and Open Questions sections, and inspected all source-region differences against the baseline. Each owning reviewer separately inspected their full page and actual editorial diff against its local passages.

A focused check executed with `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -X utf8` passed for all 23 pages:

- Exact assignment/ledger reconciliation: 23 unique paths, 23 records, required fields present, `full_read: true`, `status: reviewed`, valid outcomes.
- Canonical identity values unchanged: title, page type, slug, framework scope, factors, aliases, and source list.
- `structural_only` present only on Chiron among the factor pages.
- All six schema categories present exactly once and nonempty.
- The interpretation shortcut occurs in Identity, and `<a id="derived-synthesis"></a>` immediately precedes `## Derived Synthesis` with no intervening blank line.
- All 434 local-fragment links and 634 relative-file links resolve, including target fragments where supplied: 1,068 checks in total.
- All 23 pages differ from their baseline; the source-region comparison identifies exactly the six verified-exception pages above.

`git diff --check -- wiki/factors` exited 0. Git emitted the repository's LF-to-CRLF conversion notices, with no whitespace errors. No whole-corpus lint, navigation regeneration, raw-vault hash audit, or rendered reader-journey gate is claimed here; those remain root integration checks.

## Remaining source problems

The 65 ledger items retain exact locators and suspicious wording. The material limitations include mixed or shifted Ebertin house/sign extracts; specific anomalous codes/pages in Asc, MC, Node, and Pluto; truncated Hand endings in several factors; a missing amount in Hand's mean/true-node comparison; and suspect ABC translations or incomplete English keyword coverage on pages where no repair was made. The new synthesis excludes damaged fragments from confident doctrine. Available PDF and chapter locators are retained even where printed folios remain unavailable.

Ledger files: `ledgers/factors-001.jsonl` through `ledgers/factors-007.jsonl`. No assigned page remains unreviewed.
