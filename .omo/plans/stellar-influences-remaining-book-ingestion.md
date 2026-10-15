# stellar-influences-remaining-book-ingestion - Work Plan

## TL;DR (For humans)

**What you'll get:** The remaining Stellar Influences book candidates will be processed source by source. Direct factor/axis material will be added to the wiki; parser-heavy or schema-mismatched sources will either get a safe importer or explicit hold evidence instead of forced entries.

**Why this approach:** The wiki already has the major Witte/Ebertin/McBroom/Munkasey plus Banzhaf/Johndro coverage, and the remaining sources split into low-risk prose, abbreviation tables, reverse lexicons, and method/case material. One-source batches avoid duplicate pages and preserve activation orientation.

**What it will NOT do:** It will not modify Stellar Craft, raw source files, create new page types, ingest timing/sign/house/degree material, expand minor-body canon, merge oriented formulas, or bulk-dump reverse lexicon text.

**Effort:** Large
**Risk:** Medium - the risk is wrong source identity mapping in OCR/glyph-heavy and reverse-lexicon sources.
**Decisions I made for you:** Process low-risk direct prose first; require parser proof before Niggemann and reverse lexicons; hold Ober/angle-only/minor-body material when it cannot map to current SI page types.

Your next move: none. This was approved by `$omo:start-work`; execution continues source by source.

---

> TL;DR (machine): Large, medium-risk, SI-only ingestion completion plan; direct prose first, parser-heavy sources guarded, one source per batch.

## Scope
### Must have
- Work only in `W:/Stellar Influences` and `.omo` evidence for this run.
- Use `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe` for all Python commands.
- Treat `W:/books references etc/!master list astro` as read-only.
- Process exactly one source at a time.
- Create or update a minimal source page first for every accepted source.
- Add only explicit factor, unordered axis, oriented activation/formula, or triad sibling/formula material to canonical wiki pages.
- Preserve source-native categories and exact PDF page references.
- Preserve activation orientation: `Sun/Moon = Venus`, `Sun/Venus = Moon`, and `Moon/Venus = Sun` are distinct.
- Run `tools/lint_wiki.py` after each accepted source batch.
- Rebuild index and query manifest after accepted batches.
- Commit verified wiki batches separately from `.omo` evidence unless the user asks otherwise.

### Must NOT have (guardrails, anti-slop, scope boundaries)
- No Stellar Craft edits.
- No raw source collection edits.
- No new page types.
- No signs, houses, degrees, fixed stars, transits, progressions, directions, timing layers, or broad method/case narrative unless directly mapped to existing SI page types.
- No minor-body canon expansion.
- No IC/DSC-only axis pages unless the factor canon is expanded first.
- No full-text book dumps or reverse-lexicon bulk dumps.
- No changes to unrelated dirty worktree files.

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after plus source-surface QA; this is markdown/wiki ingestion, not application code.
- Evidence: `.omo/evidence/task-<N>-stellar-influences-remaining-book-ingestion.md`.
- Happy path per accepted source: source page exists, canonical pages updated, PDF page refs present, lint passes.
- Failure path per source: if parser/schema fit fails, evidence records why no wiki entry was added.
- Final surface proof: `tools/rebuild_index.py`, `tools/query_manifest.py`, `tools/lint_wiki.py`, and representative manual reads from `wiki/factors`, `wiki/axes`, `wiki/activations`, and `wiki/triads`.

## Execution strategy
### Parallel execution waves
- Wave 1: Low-risk direct sources, serialized by source: Hall, Harding/Harvey, Stein.
- Wave 2: Prove-or-hold source: Aren Ober.
- Wave 3: Parser-heavy direct table source: Hans Niggemann.
- Wave 4: Reverse lexicons, serialized by source: Feist, Uranian Master-Lexicon, Baker.
- Wave 5: Final rebuild, audit, report, commit.

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 | none | 2 | read-only analysis only |
| 2 | 1 | 3 | none |
| 3 | 2 | 4 | none |
| 4 | 3 | 5 | none |
| 5 | 4 | 6 | none |
| 6 | 5 | 7 | none |
| 7 | 6 | 8 | none |
| 8 | 7 | 9 | none |
| 9 | 8 | 10 | none |
| 10 | 9 | final verification | none |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->
- [x] 1. Ingest Manly P. Hall factor keyword material
  What to do / Must NOT do: Create/update source page `wiki/sources/manly-p-hall-astrological-keywords.md` first, then add compact factor-only entries to canonical factor pages for the nine planetary types present in the source. Preserve page refs from PDF pages 104-121. Do not ingest signs, houses, occupations as standalone pages, occult septenary schema beyond source-native factor notes, or noncanonical factors.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 2
  References: `AGENTS.md`; `wiki/_templates/source.md`; `wiki/factors/*.md`; PDF `W:/books references etc/!master list astro/varia - Manly P Hall - Astrological Keywords.pdf` pages 104-121; existing committed Banzhaf/Johndro factor-entry style in `wiki/factors/sun.md`.
  Acceptance criteria: Source page lists admitted factors and skipped material; factor pages include `### Manly P. Hall - Astrological Keywords`; `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/lint_wiki.py` exits 0.
  QA scenarios: happy: read `wiki/factors/sun.md`, `wiki/factors/moon.md`, and source page to confirm page refs and compact source-native categories; failure: run an `rg` check proving no Hall entries were added under `wiki/axes`, `wiki/activations`, or `wiki/triads`. Evidence `.omo/evidence/task-1-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): ingest Hall factor keywords

- [x] 2. Ingest Harding/Harvey Sun/Moon axis material
  What to do / Must NOT do: Create/update source page for `Working with Astrology`; add only the explicit Sun/Moon midpoint doctrine from the Inner Marriage chapter to `wiki/axes/sun-moon.md`. Do not ingest harmonics, Astro*Carto*Graphy, case narrative, timing, transits, progressions, directions, or quoted Ebertin material already covered elsewhere.
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 3
  References: `AGENTS.md`; `wiki/axes/sun-moon.md`; PDF `harmonics - Michael Harding Charles Harvey - Working with astrology_harmonics, midpoints and Astro_Carto_Graphy.pdf` pages 61-80.
  Acceptance criteria: Source page records admitted Sun/Moon axis only and skipped method/case material; `wiki/axes/sun-moon.md` has a source-specific block with PDF pages; lint passes.
  QA scenarios: happy: read `wiki/axes/sun-moon.md` and confirm no activation pages changed; failure: `git diff --name-only -- wiki/activations wiki/triads` is empty after this source. Evidence `.omo/evidence/task-2-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): ingest Harding Harvey Sun Moon midpoint

- [x] 3. Ingest Zane B. Stein admissible axis material
  What to do / Must NOT do: Create/update source page for `The Quadrant Midpoints: The Chart's Backbone`; add only reusable `Sun/Moon` and `Asc/MC` axis meanings if canonical pages exist. Skip IC/DSC, DSC/MC, ASC/IC, Eris, and case activations that require noncanonical factors or angle canon expansion.
  Parallelization: Wave 1 | Blocked by: 2 | Blocks: 4
  References: `AGENTS.md`; `wiki/axes/sun-moon.md`; `wiki/axes/asc-mc.md`; PDF `midpoints - Zane B Stein The Quadrant Midpoints The Chart's Backbone.pdf` pages 2-11.
  Acceptance criteria: Source page documents admitted and skipped quadrant midpoint material; only existing axis pages are updated; lint passes.
  QA scenarios: happy: read source page plus `wiki/axes/sun-moon.md` and `wiki/axes/asc-mc.md`; failure: `rg -n "IC/DSC|DSC/MC|ASC/IC|Eris" wiki/axes wiki/activations wiki/triads` shows no new canonical doctrine entries from this batch. Evidence `.omo/evidence/task-3-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): ingest Stein quadrant midpoint axes

- [x] 4. Prove or hold Aren Ober
  What to do / Must NOT do: Inspect `midpoints - Aren Ober - Midpoint Interpretation.pdf` for standalone reusable factor/axis/activation entries. If found, process exactly those entries source page first; if not found, write hold evidence only and do not create wiki doctrine pages. Do not ingest forecasting chapters, directions, transits, timing, or case narrative.
  Parallelization: Wave 2 | Blocked by: 3 | Blocks: 5
  References: `AGENTS.md`; PDF pages around table of contents, chapters 6, 9, 11, and 12; `wiki/sources` inventory.
  Acceptance criteria: Evidence file lists inspected pages and final action; if accepted, lint passes; if held, no wiki changes remain for Ober.
  QA scenarios: happy: evidence includes at least three page snippets showing either standalone entries or method/case-only status; failure: `git diff --name-only -- wiki | rg -i "ober"` is empty when held. Evidence `.omo/evidence/task-4-stellar-influences-remaining-book-ingestion.md`.
  Commit: Conditional | docs(stellar-influences): ingest Ober midpoint entries

- [x] 5. Build and run Hans Niggemann parser-backed import
  What to do / Must NOT do: Build a source-specific parser for `midpoints - Hans Niggemann - Rules for planetary pictures.pdf` that maps abbreviations (`M`, `Ar`, `Su`, `Asc`, `No`, `Me`, `Ve`, `Ma`, `Ju`, `Sa`, `Ur`, `Ne`, `Pl`, `Cu`, `Ha`, `Ze`, `Kr`, `Ap`, `Ad`, `Vu`, `Po`) to canonical factors before editing wiki pages. Create source page first. Add source blocks to factor/axis/activation pages only when formula identity and page reference are reliable. Do not ingest OCR-broken rows or merge orientations.
  Parallelization: Wave 3 | Blocked by: 4 | Blocks: 6
  References: `AGENTS.md`; `tools/wiki_identity.py`; `tools/ingest_witte.py`; PDF pages 26-283; existing Witte-style source entries.
  Acceptance criteria: Parser emits a reviewed sample manifest before writes; skipped OCR-broken rows are counted; source page records counts; lint passes after import.
  QA scenarios: happy: sample rows include `Meridian plus Venus`, `Moon plus Saturn`, and `Poseidon plus Poseidon` mapped to canonical identities; failure: deliberately feed an unknown abbreviation fixture and prove the parser skips it without writing pages. Evidence `.omo/evidence/task-5-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): ingest Niggemann planetary pictures

- [x] 6. Build Feist reverse-lexicon decision/import
  What to do / Must NOT do: Analyze `planetary expression - Michael Feist - Lexicon for Planetary Pictures.pdf` as a reverse keyword-to-formula source. If a parser can safely map formula tokens such as `Ve+Vu-Ju` to canonical activation pages and compact keywords without dumping full text, import compact source blocks. If not, create only hold evidence and do not wiki-edit. Do not hand-enter rows.
  Parallelization: Wave 4 | Blocked by: 5 | Blocks: 7
  References: `AGENTS.md`; `tools/wiki_identity.py`; PDF pages 1-475; existing source-page style.
  Acceptance criteria: Parser or hold decision is evidence-backed; no bulk full-text dump; lint passes if wiki changes occur.
  QA scenarios: happy: parser sample maps at least five formula rows with page refs; failure: unknown token fixture is skipped and reported. Evidence `.omo/evidence/task-6-stellar-influences-remaining-book-ingestion.md`.
  Commit: Conditional | docs(stellar-influences): ingest Feist planetary picture lexicon

- [x] 7. Build Uranian Master-Lexicon reverse-lexicon decision/import
  What to do / Must NOT do: Analyze `planetary expressions - Uranian Astrology - Master-Lexicon v2_1.pdf` as a reverse lexicon. Import only if formula tokens and OCR text can be reliably mapped and compacted; otherwise hold with evidence. Do not duplicate Witte entries already present unless the source adds distinct keywords.
  Parallelization: Wave 4 | Blocked by: 6 | Blocks: 8
  References: `AGENTS.md`; PDF pages 1-409; Witte source page; Feist parser decision from todo 6.
  Acceptance criteria: Source page or hold evidence explains relation to Witte; lint passes if wiki changes occur.
  QA scenarios: happy: sample rows map with page refs and duplicate handling; failure: OCR-noisy sample is skipped rather than written. Evidence `.omo/evidence/task-7-stellar-influences-remaining-book-ingestion.md`.
  Commit: Conditional | docs(stellar-influences): ingest Uranian master lexicon

- [x] 8. Build D.M. Baker reverse/glyph lexicon decision/import
  What to do / Must NOT do: Analyze `planetary expressions - D.M. Baker - Colloquialism.pdf`. Import only if glyph/formula identities can be decoded reliably to canonical factor/axis/activation pages; otherwise hold with evidence. Do not ingest colloquialisms whose glyph mapping is uncertain.
  Parallelization: Wave 4 | Blocked by: 7 | Blocks: 9
  References: `AGENTS.md`; PDF pages 1-168; reverse-lexicon parser decisions from todos 6 and 7.
  Acceptance criteria: Evidence-backed import or hold; no uncertain glyph entries written; lint passes if wiki changes occur.
  QA scenarios: happy: sample glyph rows decode with canonical factors and page refs; failure: undecodable glyph row is skipped and counted. Evidence `.omo/evidence/task-8-stellar-influences-remaining-book-ingestion.md`.
  Commit: Conditional | docs(stellar-influences): ingest Baker colloquial planetary expressions

- [x] 9. Rebuild query surfaces and run final SI verification
  What to do / Must NOT do: Run `tools/rebuild_index.py`, `tools/query_manifest.py`, and `tools/lint_wiki.py`; inspect representative changed factor, axis, activation, and triad pages. Do not claim completion from lint alone.
  Parallelization: Wave 5 | Blocked by: 8 | Blocks: 10
  References: `AGENTS.md`; `tools/lint_wiki.py`; `tools/rebuild_index.py`; `tools/query_manifest.py`; `wiki/query-guide.md`.
  Acceptance criteria: Commands pass; representative pages retain anchors and orientation-safe links; query manifest includes new source pages.
  QA scenarios: happy: run all three commands with approved Python; failure: temporary invalid activation fixture is rejected by lint or identity logic without touching live pages. Evidence `.omo/evidence/task-9-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): rebuild query surfaces after book ingestion

- [x] 10. Final report and commit hygiene
  What to do / Must NOT do: Summarize ingested, held, skipped, and already-existing sources; list changed pages and verification; stage/commit only wiki changes for the final batch. Leave unrelated dirty worktree files untouched.
  Parallelization: Wave 5 | Blocked by: 9 | Blocks: final verification
  References: `.omo/evidence/*stellar-influences-remaining-book-ingestion.md`; `git status --short`; committed baseline `ccfbfb72`.
  Acceptance criteria: Final report exists in evidence and final wiki diff is committed or explicitly clean; unrelated dirty files remain unstaged.
  QA scenarios: happy: `git status --short -- wiki` is clean after commit; failure: `git diff --cached --name-only` contains no unrelated files before commit. Evidence `.omo/evidence/task-10-stellar-influences-remaining-book-ingestion.md`.
  Commit: Y | docs(stellar-influences): complete remaining book ingestion

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [x] F1. Plan compliance audit
- [x] F2. Code/wiki quality review
- [x] F3. Real manual QA
- [x] F4. Scope fidelity

## Commit strategy
- Commit each accepted source or tightly related batch after lint passes.
- Do not commit `.omo/evidence` unless explicitly requested; use it as local run evidence.
- Keep unrelated dirty files unstaged.
- Suggested commit sequence:
  - `docs(stellar-influences): ingest Hall factor keywords`
  - `docs(stellar-influences): ingest Harding Harvey Sun Moon midpoint`
  - `docs(stellar-influences): ingest Stein quadrant midpoint axes`
  - parser-source commits only when those imports are evidence-backed.

## Success criteria
- Every `both_split` or `stellar_influences_first` source is either already ingested, newly ingested, or evidence-held with an explicit current-schema reason.
- Every accepted source has a source page and exact PDF page refs.
- Canonical factor/axis/activation/triad pages retain required anchors and orientation-safe identities.
- Rebuilt index/query surfaces reflect the final wiki state.
- Final lint passes.

